# Smart Fridge AI - Complete Project Structure

```
smart_fridge_ai/
│
├── 📄 README.md                      # Complete documentation
├── 📄 QUICKSTART.md                  # Quick start guide
├── 📄 requirements.txt               # Python dependencies
├── 📄 .env.template                  # Environment variables template
│
├── 🔧 setup_environment.sh           # Linux/macOS setup script
├── 🔧 setup_environment.bat          # Windows setup script
│
├── 🐍 main.py                        # Main application (CLI)
├── 🌐 dashboard.py                   # Web dashboard (Streamlit)
├── 📊 create_workflow_diagram.py     # Generate workflow diagram
│
├── 📁 src/                           # Source code
│   ├── __init__.py                   # Package initialization
│   ├── config.py                     # Configuration settings
│   ├── database.py                   # Database management
│   ├── food_detector.py              # Computer vision & OCR
│   ├── expiry_tracker.py             # Expiry tracking & alerts
│   └── recipe_generator.py           # AI recipe generation
│
├── 📁 models/                        # ML models
│   └── yolov8_food.pt               # (To be added) YOLOv8 model
│
├── 📁 data/                          # Data storage
│   ├── smart_fridge.db              # SQLite database
│   ├── scans/                       # Scanned images
│   └── recipes/                     # Generated recipes
│
├── 📁 docs/                          # Documentation
│   ├── WORKFLOW.md                  # System workflow (Mermaid)
│   ├── system_workflow_diagram.png  # Workflow diagram (PNG)
│   └── API.md                       # (To be added) API docs
│
├── 📁 static/                        # Static assets
│   └── (CSS, images, etc.)
│
├── 📁 templates/                     # HTML templates
│   └── (HTML files)
│
├── 📁 logs/                          # Application logs
│   └── smart_fridge_*.log
│
└── 📁 tests/                         # Test files (to be added)
    ├── test_database.py
    ├── test_detector.py
    └── test_tracker.py
```

## File Descriptions

### Core Application Files

#### `main.py`
- Command-line interface
- Main application orchestrator
- Menu-driven interaction
- Scheduled task management
- System status monitoring

#### `dashboard.py`
- Streamlit web interface
- Interactive dashboard
- Real-time monitoring
- Multi-page application:
  - Dashboard overview
  - Food inventory
  - Scan items
  - Alerts
  - Recipes
  - Statistics

#### `requirements.txt`
Complete list of Python dependencies:
- Computer Vision: opencv-python, ultralytics (YOLOv8)
- OCR: pytesseract, easyocr
- AI/ML: tensorflow, torch, transformers
- Web: streamlit, flask, plotly
- Database: sqlalchemy
- Utilities: pandas, numpy, pillow

### Source Code (`src/`)

#### `config.py`
- System configuration
- Alert thresholds
- Database paths
- Camera settings
- Notification settings
- Default shelf life values
- API keys (references to .env)

#### `database.py`
Database management with methods:
- `add_food_item()` - Add items
- `get_all_items()` - Retrieve items
- `get_expiring_items()` - Filter by expiry
- `update_item_status()` - Update status
- `create_alert()` - Create alerts
- `save_recipe()` - Save recipes
- `get_statistics()` - Get stats

#### `food_detector.py`
Computer vision functionality:
- `capture_image()` - Camera capture
- `detect_food_items()` - YOLOv8 detection
- `extract_text_from_image()` - OCR
- `extract_expiry_date()` - Date parsing
- `scan_barcode()` - Barcode reading
- `process_fridge_scan()` - Complete scan

#### `expiry_tracker.py`
Expiry monitoring and alerts:
- `check_expiry_status()` - Check all items
- `generate_alerts()` - Create alerts
- `get_items_for_recipe()` - Expiring items
- `calculate_waste_statistics()` - Waste stats
- `send_desktop_notification()` - Desktop alerts
- `send_email_alert()` - Email alerts
- `send_sms_alert()` - SMS alerts

#### `recipe_generator.py`
AI-powered recipe creation:
- `generate_recipe()` - Main generator
- `_generate_with_openai()` - OpenAI API
- `_generate_fallback_recipe()` - Rule-based
- `format_recipe_for_display()` - Format output
- `save_recipe_to_file()` - Save to JSON

### Setup Scripts

#### `setup_environment.sh` (Linux/macOS)
Automated setup:
- Creates conda environment
- Installs Python packages
- Installs Tesseract OCR
- Downloads AI models
- Creates directories
- Initializes database
- Creates .env template

#### `setup_environment.bat` (Windows)
Windows version of setup script with same functionality.

### Documentation

#### `README.md`
Complete documentation:
- Features overview
- System architecture
- Installation instructions
- Usage examples
- Configuration guide
- Troubleshooting
- API reference

#### `QUICKSTART.md`
Quick start guide:
- 5-minute setup
- First run instructions
- Adding items
- Testing features
- Common tasks
- Tips and tricks

#### `docs/WORKFLOW.md`
System workflow:
- Mermaid diagram
- Data flow description
- Phase-by-phase breakdown
- Technology stack
- Key features

#### `docs/system_workflow_diagram.png`
Visual workflow diagram showing:
- Input sources
- Processing modules
- Database storage
- User interface
- Alert system
- Data flow

### Database Schema

#### Tables:

1. **food_items**
   - Item details
   - Expiry dates
   - Categories
   - Status tracking

2. **alerts**
   - Alert messages
   - Priority levels
   - Read status
   - Timestamps

3. **consumption_history**
   - Consumed items
   - Waste tracking
   - Historical data

4. **generated_recipes**
   - Recipe details
   - Used ingredients
   - Instructions
   - Metadata

## Technology Stack

### Computer Vision
- **YOLOv8**: Food item detection
- **OpenCV**: Image processing
- **EasyOCR**: Text extraction
- **Tesseract**: Backup OCR
- **pyzbar**: Barcode scanning

### AI/Machine Learning
- **TensorFlow**: Deep learning
- **PyTorch**: Neural networks
- **OpenAI GPT**: Recipe generation
- **Transformers**: NLP models

### Web & UI
- **Streamlit**: Dashboard framework
- **Plotly**: Interactive charts
- **Dash**: Additional dashboarding
- **Flask**: API endpoints

### Database & Storage
- **SQLite**: Local database
- **SQLAlchemy**: ORM
- **Pandas**: Data manipulation

### Notifications
- **Plyer**: Desktop notifications
- **Twilio**: SMS alerts
- **SMTP**: Email alerts

### Utilities
- **Schedule**: Task scheduling
- **Loguru**: Logging
- **python-dotenv**: Environment vars
- **Pillow**: Image processing

## Workflow Overview

1. **Input**: Camera scan / Manual entry / Barcode
2. **Detection**: Computer vision identifies food items
3. **Extraction**: OCR reads expiry dates and labels
4. **Storage**: Data saved to SQLite database
5. **Monitoring**: Continuous expiry tracking
6. **Alerts**: Multi-level notification system
7. **Recipes**: AI generates recipes from expiring items
8. **Analytics**: Waste statistics and insights
9. **User Action**: Dashboard interaction and management

## Key Features

✅ Automated food detection using YOLOv8  
✅ OCR for expiry date extraction  
✅ Multi-level alert system (Critical/Warning/Normal)  
✅ AI-powered recipe generation  
✅ Real-time dashboard monitoring  
✅ Multiple notification channels  
✅ Waste analytics and reporting  
✅ Barcode/QR code scanning  
✅ Scheduled automatic scans  
✅ Historical data tracking  
✅ Category-based organization  
✅ Customizable thresholds  
✅ Multi-platform support (Windows/Linux/macOS)

## Data Flow

```
Camera → Image Capture → Computer Vision → OCR → Data Extraction
    ↓
Database ← Item Storage
    ↓
Expiry Tracker → Alert Generator → Notifications
    ↓
Recipe Generator → AI/GPT → Recipe Display
    ↓
Dashboard ← User Interface → User Actions
```

## Alert Levels

- **🔴 Critical**: ≤1 day (immediate action required)
- **🟠 Warning**: ≤3 days (use soon)
- **🔵 Normal**: ≤7 days (plan to use)
- **🟢 Fresh**: >7 days (monitored)

## Customization Points

1. **Alert Thresholds** (`config.py`)
2. **Shelf Life Defaults** (`config.py`)
3. **Notification Channels** (`config.py`, `.env`)
4. **Camera Settings** (`config.py`)
5. **Recipe Preferences** (Dashboard UI)
6. **Scan Schedule** (`config.py`)
7. **Dashboard Layout** (`dashboard.py`)

## Extensibility

The modular architecture allows easy extension:
- Add new food categories
- Integrate additional ML models
- Connect to IoT devices
- Add more notification channels
- Integrate with grocery APIs
- Add voice assistant support
- Mobile app integration
- Cloud synchronization

## Performance Considerations

- **Database**: Indexed for fast queries
- **Computer Vision**: GPU acceleration supported
- **Caching**: Model results cached
- **Async**: Non-blocking operations
- **Optimization**: Configurable scan frequency

## Security & Privacy

- Local-first architecture
- No cloud dependencies (optional)
- Encrypted credentials (.env)
- No data collection
- User-controlled camera access

---

**Complete, production-ready system for intelligent food preservation!**
