# BDD Best Practices for Project Management

## Overview

As a project that builds BDD (Behavior-Driven Development) tools for clinical decision support, we apply BDD principles to our own project management. This guide documents how to use BDD practices throughout the development lifecycle.

## Core BDD Principles

### 1. Shared Understanding

**Principle**: Everyone on the team (humans and AI agents) should have a shared understanding of what we're building and why.

**In Practice**:
- Write user stories in BDD format
- Use Given-When-Then for acceptance criteria
- Review stories with all stakeholders (including relevant agents)
- Keep stories in plain language, not technical jargon

### 2. Concrete Examples

**Principle**: Use concrete examples to illustrate expected behavior.

**In Practice**:
- Include example scenarios in issue descriptions
- Provide sample inputs and expected outputs
- Reference real clinical use cases
- Link to example code or data

### 3. Living Documentation

**Principle**: Documentation should stay up-to-date and executable.

**In Practice**:
- Write executable specifications as tests
- Update docs when behavior changes
- Link issues to test files
- Maintain wiki with current patterns

### 4. Outside-In Development

**Principle**: Start with user-facing behavior, then implement internals.

**In Practice**:
- Write acceptance tests first
- Define API before implementation
- Think from user perspective
- Validate with stakeholders early

## BDD Format for Issues

### User Stories

Every feature should start with a user story:

```gherkin
As a [role]
I want [feature]
So that [benefit]
```

**Examples**:

```gherkin
As a clinical researcher
I want to import FHIR resources into the knowledge graph
So that I can analyze real patient data against clinical guidelines
```

```gherkin
As a healthcare developer
I want to query the Santiago service via MCP
So that I can integrate clinical decision support into my application
```

### Acceptance Criteria

Use Given-When-Then format for all acceptance criteria:

```gherkin
Given [initial context/state]
When [action or event occurs]
Then [expected outcome]
And [additional outcomes]
```

**Examples**:

```gherkin
Given a patient with Type 2 Diabetes (SNOMED: 44054006)
When the system evaluates treatment recommendations
Then it should suggest Metformin as first-line therapy
And it should check for contraindications
And it should consider patient preferences
```

```gherkin
Given the Santiago service is running
When I send a clinical question via MCP
Then I should receive a response within 2 seconds
And the response should include clinical evidence
And the response should cite relevant guidelines
```

### Scenarios

Break down features into specific scenarios:

```gherkin
Feature: Clinical Guideline Query

  Background:
    Given the Santiago knowledge graph contains hypertension guidelines
    And the guidelines are from JNC 8 (2014)
    
  Scenario: Query for first-line treatment
    Given a patient with essential hypertension
    And no contraindications
    When I query for treatment recommendations
    Then I should receive ACE inhibitor as first-line
    And I should receive supporting evidence
    
  Scenario: Query with contraindications
    Given a patient with essential hypertension
    And the patient has a history of angioedema
    When I query for treatment recommendations
    Then ACE inhibitors should be excluded
    And alternative therapies should be suggested
    And the rationale should cite the contraindication
```

## BDD in Different Issue Types

### Feature Requests

```markdown
## User Story
As a [role]
I want [feature]
So that [benefit]

## Acceptance Criteria

### Scenario 1: [Primary happy path]
Given [context]
When [action]
Then [outcome]

### Scenario 2: [Edge case]
Given [context]
When [action]
Then [outcome]

### Scenario 3: [Error handling]
Given [context]
When [action]
Then [outcome]

## Examples
[Concrete examples with data]

## Non-Functional Requirements
- Performance: [specific metrics]
- Security: [specific requirements]
- Compliance: [standards to follow]
```

### Bug Reports

```markdown
## Expected Behavior (BDD Format)
Given [state that should exist]
When [action that should work]
Then [outcome that should occur]

## Actual Behavior
Given [actual state]
When [action performed]
Then [incorrect outcome]

## Steps to Reproduce
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Example
[Specific example that demonstrates the bug]
```

### Tasks

```markdown
## Task Description
[Clear description of what needs to be done]

## Acceptance Criteria (BDD Format)
- [ ] Given [context], when [action], then [outcome]
- [ ] Given [context], when [action], then [outcome]
- [ ] All tests pass
- [ ] Documentation updated

## Definition of Done
- [ ] Code written and reviewed
- [ ] Tests written (if applicable)
- [ ] Documentation updated (if applicable)
- [ ] Deployed to test environment
- [ ] Validated by stakeholder
```

## BDD for Product Hypotheses

### Hypothesis Format

```markdown
## Hypothesis
We believe that [doing X]
For [users Y]
Will achieve [outcome Z]

## Success Metrics
We'll know we're right when we see:
- [Metric 1] change from [baseline] to [target]
- [Metric 2] change from [baseline] to [target]

## Experiment Design

### Given
- [Initial state/users/environment]

### When
- [Change we will make]
- [How we will measure]

### Then
- [Expected results]
- [Timeline for evaluation]

## Validation Scenarios

### Scenario 1: Success case
Given [users in experiment group]
When [they use the new feature]
Then [we should observe X improvement]

### Scenario 2: Failure case
Given [users in experiment group]
When [they encounter Y problem]
Then [we should observe Z feedback]
```

## BDD in Sprint Planning

### Sprint Goals (BDD Style)

```gherkin
Sprint Goal: Enable clinical researchers to import FHIR data

Given we complete the planned work
When clinical researchers use the system
Then they should be able to import FHIR resources in < 5 minutes
And they should see their data in the knowledge graph
And they should be able to query imported data immediately
```

### Sprint Review (BDD Validation)

For each completed story, demonstrate:
1. **Given**: Show the starting state
2. **When**: Perform the action
3. **Then**: Verify the outcome
4. **Acceptance**: Confirm criteria are met

## BDD in Code Reviews

### Review Checklist (BDD Style)

```markdown
## Behavior Validation
- [ ] Given-When-Then scenarios are implemented
- [ ] Edge cases are handled
- [ ] Error conditions are tested
- [ ] Examples from issue work correctly

## Test Coverage
- [ ] Unit tests for core logic
- [ ] Integration tests for workflows
- [ ] BDD scenarios are executable
- [ ] Test names describe behavior

## Documentation
- [ ] Behavior is documented
- [ ] Examples are provided
- [ ] API changes are documented
- [ ] BDD scenarios are up-to-date
```

## BDD for Agent Collaboration

### Agent Task Assignment (BDD Format)

```markdown
## Agent: [Agent Name]

### Context
Given you are the [agent role]
And you have expertise in [domain]

### Task
When you work on this issue
Then you should focus on [specific aspects]
And you should collaborate with [other agents]

### Acceptance
Given you complete the task
When you submit your work
Then it should meet these criteria:
- [Criterion 1]
- [Criterion 2]
- [Criterion 3]
```

### Agent Handoff

```markdown
## Handoff from [Agent A] to [Agent B]

### Completed Work
Given [Agent A] completed:
- [Task 1]
- [Task 2]

### Current State
The system now behaves as follows:
- Given [state], when [action], then [outcome]

### Next Steps for [Agent B]
When you continue this work
Then you should:
- [Next task 1]
- [Next task 2]

### Success Criteria
Given you complete your work
When we test the system
Then we should observe:
- [Outcome 1]
- [Outcome 2]
```

## BDD for Clinical Validation

### Clinical Scenario Template

```gherkin
Feature: [Clinical Guideline Name] Implementation

  Background:
    Given the system implements [Guideline Name] [Version]
    And the guideline source is [URL/Reference]
    And the implementation date is [Date]

  Scenario: [Clinical Scenario Name]
    Given a patient with the following characteristics:
      | Attribute        | Value          | SNOMED/LOINC Code |
      | Age             | [age]          | -                 |
      | Gender          | [gender]       | -                 |
      | Primary Dx      | [diagnosis]    | [code]            |
      | Comorbidity     | [condition]    | [code]            |
      
    And the patient has the following labs:
      | Test            | Value          | LOINC Code        |
      | [test name]     | [value]        | [code]            |
      
    When the clinical decision support system evaluates the patient
    
    Then the system should recommend:
      | Recommendation  | Strength       | Evidence Level    |
      | [treatment]     | [strong/weak]  | [level]           |
      
    And the system should flag these considerations:
      | Type            | Description    | Code              |
      | Contraindication| [description]  | [code]            |
      | Drug Interaction| [description]  | [code]            |
```

## Metrics for BDD Practice

### Process Metrics

Track how well we follow BDD practices:

- **Story Completeness**: % of stories with Given-When-Then format
- **Scenario Coverage**: Average scenarios per story
- **Example Quality**: % of stories with concrete examples
- **Test Alignment**: % of acceptance criteria with corresponding tests

### Outcome Metrics

Track the impact of BDD practices:

- **Shared Understanding**: Team survey scores
- **Rework Rate**: % of stories requiring rework
- **First-Time Quality**: % of stories accepted first review
- **Cycle Time**: Time from story creation to acceptance

## Tools and Templates

### Issue Templates
Use our GitHub issue templates which enforce BDD format

### Gherkin Files
Store BDD scenarios as `.feature` files in `/examples/bdd-tests/`

### Test Framework
Use pytest-bdd or similar to make scenarios executable

### Documentation
Link BDD scenarios to implementation docs and tests

## Learning Resources

### Books
- "BDD in Action" by John Ferguson Smart
- "Specification by Example" by Gojko Adzic
- "The Cucumber Book" by Matt Wynne & Aslak Hellesøy

### Internal Resources
- [BDD Framework Documentation](../examples/bdd-tests/README.md)
- [Clinical Scenario Templates](../examples/bdd-tests/scenarios/)
- [PROJECT-MANAGEMENT.md](./PROJECT-MANAGEMENT.md)

### External Resources
- [Cucumber.io Documentation](https://cucumber.io/docs/bdd/)
- [BDD on Wikipedia](https://en.wikipedia.org/wiki/Behavior-driven_development)

## Common Anti-Patterns to Avoid

### ❌ Don't: Write implementation details in scenarios

```gherkin
# Bad
Given I query the database with SQL
When I execute the stored procedure
Then the result set has 5 rows
```

```gherkin
# Good
Given the system has 5 active patients
When I search for patients with diabetes
Then I should see a list of 5 patients
```

### ❌ Don't: Write vague acceptance criteria

```gherkin
# Bad
Then the system should work correctly
And the user should be happy
```

```gherkin
# Good
Then the query should return results in < 2 seconds
And the results should include patient name, ID, and diagnosis
And the results should be sorted by last visit date
```

### ❌ Don't: Skip the Given context

```gherkin
# Bad
When I click submit
Then I see an error
```

```gherkin
# Good
Given I am on the patient form
And I have not entered required fields
When I click submit
Then I should see validation errors for missing fields
```

## Continuous Improvement

### Retrospective Questions

- Are our BDD scenarios helping us build the right thing?
- Do our scenarios serve as living documentation?
- Are our Given-When-Then statements clear to all team members?
- Are we writing scenarios at the right level of abstraction?
- How can we improve our BDD practice?

### Regular Reviews

- **Weekly**: Review new scenarios for quality
- **Sprint**: Assess BDD practice in retrospective
- **Monthly**: Update templates and guidelines
- **Quarterly**: Train team on BDD best practices

---

**Version**: 1.0  
**Last Updated**: 2025-11-11  
**Maintainer**: @hankh95

## See Also

- [PROJECT-MANAGEMENT.md](./PROJECT-MANAGEMENT.md) - Overall project management guide
- [Examples](../examples/bdd-tests/) - BDD scenario examples
- [Testing Guide](../TESTING.md) - Testing practices
