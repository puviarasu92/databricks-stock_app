# Project Structure Guide

## Overview

The project is now organized into clear, logical folders that separate concerns and make it easier to maintain and develop.

## Folder Breakdown

### 📁 `src/` - Source Code
Contains all the main application code.

```
src/
├── __init__.py          # Python package marker
├── app.py               # Main Streamlit app (interactive, manual credentials)
├── app_env.py           # Alternative app (uses environment variables)
└── config.py            # Configuration and environment variable handling
```

**When to use:**
- `app.py` - For local development with manual credential input via the UI
- `app_env.py` - For production/automated deployments (reads from .env)

### 📁 `scripts/` - Deployment & Utility Scripts
Automation scripts for deployment, testing, and diagnostics.

```
scripts/
├── deploy_to_databricks.py    # Deploy app to Databricks workspace
├── verify_deployment.py        # Verify files were uploaded correctly
├── run_local.py               # Local Streamlit runner
├── ssl_test_connection.py     # Test Databricks connection (SSL modes)
├── ssl_diagnostic.py          # Diagnose SSL/certificate issues
├── check-all.sh               # Pre-commit validation (Linux/Mac)
└── check-all.bat              # Pre-commit validation (Windows)
```

**Usage examples:**
```bash
# Run locally
python scripts/run_local.py

# Deploy to Databricks
python scripts/deploy_to_databricks.py --host ... --token ... --workspace-path ...

# Test SSL connection
python scripts/ssl_test_connection.py

# Check code quality
bash scripts/check-all.sh  # or check-all.bat on Windows
```

### 📁 `tests/` - Test Suite
All unit and integration tests.

```
tests/
├── __init__.py          # Python package marker
├── conftest.py          # pytest configuration and fixtures
├── test_app.py          # Application unit tests
├── test_integration.py  # Databricks connection tests
└── test_connection.py   # Connection testing
```

**Run tests:**
```bash
pytest                    # Run all tests
pytest -m unit           # Run unit tests only
pytest -m integration    # Run integration tests only
pytest --cov src         # Run with coverage report
```

### 📁 `docs/` - Documentation
Complete project documentation.

```
docs/
├── readme.md                              # Full project documentation
├── QUICKSTART.md                          # 5-minute quick start
├── CI-CD-DEPLOYMENT.md                    # CI/CD pipeline guide
├── CI-CD-SETUP.md                         # CI/CD setup instructions
├── DEPLOYMENT-ARCHITECTURE.md             # Architecture & deployment
├── GITHUB-ACTIONS-SETUP.md                # GitHub Actions setup
├── SETUP-CHECKLIST.md                     # Setup checklist
├── SETUP-COMPLETE.md                      # Complete setup guide
├── SSL-CERTIFICATE-RESOLUTION.md          # SSL solutions (all 6)
├── SSL-CERTIFICATE-TROUBLESHOOTING.md     # Detailed SSL guide
├── SSL-FIXES-SUMMARY.md                   # SSL fixes overview
├── SSL-QUICK-FIX.md                       # Quick SSL solutions
├── YOUR-SSL-ERROR-SOLUTION.md             # Your specific error
└── SSL-VISUAL-GUIDE.md                    # Visual step-by-step guide
```

### 📁 `config/` - Configuration Templates
Example configuration files (don't modify these - copy them for local use).

```
config/
├── .env.example           # Environment variables template
└── .databrickscfg.example # Databricks CLI config template
```

**Setup:**
```bash
# Copy template for local use
cp config/.env.example .env
# Edit .env with your Databricks credentials
```

### 📁 `.github/` - GitHub Automation
GitHub Actions CI/CD workflows.

```
.github/
└── workflows/
    ├── lint-and-test.yml        # Code quality & testing (on every push)
    ├── deploy-databricks.yml    # Deploy to Databricks (main branch)
    └── security-scan.yml        # Security scanning (daily + on push)
```

### 📁 `.streamlit/` - Streamlit Configuration
Streamlit app configuration and theming.

```
.streamlit/
└── config.toml  # Streamlit UI settings (theme, fonts, etc.)
```

### 📁 Root Files

```
databricks-stock_app/
├── README.md                # Quick overview (points to docs/)
├── requirements.txt         # Python dependencies
├── pytest.ini              # pytest configuration
├── pyproject.toml          # Project metadata & build config
├── .gitignore              # Git ignore rules
├── .git/                   # Git repository
└── .github/                # GitHub configuration
```

## File Location Reference

### Where do I...?

**Run the app locally?**
```bash
streamlit run src/app.py
# or
python scripts/run_local.py
```

**Edit app code?**
- `src/app.py` - main app
- `src/config.py` - configuration logic

**Write tests?**
- `tests/test_app.py` - add new test functions

**Add documentation?**
- `docs/` - add markdown files

**Configure environment variables?**
- Copy `config/.env.example` → `.env` in root
- Edit `.env` with your Databricks credentials

**Deploy to Databricks?**
```bash
python scripts/deploy_to_databricks.py \
  --host your-workspace.cloud.databricks.com \
  --token your_token \
  --workspace-path /your/path
```

**Check code quality?**
```bash
python scripts/check-all.sh  # or .bat on Windows
```

## Import Guidelines

### In Tests
```python
# Import from src
from src.config import DEFAULT_MAX_ROWS
from src.app import some_function  # if exported
```

### In App Code
```python
# App can import from relative paths
import config
from config import DEFAULT_MAX_ROWS
```

### From Scripts
```python
# Scripts should use absolute imports from src
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from config import DEFAULT_MAX_ROWS
```

## Development Workflow

1. **Clone & Setup**
   ```bash
   git clone <repo>
   cd databricks-stock_app
   pip install -r requirements.txt
   cp config/.env.example .env
   ```

2. **Configure**
   - Edit `.env` with your Databricks credentials

3. **Develop**
   ```bash
   streamlit run src/app.py
   ```

4. **Test**
   ```bash
   pytest
   bash scripts/check-all.sh
   ```

5. **Deploy**
   ```bash
   python scripts/deploy_to_databricks.py \
     --host ... --token ... --workspace-path ...
   ```

## CI/CD Pipeline

The project includes automated GitHub Actions workflows:

- **lint-and-test.yml** - Runs on every push to main/develop
  - Code quality checks (flake8, black, isort, pylint)
  - Unit tests with coverage
  - Python 3.8-3.11 compatibility

- **deploy-databricks.yml** - Runs on main branch push
  - Deploys to Databricks workspace
  - Sends Slack notifications (optional)
  - Requires: DATABRICKS_HOST, DATABRICKS_TOKEN, DATABRICKS_WORKSPACE_PATH

- **security-scan.yml** - Runs daily + on every push
  - Vulnerability scanning (bandit, safety, pip-audit)
  - Identifies security issues

See [`docs/CI-CD-DEPLOYMENT.md`](../docs/CI-CD-DEPLOYMENT.md) for complete setup.

## Key Features of This Structure

✅ **Clear Separation of Concerns**
- Source code separate from tests and scripts
- Documentation in its own folder

✅ **Easy Maintenance**
- Quick to find files
- Related code grouped together

✅ **Professional Layout**
- Follows Python best practices
- Similar to popular projects (Flask, Django, etc.)

✅ **CI/CD Ready**
- Scripts can be easily integrated with automation
- Standard folder names recognized by tools

✅ **Scalable**
- Easy to add new modules to `src/`
- Room to grow without reorganization

## Questions?

- **Quick start?** See [`docs/QUICKSTART.md`](../docs/QUICKSTART.md)
- **SSL errors?** See [`docs/SSL-QUICK-FIX.md`](../docs/SSL-QUICK-FIX.md)
- **Full docs?** See [`docs/readme.md`](../docs/readme.md)
- **Deployment?** See [`docs/CI-CD-DEPLOYMENT.md`](../docs/CI-CD-DEPLOYMENT.md)
