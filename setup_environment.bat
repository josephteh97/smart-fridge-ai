@echo off
REM Smart Fridge AI - Windows Environment Setup Script

echo ==========================================
echo Smart Fridge AI - Environment Setup
echo ==========================================
echo.

REM Check if conda is installed
where conda >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: Conda is not installed!
    echo Please install Anaconda or Miniconda first:
    echo https://docs.conda.io/en/latest/miniconda.html
    pause
    exit /b 1
)

conda --version
echo.

REM Environment name
set ENV_NAME=smart_fridge

REM Check if environment already exists
conda env list | find "%ENV_NAME%" >nul
if %errorlevel% equ 0 (
    echo Warning: Environment '%ENV_NAME%' already exists.
    set /p RECREATE="Do you want to remove and recreate it? (y/n): "
    if /i "%RECREATE%"=="y" (
        echo Removing existing environment...
        conda env remove -n %ENV_NAME% -y
    ) else (
        echo Setup cancelled.
        pause
        exit /b 0
    )
)

echo Creating Anaconda environment: %ENV_NAME%
echo ----------------------------------------
echo.

REM Create conda environment with Python 3.9
conda create -n %ENV_NAME% python=3.9 -y

if %errorlevel% neq 0 (
    echo Error: Failed to create environment
    pause
    exit /b 1
)

echo.
echo Environment created successfully!
echo.

REM Activate environment
echo Activating environment...
call conda activate %ENV_NAME%

if %errorlevel% neq 0 (
    echo Error: Failed to activate environment
    pause
    exit /b 1
)

echo Environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install packages from requirements.txt
echo.
echo Installing Python packages...
echo ----------------------------------------
echo.

if exist requirements.txt (
    pip install -r requirements.txt
    
    if %errorlevel% neq 0 (
        echo Error: Failed to install some packages
        echo Please check the error messages above
        pause
        exit /b 1
    )
) else (
    echo Error: requirements.txt not found!
    pause
    exit /b 1
)

echo.
echo All Python packages installed successfully!
echo.

REM System dependencies
echo Installing system dependencies...
echo ----------------------------------------
echo.
echo Please install Tesseract OCR manually:
echo Download from: https://github.com/UB-Mannheim/tesseract/wiki
echo.

REM Create necessary directories
echo Creating project directories...
echo ----------------------------------------

if not exist data\scans mkdir data\scans
if not exist data\recipes mkdir data\recipes
if not exist models mkdir models
if not exist logs mkdir logs
if not exist static mkdir static
if not exist templates mkdir templates

echo Directories created
echo.

REM Download EasyOCR models
echo Downloading EasyOCR models...
echo ----------------------------------------
python -c "import easyocr; reader = easyocr.Reader(['en'], download_enabled=True); print('EasyOCR models downloaded')"
echo.

REM Create .env template
if not exist .env (
    echo Creating .env template...
    (
        echo # OpenAI API (for advanced recipe generation^)
        echo OPENAI_API_KEY=
        echo.
        echo # Email Configuration (optional^)
        echo SENDER_EMAIL=
        echo SENDER_PASSWORD=
        echo.
        echo # Twilio SMS Configuration (optional^)
        echo TWILIO_ACCOUNT_SID=
        echo TWILIO_AUTH_TOKEN=
        echo TWILIO_PHONE_NUMBER=
    ) > .env
    echo .env template created
) else (
    echo .env file already exists
)

echo.

REM Initialize database
echo Initializing database...
python -c "from src.database import FridgeDatabase; db = FridgeDatabase(); print('Database initialized')"

echo.

REM Display summary
echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo Environment: %ENV_NAME%
echo.
echo To activate the environment, run:
echo   conda activate %ENV_NAME%
echo.
echo To start the application:
echo   1. Command Line: python main.py
echo   2. Web Dashboard: streamlit run dashboard.py
echo.
echo Configuration:
echo   - Edit src\config.py for system settings
echo   - Edit .env for API keys and credentials
echo.
echo Next steps:
echo   1. Install Tesseract OCR from the link above
echo   2. Configure your camera ID in src\config.py
echo   3. (Optional) Add OpenAI API key to .env for AI recipes
echo   4. (Optional) Configure email/SMS in .env for notifications
echo   5. Run 'python main.py' to start!
echo.
echo For documentation, see README.md
echo ==========================================
echo.

pause
