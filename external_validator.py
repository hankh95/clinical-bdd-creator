#!/usr/bin/env python3
"""
External AI Validation System - Phase 1

Validates BDD test scenarios using multiple external AI providers.
Uses Doppler for secret management to access OpenAI and xAI APIs.

Supports 2-4 different validators with model selection (default GPT-4o).
"""

import os
import json
import asyncio
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import aiohttp
import openai
from openai import AsyncOpenAI

class AIProvider(Enum):
    """Supported AI providers for validation"""
    OPENAI = "openai"
    XAI = "xai"
    ANTHROPIC = "anthropic"  # Future expansion
    GOOGLE = "google"        # Future expansion

class AIModel(Enum):
    """Available models across providers"""
    GPT_4O = "gpt-4o"
    GPT_4_TURBO = "gpt-4-turbo-preview"
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    XAI_GROK = "grok-beta"

@dataclass
class ValidationResult:
    """Result from external AI validation"""
    provider: AIProvider
    model: AIModel
    scenario_id: str
    clinical_accuracy_score: float  # 0.0 to 1.0
    reasoning_quality_score: float  # 0.0 to 1.0
    response: str
    validation_criteria: Dict[str, bool]
    error: Optional[str] = None

@dataclass
class ComparativeValidation:
    """Comparative analysis across multiple AI providers"""
    scenario_id: str
    validations: List[ValidationResult]
    consensus_score: float
    agreement_level: str  # "high", "medium", "low", "conflicting"
    recommended_improvements: List[str]

class SecretManager:
    """Manages API secrets using Doppler"""

    def __init__(self):
        self.secrets = {}
        self._load_secrets()

    def _load_secrets(self):
        """Load secrets from Doppler"""
        try:
            # Run Doppler command to get secrets
            result = subprocess.run(
                ["doppler", "secrets", "download", "--no-file"],
                capture_output=True,
                text=True,
                check=True
            )

            # Parse JSON output
            secrets_json = json.loads(result.stdout)
            self.secrets = secrets_json

        except subprocess.CalledProcessError as e:
            print(f"Warning: Could not load Doppler secrets: {e}")
            print("Falling back to environment variables")
            self._fallback_env_secrets()

        except json.JSONDecodeError:
            print("Warning: Invalid Doppler secrets format")
            self._fallback_env_secrets()

    def _fallback_env_secrets(self):
        """Fallback to environment variables"""
        self.secrets = {
            "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
            "XAI_API_KEY": os.getenv("XAI_API_KEY", ""),
            "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY", ""),
            "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY", ""),
        }

    def get_secret(self, key: str) -> str:
        """Get a secret value"""
        return self.secrets.get(key, "")

class AIValidator:
    """Validates BDD scenarios using external AI providers"""

    def __init__(self):
        self.secret_manager = SecretManager()
        self.clients = self._initialize_clients()

    def _initialize_clients(self) -> Dict[AIProvider, Any]:
        """Initialize API clients for each provider"""
        clients = {}

        # OpenAI client
        openai_key = self.secret_manager.get_secret("OPENAI_API_KEY")
        if openai_key:
            clients[AIProvider.OPENAI] = AsyncOpenAI(api_key=openai_key)

        # xAI client (using OpenAI-compatible interface)
        xai_key = self.secret_manager.get_secret("XAI_API_KEY")
        if xai_key:
            clients[AIProvider.XAI] = AsyncOpenAI(
                api_key=xai_key,
                base_url="https://api.x.ai/v1"
            )

        return clients

    async def validate_scenario(
        self,
        scenario: Dict[str, Any],
        providers: List[AIProvider] = None,
        models: Dict[AIProvider, AIModel] = None
    ) -> List[ValidationResult]:
        """
        Validate a single BDD scenario using multiple AI providers

        Args:
            scenario: BDD scenario dictionary
            providers: List of providers to use (default: all available)
            models: Specific models per provider (default: GPT-4o for OpenAI, Grok for xAI)
        """

        if providers is None:
            providers = list(self.clients.keys())

        if models is None:
            models = {
                AIProvider.OPENAI: AIModel.GPT_4O,
                AIProvider.XAI: AIModel.XAI_GROK,
            }

        # Filter to available providers
        available_providers = [p for p in providers if p in self.clients]

        if not available_providers:
            return [ValidationResult(
                provider=AIProvider.OPENAI,
                model=AIModel.GPT_4O,
                scenario_id=scenario.get('id', 'unknown'),
                clinical_accuracy_score=0.0,
                reasoning_quality_score=0.0,
                response="",
                validation_criteria={},
                error="No AI providers available"
            )]

        # Run validations in parallel
        tasks = []
        for provider in available_providers:
            model = models.get(provider, AIModel.GPT_4O)
            task = self._validate_with_provider(scenario, provider, model)
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out exceptions and return valid results
        valid_results = []
        for result in results:
            if isinstance(result, ValidationResult):
                valid_results.append(result)
            else:
                # Log exception
                print(f"Validation error: {result}")

        return valid_results

    async def _validate_with_provider(
        self,
        scenario: Dict[str, Any],
        provider: AIProvider,
        model: AIModel
    ) -> ValidationResult:
        """Validate scenario with a specific provider"""

        scenario_id = scenario.get('id', 'unknown')

        try:
            client = self.clients[provider]

            # Create validation prompt
            prompt = self._create_validation_prompt(scenario)

            # Call appropriate API
            if provider == AIProvider.OPENAI:
                response = await self._call_openai(client, model.value, prompt)
            elif provider == AIProvider.XAI:
                response = await self._call_xai(client, model.value, prompt)
            else:
                raise ValueError(f"Unsupported provider: {provider}")

            # Parse and score response
            scores = self._score_validation_response(response)

            return ValidationResult(
                provider=provider,
                model=model,
                scenario_id=scenario_id,
                clinical_accuracy_score=scores['clinical_accuracy'],
                reasoning_quality_score=scores['reasoning_quality'],
                response=response,
                validation_criteria=scores['criteria']
            )

        except Exception as e:
            return ValidationResult(
                provider=provider,
                model=model,
                scenario_id=scenario_id,
                clinical_accuracy_score=0.0,
                reasoning_quality_score=0.0,
                response="",
                validation_criteria={},
                error=str(e)
            )

    def _create_validation_prompt(self, scenario: Dict[str, Any]) -> str:
        """Create validation prompt for AI providers"""

        # Extract scenario components
        given = scenario.get('given', '')
        when = scenario.get('when', '')
        then = scenario.get('then', '')

        prompt = f"""
You are a clinical informatics expert validating a Behavior-Driven Development (BDD) test scenario for clinical decision support.

Please evaluate the following BDD scenario for clinical accuracy and reasoning quality:

**Given:** {given}
**When:** {when}
**Then:** {then}

**Validation Criteria:**
1. **Clinical Accuracy (0-10)**: Does this scenario reflect real clinical practice and guideline recommendations?
2. **Patient Safety (Yes/No)**: Does this scenario promote safe clinical decisions?
3. **Evidence-Based (Yes/No)**: Is this based on established clinical evidence?
4. **Logical Consistency (Yes/No)**: Does the scenario logic make clinical sense?
5. **Completeness (Yes/No)**: Does the scenario cover all necessary clinical considerations?

**Response Format:**
Please provide your evaluation in the following JSON format:
{{
    "clinical_accuracy_score": <0-10>,
    "patient_safety": <true/false>,
    "evidence_based": <true/false>,
    "logical_consistency": <true/false>,
    "completeness": <true/false>,
    "reasoning": "<brief explanation of your evaluation>",
    "improvements": ["<suggested improvement 1>", "<suggested improvement 2>"]
}}

Your evaluation:
"""

        return prompt

    async def _call_openai(self, client: AsyncOpenAI, model: str, prompt: str) -> str:
        """Call OpenAI API"""
        response = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,  # Low temperature for consistent evaluation
            max_tokens=1000
        )
        return response.choices[0].message.content

    async def _call_xai(self, client: AsyncOpenAI, model: str, prompt: str) -> str:
        """Call xAI API (using OpenAI-compatible interface)"""
        response = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=1000
        )
        return response.choices[0].message.content

    def _score_validation_response(self, response: str) -> Dict[str, Any]:
        """Parse and score AI validation response"""

        try:
            # Try to parse as JSON
            data = json.loads(response)

            # Extract scores
            clinical_score = min(max(data.get('clinical_accuracy_score', 0) / 10.0, 0.0), 1.0)

            # Calculate reasoning quality based on criteria
            criteria = {
                'patient_safety': data.get('patient_safety', False),
                'evidence_based': data.get('evidence_based', False),
                'logical_consistency': data.get('logical_consistency', False),
                'completeness': data.get('completeness', False)
            }

            reasoning_score = sum(criteria.values()) / len(criteria)

            return {
                'clinical_accuracy': clinical_score,
                'reasoning_quality': reasoning_score,
                'criteria': criteria
            }

        except json.JSONDecodeError:
            # Fallback scoring for non-JSON responses
            return {
                'clinical_accuracy': 0.5,  # Neutral score
                'reasoning_quality': 0.5,
                'criteria': {
                    'patient_safety': 'unknown' in response.lower(),
                    'evidence_based': 'evidence' in response.lower(),
                    'logical_consistency': 'consistent' in response.lower(),
                    'completeness': 'complete' in response.lower()
                }
            }

    async def comparative_validation(
        self,
        scenarios: List[Dict[str, Any]],
        providers: List[AIProvider] = None
    ) -> List[ComparativeValidation]:
        """Run comparative validation across multiple providers"""

        comparative_results = []

        for scenario in scenarios:
            # Get individual validations
            validations = await self.validate_scenario(scenario, providers)

            if not validations:
                continue

            # Calculate consensus
            clinical_scores = [v.clinical_accuracy_score for v in validations]
            reasoning_scores = [v.reasoning_quality_score for v in validations]

            avg_clinical = sum(clinical_scores) / len(clinical_scores)
            avg_reasoning = sum(reasoning_scores) / len(reasoning_scores)
            consensus_score = (avg_clinical + avg_reasoning) / 2.0

            # Determine agreement level
            clinical_std = (sum((x - avg_clinical) ** 2 for x in clinical_scores) / len(clinical_scores)) ** 0.5
            agreement_level = "high" if clinical_std < 0.2 else "medium" if clinical_std < 0.4 else "low"

            # Collect improvement suggestions
            improvements = []
            for validation in validations:
                if hasattr(validation, 'response') and 'improvements' in validation.response:
                    try:
                        data = json.loads(validation.response)
                        improvements.extend(data.get('improvements', []))
                    except:
                        pass

            comparative_results.append(ComparativeValidation(
                scenario_id=scenario.get('id', 'unknown'),
                validations=validations,
                consensus_score=consensus_score,
                agreement_level=agreement_level,
                recommended_improvements=list(set(improvements))  # Remove duplicates
            ))

        return comparative_results

    def generate_validation_report(self, comparative_results: List[ComparativeValidation]) -> Dict[str, Any]:
        """Generate comprehensive validation report"""

        total_scenarios = len(comparative_results)
        avg_consensus = sum(r.consensus_score for r in comparative_results) / total_scenarios

        agreement_distribution = {}
        for result in comparative_results:
            agreement_distribution[result.agreement_level] = agreement_distribution.get(result.agreement_level, 0) + 1

        # Collect all improvement suggestions
        all_improvements = []
        for result in comparative_results:
            all_improvements.extend(result.recommended_improvements)

        # Find most common improvements
        improvement_counts = {}
        for imp in all_improvements:
            improvement_counts[imp] = improvement_counts.get(imp, 0) + 1

        top_improvements = sorted(improvement_counts.items(), key=lambda x: x[1], reverse=True)[:10]

        return {
            "summary": {
                "total_scenarios_validated": total_scenarios,
                "average_consensus_score": round(avg_consensus, 3),
                "agreement_distribution": agreement_distribution
            },
            "top_improvements": top_improvements,
            "detailed_results": [
                {
                    "scenario_id": r.scenario_id,
                    "consensus_score": round(r.consensus_score, 3),
                    "agreement_level": r.agreement_level,
                    "provider_scores": [
                        {
                            "provider": v.provider.value,
                            "model": v.model.value,
                            "clinical_accuracy": round(v.clinical_accuracy_score, 3),
                            "reasoning_quality": round(v.reasoning_quality_score, 3)
                        } for v in r.validations
                    ],
                    "improvements": r.recommended_improvements
                } for r in comparative_results
            ]
        }