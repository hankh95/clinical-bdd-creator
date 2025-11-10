#!/usr/bin/env python3
"""
Tests for Santiago: NeuroSymbolic Clinical Knowledge Graph Service

Tests the four-layer model processing and clinical question answering capabilities.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch
from pathlib import Path
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from santiago_service import (
    SantiagoService,
    SantiagoLayer,
    KnowledgeRepresentation,
    GraphNode,
    GraphQuery,
    SantiagoResponse
)


class TestSantiagoService:
    """Test cases for the Santiago service"""

    @pytest.fixture
    def service(self):
        """Create a Santiago service instance for testing"""
        return SantiagoService()

    @pytest.fixture
    def sample_guideline_metadata(self):
        """Sample guideline metadata for testing"""
        return {
            "id": "test_guideline_001",
            "title": "Hypertension Management Guidelines 2024",
            "source": "American Heart Association",
            "version": "2024.1",
            "publication_date": "2024-01-15",
            "url": "https://example.com/hta2024"
        }

    @pytest.fixture
    def sample_guideline_content(self):
        """Sample guideline content for testing"""
        return """
        Hypertension Management Guidelines

        1. Assessment and Diagnosis
        - Blood pressure should be measured using validated devices
        - Classification: Normal <120/80, Elevated 120-129/<80, Stage 1 130-139/80-89, Stage 2 ≥140/≥90

        2. Treatment Recommendations
        - Lifestyle modifications for all patients
        - Pharmacological treatment for Stage 1+ with cardiovascular risk
        - First-line medications: ACE inhibitors, ARBs, CCBs, Thiazide diuretics

        3. Monitoring and Follow-up
        - Regular blood pressure monitoring
        - Medication adherence assessment
        - Target BP <130/80 for most patients
        """

    def test_service_initialization(self, service):
        """Test that the service initializes correctly"""
        assert service.initialized is True
        assert isinstance(service.knowledge_graph, dict)
        assert len(service.layer_processors) == 4

    @pytest.mark.asyncio
    async def test_process_guideline_basic(self, service, sample_guideline_content, sample_guideline_metadata):
        """Test basic guideline processing through all layers"""
        result = await service.process_guideline(
            sample_guideline_content,
            sample_guideline_metadata
        )

        # Check result structure
        assert "guideline_id" in result
        assert "layers" in result
        assert "total_nodes" in result
        assert "processing_status" in result

        # Check that all layers are represented
        layers = result["layers"]
        assert "raw_text" in layers
        assert "structured_knowledge" in layers
        assert "computable_logic" in layers
        assert "executable_workflows" in layers

        # Check that nodes were created
        assert result["total_nodes"] > 0
        assert result["processing_status"] == "completed"

    @pytest.mark.asyncio
    async def test_raw_text_processing(self, service, sample_guideline_content, sample_guideline_metadata):
        """Test Layer 1: Raw text processing"""
        nodes = await service._process_raw_text(
            sample_guideline_content,
            sample_guideline_metadata
        )

        assert len(nodes) > 0
        node = nodes[0]
        assert node.layer == SantiagoLayer.RAW_TEXT
        assert node.node_type == KnowledgeRepresentation.CONCEPT
        assert "text" in node.content
        assert node.metadata["processing_layer"] == "raw_text"

    @pytest.mark.asyncio
    async def test_structured_knowledge_processing(self, service, sample_guideline_metadata):
        """Test Layer 2: Structured knowledge extraction"""
        # Create mock input nodes
        input_nodes = [
            GraphNode(
                id="test_raw_1",
                layer=SantiagoLayer.RAW_TEXT,
                node_type=KnowledgeRepresentation.CONCEPT,
                content={"text": "sample content"},
                metadata=sample_guideline_metadata
            )
        ]

        nodes = await service._process_structured_knowledge(
            input_nodes,
            sample_guideline_metadata
        )

        assert len(nodes) > 0
        node = nodes[0]
        assert node.layer == SantiagoLayer.STRUCTURED_KNOWLEDGE
        assert "concepts" in node.content
        assert node.metadata["processing_layer"] == "structured_knowledge"

    @pytest.mark.asyncio
    async def test_computable_logic_processing(self, service, sample_guideline_metadata):
        """Test Layer 3: Computable logic formalization"""
        # Create mock input nodes
        input_nodes = [
            GraphNode(
                id="test_structured_1",
                layer=SantiagoLayer.STRUCTURED_KNOWLEDGE,
                node_type=KnowledgeRepresentation.CONCEPT,
                content={"concepts": ["hypertension"]},
                metadata=sample_guideline_metadata
            )
        ]

        nodes = await service._process_computable_logic(
            input_nodes,
            sample_guideline_metadata
        )

        assert len(nodes) > 0
        node = nodes[0]
        assert node.layer == SantiagoLayer.COMPUTABLE_LOGIC
        assert node.node_type == KnowledgeRepresentation.RULE
        assert "rules" in node.content
        assert node.symbolic_logic is not None
        assert node.metadata["processing_layer"] == "computable_logic"

    @pytest.mark.asyncio
    async def test_executable_workflows_processing(self, service, sample_guideline_metadata):
        """Test Layer 4: Executable workflow compilation"""
        # Create mock input nodes
        input_nodes = [
            GraphNode(
                id="test_logic_1",
                layer=SantiagoLayer.COMPUTABLE_LOGIC,
                node_type=KnowledgeRepresentation.RULE,
                content={"rules": []},
                metadata=sample_guideline_metadata,
                symbolic_logic={"execution_engine": "fhir-cpg"}
            )
        ]

        nodes = await service._process_executable_workflows(
            input_nodes,
            sample_guideline_metadata
        )

        assert len(nodes) > 0
        node = nodes[0]
        assert node.layer == SantiagoLayer.EXECUTABLE_WORKFLOWS
        assert node.node_type == KnowledgeRepresentation.WORKFLOW
        assert "workflow_dag" in node.content
        assert node.metadata["processing_layer"] == "executable_workflows"

    @pytest.mark.asyncio
    async def test_clinical_question_answering(self, service):
        """Test clinical question answering"""
        query = GraphQuery(
            question="What is the target blood pressure for hypertension management?",
            context={"patient_age": 65, "comorbidities": ["diabetes"]},
            reasoning_depth="standard",
            include_evidence=True,
            confidence_threshold=0.7
        )

        response = await service.answer_clinical_question(query)

        assert isinstance(response, SantiagoResponse)
        assert response.query == query
        assert isinstance(response.answer, str)
        assert isinstance(response.confidence, float)
        assert isinstance(response.evidence, list)
        assert isinstance(response.reasoning_path, list)
        assert response.processing_time >= 0

    def test_mcp_initialization(self, service):
        """Test MCP protocol initialization"""
        # This would normally be async, but we'll test the structure
        # In a real test, we'd mock the async call
        assert hasattr(service, 'handle_initialize')
        assert hasattr(service, 'handle_process_guideline')
        assert hasattr(service, 'handle_answer_question')

    def test_graph_node_creation(self):
        """Test GraphNode dataclass creation"""
        node = GraphNode(
            id="test_node_001",
            layer=SantiagoLayer.RAW_TEXT,
            node_type=KnowledgeRepresentation.CONCEPT,
            content={"text": "test content"},
            metadata={"source": "test"}
        )

        assert node.id == "test_node_001"
        assert node.layer == SantiagoLayer.RAW_TEXT
        assert node.node_type == KnowledgeRepresentation.CONCEPT
        assert node.content["text"] == "test content"
        assert node.relationships == []
        assert node.symbolic_logic is None
        assert node.neural_embeddings is None

    def test_santiago_response_creation(self):
        """Test SantiagoResponse dataclass creation"""
        query = GraphQuery(question="Test question", context={})
        response = SantiagoResponse(
            query=query,
            answer="Test answer",
            confidence=0.85,
            evidence=[{"type": "guideline", "content": "test"}],
            reasoning_path=[{"step": "analysis"}]
        )

        assert response.query == query
        assert response.answer == "Test answer"
        assert response.confidence == 0.85
        assert len(response.evidence) == 1
        assert len(response.reasoning_path) == 1
        assert response.alternative_answers == []


# Integration tests (would require external services)
class TestSantiagoIntegration:
    """Integration tests for Santiago service"""

    @pytest.mark.skip(reason="Requires CosmosDB connection")
    def test_cosmosdb_integration(self):
        """Test integration with CosmosDB/Gremlin"""
        # TODO: Implement when CosmosDB is available
        pass

    @pytest.mark.skip(reason="Requires FHIR server")
    def test_fhir_integration(self):
        """Test integration with FHIR services"""
        # TODO: Implement when FHIR server is available
        pass

    @pytest.mark.skip(reason="Requires NeuroSymbolic models")
    def test_neurosymbolic_reasoning_integration(self):
        """Test NeuroSymbolic reasoning integration"""
        # TODO: Implement when models are available
        pass


if __name__ == "__main__":
    # Run basic tests
    pytest.main([__file__, "-v"])