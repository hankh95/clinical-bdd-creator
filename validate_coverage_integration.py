#!/usr/bin/env python3
"""
Coverage Integration Validation Script

This script validates that the layered coverage system is properly integrated:
1. Service configuration guide supports the required parameters
2. Implementation guide uses category-based mappings
3. Mapping reference provides complete CDS scenario coverage
4. Project defaults are consistent with the mapping system

Usage: python validate_coverage_integration.py
"""

import os
import yaml
import re
from pathlib import Path

class CoverageValidator:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.errors = []
        self.warnings = []

    def validate_service_config_guide(self) -> bool:
        """Validate that service configuration guide supports tiered coverage"""
        config_file = self.project_root / "service-configuration-guide.md"

        if not config_file.exists():
            self.errors.append("Service configuration guide not found")
            return False

        content = config_file.read_text()

        # Check for tiered strategy support
        if 'strategy": "tiered"' not in content:
            self.errors.append("Service config guide missing tiered strategy support")

        # Check for tier definitions
        if 'tier_definitions' not in content:
            self.errors.append("Service config guide missing tier definitions")

        # Check for category mappings
        if 'category_mappings' not in content:
            self.errors.append("Service config guide missing category mappings")

        return len(self.errors) == 0

    def validate_implementation_guide(self) -> bool:
        """Validate implementation guide uses category-based approach"""
        impl_file = self.project_root / "coverage-implementation-guide.md"

        if not impl_file.exists():
            self.errors.append("Coverage implementation guide not found")
            return False

        content = impl_file.read_text()

        # Should use category_mappings, not hardcoded scenario IDs
        if 'category_mappings:' in content and 'scenario_defaults:' not in content:
            return True
        else:
            self.errors.append("Implementation guide should use category_mappings instead of scenario_defaults")
            return False

    def validate_mapping_reference(self) -> dict:
        """Validate mapping reference completeness and extract mappings"""
        mapping_file = self.project_root / "coverage-mapping-reference.md"

        if not mapping_file.exists():
            self.errors.append("Coverage mapping reference not found")
            return {}

        content = mapping_file.read_text()
        mappings = {}

        # Extract CDS scenario mappings from markdown table
        table_pattern = r'\| (\d+\.\d+\.\d+) \| ([^|]+) \| ([^|]+) \|'
        matches = re.findall(table_pattern, content)

        for match in matches:
            scenario_id, usage_scenario, category = match
            mappings[scenario_id.strip()] = category.strip()

        # Validate we have mappings for all expected scenarios
        expected_scenarios = [
            '1.1.1', '1.1.2', '1.1.3', '1.1.4', '1.1.5', '1.1.6', '1.1.7',  # Assessment & Diagnosis
            '1.2.1', '1.2.2',                                                   # Medication Management
            '1.3.1',                                                           # Patient Safety
            '2.1.1', '2.2.1', '2.3.1', '2.4.1',                             # Care Management, Quality, Risk, Public Health
            '3.1.1', '3.2.1', '3.3.1',                                       # Patient Engagement, SDOH, Education
            '4.1.1', '4.2.1', '4.3.1', '4.4.1'                             # Information, Pathways, Documentation, Coordination
        ]

        missing_scenarios = set(expected_scenarios) - set(mappings.keys())
        if missing_scenarios:
            self.errors.append(f"Missing mappings for scenarios: {sorted(missing_scenarios)}")

        return mappings

    def validate_project_defaults(self, scenario_mappings: dict) -> bool:
        """Validate project defaults are consistent with mappings"""
        defaults_file = self.project_root / "project-coverage-defaults.md"

        if not defaults_file.exists():
            self.errors.append("Project coverage defaults not found")
            return False

        content = defaults_file.read_text()

        # Extract category mappings from YAML in markdown
        yaml_blocks = re.findall(r'```yaml\s*(.*?)\s*```', content, re.DOTALL)

        category_mappings = {}
        for block in yaml_blocks:
            try:
                parsed = yaml.safe_load(block)
                if 'category_mappings' in parsed.get('coverage_targets', {}):
                    category_mappings.update(parsed['coverage_targets']['category_mappings'])
                    break
            except yaml.YAMLError:
                continue

        if not category_mappings:
            self.errors.append("Could not extract category mappings from project defaults")
            return False

        # Validate that all categories from mappings are covered in defaults
        mapped_categories = set(scenario_mappings.values())
        default_categories = set(category_mappings.keys())

        missing_categories = mapped_categories - default_categories
        if missing_categories:
            self.errors.append(f"Project defaults missing categories: {sorted(missing_categories)}")

        extra_categories = default_categories - mapped_categories
        if extra_categories:
            self.warnings.append(f"Project defaults have extra categories: {sorted(extra_categories)}")

        return len(self.errors) == 0

    def validate_tier_consistency(self) -> bool:
        """Validate tier definitions are consistent across documents"""
        files_to_check = [
            "service-configuration-guide.md",
            "coverage-implementation-guide.md",
            "project-coverage-defaults.md"
        ]

        tier_definitions = {}

        for filename in files_to_check:
            filepath = self.project_root / filename
            if not filepath.exists():
                continue

            content = filepath.read_text()

            # Look for tier definitions in YAML blocks
            yaml_blocks = re.findall(r'```yaml\s*(.*?)\s*```', content, re.DOTALL)

            for block in yaml_blocks:
                try:
                    parsed = yaml.safe_load(block)
                    if parsed and 'coverage_targets' in parsed:
                        coverage_targets = parsed['coverage_targets']
                        if 'tier_definitions' in coverage_targets:
                            tiers = coverage_targets['tier_definitions']
                            for tier_name, tier_config in tiers.items():
                                if tier_name in tier_definitions:
                                    # Check consistency
                                    existing = tier_definitions[tier_name]
                                    if existing != tier_config:
                                        self.warnings.append(f"Tier '{tier_name}' definition differs between files")
                                else:
                                    tier_definitions[tier_name] = tier_config
                except yaml.YAMLError:
                    continue

        return True

    def run_validation(self) -> bool:
        """Run all validation checks"""
        print("🔍 Validating Coverage Integration...")
        print("=" * 50)

        # 1. Validate service configuration guide
        print("1. Checking Service Configuration Guide...")
        if self.validate_service_config_guide():
            print("   ✅ Service configuration guide is valid")
        else:
            print("   ❌ Service configuration guide has issues")

        # 2. Validate implementation guide
        print("2. Checking Implementation Guide...")
        if self.validate_implementation_guide():
            print("   ✅ Implementation guide uses category-based approach")
        else:
            print("   ❌ Implementation guide has issues")

        # 3. Validate mapping reference
        print("3. Checking Mapping Reference...")
        scenario_mappings = self.validate_mapping_reference()
        if scenario_mappings:
            print(f"   ✅ Found mappings for {len(scenario_mappings)} CDS scenarios")
        else:
            print("   ❌ Mapping reference has issues")

        # 4. Validate project defaults
        print("4. Checking Project Defaults...")
        if self.validate_project_defaults(scenario_mappings):
            print("   ✅ Project defaults are consistent with mappings")
        else:
            print("   ❌ Project defaults have issues")

        # 5. Validate tier consistency
        print("5. Checking Tier Consistency...")
        self.validate_tier_consistency()
        if self.warnings:
            print(f"   ⚠️  Found {len(self.warnings)} warnings")

        # Summary
        print("\n" + "=" * 50)
        if self.errors:
            print(f"❌ VALIDATION FAILED: {len(self.errors)} errors found")
            for error in self.errors:
                print(f"   - {error}")
            return False
        else:
            print("✅ VALIDATION PASSED")
            if self.warnings:
                print(f"⚠️  {len(self.warnings)} warnings:")
                for warning in self.warnings:
                    print(f"   - {warning}")
            return True

def main():
    """Main validation function"""
    project_root = Path(__file__).parent
    validator = CoverageValidator(project_root)
    success = validator.run_validation()
    exit(0 if success else 1)

if __name__ == "__main__":
    main()
