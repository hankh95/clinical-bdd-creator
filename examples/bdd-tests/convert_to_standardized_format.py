#!/usr/bin/env python3
"""
BDD Test Format Conversion Script

This script helps convert existing BDD test examples to the standardized format
as defined in BDD_FORMAT_STANDARDIZATION.md.

Usage:
    python convert_to_standardized_format.py --input <input_dir> --output <output_dir>
    
Example:
    python convert_to_standardized_format.py --input examples/bdd-tests/unsorted/ --output examples/bdd-tests/scenarios/
"""

import argparse
import os
import yaml
from pathlib import Path
from datetime import datetime


def generate_scenario_id(domain, category, condition):
    """
    Generate a unique scenario ID following the hierarchical structure.
    
    Format: {domain}-{category}-{condition}-{sequence}
    
    Args:
        domain: Clinical domain (e.g., cardiology, oncology, primary-care)
        category: Scenario category (e.g., treatment-recommendation, diagnosis, monitoring)
        condition: Medical condition (e.g., hfref, afib, diabetes)
    
    Returns:
        Base ID without sequence number (sequence should be added based on existing IDs)
    """
    domain = domain.lower().replace(' ', '-')
    category = category.lower().replace(' ', '-')
    condition = condition.lower().replace(' ', '-')
    
    return f"{domain}-{category}-{condition}"


def get_next_sequence(base_id, output_dir):
    """
    Find the next available sequence number for a given base ID.
    
    Args:
        base_id: Base scenario ID without sequence
        output_dir: Output directory to check for existing IDs
    
    Returns:
        Next sequence number (e.g., "001", "002")
    """
    existing_files = list(Path(output_dir).glob(f"{base_id}-*.yaml"))
    
    if not existing_files:
        return "001"
    
    # Extract sequence numbers from existing files
    sequences = []
    for file in existing_files:
        parts = file.stem.split('-')
        if len(parts) >= 4 and parts[-1].isdigit():
            sequences.append(int(parts[-1]))
    
    if sequences:
        next_seq = max(sequences) + 1
        return f"{next_seq:03d}"
    
    return "001"


def create_clinical_yaml_template(scenario_id, domain, category, condition, original_file):
    """
    Create a template for the clinical scenario YAML file.
    
    Returns:
        Dictionary representing the YAML structure
    """
    template = {
        'scenario': {
            'id': scenario_id,
            'title': 'TODO: Add descriptive title',
            'domain': domain,
            'category': category,
            'condition': condition,
            'version': '1.0',
            'created': datetime.now().strftime('%Y-%m-%d'),
            'author': 'Clinical BDD Creator',
            'guidelines': [
                {
                    'name': 'TODO: Add guideline name',
                    'url': 'TODO: Add guideline URL or reference'
                }
            ]
        },
        'clinical': {
            'patient': {
                'demographics': {
                    'age': 'TODO: Add age',
                    'gender': 'TODO: Add gender'
                },
                'presentation': {
                    'chief_complaint': 'TODO: Add chief complaint',
                    'symptoms': []
                }
            },
            'diagnosis': {
                'primary': 'TODO: Add primary diagnosis',
                'status': 'TODO: Add status'
            },
            'vitals': {},
            'labs': {},
            'medications': {
                'current': [],
                'allergies': []
            },
            'comorbidities': [],
            'contraindications': []
        },
        'expectations': {
            'recommendations': [],
            'monitoring': [],
            'education': {
                'topics': []
            }
        },
        'testing': {
            'complexity': 'TODO: basic, advanced, or expert',
            'fidelity': 'TODO: low, medium, or high',
            'priority': 'TODO: P1, P2, or P3',
            'tags': [],
            'clinical_decision_points': [],
            'edge_cases': []
        },
        'source': {
            'original_file': original_file,
            'original_location': 'examples/bdd-tests/unsorted/',
            'migration_date': datetime.now().strftime('%Y-%m-%d'),
            'notes': 'Converted to standardized format - requires manual clinical data entry'
        }
    }
    
    return template


def create_feature_template(scenario_id, domain, category, title):
    """
    Create a template for the Gherkin feature file.
    
    Returns:
        String containing the feature file template
    """
    template = f"""# Clinical Scenario ID: {scenario_id}
# Title: {title}
# Domain: {domain.title()} | Category: {category.replace('-', ' ').title()}
# Guidelines: TODO: Add guidelines
# Complexity: TODO | Fidelity: TODO | Priority: TODO

Feature: {title}

  As a clinical decision support system
  I want to TODO: describe the goal
  So that TODO: describe the benefit

  Background:
    Given TODO: describe the patient scenario
    And TODO: add additional context

  Scenario: TODO: First scenario name
    Given TODO: initial conditions
    When TODO: action or evaluation
    Then TODO: expected outcome
    And TODO: additional expectations

  Scenario: TODO: Second scenario name
    Given TODO: initial conditions
    When TODO: action or evaluation
    Then TODO: expected outcome
    And TODO: additional expectations
"""
    
    return template


def create_assertions_template(scenario_id, guideline):
    """
    Create a template for the assertions YAML file.
    
    Returns:
        Dictionary representing the assertions structure
    """
    template = {
        'scenario_id': scenario_id,
        'validation_level': 'clinical-outcome',
        'guideline': guideline,
        'assertions': [
            {
                'id': 'patient-resource-exists',
                'description': 'Bundle has a Patient resource',
                'severity': 'error',
                'fhirpath': 'entry.resource.ofType(Patient).exists()',
                'expect': True,
                'rationale': 'Valid FHIR bundle must contain patient'
            },
            {
                'id': 'TODO-add-assertion-id',
                'description': 'TODO: Add assertion description',
                'severity': 'error',
                'fhirpath': 'TODO: Add FHIRPath expression',
                'expect': True,
                'rationale': 'TODO: Add rationale'
            }
        ],
        'contraindications': [
            {
                'id': 'TODO-add-contraindication-id',
                'description': 'TODO: Add contraindication check',
                'severity': 'error',
                'fhirpath': 'TODO: Add FHIRPath expression',
                'rationale': 'TODO: Add rationale'
            }
        ]
    }
    
    return template


def convert_scenario(input_file, output_dir, domain, category, condition):
    """
    Convert a single BDD test to standardized format.
    
    Args:
        input_file: Path to the original file
        output_dir: Directory to output the standardized files
        domain: Clinical domain
        category: Scenario category
        condition: Medical condition
    """
    # Generate scenario ID
    base_id = generate_scenario_id(domain, category, condition)
    sequence = get_next_sequence(base_id, output_dir)
    scenario_id = f"{base_id}-{sequence}"
    
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Generate file paths
    yaml_path = Path(output_dir) / f"{scenario_id}.yaml"
    feature_path = Path(output_dir) / f"{scenario_id}.feature"
    assert_path = Path(output_dir) / f"{scenario_id}.assert.yaml"
    
    # Create clinical YAML
    clinical_yaml = create_clinical_yaml_template(
        scenario_id, domain, category, condition, Path(input_file).name
    )
    
    with open(yaml_path, 'w') as f:
        yaml.dump(clinical_yaml, f, default_flow_style=False, sort_keys=False, indent=2)
    
    print(f"Created: {yaml_path}")
    
    # Create feature file
    feature_content = create_feature_template(
        scenario_id, domain, category, clinical_yaml['scenario']['title']
    )
    
    with open(feature_path, 'w') as f:
        f.write(feature_content)
    
    print(f"Created: {feature_path}")
    
    # Create assertions file
    assertions = create_assertions_template(
        scenario_id, clinical_yaml['scenario']['guidelines'][0]['name']
    )
    
    with open(assert_path, 'w') as f:
        yaml.dump(assertions, f, default_flow_style=False, sort_keys=False, indent=2)
    
    print(f"Created: {assert_path}")
    
    print(f"\n✅ Conversion complete for scenario: {scenario_id}")
    print(f"⚠️  Manual steps required:")
    print(f"   1. Fill in TODO items in {yaml_path}")
    print(f"   2. Complete Gherkin scenarios in {feature_path}")
    print(f"   3. Add FHIRPath assertions in {assert_path}")
    print(f"   4. Verify clinical accuracy against guidelines\n")


def main():
    parser = argparse.ArgumentParser(
        description='Convert BDD tests to standardized format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert a single scenario
  python convert_to_standardized_format.py \\
    --input unsorted/example.feature \\
    --output scenarios/ \\
    --domain cardiology \\
    --category treatment-recommendation \\
    --condition afib

  # Interactive mode (prompts for details)
  python convert_to_standardized_format.py \\
    --input unsorted/example.feature \\
    --output scenarios/ \\
    --interactive
        """
    )
    
    parser.add_argument('--input', required=True, help='Input file path')
    parser.add_argument('--output', required=True, help='Output directory path')
    parser.add_argument('--domain', help='Clinical domain (e.g., cardiology, oncology)')
    parser.add_argument('--category', help='Category (e.g., treatment-recommendation)')
    parser.add_argument('--condition', help='Medical condition (e.g., afib, diabetes)')
    parser.add_argument('--interactive', action='store_true', help='Interactive mode')
    
    args = parser.parse_args()
    
    # Interactive mode
    if args.interactive:
        print("Interactive Conversion Mode")
        print("=" * 50)
        args.domain = input("Enter domain (e.g., cardiology, oncology, primary-care): ")
        args.category = input("Enter category (e.g., treatment-recommendation, diagnosis): ")
        args.condition = input("Enter condition (e.g., afib, diabetes, breast-cancer): ")
    
    # Validate required fields
    if not all([args.domain, args.category, args.condition]):
        parser.error("--domain, --category, and --condition are required (or use --interactive)")
    
    # Convert the scenario
    convert_scenario(args.input, args.output, args.domain, args.category, args.condition)


if __name__ == '__main__':
    main()
