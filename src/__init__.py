"""
Smart Fridge AI System
A comprehensive AI-powered refrigerator management system
"""

__version__ = '1.0.0'
__author__ = 'Smart Fridge AI Team'
__license__ = 'MIT'

from .database import FridgeDatabase
from .food_detector import FoodDetector
from .expiry_tracker import ExpiryTracker, AlertManager
from .recipe_generator import RecipeGenerator

__all__ = [
    'FridgeDatabase',
    'FoodDetector',
    'ExpiryTracker',
    'AlertManager',
    'RecipeGenerator'
]
