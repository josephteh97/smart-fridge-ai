# 🚀 Quick Start Guide - Smart Fridge AI

Get up and running with Smart Fridge AI in 5 minutes!

## Prerequisites Checklist

- [ ] Python 3.8+ installed
- [ ] Anaconda or Miniconda installed
- [ ] Camera available (USB or built-in)
- [ ] (Optional) OpenAI API key for advanced recipe generation

## Installation Steps

### Step 1: Get the Code
```bash
# Clone or download the repository
cd smart-fridge-ai
```

### Step 2: Run Setup Script

**Linux/macOS:**
```bash
chmod +x setup_environment.sh
./setup_environment.sh
```

**Windows:**
```bash
setup_environment.bat
```

This will:
- ✅ Create conda environment
- ✅ Install all dependencies
- ✅ Download AI models
- ✅ Create database
- ✅ Set up directories

### Step 3: Activate Environment
```bash
conda activate smart_fridge
```

## First Run

### Option 1: Command Line (Recommended for First-Time)

```bash
python main.py
```

**Try these options:**
1. Press `1` → Test camera scan (uses webcam)
2. Press `4` → View system status
3. Press `6` → Launch dashboard

### Option 2: Web Dashboard

```bash
streamlit run dashboard.py
```

Then open browser to: http://localhost:8501

## Adding Your First Food Items

### Method 1: Manual Entry (Easiest)

1. Open dashboard: `streamlit run dashboard.py`
2. Go to **"Food Inventory"** page
3. Click **"➕ Add New Item Manually"**
4. Fill in:
   - Food Name: e.g., "Milk"
   - Category: "Dairy"
   - Quantity: 1
   - Expiry Date: Set a date
5. Click **"Add Item"**

### Method 2: Camera Scan

1. Position items in front of camera
2. In dashboard, go to **"Scan Items"**
3. Upload an image or capture from camera
4. Click **"🔍 Scan and Detect Items"**
5. Review detected items and add them

### Method 3: Programmatically

```python
from src.database import FridgeDatabase
from datetime import datetime, timedelta

db = FridgeDatabase()

# Add a food item
item = {
    'name': 'Milk',
    'category': 'Dairy',
    'quantity': 1,
    'unit': 'L',
    'expiry_date': (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d'),
    'location': 'main_compartment'
}

db.add_food_item(item)
print("Item added successfully!")
```

## Testing the Alert System

1. Add an item with expiry date tomorrow
2. Run: `python main.py`
3. Choose option `2` (Check Alerts)
4. You should see a critical alert!

Or in dashboard:
1. Go to **"Alerts"** page
2. Click **"🔄 Refresh Alerts"**
3. View your alerts

## Generating Your First Recipe

### In Dashboard:
1. Add some items that expire soon
2. Go to **"Recipes"** page
3. Select cuisine type and dietary restrictions
4. Click **"🎲 Generate Recipe"**

### In CLI:
```bash
python main.py
# Choose option 3: Generate Recipe
```

### Programmatically:
```python
from src.recipe_generator import RecipeGenerator

recipe_gen = RecipeGenerator()

recipe = recipe_gen.generate_recipe(
    ingredients=['chicken', 'tomatoes', 'rice'],
    cuisine_type='Italian'
)

print(recipe_gen.format_recipe_for_display(recipe))
```

## Configuration

### Configure Camera
Edit `src/config.py`:
```python
CAMERA_ID = 0  # Change if you have multiple cameras
```

### Set Alert Thresholds
Edit `src/config.py`:
```python
ALERT_THRESHOLDS = {
    'critical': 1,   # Alert when 1 day left
    'warning': 3,    # Alert when 3 days left
    'normal': 7      # Alert when 7 days left
}
```

### Enable Notifications
Edit `src/config.py`:
```python
ENABLE_DESKTOP_NOTIFICATIONS = True   # Desktop alerts
ENABLE_EMAIL_NOTIFICATIONS = False    # Email alerts (needs .env setup)
ENABLE_SMS_NOTIFICATIONS = False      # SMS alerts (needs Twilio)
```

### Add OpenAI Key for Better Recipes
Edit `.env`:
```
OPENAI_API_KEY=sk-your-api-key-here
```

## Dashboard Pages Overview

### 📊 Dashboard
- System overview
- Total items count
- Critical alerts
- Category distribution pie chart
- Expiry timeline

### 📦 Food Inventory
- View all items
- Filter by category
- Add new items manually
- Delete items
- See days until expiry

### 📷 Scan Items
- Upload images
- Automatic food detection
- Add detected items to inventory

### 🔔 Alerts
- View all alerts by priority
- Critical (red), Warning (orange), Normal (blue)
- Mark alerts as read
- Refresh alerts

### 🍳 Recipes
- See expiring ingredients
- Generate AI recipes
- Save recipes
- View recipe details

### 📈 Statistics
- Waste statistics
- Items by category
- Consumption patterns
- Recommendations

## Common Tasks

### Check What's Expiring Soon
```bash
# In CLI
python -c "from src.database import FridgeDatabase; from src.expiry_tracker import ExpiryTracker; db = FridgeDatabase(); tracker = ExpiryTracker(db); items = tracker.get_items_for_recipe(); print(f'Expiring soon: {[item[\"name\"] for item in items]}')"
```

### View All Items
```bash
# In CLI
python -c "from src.database import FridgeDatabase; import pandas as pd; db = FridgeDatabase(); print(db.get_all_items())"
```

### Manual Scan
```bash
# Take photo of fridge
# Then run:
python -c "from src.food_detector import FoodDetector; detector = FoodDetector(); items = detector.process_fridge_scan('path/to/photo.jpg'); print(items)"
```

## Troubleshooting

### Camera Not Working
```python
# Test camera
import cv2
cap = cv2.VideoCapture(0)  # Try 0, 1, 2...
print("Camera opened:", cap.isOpened())
```

### Database Issues
```bash
# Reset database
rm data/smart_fridge.db
python -c "from src.database import FridgeDatabase; FridgeDatabase()"
```

### Missing Dependencies
```bash
# Reinstall
pip install -r requirements.txt --force-reinstall
```

### Tesseract Not Found
- Linux: `sudo apt-get install tesseract-ocr`
- macOS: `brew install tesseract`
- Windows: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

## Next Steps

1. ✅ Add your actual fridge items
2. ✅ Set up scheduled scans (option 5 in main menu)
3. ✅ Configure notifications
4. ✅ Try recipe generation
5. ✅ Check analytics after a week

## Tips for Best Results

### Food Scanning:
- 📸 Good lighting is essential
- 🏷️ Keep labels facing camera
- 📏 Items should be clearly visible
- 🧹 Remove clutter for better detection

### Inventory Management:
- 📅 Update expiry dates when you open packages
- 🗑️ Mark items as consumed when used
- 📊 Review analytics weekly
- 🔄 Scan after grocery shopping

### Reduce Waste:
- ⏰ Check alerts daily
- 🍳 Generate recipes for expiring items
- 📱 Enable notifications
- 📈 Review waste statistics

## Getting Help

- 📖 Read full documentation: [README.md](README.md)
- 🔍 Check workflow: [docs/WORKFLOW.md](docs/WORKFLOW.md)
- 🐛 Report issues: GitHub Issues
- 💬 Questions: Check documentation first

## Demo Data

Want to test without real items? Add demo data:

```python
from src.database import FridgeDatabase
from datetime import datetime, timedelta

db = FridgeDatabase()

demo_items = [
    {'name': 'Milk', 'category': 'Dairy', 'expiry_date': (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')},
    {'name': 'Eggs', 'category': 'Dairy', 'expiry_date': (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d')},
    {'name': 'Chicken', 'category': 'Meat', 'expiry_date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')},
    {'name': 'Broccoli', 'category': 'Vegetables', 'expiry_date': (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')},
]

for item in demo_items:
    item['quantity'] = 1
    item['unit'] = 'piece'
    db.add_food_item(item)

print("Demo data added!")
```

## Success Indicators

After setup, you should be able to:
- ✅ See items in dashboard
- ✅ Receive alerts for expiring items
- ✅ Generate recipes
- ✅ View statistics
- ✅ Scan and add new items

---

**You're all set! Enjoy reducing food waste with Smart Fridge AI! 🎉**
