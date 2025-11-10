# Santiago: NeuroSymbolic Clinical Knowledge Graph Service

> *"But man is not made for defeat. A man can be destroyed but not defeated." - Ernest Hemingway, The Old Man and the Sea*

Santiago is a NeuroSymbolic clinical knowledge graph service that transforms clinical guidelines into four-layer knowledge representations and provides clinical question answering capabilities. Named after the fisherman in Hemingway's novel, Santiago represents the evolution from simple guideline conversion ("catching fish") to providing wisdom and revenue-generating services for guideline companies.

## Overview

Santiago implements a four-layer model for clinical knowledge representation:

1. **Layer 1 - Raw Text**: Original guideline content and structure
2. **Layer 2 - Structured Knowledge**: Extracted clinical concepts and relationships
3. **Layer 3 - Computable Logic**: Formalized clinical rules and decision algorithms
4. **Layer 4 - Executable Workflows**: DAG-based clinical pathways and reasoning workflows

The service uses hybrid NeuroSymbolic AI to combine:
- **Neural Components**: Similarity matching, concept embedding, pattern recognition
- **Symbolic Components**: Logical reasoning, rule execution, graph traversal

## Architecture

### Core Components

- **Guideline Processor**: Multi-format guideline ingestion (PDF, HTML, DOCX, JSON)
- **Four-Layer Converter**: Progressive knowledge formalization pipeline
- **NeuroSymbolic Engine**: Hybrid reasoning over knowledge graphs
- **Clinical QA Service**: Evidence-based question answering
- **MCP Interface**: Model Context Protocol for AI/human interaction

### Technology Stack

- **Graph Database**: Azure CosmosDB with Gremlin/TinkerPop
- **Clinical Standards**: FHIR, CPG, CRMI, CQL, ELM
- **AI/ML**: PyTorch, TensorFlow, spaCy, Transformers
- **Reasoning**: Custom NeuroSymbolic engine
- **Protocol**: Model Context Protocol (MCP)

## Installation

1. **Clone and navigate to the Santiago service directory:**
   ```bash
   cd santiago-service/
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install clinical NLP models (optional but recommended):**
   ```bash
   pip install scispacy
   python -m spacy download en_core_sci_sm
   python -m spacy download en_ner_bc5cdr_md
   ```

## Configuration

Edit `config/santiago_config.ini` to configure:

- **CosmosDB connection**: Graph database endpoint and credentials
- **FHIR services**: Clinical terminology and resource servers
- **NeuroSymbolic settings**: Embedding models and reasoning parameters
- **MCP settings**: Protocol configuration and timeouts

## Usage

### Basic Usage

```python
from santiago_service import SantiagoService, GraphQuery

# Initialize the service
service = SantiagoService()

# Process a clinical guideline
result = await service.process_guideline(
    guideline_content="path/to/guideline.pdf",
    guideline_metadata={
        "title": "Hypertension Guidelines 2024",
        "source": "AHA/ACC",
        "version": "2024.1"
    }
)

# Ask clinical questions
query = GraphQuery(
    question="What is the target blood pressure for diabetic patients?",
    context={"patient_conditions": ["diabetes", "hypertension"]},
    reasoning_depth="deep",
    include_evidence=True
)

response = await service.answer_clinical_question(query)
print(f"Answer: {response.answer}")
print(f"Confidence: {response.confidence}")
print(f"Evidence: {len(response.evidence)} sources")
```

### MCP Server Mode

Run as an MCP server for integration with AI assistants:

```bash
python src/santiago_service.py
```

The service exposes two main tools via MCP:

1. **process_guideline**: Convert clinical guidelines to knowledge graphs
2. **answer_question**: Answer clinical questions with evidence

### Command Line Interface

```bash
# Process a guideline
python -m santiago_service process --input guideline.pdf --output results.json

# Ask a question
python -m santiago_service ask "What medications treat hypertension?" --context patient.json

# Start MCP server
python -m santiago_service serve
```

## API Reference

### SantiagoService Class

#### Methods

- `process_guideline(content, metadata)`: Process guideline through four layers
- `answer_clinical_question(query)`: Answer clinical questions
- `handle_initialize(params)`: MCP initialization
- `handle_process_guideline(params)`: MCP guideline processing
- `handle_answer_question(params)`: MCP question answering

### Data Models

#### GraphNode
Represents a node in the knowledge graph:
```python
@dataclass
class GraphNode:
    id: str
    layer: SantiagoLayer
    node_type: KnowledgeRepresentation
    content: Dict[str, Any]
    metadata: Dict[str, Any]
    relationships: Optional[List[Dict[str, Any]]] = None
    symbolic_logic: Optional[Dict[str, Any]] = None
    neural_embeddings: Optional[List[float]] = None
```

#### GraphQuery
Clinical question with context:
```python
@dataclass
class GraphQuery:
    question: str
    context: Dict[str, Any]
    reasoning_depth: str = "standard"
    include_evidence: bool = True
    confidence_threshold: float = 0.7
```

#### SantiagoResponse
Response with answer and evidence:
```python
@dataclass
class SantiagoResponse:
    query: GraphQuery
    answer: str
    confidence: float
    evidence: List[Dict[str, Any]]
    reasoning_path: List[Dict[str, Any]]
    alternative_answers: Optional[List[Dict[str, Any]]] = None
    processing_time: float = 0.0
```

## Development

### Project Structure

```
santiago-service/
├── src/
│   └── santiago_service.py      # Main service implementation
├── tests/
│   └── test_santiago_service.py # Unit and integration tests
├── config/
│   └── santiago_config.ini      # Configuration file
├── docs/                        # Documentation
├── research/                    # Research notes and prototypes
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

### Testing

Run the test suite:

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src --cov-report=html tests/
```

### Code Quality

```bash
# Format code
black src/ tests/

# Type checking
mypy src/

# Linting
flake8 src/ tests/
```

## Research Areas

Santiago is built on several key research areas:

1. **NeuroSymbolic AI**: Hybrid neural-symbolic reasoning for clinical decision support
2. **Clinical Knowledge Graphs**: Graph-based representation of clinical guidelines
3. **FHIR-CPG Integration**: Computable clinical practice guidelines
4. **Graph Reasoning**: Gremlin-based traversal and inference
5. **Clinical NLP**: Medical concept extraction and normalization

See `research/` directory for detailed research plans and prototypes.

## Integration with BDD Creator

Santiago integrates with the Clinical BDD Creator as a sister service:

- **BDD Creator**: Generates test scenarios from guidelines
- **Santiago**: Provides four-layer knowledge graphs for deeper analysis

The services can work together to:
1. Convert guidelines to knowledge graphs (Santiago)
2. Generate comprehensive test suites (BDD Creator)
3. Provide clinical QA and reasoning (Santiago)

## Deployment

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
COPY config/ ./config/

EXPOSE 8000
CMD ["python", "src/santiago_service.py"]
```

### Azure Deployment

Santiago is designed for Azure deployment:

- **CosmosDB**: Graph database for knowledge storage
- **Azure Functions**: Serverless API endpoints
- **Azure AI**: Neural model hosting
- **Azure Monitor**: Observability and logging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Citation

If you use Santiago in your research, please cite:

```bibtex
@software{santiago2024,
  title={Santiago: NeuroSymbolic Clinical Knowledge Graph Service},
  author={GitHub Copilot},
  year={2024},
  url={https://github.com/your-org/santiago}
}
```

## Acknowledgments

- Inspired by Ernest Hemingway's *The Old Man and the Sea*
- Built on the Clinical BDD Creator foundation
- Leverages FHIR, CPG, and clinical informatics standards
- Powered by NeuroSymbolic AI research