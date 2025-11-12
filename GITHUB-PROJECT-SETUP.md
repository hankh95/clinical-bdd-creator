# GitHub Project Management Setup

## Overview

This directory contains the complete GitHub project management infrastructure for the Clinical BDD Creator project. The setup enables effective collaboration between human developers and AI agents using GitHub's native tools.

## Quick Start

### For Team Members

1. **Read the guides**:
   - [PROJECT-MANAGEMENT.md](PROJECT-MANAGEMENT.md) - Complete project management guide
   - [BDD-PROJECT-MANAGEMENT.md](BDD-PROJECT-MANAGEMENT.md) - BDD best practices
   - [LABELS.md](LABELS.md) - Label system documentation

2. **Create your first issue**:
   - Go to [Issues](https://github.com/hankh95/clinical-bdd-creator/issues)
   - Click "New Issue"
   - Choose appropriate template
   - Fill in BDD-style acceptance criteria

3. **View the project board**:
   - Visit [Project Board](https://github.com/users/hankh95/projects/2)
   - See current work and priorities
   - Track your assigned tasks

### For Repository Administrators

1. **Enable GitHub features**:
   ```bash
   # Enable Issues (should already be enabled)
   # Enable Projects (should already be enabled)
   # Enable Discussions
   # Enable Wiki
   ```

2. **Set up labels**:
   ```bash
   cd scripts
   ./setup-labels.sh
   ```

3. **Configure project board**:
   - Create views (Board, Table, Roadmap, Agent Assignment)
   - Set up custom fields
   - Configure automation rules

4. **Enable workflows**:
   - Workflows in `.github/workflows/` will auto-run
   - Verify actions are enabled in repository settings

## What's Included

### Issue Templates

Located in `.github/ISSUE_TEMPLATE/`:

- **feature.yml** - Feature request template with BDD format
- **bug.yml** - Bug report template with expected/actual behavior
- **task.yml** - Development task template
- **documentation.yml** - Documentation improvement template
- **config.yml** - Template configuration and links

Each template includes:
- BDD-style acceptance criteria fields
- Agent assignment suggestions
- Priority and area selection
- Clinical safety considerations (where applicable)

### Workflows

Located in `.github/workflows/`:

- **auto-add-to-project.yml** - Automatically adds new issues/PRs to project board
- **auto-label.yml** - Automatically labels issues/PRs based on file paths
- **stale.yml** - Manages stale issues (marks after 60 days, closes after 7 more)

### Documentation

- **PROJECT-MANAGEMENT.md** - Comprehensive project management guide
  - Issue creation and management
  - Agent assignment system
  - Label system
  - BDD best practices
  - Sprint planning and ceremonies
  - Wiki usage guide

- **BDD-PROJECT-MANAGEMENT.md** - BDD practices for project management
  - User story format
  - Acceptance criteria patterns
  - Scenario templates
  - Clinical validation scenarios
  - Agent collaboration patterns

- **LABELS.md** - Complete label documentation
  - All label categories and descriptions
  - Label creation script
  - Usage guidelines
  - Color coding reference

- **WIKI-GUIDE.md** - GitHub Wiki structure guide
  - Proposed wiki structure
  - Migration strategy
  - Content guidelines
  - Wiki vs documentation decisions

### Scripts

Located in `scripts/`:

- **setup-labels.sh** - Creates all GitHub labels
  ```bash
  ./scripts/setup-labels.sh
  ```

- **convert_todos_to_issues.py** - Converts TODO comments to issues
  ```bash
  # Dry run to see what would be created
  python scripts/convert_todos_to_issues.py --dry-run
  
  # Actually create issues
  python scripts/convert_todos_to_issues.py --create
  
  # Create issues for specific area only
  python scripts/convert_todos_to_issues.py --create --area santiago-service
  
  # Export TODOs to JSON
  python scripts/convert_todos_to_issues.py --output-json todos.json
  ```

### Label System

The project uses a comprehensive label system:

#### Categories
- **Type** (8 labels): feature, bug, task, documentation, refactor, security, performance, test
- **Status** (8 labels): needs-triage, planned, in-progress, blocked, review, stale, wont-fix, duplicate
- **Priority** (4 labels): p0-critical, p1-high, p2-medium, p3-low
- **Area** (9 labels): santiago-service, bdd-framework, testing, documentation, devops, clinical-knowledge, api, mcp, fhir
- **Agent** (8 labels): human, development, clinical-informaticist, neurosymbolic-architect, qa, product-manager, devops, monetization
- **Effort** (6 labels): xs, s, m, l, xl, xxl
- **Clinical** (5 labels): safety-critical, accuracy-required, evidence-based, fhir-compliant, terminology
- **Special** (7 labels): good first issue, help wanted, keep-open, breaking-change, needs-discussion, experiment, technical-debt

**Total: 55 labels**

## Agent Assignment System

The project supports a hybrid human-AI team:

### Available Agents

| Agent | Expertise | Use For |
|-------|-----------|---------|
| 👤 Human Developer | All areas | Complex decisions, architecture, clinical safety |
| 🤖 Development Agent | General coding | Standard development tasks |
| 🏥 Clinical Informaticist | Clinical domain | Clinical workflows, terminology, validation |
| 🧬 NeuroSymbolic Architect | Advanced AI | Knowledge graphs, reasoning, architecture |
| ✅ Clinical Knowledge QA | Quality + Clinical | Testing clinical accuracy, validation |
| 📊 Product Manager | Product strategy | Requirements, hypotheses, prioritization |
| 🔧 DevOps Expert | Infrastructure | CI/CD, deployment, monitoring |
| 💰 Monetization Expert | Business model | Revenue, pricing, business strategy |

### How to Assign Agents

1. **In Issue Templates**: Select suggested agents from dropdown
2. **Manual Labeling**: Add `agent: [agent-name]` label
3. **In Comments**: Mention the need for specific agent expertise

## BDD Best Practices

### User Story Format

```gherkin
As a [role]
I want [feature]
So that [benefit]
```

### Acceptance Criteria Format

```gherkin
Given [initial context]
When [action occurs]
Then [expected outcome]
```

### Example

```gherkin
As a clinical researcher
I want to query the knowledge graph for drug interactions
So that I can validate clinical decision support logic

Given a patient with multiple medications
When I query for potential drug interactions
Then the system should return all known interactions
And the system should cite clinical evidence
And the response should include severity ratings
```

## Project Board Views

The project board at https://github.com/users/hankh95/projects/2 has multiple views:

### Board View
Kanban-style columns:
- Backlog
- Ready
- In Progress
- In Review
- Done

### Table View
Spreadsheet with columns:
- Title, Status, Priority, Area, Agent, Effort, Sprint

### Roadmap View
Timeline showing:
- Milestones
- Epics
- Release planning

### Agent Assignment View
Grouped by assigned agent for workload visibility

## GitHub Discussions

Use [Discussions](https://github.com/hankh95/clinical-bdd-creator/discussions) for:

- **Announcements**: Project updates and releases
- **Ideas**: Brainstorming before creating issues
- **Q&A**: Questions and answers
- **General**: Open-ended discussions
- **Show and Tell**: Demos and showcases

## GitHub Wiki

The [Wiki](https://github.com/hankh95/clinical-bdd-creator/wiki) contains:

- Architecture documentation
- Clinical domain knowledge
- Integration guides
- Agent collaboration patterns
- Troubleshooting guides
- Research findings

See [WIKI-GUIDE.md](WIKI-GUIDE.md) for the proposed structure.

## Automation

### Auto-add to Project
New issues and PRs are automatically added to the project board.

### Auto-labeling
Issues and PRs are automatically labeled based on file paths:
- `santiago-service/` → `area: santiago-service`
- `examples/bdd-tests/` → `area: bdd-framework`
- `*test*.py` → `area: testing`
- `*.md` → `area: documentation`
- `.github/` → `area: devops`

### Stale Management
Issues inactive for 60 days are marked stale and closed after 7 more days (unless marked with `keep-open` label).

## Converting TODOs to Issues

The repository contains TODO comments that should be converted to issues:

```bash
# See what TODOs exist
python scripts/convert_todos_to_issues.py --dry-run

# Create issues from TODOs
python scripts/convert_todos_to_issues.py --create

# Process specific area
python scripts/convert_todos_to_issues.py --create --area santiago-service
```

## Sprint Planning

### Sprint Cadence
- **Duration**: 2 weeks
- **Planning**: Every other Monday
- **Review**: Every other Friday
- **Retrospective**: After review

### Sprint Process
1. Review backlog (Product Manager)
2. Prioritize issues (Team + PM)
3. Assign agents (Technical Lead)
4. Estimate effort (Assigned agent/human)
5. Commit to sprint (Team)

## Clinical Safety

For issues involving clinical decision support:

### Required Checks
- [ ] Clinical accuracy validation
- [ ] Evidence-based rationale documented
- [ ] Safety implications reviewed
- [ ] FHIR compliance verified
- [ ] Terminology standards followed

### Labels to Use
- `clinical: safety-critical` - Affects patient safety
- `clinical: accuracy-required` - Requires clinical validation
- `clinical: evidence-based` - Follows evidence-based guidelines
- `clinical: fhir-compliant` - Must comply with FHIR standards
- `clinical: terminology` - Involves clinical terminology

## Getting Help

### Resources
- Read [PROJECT-MANAGEMENT.md](PROJECT-MANAGEMENT.md) for detailed guidance
- Check [BDD-PROJECT-MANAGEMENT.md](BDD-PROJECT-MANAGEMENT.md) for BDD practices
- Review [LABELS.md](LABELS.md) for label usage
- See [WIKI-GUIDE.md](WIKI-GUIDE.md) for wiki structure

### Support
- **Questions**: Use GitHub Discussions Q&A
- **Issues**: Comment on the relevant issue or PR
- **Urgent**: Mention @hankh95

## Implementation Status

- [x] Issue templates created with BDD format
- [x] Workflow automations configured
- [x] Label system documented
- [x] Scripts for setup and TODO conversion
- [x] Comprehensive documentation
- [ ] Labels created in repository (run `scripts/setup-labels.sh`)
- [ ] GitHub Discussions enabled
- [ ] GitHub Wiki enabled and structured
- [ ] TODOs converted to issues (run `scripts/convert_todos_to_issues.py`)
- [ ] Project board views configured
- [ ] Team training completed

## Next Steps

1. **Administrator Setup** (1-2 hours):
   - Run `scripts/setup-labels.sh` to create labels
   - Enable Discussions in repository settings
   - Enable Wiki in repository settings
   - Configure project board views

2. **Content Migration** (2-4 hours):
   - Run TODO converter to create initial issues
   - Populate wiki with key documentation
   - Create initial discussion topics

3. **Team Onboarding** (2 hours):
   - Team training session on new system
   - Practice creating issues
   - Review BDD best practices

4. **Adoption** (Ongoing):
   - Start using issues for all new work
   - Participate in discussions
   - Update wiki with learnings
   - Refine processes based on feedback

## Success Metrics

Track these to measure adoption and effectiveness:

### Adoption Metrics
- % of work tracked in Issues
- Daily project board engagement
- Discussion participation rate
- Wiki page views and edits

### Efficiency Metrics
- Cycle time (issue creation to closure)
- Issue churn rate
- BDD scenario coverage
- Agent utilization balance

### Quality Metrics
- Issue description completeness
- Proper use of BDD format
- Clinical validation coverage
- Documentation quality scores

## Contributing

When contributing to the project:

1. **Create an issue** using appropriate template
2. **Use BDD format** for acceptance criteria
3. **Select appropriate agent** if you have a suggestion
4. **Apply labels** (type, priority, area minimum)
5. **Link related issues** using #issue-number
6. **Update status** as you work
7. **Participate in discussions** for complex topics

## Continuous Improvement

This project management system will evolve based on:
- Team feedback in retrospectives
- Metrics analysis
- New GitHub features
- Lessons learned from usage

Suggest improvements via:
- Discussion threads
- Sprint retrospectives
- Direct feedback to @hankh95

---

**Version**: 1.0  
**Date**: 2025-11-11  
**Maintainer**: @hankh95  
**Status**: Ready for implementation

## See Also

- [Main README](../README.md) - Project overview
- [Contributing Guide](../CONTRIBUTING.md) - How to contribute (if exists)
- [Santiago Service](../santiago-service/README.md) - Santiago service documentation
- [BDD Examples](../examples/bdd-tests/README.md) - BDD scenario examples
