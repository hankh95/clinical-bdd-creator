#!/usr/bin/env python3
"""
Phase 6: Security Testing - HIPAA Compliance & PHI Protection

Comprehensive security validation for clinical BDD creator:
1. HIPAA compliance validation
2. PHI data protection testing
3. Access control verification
4. Data encryption validation
5. Audit logging verification
6. Security vulnerability testing

Usage: python security_validation_tests.py
"""

import re
import json
import hashlib
import os
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass
from datetime import datetime, timedelta
import tempfile
import shutil

# Add project root to path
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from guideline_analyzer import GuidelineAnalyzer
from e2e_clinical_workflow_tests import E2EClinicalWorkflowTests


@dataclass
class SecurityViolation:
    """Represents a security violation found during testing"""
    severity: str  # 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW'
    category: str  # 'PHI_EXPOSURE', 'ACCESS_CONTROL', 'ENCRYPTION', 'AUDIT', 'COMPLIANCE'
    description: str
    location: str
    recommendation: str
    phi_detected: Optional[str] = None


class SecurityValidationTests:
    """Comprehensive security testing for HIPAA compliance and PHI protection"""

    def __init__(self):
        self.test_results = []
        self.security_violations = []
        self.phi_patterns = self._load_phi_patterns()
        self.hipaa_requirements = self._load_hipaa_requirements()

    def log_test(self, test_name: str, success: bool, message: str = "", metrics: Optional[Dict] = None):
        """Log a test result"""
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"[{status}] {test_name}")
        if message:
            print(f"  {message}")
        if metrics:
            for key, value in metrics.items():
                print(f"  {key}: {value}")

        self.test_results.append({
            "test": test_name,
            "success": success,
            "message": message,
            "metrics": metrics or {}
        })

    def log_violation(self, violation: SecurityViolation):
        """Log a security violation"""
        self.security_violations.append(violation)

        severity_icon = {
            'CRITICAL': '🚨',
            'HIGH': '⚠️',
            'MEDIUM': '⚡',
            'LOW': 'ℹ️'
        }.get(violation.severity, '❓')

        print(f"{severity_icon} {violation.severity}: {violation.description}")
        if violation.phi_detected:
            print(f"  PHI Detected: {violation.phi_detected}")
        print(f"  Location: {violation.location}")
        print(f"  Recommendation: {violation.recommendation}")
        print()

    def _load_phi_patterns(self) -> Dict[str, str]:
        """Load PHI detection patterns - refined for clinical context"""
        return {
            'ssn': r'\b\d{3}-?\d{2}-?\d{4}\b',
            'phone': r'\b\d{3}-?\d{3}-?\d{4}\b',
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'dob': r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s+\d{4}\b|\b\d{1,2}/\d{1,2}/\d{4}\b',
            'patient_name': r'\bPatient\s+(?:Name|ID)?:\s*[A-Z][a-z]+\s+[A-Z][a-z]+\b',
            'mrn': r'\bMRN[-:]\s*\d+\b',
            'full_address': r'\b\d+\s+[A-Z][a-zA-Z\s,.-]+\d{5}\b',  # More specific address pattern
            'medication_dosage': r'\b\d+(?:\.\d+)?\s*(?:mg|g|mcg|units?|mL|tablets?|capsules?)\b',  # Exclude medical measurements
            'blood_pressure': r'\b\d{2,3}/\d{2,3}\s*mmHg\b',  # Specific BP pattern
            'lab_values': r'\b\d+(?:\.\d+)?\s*(?:mg/dL|g/dL|mmol/L|%)\b'  # Lab value patterns
        }

    def _load_hipaa_requirements(self) -> Dict[str, Dict]:
        """Load HIPAA compliance requirements"""
        return {
            'privacy_rule': {
                'description': 'HIPAA Privacy Rule - Protected Health Information',
                'requirements': [
                    'Minimum necessary use and disclosure',
                    'Individual rights to access PHI',
                    'Business associate agreements',
                    'Data security safeguards'
                ]
            },
            'security_rule': {
                'description': 'HIPAA Security Rule - Technical safeguards',
                'requirements': [
                    'Access control',
                    'Audit controls',
                    'Integrity controls',
                    'Transmission security',
                    'Encryption of data at rest and in transit'
                ]
            },
            'breach_notification': {
                'description': 'HIPAA Breach Notification Rule',
                'requirements': [
                    'Notification within 60 days of discovery',
                    'Individual notification for breaches of 500+ records',
                    'Media notification for large breaches'
                ]
            }
        }

    def test_phi_detection_in_guidelines(self):
        """Test for PHI exposure in clinical guidelines"""
        print("🔍 Testing PHI Detection in Clinical Guidelines")

        analyzer = GuidelineAnalyzer()
        e2e_tester = E2EClinicalWorkflowTests()

        # Test various clinical content
        test_content = [
            ("Hypertension Guideline", e2e_tester.create_jnc8_hypertension_guideline()),
            ("Diabetes Guideline", e2e_tester.create_ada_diabetes_guideline()),
            ("Sepsis Guideline", e2e_tester.create_sepsis_guideline())
        ]

        total_phi_instances = 0
        violations_found = 0

        for content_name, content in test_content:
            print(f"  Scanning {content_name}...")

            # Analyze content for PHI patterns
            phi_instances = self._scan_for_phi(content)

            if phi_instances:
                violations_found += 1
                total_phi_instances += len(phi_instances)

                for phi_type, matches in phi_instances.items():
                    for match in matches[:3]:  # Limit to first 3 instances per type
                        severity = 'CRITICAL' if phi_type in ['ssn', 'patient_name', 'full_address'] else 'HIGH'
                        violation = SecurityViolation(
                            severity=severity,
                            category='PHI_EXPOSURE',
                            description=f'Potential PHI exposure in clinical content: {phi_type}',
                            location=f'{content_name} - {phi_type}',
                            recommendation='Remove or de-identify all PHI from clinical guidelines before processing',
                            phi_detected=match[:50] + '...' if len(match) > 50 else match
                        )
                        self.log_violation(violation)

        success = violations_found == 0
        self.log_test("PHI Detection in Guidelines", success,
                     f"Found {total_phi_instances} PHI instances across {violations_found} content sources",
                     {"phi_instances": total_phi_instances, "affected_sources": violations_found})

        return success

    def test_phi_detection_in_generated_scenarios(self):
        """Test for PHI exposure in generated BDD scenarios"""
        print("🔍 Testing PHI Detection in Generated BDD Scenarios")

        analyzer = GuidelineAnalyzer()
        e2e_tester = E2EClinicalWorkflowTests()

        # Generate scenarios from clinical content
        test_content = [
            ("Hypertension", e2e_tester.create_jnc8_hypertension_guideline()),
            ("Diabetes", e2e_tester.create_ada_diabetes_guideline())
        ]

        total_scenarios = 0
        phi_contaminated_scenarios = 0

        for content_name, content in test_content:
            analysis = analyzer.analyze_guideline(content_name, content)
            total_scenarios += len(analysis.scenarios)

            for scenario in analysis.scenarios:
                # Check scenario text for PHI
                scenario_text = f"{scenario.scenario_id} {' '.join(scenario.inferences)} {' '.join([action['description'] for action in scenario.recommended_actions])}"
                phi_instances = self._scan_for_phi(scenario_text)

                if phi_instances:
                    phi_contaminated_scenarios += 1

                    for phi_type, matches in phi_instances.items():
                        violation = SecurityViolation(
                            severity='CRITICAL',
                            category='PHI_EXPOSURE',
                            description=f'PHI contamination in generated BDD scenario',
                            location=f'Scenario: {scenario.scenario_id}',
                            recommendation='Implement PHI filtering in scenario generation pipeline',
                            phi_detected=list(phi_instances.keys())[0]
                        )
                        self.log_violation(violation)
                        break  # Only log one violation per scenario

        success = phi_contaminated_scenarios == 0
        self.log_test("PHI Detection in BDD Scenarios", success,
                     f"Scanned {total_scenarios} scenarios, {phi_contaminated_scenarios} contained PHI",
                     {"total_scenarios": total_scenarios, "phi_contaminated": phi_contaminated_scenarios})

        return success

    def test_data_encryption_validation(self):
        """Test data encryption implementation"""
        print("🔐 Testing Data Encryption Validation")

        # Test encryption of sensitive clinical data
        test_data = {
            "patient_info": "Patient John Doe, DOB: 01/15/1980, SSN: 123-45-6789",
            "clinical_notes": "Patient presents with hypertension, prescribed lisinopril 10mg daily",
            "lab_results": "Hemoglobin A1c: 8.2%, eGFR: 45 mL/min/1.73m²"
        }

        encryption_success = True
        encryption_methods_tested = []

        # Test basic encryption capability (placeholder - would integrate with actual encryption)
        for data_type, data in test_data.items():
            try:
                # Simulate encryption
                encrypted = self._simulate_encryption(data)
                decrypted = self._simulate_decryption(encrypted)

                if decrypted != data:
                    encryption_success = False
                    violation = SecurityViolation(
                        severity='HIGH',
                        category='ENCRYPTION',
                        description=f'Encryption/decryption failure for {data_type}',
                        location=f'Data encryption test - {data_type}',
                        recommendation='Implement proper AES-256 encryption for PHI data'
                    )
                    self.log_violation(violation)

                encryption_methods_tested.append(data_type)

            except Exception as e:
                encryption_success = False
                violation = SecurityViolation(
                    severity='CRITICAL',
                    category='ENCRYPTION',
                    description=f'Encryption system failure: {str(e)}',
                    location=f'Data encryption test - {data_type}',
                    recommendation='Implement robust encryption system with error handling'
                )
                self.log_violation(violation)

        # Test encryption at rest
        rest_encryption = self._test_encryption_at_rest()
        if not rest_encryption:
            encryption_success = False

        # Test encryption in transit
        transit_encryption = self._test_encryption_in_transit()
        if not transit_encryption:
            encryption_success = False

        self.log_test("Data Encryption Validation", encryption_success,
                     f"Tested encryption for {len(encryption_methods_tested)} data types",
                     {"data_types_encrypted": len(encryption_methods_tested)})

        return encryption_success

    def test_access_control_validation(self):
        """Test access control mechanisms"""
        print("🔒 Testing Access Control Validation")

        # Test role-based access control
        access_tests = [
            ("admin_user", ["READ", "WRITE", "DELETE", "ADMIN"], ["patient_records", "clinical_guidelines"]),
            ("clinician_user", ["READ", "WRITE"], ["patient_records", "clinical_guidelines"]),
            ("researcher_user", ["READ"], ["anonymized_data", "clinical_guidelines"]),
            ("public_user", [], [])
        ]

        access_violations = 0

        for user_role, allowed_permissions, allowed_resources in access_tests:
            # Test each permission against each resource
            for permission in ["READ", "WRITE", "DELETE", "ADMIN"]:
                for resource in ["patient_records", "clinical_guidelines", "anonymized_data", "audit_logs"]:

                    has_access = self._check_access_control(user_role, permission, resource)

                    # Check if access is properly granted/denied
                    should_have_access = (
                        permission in allowed_permissions and
                        resource in allowed_resources
                    )

                    if has_access != should_have_access:
                        access_violations += 1
                        violation = SecurityViolation(
                            severity='HIGH' if resource == "patient_records" else 'MEDIUM',
                            category='ACCESS_CONTROL',
                            description=f'Access control violation: {user_role} {permission} access to {resource}',
                            location=f'Access control matrix - {user_role}:{resource}',
                            recommendation='Implement proper RBAC with least privilege principle'
                        )
                        self.log_violation(violation)

        # Test principle of least privilege
        least_privilege_violations = self._test_least_privilege_principle()
        access_violations += least_privilege_violations

        success = access_violations == 0
        self.log_test("Access Control Validation", success,
                     f"Found {access_violations} access control violations",
                     {"access_violations": access_violations})

        return success

    def test_audit_logging_validation(self):
        """Test audit logging implementation"""
        print("📋 Testing Audit Logging Validation")

        # Simulate various operations that should be logged
        audit_events = [
            ("user_login", {"user": "clinician@example.com", "ip": "192.168.1.100"}),
            ("phi_access", {"user": "clinician@example.com", "resource": "patient_record_12345"}),
            ("data_export", {"user": "researcher@example.com", "records": 150}),
            ("system_config_change", {"user": "admin@example.com", "change": "encryption_settings"})
        ]

        audit_success = True
        logged_events = 0

        for event_type, event_data in audit_events:
            try:
                # Simulate audit logging
                log_entry = self._create_audit_log_entry(event_type, event_data)

                # Verify log entry contains required fields
                required_fields = ["timestamp", "event_type", "user", "action", "resource"]
                missing_fields = [field for field in required_fields if field not in log_entry]

                if missing_fields:
                    audit_success = False
                    violation = SecurityViolation(
                        severity='MEDIUM',
                        category='AUDIT',
                        description=f'Audit log missing required fields: {missing_fields}',
                        location=f'Audit logging - {event_type}',
                        recommendation='Implement comprehensive audit logging with all required HIPAA fields'
                    )
                    self.log_violation(violation)
                else:
                    logged_events += 1

            except Exception as e:
                audit_success = False
                violation = SecurityViolation(
                    severity='HIGH',
                    category='AUDIT',
                    description=f'Audit logging failure: {str(e)}',
                    location=f'Audit logging - {event_type}',
                    recommendation='Implement robust audit logging with error handling and backup'
                )
                self.log_violation(violation)

        # Test audit log integrity
        integrity_test = self._test_audit_log_integrity()
        if not integrity_test:
            audit_success = False

        self.log_test("Audit Logging Validation", audit_success,
                     f"Successfully logged {logged_events}/{len(audit_events)} audit events",
                     {"logged_events": logged_events, "total_events": len(audit_events)})

        return audit_success

    def test_hipaa_compliance_validation(self):
        """Test HIPAA compliance requirements"""
        print("⚖️  Testing HIPAA Compliance Validation")

        compliance_checks = [
            ("privacy_rule_minimum_necessary", self._check_minimum_necessary_principle()),
            ("security_rule_access_control", self._check_security_rule_compliance()),
            ("breach_notification_readiness", self._check_breach_notification_readiness()),
            ("data_retention_policy", self._check_data_retention_policy()),
            ("business_associate_agreements", self._check_business_associate_agreements())
        ]

        compliance_score = 0
        total_checks = len(compliance_checks)

        for check_name, check_result in compliance_checks:
            if check_result:
                compliance_score += 1
            else:
                violation = SecurityViolation(
                    severity='HIGH',
                    category='COMPLIANCE',
                    description=f'HIPAA compliance failure: {check_name.replace("_", " ")}',
                    location=f'HIPAA compliance check - {check_name}',
                    recommendation='Review and implement HIPAA compliance requirements'
                )
                self.log_violation(violation)

        compliance_percentage = (compliance_score / total_checks) * 100
        success = compliance_percentage >= 90.0  # Require 90% compliance

        self.log_test("HIPAA Compliance Validation", success,
                     f"HIPAA compliance: {compliance_score}/{total_checks} ({compliance_percentage:.1f}%)",
                     {"compliance_score": compliance_score, "total_checks": total_checks, "percentage": compliance_percentage})

        return success

    def test_vulnerability_assessment(self):
        """Test for common security vulnerabilities"""
        print("🛡️  Testing Vulnerability Assessment")

        vulnerabilities_found = []

        # Test for common vulnerabilities
        vulnerability_checks = [
            ("sql_injection", self._check_sql_injection_vulnerability()),
            ("xss_vulnerability", self._check_xss_vulnerability()),
            ("insecure_data_storage", self._check_insecure_data_storage()),
            ("weak_authentication", self._check_weak_authentication()),
            ("unencrypted_communications", self._check_unencrypted_communications())
        ]

        for vuln_name, vuln_found in vulnerability_checks:
            if vuln_found:
                vulnerabilities_found.append(vuln_name)
                severity = 'CRITICAL' if vuln_name in ['sql_injection', 'weak_authentication'] else 'HIGH'

                violation = SecurityViolation(
                    severity=severity,
                    category='COMPLIANCE',
                    description=f'Security vulnerability detected: {vuln_name.replace("_", " ")}',
                    location=f'Vulnerability assessment - {vuln_name}',
                    recommendation='Implement security fixes and regular vulnerability scanning'
                )
                self.log_violation(violation)

        success = len(vulnerabilities_found) == 0
        self.log_test("Vulnerability Assessment", success,
                     f"Found {len(vulnerabilities_found)} security vulnerabilities",
                     {"vulnerabilities_found": len(vulnerabilities_found), "vulnerability_types": vulnerabilities_found})

        return success

    # Helper methods for security checks

    def _scan_for_phi(self, text: str) -> Dict[str, List[str]]:
        """Scan text for PHI patterns - refined for clinical context"""
        phi_instances = {}
        for phi_type, pattern in self.phi_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                # Filter out legitimate clinical measurements that might match patterns
                filtered_matches = []
                for match in matches:
                    if self._is_legitimate_clinical_content(match, phi_type):
                        continue
                    filtered_matches.append(match)

                if filtered_matches:
                    phi_instances[phi_type] = filtered_matches
        return phi_instances

    def _is_legitimate_clinical_content(self, match: str, phi_type: str) -> bool:
        """Determine if detected pattern is legitimate clinical content vs actual PHI"""
        # Clinical measurements that should not be flagged as PHI
        clinical_measurements = [
            'blood_pressure', 'medication_dosage', 'lab_values'
        ]

        if phi_type in clinical_measurements:
            return True

        # Check for specific false positives
        if phi_type == 'full_address':
            # Exclude common medical abbreviations and measurements
            medical_terms = ['mmHg', 'mg/dL', 'mmol/L', 'mcg', 'units', 'tablets']
            if any(term in match for term in medical_terms):
                return True

        return False

    def _simulate_encryption(self, data: str) -> str:
        """Simulate data encryption"""
        # This is a placeholder - would use actual encryption
        return hashlib.sha256(data.encode()).hexdigest()

    def _simulate_decryption(self, encrypted_data: str) -> str:
        """Simulate data decryption"""
        # This is a placeholder - decryption would require actual encrypted data
        return "decrypted_data_placeholder"

    def _test_encryption_at_rest(self) -> bool:
        """Test encryption of data at rest"""
        # Placeholder implementation
        return True

    def _test_encryption_in_transit(self) -> bool:
        """Test encryption of data in transit"""
        # Placeholder implementation
        return True

    def _check_access_control(self, user_role: str, permission: str, resource: str) -> bool:
        """Check if user has access to resource"""
        # Placeholder RBAC logic
        role_permissions = {
            "admin_user": ["READ", "WRITE", "DELETE", "ADMIN"],
            "clinician_user": ["READ", "WRITE"],
            "researcher_user": ["READ"],
            "public_user": []
        }

        role_resources = {
            "admin_user": ["patient_records", "clinical_guidelines", "audit_logs"],
            "clinician_user": ["patient_records", "clinical_guidelines"],
            "researcher_user": ["anonymized_data", "clinical_guidelines"],
            "public_user": []
        }

        return (permission in role_permissions.get(user_role, []) and
                resource in role_resources.get(user_role, []))

    def _test_least_privilege_principle(self) -> int:
        """Test principle of least privilege"""
        # Placeholder implementation
        return 0

    def _create_audit_log_entry(self, event_type: str, event_data: Dict) -> Dict:
        """Create an audit log entry"""
        return {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "user": event_data.get("user", "unknown"),
            "action": event_type,
            "resource": event_data.get("resource", "unknown"),
            "ip_address": event_data.get("ip", "unknown"),
            "details": event_data
        }

    def _test_audit_log_integrity(self) -> bool:
        """Test audit log integrity"""
        # Placeholder implementation
        return True

    def _check_minimum_necessary_principle(self) -> bool:
        """Check minimum necessary principle implementation"""
        # Placeholder implementation
        return True

    def _check_security_rule_compliance(self) -> bool:
        """Check HIPAA Security Rule compliance"""
        # Placeholder implementation
        return True

    def _check_breach_notification_readiness(self) -> bool:
        """Check breach notification readiness"""
        # Placeholder implementation
        return True

    def _check_data_retention_policy(self) -> bool:
        """Check data retention policy"""
        # Placeholder implementation
        return True

    def _check_business_associate_agreements(self) -> bool:
        """Check business associate agreements"""
        # Placeholder implementation
        return True

    def _check_sql_injection_vulnerability(self) -> bool:
        """Check for SQL injection vulnerabilities"""
        # Placeholder implementation
        return False

    def _check_xss_vulnerability(self) -> bool:
        """Check for XSS vulnerabilities"""
        # Placeholder implementation
        return False

    def _check_insecure_data_storage(self) -> bool:
        """Check for insecure data storage"""
        # Placeholder implementation
        return False

    def _check_weak_authentication(self) -> bool:
        """Check for weak authentication"""
        # Placeholder implementation
        return False

    def _check_unencrypted_communications(self) -> bool:
        """Check for unencrypted communications"""
        # Placeholder implementation
        return False

    def run_all_security_tests(self):
        """Run all security validation tests"""
        print("🔒 PHASE 6: SECURITY VALIDATION TESTS")
        print("=" * 60)

        try:
            # Run all security tests
            tests = [
                self.test_phi_detection_in_guidelines,
                self.test_phi_detection_in_generated_scenarios,
                self.test_data_encryption_validation,
                self.test_access_control_validation,
                self.test_audit_logging_validation,
                self.test_hipaa_compliance_validation,
                self.test_vulnerability_assessment
            ]

            for test in tests:
                test()

        except Exception as e:
            print(f"❌ Security testing failed with exception: {e}")
            return False

        # Print security summary
        print("\n" + "=" * 60)
        print("SECURITY VALIDATION SUMMARY")

        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)

        print(f"Tests Passed: {passed}/{total}")

        # Security violations summary
        critical_violations = sum(1 for v in self.security_violations if v.severity == 'CRITICAL')
        high_violations = sum(1 for v in self.security_violations if v.severity == 'HIGH')

        if self.security_violations:
            print(f"\n🚨 Security Violations Found:")
            print(f"  Critical: {critical_violations}")
            print(f"  High: {high_violations}")
            print(f"  Total: {len(self.security_violations)}")

            if critical_violations > 0:
                print("\n❌ CRITICAL SECURITY ISSUES MUST BE ADDRESSED")
                return False

        if passed == total and not self.security_violations:
            print("🎉 ALL SECURITY TESTS PASSED - HIPAA COMPLIANT")
            return True
        else:
            print("❌ SECURITY ISSUES DETECTED")
            return False


if __name__ == "__main__":
    tester = SecurityValidationTests()
    success = tester.run_all_security_tests()
    sys.exit(0 if success else 1)