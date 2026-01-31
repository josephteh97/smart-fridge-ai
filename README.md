# 🧊 Smart Fridge AI System

An intelligent AI-powered refrigerator management system that uses computer vision, OCR, and machine learning to track food items, monitor expiry dates, send alerts, and generate recipes using ingredients that are about to expire.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## 🎯 Features

### Core Functionality
- **🔍 Automated Food Detection**: Uses YOLOv8 for real-time food item recognition
- **📸 Camera Integration**: Scans fridge contents using embedded or external camera
- **📝 OCR Text Extraction**: Reads expiry dates from product labels
- **📊 Barcode Scanning**: Identifies products via barcode/QR code
- **⏰ Expiry Tracking**: Monitors shelf life with configurable alert thresholds
- **🔔 Multi-Channel Alerts**: Desktop notifications, email, and SMS alerts
- **🍳 AI Recipe Generation**: Creates recipes using expiring ingredients (GPT-powered)
- **📈 Analytics Dashboard**: Real-time monitoring and waste analytics
- **🗄️ Database Management**: SQLite database for persistent storage

### Alert System
- **Critical Alerts**: Items expiring within 1 day
- **Warning Alerts**: Items expiring within 3 days
- **Normal Alerts**: Items expiring within 7 days
- Customizable thresholds for each category

### Recipe Intelligence
- AI-powered recipe suggestions
- Uses ingredients about to expire
- Supports dietary restrictions
- Multiple cuisine types
- Step-by-step instructions

## 🏗️ System Architecture

```
smart_fridge_ai/
├── src/
│   ├── config.py              # Configuration settings
│   ├── database.py            # Database management
│   ├── food_detector.py       # Computer vision & OCR
│   ├── expiry_tracker.py      # Expiry monitoring & alerts
│   └── recipe_generator.py    # AI recipe generation
├── models/                    # Trained ML models
├── data/
│   ├── scans/                # Stored scan images
│   ├── recipes/              # Generated recipes
│   └── smart_fridge.db       # SQLite database
├── docs/
│   ├── WORKFLOW.md           # System workflow diagram
│   └── system_workflow_diagram.png
├── static/                   # Static assets
├── templates/                # HTML templates
├── dashboard.py              # Streamlit web interface
├── main.py                   # Main application
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## 📋 Prerequisites

- Python 3.8 or higher
- Anaconda or Miniconda (recommended)
- Camera (USB webcam or integrated camera)
- (Optional) GPU for faster processing

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/smart-fridge-ai.git
cd smart-fridge-ai
```

### 2. Create Anaconda Environment
```bash
# Create environment
conda create -n smart_fridge python=3.9 -y

# Activate environment
conda activate smart_fridge
```

### 3. Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt

# Install Tesseract OCR (for OCR functionality)
# Ubuntu/Debian:
sudo apt-get install tesseract-ocr

# macOS:
brew install tesseract

# Windows:
# Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
```

### 4. Download Pre-trained Models (Optional)
```bash
# YOLOv8 food detection model
# You can train your own or use a pre-trained model
# Place the model file in: models/yolov8_food.pt
```

### 5. Configure Environment Variables (Optional)
Create a `.env` file in the root directory:
```bash
# For AI recipe generation
OPENAI_API_KEY=your_openai_api_key

# For email notifications
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password

# For SMS notifications
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=your_twilio_phone
```

## 🎮 Usage

### Option 1: Command Line Interface

```bash
# Run the main application
python main.py
```

**Main Menu Options:**
1. Scan Fridge - Capture and process fridge contents
2. Check Alerts - View pending alerts
3. Generate Recipe - Create recipe from expiring items
4. View Status - Display system status
5. Start Scheduled Tasks - Enable automatic scanning
6. Launch Dashboard - Open web interface
7. Exit

### Option 2: Web Dashboard

```bash
# Launch the Streamlit dashboard
streamlit run dashboard.py
```

Access the dashboard at: `http://localhost:8501`

**Dashboard Features:**
- 📊 Real-time inventory overview
- 🗂️ Category-wise food distribution
- ⏰ Expiry timeline visualization
- 🔔 Alert management
- 🍳 Recipe generation
- 📈 Statistics and analytics

### Option 3: Python API

```python
from src.database import FridgeDatabase
from src.food_detector import FoodDetector
from src.expiry_tracker import ExpiryTracker
from src.recipe_generator import RecipeGenerator

# Initialize components
db = FridgeDatabase()
detector = FoodDetector()
tracker = ExpiryTracker(db)
recipe_gen = RecipeGenerator()

# Scan fridge
items = detector.process_fridge_scan('path/to/image.jpg')

# Add items to database
for item in items:
    db.add_food_item(item)

# Check expiry and generate alerts
tracker.generate_alerts()

# Generate recipe
expiring_items = tracker.get_items_for_recipe()
ingredients = [item['name'] for item in expiring_items]
recipe = recipe_gen.generate_recipe(ingredients)
```

## 📸 Food Scanning

### Automatic Scanning
1. Position camera to capture fridge contents
2. Ensure good lighting
3. Food labels should be visible
4. Run scan through dashboard or CLI

### Manual Entry
1. Navigate to "Food Inventory" in dashboard
2. Click "Add New Item Manually"
3. Enter food details
4. Set expiry date
5. Save item

### Best Practices
- ✅ Label all food items clearly
- ✅ Keep items organized by category
- ✅ Ensure labels face the camera
- ✅ Use consistent lighting
- ✅ Scan after grocery shopping

## ⚙️ Configuration

Edit `src/config.py` to customize:

```python
# Alert thresholds (in days)
ALERT_THRESHOLDS = {
    'critical': 1,
    'warning': 3,
    'normal': 7
}

# Auto-scan settings
AUTO_SCAN_ENABLED = True
SCAN_INTERVAL_HOURS = 12

# Notification channels
ENABLE_DESKTOP_NOTIFICATIONS = True
ENABLE_EMAIL_NOTIFICATIONS = False
ENABLE_SMS_NOTIFICATIONS = False

# Default shelf life by category (days)
DEFAULT_SHELF_LIFE = {
    'Vegetables': 7,
    'Fruits': 5,
    'Dairy': 7,
    'Meat': 3,
    'Seafood': 2,
    # ... more categories
}
```

## 🗄️ Database Schema

### Food Items Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| name | TEXT | Food item name |
| category | TEXT | Food category |
| quantity | INTEGER | Item quantity |
| expiry_date | DATE | Expiration date |
| status | TEXT | fresh/expiring/expired |
| storage_date | TIMESTAMP | When item was added |

### Alerts Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| food_item_id | INTEGER | Foreign key to food_items |
| alert_level | TEXT | critical/warning/normal |
| message | TEXT | Alert message |
| is_read | BOOLEAN | Read status |

## 🔧 Troubleshooting

### Camera Issues
```bash
# List available cameras
python -c "import cv2; print([i for i in range(10) if cv2.VideoCapture(i).isOpened()])"

# Update camera ID in config.py
CAMERA_ID = 0  # Change to your camera index
```

### OCR Not Working
```bash
# Verify Tesseract installation
tesseract --version

# Install EasyOCR models
python -c "import easyocr; reader = easyocr.Reader(['en'])"
```

### Model Not Found
```bash
# Download YOLOv8 base model
from ultralytics import YOLO
model = YOLO('yolov8n.pt')  # Downloads if not present
```

## 🧪 Testing

```bash
# Run tests
pytest tests/

# With coverage
pytest --cov=src tests/
```

## 📊 Analytics & Reporting

The system provides:
- **Waste Statistics**: Track expired items and waste rate
- **Consumption Patterns**: Most consumed categories
- **Timeline Analysis**: Expiry trends over time
- **Category Distribution**: Item counts by category

## 🤖 AI Recipe Generation

### With OpenAI API
```python
# Set API key in .env file
OPENAI_API_KEY=sk-...

# Generate recipe
recipe = recipe_gen.generate_recipe(
    ingredients=['chicken', 'broccoli', 'rice'],
    cuisine_type='Asian',
    dietary_restrictions=['gluten-free']
)
```

### Without API (Fallback)
The system includes rule-based recipe templates that work without external APIs.

## 📱 Notifications

### Desktop Notifications
- Enabled by default
- Uses system notification center
- Critical alerts appear immediately

### Email Notifications
1. Enable in config.py
2. Set SMTP credentials in .env
3. Use app-specific password for Gmail

### SMS Notifications
1. Create Twilio account
2. Add credentials to .env
3. Enable in config.py

## 🔐 Security & Privacy

- All data stored locally in SQLite database
- No data sent to external servers (except for recipe API if enabled)
- Camera access only when scanning
- Credentials stored in .env file (gitignored)

## 🛣️ Roadmap

- [ ] Mobile app (iOS/Android)
- [ ] Multi-user support
- [ ] Cloud synchronization
- [ ] Grocery list integration
- [ ] Nutritional information
- [ ] Shopping recommendations
- [ ] Voice commands
- [ ] Smart speaker integration

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- YOLOv8 by Ultralytics
- EasyOCR
- Streamlit
- OpenAI
- Python community

## 📞 Support

For issues and questions:
- GitHub Issues: https://github.com/yourusername/smart-fridge-ai/issues
- Email: support@smartfridgeai.com

## 📚 Documentation

- [System Workflow](docs/WORKFLOW.md)
- [API Documentation](docs/API.md)
- [User Guide](docs/USER_GUIDE.md)

---

**Made with ❤️ for reducing food waste and promoting sustainability**
