#!/usr/bin/env python3
"""
TODO to GitHub Issues Converter

This script scans the repository for TODO, FIXME, XXX, and HACK comments
and helps convert them into GitHub issues with proper formatting and labels.
"""

import os
import re
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Optional
from collections import defaultdict


class TodoItem:
    """Represents a TODO item found in code"""
    
    def __init__(self, file_path: str, line_number: int, todo_type: str, 
                 content: str, context_lines: List[str]):
        self.file_path = file_path
        self.line_number = line_number
        self.todo_type = todo_type  # TODO, FIXME, XXX, HACK
        self.content = content.strip()
        self.context_lines = context_lines
        
    def to_dict(self) -> Dict:
        return {
            'file': self.file_path,
            'line': self.line_number,
            'type': self.todo_type,
            'content': self.content,
            'context': self.context_lines
        }
    
    def infer_area(self) -> str:
        """Infer the area label based on file path"""
        path_lower = self.file_path.lower()
        
        if 'santiago-service' in path_lower or 'santiago_service' in path_lower:
            return 'area: santiago-service'
        elif 'bdd' in path_lower or 'spec-pack' in path_lower:
            return 'area: bdd-framework'
        elif 'test' in path_lower:
            return 'area: testing'
        elif '.md' in path_lower or 'doc' in path_lower:
            return 'area: documentation'
        elif 'docker' in path_lower or 'deploy' in path_lower or '.github' in path_lower:
            return 'area: devops'
        elif 'fhir' in path_lower:
            return 'area: fhir'
        elif 'api' in path_lower or 'app.py' in path_lower:
            return 'area: api'
        else:
            return 'area: other'
    
    def infer_type(self) -> str:
        """Infer issue type from TODO type"""
        if self.todo_type in ['FIXME', 'BUG']:
            return 'type: bug'
        elif self.todo_type == 'HACK':
            return 'type: refactor'
        else:
            return 'type: task'
    
    def infer_priority(self) -> str:
        """Infer priority from TODO content"""
        content_lower = self.content.lower()
        
        if any(word in content_lower for word in ['critical', 'urgent', 'security', 'blocking']):
            return 'priority: p0-critical'
        elif any(word in content_lower for word in ['important', 'should', 'must']):
            return 'priority: p1-high'
        elif any(word in content_lower for word in ['nice', 'optional', 'later']):
            return 'priority: p3-low'
        else:
            return 'priority: p2-medium'
    
    def suggest_agent(self) -> str:
        """Suggest appropriate agent based on content"""
        content_lower = self.content.lower()
        path_lower = self.file_path.lower()
        
        # Check for clinical-related TODOs
        if any(word in content_lower or word in path_lower for word in 
               ['fhir', 'clinical', 'snomed', 'loinc', 'terminology', 'guideline']):
            return 'agent: clinical-informaticist'
        
        # Check for architecture-related TODOs
        if any(word in content_lower for word in 
               ['architecture', 'design', 'graph', 'neurosymbolic', 'knowledge']):
            return 'agent: neurosymbolic-architect'
        
        # Check for DevOps-related TODOs
        if any(word in path_lower for word in ['docker', 'deploy', '.github', 'ci', 'cd']):
            return 'agent: devops'
        
        # Check for testing-related TODOs
        if 'test' in path_lower or 'test' in content_lower:
            return 'agent: qa'
        
        # Default to development agent
        return 'agent: development'
    
    def generate_issue_title(self) -> str:
        """Generate a concise issue title"""
        # Take first sentence or first 80 chars
        title = self.content.split('.')[0].split('\n')[0]
        title = title.replace('TODO:', '').replace('FIXME:', '').strip()
        
        if len(title) > 80:
            title = title[:77] + '...'
        
        return f"[{self.todo_type}] {title}"
    
    def generate_issue_body(self) -> str:
        """Generate the full issue body"""
        body = f"""## {self.todo_type} from Code

**File:** `{self.file_path}`  
**Line:** {self.line_number}

### Description

{self.content}

### Code Context

```python
"""
        # Add context lines
        for i, line in enumerate(self.context_lines, start=self.line_number - 2):
            body += f"{i}: {line}\n"
        
        body += """```

### Suggested Implementation

_TODO: Add implementation details_

### Acceptance Criteria

- [ ] TODO comment is resolved
- [ ] Code is properly implemented and tested
- [ ] Documentation is updated if needed

### Additional Context

This issue was automatically generated from a TODO comment in the codebase.
Review the context and update the description with more details if needed.
"""
        return body


def find_todos(root_dir: str, extensions: List[str]) -> List[TodoItem]:
    """Find all TODO items in specified file types"""
    todos = []
    
    # Patterns to match
    todo_pattern = re.compile(r'#?\s*(TODO|FIXME|XXX|HACK)[\s:]+(.+?)(?=\n|$)', re.IGNORECASE)
    
    # Files to skip
    skip_dirs = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', 'dist', 'build'}
    skip_files = {'setup-labels.sh', 'convert_todos_to_issues.py'}
    
    for root, dirs, files in os.walk(root_dir):
        # Skip directories
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for file in files:
            if file in skip_files:
                continue
                
            if any(file.endswith(ext) for ext in extensions):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, root_dir)
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        
                    for i, line in enumerate(lines, start=1):
                        match = todo_pattern.search(line)
                        if match:
                            todo_type = match.group(1).upper()
                            content = match.group(2).strip()
                            
                            # Get context (2 lines before and after)
                            context_start = max(0, i - 3)
                            context_end = min(len(lines), i + 2)
                            context_lines = [lines[j].rstrip() for j in range(context_start, context_end)]
                            
                            todo_item = TodoItem(rel_path, i, todo_type, content, context_lines)
                            todos.append(todo_item)
                            
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    
    return todos


def group_todos(todos: List[TodoItem]) -> Dict[str, List[TodoItem]]:
    """Group TODOs by area"""
    grouped = defaultdict(list)
    for todo in todos:
        area = todo.infer_area()
        grouped[area].append(todo)
    return dict(grouped)


def create_github_issue(todo: TodoItem, dry_run: bool = True) -> Optional[str]:
    """Create a GitHub issue from a TODO item"""
    title = todo.generate_issue_title()
    body = todo.generate_issue_body()
    
    labels = [
        todo.infer_type(),
        'status: needs-triage',
        todo.infer_priority(),
        todo.infer_area(),
        todo.suggest_agent()
    ]
    
    if dry_run:
        print(f"\n{'='*80}")
        print(f"Would create issue:")
        print(f"Title: {title}")
        print(f"Labels: {', '.join(labels)}")
        print(f"\nBody preview:")
        print(body[:300] + "..." if len(body) > 300 else body)
        return None
    else:
        try:
            # Create issue using gh CLI
            cmd = ['gh', 'issue', 'create', 
                   '--title', title,
                   '--body', body]
            
            for label in labels:
                cmd.extend(['--label', label])
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            issue_url = result.stdout.strip()
            print(f"✅ Created issue: {issue_url}")
            return issue_url
        except subprocess.CalledProcessError as e:
            print(f"❌ Error creating issue: {e}")
            print(f"Output: {e.output}")
            return None


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Convert TODO comments to GitHub issues')
    parser.add_argument('--root', default='.', help='Root directory to scan')
    parser.add_argument('--extensions', nargs='+', 
                       default=['.py', '.js', '.ts', '.md', '.sh'],
                       help='File extensions to scan')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Show what would be created without creating issues')
    parser.add_argument('--output-json', help='Output TODOs to JSON file')
    parser.add_argument('--area', help='Only process TODOs from specific area')
    parser.add_argument('--create', action='store_true', 
                       help='Actually create GitHub issues (requires gh CLI)')
    
    args = parser.parse_args()
    
    print("🔍 Scanning for TODO comments...")
    todos = find_todos(args.root, args.extensions)
    
    print(f"\n📊 Found {len(todos)} TODO items")
    
    if args.output_json:
        with open(args.output_json, 'w') as f:
            json.dump([todo.to_dict() for todo in todos], f, indent=2)
        print(f"💾 Saved to {args.output_json}")
    
    # Group and display
    grouped = group_todos(todos)
    
    print("\n📂 TODOs by Area:")
    for area, items in sorted(grouped.items()):
        print(f"\n{area}: {len(items)} items")
        for todo in items[:3]:  # Show first 3
            print(f"  - {todo.file_path}:{todo.line_number} - {todo.content[:60]}...")
        if len(items) > 3:
            print(f"  ... and {len(items) - 3} more")
    
    # Create issues if requested
    if args.create or args.dry_run:
        print(f"\n{'='*80}")
        print("Creating GitHub Issues" if args.create else "DRY RUN - No issues will be created")
        print(f"{'='*80}")
        
        # Filter by area if specified
        todos_to_process = todos
        if args.area:
            todos_to_process = [t for t in todos if args.area in t.infer_area()]
            print(f"Processing {len(todos_to_process)} items from {args.area}")
        
        created_count = 0
        for todo in todos_to_process:
            result = create_github_issue(todo, dry_run=not args.create)
            if result:
                created_count += 1
        
        if args.create:
            print(f"\n✅ Created {created_count} issues")
        else:
            print(f"\n💡 Run with --create to actually create these {len(todos_to_process)} issues")


if __name__ == '__main__':
    main()
