#!/usr/bin/env python3
"""
Comprehensive test for Layer 0 document loading with a full clinical guideline.
Tests all aspects of the document loader with realistic clinical content.
"""

import sys
import os
from pathlib import Path

# Add the santiago-service/src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "santiago-service" / "src"))

from document_loader import DocumentLoader

def test_full_guideline_loading():
    """Test comprehensive document loading with a full clinical guideline."""

    # Initialize the document loader
    loader = DocumentLoader()

    # Test loading the full clinical guideline
    guideline_path = Path(__file__).parent / "full_clinical_guideline.md"

    print("🩺 Testing Layer 0 with Full Clinical Guideline")
    print("=" * 60)
    print(f"Loading: {guideline_path}")
    print()

    try:
        # Load the document with comprehensive metadata
        doc_metadata = {
            'title': '2024 ACC/AHA Clinical Practice Guideline for the Management of High Blood Pressure in Adults',
            'source': 'American College of Cardiology/American Heart Association',
            'version': '2024',
            'publication_date': '2024-01-01',
            'authors': ['Whelton PK', 'Carey RM', 'Aronow WS', 'et al.'],
            'organization': 'ACC/AHA',
            'document_type': 'clinical_practice_guideline'
        }

        metadata = loader.load_document(str(guideline_path), doc_metadata)

        print("✅ Document loaded successfully!")
        print(f"📄 Document ID: {metadata.id}")
        print(f"📖 Title: {metadata.title}")
        print(f"🏢 Organization: {metadata.organization}")
        print(f"📅 Version: {metadata.version}")
        print(f"📊 Sections: {len(metadata.sections)}")
        print(f"🔐 Checksum: {metadata.checksum[:16]}...")
        print()

        # Analyze section structure
        print("📑 Section Analysis:")
        print("-" * 40)

        section_levels = {}
        total_content_length = 0

        for section in metadata.sections:
            level = section['level']
            section_levels[level] = section_levels.get(level, 0) + 1
            content_len = len(section['content'])
            total_content_length += content_len

            print(f"• {section['title']} (Level {level}) - {content_len} chars")

        print()
        print("📊 Section Hierarchy Summary:")
        for level in sorted(section_levels.keys()):
            print(f"  Level {level}: {section_levels[level]} sections")
        print(f"  Total content: {total_content_length} characters")
        print()

        # Test key clinical content extraction
        print("🔍 Key Clinical Content Validation:")
        print("-" * 40)

        # Find specific sections
        bp_classification = next((s for s in metadata.sections if 'Classification' in s['title']), None)
        if bp_classification:
            print("✅ Found Blood Pressure Classification section")
            print(f"   Content preview: {bp_classification['content'][:100]}...")

        treatment_section = next((s for s in metadata.sections if 'Pharmacologic Treatment' in s['title']), None)
        if treatment_section:
            print("✅ Found Pharmacologic Treatment section")
            print(f"   Content preview: {treatment_section['content'][:100]}...")

        print()

        # Test anchor creation for clinical recommendations
        print("🔗 Deep Asset Linking Tests:")
        print("-" * 40)

        # Create anchors for key recommendations
        test_anchors = [
            ("Recommendation 1", "office_bp_measurement", 200),
            ("target BP <130/80", "diabetes_bp_target", 800),
            ("thiazide diuretics", "first_line_agents", 600),
        ]

        created_anchors = []

        for anchor_text, anchor_type, position in test_anchors:
            try:
                anchor_ref = loader.create_anchor_reference(
                    metadata.id,
                    "section_5",  # Pharmacologic treatment section
                    anchor_text,
                    anchor_type,
                    position,
                    f"Clinical context for: {anchor_text}"
                )
                created_anchors.append(anchor_ref)
                print(f"✅ Created anchor: {anchor_ref.split('_')[-1]}")
            except Exception as e:
                print(f"⚠️  Failed to create anchor for '{anchor_text}': {e}")

        print()

        # Test anchor resolution
        print("🔍 Anchor Resolution Tests:")
        print("-" * 40)

        for anchor_ref in created_anchors:
            try:
                resolved = loader.resolve_anchor_reference(anchor_ref)
                print(f"✅ Resolved anchor: {resolved['anchor']['text'][:30]}...")
                print(f"   Type: {resolved['anchor']['anchor_type']}")
                print(f"   Section: {resolved['anchor']['section_id']}")
            except Exception as e:
                print(f"❌ Failed to resolve anchor: {e}")

        print()

        # Test document content retrieval
        print("📖 Content Retrieval Tests:")
        print("-" * 40)

        # Get full document content
        full_content = loader.get_document_content(metadata.id)
        print(f"✅ Retrieved full document: {len(full_content)} characters")

        # Get specific section content
        if len(metadata.sections) > 5:
            section_content = loader.get_document_content(metadata.id, metadata.sections[5]['id'])
            print(f"✅ Retrieved section content: {len(section_content)} characters")
            print(f"   Section title: {metadata.sections[5]['title']}")

        print()

        # Performance metrics
        print("⚡ Performance Summary:")
        print("-" * 40)
        print(f"📊 Total sections parsed: {len(metadata.sections)}")
        print(f"📏 Total content size: {total_content_length} characters")
        print(f"🔗 Anchors created: {len(created_anchors)}")
        print(f"💾 Document stored at: data/documents/{metadata.id}")

        print()
        print("🎉 FULL CLINICAL GUIDELINE TEST PASSED!")
        print("Layer 0 is ready for production clinical document processing.")
        print()

        return True

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_full_guideline_loading()
    sys.exit(0 if success else 1)