#!/bin/bash

# Smart Fridge AI - Anaconda Environment Setup Script
# This script creates and configures the Anaconda environment

echo "=========================================="
echo "Smart Fridge AI - Environment Setup"
echo "=========================================="
echo ""

# Check if conda is installed
if ! command -v conda &> /dev/null
then
    echo "❌ Conda is not installed!"
    echo "Please install Anaconda or Miniconda first:"
    echo "https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

echo "✅ Conda found: $(conda --version)"
echo ""

# Environment name
ENV_NAME="smart_fridge"

# Check if environment already exists
if conda env list | grep -q "^$ENV_NAME "; then
    echo "⚠️  Environment '$ENV_NAME' already exists."
    read -p "Do you want to remove and recreate it? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Removing existing environment..."
        conda env remove -n $ENV_NAME -y
    else
        echo "Setup cancelled."
        exit 0
    fi
fi

echo "Creating Anaconda environment: $ENV_NAME"
echo "----------------------------------------"

# Create conda environment with Python 3.9
conda create -n $ENV_NAME python=3.9 -y

if [ $? -ne 0 ]; then
    echo "❌ Failed to create environment"
    exit 1
fi

echo ""
echo "✅ Environment created successfully!"
echo ""

# Activate environment
echo "Activating environment..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate $ENV_NAME

if [ $? -ne 0 ]; then
    echo "❌ Failed to activate environment"
    exit 1
fi

echo "✅ Environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install packages from requirements.txt
echo ""
echo "Installing Python packages..."
echo "----------------------------------------"

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install some packages"
        echo "Please check the error messages above"
        exit 1
    fi
else
    echo "❌ requirements.txt not found!"
    exit 1
fi

echo ""
echo "✅ All Python packages installed successfully!"
echo ""

# Install system dependencies (OS-specific)
echo "Installing system dependencies..."
echo "----------------------------------------"

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Detected Linux system"
    echo "Installing Tesseract OCR..."
    
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y tesseract-ocr libtesseract-dev
    elif command -v yum &> /dev/null; then
        sudo yum install -y tesseract tesseract-devel
    else
        echo "⚠️  Please install Tesseract OCR manually"
    fi
    
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detected macOS system"
    
    if command -v brew &> /dev/null; then
        echo "Installing Tesseract OCR via Homebrew..."
        brew install tesseract
    else
        echo "⚠️  Homebrew not found. Please install Tesseract manually:"
        echo "   brew install tesseract"
    fi
    
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    echo "Detected Windows system"
    echo "⚠️  Please install Tesseract OCR manually:"
    echo "   Download from: https://github.com/UB-Mannheim/tesseract/wiki"
else
    echo "⚠️  Unknown OS. Please install Tesseract OCR manually"
fi

echo ""

# Verify Tesseract installation
if command -v tesseract &> /dev/null; then
    echo "✅ Tesseract OCR installed: $(tesseract --version | head -n 1)"
else
    echo "⚠️  Tesseract OCR not found in PATH"
fi

echo ""

# Create necessary directories
echo "Creating project directories..."
echo "----------------------------------------"

mkdir -p data/scans
mkdir -p data/recipes
mkdir -p models
mkdir -p logs
mkdir -p static
mkdir -p templates

echo "✅ Directories created"
echo ""

# Download EasyOCR models
echo "Downloading EasyOCR models..."
echo "----------------------------------------"

python -c "import easyocr; reader = easyocr.Reader(['en'], download_enabled=True); print('✅ EasyOCR models downloaded')"

echo ""

# Create .env template
if [ ! -f ".env" ]; then
    echo "Creating .env template..."
    cat > .env << 'EOF'
# OpenAI API (for advanced recipe generation)
OPENAI_API_KEY=

# Email Configuration (optional)
SENDER_EMAIL=
SENDER_PASSWORD=

# Twilio SMS Configuration (optional)
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=
EOF
    echo "✅ .env template created"
else
    echo "✅ .env file already exists"
fi

echo ""

# Initialize database
echo "Initializing database..."
python -c "from src.database import FridgeDatabase; db = FridgeDatabase(); print('✅ Database initialized')"

echo ""

# Display summary
echo "=========================================="
echo "Setup Complete! 🎉"
echo "=========================================="
echo ""
echo "Environment: $ENV_NAME"
echo ""
echo "To activate the environment, run:"
echo "  conda activate $ENV_NAME"
echo ""
echo "To start the application:"
echo "  1. Command Line: python main.py"
echo "  2. Web Dashboard: streamlit run dashboard.py"
echo ""
echo "Configuration:"
echo "  - Edit src/config.py for system settings"
echo "  - Edit .env for API keys and credentials"
echo ""
echo "Next steps:"
echo "  1. Configure your camera ID in src/config.py"
echo "  2. (Optional) Add OpenAI API key to .env for AI recipes"
echo "  3. (Optional) Configure email/SMS in .env for notifications"
echo "  4. Run 'python main.py' to start!"
echo ""
echo "For documentation, see README.md"
echo "=========================================="
