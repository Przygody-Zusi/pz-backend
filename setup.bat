@echo off
setlocal enabledelayedexpansion

REM Check for Python installation
where python >nul 2>nul
if errorlevel 1 (
    echo Python is not installed. Please install it from https://www.python.org/downloads/
    exit /b 1
)

REM Create virtual environment
python -m venv .venv
if errorlevel 1 (
    echo Failed to create virtual environment.
    exit /b 1
)

REM Activate virtual environment
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo Failed to activate virtual environment.
    exit /b 1
)

REM Upgrade pip
python -m pip install --upgrade pip
if errorlevel 1 (
    echo Failed to upgrade pip.
    exit /b 1
)

REM Check for requirements.txt
if not exist requirements.txt (
    echo "requirements.txt" does not exist!
    exit /b 1
)

REM Install dependencies
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies.
    exit /b 1
)

REM Install pre-commit
pip install pre-commit
if errorlevel 1 (
    echo Failed to install pre-commit.
    exit /b 1
)

REM Register git hooks
pre-commit install
if errorlevel 1 (
    echo Failed to register git hooks.
    exit /b 1
)

echo Done
