#!/usr/bin/env python3
"""
GitHub Copilot Agent Task Monitor

A flexible monitoring system for tracking progress of any GitHub Copilot agent task.
Provides real-time progress updates, status tracking, and GitHub issue integration.

Usage:
    python task_monitor.py create --title "Task Title" --description "Task Description"
    python task_monitor.py update <task_id> --status "in-progress" --progress "50%" --message "Current status"
    python task_monitor.py list
    python task_monitor.py show <task_id>
"""

import json
import sys
import os
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
import uuid

@dataclass
class TaskStep:
    """Individual step within a task"""
    id: str
    title: str
    description: str
    status: str  # not-started, in-progress, completed, blocked
    progress_percentage: int
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    notes: Optional[List[str]] = None
    dependencies: Optional[List[str]] = None

    def __post_init__(self):
        if self.notes is None:
            self.notes = []
        if self.dependencies is None:
            self.dependencies = []

@dataclass
class Task:
    """GitHub Copilot Agent Task"""
    id: str
    title: str
    description: str
    status: str  # not-started, in-progress, completed, blocked, cancelled
    priority: str  # low, medium, high, critical
    created_at: str
    updated_at: str
    github_issue_number: Optional[int] = None
    steps: Optional[List[TaskStep]] = None
    tags: Optional[List[str]] = None
    assignee: Optional[str] = None
    estimated_hours: Optional[float] = None
    actual_hours: Optional[float] = None
    progress_percentage: int = 0
    current_step: Optional[str] = None
    recent_activity: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if self.steps is None:
            self.steps = []
        if self.tags is None:
            self.tags = []
        if self.recent_activity is None:
            self.recent_activity = []
        if self.metadata is None:
            self.metadata = {}

class TaskMonitor:
    """Monitor for GitHub Copilot Agent tasks"""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.tasks_dir = self.project_root / "generated" / "task-monitoring"
        self.tasks_dir.mkdir(parents=True, exist_ok=True)
        self.tasks_file = self.tasks_dir / "tasks.json"

        # Load existing tasks
        self.tasks = self.load_tasks()

    def load_tasks(self) -> Dict[str, Task]:
        """Load tasks from storage"""
        if not self.tasks_file.exists():
            return {}

        try:
            with open(self.tasks_file, 'r') as f:
                data = json.load(f)
                tasks = {}
                for task_id, task_data in data.items():
                    # Convert step dictionaries back to TaskStep objects
                    steps = []
                    for step_data in task_data.get('steps', []):
                        steps.append(TaskStep(**step_data))
                    task_data['steps'] = steps
                    tasks[task_id] = Task(**task_data)
                return tasks
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Warning: Could not load tasks file: {e}")
            return {}

    def save_tasks(self):
        """Save tasks to storage"""
        data = {}
        for task_id, task in self.tasks.items():
            task_dict = asdict(task)
            # Convert datetime objects to strings
            for step in task_dict['steps']:
                if step['started_at']:
                    step['started_at'] = str(step['started_at'])
                if step['completed_at']:
                    step['completed_at'] = str(step['completed_at'])
            data[task_id] = task_dict

        with open(self.tasks_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)

    def create_task(self, title: str, description: str, priority: str = "medium",
                   tags: Optional[List[str]] = None, estimated_hours: Optional[float] = None) -> str:
        """Create a new task"""
        task_id = str(uuid.uuid4())[:8]

        task = Task(
            id=task_id,
            title=title,
            description=description,
            status="not-started",
            priority=priority,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            tags=tags or [],
            estimated_hours=estimated_hours,
            recent_activity=[f"Task created: {datetime.now().isoformat()}"]
        )

        self.tasks[task_id] = task
        self.save_tasks()

        # Create GitHub issue
        issue_number = self.create_github_issue(task)
        if issue_number:
            task.github_issue_number = issue_number
            self.save_tasks()

        return task_id

    def create_github_issue(self, task: Task) -> Optional[int]:
        """Create a GitHub issue for the task"""
        try:
            # Create issue body
            body = self.generate_issue_body(task)

            # Use gh CLI to create issue
            cmd = [
                "gh", "issue", "create",
                "--title", f"🤖 {task.title}",
                "--body", body,
                "--label", f"copilot-agent,{task.priority}"
            ]

            if task.tags:
                for tag in task.tags:
                    cmd.extend(["--label", tag])

            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)

            if result.returncode == 0:
                # Extract issue number from output
                output_lines = result.stdout.strip().split('\n')
                for line in output_lines:
                    if line.startswith('https://github.com/'):
                        # Extract issue number from URL
                        parts = line.split('/')
                        if len(parts) >= 7 and parts[6].isdigit():
                            return int(parts[6])

            print(f"Warning: Could not create GitHub issue: {result.stderr}")
            return None

        except Exception as e:
            print(f"Error creating GitHub issue: {e}")
            return None

    def generate_issue_body(self, task: Task) -> str:
        """Generate GitHub issue body for task"""
        body = f"""## 🤖 GitHub Copilot Agent Task

**Task ID**: `{task.id}`
**Priority**: {task.priority.title()}
**Status**: {task.status.replace('-', ' ').title()}
**Created**: {task.created_at}

### 📋 Description
{task.description}

### 📊 Progress
**Overall Progress**: {task.progress_percentage}%
"""

        if task.estimated_hours:
            body += f"**Estimated Hours**: {task.estimated_hours}\n"

        if task.current_step:
            body += f"**Current Step**: {task.current_step}\n"

        if task.steps:
            body += "\n### 🏗️ Task Steps\n"
            for step in task.steps:
                status_emoji = {
                    "not-started": "⏳",
                    "in-progress": "🔄",
                    "completed": "✅",
                    "blocked": "🚫"
                }.get(step.status, "❓")

                body += f"- {status_emoji} **{step.title}** ({step.progress_percentage}%)\n"
                if step.status == "in-progress":
                    body += f"  - Currently working on this step\n"
                elif step.status == "completed":
                    body += f"  - Completed: {step.completed_at}\n"

        if task.recent_activity:
            body += "\n### 📝 Recent Activity\n"
            for activity in task.recent_activity[-5:]:  # Last 5 activities
                body += f"- {activity}\n"

        if task.tags:
            body += "\n### 🏷️ Tags\n"
            for tag in task.tags:
                body += f"- `{tag}`\n"

        body += "\n---\n\n**Monitored by GitHub Copilot Agent Task Monitor** 🤖"

        return body

    def update_task(self, task_id: str, status: Optional[str] = None, progress: Optional[int] = None,
                   message: Optional[str] = None, current_step: Optional[str] = None) -> bool:
        """Update task progress"""
        if task_id not in self.tasks:
            print(f"Error: Task {task_id} not found")
            return False

        task = self.tasks[task_id]
        updated = False

        if status and status != task.status:
            task.status = status
            if task.recent_activity is not None:
                task.recent_activity.append(f"Status changed to {status}: {datetime.now().isoformat()}")
            updated = True

        if progress is not None and progress != task.progress_percentage:
            task.progress_percentage = progress
            if task.recent_activity is not None:
                task.recent_activity.append(f"Progress updated to {progress}%: {datetime.now().isoformat()}")
            updated = True

        if current_step and current_step != task.current_step:
            task.current_step = current_step
            if task.recent_activity is not None:
                task.recent_activity.append(f"Now working on: {current_step}: {datetime.now().isoformat()}")
            updated = True

        if message:
            if task.recent_activity is not None:
                task.recent_activity.append(f"{message}: {datetime.now().isoformat()}")
            updated = True

        if updated:
            task.updated_at = datetime.now().isoformat()
            self.save_tasks()

            # Update GitHub issue
            if task.github_issue_number:
                self.update_github_issue(task)

        return updated

    def update_github_issue(self, task: Task):
        """Update GitHub issue with latest task information"""
        try:
            body = self.generate_issue_body(task)

            cmd = [
                "gh", "issue", "edit", str(task.github_issue_number),
                "--body", body
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)

            if result.returncode != 0:
                print(f"Warning: Could not update GitHub issue: {result.stderr}")

        except Exception as e:
            print(f"Error updating GitHub issue: {e}")

    def add_step(self, task_id: str, title: str, description: str,
                dependencies: Optional[List[str]] = None) -> bool:
        """Add a step to a task"""
        if task_id not in self.tasks:
            print(f"Error: Task {task_id} not found")
            return False

        task = self.tasks[task_id]
        step_id = f"{task_id}-{len(task.steps or []) + 1}"

        step = TaskStep(
            id=step_id,
            title=title,
            description=description,
            status="not-started",
            progress_percentage=0,
            dependencies=dependencies or []
        )

        task.steps = task.steps or []
        task.steps.append(step)
        task.recent_activity = task.recent_activity or []
        task.recent_activity.append(f"Added step: {title}: {datetime.now().isoformat()}")
        task.updated_at = datetime.now().isoformat()

        self.save_tasks()

        # Update GitHub issue
        if task.github_issue_number:
            self.update_github_issue(task)

        return True

    def update_step(self, task_id: str, step_id: str, status: Optional[str] = None,
                   progress: Optional[int] = None, notes: Optional[str] = None) -> bool:
        """Update a task step"""
        if task_id not in self.tasks:
            print(f"Error: Task {task_id} not found")
            return False

        task = self.tasks[task_id]
        task.steps = task.steps or []
        step = None

        for s in task.steps:
            if s.id == step_id:
                step = s
                break

        if not step:
            print(f"Error: Step {step_id} not found in task {task_id}")
            return False

        updated = False

        if status and status != step.status:
            step.status = status
            if status == "in-progress" and not step.started_at:
                step.started_at = datetime.now().isoformat()
            elif status == "completed" and not step.completed_at:
                step.completed_at = datetime.now().isoformat()
            updated = True

        if progress is not None and progress != step.progress_percentage:
            step.progress_percentage = progress
            updated = True

        if notes:
            step.notes = step.notes or []
            step.notes.append(f"{notes}: {datetime.now().isoformat()}")
            updated = True

        if updated:
            task.updated_at = datetime.now().isoformat()
            # Recalculate overall task progress
            task.steps = task.steps or []
            completed_steps = sum(1 for s in task.steps if s.status == "completed")
            task.progress_percentage = int((completed_steps / len(task.steps)) * 100) if task.steps else 0

            self.save_tasks()

            # Update GitHub issue
            if task.github_issue_number:
                self.update_github_issue(task)

        return updated

    def list_tasks(self, status_filter: Optional[str] = None) -> List[Task]:
        """List tasks with optional status filter"""
        tasks = list(self.tasks.values())

        if status_filter:
            tasks = [t for t in tasks if t.status == status_filter]

        # Sort by priority and creation date
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        tasks.sort(key=lambda t: (priority_order.get(t.priority, 4), t.created_at))

        return tasks

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a specific task"""
        return self.tasks.get(task_id)

    def generate_report(self, task_id: str) -> str:
        """Generate a detailed report for a task"""
        task = self.get_task(task_id)
        if not task:
            return f"Task {task_id} not found"

        report = []
        report.append(f"🤖 TASK REPORT: {task.title}")
        report.append("=" * 60)
        report.append(f"Task ID: {task.id}")
        report.append(f"Status: {task.status.title()}")
        report.append(f"Priority: {task.priority.title()}")
        report.append(f"Progress: {task.progress_percentage}%")
        report.append(f"Created: {task.created_at}")
        report.append(f"Updated: {task.updated_at}")

        if task.github_issue_number:
            report.append(f"GitHub Issue: #{task.github_issue_number}")

        if task.estimated_hours:
            report.append(f"Estimated Hours: {task.estimated_hours}")

        if task.actual_hours:
            report.append(f"Actual Hours: {task.actual_hours}")

        if task.assignee:
            report.append(f"Assignee: {task.assignee}")

        if task.tags:
            report.append(f"Tags: {', '.join(task.tags)}")

        if task.current_step:
            report.append(f"Current Step: {task.current_step}")

        if task.description:
            report.append("")
            report.append("DESCRIPTION:")
            report.append("-" * 20)
            report.append(task.description)

        if task.steps:
            report.append("")
            report.append("TASK STEPS:")
            report.append("-" * 20)
            for i, step in enumerate(task.steps, 1):
                status_emoji = {
                    "not-started": "⏳",
                    "in-progress": "🔄",
                    "completed": "✅",
                    "blocked": "🚫"
                }.get(step.status, "❓")

                report.append(f"{i}. {status_emoji} {step.title} ({step.progress_percentage}%)")
                report.append(f"   Status: {step.status.replace('-', ' ').title()}")

                if step.started_at:
                    report.append(f"   Started: {step.started_at}")
                if step.completed_at:
                    report.append(f"   Completed: {step.completed_at}")

                if step.notes:
                    report.append("   Notes:")
                    for note in step.notes[-3:]:  # Last 3 notes
                        report.append(f"   - {note}")

                if step.dependencies:
                    report.append(f"   Dependencies: {', '.join(step.dependencies)}")

                report.append("")

        if task.recent_activity:
            report.append("RECENT ACTIVITY:")
            report.append("-" * 20)
            for activity in task.recent_activity[-10:]:  # Last 10 activities
                report.append(f"• {activity}")

        return "\n".join(report)

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description="GitHub Copilot Agent Task Monitor")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Create task
    create_parser = subparsers.add_parser("create", help="Create a new task")
    create_parser.add_argument("--title", required=True, help="Task title")
    create_parser.add_argument("--description", required=True, help="Task description")
    create_parser.add_argument("--priority", choices=["low", "medium", "high", "critical"], default="medium")
    create_parser.add_argument("--tags", help="Comma-separated tags")
    create_parser.add_argument("--estimated-hours", type=float, help="Estimated hours")

    # Update task
    update_parser = subparsers.add_parser("update", help="Update task progress")
    update_parser.add_argument("task_id", help="Task ID")
    update_parser.add_argument("--status", choices=["not-started", "in-progress", "completed", "blocked", "cancelled"])
    update_parser.add_argument("--progress", type=int, help="Progress percentage (0-100)")
    update_parser.add_argument("--message", help="Activity message")
    update_parser.add_argument("--current-step", help="Current step being worked on")

    # Add step
    add_step_parser = subparsers.add_parser("add-step", help="Add a step to a task")
    add_step_parser.add_argument("task_id", help="Task ID")
    add_step_parser.add_argument("--title", required=True, help="Step title")
    add_step_parser.add_argument("--description", required=True, help="Step description")
    add_step_parser.add_argument("--dependencies", help="Comma-separated dependency step IDs")

    # Update step
    update_step_parser = subparsers.add_parser("update-step", help="Update a task step")
    update_step_parser.add_argument("task_id", help="Task ID")
    update_step_parser.add_argument("step_id", help="Step ID")
    update_step_parser.add_argument("--status", choices=["not-started", "in-progress", "completed", "blocked"])
    update_step_parser.add_argument("--progress", type=int, help="Progress percentage (0-100)")
    update_step_parser.add_argument("--notes", help="Add notes to the step")

    # List tasks
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("--status", choices=["not-started", "in-progress", "completed", "blocked", "cancelled"],
                           help="Filter by status")

    # Show task
    show_parser = subparsers.add_parser("show", help="Show task details")
    show_parser.add_argument("task_id", help="Task ID")
    show_parser.add_argument("--report", action="store_true", help="Generate detailed report")

    args = parser.parse_args()

    monitor = TaskMonitor()

    if args.command == "create":
        tags = args.tags.split(',') if args.tags else []
        task_id = monitor.create_task(
            title=args.title,
            description=args.description,
            priority=args.priority,
            tags=tags,
            estimated_hours=args.estimated_hours
        )
        print(f"✅ Created task: {task_id}")
        task = monitor.get_task(task_id)
        if task and task.github_issue_number:
            print(f"📋 GitHub issue: #{task.github_issue_number}")

    elif args.command == "update":
        if monitor.update_task(
            task_id=args.task_id,
            status=args.status,
            progress=args.progress,
            message=args.message,
            current_step=args.current_step
        ):
            print(f"✅ Updated task: {args.task_id}")
        else:
            print(f"❌ Failed to update task: {args.task_id}")

    elif args.command == "add-step":
        dependencies = args.dependencies.split(',') if args.dependencies else []
        if monitor.add_step(
            task_id=args.task_id,
            title=args.title,
            description=args.description,
            dependencies=dependencies
        ):
            print(f"✅ Added step to task: {args.task_id}")
        else:
            print(f"❌ Failed to add step to task: {args.task_id}")

    elif args.command == "update-step":
        if monitor.update_step(
            task_id=args.task_id,
            step_id=args.step_id,
            status=args.status,
            progress=args.progress,
            notes=args.notes
        ):
            print(f"✅ Updated step: {args.step_id}")
        else:
            print(f"❌ Failed to update step: {args.step_id}")

    elif args.command == "list":
        tasks = monitor.list_tasks(args.status)
        if not tasks:
            print("No tasks found")
            return

        print("🤖 GitHub Copilot Agent Tasks")
        print("=" * 50)
        for task in tasks:
            status_emoji = {
                "not-started": "⏳",
                "in-progress": "🔄",
                "completed": "✅",
                "blocked": "🚫",
                "cancelled": "❌"
            }.get(task.status, "❓")

            priority_emoji = {
                "critical": "🔴",
                "high": "🟠",
                "medium": "🟡",
                "low": "🟢"
            }.get(task.priority, "⚪")

            issue_info = f" (#{task.github_issue_number})" if task.github_issue_number else ""

            print(f"{status_emoji} {priority_emoji} {task.id}: {task.title} [{task.progress_percentage}%]{issue_info}")
            print(f"   Status: {task.status.replace('-', ' ').title()} | Created: {task.created_at[:10]}")

            if task.current_step:
                print(f"   Current: {task.current_step}")

            if task.tags:
                print(f"   Tags: {', '.join(task.tags)}")

            print()

    elif args.command == "show":
        task = monitor.get_task(args.task_id)
        if not task:
            print(f"❌ Task not found: {args.task_id}")
            return

        if args.report:
            print(monitor.generate_report(args.task_id))
        else:
            # Brief summary
            print(f"🤖 Task: {task.title}")
            print(f"ID: {task.id}")
            print(f"Status: {task.status.title()}")
            print(f"Progress: {task.progress_percentage}%")
            print(f"Priority: {task.priority.title()}")

            if task.github_issue_number:
                print(f"GitHub Issue: #{task.github_issue_number}")

            if task.description:
                print(f"\nDescription: {task.description}")

            if task.steps:
                print(f"\nSteps ({len(task.steps)}):")
                for step in task.steps:
                    status_emoji = {
                        "not-started": "⏳",
                        "in-progress": "🔄",
                        "completed": "✅",
                        "blocked": "🚫"
                    }.get(step.status, "❓")
                    print(f"  {status_emoji} {step.title} ({step.progress_percentage}%)")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()