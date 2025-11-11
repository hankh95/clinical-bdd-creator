"""
Scenario Loader for Fishnet Testing Framework

Loads clinical BDD scenarios from YAML files and prepares them for validation testing.
"""

import yaml
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional


@dataclass
class ClinicalScenario:
    """Represents a clinical BDD scenario for testing"""
    
    scenario_id: str
    title: str
    domain: str
    category: str
    condition: str
    version: str
    guidelines: List[Dict[str, str]]
    
    # Clinical context
    patient: Dict[str, Any]
    diagnosis: Dict[str, Any]
    vitals: Dict[str, Any]
    labs: Dict[str, Any]
    medications: Dict[str, Any]
    comorbidities: List[str]
    contraindications: Dict[str, Any]
    
    # Expected outcomes
    expectations: Dict[str, Any]
    
    # Testing metadata
    testing: Dict[str, Any]
    
    # Source information
    source: Optional[Dict[str, Any]] = None
    
    # Santiago-specific assertions
    santiago_assertions: Optional[Dict[str, Any]] = None
    
    # File paths
    yaml_path: Optional[Path] = None
    feature_path: Optional[Path] = None
    assertions_path: Optional[Path] = None
    santiago_assertions_path: Optional[Path] = None


class ScenarioLoader:
    """Loads and manages clinical BDD scenarios"""
    
    def __init__(self, scenarios_base_path: Optional[Path] = None):
        """
        Initialize the scenario loader
        
        Args:
            scenarios_base_path: Base path for BDD scenarios. Defaults to examples/bdd-tests/scenarios/
        """
        if scenarios_base_path is None:
            # Default to examples/bdd-tests/scenarios relative to repository root
            repo_root = Path(__file__).parent.parent.parent.parent.parent
            scenarios_base_path = repo_root / "examples" / "bdd-tests" / "scenarios"
        
        self.scenarios_base_path = Path(scenarios_base_path)
        self._scenario_cache: Dict[str, ClinicalScenario] = {}
    
    def load_scenario(self, scenario_id: str, load_santiago_assertions: bool = True) -> ClinicalScenario:
        """
        Load a clinical scenario by ID
        
        Args:
            scenario_id: Unique scenario identifier (e.g., "cardiology-treatment-hfref-001")
            load_santiago_assertions: Whether to load Santiago-specific assertions
        
        Returns:
            ClinicalScenario object
        
        Raises:
            FileNotFoundError: If scenario files don't exist
            ValueError: If scenario data is invalid
        """
        # Check cache first
        if scenario_id in self._scenario_cache:
            return self._scenario_cache[scenario_id]
        
        # Build file paths
        yaml_path = self.scenarios_base_path / f"{scenario_id}.yaml"
        feature_path = self.scenarios_base_path / f"{scenario_id}.feature"
        assertions_path = self.scenarios_base_path / f"{scenario_id}.assert.yaml"
        santiago_assertions_path = self.scenarios_base_path / f"{scenario_id}.santiago.yaml"
        
        # Check if files exist
        if not yaml_path.exists():
            raise FileNotFoundError(f"Clinical scenario YAML not found: {yaml_path}")
        
        # Load clinical scenario YAML
        with open(yaml_path, 'r') as f:
            scenario_data = yaml.safe_load(f)
        
        # Extract main sections
        scenario_info = scenario_data.get('scenario', {})
        clinical = scenario_data.get('clinical', {})
        expectations = scenario_data.get('expectations', {})
        testing = scenario_data.get('testing', {})
        source = scenario_data.get('source', None)
        
        # Load Santiago assertions if requested and file exists
        santiago_assertions = None
        if load_santiago_assertions and santiago_assertions_path.exists():
            with open(santiago_assertions_path, 'r') as f:
                santiago_assertions = yaml.safe_load(f)
        
        # Create scenario object
        scenario = ClinicalScenario(
            scenario_id=scenario_info.get('id', scenario_id),
            title=scenario_info.get('title', ''),
            domain=scenario_info.get('domain', ''),
            category=scenario_info.get('category', ''),
            condition=scenario_info.get('condition', ''),
            version=scenario_info.get('version', '1.0'),
            guidelines=scenario_info.get('guidelines', []),
            
            patient=clinical.get('patient', {}),
            diagnosis=clinical.get('diagnosis', {}),
            vitals=clinical.get('vitals', {}),
            labs=clinical.get('labs', {}),
            medications=clinical.get('medications', {}),
            comorbidities=clinical.get('comorbidities', []),
            contraindications=clinical.get('contraindications', {}),
            
            expectations=expectations,
            testing=testing,
            source=source,
            santiago_assertions=santiago_assertions,
            
            yaml_path=yaml_path,
            feature_path=feature_path if feature_path.exists() else None,
            assertions_path=assertions_path if assertions_path.exists() else None,
            santiago_assertions_path=santiago_assertions_path if santiago_assertions_path.exists() else None,
        )
        
        # Cache the scenario
        self._scenario_cache[scenario_id] = scenario
        
        return scenario
    
    def load_scenarios_by_domain(self, domain: str) -> List[ClinicalScenario]:
        """
        Load all scenarios for a specific clinical domain
        
        Args:
            domain: Clinical domain (e.g., "cardiology", "oncology")
        
        Returns:
            List of ClinicalScenario objects
        """
        scenarios = []
        
        # Find all YAML files in scenarios directory
        for yaml_file in self.scenarios_base_path.glob("*.yaml"):
            # Skip assertion files
            if yaml_file.stem.endswith('.assert') or yaml_file.stem.endswith('.santiago'):
                continue
            
            # Load scenario
            try:
                scenario = self.load_scenario(yaml_file.stem)
                if scenario.domain == domain:
                    scenarios.append(scenario)
            except Exception as e:
                print(f"Warning: Failed to load scenario {yaml_file.stem}: {e}")
        
        return scenarios
    
    def list_available_scenarios(self) -> List[str]:
        """
        List all available scenario IDs
        
        Returns:
            List of scenario IDs
        """
        scenario_ids = []
        
        for yaml_file in self.scenarios_base_path.glob("*.yaml"):
            # Skip assertion files
            if yaml_file.stem.endswith('.assert') or yaml_file.stem.endswith('.santiago'):
                continue
            scenario_ids.append(yaml_file.stem)
        
        return sorted(scenario_ids)
    
    def clear_cache(self):
        """Clear the scenario cache"""
        self._scenario_cache.clear()


def load_santiago_assertions(scenario_id: str, base_path: Optional[Path] = None) -> Optional[Dict[str, Any]]:
    """
    Load Santiago-specific assertions for a scenario
    
    Args:
        scenario_id: Scenario identifier
        base_path: Base path for scenarios (defaults to examples/bdd-tests/scenarios/)
    
    Returns:
        Santiago assertions dictionary or None if file doesn't exist
    """
    if base_path is None:
        repo_root = Path(__file__).parent.parent.parent.parent.parent
        base_path = repo_root / "examples" / "bdd-tests" / "scenarios"
    
    santiago_path = Path(base_path) / f"{scenario_id}.santiago.yaml"
    
    if not santiago_path.exists():
        return None
    
    with open(santiago_path, 'r') as f:
        return yaml.safe_load(f)
