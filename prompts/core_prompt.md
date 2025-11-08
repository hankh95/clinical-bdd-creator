# Core Prompt for Collaborative Development with GitHub Copilot

**Purpose:** This prompt guides GitHub Copilot's behavior during collaborative work on the Clinical BDD MCP Service project. It ensures consistent tracking, communication, and progress management.

## Key Instructions for Copilot

1. **Daily Notes Tracking:**
   - Create a new Markdown file each day in the `daily-notes/` folder (e.g., `2025-11-08.md`).
   - Update the current day's daily notes file every 2-3 hours during active work sessions.
   - Always update at stop points, major decisions, or when committing changes to Git.
   - Include in each update:
     - Tasks completed.
     - Decisions made (with rationale).
     - Challenges encountered and resolutions.
     - Next steps or blockers.

2. **Work Session Management:**
   - Start each session by reviewing the current daily notes and development plan.
   - End sessions by updating daily notes and committing changes if applicable.
   - Use Git commits for version control; commit messages should reference the daily notes date (e.g., "Update requirements per 2025-11-07 notes").

3. **Collaboration Style:**
   - Be proactive, friendly, and helpful.
   - Ask for clarification when needed, but avoid unnecessary questions.
   - Track progress using the development plan and todo lists.
   - Validate code/test changes before presenting them.

4. **Project Structure Adherence:**
   - Follow the established folder structure (e.g., spec-pack/, dev_plan/, daily-notes/, prompts/).
   - Use the development plan in `spec-pack/11-plan/` as the guiding document.
   - Record all work in daily notes for continuity across sessions or collaborators.

5. **Quality Assurance:**
   - Run tests or validations after substantive changes.
   - Fix errors immediately if possible; otherwise, note in daily notes.
   - Ensure deliverables are complete (source files, tests, docs) for non-trivial tasks.

This prompt ensures transparency and efficiency in our collaborative development process.
