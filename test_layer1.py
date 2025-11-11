#!/usr/bin/env python3
"""
Test Layer 1: Structured Knowledge Extraction with Semantic Relationships
"""

import sys
import asyncio
from pathlib import Path

# Add the santiago-service/src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "santiago-service" / "src"))

from santiago_service import SantiagoService, SantiagoLayer, KnowledgeRepresentation, GraphNode

async def test_layer1_extraction():
    """Test Layer 1 structured knowledge extraction"""

    print("🧠 Testing Layer 1: Structured Knowledge Extraction")
    print("=" * 60)

    # Initialize Santiago service
    service = SantiagoService()

    # Create a sample Layer 0 node (simulating document processing)
    sample_content = """
    Treatment Recommendations for Hypertension

    First-line medications for hypertension include:
    - Angiotensin-converting enzyme (ACE) inhibitors such as lisinopril
    - Angiotensin II receptor blockers (ARBs) such as losartan
    - Calcium channel blockers such as amlodipine
    - Thiazide diuretics such as hydrochlorothiazide

    These medications treat hypertension and reduce cardiovascular risk.
    Diabetes complicates hypertension management and increases stroke risk.
    Obesity is a risk factor for both hypertension and diabetes.
    """

    layer0_node = GraphNode(
        id="test_doc_section_1",
        layer=SantiagoLayer.RAW_TEXT,
        node_type=KnowledgeRepresentation.CONTEXT,
        content={
            "section_id": "section_1",
            "title": "Treatment Recommendations",
            "content": sample_content,
            "document_id": "test_guideline"
        },
        metadata={
            "document_id": "test_guideline",
            "processing_layer": "raw_text",
            "layer": "L0"
        }
    )

    print("📄 Sample clinical text:")
    print("-" * 40)
    print(sample_content.strip())
    print()

    # Process through Layer 1
    print("🔍 Extracting structured knowledge...")
    layer1_nodes = await service._process_structured_knowledge([layer0_node], {"test": True})

    print(f"✅ Created {len(layer1_nodes)} Layer 1 nodes")
    print()

    # Analyze extracted concepts
    concepts = [node for node in layer1_nodes if node.node_type == KnowledgeRepresentation.CONCEPT]
    relationships = [node for node in layer1_nodes if node.node_type == KnowledgeRepresentation.RELATIONSHIP]

    print("🏥 Extracted Concepts:")
    print("-" * 30)
    for concept in concepts:
        content = concept.content
        print(f"• {content['name']} ({content['type']}) - Confidence: {content['confidence']}")

    print()
    print("🔗 Extracted Relationships:")
    print("-" * 30)
    for rel in relationships:
        content = rel.content
        print(f"• {content['source_concept']} → {content['type']} → {content['target_concept']}")
        print(f"  Evidence: {content['evidence_text'][:100]}...")
        print(f"  Confidence: {content['confidence']}")
        print()

    # Validate core relationships from lessons learned
    core_relationships_found = set()
    for rel in relationships:
        rel_type = rel.content['type']
        if rel_type in ['treats', 'investigates', 'complicates', 'risk_factor']:
            core_relationships_found.add(rel_type)

    print("📋 Core Relationships Validation:")
    print("-" * 35)
    expected_core = {'treats', 'complicates', 'risk_factor'}
    print(f"Expected: {expected_core}")
    print(f"Found: {core_relationships_found}")
    print(f"Coverage: {len(core_relationships_found)}/{len(expected_core)} core relationships")

    if core_relationships_found == expected_core:
        print("✅ All core relationships from lessons learned successfully extracted!")
    else:
        missing = expected_core - core_relationships_found
        print(f"⚠️  Missing relationships: {missing}")

    print()
    print("🎉 Layer 1 structured knowledge extraction test completed!")
    print(f"Total: {len(concepts)} concepts, {len(relationships)} relationships extracted")

    return len(concepts) > 0 and len(relationships) > 0

if __name__ == "__main__":
    success = asyncio.run(test_layer1_extraction())
    sys.exit(0 if success else 1)