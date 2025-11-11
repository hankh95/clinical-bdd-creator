# Copilot Coding Agent Instructions

## Repository Overview

This repository (`clinical-bdd-creator`) contains the **Clinical BDD Creator** project, a comprehensive system for transforming clinical guidelines into Behavior-Driven Development (BDD) scenarios and executable clinical decision support systems.

### Key Components

1. **Santiago Service** (`santiago-service/`): NeuroSymbolic clinical knowledge graph service
   - Four-layer architecture: Raw Text → Structured Knowledge → Computable Logic → Executable Workflows
   - MCP (Model Context Protocol) integration for clinical question answering
   - Dynamic Relationship Discovery Engine (DRDE) for clinical relationship discovery

2. **Agent Instructions** (`.github/agents/`): Specialized agent configurations for different aspects of clinical informatics work

3. **Documentation** (`prompts/`, `requirements/`, `dev_plan/`): Comprehensive documentation and planning materials

4. **Testing Infrastructure**: Comprehensive test suites for clinical workflow validation

## Coding Standards & Practices

### Python Standards
- **Style**: Follow PEP 8 with Black formatting
- **Type Hints**: Use comprehensive type annotations
- **Documentation**: Docstrings for all public functions/classes
- **Error Handling**: Comprehensive exception handling with meaningful messages
- **Logging**: Use Python logging module with appropriate levels

### Clinical Informatics Standards
- **Terminology**: Use SNOMED CT, LOINC, ICD-10, RxNorm appropriately
- **Standards Compliance**: Follow HL7 FHIR, OpenEHR, and clinical practice guidelines
- **Patient Safety**: Prioritize clinical accuracy and safety in all implementations
- **Evidence-Based**: Ground implementations in clinical evidence and best practices

### Testing Requirements
- **Unit Tests**: 80%+ code coverage minimum
- **Integration Tests**: End-to-end clinical workflow testing
- **Clinical Validation**: Test against real clinical scenarios
- **Performance**: Benchmark clinical decision support performance

## Agent Collaboration Guidelines

### When to Use Agents
- **Research Tasks**: Clinical standards analysis, terminology research
- **Implementation**: Complex feature development with clear specifications
- **Documentation**: Technical writing and specification development
- **Testing**: Comprehensive test suite development

### Agent Communication
- **Clear Specifications**: Provide detailed requirements and acceptance criteria
- **Context Sharing**: Include relevant clinical context and use cases
- **Review Process**: All agent work should be reviewed by human experts
- **Iterative Development**: Use feedback loops for refinement

### Quality Assurance
- **Clinical Accuracy**: All outputs must be clinically validated
- **Code Quality**: Follow repository standards and best practices
- **Documentation**: Comprehensive documentation for all deliverables
- **Testing**: Automated testing for all new functionality

## Project-Specific Context

### Clinical Domain Knowledge
- **Cardiovascular Disease**: Focus on hypertension, diabetes management, heart failure
- **Evidence-Based Medicine**: Ground all implementations in clinical evidence
- **Interoperability**: Ensure compatibility with EHR systems and clinical workflows
- **Regulatory Compliance**: Consider HIPAA, GDPR, and clinical safety requirements

### Technical Architecture
- **Microservices**: Modular design with clear service boundaries
- **API-First**: RESTful APIs with OpenAPI specifications
- **Database**: Graph databases for knowledge representation, relational for structured data
- **Deployment**: Containerized deployment with Kubernetes orchestration

### Development Workflow
- **Git Flow**: Feature branches with pull request reviews
- **Documentation**: Update documentation with all changes
- **Testing**: Automated testing in CI/CD pipeline
- **Code Review**: Peer review for all changes

## Agent Task Guidelines

### Task Assignment Criteria
- **Complexity**: Tasks requiring research, analysis, or specialized knowledge
- **Scope**: Well-defined deliverables with clear acceptance criteria
- **Independence**: Tasks that can be completed with minimal ongoing supervision
- **Value**: High-impact tasks that advance clinical informatics goals

### Task Completion Standards
- **Deliverables**: Complete, tested, and documented code/features
- **Quality**: Meets all coding standards and clinical requirements
- **Documentation**: Comprehensive documentation and usage examples
- **Testing**: Full test coverage with clinical validation scenarios

### Communication Expectations
- **Progress Updates**: Regular updates on task progress and challenges
- **Issue Escalation**: Immediate notification of blockers or critical issues
- **Knowledge Sharing**: Documentation of learnings and best practices
- **Collaboration**: Proactive coordination with other agents and human team members

## Repository Structure Expectations

### File Organization
- **Source Code**: Organized by feature/module with clear naming conventions
- **Tests**: Parallel test structure mirroring source code organization
- **Documentation**: Comprehensive docs in appropriate directories
- **Configuration**: Centralized configuration management

### Naming Conventions
- **Files**: snake_case for Python files, kebab-case for documentation
- **Classes**: PascalCase with descriptive names
- **Functions**: snake_case with verb-noun pattern
- **Variables**: snake_case with descriptive names

### Commit Standards
- **Messages**: Clear, descriptive commit messages following conventional commits
- **Atomic**: Each commit represents a single logical change
- **Frequent**: Regular commits to maintain history granularity

## Clinical Safety & Ethics

### Patient Safety First
- **Clinical Accuracy**: All implementations must prioritize patient safety
- **Evidence-Based**: Ground decisions in clinical evidence and best practices
- **Error Prevention**: Comprehensive validation and error handling
- **Audit Trail**: Maintain traceability for clinical decision support

### Ethical Considerations
- **Privacy**: Protect patient data and maintain confidentiality
- **Bias Mitigation**: Ensure equitable clinical decision support
- **Transparency**: Clear documentation of algorithms and decision logic
- **Accountability**: Maintain responsibility for clinical recommendations

## Performance & Scalability

### Performance Targets
- **Response Time**: <100ms for clinical decision support queries
- **Throughput**: Support concurrent clinical workflows
- **Resource Usage**: Efficient memory and CPU utilization
- **Scalability**: Horizontal scaling for increased load

### Monitoring & Observability
- **Metrics**: Comprehensive performance and clinical outcome metrics
- **Logging**: Structured logging with appropriate detail levels
- **Alerting**: Proactive monitoring and alerting for issues
- **Tracing**: End-to-end request tracing for debugging

## Integration Points

### External Systems
- **EHR Integration**: FHIR-based integration with electronic health records
- **Terminology Services**: Integration with clinical terminology systems
- **Knowledge Bases**: Connection to clinical knowledge repositories
- **Decision Support**: Integration with clinical decision support systems

### API Design
- **RESTful**: Consistent REST API design following FHIR patterns
- **Versioning**: API versioning for backward compatibility
- **Documentation**: OpenAPI specifications for all APIs
- **Security**: OAuth2/JWT authentication and authorization

## Development Environment

### Local Development
- **Containerization**: Docker-based development environment
- **Dependencies**: Comprehensive dependency management
- **Testing**: Local test execution with coverage reporting
- **Debugging**: Integrated debugging and profiling tools

### CI/CD Pipeline
- **Automated Testing**: Comprehensive test automation
- **Code Quality**: Static analysis and code quality checks
- **Security Scanning**: Automated security vulnerability detection
- **Deployment**: Automated deployment to staging and production

## Agent-Specific Instructions

### For Clinical Research Tasks
- **Evidence Review**: Comprehensive review of clinical literature
- **Standards Analysis**: Deep analysis of clinical standards and specifications
- **Implementation Guidance**: Practical implementation recommendations
- **Validation Strategies**: Methods for clinical validation and testing

### For Implementation Tasks
- **Code Quality**: Production-ready code following all standards
- **Testing**: Comprehensive test coverage with clinical scenarios
- **Documentation**: Complete documentation and usage examples
- **Integration**: Seamless integration with existing systems

### For Documentation Tasks
- **Clarity**: Clear, concise, and clinically accurate documentation
- **Completeness**: Comprehensive coverage of all aspects
- **Accessibility**: Appropriate for different audiences (clinicians, developers, administrators)
- **Maintenance**: Easy to update and maintain over time

## Emergency Procedures

### Critical Issues
- **Patient Safety**: Immediate escalation for any patient safety concerns
- **Data Breach**: Immediate response to potential data security issues
- **System Downtime**: Rapid response to system availability issues
- **Clinical Errors**: Immediate investigation of potential clinical errors

### Escalation Paths
- **Technical Issues**: Escalate to development team leads
- **Clinical Issues**: Escalate to clinical informatics experts
- **Security Issues**: Escalate to security team immediately
- **Compliance Issues**: Escalate to compliance and legal teams

## Continuous Improvement

### Feedback Loops
- **Code Reviews**: Regular review and feedback on all changes
- **Performance Monitoring**: Continuous monitoring of system performance
- **User Feedback**: Incorporation of user feedback and requirements
- **Clinical Validation**: Ongoing validation of clinical accuracy

### Learning & Adaptation
- **Technology Updates**: Stay current with evolving technologies and standards
- **Best Practices**: Adopt industry best practices and lessons learned
- **Innovation**: Explore new approaches to improve clinical outcomes
- **Knowledge Sharing**: Share learnings across the team and organization

---

*This document provides comprehensive guidance for Copilot coding agents working on the Clinical BDD Creator project. All agents should familiarize themselves with this document and follow the established standards and practices.*