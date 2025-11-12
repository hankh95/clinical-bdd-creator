#!/usr/bin/env python3
"""
Debug script for Layer 1 relationship extraction
"""

import sys
import os
sys.path.append('/Users/hankhead/Projects/Personal/clinical-bdd-creator/santiago-service/src')

from santiago_service import SantiagoService
from semantic_relationships import RelationshipType
import asyncio