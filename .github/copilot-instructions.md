# GitHub Copilot Instructions for Clinical BDD Creator

## Project Overview

The **Clinical BDD Creator** is a Python-based application that transforms clinical practice guidelines into Behavior-Driven Development (BDD) test scenarios and computable FHIR-CPG assets. The repository includes:

1. **Clinical BDD Creator**: Main application for generating BDD test scenarios from clinical guidelines
2. **Santiago NeuroSymbolic Service**: A sister MCP (Model Context Protocol) service that transforms clinical guidelines into a four-layer NeuroSymbolic knowledge graph

### Key Capabilities
- Transform clinical guidelines into BDD test scenarios (Gherkin format)
- Generate FHIR-CPG (Clinical Practice Guidelines) assets
- Four-layer knowledge representation (L0 Prose → L1 GSRL → L2 RALL → L3 WATL)
- NeuroSymbolic reasoning combining symbolic logic with neural networks
- MCP interface for AI assistant integrations
- REST API endpoints with health checks and monitoring

## Repository Structure

```
├── app.py                          # Main Flask application entry point
├── guideline_analyzer.py           # Core guideline analysis logic
├── integration_test_runner.py      # Integration testing framework
├── santiago-service/               # Santiago NeuroSymbolic service implementation
├── spec-pack/                      # Clinical specifications and guidelines
├── test*.py                        # Test files (pytest)
├── config/                         # Configuration files
├── monitoring/                     # Monitoring and observability setup
├── .github/agents/                 # Custom agent instructions
├── requirements.txt                # Python dependencies
└── Dockerfile                      # Container configuration
```

## Technology Stack

### Core Technologies
- **Python 3.11+**: Primary development language with type hints and dataclasses
- **Flask**: Web framework for REST API endpoints
- **pytest**: Testing framework with fixtures and coverage reporting
- **Docker**: Containerized deployment
- **Azure CosmosDB/Gremlin**: Graph database for knowledge storage
- **FHIR-CPG**: HL7 Clinical Practice Guidelines implementation (R4)

### Key Dependencies
- Flask, Flask-CORS, Gunicorn (web framework)
- pandas, numpy, scipy (data processing)
- scikit-learn, nltk, spacy, transformers, torch (ML/NLP)
- pytest, pytest-cov (testing)
- prometheus-client, structlog (monitoring)

## Development Practices

### Code Standards
- **Type Hints**: Use type hints for all function parameters and return values
- **Dataclasses**: Leverage dataclasses for data structures
- **PEP 8**: Follow PEP 8 naming conventions
- **pathlib**: Use `pathlib.Path` for file operations
- **Error Handling**: Implement proper error handling and logging

### Import Organization
```python
from __future__ import annotations
import standard_library
import third_party
import local_modules
```

### Testing Framework
- **Unit Tests**: Individual function/component testing
- **Integration Tests**: Cross-component pipeline validation
- **BDD Tests**: Clinical scenario validation using Gherkin
- **Performance Tests**: API call efficiency and resource usage
- **Fidelity Tests**: Validation of clinical knowledge accuracy

## How to Build and Test

### Setup Environment
```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment configuration
cp .env.example .env
# Edit .env with your configuration
```

### Run Tests
```bash
# Run all tests with pytest
pytest

# Run tests with coverage
python -m pytest --cov

# Run specific test file
pytest test_sample_guidelines.py

# Run integration tests
python integration_test_runner.py
```

### Run the Application
```bash
# Development mode
python app.py

# Production deployment with Docker
docker-compose up -d

# Check deployment status
./deploy.sh status
```

### Health Checks
```bash
# Check service health
curl -k https://localhost/health

# View logs
./deploy.sh logs clinical-bdd-creator
```

## Git Workflow

### Branch Strategy
- `main`: Production-ready code
- Feature branches: `feature/santiago-component-description`
- Bug fixes: `fix/component-issue-description`
- Research branches: `research/santiago-capability`

### Commit Standards
- Clear, descriptive commit messages
- Reference GitHub Issues in commits (use closing keywords: `Closes #123`, `Fixes #123`, `Resolves #123`)
- Group related changes logically
- Use conventional commit format when appropriate

## GitHub Collaboration

### Issues Management
- **Create Issues First**: Always create a GitHub issue before starting work on new features, bugs, or enhancements
- Tag issues with appropriate labels (bug, enhancement, documentation, santiago, research)
- Reference issues in commits and PRs
- **Close Issues When Complete**: Use closing keywords in PR descriptions to automatically close issues when work is merged

### Pull Request Process
- Create feature branches from `main`
- Keep PRs focused on single concerns
- Request clinical informaticist review for Santiago logic changes
- Include testing and documentation updates
- Link to issues in PR descriptions using closing keywords

## Santiago Four-Layer Model

When working with the Santiago service, understand the four-layer architecture:
- **Layer 0 (Prose)**: Human-readable clinical content with YAML metadata and provenance
- **Layer 1 (GSRL)**: Semantic triples using canonical relations (no logic/thresholds)
- **Layer 2 (RALL)**: Computable FHIR-CPG assets (ActivityDefinitions, PlanDefinitions, Libraries)
- **Layer 3 (WATL)**: Workflow orchestration with temporal sequencing and NeuroSymbolic reasoning

## Clinical Safety Considerations

- **Clinical Accuracy**: Ensure all Santiago components maintain clinical accuracy
- **Provenance**: All assets must link back to source content
- **Interoperability**: Follow FHIR standards for healthcare data exchange
- **Testing**: Comprehensive testing required for clinical decision support features

## Important Files and Documentation

- **PRODUCTION-README.md**: Production operations guide
- **OPERATIONAL-RUNBOOK.md**: Complete operational procedures and troubleshooting
- **UAT-CHECKLIST.md**: User acceptance testing validation checklist
- **santiago-research-plan.md**: Santiago service research and development roadmap
- **.github/agents/**: Custom agent instructions for specialized tasks

## Notes for Copilot

- This project involves clinical decision support, so accuracy and safety are paramount
- Always run tests after making changes to ensure clinical logic remains correct
- When working with Santiago service, maintain the four-layer architecture integrity
- Reference existing agent instructions in `.github/agents/` for specialized guidance
- Follow established patterns in the codebase for consistency
- Document any changes that affect clinical logic or FHIR-CPG output
