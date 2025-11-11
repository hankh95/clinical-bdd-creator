#!/usr/bin/env python3
"""
Santiago: NeuroSymbolic Clinical Knowledge Graph Service

A Model Context Protocol (MCP) service that transforms clinical guidelines
into four-layer NeuroSymbolic knowledge graphs for clinical question answering.

Sister service to the Clinical BDD Creator, inspired by "The Old Man and the Sea" -
not just catching fish (converting guidelines), but providing wisdom and
revenue-generating services for guideline companies.

Author: GitHub Copilot
Date: November 9, 2025
"""

import json
import sys
import os
import asyncio
from pathlib import Path
from typing import Dict, Any, List, Optional, Union, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging

from document_loader import DocumentLoader, DocumentMetadata
from semantic_relationships import SemanticRelationships, RelationshipType

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SantiagoLayer(Enum):
    """Four-layer model layers for clinical knowledge representation"""
    RAW_TEXT = "raw_text"           # Layer 1: Original guideline content
    STRUCTURED_KNOWLEDGE = "structured_knowledge"  # Layer 2: Extracted concepts & relationships
    COMPUTABLE_LOGIC = "computable_logic"          # Layer 3: Rules, algorithms, decision logic
    EXECUTABLE_WORKFLOWS = "executable_workflows"   # Layer 4: DAGs, workflows, reasoning paths

class KnowledgeRepresentation(Enum):
    """Types of knowledge representation in the graph"""
    CONCEPT = "concept"             # Clinical concepts (conditions, medications, procedures)
    RELATIONSHIP = "relationship"   # Relationships between concepts
    RULE = "rule"                   # Clinical rules and logic
    WORKFLOW = "workflow"           # Clinical workflows and pathways
    EVIDENCE = "evidence"           # Evidence supporting clinical knowledge
    CONTEXT = "context"             # Clinical context and constraints

@dataclass
class GraphNode:
    """Node in the NeuroSymbolic knowledge graph"""
    id: str
    layer: SantiagoLayer
    node_type: KnowledgeRepresentation
    content: Dict[str, Any]
    metadata: Dict[str, Any]
    relationships: Optional[List[Dict[str, Any]]] = None
    symbolic_logic: Optional[Dict[str, Any]] = None  # For executable logic
    neural_embeddings: Optional[List[float]] = None  # For similarity matching

    def __post_init__(self):
        if self.relationships is None:
            self.relationships = []

@dataclass
class GraphQuery:
    """Query for the knowledge graph"""
    question: str
    context: Dict[str, Any]
    reasoning_depth: str = "standard"  # standard, deep, comprehensive
    include_evidence: bool = True
    confidence_threshold: float = 0.7

@dataclass
class SantiagoResponse:
    """Response from Santiago service"""
    query: GraphQuery
    answer: str
    confidence: float
    evidence: List[Dict[str, Any]]
    reasoning_path: List[Dict[str, Any]]
    alternative_answers: Optional[List[Dict[str, Any]]] = None
    processing_time: float = 0.0

    def __post_init__(self):
        if self.alternative_answers is None:
            self.alternative_answers = []

class SantiagoService:
    """
    Santiago: NeuroSymbolic Clinical Knowledge Graph Service

    Transforms clinical guidelines into four-layer knowledge graphs and provides
    clinical question answering capabilities using hybrid symbolic-neural reasoning.
    """

    def __init__(self):
        self.initialized = False
        self.knowledge_graph: Dict[str, GraphNode] = {}
        self.document_loader = DocumentLoader()  # Initialize document loader for Layer 0
        self.semantic_relationships = SemanticRelationships()  # Initialize semantic relationships for Layer 1
        self.layer_processors = {
            SantiagoLayer.RAW_TEXT: self._process_raw_text,
            SantiagoLayer.STRUCTURED_KNOWLEDGE: self._process_structured_knowledge,
            SantiagoLayer.COMPUTABLE_LOGIC: self._process_computable_logic,
            SantiagoLayer.EXECUTABLE_WORKFLOWS: self._process_executable_workflows
        }

        # Initialize service components
        self._initialize_components()

    def _initialize_components(self):
        """Initialize Santiago service components"""
        logger.info("Initializing Santiago service components...")

        # TODO: Initialize CosmosDB/Gremlin connection
        # TODO: Initialize FHIR-CPG processor
        # TODO: Initialize NeuroSymbolic reasoning engine
        # TODO: Initialize NLP components for guideline processing

        self.initialized = True
        logger.info("Santiago service initialized successfully")

    async def process_guideline(self, guideline_content: Union[str, Path],
                               guideline_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a clinical guideline through the four-layer model

        Args:
            guideline_content: Raw guideline content or file path
            guideline_metadata: Metadata about the guideline (title, source, date, etc.)

        Returns:
            Processing results with four-layer representations
        """
        logger.info(f"Processing guideline: {guideline_metadata.get('title', 'Unknown')}")

        # Layer 1: Raw text processing
        raw_nodes = await self.layer_processors[SantiagoLayer.RAW_TEXT](
            guideline_content, guideline_metadata
        )

        # Layer 2: Structured knowledge extraction
        structured_nodes = await self.layer_processors[SantiagoLayer.STRUCTURED_KNOWLEDGE](
            raw_nodes, guideline_metadata
        )

        # Layer 3: Computable logic formalization
        logic_nodes = await self.layer_processors[SantiagoLayer.COMPUTABLE_LOGIC](
            structured_nodes, guideline_metadata
        )

        # Layer 4: Executable workflow compilation
        workflow_nodes = await self.layer_processors[SantiagoLayer.EXECUTABLE_WORKFLOWS](
            logic_nodes, guideline_metadata
        )

        # Store in knowledge graph
        await self._store_in_graph(workflow_nodes)

        return {
            "guideline_id": guideline_metadata.get("id"),
            "layers": {
                "raw_text": len(raw_nodes),
                "structured_knowledge": len(structured_nodes),
                "computable_logic": len(logic_nodes),
                "executable_workflows": len(workflow_nodes)
            },
            "total_nodes": len(raw_nodes) + len(structured_nodes) + len(logic_nodes) + len(workflow_nodes),
            "processing_status": "completed"
        }

    async def answer_clinical_question(self, query: GraphQuery) -> SantiagoResponse:
        """
        Answer a clinical question using NeuroSymbolic reasoning over the knowledge graph

        Args:
            query: Clinical question with context

        Returns:
            SantiagoResponse with answer, evidence, and reasoning
        """
        start_time = asyncio.get_event_loop().time()

        logger.info(f"Processing clinical question: {query.question[:100]}...")

        # Parse and understand the question
        parsed_query = await self._parse_clinical_question(query)

        # Perform graph traversal and reasoning
        reasoning_result = await self._perform_neurosymbolic_reasoning(parsed_query)

        # Generate response with evidence
        response = await self._generate_response(query, reasoning_result)

        # Calculate processing time
        response.processing_time = asyncio.get_event_loop().time() - start_time

        logger.info(".2f")
        return response

    def create_anchor_reference(self, doc_id: str, section_id: str,
                              anchor_text: str, anchor_type: str,
                              position: int, context: str,
                              higher_level_asset_id: str = None) -> str:
        """
        Create a deep link reference from higher-level assets back to source text

        Based on lessons learned: "We should be able to trace back any asset, logic,
        decision table, workflow back to the text."

        Args:
            doc_id: Document identifier
            section_id: Section identifier
            anchor_text: Text being referenced
            anchor_type: Type of anchor (recommendation, table, figure, etc.)
            position: Character position in document
            context: Surrounding context text
            higher_level_asset_id: ID of the higher-level asset this anchors to

        Returns:
            Anchor reference ID
        """
        anchor_id = self.document_loader.create_anchor_reference(
            doc_id, section_id, anchor_text, anchor_type, position, context
        )

        # Store reference to higher-level asset for bidirectional linking
        if higher_level_asset_id:
            # TODO: Store bidirectional link in knowledge graph
            logger.info(f"Created anchor {anchor_id} linking to asset {higher_level_asset_id}")

        return anchor_id

    def resolve_anchor_reference(self, anchor_id: str) -> Dict[str, Any]:
        """
        Resolve an anchor reference to get full context and traceability

        Args:
            anchor_id: Anchor reference identifier

        Returns:
            Full anchor context with document and section information
        """
        return self.document_loader.resolve_anchor_reference(anchor_id)

    def get_document_content(self, doc_id: str, section_id: Optional[str] = None) -> str:
        """
        Retrieve document content for traceability and validation

        Args:
            doc_id: Document identifier
            section_id: Optional section identifier

        Returns:
            Document or section content
        """
        return self.document_loader.get_document_content(doc_id, section_id)

    async def _process_raw_text(self, content: Union[str, Path],
                               metadata: Dict[str, Any]) -> List[GraphNode]:
        """
        Process raw guideline text into Layer 0 nodes with deep linking capabilities

        Based on lessons learned: Load original documents and create Layer 0 in graph
        for deep asset linking from all other layers back to source text.
        """
        logger.info(f"Processing Layer 0 for guideline: {metadata.get('title', 'Unknown')}")

        # Load document using document loader
        doc_metadata = self.document_loader.load_document(content, metadata)

        # Create Layer 0 nodes for each section
        nodes = []

        # Create main document node
        doc_node = GraphNode(
            id=f"{doc_metadata.id}_doc",
            layer=SantiagoLayer.RAW_TEXT,
            node_type=KnowledgeRepresentation.CONTEXT,
            content={
                "document_id": doc_metadata.id,
                "title": doc_metadata.title,
                "source": doc_metadata.source,
                "sections_count": len(doc_metadata.sections),
                "toc": doc_metadata.toc,
                "checksum": doc_metadata.checksum
            },
            metadata={
                **metadata,
                "processing_layer": "raw_text",
                "document_metadata": asdict(doc_metadata),
                "layer": "L0",
                "loaded_at": doc_metadata.loaded_at
            }
        )
        nodes.append(doc_node)

        # Create section nodes with deep linking capabilities
        for section_data in doc_metadata.sections:
            section_node = GraphNode(
                id=f"{doc_metadata.id}_section_{section_data['id']}",
                layer=SantiagoLayer.RAW_TEXT,
                node_type=KnowledgeRepresentation.CONTEXT,
                content={
                    "section_id": section_data["id"],
                    "title": section_data["title"],
                    "content": section_data["content"][:2000] + "..." if len(section_data["content"]) > 2000 else section_data["content"],
                    "level": section_data["level"],
                    "document_id": doc_metadata.id,
                    "full_content_available": True
                },
                metadata={
                    **metadata,
                    "processing_layer": "raw_text",
                    "section_metadata": section_data,
                    "document_id": doc_metadata.id,
                    "layer": "L0",
                    "parent_id": section_data.get("parent_id"),
                    "subsections": section_data.get("subsections", []),
                    "anchors": section_data.get("anchors", [])
                }
            )
            nodes.append(section_node)

        logger.info(f"Created {len(nodes)} Layer 0 nodes for document {doc_metadata.id}")
        return nodes

    async def _process_structured_knowledge(self, input_nodes: List[GraphNode],
                                          metadata: Dict[str, Any]) -> List[GraphNode]:
        """
        Extract structured knowledge using defined semantic relationships

        Layer 1: Extract clinical concepts and relationships from raw text using
        the core semantic relationships (treats, investigates, complicates, risk-factor).
        """
        logger.info("Processing Layer 1: Structured Knowledge Extraction")

        structured_nodes = []

        for node in input_nodes:
            if node.node_type == KnowledgeRepresentation.CONTEXT and "section_" in node.id:
                # Process section nodes for concept and relationship extraction
                section_content = node.content.get("content", "")
                section_title = node.content.get("title", "")

                # Extract concepts and relationships from section content
                concepts, relationships = self._extract_clinical_knowledge(
                    section_content, section_title, node.metadata.get("document_id")
                )

                # Create concept nodes
                for concept in concepts:
                    concept_node = GraphNode(
                        id=f"{node.id}_concept_{concept['id']}",
                        layer=SantiagoLayer.STRUCTURED_KNOWLEDGE,
                        node_type=KnowledgeRepresentation.CONCEPT,
                        content={
                            "concept_id": concept["id"],
                            "name": concept["name"],
                            "type": concept["type"],
                            "context": concept["context"],
                            "confidence": concept["confidence"],
                            "source_section": node.id,
                            "document_id": node.metadata.get("document_id")
                        },
                        metadata={
                            **metadata,
                            "processing_layer": "structured_knowledge",
                            "layer": "L1",
                            "extraction_method": "semantic_relationships",
                            "concept_type": concept["type"]
                        }
                    )
                    structured_nodes.append(concept_node)

                # Create relationship nodes
                for relationship in relationships:
                    rel_node = GraphNode(
                        id=f"{node.id}_relationship_{relationship['id']}",
                        layer=SantiagoLayer.STRUCTURED_KNOWLEDGE,
                        node_type=KnowledgeRepresentation.RELATIONSHIP,
                        content={
                            "relationship_id": relationship["id"],
                            "type": relationship["type"].value,
                            "source_concept": relationship["source_concept"],
                            "target_concept": relationship["target_concept"],
                            "properties": relationship["properties"],
                            "evidence_text": relationship["evidence_text"],
                            "confidence": relationship["confidence"],
                            "source_section": node.id,
                            "document_id": node.metadata.get("document_id")
                        },
                        metadata={
                            **metadata,
                            "processing_layer": "structured_knowledge",
                            "layer": "L1",
                            "extraction_method": "semantic_relationships",
                            "relationship_type": relationship["type"].value
                        },
                        relationships=[
                            {
                                "type": relationship["type"].value,
                                "source": relationship["source_concept"],
                                "target": relationship["target_concept"],
                                "properties": relationship["properties"]
                            }
                        ]
                    )
                    structured_nodes.append(rel_node)

        logger.info(f"Created {len(structured_nodes)} structured knowledge nodes from {len(input_nodes)} input nodes")
        return structured_nodes

    async def _process_computable_logic(self, input_nodes: List[GraphNode],
                                      metadata: Dict[str, Any]) -> List[GraphNode]:
        """Formalize computable logic from structured knowledge"""
        # TODO: Implement FHIR-CPG logic formalization
        # - Rule extraction and representation
        # - Decision algorithms
        # - Clinical logic expressions (CQL/ELM)

        nodes = []
        for node in input_nodes:
            logic_node = GraphNode(
                id=f"{node.id}_logic",
                layer=SantiagoLayer.COMPUTABLE_LOGIC,
                node_type=KnowledgeRepresentation.RULE,
                content={
                    "rules": [],  # Placeholder for FHIR-CPG rules
                    "algorithms": [],  # Placeholder for decision algorithms
                    "logic_expressions": {}  # Placeholder for CQL/ELM
                },
                metadata={**metadata, "processing_layer": "computable_logic"},
                symbolic_logic={
                    "execution_engine": "fhir-cpg",
                    "logic_type": "conditional_rules"
                }
            )
            nodes.append(logic_node)

        logger.info(f"Created {len(nodes)} computable logic nodes")
        return nodes

    async def _process_executable_workflows(self, input_nodes: List[GraphNode],
                                          metadata: Dict[str, Any]) -> List[GraphNode]:
        """Compile executable workflows from logic nodes"""
        # TODO: Implement workflow compilation
        # - DAG construction from clinical pathways
        # - Workflow execution logic
        # - Integration with Gremlin traversal patterns

        nodes = []
        for node in input_nodes:
            workflow_node = GraphNode(
                id=f"{node.id}_workflow",
                layer=SantiagoLayer.EXECUTABLE_WORKFLOWS,
                node_type=KnowledgeRepresentation.WORKFLOW,
                content={
                    "workflow_dag": {},  # Placeholder for DAG structure
                    "execution_paths": [],  # Placeholder for traversal paths
                    "entry_points": [],  # Placeholder for workflow starts
                    "exit_points": []  # Placeholder for workflow ends
                },
                metadata={**metadata, "processing_layer": "executable_workflows"}
            )
            nodes.append(workflow_node)

        logger.info(f"Created {len(nodes)} executable workflow nodes")
        return nodes

    def _extract_clinical_knowledge(self, text: str, section_title: str,
                                  document_id: str) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Extract clinical concepts and relationships from text using semantic relationships

        This implements Layer 1 knowledge extraction using pattern matching and
        the defined semantic relationships.

        Args:
            text: Section text content
            section_title: Section title for context
            document_id: Source document identifier

        Returns:
            Tuple of (concepts, relationships) lists
        """
        concepts = []
        relationships = []
        concept_counter = 0
        relationship_counter = 0

        # Extract concepts using improved pattern matching
        all_concepts = self._extract_concepts_from_text(text, section_title, document_id)
        concepts.extend(all_concepts)
        concept_counter = len(concepts)

        # Extract relationships using sentence-level analysis
        all_relationships = self._extract_relationships_from_text(text, section_title, document_id)
        relationships.extend(all_relationships)
        relationship_counter = len(relationships)

        # Remove duplicate concepts (simple deduplication)
        unique_concepts = []
        seen_names = set()
        for concept in concepts:
            name_key = concept["name"].lower().strip('.')
            if name_key not in seen_names:
                unique_concepts.append(concept)
                seen_names.add(name_key)

        logger.info(f"Extracted {len(unique_concepts)} concepts and {len(relationships)} relationships from section '{section_title}'")
        return unique_concepts, relationships

    def _get_concept_patterns(self, concept_type: str) -> List[str]:
        """
        Get patterns for identifying concepts of a specific type

        Args:
            concept_type: Type of concept (medication, condition, etc.)

        Returns:
            List of patterns to match
        """
        # Simple pattern matching - can be enhanced with NLP/entity recognition
        patterns = {
            "medication": [
                "metformin", "insulin", "aspirin", "statin", "warfarin",
                "lisinopril", "amlodipine", "losartan", "hydrochlorothiazide"
            ],
            "condition": [
                "diabetes", "hypertension", "cancer", "heart disease", "stroke",
                "kidney disease", "obesity", "depression", "asthma", "copd"
            ],
            "intervention": [
                "treatment", "therapy", "surgery", "vaccination", "exercise",
                "diet", "medication", "procedure", "counseling", "monitoring"
            ],
            "diagnostic_test": [
                "blood test", "x-ray", "mri", "ct scan", "ultrasound", "ecg",
                "echocardiogram", "colonoscopy", "biopsy", "lab test"
            ],
            "risk_factor": [
                "smoking", "obesity", "family history", "age", "gender",
                "hypertension", "diabetes", "cholesterol", "stress"
            ]
        }

        return patterns.get(concept_type, [])

    def _get_relationship_patterns(self, rel_type: RelationshipType) -> List[Dict[str, str]]:
        """
        Get patterns for identifying specific relationship types

        Args:
            rel_type: Type of relationship

        Returns:
            List of pattern dictionaries with keywords and context
        """
        patterns = {
            RelationshipType.TREATS: [
                {"keyword": "treats", "context": "treatment"},
                {"keyword": "treat", "context": "treatment"},
                {"keyword": "used for", "context": "indication"},
                {"keyword": "indicated for", "context": "indication"},
                {"keyword": "prescribed for", "context": "prescription"},
                {"keyword": "effective for", "context": "efficacy"}
            ],
            RelationshipType.INVESTIGATES: [
                {"keyword": "diagnoses", "context": "diagnosis"},
                {"keyword": "detects", "context": "detection"},
                {"keyword": "screens for", "context": "screening"},
                {"keyword": "used to diagnose", "context": "diagnosis"},
                {"keyword": "test for", "context": "testing"}
            ],
            RelationshipType.COMPLICATES: [
                {"keyword": "complicates", "context": "complication"},
                {"keyword": "worsens", "context": "worsening"},
                {"keyword": "leads to", "context": "progression"},
                {"keyword": "causes", "context": "causation"},
                {"keyword": "increases risk of", "context": "risk"}
            ],
            RelationshipType.RISK_FACTOR: [
                {"keyword": "risk factor", "context": "risk"},
                {"keyword": "increases risk", "context": "risk"},
                {"keyword": "associated with", "context": "association"},
                {"keyword": "predisposes to", "context": "predisposition"}
            ]
        }

        return patterns.get(rel_type, [])

    def _extract_concepts_from_text(self, text: str, section_title: str,
                                  document_id: str) -> List[Dict[str, Any]]:
        """
        Extract clinical concepts from text using improved pattern matching

        Args:
            text: Source text
            section_title: Section title
            document_id: Document ID

        Returns:
            List of concept dictionaries
        """
        concepts = []
        concept_counter = 0

        # Define concept patterns with better matching
        concept_patterns = {
            "medication": [
                r'\b(lisinopril|amlodipine|losartan|hydrochlorothiazide|metformin|insulin|aspirin|statin|warfarin)\b'
            ],
            "condition": [
                r'\b(diabetes|hypertension|cancer|heart disease|stroke|kidney disease|obesity|depression|asthma|copd)\b'
            ],
            "intervention": [
                r'\b(treatment|therapy|surgery|vaccination|exercise|diet|medication|medications|procedure|counseling|monitoring)\b'
            ],
            "diagnostic_test": [
                r'\b(blood test|x-ray|mri|ct scan|ultrasound|ecg|echocardiogram|colonoscopy|biopsy|lab test)\b'
            ],
            "risk_factor": [
                r'\b(smoking|obesity|family history|age|gender|hypertension|diabetes|cholesterol|stress)\b'
            ]
        }

        import re

        # Extract concepts using regex patterns
        for concept_type, patterns in concept_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    concept_text = match.group(0)

                    # Get context around the concept
                    start_pos = max(0, match.start() - 50)
                    end_pos = min(len(text), match.end() + 50)
                    context = text[start_pos:end_pos]

                    concept = {
                        "id": f"concept_{concept_counter}",
                        "name": concept_text,
                        "type": concept_type,
                        "context": context,
                        "confidence": 0.8,  # High confidence for direct pattern matches
                        "source_pattern": pattern,
                        "section_title": section_title,
                        "document_id": document_id
                    }
                    concepts.append(concept)
                    concept_counter += 1

        return concepts

    def _extract_relationships_from_text(self, text: str, section_title: str,
                                       document_id: str) -> List[Dict[str, Any]]:
        """
        Extract relationships from text using sentence-level analysis

        Args:
            text: Source text
            section_title: Section title
            document_id: Document ID

        Returns:
            List of relationship dictionaries
        """
        relationships = []
        relationship_counter = 0

        import re

        # Split text into sentences for better analysis
        sentences = re.split(r'[.!?]+', text)

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            sentence_lower = sentence.lower()

            # Check for each relationship type
            for rel_type in self.semantic_relationships.relationships.keys():
                rel_def = self.semantic_relationships.relationships[rel_type]
                patterns = self._get_relationship_patterns(rel_type)

                for pattern in patterns:
                    keyword = pattern["keyword"].lower()
                    if keyword in sentence_lower:
                        # Extract relationship using sentence context
                        rel = self._extract_relationship_from_sentence(
                            sentence, keyword, rel_type, document_id
                        )
                        if rel:
                            relationship = {
                                "id": f"relationship_{relationship_counter}",
                                "type": rel_type,
                                "source_concept": rel["source"],
                                "target_concept": rel["target"],
                                "properties": rel["properties"],
                                "evidence_text": sentence,
                                "confidence": rel["confidence"],
                                "pattern_used": keyword,
                                "section_title": section_title,
                                "document_id": document_id
                            }
                            relationships.append(relationship)
                            relationship_counter += 1

        return relationships

    def _extract_relationship_from_sentence(self, sentence: str, keyword: str,
                                          rel_type: RelationshipType, document_id: str) -> Optional[Dict[str, Any]]:
        """
        Extract a single relationship from a sentence containing a keyword

        Args:
            sentence: Sentence containing the relationship
            keyword: Relationship keyword found in sentence
            rel_type: Type of relationship
            document_id: Document ID

        Returns:
            Relationship dictionary or None if extraction fails
        """
        rel_def = self.semantic_relationships.get_relationship(rel_type)

        # Split sentence around the keyword
        keyword_pos = sentence.lower().find(keyword)
        before_keyword = sentence[:keyword_pos].strip()
        after_keyword = sentence[keyword_pos + len(keyword):].strip()

        # Extract potential source and target entities
        source_candidates = self._find_entities_in_text(before_keyword, rel_def.domain)
        target_candidates = self._find_entities_in_text(after_keyword, rel_def.range)

        # Special handling for collective medication references
        if rel_type == RelationshipType.TREATS and not source_candidates:
            # Look for collective medication terms before the keyword
            collective_med_terms = ['medications', 'drugs', 'treatment', 'therapy']
            for term in collective_med_terms:
                if term.lower() in before_keyword.lower():
                    # For collective terms, create relationship with the collective term as source
                    # and the condition as target
                    source_candidates = [term]
                    break

        if not source_candidates or not target_candidates:
            return None

        # For now, take the first candidate (can be improved with better NLP)
        source = source_candidates[0]
        target = target_candidates[0]

        # Special handling for different relationship types
        properties = {}
        confidence = 0.6  # Base confidence

        if rel_type == RelationshipType.COMPLICATES:
            # "diabetes complicates hypertension" - diabetes (source) complicates hypertension (target)
            confidence = 0.7

        elif rel_type == RelationshipType.RISK_FACTOR:
            # "obesity is a risk factor for diabetes" - obesity (source) is risk factor for diabetes (target)
            confidence = 0.7

        elif rel_type == RelationshipType.TREATS:
            # "medications treat hypertension" - medications (source) treat hypertension (target)
            confidence = 0.8

        return {
            "source": source,
            "target": target,
            "properties": properties,
            "confidence": confidence
        }
        """
        Extract concept mentions from text around a pattern

        Args:
            text: Source text
            pattern: Pattern that triggered extraction

        Returns:
            List of concept mention dictionaries
        """
        mentions = []
        text_lower = text.lower()
        pattern_lower = pattern.lower()

        # Find pattern occurrences
        start = 0
        while True:
            pos = text_lower.find(pattern_lower, start)
            if pos == -1:
                break

            # Extract context around the pattern (word boundaries)
            word_start = text.rfind(' ', 0, pos) + 1
            word_end = text.find(' ', pos + len(pattern))
            if word_end == -1:
                word_end = len(text)

            concept_text = text[word_start:word_end].strip()

            # Get surrounding context
            context_start = max(0, pos - 100)
            context_end = min(len(text), pos + len(pattern) + 100)
            context = text[context_start:context_end]

            mention = {
                "text": concept_text,
                "position": pos,
                "context": context,
                "confidence": 0.8 if len(concept_text) > 3 else 0.5  # Simple confidence heuristic
            }
            mentions.append(mention)

            start = pos + 1

        return mentions

    def _extract_relationships(self, text: str, pattern: Dict[str, str],
                             rel_type: RelationshipType, document_id: str) -> List[Dict[str, Any]]:
        """
        Extract relationship triples from text around a pattern

        Args:
            text: Source text
            pattern: Pattern dictionary with keyword and context
            rel_type: Type of relationship to extract
            document_id: Source document ID

        Returns:
            List of relationship dictionaries
        """
        relationships = []
        text_lower = text.lower()
        keyword = pattern["keyword"].lower()

        # Find keyword occurrences
        start = 0
        while True:
            pos = text_lower.find(keyword, start)
            if pos == -1:
                break

            # Extract context around the relationship keyword
            context_start = max(0, pos - 200)
            context_end = min(len(text), pos + len(keyword) + 200)
            context = text[context_start:context_end]

            # Simple heuristic extraction (can be enhanced with NLP)
            # Look for potential source and target entities around the keyword
            rel_def = self.semantic_relationships.get_relationship(rel_type)

            # Try to identify source and target based on position relative to keyword
            before_keyword = text[context_start:pos].strip()
            after_keyword = text[pos + len(keyword):context_end].strip()

            # Extract potential entities (simplified - real implementation would use NER)
            source_candidates = self._find_entities_in_text(before_keyword, rel_def.domain)
            target_candidates = self._find_entities_in_text(after_keyword, rel_def.range)

            if source_candidates and target_candidates:
                relationship = {
                    "source": source_candidates[0],  # Take first candidate
                    "target": target_candidates[0],  # Take first candidate
                    "properties": {},
                    "evidence": context,
                    "confidence": 0.6  # Base confidence for pattern-based extraction
                }
                relationships.append(relationship)

            start = pos + 1

        return relationships

    def _find_entities_in_text(self, text: str, entity_type: str) -> List[str]:
        """
        Find entities of a specific type in text using regex patterns

        Args:
            text: Text to search
            entity_type: Type of entity to find

        Returns:
            List of found entity names
        """
        import re

        patterns = {
            "medication": [
                r'\b(lisinopril|amlodipine|losartan|hydrochlorothiazide|metformin|insulin|aspirin|statin|warfarin)\b'
            ],
            "condition": [
                r'\b(diabetes|hypertension|cancer|heart disease|stroke|kidney disease|obesity|depression|asthma|copd)\b'
            ],
            "intervention": [
                r'\b(treatment|therapy|surgery|vaccination|exercise|diet|medication|medications|procedure|counseling|monitoring)\b'
            ],
            "diagnostic_test": [
                r'\b(blood test|x-ray|mri|ct scan|ultrasound|ecg|echocardiogram|colonoscopy|biopsy|lab test)\b'
            ],
            "risk_factor": [
                r'\b(smoking|obesity|family history|age|gender|hypertension|diabetes|cholesterol|stress)\b'
            ]
        }

        entity_patterns = patterns.get(entity_type, [])
        found_entities = []

        for pattern in entity_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                found_entities.append(match.group(0))

        return found_entities

    async def _store_in_graph(self, nodes: List[GraphNode]):
        """Store nodes in the knowledge graph (CosmosDB/Gremlin)"""
        # TODO: Implement CosmosDB storage
        # - Graph schema mapping
        # - Gremlin query construction
        # - Batch insertion optimization

        for node in nodes:
            self.knowledge_graph[node.id] = node

        logger.info(f"Stored {len(nodes)} nodes in knowledge graph")

    async def _parse_clinical_question(self, query: GraphQuery) -> Dict[str, Any]:
        """Parse and understand clinical question"""
        # TODO: Implement clinical question parsing
        # - Intent recognition
        # - Entity extraction
        # - Context understanding

        return {
            "parsed_question": query.question,
            "intent": "clinical_guidance",  # Placeholder
            "entities": [],  # Placeholder
            "context": query.context
        }

    async def _perform_neurosymbolic_reasoning(self, parsed_query: Dict[str, Any]) -> Dict[str, Any]:
        """Perform NeuroSymbolic reasoning over the knowledge graph"""
        # TODO: Implement hybrid reasoning
        # - Graph traversal with Gremlin
        # - Symbolic logic execution
        # - Neural similarity matching
        # - Confidence score calculation

        return {
            "answer": "Based on current guidelines...",  # Placeholder
            "confidence": 0.85,
            "evidence": [],
            "reasoning_path": []
        }

    async def _generate_response(self, query: GraphQuery,
                               reasoning_result: Dict[str, Any]) -> SantiagoResponse:
        """Generate final response with evidence and reasoning"""
        # TODO: Implement response generation
        # - Evidence compilation
        # - Reasoning path documentation
        # - Alternative answers consideration

        return SantiagoResponse(
            query=query,
            answer=reasoning_result.get("answer", "Unable to determine answer"),
            confidence=reasoning_result.get("confidence", 0.0),
            evidence=reasoning_result.get("evidence", []),
            reasoning_path=reasoning_result.get("reasoning_path", [])
        )

    # MCP Protocol Handlers
    async def handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP initialize request"""
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {
                    "process_guideline": {
                        "description": "Process a clinical guideline into four-layer knowledge graph",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "guideline_content": {"type": "string"},
                                "guideline_metadata": {"type": "object"}
                            },
                            "required": ["guideline_content"]
                        }
                    },
                    "answer_question": {
                        "description": "Answer clinical questions using NeuroSymbolic reasoning",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "question": {"type": "string"},
                                "context": {"type": "object"},
                                "reasoning_depth": {"type": "string", "enum": ["standard", "deep", "comprehensive"]},
                                "include_evidence": {"type": "boolean"},
                                "confidence_threshold": {"type": "number"}
                            },
                            "required": ["question"]
                        }
                    },
                    "load_document": {
                        "description": "Load a clinical document for Layer 0 processing with deep linking",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "source": {"type": "string", "description": "File path, URL, or content string"},
                                "metadata": {"type": "object", "description": "Document metadata"}
                            },
                            "required": ["source", "metadata"]
                        }
                    },
                    "create_anchor": {
                        "description": "Create deep link reference from higher-level assets to source text",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "doc_id": {"type": "string"},
                                "section_id": {"type": "string"},
                                "anchor_text": {"type": "string"},
                                "anchor_type": {"type": "string"},
                                "position": {"type": "integer"},
                                "context": {"type": "string"},
                                "higher_level_asset_id": {"type": "string"}
                            },
                            "required": ["doc_id", "section_id", "anchor_text", "anchor_type", "position", "context"]
                        }
                    }
                }
            },
            "serverInfo": {
                "name": "Santiago",
                "version": "0.1.0",
                "description": "NeuroSymbolic Clinical Knowledge Graph Service"
            }
        }

    async def handle_process_guideline(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle guideline processing request"""
        try:
            result = await self.process_guideline(
                params["guideline_content"],
                params.get("guideline_metadata", {})
            )
            return {"result": result}
        except Exception as e:
            logger.error(f"Error processing guideline: {e}")
            return {"error": str(e)}

    async def handle_answer_question(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle clinical question answering request"""
        try:
            query = GraphQuery(
                question=params["question"],
                context=params.get("context", {}),
                reasoning_depth=params.get("reasoning_depth", "standard"),
                include_evidence=params.get("include_evidence", True),
                confidence_threshold=params.get("confidence_threshold", 0.7)
            )

            response = await self.answer_clinical_question(query)
            return {"result": asdict(response)}
        except Exception as e:
            logger.error(f"Error answering question: {e}")
            return {"error": str(e)}

    async def handle_load_document(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle document loading request"""
        try:
            doc_metadata = self.document_loader.load_document(
                params["source"],
                params.get("metadata", {})
            )
            return {"result": asdict(doc_metadata)}
        except Exception as e:
            logger.error(f"Error loading document: {e}")
            return {"error": str(e)}

    async def handle_create_anchor(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle anchor creation request"""
        try:
            anchor_id = self.create_anchor_reference(
                params["doc_id"],
                params["section_id"],
                params["anchor_text"],
                params["anchor_type"],
                params["position"],
                params["context"],
                params.get("higher_level_asset_id")
            )
            return {"result": {"anchor_id": anchor_id}}
        except Exception as e:
            logger.error(f"Error creating anchor: {e}")
            return {"error": str(e)}

async def main():
    """Main MCP server loop"""
    service = SantiagoService()

    # MCP stdio protocol implementation
    # TODO: Implement full MCP protocol handling
    logger.info("Santiago MCP service starting...")

    try:
        while True:
            # Read MCP message from stdin
            line = sys.stdin.readline()
            if not line:
                break

            try:
                message = json.loads(line.strip())
                logger.info(f"Received MCP message: {message.get('method', 'unknown')}")

                # Route to appropriate handler
                if message.get("method") == "initialize":
                    response = await service.handle_initialize(message.get("params", {}))
                elif message.get("method") == "tools/call" and message.get("params", {}).get("name") == "process_guideline":
                    response = await service.handle_process_guideline(message["params"].get("arguments", {}))
                elif message.get("method") == "tools/call" and message.get("params", {}).get("name") == "answer_question":
                    response = await service.handle_answer_question(message["params"].get("arguments", {}))
                elif message.get("method") == "tools/call" and message.get("params", {}).get("name") == "load_document":
                    response = await service.handle_load_document(message["params"].get("arguments", {}))
                elif message.get("method") == "tools/call" and message.get("params", {}).get("name") == "create_anchor":
                    response = await service.handle_create_anchor(message["params"].get("arguments", {}))
                else:
                    response = {"error": "Unknown method"}

                # Send response
                response_message = {
                    "jsonrpc": "2.0",
                    "id": message.get("id"),
                    "result": response
                }
                print(json.dumps(response_message), flush=True)

            except json.JSONDecodeError:
                logger.error("Invalid JSON received")
                continue

    except KeyboardInterrupt:
        logger.info("Santiago service shutting down...")

if __name__ == "__main__":
    asyncio.run(main())