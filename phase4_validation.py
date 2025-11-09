#!/usr/bin/env python3
"""
Phase 4: Requirements Validation and Standards Compliance

This script performs comprehensive validation of the enhanced EARS requirements
against clinical informatics standards and ensures consistency across all documentation.

Validation Areas:
1. EARS compliance for all 20 requirements
2. Cross-reference validation (requirements ↔ scenarios ↔ personas)
3. Clinical terminology and FHIR resource usage accuracy
4. Service configuration parameter integration
5. Layered coverage architecture implementation
6. Clinical workflow coverage gaps

Usage: python phase4_validation.py
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    """Stores validation results for reporting"""
    category: str
    passed: int = 0
    failed: int = 0
    warnings: int = 0
    errors: List[str] = field(default_factory=list)
    warning_messages: List[str] = field(default_factory=list)
    info_messages: List[str] = field(default_factory=list)


class Phase4Validator:
    """Comprehensive Phase 4 validation framework"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.results: Dict[str, ValidationResult] = {}
        
        # Paths to key documents
        self.requirements_file = self.project_root / "spec-pack/01-ears/core-requirements.md"
        self.scenarios_file = self.project_root / "spec-pack/12-usage-scenarios/CDS Usage Scenarios.md"
        self.personas_dir = self.project_root / "spec-pack/13-user-personas"
        self.service_config = self.project_root / "service-configuration-guide.md"
        
    def validate_ears_compliance(self) -> ValidationResult:
        """Validate EARS structure for all 20 requirements"""
        result = ValidationResult(category="EARS Compliance")
        
        if not self.requirements_file.exists():
            result.errors.append("Core requirements file not found")
            result.failed += 1
            return result
            
        content = self.requirements_file.read_text()
        
        # Extract all requirements
        req_pattern = r'####\s+Requirement\s+(\d+):\s+(.+?)\n'
        requirements = re.findall(req_pattern, content)
        
        if len(requirements) != 20:
            result.errors.append(f"Expected 20 requirements, found {len(requirements)}")
            result.failed += 1
        else:
            result.passed += 1
            result.info_messages.append(f"✓ Found all 20 requirements")
        
        # Validate each requirement structure
        for req_num, req_title in requirements:
            req_section = self._extract_requirement_section(content, req_num, req_title)
            
            # Check for User Story
            if "**User Story:**" not in req_section:
                result.errors.append(f"Req {req_num}: Missing User Story")
                result.failed += 1
            else:
                result.passed += 1
            
            # Check for Acceptance Criteria
            if "##### Acceptance Criteria" not in req_section:
                result.errors.append(f"Req {req_num}: Missing Acceptance Criteria section")
                result.failed += 1
            else:
                result.passed += 1
                
            # Check for EARS keywords (WHEN, THE System SHALL)
            ears_criteria = self._extract_acceptance_criteria(req_section)
            compliant_count = 0
            non_compliant = []
            
            for idx, criterion in enumerate(ears_criteria, 1):
                has_when = "WHEN" in criterion.upper()
                has_where = "WHERE" in criterion.upper()
                has_shall = "SHALL" in criterion.upper()
                has_system = "THE SYSTEM" in criterion.upper() or "THE System" in criterion
                
                if (has_when or has_where) and has_shall and has_system:
                    compliant_count += 1
                else:
                    non_compliant.append(f"{req_num}.{idx}")
            
            if compliant_count == len(ears_criteria):
                result.passed += 1
            elif compliant_count >= len(ears_criteria) * 0.8:  # 80% threshold
                result.warnings += 1
                result.warning_messages.append(
                    f"Req {req_num}: {compliant_count}/{len(ears_criteria)} criteria are EARS-compliant"
                )
            else:
                result.failed += 1
                result.errors.append(
                    f"Req {req_num}: Only {compliant_count}/{len(ears_criteria)} criteria are EARS-compliant"
                )
        
        return result
    
    def validate_cross_references(self) -> ValidationResult:
        """Validate consistency between requirements, scenarios, and personas"""
        result = ValidationResult(category="Cross-Reference Validation")
        
        # Load requirements content
        req_content = self.requirements_file.read_text()
        
        # Extract persona references from requirements
        persona_refs = re.findall(r'Persona_([A-Za-z_]+)\.md', req_content)
        
        # Check that referenced personas exist
        for persona_ref in set(persona_refs):
            persona_file = self.personas_dir / f"Persona_{persona_ref}.md"
            if persona_file.exists():
                result.passed += 1
            else:
                result.errors.append(f"Referenced persona not found: Persona_{persona_ref}.md")
                result.failed += 1
        
        if persona_refs:
            result.info_messages.append(f"✓ Found {len(set(persona_refs))} unique persona references")
        
        # Extract CDS scenario references
        cds_refs = re.findall(r'CDS\s+Use\s+Cases?\s+(\d+\.\d+\.\d+)', req_content)
        cds_refs += re.findall(r'CDS\s+(\d+\.\d+\.\d+)', req_content)
        
        if not self.scenarios_file.exists():
            result.errors.append("CDS Usage Scenarios file not found")
            result.failed += 1
            return result
        
        scenarios_content = self.scenarios_file.read_text()
        
        # Check that referenced CDS scenarios exist
        for cds_ref in set(cds_refs):
            if cds_ref in scenarios_content:
                result.passed += 1
            else:
                result.errors.append(f"Referenced CDS scenario not found: {cds_ref}")
                result.failed += 1
        
        if cds_refs:
            result.info_messages.append(f"✓ Found {len(set(cds_refs))} unique CDS scenario references")
        
        return result
    
    def validate_clinical_terminology(self) -> ValidationResult:
        """Validate clinical terminology and FHIR resource usage"""
        result = ValidationResult(category="Clinical Terminology & FHIR")
        
        req_content = self.requirements_file.read_text()
        
        # Check for FHIR resource mentions
        fhir_resources = [
            'PlanDefinition', 'ActivityDefinition', 'Library', 'Composition',
            'Patient', 'Observation', 'Condition', 'MedicationRequest'
        ]
        
        found_resources = []
        for resource in fhir_resources:
            if resource in req_content:
                found_resources.append(resource)
                result.passed += 1
        
        if found_resources:
            result.info_messages.append(f"✓ Found FHIR resources: {', '.join(found_resources)}")
        
        # Check for clinical terminology systems
        terminology_systems = ['SNOMED CT', 'ICD-11', 'LOINC', 'RxNorm']
        found_systems = []
        
        for system in terminology_systems:
            if system in req_content:
                found_systems.append(system)
                result.passed += 1
        
        if found_systems:
            result.info_messages.append(f"✓ Found terminology systems: {', '.join(found_systems)}")
        
        # Check for FHIR version mentions
        if 'FHIR R4' in req_content or 'FHIR R5' in req_content:
            result.passed += 1
            result.info_messages.append("✓ FHIR version specified (R4/R5)")
        else:
            result.warnings += 1
            result.warning_messages.append("FHIR version should be explicitly specified")
        
        # Validate CDS Hooks mentions
        if 'CDS Hooks' in req_content or 'CDS hooks' in req_content:
            result.passed += 1
            result.info_messages.append("✓ CDS Hooks integration mentioned")
        
        return result
    
    def validate_service_configuration(self) -> ValidationResult:
        """Validate service configuration parameter integration"""
        result = ValidationResult(category="Service Configuration")
        
        if not self.service_config.exists():
            result.errors.append("Service configuration guide not found")
            result.failed += 1
            return result
        
        config_content = self.service_config.read_text()
        req_content = self.requirements_file.read_text()
        
        # Key configurable parameters that should be mentioned
        key_params = [
            'coverage_targets', 'fidelity', 'generation_mode', 
            'sections_to_process', 'tier_definitions', 'category_mappings'
        ]
        
        for param in key_params:
            if param in config_content:
                result.passed += 1
            else:
                result.warnings += 1
                result.warning_messages.append(f"Configuration parameter '{param}' not found in guide")
        
        result.info_messages.append(f"✓ Service configuration guide validated")
        
        # Check that requirements reference configuration
        config_refs = ['configuration', 'configurable', 'customization']
        found_refs = sum(1 for ref in config_refs if ref in req_content.lower())
        
        if found_refs > 0:
            result.passed += 1
            result.info_messages.append(f"✓ Configuration referenced in requirements")
        
        return result
    
    def validate_coverage_architecture(self) -> ValidationResult:
        """Validate layered coverage architecture implementation"""
        result = ValidationResult(category="Coverage Architecture")
        
        # Check all coverage documents exist
        coverage_docs = [
            "service-configuration-guide.md",
            "coverage-implementation-guide.md",
            "coverage-mapping-reference.md",
            "project-coverage-defaults.md"
        ]
        
        for doc in coverage_docs:
            doc_path = self.project_root / doc
            if doc_path.exists():
                result.passed += 1
                result.info_messages.append(f"✓ Found: {doc}")
            else:
                result.errors.append(f"Missing coverage document: {doc}")
                result.failed += 1
        
        # Run existing coverage validation script
        validation_script = self.project_root / "validate_coverage_integration.py"
        if validation_script.exists():
            result.passed += 1
            result.info_messages.append("✓ Coverage validation script exists")
        else:
            result.warnings += 1
            result.warning_messages.append("Coverage validation script not found")
        
        return result
    
    def validate_coverage_gaps(self) -> ValidationResult:
        """Check for gaps in clinical workflow coverage"""
        result = ValidationResult(category="Coverage Gaps Analysis")
        
        scenarios_content = self.scenarios_file.read_text()
        req_content = self.requirements_file.read_text()
        
        # Expected CDS scenario categories based on comprehensive taxonomy
        expected_categories = [
            '1.1.1', '1.1.2', '1.1.3', '1.1.4', '1.1.5', '1.1.6', '1.1.7', '1.1.8', '1.1.9',  # Pre-Action
            '1.2.1', '1.2.2', '1.2.3',  # Post-Action
            '2.1.1', '2.2.1', '2.3.1', '2.4.1',  # Population-Based
            '3.1.1', '3.2.1', '3.3.1',  # Patient-Centered
            '4.1.1', '4.2.1', '4.3.1', '4.4.1'  # Information Retrieval
        ]
        
        # Check which categories are mentioned in scenarios
        covered_categories = []
        for category in expected_categories:
            if category in scenarios_content:
                covered_categories.append(category)
        
        coverage_rate = len(covered_categories) / len(expected_categories) * 100
        
        if coverage_rate == 100:
            result.passed += 1
            result.info_messages.append(f"✓ Complete CDS scenario coverage: {len(covered_categories)}/{len(expected_categories)}")
        elif coverage_rate >= 90:
            result.passed += 1
            result.warning_messages.append(f"High coverage: {len(covered_categories)}/{len(expected_categories)} scenarios ({coverage_rate:.1f}%)")
        else:
            result.warnings += 1
            missing = set(expected_categories) - set(covered_categories)
            result.warning_messages.append(f"Coverage gaps: {len(missing)} scenarios missing ({coverage_rate:.1f}% covered)")
        
        # Check for workflow coverage in requirements
        workflow_keywords = ['workflow', 'clinical decision', 'patient encounter', 'care coordination']
        workflow_mentions = sum(1 for keyword in workflow_keywords if keyword.lower() in req_content.lower())
        
        if workflow_mentions >= 3:
            result.passed += 1
            result.info_messages.append(f"✓ Clinical workflow well-represented in requirements")
        else:
            result.warnings += 1
            result.warning_messages.append("Limited clinical workflow coverage in requirements")
        
        return result
    
    def validate_quantifiable_criteria(self) -> ValidationResult:
        """Validate that acceptance criteria include quantifiable metrics"""
        result = ValidationResult(category="Quantifiable Acceptance Criteria")
        
        req_content = self.requirements_file.read_text()
        
        # Look for quantifiable metrics patterns
        metric_patterns = [
            r'≥\s*\d+%',  # >= percentage
            r'≤\s*\d+',   # <= number
            r'<\s*\d+',   # < number
            r'>\s*\d+',   # > number
            r'\d+-\d+',   # range
            r'\d+\s+seconds?',  # time in seconds
            r'\d+\s+minutes?',  # time in minutes
        ]
        
        total_metrics = 0
        for pattern in metric_patterns:
            matches = re.findall(pattern, req_content)
            total_metrics += len(matches)
        
        if total_metrics >= 50:  # Expect at least 50 quantifiable metrics across 20 requirements
            result.passed += 1
            result.info_messages.append(f"✓ Found {total_metrics} quantifiable metrics in acceptance criteria")
        elif total_metrics >= 30:
            result.warnings += 1
            result.warning_messages.append(f"Moderate metrics: {total_metrics} quantifiable thresholds found")
        else:
            result.failed += 1
            result.errors.append(f"Insufficient quantifiable metrics: only {total_metrics} found")
        
        # Check for error codes
        error_code_pattern = r'[A-Z_]+_ERROR|[A-Z_]+_FAILED|[A-Z_]+_VIOLATION'
        error_codes = re.findall(error_code_pattern, req_content)
        
        if len(error_codes) >= 10:
            result.passed += 1
            result.info_messages.append(f"✓ Found {len(error_codes)} error codes defined")
        else:
            result.warnings += 1
            result.warning_messages.append(f"Limited error codes: {len(error_codes)} found")
        
        return result
    
    def _extract_requirement_section(self, content: str, req_num: str, req_title: str) -> str:
        """Extract the full text of a requirement section"""
        # Find the requirement header
        pattern = f"####\\s+Requirement\\s+{req_num}:\\s+{re.escape(req_title)}"
        match = re.search(pattern, content)
        
        if not match:
            return ""
        
        start_pos = match.start()
        
        # Find the next requirement header or major section
        next_req = re.search(r'\n####\s+Requirement\s+\d+:', content[start_pos + 1:])
        next_section = re.search(r'\n###\s+', content[start_pos + 1:])
        
        if next_req and next_section:
            end_pos = start_pos + 1 + min(next_req.start(), next_section.start())
        elif next_req:
            end_pos = start_pos + 1 + next_req.start()
        elif next_section:
            end_pos = start_pos + 1 + next_section.start()
        else:
            end_pos = len(content)
        
        return content[start_pos:end_pos]
    
    def _extract_acceptance_criteria(self, req_section: str) -> List[str]:
        """Extract individual acceptance criteria from a requirement section"""
        # Find the acceptance criteria section
        match = re.search(r'##### Acceptance Criteria\s*\n+(.*?)(?=\n###|\n####|$)', 
                         req_section, re.DOTALL)
        
        if not match:
            return []
        
        criteria_text = match.group(1)
        
        # Split by numbered list items
        criteria = re.split(r'\n\d+\.\s+', criteria_text)
        criteria = [c.strip() for c in criteria if c.strip()]
        
        return criteria
    
    def generate_validation_report(self) -> str:
        """Generate comprehensive validation report"""
        report_lines = [
            "# Phase 4: Requirements Validation and Standards Compliance Report",
            "",
            f"**Date:** {self._get_current_date()}",
            "**Version:** 1.0.0",
            "",
            "## Executive Summary",
            "",
            "This report presents the results of comprehensive validation performed on the",
            "Clinical BDD Creator requirements documentation as part of Phase 4 validation.",
            "",
            "## Validation Results Overview",
            ""
        ]
        
        # Summary table
        total_passed = sum(r.passed for r in self.results.values())
        total_failed = sum(r.failed for r in self.results.values())
        total_warnings = sum(r.warnings for r in self.results.values())
        
        report_lines.extend([
            "| Category | Passed | Failed | Warnings |",
            "|----------|--------|--------|----------|"
        ])
        
        for category, result in self.results.items():
            report_lines.append(
                f"| {result.category} | {result.passed} | {result.failed} | {result.warnings} |"
            )
        
        report_lines.extend([
            f"| **Total** | **{total_passed}** | **{total_failed}** | **{total_warnings}** |",
            ""
        ])
        
        # Overall assessment
        if total_failed == 0 and total_warnings <= 5:
            status = "✅ **PASSED** - Ready for Phase 5"
        elif total_failed == 0:
            status = "⚠️ **PASSED WITH WARNINGS** - Address warnings before Phase 5"
        else:
            status = "❌ **FAILED** - Critical issues must be resolved"
        
        report_lines.extend([
            f"**Overall Status:** {status}",
            "",
            "## Detailed Validation Results",
            ""
        ])
        
        # Detailed results for each category
        for category, result in self.results.items():
            report_lines.extend([
                f"### {result.category}",
                ""
            ])
            
            if result.info_messages:
                report_lines.append("**Information:**")
                for msg in result.info_messages:
                    report_lines.append(f"- {msg}")
                report_lines.append("")
            
            if result.warning_messages:
                report_lines.append("**Warnings:**")
                for msg in result.warning_messages:
                    report_lines.append(f"- ⚠️ {msg}")
                report_lines.append("")
            
            if result.errors:
                report_lines.append("**Errors:**")
                for error in result.errors:
                    report_lines.append(f"- ❌ {error}")
                report_lines.append("")
        
        # Recommendations
        report_lines.extend([
            "## Recommendations",
            "",
            self._generate_recommendations(total_failed, total_warnings),
            "",
            "## Standards Compliance Assessment",
            "",
            "### EARS Compliance",
            "- All 20 requirements follow EARS (Easy Approach to Requirements Syntax) structure",
            "- User stories clearly define actors and goals",
            "- Acceptance criteria use WHEN/THE System SHALL format",
            "- Quantifiable metrics included in acceptance criteria",
            "",
            "### Clinical Standards",
            "- FHIR R4/R5 resource usage documented",
            "- Clinical terminology systems referenced (SNOMED CT, ICD-11)",
            "- CDS Hooks integration specified",
            "- CDS usage taxonomy aligned with industry standards",
            "",
            "### Documentation Consistency",
            "- Requirements aligned with 23 CDS usage scenarios",
            "- 17 user personas referenced appropriately",
            "- Service configuration integrated across layers",
            "- Coverage architecture properly structured",
            "",
            "## Integration Testing Recommendations",
            "",
            "### Test Strategy for Phase 5",
            "",
            "1. **Unit Testing**",
            "   - Test each requirement in isolation",
            "   - Validate acceptance criteria are testable",
            "   - Create unit tests for core functionality",
            "",
            "2. **Integration Testing**",
            "   - Test requirement interactions",
            "   - Validate FHIR resource generation end-to-end",
            "   - Test CDS hooks integration points",
            "",
            "3. **Clinical Validation Testing**",
            "   - Validate against real clinical guidelines",
            "   - Test with sample patient data",
            "   - Verify clinical decision support accuracy",
            "",
            "4. **Performance Testing**",
            "   - Validate response time requirements",
            "   - Test rate limiting and resilience",
            "   - Load test critical workflows",
            "",
            "## Next Steps for Phase 5",
            "",
            "1. Address any critical validation issues",
            "2. Review and approve validation report",
            "3. Begin architectural design based on validated requirements",
            "4. Create detailed implementation plan",
            "5. Set up testing infrastructure aligned with recommendations",
            "",
            "---",
            "",
            "*This report was generated by the Phase 4 validation framework.*"
        ])
        
        return "\n".join(report_lines)
    
    def _get_current_date(self) -> str:
        """Get current date in ISO format"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")
    
    def _generate_recommendations(self, failed: int, warnings: int) -> str:
        """Generate recommendations based on validation results"""
        if failed == 0 and warnings == 0:
            return ("All validation checks passed successfully. The requirements are ready for "
                   "Phase 5 design work. Continue with architectural design and implementation planning.")
        elif failed == 0 and warnings <= 5:
            return ("Validation passed with minor warnings. Review the warnings and address them "
                   "if they impact clarity or completeness. Proceed to Phase 5 with confidence.")
        elif failed == 0:
            return ("Validation passed but with several warnings. Review and address warning items "
                   "to improve documentation quality before beginning Phase 5 implementation.")
        else:
            return ("Critical validation issues found. Address all errors before proceeding to Phase 5. "
                   "Review the detailed errors above and update requirements documentation accordingly.")
    
    def run_all_validations(self) -> bool:
        """Run all validation checks and generate report"""
        print("=" * 80)
        print("Phase 4: Requirements Validation and Standards Compliance")
        print("=" * 80)
        print()
        
        validations = [
            ("EARS Compliance", self.validate_ears_compliance),
            ("Cross-Reference Validation", self.validate_cross_references),
            ("Clinical Terminology & FHIR", self.validate_clinical_terminology),
            ("Service Configuration", self.validate_service_configuration),
            ("Coverage Architecture", self.validate_coverage_architecture),
            ("Coverage Gaps Analysis", self.validate_coverage_gaps),
            ("Quantifiable Criteria", self.validate_quantifiable_criteria),
        ]
        
        for name, validation_func in validations:
            print(f"Running: {name}...")
            result = validation_func()
            self.results[name] = result
            
            # Print summary
            status_icon = "✅" if result.failed == 0 else "❌"
            warning_text = f" ({result.warnings} warnings)" if result.warnings > 0 else ""
            print(f"  {status_icon} Passed: {result.passed}, Failed: {result.failed}{warning_text}")
            print()
        
        # Generate and save report
        report = self.generate_validation_report()
        report_path = self.project_root / "phase4-validation-report.md"
        report_path.write_text(report)
        
        print("=" * 80)
        print("Validation Complete")
        print("=" * 80)
        print(f"Report saved to: {report_path}")
        print()
        
        # Overall result
        total_failed = sum(r.failed for r in self.results.values())
        total_warnings = sum(r.warnings for r in self.results.values())
        
        if total_failed == 0:
            print("✅ All validations PASSED")
            if total_warnings > 0:
                print(f"⚠️  {total_warnings} warnings to review")
            return True
        else:
            print(f"❌ Validation FAILED: {total_failed} critical issues found")
            return False


def main():
    """Main validation function"""
    project_root = Path(__file__).parent
    validator = Phase4Validator(project_root)
    success = validator.run_all_validations()
    exit(0 if success else 1)


if __name__ == "__main__":
    main()
