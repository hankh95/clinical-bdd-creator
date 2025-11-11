"""
Fishnet: Santiago-BDD Testing Framework

This package provides the core testing framework for validating clinical knowledge graphs,
neurosymbolic reasoning, and clinical decision support in the Santiago service.
"""

from .framework.scenario_loader import ScenarioLoader, ClinicalScenario
from .framework.graph_validator import GraphValidator, GraphValidationResult
from .framework.reasoning_tester import ReasoningTester, ReasoningTestResult
from .framework.qa_validator import QAValidator, QAValidationResult
from .framework.whatif_engine import WhatIfEngine, WhatIfResult
from .framework.assertion_engine import AssertionEngine, AssertionResult

__all__ = [
    'ScenarioLoader',
    'ClinicalScenario',
    'GraphValidator',
    'GraphValidationResult',
    'ReasoningTester',
    'ReasoningTestResult',
    'QAValidator',
    'QAValidationResult',
    'WhatIfEngine',
    'WhatIfResult',
    'AssertionEngine',
    'AssertionResult',
]

__version__ = '1.0.0'
__author__ = 'Clinical BDD Creator Team'
