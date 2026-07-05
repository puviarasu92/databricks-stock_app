@echo off
REM Local pre-commit checks for Windows
REM Run this before pushing to verify all checks will pass in GitHub Actions

setlocal enabledelayedexpansion

echo ================================
echo Local Pre-commit Checks
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python is not installed
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYVER=%%i
echo + Python version: %PYVER%

REM Install dev dependencies
echo.
echo Installing dependencies...
pip install -q -r requirements.txt 2>nul
if errorlevel 1 (
    pip install -r requirements.txt
)

REM Flake8 linting
echo.
echo Running flake8 linting...
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
if errorlevel 1 (
    echo X flake8 failed
    exit /b 1
)
echo + flake8 passed

REM Black formatting check
echo.
echo Checking black formatting...
black --check . --quiet 2>nul
if errorlevel 1 (
    echo - black formatting issues found
    echo   Run: black . ^&^& isort .
    set /p "choice=Auto-fix? (y/n): "
    if /i "!choice!"=="y" (
        black . --quiet
        isort . --quiet
        echo + Code formatted
    ) else (
        exit /b 1
    )
) else (
    echo + black formatting passed
)

REM isort import sorting
echo.
echo Checking import sorting with isort...
isort --check-only . --quiet 2>nul
if errorlevel 1 (
    echo - isort issues found
    echo   Run: isort .
    set /p "choice=Auto-fix? (y/n): "
    if /i "!choice!"=="y" (
        isort . --quiet
        echo + Imports sorted
    ) else (
        exit /b 1
    )
) else (
    echo + isort passed
)

REM Pylint
echo.
echo Running pylint...
pylint app.py app_env.py config.py --disable=C0111,W0612,C0103,C0301 --exit-zero 2>nul
echo + pylint completed

REM Tests
echo.
echo Running pytest...
pytest tests/ -v --tb=short 2>nul
if errorlevel 1 (
    echo - Some tests may have failed
)

echo.
echo ================================
echo + All checks completed!
echo ================================
echo.
echo Ready to push?
echo   git push origin ^<branch^>
echo.
