#!/usr/bin/env python3
"""
BDD Generation POC - Minimal BDD Generator for Clinical Scenarios

This POC demonstrates converting simple clinical scenarios to Gherkin format.
It accepts JSON input and generates valid Gherkin scenarios with Given-When-Then structure.

Author: GitHub Copilot
Date: 2025-11-09
"""

import json
import sys
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ClinicalScenario:
    """Represents a clinical scenario to be converted to BDD"""
    scenario: str
    condition: str
    action: str
    context: str
    contraindications: Optional[List[str]] = None
    expected_outcome: Optional[str] = None


class BDDGenerator:
    """
    Converts clinical scenarios to Gherkin BDD format
    
    Supports:
    - Positive test cases (expected behavior)
    - Negative test cases (boundary conditions)
    - Clinical terminology and realistic assertions
    """
    
    def __init__(self):
        self.scenarios_generated = 0
    
    def generate_feature(self, scenario: ClinicalScenario) -> str:
        """
        Generate a complete Gherkin feature with positive and negative scenarios
        
        Args:
            scenario: ClinicalScenario object with clinical details
            
        Returns:
            str: Valid Gherkin feature text
        """
        feature_lines = []
        
        # Feature header
        feature_lines.append(f"Feature: {scenario.scenario}")
        feature_lines.append("")
        
        # Positive scenario
        positive = self._generate_positive_scenario(scenario)
        feature_lines.extend(positive)
        feature_lines.append("")
        
        # Negative scenario
        negative = self._generate_negative_scenario(scenario)
        feature_lines.extend(negative)
        
        self.scenarios_generated += 2
        
        return "\n".join(feature_lines)
    
    def _generate_positive_scenario(self, scenario: ClinicalScenario) -> List[str]:
        """Generate positive test case (expected behavior)"""
        lines = []
        
        # Extract key terms from condition
        condition_text = self._format_condition(scenario.condition)
        action_text = self._format_action(scenario.action)
        
        lines.append("  @positive @treatment")
        lines.append(f"  Scenario: Patient with {condition_text} receives appropriate treatment")
        
        # Given steps (setup)
        lines.append(f"    Given a patient with {condition_text}")
        
        if scenario.context:
            context_parts = scenario.context.split(',')
            for part in context_parts:
                lines.append(f"    And the patient is {part.strip()}")
        
        if scenario.contraindications:
            lines.append(f"    And the patient has no contraindications for {action_text}")
        
        # When step (action)
        algorithm_name = self._get_algorithm_name(scenario.scenario)
        lines.append(f"    When the {algorithm_name} algorithm is applied")
        
        # Then steps (assertions)
        lines.append(f"    Then {action_text} should be initiated")
        
        if scenario.expected_outcome:
            lines.append(f"    And {scenario.expected_outcome}")
        else:
            lines.append("    And the intervention should be documented in the medical record")
        
        return lines
    
    def _generate_negative_scenario(self, scenario: ClinicalScenario) -> List[str]:
        """Generate negative test case (boundary condition)"""
        lines = []
        
        # Create opposite condition
        negative_condition = self._create_negative_condition(scenario.condition)
        action_text = self._format_action(scenario.action)
        
        lines.append("  @negative @treatment")
        lines.append(f"  Scenario: Patient with {negative_condition} receives no treatment")
        
        # Given steps (setup with opposite condition)
        lines.append(f"    Given a patient with {negative_condition}")
        
        # When step (same algorithm)
        algorithm_name = self._get_algorithm_name(scenario.scenario)
        lines.append(f"    When the {algorithm_name} algorithm is applied")
        
        # Then steps (no action taken)
        lines.append("    Then no treatment should be initiated")
        lines.append("    And the patient should be monitored for changes")
        
        return lines
    
    def _format_condition(self, condition: str) -> str:
        """Format condition text for readability in Gherkin"""
        # Simple formatting - replace comparison operators
        formatted = condition.replace('>=', 'of').replace('>', 'above').replace('<=', 'below')
        return formatted.lower()
    
    def _format_action(self, action: str) -> str:
        """Format action text for Gherkin"""
        return action.lower()
    
    def _create_negative_condition(self, condition: str) -> str:
        """Create opposite/normal condition for negative test"""
        # Simple logic to create opposite condition
        if '>=' in condition:
            # Replace with below threshold
            parts = condition.split('>=')
            if len(parts) == 2:
                try:
                    # Try to parse threshold value, handling decimals and percentages
                    threshold_str = parts[1].split()[0].rstrip('%')
                    threshold = float(threshold_str)
                    normal_value = threshold - (threshold * 0.2)  # 20% below threshold
                    unit = parts[1].split()[1] if len(parts[1].split()) > 1 else ''
                    return f"{parts[0].strip()} of {normal_value:.1f} {unit}".strip()
                except (ValueError, IndexError):
                    # Fallback if parsing fails
                    return f"normal {parts[0].strip()}"
        
        return "normal " + condition.split()[0] if condition else "normal values"
    
    def _get_algorithm_name(self, scenario_name: str) -> str:
        """Extract algorithm name from scenario"""
        return scenario_name.lower().replace(' ', '_')
    
    def generate_from_json(self, json_data: Dict) -> str:
        """
        Generate Gherkin from JSON input
        
        Args:
            json_data: Dictionary with scenario details
            
        Returns:
            str: Generated Gherkin feature
        """
        scenario = ClinicalScenario(
            scenario=json_data.get('scenario', 'Clinical Scenario'),
            condition=json_data.get('condition', ''),
            action=json_data.get('action', ''),
            context=json_data.get('context', ''),
            contraindications=json_data.get('contraindications'),
            expected_outcome=json_data.get('expected_outcome')
        )
        
        return self.generate_feature(scenario)
    
    def generate_from_file(self, input_path: Path, output_path: Optional[Path] = None) -> str:
        """
        Generate Gherkin from JSON file
        
        Args:
            input_path: Path to input JSON file
            output_path: Optional path to save output. If None, returns string only
            
        Returns:
            str: Generated Gherkin feature
        """
        with open(input_path, 'r') as f:
            data = json.load(f)
        
        # Handle single scenario or array of scenarios
        if isinstance(data, list):
            # Multiple scenarios - generate feature for first one
            # In production, this would iterate and create multiple features
            scenario_data = data[0]
        else:
            scenario_data = data
        
        gherkin = self.generate_from_json(scenario_data)
        
        if output_path:
            with open(output_path, 'w') as f:
                f.write(gherkin)
            print(f"✓ Generated Gherkin feature saved to: {output_path}")
        
        return gherkin


def main():
    """Command-line interface for BDD Generator POC"""
    if len(sys.argv) < 2:
        print("Usage: python poc_bdd_generator.py <input.json> [output.feature]")
        print("\nExample:")
        print("  python poc_bdd_generator.py sample_scenarios.json hypertension.feature")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    
    if not input_file.exists():
        print(f"Error: Input file not found: {input_file}")
        sys.exit(1)
    
    generator = BDDGenerator()
    
    try:
        gherkin = generator.generate_from_file(input_file, output_file)
        
        if not output_file:
            print("\n" + "=" * 80)
            print("GENERATED GHERKIN:")
            print("=" * 80)
            print(gherkin)
            print("=" * 80)
        
        print(f"\n✓ Successfully generated {generator.scenarios_generated} scenarios")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
