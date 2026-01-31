"""
Configuration settings for Smart Fridge AI System
"""
import os
from datetime import timedelta

# Base Directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database Configuration
DATABASE_PATH = os.path.join(BASE_DIR, 'data', 'smart_fridge.db')

# Model Paths
FOOD_DETECTION_MODEL = os.path.join(BASE_DIR, 'models', 'yolov8_food.pt')
OCR_MODEL = 'easyocr'  # or 'tesseract'

# Camera Configuration
CAMERA_ID = 0  # Default camera
IMAGE_SIZE = (640, 640)
CONFIDENCE_THRESHOLD = 0.5

# Expiry Alert Thresholds (in days)
ALERT_THRESHOLDS = {
    'critical': 1,    # Alert when 1 day left
    'warning': 3,     # Alert when 3 days left
    'normal': 7       # Alert when 7 days left
}

# Food Categories
FOOD_CATEGORIES = [
    'Vegetables',
    'Fruits',
    'Dairy',
    'Meat',
    'Seafood',
    'Beverages',
    'Condiments',
    'Leftovers',
    'Frozen',
    'Others'
]

# Shelf Life Defaults (in days) - used if expiry date not detected
DEFAULT_SHELF_LIFE = {
    'Vegetables': 7,
    'Fruits': 5,
    'Dairy': 7,
    'Meat': 3,
    'Seafood': 2,
    'Beverages': 30,
    'Condiments': 180,
    'Leftovers': 3,
    'Frozen': 90,
    'Others': 7
}

# Dashboard Configuration
DASHBOARD_PORT = 8050
DASHBOARD_HOST = '0.0.0.0'

# API Configuration
API_PORT = 5000
API_HOST = '0.0.0.0'

# Notification Settings
ENABLE_DESKTOP_NOTIFICATIONS = True
ENABLE_EMAIL_NOTIFICATIONS = False
ENABLE_SMS_NOTIFICATIONS = False

# Email Settings (if enabled)
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = os.getenv('SENDER_EMAIL', '')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD', '')

# SMS Settings (if enabled)
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER', '')

# Recipe Generation
RECIPE_API_KEY = os.getenv('OPENAI_API_KEY', '')  # For AI-powered recipe generation
MAX_INGREDIENTS_FOR_RECIPE = 10

# Logging
LOG_LEVEL = 'INFO'
LOG_FILE = os.path.join(BASE_DIR, 'logs', 'smart_fridge.log')

# Scan Schedule
AUTO_SCAN_ENABLED = True
SCAN_INTERVAL_HOURS = 12  # Scan every 12 hours
