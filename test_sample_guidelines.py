#!/usr/bin/env python3
"""
Test Script: Process Sample Clinical Guidelines with POCs

This script demonstrates processing sample clinical guidelines from the examples/
directory using our working POCs:

1. CIKG Processor: Extract clinical knowledge from guideline text
2. MCP Server: Process clinical scenarios with coverage configuration
3. BDD Generator: Generate Gherkin test scenarios

Usage:
    python test_sample_guidelines.py [--guideline <guideline_name>]

Available guidelines:
    - diabetes-management
    - acc-afib
    - nccn-breast-cancer
"""

import json
import yaml
import sys
import os
import copy
from pathlib import Path
from typing import Dict, Any, List, Optional
import subprocess
import time
from datetime import datetime

# Import our new analysis components
from guideline_analyzer import GuidelineAnalyzer
# from external_validator import ExternalValidator  # TODO: Install dependencies

class GuidelineTester:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.python_cmd = sys.executable
        self.generated_dir = self.project_root / "generated"
        self.ensure_generated_dirs()

    def ensure_generated_dirs(self):
        """Ensure all generated output directories exist"""
        # Create main structure
        dirs = [
            self.generated_dir / "guideline-topics",
            self.generated_dir / "summary-reports"
        ]
        
        # Create topic directories
        topic_dirs = [
            "diabetes-management",
            "cardiology", 
            "oncology"
        ]
        
        for topic in topic_dirs:
            dirs.append(self.generated_dir / "guideline-topics" / topic)
        
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)

    def get_topic_from_scenario(self, scenario_name: str) -> str:
        """Determine the guideline topic from scenario name"""
        if "diabetes" in scenario_name.lower():
            return "diabetes-management"
        elif "afib" in scenario_name.lower() or "heart" in scenario_name.lower() or "cardiology" in scenario_name.lower():
            return "cardiology"
        elif "cancer" in scenario_name.lower() or "oncology" in scenario_name.lower():
            return "oncology"
        else:
            return "general-clinical"

    def get_topic_from_pdf_path(self, pdf_path: str) -> str:
        """Determine the guideline topic from PDF path"""
        pdf_path_lower = pdf_path.lower()
        if "diabetes" in pdf_path_lower:
            return "diabetes-management"
        elif "afib" in pdf_path_lower or "heart" in pdf_path_lower or "cardiology" in pdf_path_lower:
            return "cardiology"
        elif "cancer" in pdf_path_lower or "oncology" in pdf_path_lower:
            return "oncology"
        else:
            return "general-clinical"

    def get_next_version(self, topic_dir: Path) -> str:
        """Get the next version number for a topic"""
        if not topic_dir.exists():
            return "v1"
        
        # Find existing version directories
        version_dirs = [d for d in topic_dir.iterdir() if d.is_dir() and d.name.startswith(datetime.now().strftime("%Y-%m-%d"))]
        if not version_dirs:
            return "v1"
        
        # Extract version numbers
        versions = []
        for d in version_dirs:
            parts = d.name.split("_v")
            if len(parts) == 2:
                try:
                    versions.append(int(parts[1]))
                except ValueError:
                    continue
        
        return f"v{max(versions) + 1}" if versions else "v1"

    def create_versioned_run_dir(self, topic: str, scenario_name: str) -> Path:
        """Create a versioned run directory for this test run"""
        topic_dir = self.generated_dir / "guideline-topics" / topic
        date_str = datetime.now().strftime("%Y-%m-%d")
        version = self.get_next_version(topic_dir)
        run_dir_name = f"{date_str}_{version}"
        run_dir = topic_dir / run_dir_name
        
        # Create subdirectories
        subdirs = ["bdd-tests", "cikg-triples", "mcp-logs", "integration-results"]
        for subdir in subdirs:
            (run_dir / subdir).mkdir(parents=True, exist_ok=True)
        
        # Update latest symlink
        latest_link = topic_dir / "latest"
        if latest_link.exists():
            latest_link.unlink()
        try:
            latest_link.symlink_to(run_dir_name, target_is_directory=True)
        except OSError:
            # Symlinks might not work on all systems, create a text file instead
            with open(latest_link, 'w') as f:
                f.write(run_dir_name)
        
        return run_dir

    def load_scenario_from_yaml(self, yaml_path: Path) -> Dict[str, Any]:
        """Load a clinical scenario from YAML format"""
        with open(yaml_path, 'r') as f:
            return yaml.safe_load(f)

    def convert_scenario_for_bdd(self, yaml_scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Convert YAML scenario to BDD generator format"""
        clinical = yaml_scenario.get('clinical', {})
        expectations = yaml_scenario.get('expectations', {})

        # Extract key information for BDD generation
        scenario_title = yaml_scenario['scenario']['title']
        patient_info = clinical.get('patient', {})
        diagnosis = clinical.get('diagnosis', {})
        recommendations = expectations.get('recommendations', [])

        # Build context from patient and clinical info
        context_parts = []
        if patient_info.get('presentation', {}).get('chief_complaint'):
            context_parts.append(f"Patient presents with: {patient_info['presentation']['chief_complaint']}")

        if diagnosis.get('primary'):
            context_parts.append(f"Diagnosis: {diagnosis['primary']}")

        if clinical.get('comorbidities'):
            for comorbidity in clinical['comorbidities']:
                context_parts.append(f"Comorbidity: {comorbidity['name']}")

        # Build condition from diagnosis and labs
        condition_parts = []
        if diagnosis.get('primary'):
            condition_parts.append(diagnosis['primary'])

        if clinical.get('labs', {}).get('hba1c'):
            hba1c = clinical['labs']['hba1c']
            condition_parts.append(f"HbA1c: {hba1c['value']}% (target: {hba1c['target']})")

        # Build action from recommendations
        action_parts = []
        for rec in recommendations[:2]:  # Take first 2 recommendations
            if rec.get('drug_class'):
                action_parts.append(f"Initiate {rec['drug_class']}")
            elif rec.get('type') == 'medication':
                action_parts.append(f"Prescribe {rec.get('drug_class', 'medication')}")

        # Build expected outcome
        outcome_parts = []
        if expectations.get('targets', {}).get('hba1c'):
            outcome_parts.append(f"Achieve HbA1c {expectations['targets']['hba1c']}")

        return {
            "scenario": scenario_title,
            "condition": "; ".join(condition_parts) if condition_parts else "Clinical condition requiring treatment",
            "action": "; ".join(action_parts) if action_parts else "Provide appropriate clinical treatment",
            "context": "; ".join(context_parts) if context_parts else "Standard clinical setting",
            "expected_outcome": "; ".join(outcome_parts) if outcome_parts else "Patient receives optimal care"
        }

    def create_clinical_text_from_scenario(self, yaml_scenario: Dict[str, Any]) -> str:
        """Create clinical guideline text from scenario data for CIKG processing"""
        # Extract clinical and expectations data
        clinical = yaml_scenario.get('clinical', {})
        expectations = yaml_scenario.get('expectations', {})

        # Build clinical guideline text
        text_parts = []

        # Patient context
        patient = clinical.get('patient', {})
        if patient.get('presentation', {}).get('chief_complaint'):
            text_parts.append(f"For patients presenting with {patient['presentation']['chief_complaint'].lower()}")

        # Diagnosis and conditions
        diagnosis = clinical.get('diagnosis', {})
        if not diagnosis and 'patient' in clinical:
            # Fallback for old structure where diagnosis was under patient
            diagnosis = clinical['patient'].get('diagnosis', {})
        if diagnosis.get('primary'):
            text_parts.append(f"diagnosed with {diagnosis['primary'].lower()}")

        # Labs and criteria
        labs = clinical.get('labs', {})
        if labs.get('hba1c'):
            hba1c = labs['hba1c']
            text_parts.append(f"and HbA1c > {hba1c['target'].replace('< ', '')}%")

        # Recommendations
        recommendations = expectations.get('recommendations', [])
        if recommendations:
            drug_classes = [r.get('drug_class', '') for r in recommendations if r.get('drug_class')]
            if drug_classes:
                text_parts.append(f", {drug_classes[0].lower()} therapy should be initiated")

        text_parts.append("unless contraindicated.")

        return " ".join(text_parts)

    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """Extract text content from PDF file"""
        from pypdf import PdfReader

        reader = PdfReader(pdf_path)
        text_content = []

        for page in reader.pages:
            text = page.extract_text()
            if text.strip():
                text_content.append(text)

        return "\n\n".join(text_content)

    def parse_guidelines_from_pdf_text(self, pdf_text: str, pdf_name: str, pdf_path: str) -> List[Dict[str, Any]]:
        """Parse clinical guidelines from PDF text and generate comprehensive scenarios for each clinical directive"""
        scenarios = []

        # Split text into sections (rough approximation)
        sections = pdf_text.split('\n\n')

        # Look for recommendation patterns
        recommendations = []
        current_section = ""
        in_recommendations = False

        for section in sections:
            section = section.strip()
            if not section:
                continue

            # Look for recommendation patterns
            if any(keyword in section.lower() for keyword in ['recommend', 'initiate', 'start', 'prescribe', 'therapy']):
                if not in_recommendations:
                    in_recommendations = True
                    current_section = section
                else:
                    current_section += " " + section
            elif in_recommendations and len(current_section) > 100:
                recommendations.append(current_section)
                in_recommendations = False
                current_section = ""
            elif in_recommendations:
                current_section += " " + section

        # If still in recommendations at the end
        if current_section:
            recommendations.append(current_section)

        # Generate scenarios from recommendations
        for i, rec in enumerate(recommendations[:3]):  # Limit to first 3 recommendations
            scenario_id = f"{pdf_name.replace('.pdf', '')}_rec_{i+1:03d}"

            # Extract key clinical information
            scenario = {
                "scenario": {
                    "id": scenario_id,
                    "title": f"Clinical Recommendation from {pdf_name}",
                    "domain": "general-medicine",
                    "category": "treatment-recommendation",
                    "condition": "clinical-condition",
                    "version": "1.0",
                    "created": datetime.now().strftime("%Y-%m-%d"),
                    "author": "PDF Guideline Parser",
                    "guidelines": [{"name": pdf_name, "section": "Extracted Recommendations"}]
                },
                "clinical": {
                    "patient": {
                        "demographics": {"age": "adult", "gender": "not specified"},
                        "presentation": {"chief_complaint": "Clinical condition requiring treatment"}
                    },
                    "diagnosis": {"primary": "Clinical condition", "status": "requires treatment"},
                    "labs": {},
                    "medications": {"current": "none"},
                    "comorbidities": []
                },
                "expectations": {
                    "recommendations": [{"drug_class": "appropriate therapy", "rationale": rec[:200]}],
                    "treatment_strategy": {"approach": "Follow clinical guidelines"},
                    "monitoring": [],
                    "education": []
                },
                "testing": {
                    "complexity": "medium",
                    "fidelity": "medium",
                    "priority": "P2",
                    "tags": ["pdf-extracted", "guideline-based"],
                    "clinical_decision_points": ["Apply clinical recommendation"],
                    "edge_cases": []
                },
                "source": {
                    "original_file": pdf_name,
                    "original_location": pdf_path,
                    "migration_date": datetime.now().strftime("%Y-%m-%d"),
                    "notes": f"Auto-generated from PDF guideline extraction: {rec[:100]}..."
                }
            }

            # Try to extract more specific information
            rec_lower = rec.lower()

            # Look for specific conditions
            if 'diabetes' in rec_lower:
                scenario["scenario"]["condition"] = "diabetes"
                scenario["clinical"]["diagnosis"]["primary"] = "Diabetes Mellitus"
                if 'hba1c' in rec_lower:
                    scenario["clinical"]["labs"]["hba1c"] = {"value": "8.0", "unit": "%", "target": "< 7%"}

            # Look for specific medications
            if 'metformin' in rec_lower:
                scenario["expectations"]["recommendations"][0]["drug_class"] = "Metformin"
            elif 'sglt2' in rec_lower or 'empagliflozin' in rec_lower:
                scenario["expectations"]["recommendations"][0]["drug_class"] = "SGLT2 inhibitor"
            elif 'glp-1' in rec_lower or 'liraglutide' in rec_lower:
                scenario["expectations"]["recommendations"][0]["drug_class"] = "GLP-1 receptor agonist"

            scenarios.append(scenario)

        return scenarios

    def parse_guidelines_from_pdf_text_comprehensive(self, pdf_text: str, pdf_name: str, pdf_path: str) -> List[Dict[str, Any]]:
        """Parse clinical guidelines from PDF text and generate comprehensive scenarios for each clinical directive"""
        scenarios = []

        # Split into paragraphs and sections
        paragraphs = [p.strip() for p in pdf_text.split('\n\n') if p.strip() and len(p.strip()) > 50]

        # Look for clinical directives using keyword-based approach
        clinical_keywords = [
            'should', 'may', 'can', 'must', 'recommend', 'initiate', 'start', 'prescribe',
            'therapy', 'treatment', 'consider', 'use', 'add', 'combine', 'switch',
            'monitor', 'assess', 'evaluate', 'adjust', 'titrate', 'modify', 'target',
            'goal', 'aim', 'patients with', 'when', 'if', 'early use', 'offer', 'receive'
        ]

        clinical_directives = []
        import re

        print(f"Processing {len(paragraphs)} paragraphs...")

        paragraphs_with_keywords = 0
        paragraphs_skipped = 0

        for para in paragraphs:
            para_lower = para.lower()

            # Skip headers, references, tables, and acknowledgments
            # Be more specific to avoid skipping legitimate content
            skip_indicators = [
                'references', 'acknowledgments', 'disclosure',
                'author contributions', 'doi:', 'https://'
            ]
            should_skip = (
                para_lower.startswith('table ') or
                para_lower.startswith('figure ') or
                any(indicator in para_lower for indicator in skip_indicators)
            )

            if should_skip:
                paragraphs_skipped += 1
                continue

            # Look for paragraphs containing clinical keywords
            if any(keyword in para_lower for keyword in clinical_keywords):
                paragraphs_with_keywords += 1
                # Clean up the paragraph text (remove excessive line breaks)
                clean_para = re.sub(r'\n+', ' ', para)
                clean_para = re.sub(r'\s+', ' ', clean_para)

                # Split into sentences (handle various punctuation)
                sentences = re.split(r'[.!?]+', clean_para)
                clinical_sentences = []

                for sentence in sentences:
                    sentence = sentence.strip()
                    if len(sentence) < 15:  # Too short
                        continue

                    # Check if sentence contains clinical keywords
                    sentence_lower = sentence.lower()
                    if any(keyword in sentence_lower for keyword in clinical_keywords):
                        clinical_sentences.append(sentence)

                # Take the most relevant sentences (up to 3 per paragraph)
                for sentence in clinical_sentences[:3]:
                    if len(sentence) > 300:  # Truncate long sentences
                        sentence = sentence[:300] + "..."

                    clinical_directives.append({
                        'directive': sentence,
                        'context': clean_para[:500] if len(clean_para) > 500 else clean_para,
                        'paragraph': para
                    })

        # Remove duplicates and limit to most relevant
        unique_directives = []
        seen = set()
        for directive in clinical_directives:
            # Clean up the directive text
            clean_directive = directive['directive'].strip()
            if len(clean_directive) < 10:  # Too short
                continue
            if len(clean_directive) > 200:  # Too long, truncate
                clean_directive = clean_directive[:200] + "..."
            
            key = clean_directive.lower()[:30]  # Shorter key for better deduplication
            if key not in seen:
                unique_directives.append({
                    'directive': clean_directive,
                    'context': directive['context'],
                    'paragraph': directive['paragraph']
                })
                seen.add(key)

        print(f"Found {len(unique_directives)} unique clinical directives from PDF")
        print(f"Paragraphs processed: {len(paragraphs)}")
        print(f"Paragraphs skipped: {paragraphs_skipped}")
        print(f"Paragraphs with keywords: {paragraphs_with_keywords}")
        print(f"Sample directives: {[d['directive'][:50] + '...' for d in unique_directives[:3]]}")
        
        # Generate clinical contexts dynamically from guideline analysis (once per PDF)
        analyzer = GuidelineAnalyzer()
        pdf_path_full = Path(pdf_path)
        analysis = analyzer.analyze_guideline_from_file(pdf_path_full)
        
        # Generate scenarios from all clinical directives
        for i, directive_info in enumerate(unique_directives):
            directive = directive_info['directive']
            context = directive_info['context']

            # Use the pre-computed analysis to generate clinical contexts
            clinical_contexts = []
            for scenario in analysis.scenarios:
                # Create patient context from scenario
                patient_context = {
                    "patient": {
                        "demographics": {"age": "adult", "gender": "not specified"},
                        "presentation": {"chief_complaint": f"Management of {', '.join(scenario.patient_context.get('conditions', ['clinical condition']))}"},
                        "history": {"relevant_conditions": scenario.patient_context.get('conditions', [])}
                    },
                    "diagnosis": {
                        "primary": ', '.join(scenario.patient_context.get('conditions', ['Clinical condition'])),
                        "status": "requires clinical decision"
                    },
                    "specialty": scenario.patient_context.get('specialty', 'general'),
                    "cds_scenarios": [s.value for s in scenario.cds_scenarios],
                    "recommended_actions": [action['description'] for action in scenario.recommended_actions],
                    "clinical_observations": [
                        {
                            "type": obs.get('observation_type', 'condition'),
                            "value": obs.get('value', ''),
                            "interpretation": obs.get('interpretation', 'present')
                        } for obs in scenario.clinical_observations
                    ]
                }
                clinical_contexts.append(patient_context)
            
            print(f"DEBUG: Directive {i+1} has {len(clinical_contexts)} clinical contexts")

            # Create multiple scenarios per directive for comprehensive testing
            for context_idx, clinical_ctx in enumerate(clinical_contexts):
                print(f"DEBUG: Creating scenario for directive {i+1}, context {context_idx+1}")
                scenario_id = f"{pdf_name.replace('.pdf', '')}_directive_{i+1:03d}_context_{context_idx+1:02d}"
                scenario = {
                "scenario": {
                    "id": scenario_id,
                    "title": f"Clinical Directive: {directive[:80]}...",
                    "domain": "diabetes-management",
                    "category": "treatment-recommendation",
                    "condition": "diabetes",
                    "version": "1.0",
                    "created": datetime.now().strftime("%Y-%m-%d"),
                    "author": "AI Clinical Guideline Parser",
                    "guidelines": [{"name": pdf_name, "section": f"Clinical Directive {i+1}"}]
                },
                "clinical": copy.deepcopy(clinical_ctx),  # Use deep copy to avoid reference issues
                "expectations": {
                    "recommendations": [{"drug_class": directive[:100], "rationale": context[:200]}],
                    "treatment_strategy": {"approach": "Follow ADA guidelines"},
                    "monitoring": [{"parameter": "HbA1c", "frequency": "quarterly"}],
                    "education": [{"topic": "diabetes self-management"}]
                },
                "testing": {
                    "complexity": "medium",
                    "fidelity": "high",
                    "priority": "P1",
                    "tags": ["pdf-extracted", "clinical-directive", "ada-guideline"],
                    "clinical_decision_points": [f"Apply directive: {directive[:50]}"],
                    "edge_cases": ["Patient refusal", "Contraindications"]
                },
                "source": {
                    "original_file": pdf_name,
                    "original_location": pdf_path,
                    "extraction_method": "paragraph_analysis",
                    "directive_text": directive,
                    "context": context,
                    "migration_date": datetime.now().strftime("%Y-%m-%d"),
                    "notes": f"AI-extracted clinical directive from ADA guidelines: {directive[:100]}..."
                }
            }

                # Customize based on directive content
                directive_lower = directive.lower()
                if 'metformin' in directive_lower:
                    scenario["expectations"]["recommendations"][0]["drug_class"] = "Metformin"
                    scenario["clinical"]["medications"]["current"] = "none"
                elif 'insulin' in directive_lower:
                    scenario["expectations"]["recommendations"][0]["drug_class"] = "Insulin therapy"
                    scenario["clinical"]["diagnosis"]["severity"] = "poor glycemic control"
                elif 'sglt2' in directive_lower or 'empagliflozin' in directive_lower:
                    scenario["expectations"]["recommendations"][0]["drug_class"] = "SGLT2 inhibitor"
                    scenario["clinical"]["comorbidities"].append({"name": "Cardiovascular disease", "risk_level": "high"})
                elif 'glp-1' in directive_lower or 'liraglutide' in directive_lower:
                    scenario["expectations"]["recommendations"][0]["drug_class"] = "GLP-1 receptor agonist"
                    scenario["clinical"]["diagnosis"]["complications"] = "overweight"

                scenarios.append(scenario)
                print(f"DEBUG: Appended scenario {len(scenarios)}: {scenario['scenario']['id']}")

        print(f"DEBUG: About to return {len(scenarios)} scenarios from comprehensive function")
        return scenarios

    def test_pdf_processing(self, pdf_path: str):
        """Test processing a PDF guideline file"""
        pdf_file = Path(pdf_path)
        if not pdf_file.exists():
            print(f"❌ PDF file not found: {pdf_path}")
            return False

        pdf_name = pdf_file.stem
        print(f"\n{'='*80}")
        print(f"TESTING PDF: {pdf_name}")
        print(f"PATH: {pdf_path}")
        print('='*80)

        try:
            # Extract text from PDF
            print("📄 Extracting text from PDF...")
            pdf_text = self.extract_text_from_pdf(pdf_file)
            print(f"✅ Extracted {len(pdf_text)} characters from PDF")

            # Parse guidelines and generate scenarios
            print("🔍 Parsing clinical guidelines...")
            scenarios = self.parse_guidelines_from_pdf_text_comprehensive(pdf_text, pdf_name, pdf_path)
            print(f"✅ Generated {len(scenarios)} clinical scenarios from PDF")

            if not scenarios:
                print("⚠️  No scenarios could be extracted from PDF")
                return False

            # Process each generated scenario
            successful_scenarios = 0
            topic = self.get_topic_from_pdf_path(pdf_path)
            for i, scenario in enumerate(scenarios):
                scenario_id = scenario["scenario"]["id"]
                print(f"\n📋 Processing scenario {i+1}/{len(scenarios)}: {scenario_id}")

                # Test the scenario
                if self.test_scenario_processing(scenario_id, scenario_data=scenario, topic=topic):
                    successful_scenarios += 1
                else:
                    print(f"❌ Failed to process scenario: {scenario_id}")

            print(f"\n{'='*80}")
            print(f"PDF PROCESSING SUMMARY: {pdf_name}")
            print(f"Scenarios Generated: {len(scenarios)}")
            print(f"Successful: {successful_scenarios}")
            print(f"Success Rate: {successful_scenarios/len(scenarios)*100:.1f}%")
            print('='*80)

            return successful_scenarios > 0

        except Exception as e:
            print(f"❌ Error processing PDF: {str(e)}")
            return False

    def test_scenario_processing(self, scenario_name: str, scenario_data: Optional[Dict[str, Any]] = None, topic: Optional[str] = None):
        """Test processing a single scenario through the full pipeline"""
        # Determine topic and create versioned run directory
        if topic is None:
            topic = self.get_topic_from_scenario(scenario_name)
        run_dir = self.create_versioned_run_dir(topic, scenario_name)
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_prefix = f"{scenario_name}_{timestamp}"
        
        print(f"\n{'='*80}")
        print(f"TESTING SCENARIO: {scenario_name}")
        print(f"TOPIC: {topic}")
        print(f"RUN DIR: {run_dir}")
        print(f"OUTPUT PREFIX: {output_prefix}")
        print('='*80)

        # Initialize run summary
        run_summary = {
            "scenario": scenario_name,
            "topic": topic,
            "timestamp": datetime.now().isoformat(),
            "run_directory": str(run_dir.relative_to(self.generated_dir)),
            "tests": [],
            "overall_status": "running"
        }

        # Load scenario
        if scenario_data is not None:
            yaml_scenario = scenario_data
            print(f"✅ Using provided scenario data: {yaml_scenario['scenario']['title']}")
        else:
            scenario_path = self.project_root / "examples" / "bdd-tests" / "scenarios" / f"{scenario_name}.yaml"
            if not scenario_path.exists():
                print(f"❌ Scenario file not found: {scenario_path}")
                return False

            yaml_scenario = self.load_scenario_from_yaml(scenario_path)
            print(f"✅ Loaded scenario: {yaml_scenario['scenario']['title']}")

        try:

            # Step 1: Create clinical text for CIKG processing
            clinical_text = self.create_clinical_text_from_scenario(yaml_scenario)
            print(f"📝 Generated clinical text: {clinical_text[:100]}...")

            # Create temporary JSON file for CIKG
            cikg_input = {
                "text": clinical_text,
                "source": yaml_scenario['scenario'].get('guidelines', [{}])[0].get('name', 'Clinical Guideline'),
                "category": yaml_scenario['scenario'].get('category', 'treatment')
            }

            cikg_file = self.project_root / "temp_cikg_input.json"
            with open(cikg_file, 'w') as f:
                json.dump([cikg_input], f, indent=2)

            # Step 2: Process with CIKG
            print("🔬 Processing with CIKG...")
            cikg_result = subprocess.run(
                [self.python_cmd, "poc/cikg-processor/poc_cikg_processor.py", str(cikg_file)],
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=15
            )

            if cikg_result.returncode == 0:
                print("✅ CIKG processing successful")
                # Extract entities and triples count
                output = cikg_result.stdout
                if "Extracted" in output and "GSRL triples" in output:
                    print("📊 CIKG extracted clinical entities and generated knowledge triples")
                    
                    # Save CIKG output
                    cikg_output_file = run_dir / "cikg-triples" / f"{output_prefix}_cikg_output.json"
                    # Extract JSON from output for saving
                    output_lines = output.split('\n')
                    json_content = []
                    in_json = False
                    for line in output_lines:
                        if 'CIKG PROCESSING OUTPUT:' in line:
                            in_json = True
                            continue
                        elif line.startswith('=') and in_json:
                            if json_content:
                                break  # Stop at the end marker if we have content
                            # Skip separator lines before JSON
                            continue
                        elif in_json and line.strip():
                            json_content.append(line)
                    
                    cikg_success = False
                    if json_content:
                        try:
                            json_data = json.loads('\n'.join(json_content))
                            with open(cikg_output_file, 'w') as f:
                                json.dump(json_data, f, indent=2)
                            print(f"💾 Saved CIKG output to: {cikg_output_file}")
                            cikg_success = True
                        except:
                            print("⚠️  Could not parse CIKG JSON output")
                    
                    run_summary["tests"].append({
                        "test": "CIKG Processing",
                        "status": "success" if cikg_success else "warning",
                        "output_file": str(cikg_output_file.relative_to(self.generated_dir)) if cikg_success else None,
                        "timestamp": datetime.now().isoformat()
                    })
                else:
                    print("⚠️  CIKG output format unexpected")
                    run_summary["tests"].append({
                        "test": "CIKG Processing",
                        "status": "warning",
                        "message": "Unexpected output format",
                        "timestamp": datetime.now().isoformat()
                    })
            else:
                print(f"❌ CIKG processing failed: {cikg_result.stderr}")
                run_summary["tests"].append({
                    "test": "CIKG Processing",
                    "status": "failed",
                    "error": cikg_result.stderr,
                    "timestamp": datetime.now().isoformat()
                })
                return False

            # Step 3: Convert scenario for BDD generation
            bdd_scenario = self.convert_scenario_for_bdd(yaml_scenario)
            print("🔄 Converted scenario for BDD generation")

            # Step 4: Start MCP server and process scenario
            print("🚀 Starting MCP server for scenario processing...")

            # Start MCP server
            mcp_process = subprocess.Popen(
                [self.python_cmd, "poc/mcp-server/poc_mcp_server.py"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.project_root
            )

            time.sleep(2)  # Wait for server to start

            try:
                # Initialize
                init_request = {
                    "jsonrpc": "2.0", "id": 1,
                    "method": "initialize",
                    "params": {
                        "protocolVersion": "1.0",
                        "capabilities": {},
                        "clientInfo": {"name": "guideline-tester", "version": "1.0"}
                    }
                }
                if mcp_process.stdin:
                    mcp_process.stdin.write(json.dumps(init_request) + "\n")
                    mcp_process.stdin.flush()

                    if mcp_process.stdout:
                        response = json.loads(mcp_process.stdout.readline().strip())
                        if "result" in response:
                            print("✅ MCP server initialized")
                        else:
                            print("❌ MCP initialization failed")
                            return False
                    else:
                        print("❌ No stdout from MCP server")
                        return False
                else:
                    print("❌ No stdin to MCP server")
                    return False

                # Configure coverage
                config_request = {
                    "jsonrpc": "2.0", "id": 2,
                    "method": "configure_coverage",
                    "params": {
                        "strategy": "tiered",
                        "default_tier": "high",
                        "categories": [yaml_scenario['scenario'].get('category', 'treatment-recommendation')]
                    }
                }
                if mcp_process.stdin:
                    mcp_process.stdin.write(json.dumps(config_request) + "\n")
                    mcp_process.stdin.flush()

                    if mcp_process.stdout:
                        response = json.loads(mcp_process.stdout.readline().strip())
                        if "result" in response:
                            print("✅ Coverage configured")
                        else:
                            print("❌ Coverage configuration failed")
                            return False
                    else:
                        print("❌ No stdout from MCP server")
                        return False
                else:
                    print("❌ No stdin to MCP server")
                    return False

                # Process scenario
                process_request = {
                    "jsonrpc": "2.0", "id": 3,
                    "method": "process_scenario",
                    "params": {
                        "scenario": bdd_scenario,
                        "coverage_config": {
                            "fidelity_level": "high",
                            "generation_mode": "comprehensive"
                        }
                    }
                }
                if mcp_process.stdin:
                    mcp_process.stdin.write(json.dumps(process_request) + "\n")
                    mcp_process.stdin.flush()

                    if mcp_process.stdout:
                        response = json.loads(mcp_process.stdout.readline().strip())
                        if "result" in response and response["result"].get("status") == "success":
                            print("✅ Scenario processed successfully")
                            print("📋 Generated BDD test scenarios")
                            
                            # Save MCP session log
                            mcp_log_file = run_dir / "mcp-logs" / f"{output_prefix}_mcp_session.json"
                            session_data = {
                                "timestamp": timestamp,
                                "scenario": scenario_name,
                                "requests": [
                                    {"method": "initialize", "status": "success"},
                                    {"method": "configure_coverage", "status": "success"},
                                    {"method": "process_scenario", "status": "success"}
                                ],
                                "generated_scenarios": response["result"].get("metadata", {}).get("scenarios_generated", 0)
                            }
                            with open(mcp_log_file, 'w') as f:
                                json.dump(session_data, f, indent=2)
                            print(f"💾 Saved MCP session log to: {mcp_log_file}")
                            
                            # Save BDD test scenarios
                            if "gherkin" in response["result"]:
                                bdd_file = run_dir / "bdd-tests" / f"{output_prefix}.feature"
                                with open(bdd_file, 'w') as f:
                                    f.write(response["result"]["gherkin"])
                                print(f"💾 Saved BDD test scenarios to: {bdd_file}")
                                
                                run_summary["tests"].append({
                                    "test": "BDD Generation",
                                    "status": "success", 
                                    "output_file": str(bdd_file.relative_to(self.generated_dir)),
                                    "timestamp": datetime.now().isoformat()
                                })
                            
                            run_summary["tests"].append({
                                "test": "MCP Processing",
                                "status": "success",
                                "output_file": str(mcp_log_file.relative_to(self.generated_dir)),
                                "generated_scenarios": response["result"].get("metadata", {}).get("scenarios_generated", 0),
                                "timestamp": datetime.now().isoformat()
                            })
                            
                        else:
                            print(f"❌ Scenario processing failed: {response}")
                            run_summary["tests"].append({
                                "test": "MCP Processing",
                                "status": "failed",
                                "error": str(response),
                                "timestamp": datetime.now().isoformat()
                            })
                            return False
                    else:
                        print("❌ No stdout from MCP server")
                        return False
                else:
                    print("❌ No stdin to MCP server")
                    return False

            finally:
                # Clean up
                mcp_process.terminate()
                mcp_process.wait(timeout=5)
                if cikg_file.exists():
                    cikg_file.unlink()

            print(f"✅ SUCCESS: {scenario_name} processed through complete pipeline")
            
            # Save run summary
            run_summary["overall_status"] = "success"
            run_summary["end_timestamp"] = datetime.now().isoformat()
            run_summary["duration_seconds"] = (datetime.fromisoformat(run_summary["end_timestamp"]) - datetime.fromisoformat(run_summary["timestamp"])).total_seconds()
            
            summary_file = run_dir / "run-summary.json"
            with open(summary_file, 'w') as f:
                json.dump(run_summary, f, indent=2)
            print(f"💾 Saved run summary to: {summary_file}")
            
            return True

        except Exception as e:
            print(f"❌ Error processing scenario: {str(e)}")
            return False

    def run_available_tests(self):
        """Run tests on all available scenarios"""
        scenarios_dir = self.project_root / "examples" / "bdd-tests" / "scenarios"
        scenario_files = [f for f in scenarios_dir.glob("*.yaml") if not f.name.startswith('.') and not f.name.endswith('.assert.yaml')]

        print(f"Found {len(scenario_files)} clinical scenarios to test:")
        for f in scenario_files:
            print(f"  - {f.stem}")

        successful = 0
        total = len(scenario_files)

        for scenario_file in scenario_files:
            scenario_name = scenario_file.stem
            if self.test_scenario_processing(scenario_name):
                successful += 1

        print(f"\n{'='*80}")
        print("TEST SUMMARY")
        print('='*80)
        print(f"Scenarios tested: {total}")
        print(f"Successful: {successful}")
        print(f"Failed: {total - successful}")

        if successful == total:
            print("🎉 ALL SCENARIOS PROCESSED SUCCESSFULLY!")
            print("The clinical BDD creator is ready for production use.")
            
            # Save overall summary report
            overall_summary = {
                "timestamp": datetime.now().isoformat(),
                "test_type": "comprehensive_guideline_processing",
                "scenarios_tested": total,
                "successful": successful,
                "failed": total - successful,
                "success_rate": successful / total if total > 0 else 0,
                "status": "PASSED" if successful == total else "FAILED",
                "topics_covered": list(set(self.get_topic_from_scenario(f.stem) for f in scenario_files)),
                "run_version": datetime.now().strftime("%Y-%m-%d_v1")
            }
            
            summary_file = self.generated_dir / "summary-reports" / "overall-summary.json"
            with open(summary_file, 'w') as f:
                json.dump(overall_summary, f, indent=2)
            print(f"💾 Saved overall summary to: {summary_file}")
            
        else:
            print("⚠️  Some scenarios failed processing.")
            print("Check the output above for details.")

        return successful == total

def main():
    """Main test execution"""
    tester = GuidelineTester()

    if len(sys.argv) > 1:
        input_arg = sys.argv[1]

        # Check if it's a PDF file
        if input_arg.endswith('.pdf'):
            success = tester.test_pdf_processing(input_arg)
            sys.exit(0 if success else 1)
        else:
            # Test specific scenario
            scenario_name = input_arg
            success = tester.test_scenario_processing(scenario_name)
            sys.exit(0 if success else 1)
    else:
        # Test all scenarios
        success = tester.run_available_tests()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()