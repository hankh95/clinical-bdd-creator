# GitHub Project Management - Next Steps

## Immediate Actions Required

These steps must be completed by a repository administrator to activate the GitHub project management system.

### 1. Create Labels (5 minutes)

Run the label creation script:

```bash
cd /home/runner/work/clinical-bdd-creator/clinical-bdd-creator
./scripts/setup-labels.sh
```

This will create 55 labels across 8 categories:
- Type (8 labels)
- Status (8 labels)  
- Priority (4 labels)
- Area (9 labels)
- Agent (8 labels)
- Effort (6 labels)
- Clinical (5 labels)
- Special (7 labels)

### 2. Enable GitHub Features (3 minutes)

Go to Repository Settings → Features:

- ✅ Issues (already enabled)
- ✅ Projects (already enabled)
- ⬜ **Enable Discussions**
  - Click "Set up discussions"
  - Use default categories (Announcements, Ideas, Q&A, General, Show and Tell)
  - Create welcome post
  
- ⬜ **Enable Wiki**
  - Check "Wikis" checkbox
  - Click "Save"

### 3. Configure Project Board (10 minutes)

Visit https://github.com/users/hankh95/projects/2

Create these views:

#### Board View (Default)
- Status: Backlog, Ready, In Progress, In Review, Done

#### Table View
Add columns:
- Title
- Status
- Priority
- Area
- Assigned Agent
- Effort Estimate
- Sprint

#### Roadmap View
- Group by: Milestone
- Time range: 3 months

#### Agent Assignment View
- Group by: Agent label
- Sort by: Priority

Add custom fields:
- **Sprint** (text)
- **Effort** (single select: XS, S, M, L, XL, XXL)
- **Agent** (single select: matching agent labels)

### 4. Convert TODOs to Issues (15 minutes)

Preview what will be created:
```bash
python scripts/convert_todos_to_issues.py --dry-run
```

Create issues by area:
```bash
# Santiago service TODOs (16 items)
python scripts/convert_todos_to_issues.py --create --area santiago-service

# BDD framework TODOs (35 items) - Review first, many are template placeholders
python scripts/convert_todos_to_issues.py --create --area bdd-framework

# Testing TODOs (1 item)
python scripts/convert_todos_to_issues.py --create --area testing
```

**Note**: Skip the BDD framework TODOs initially as most are template placeholders in example files.

### 5. Populate Wiki (30 minutes)

Create these initial wiki pages:

#### Home Page
```markdown
# Clinical BDD Creator Wiki

Welcome to the Clinical BDD Creator project wiki!

## Quick Links
- [Architecture Overview](Architecture-Overview)
- [Getting Started](Getting-Started)
- [Agent Specifications](Agent-Specifications)
- [Clinical Domain Guide](Clinical-Domain)

## Recent Updates
[List recent changes]
```

#### High-Priority Pages
1. **Architecture Overview** - Overview of Santiago service, BDD framework
2. **Getting Started** - Environment setup, first contribution
3. **Agent Specifications** - Detailed agent capabilities and selection guide
4. **Santiago Service Architecture** - Four-layer model, components
5. **Clinical Domain Guide** - Terminology systems, FHIR integration

See [WIKI-GUIDE.md](../WIKI-GUIDE.md) for complete structure.

### 6. Team Training (2 hours)

Conduct training session covering:

#### Session Outline
1. **Introduction** (15 min)
   - Why we're using GitHub project management
   - Overview of new system
   - Benefits for team and agents

2. **Creating Issues** (30 min)
   - Demo: Create feature request
   - Demo: Create bug report
   - Practice: Each person creates a sample issue
   - Review: BDD format for acceptance criteria

3. **Using the Project Board** (20 min)
   - Demo: Navigate different views
   - Demo: Update issue status
   - Demo: Filter and search
   - Practice: Find assigned work

4. **Agent Assignment** (15 min)
   - Explain agent system
   - When to suggest which agent
   - How agents will interact with issues

5. **GitHub Discussions and Wiki** (15 min)
   - When to use Discussions vs Issues
   - How to contribute to wiki
   - Finding information

6. **BDD Best Practices** (15 min)
   - Review BDD-PROJECT-MANAGEMENT.md
   - Examples of good user stories
   - Examples of good acceptance criteria

7. **Q&A** (10 min)

#### Training Materials
- [PROJECT-MANAGEMENT.md](../PROJECT-MANAGEMENT.md) - Full guide
- [BDD-PROJECT-MANAGEMENT.md](../BDD-PROJECT-MANAGEMENT.md) - BDD practices
- [GITHUB-PROJECT-SETUP.md](../GITHUB-PROJECT-SETUP.md) - Setup guide

### 7. Initial Migration (1 hour)

Move these from daily-notes to appropriate places:

#### To Wiki
- Architecture decisions
- Research findings
- Best practices learned
- Troubleshooting tips

#### To Discussions
- Open questions
- Ideas for future features
- General project updates

#### To Issues
- Action items from daily notes
- Planned work items
- Known bugs/improvements

## Timeline

| Task | Duration | Responsible | Priority |
|------|----------|-------------|----------|
| Create labels | 5 min | Admin | High |
| Enable Discussions/Wiki | 3 min | Admin | High |
| Configure project board | 10 min | Admin/PM | High |
| Convert TODOs | 15 min | Admin/Dev | Medium |
| Populate wiki | 30 min | Team | Medium |
| Team training | 2 hours | PM | High |
| Initial migration | 1 hour | Team | Low |
| **Total** | **~4 hours** | | |

## Success Criteria

After completing these steps:

- [ ] All 55 labels are created and visible in the repository
- [ ] GitHub Discussions is enabled with 5 categories
- [ ] GitHub Wiki is enabled with Home page created
- [ ] Project board has 4 views configured (Board, Table, Roadmap, Agent)
- [ ] At least 17 issues created from TODOs (santiago-service + testing)
- [ ] At least 5 wiki pages created
- [ ] All team members have completed training
- [ ] First sprint planned using new system
- [ ] Team feedback collected

## Rollback Plan

If the new system isn't working:

1. **Preserve data**:
   ```bash
   gh issue list --state all --json number,title,body,labels > issues-backup.json
   ```

2. **Export project board**:
   - Export as CSV from project board

3. **Archive issues**:
   - Close all issues with "Archived" label
   - Keep for reference

4. **Return to previous system**:
   - Continue using daily-notes for tracking
   - Keep documentation for future retry

## Monitoring

Track these metrics weekly:

- Number of issues created/closed
- Project board activity (views, updates)
- Discussion posts
- Wiki page views and edits
- Label usage distribution
- Agent assignment distribution

## Support During Transition

### Week 1-2
- Daily standup to address questions
- Quick reference guide available
- PM available for troubleshooting
- Practice creating issues together

### Week 3-4
- Reduce to 3x/week check-ins
- Gather feedback in retrospective
- Adjust processes as needed
- Celebrate quick wins

### Month 2+
- Monthly review of metrics
- Quarterly process improvements
- Continue gathering feedback
- Scale successful patterns

## Common Questions

**Q: Do we still use daily-notes?**
A: Yes! Daily notes remain for session logs and working notes. Wiki is for knowledge that should be preserved and shared.

**Q: What if I don't know which agent to suggest?**
A: Leave it blank or select "Development Agent" as default. The PM can reassign during triage.

**Q: How do I know if something should be an Issue or a Discussion?**
A: Issue = specific task with clear done state. Discussion = open-ended question or idea exploration.

**Q: Can I edit issue templates?**
A: Yes! Templates are in `.github/ISSUE_TEMPLATE/`. Suggest changes via PR.

**Q: What if the project board gets too crowded?**
A: Use filters and views. Create sprint-specific views. Archive completed work regularly.

## Resources

### Documentation
- [PROJECT-MANAGEMENT.md](../PROJECT-MANAGEMENT.md) - Complete guide (11KB)
- [BDD-PROJECT-MANAGEMENT.md](../BDD-PROJECT-MANAGEMENT.md) - BDD practices (12KB)
- [LABELS.md](../LABELS.md) - Label reference (10KB)
- [WIKI-GUIDE.md](../WIKI-GUIDE.md) - Wiki structure (9KB)
- [GITHUB-PROJECT-SETUP.md](../GITHUB-PROJECT-SETUP.md) - Setup guide (12KB)

### Scripts
- `scripts/setup-labels.sh` - Create all labels
- `scripts/convert_todos_to_issues.py` - Convert TODOs to issues

### External Resources
- [GitHub Issues Guide](https://docs.github.com/en/issues)
- [GitHub Projects Guide](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [GitHub Discussions Guide](https://docs.github.com/en/discussions)
- [GitHub Wiki Guide](https://docs.github.com/en/communities/documenting-your-project-with-wikis)

## Contact

**Questions or Issues?**
- Create an issue: https://github.com/hankh95/clinical-bdd-creator/issues/new/choose
- Start a discussion: https://github.com/hankh95/clinical-bdd-creator/discussions
- Contact: @hankh95

---

**Version**: 1.0  
**Date**: 2025-11-11  
**Status**: Ready for execution
