# GitHub Wiki Structure Guide

This document outlines the proposed structure for the Clinical BDD Creator GitHub Wiki.

## Why Use the Wiki?

The Wiki complements our documentation by providing:
- **Living documentation** that can be edited by team members
- **Shared understanding** across human and AI team members
- **Quick reference** for common patterns and practices
- **Collaborative knowledge building** through wiki-style editing

## Wiki vs Repository Docs

| Use Repository Docs | Use Wiki |
|---------------------|----------|
| Formal specifications | Working notes and drafts |
| Version-controlled docs | Frequently updated content |
| Code-adjacent docs (API) | High-level overviews |
| Release documentation | Troubleshooting guides |
| | Team collaboration notes |

## Proposed Wiki Structure

### Home Page
- Project overview
- Quick links to key resources
- Latest updates and announcements
- Navigation guide

### Architecture Section

#### Santiago Service Architecture
- Four-layer model overview
- Component diagrams
- Data flow documentation
- Integration points

#### NeuroSymbolic Knowledge Graph
- Graph schema documentation
- Relationship types
- Query patterns
- Performance considerations

#### BDD Framework Architecture
- Test structure and organization
- Scenario templates
- Integration with Santiago service
- Test execution flow

#### MCP Integration
- Model Context Protocol overview
- Clinical question answering
- Integration patterns
- Example queries

### Clinical Domain Section

#### Clinical Terminology Systems
- SNOMED CT usage guide
- LOINC integration
- ICD-10 mapping
- RxNorm for medications
- Interoperability patterns

#### Clinical Guidelines Documentation
- Guideline processing workflow
- Evidence grading system
- Recommendation extraction
- Conflict resolution

#### FHIR Integration Guide
- FHIR resource usage
- CPG (Clinical Practice Guidelines) extension
- Terminology bindings
- Example mappings

#### Clinical Safety Protocols
- Safety review checklist
- Validation procedures
- Evidence documentation
- Approval workflows

### Development Section

#### Getting Started
- Environment setup
- Prerequisites
- First-time contributor guide
- Development workflow

#### Santiago Service Development
- Local development setup
- Testing Santiago service
- Debugging tips
- Common issues

#### BDD Test Development
- Writing BDD scenarios
- Test data management
- Clinical scenario templates
- Assertion patterns

#### Testing Guide
- Unit testing approach
- Integration testing
- End-to-end testing
- Clinical validation testing

#### Deployment Guide
- Docker deployment
- CosmosDB setup
- Environment configuration
- Monitoring setup

### Agent Collaboration Section

#### Agent Specifications
- Detailed agent capabilities
- Agent selection guide
- Task assignment patterns
- Agent communication protocols

#### Human-AI Collaboration Patterns
- Pairing strategies
- Review workflows
- Quality assurance
- Escalation procedures

#### Workflow Patterns
- Feature development workflow
- Bug fix workflow
- Documentation workflow
- Research workflow

#### Best Practices
- Code review guidelines
- Clinical validation process
- Documentation standards
- Testing strategies

### Knowledge Base Section

#### Common Patterns
- Graph traversal patterns
- Clinical reasoning patterns
- BDD scenario patterns
- Integration patterns

#### Troubleshooting
- Common issues and solutions
- Debugging strategies
- Performance optimization
- Error resolution

#### Research Findings
- NeuroSymbolic AI insights
- Clinical informatics research
- Performance benchmarks
- Lessons learned

#### Decision Records
- Architecture decisions
- Technology choices
- Process decisions
- Rationale documentation

### Project Management Section

#### Workflows
- Issue creation workflow
- Sprint planning process
- Release management
- Retrospective format

#### Templates
- Issue templates usage
- PR templates
- Meeting notes templates
- Decision record templates

#### Metrics and Reporting
- Velocity tracking
- Quality metrics
- Clinical accuracy metrics
- Team performance

## Creating Wiki Content

### Initial Setup Steps

1. **Enable Wiki**:
   - Go to repository Settings
   - Scroll to Features section
   - Check "Wikis"

2. **Create Home Page**:
   - Navigate to Wiki tab
   - Create initial home page
   - Add navigation links

3. **Create Main Sections**:
   - Architecture
   - Clinical Domain
   - Development
   - Agent Collaboration
   - Knowledge Base
   - Project Management

4. **Populate Content**:
   - Start with high-priority pages
   - Migrate relevant content from daily-notes
   - Extract wisdom from existing documentation
   - Add examples and diagrams

### Wiki Maintenance

**Weekly**:
- Review recent changes
- Update based on daily-notes
- Add new troubleshooting tips

**Monthly**:
- Comprehensive review
- Archive outdated content
- Improve navigation
- Add new sections as needed

**Quarterly**:
- Major restructuring if needed
- Content quality review
- Remove obsolete information

### Content Guidelines

**Writing Style**:
- Clear and concise
- Use examples liberally
- Add diagrams where helpful
- Link to related pages
- Include code samples

**Formatting**:
- Use headers for structure
- Bullet points for lists
- Code blocks for examples
- Tables for comparisons
- Callouts for important notes

**Linking**:
- Link to repository docs
- Cross-link wiki pages
- Link to issues/PRs
- Link to external resources

## Migration Strategy

### Priority 1 (Week 1)
- [ ] Enable Wiki
- [ ] Create Home page
- [ ] Create Architecture overview
- [ ] Create Agent specifications
- [ ] Create Getting Started guide

### Priority 2 (Week 2-3)
- [ ] Santiago Service architecture
- [ ] Clinical terminology guide
- [ ] Development workflow
- [ ] Troubleshooting guide
- [ ] Common patterns

### Priority 3 (Week 4+)
- [ ] Advanced topics
- [ ] Research findings
- [ ] Decision records
- [ ] Comprehensive examples
- [ ] Performance optimization

## Wiki vs Daily Notes

**Keep in Daily Notes**:
- Session logs and progress
- Temporary working notes
- Date-specific information
- Conversation history

**Move to Wiki**:
- Reusable knowledge
- Architecture decisions
- Process documentation
- Best practices
- Troubleshooting guides

## Collaboration on Wiki

### Editing Permissions
- All team members can edit
- Agents can suggest content via PR
- Require human review for clinical content

### Review Process
1. Make edits on wiki page
2. Add edit summary
3. Review changes in history
4. Revert if necessary

### Quality Standards
- Clinical accuracy verified
- Technical accuracy verified
- Clear and understandable
- Properly formatted
- Well-linked to related content

## Example Wiki Pages

### Example: Santiago Service Architecture

```markdown
# Santiago Service Architecture

## Overview
Santiago is a NeuroSymbolic clinical knowledge graph service...

## Four-Layer Model
1. **Layer 1: Raw Text** - Clinical guideline documents
2. **Layer 2: Structured Knowledge** - Extracted entities and relationships
3. **Layer 3: Computable Logic** - FHIR-CPG representation
4. **Layer 4: Executable Workflows** - Deployable decision support

## Component Diagram
[Mermaid diagram here]

## Integration Points
- MCP Server for clinical Q&A
- FHIR server for patient data
- Graph database for knowledge storage

## Related Pages
- [[NeuroSymbolic Knowledge Graph]]
- [[MCP Integration]]
- [[FHIR Integration Guide]]
```

### Example: Agent Selection Guide

```markdown
# Agent Selection Guide

## When to Use Which Agent

### Clinical Informaticist Agent
**Use for:**
- Clinical terminology mapping
- Guideline interpretation
- Clinical workflow design
- Domain-specific validation

**Examples:**
- "Map SNOMED CT concepts to ICD-10"
- "Validate clinical decision logic"

### NeuroSymbolic Architect Agent
**Use for:**
- Knowledge graph design
- Advanced reasoning patterns
- Architecture decisions
- NeuroSymbolic integration

**Examples:**
- "Design relationship schema"
- "Optimize graph traversal"

[Continue for all agents...]
```

## Tools and Integrations

### Wiki Automation
- Automated TOC generation
- Link checking
- Content validation
- Search optimization

### External Tools
- Mermaid for diagrams
- GitHub-flavored Markdown
- Code syntax highlighting
- Table formatting

## Success Metrics

Track wiki effectiveness:
- Page views
- Edit frequency
- Search success rate
- User feedback
- Content freshness

## Resources

- [GitHub Wiki Documentation](https://docs.github.com/en/communities/documenting-your-project-with-wikis)
- [Markdown Guide](https://guides.github.com/features/mastering-markdown/)
- [Mermaid Documentation](https://mermaid-js.github.io/)

---

**Version**: 1.0  
**Last Updated**: 2025-11-11  
**Maintainer**: @hankh95
