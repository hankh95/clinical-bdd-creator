# GitHub Labels Configuration

This file documents all labels used in the Clinical BDD Creator project. These labels should be created manually in the repository settings or via the GitHub API.

## Label Categories

### Type Labels (What kind of work?)

| Label | Color | Description |
|-------|-------|-------------|
| `type: feature` | `#0075ca` | New feature or enhancement |
| `type: bug` | `#d73a4a` | Bug report or fix |
| `type: task` | `#1d76db` | Development task or work item |
| `type: documentation` | `#0075ca` | Documentation improvements |
| `type: refactor` | `#fbca04` | Code refactoring |
| `type: security` | `#ee0701` | Security issue or improvement |
| `type: performance` | `#d876e3` | Performance improvement |
| `type: test` | `#5319e7` | Testing related |

### Status Labels (Where is it in the workflow?)

| Label | Color | Description |
|-------|-------|-------------|
| `status: needs-triage` | `#ffffff` | Needs initial review and categorization |
| `status: planned` | `#0e8a16` | Approved and in backlog |
| `status: in-progress` | `#fbca04` | Actively being worked on |
| `status: blocked` | `#d93f0b` | Blocked by dependencies |
| `status: review` | `#d876e3` | In code review |
| `status: stale` | `#cccccc` | No recent activity |
| `status: wont-fix` | `#ffffff` | Will not be addressed |
| `status: duplicate` | `#cfd3d7` | Duplicate of another issue |

### Priority Labels (How urgent?)

| Label | Color | Description |
|-------|-------|-------------|
| `priority: p0-critical` | `#b60205` | 🔴 Critical - Blocking/Security/Data loss |
| `priority: p1-high` | `#d93f0b` | 🟠 High priority |
| `priority: p2-medium` | `#fbca04` | 🟡 Medium priority |
| `priority: p3-low` | `#0e8a16` | 🟢 Low priority |

### Area Labels (Which part of the system?)

| Label | Color | Description |
|-------|-------|-------------|
| `area: santiago-service` | `#1d76db` | Santiago NeuroSymbolic service |
| `area: bdd-framework` | `#0075ca` | BDD testing framework |
| `area: testing` | `#5319e7` | Testing infrastructure |
| `area: documentation` | `#0075ca` | Documentation |
| `area: devops` | `#006b75` | DevOps and deployment |
| `area: clinical-knowledge` | `#c5def5` | Clinical knowledge graphs |
| `area: api` | `#d876e3` | API development |
| `area: mcp` | `#5319e7` | Model Context Protocol |
| `area: fhir` | `#c5def5` | FHIR integration |

### Agent Labels (Who should work on this?)

| Label | Color | Description |
|-------|-------|-------------|
| `agent: human` | `#000000` | 👤 Requires human judgment |
| `agent: development` | `#0052cc` | 🤖 General development agent |
| `agent: clinical-informaticist` | `#006b75` | 🏥 Clinical domain expert agent |
| `agent: neurosymbolic-architect` | `#5319e7` | 🧬 NeuroSymbolic architecture agent |
| `agent: qa` | `#0e8a16` | ✅ Quality assurance agent |
| `agent: product-manager` | `#fbca04` | 📊 Product manager agent |
| `agent: devops` | `#1d76db` | 🔧 DevOps expert agent |
| `agent: monetization` | `#d876e3` | 💰 Monetization expert agent |

### Effort Labels (How much work?)

| Label | Color | Description |
|-------|-------|-------------|
| `effort: xs` | `#c5def5` | < 2 hours |
| `effort: s` | `#bfd4f2` | 2-4 hours |
| `effort: m` | `#9cc4e4` | 4-8 hours (half day to full day) |
| `effort: l` | `#7cb4da` | 1-2 days |
| `effort: xl` | `#5da5cf` | 2-5 days |
| `effort: xxl` | `#3e95c5` | > 1 week |

### Clinical Labels (Clinical considerations)

| Label | Color | Description |
|-------|-------|-------------|
| `clinical: safety-critical` | `#b60205` | Affects patient safety |
| `clinical: accuracy-required` | `#d93f0b` | Requires clinical validation |
| `clinical: evidence-based` | `#0e8a16` | Follows evidence-based guidelines |
| `clinical: fhir-compliant` | `#0075ca` | Must comply with FHIR standards |
| `clinical: terminology` | `#c5def5` | Involves clinical terminology (SNOMED, LOINC) |

### Special Labels

| Label | Color | Description |
|-------|-------|-------------|
| `good first issue` | `#7057ff` | Good for newcomers |
| `help wanted` | `#008672` | Extra attention needed |
| `keep-open` | `#0e8a16` | Prevent stale bot from closing |
| `breaking-change` | `#d93f0b` | Breaking API or interface change |
| `needs-discussion` | `#d876e3` | Needs team discussion |
| `experiment` | `#fbca04` | Experimental feature (hypothesis testing) |
| `technical-debt` | `#d93f0b` | Technical debt to address |

## Creating Labels via GitHub CLI

To create all labels at once, use the following script:

```bash
#!/bin/bash

# Type labels
gh label create "type: feature" -c 0075ca -d "New feature or enhancement"
gh label create "type: bug" -c d73a4a -d "Bug report or fix"
gh label create "type: task" -c 1d76db -d "Development task or work item"
gh label create "type: documentation" -c 0075ca -d "Documentation improvements"
gh label create "type: refactor" -c fbca04 -d "Code refactoring"
gh label create "type: security" -c ee0701 -d "Security issue or improvement"
gh label create "type: performance" -c d876e3 -d "Performance improvement"
gh label create "type: test" -c 5319e7 -d "Testing related"

# Status labels
gh label create "status: needs-triage" -c ffffff -d "Needs initial review and categorization"
gh label create "status: planned" -c 0e8a16 -d "Approved and in backlog"
gh label create "status: in-progress" -c fbca04 -d "Actively being worked on"
gh label create "status: blocked" -c d93f0b -d "Blocked by dependencies"
gh label create "status: review" -c d876e3 -d "In code review"
gh label create "status: stale" -c cccccc -d "No recent activity"
gh label create "status: wont-fix" -c ffffff -d "Will not be addressed"
gh label create "status: duplicate" -c cfd3d7 -d "Duplicate of another issue"

# Priority labels
gh label create "priority: p0-critical" -c b60205 -d "🔴 Critical - Blocking/Security/Data loss"
gh label create "priority: p1-high" -c d93f0b -d "🟠 High priority"
gh label create "priority: p2-medium" -c fbca04 -d "🟡 Medium priority"
gh label create "priority: p3-low" -c 0e8a16 -d "🟢 Low priority"

# Area labels
gh label create "area: santiago-service" -c 1d76db -d "Santiago NeuroSymbolic service"
gh label create "area: bdd-framework" -c 0075ca -d "BDD testing framework"
gh label create "area: testing" -c 5319e7 -d "Testing infrastructure"
gh label create "area: documentation" -c 0075ca -d "Documentation"
gh label create "area: devops" -c 006b75 -d "DevOps and deployment"
gh label create "area: clinical-knowledge" -c c5def5 -d "Clinical knowledge graphs"
gh label create "area: api" -c d876e3 -d "API development"
gh label create "area: mcp" -c 5319e7 -d "Model Context Protocol"
gh label create "area: fhir" -c c5def5 -d "FHIR integration"

# Agent labels
gh label create "agent: human" -c 000000 -d "👤 Requires human judgment"
gh label create "agent: development" -c 0052cc -d "🤖 General development agent"
gh label create "agent: clinical-informaticist" -c 006b75 -d "🏥 Clinical domain expert agent"
gh label create "agent: neurosymbolic-architect" -c 5319e7 -d "🧬 NeuroSymbolic architecture agent"
gh label create "agent: qa" -c 0e8a16 -d "✅ Quality assurance agent"
gh label create "agent: product-manager" -c fbca04 -d "📊 Product manager agent"
gh label create "agent: devops" -c 1d76db -d "🔧 DevOps expert agent"
gh label create "agent: monetization" -c d876e3 -d "💰 Monetization expert agent"

# Effort labels
gh label create "effort: xs" -c c5def5 -d "< 2 hours"
gh label create "effort: s" -c bfd4f2 -d "2-4 hours"
gh label create "effort: m" -c 9cc4e4 -d "4-8 hours"
gh label create "effort: l" -c 7cb4da -d "1-2 days"
gh label create "effort: xl" -c 5da5cf -d "2-5 days"
gh label create "effort: xxl" -c 3e95c5 -d "> 1 week"

# Clinical labels
gh label create "clinical: safety-critical" -c b60205 -d "Affects patient safety"
gh label create "clinical: accuracy-required" -c d93f0b -d "Requires clinical validation"
gh label create "clinical: evidence-based" -c 0e8a16 -d "Follows evidence-based guidelines"
gh label create "clinical: fhir-compliant" -c 0075ca -d "Must comply with FHIR standards"
gh label create "clinical: terminology" -c c5def5 -d "Involves clinical terminology"

# Special labels
gh label create "good first issue" -c 7057ff -d "Good for newcomers"
gh label create "help wanted" -c 008672 -d "Extra attention needed"
gh label create "keep-open" -c 0e8a16 -d "Prevent stale bot from closing"
gh label create "breaking-change" -c d93f0b -d "Breaking API or interface change"
gh label create "needs-discussion" -c d876e3 -d "Needs team discussion"
gh label create "experiment" -c fbca04 -d "Experimental feature"
gh label create "technical-debt" -c d93f0b -d "Technical debt to address"
```

## Using Labels

### Basic Labeling Guidelines

1. **Every issue should have**:
   - One `type:` label
   - One `status:` label
   - One `priority:` label
   - At least one `area:` label

2. **Optional labels**:
   - `agent:` labels (for assignment)
   - `effort:` labels (for estimation)
   - `clinical:` labels (if applicable)
   - Special labels as needed

### Label Combinations

**New Feature Example**:
- `type: feature`
- `status: needs-triage`
- `priority: p2-medium`
- `area: santiago-service`
- `agent: neurosymbolic-architect`

**Critical Bug Example**:
- `type: bug`
- `status: in-progress`
- `priority: p0-critical`
- `area: api`
- `clinical: safety-critical`
- `agent: human`

**Documentation Task Example**:
- `type: documentation`
- `status: planned`
- `priority: p3-low`
- `area: documentation`
- `effort: s`
- `good first issue`

## Automated Labeling

The following labels are automatically applied:

- **Area labels**: Applied by `.github/labeler.yml` based on file paths
- **Stale labels**: Applied by stale workflow after 60 days of inactivity

## Label Maintenance

Review and update labels:
- Monthly: Review label usage patterns
- Quarterly: Update label descriptions if needed
- As needed: Add new labels for emerging needs
- Archive: Unused labels after 6 months

---

**Version**: 1.0  
**Last Updated**: 2025-11-11  
**Maintainer**: @hankh95
