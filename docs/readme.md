# Databricks Gold Table Viewer

[![Lint and Test](https://github.com/YOUR_USERNAME/databricks-stock_app/actions/workflows/lint-and-test.yml/badge.svg)](https://github.com/YOUR_USERNAME/databricks-stock_app/actions/workflows/lint-and-test.yml)
[![Deploy to Databricks](https://github.com/YOUR_USERNAME/databricks-stock_app/actions/workflows/deploy-databricks.yml/badge.svg)](https://github.com/YOUR_USERNAME/databricks-stock_app/actions/workflows/deploy-databricks.yml)
[![Security Scan](https://github.com/YOUR_USERNAME/databricks-stock_app/actions/workflows/security-scan.yml/badge.svg)](https://github.com/YOUR_USERNAME/databricks-stock_app/actions/workflows/security-scan.yml)

A Streamlit-based web application to display rows from a Databricks gold table in an interactive table format.

## Features

- ✨ Interactive web interface for viewing gold table data
- 📊 Display table data in an easy-to-read format
- 🔧 Configurable connection settings
- 📥 Download data as CSV
- 🎯 Row limit controls for performance
- 🔐 Secure PAT authentication
- 🚀 Automated CI/CD deployment to Databricks
- 🔍 Automated code quality & security scanning

## Prerequisites

- Python 3.8 or later
- Databricks workspace with SQL warehouse or compute cluster
- Databricks Personal Access Token (PAT)
- Table name in format: `catalog.schema.table_name`
- (Optional) GitHub repository for CI/CD automation

## Installation

1. Clone or navigate to this repository:
   ```bash
   cd databricks-stock_app
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the App

Start the Streamlit app:

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## Usage

1. **Enter Connection Details** (in the sidebar):
   - **Server Hostname**: Your Databricks workspace hostname (e.g., `example.cloud.databricks.com`)
   - **HTTP Path**: Your SQL Warehouse or cluster HTTP path (e.g., `/sql/1.0/warehouses/abc123def456`)
   - **Personal Access Token**: Your Databricks PAT token
   - **Table Name**: Full path to your gold table (e.g., `my_catalog.gold.sales_data`)

2. **Configure Options**:
   - **Max Rows to Display**: Set the maximum number of rows to fetch (default: 100)

3. **Load Data**:
   - Click the "Load Data" button
   - The app will fetch and display the data in a table format

4. **Download**:
   - Use the "Download as CSV" button to export the data

## Getting Your Databricks Connection Details

### Server Hostname
- In Databricks workspace, click your username → Account settings
- Copy your workspace URL (e.g., `https://example.cloud.databricks.com`)
- Use only the hostname part: `example.cloud.databricks.com`

### HTTP Path
- Navigate to SQL Warehouse or Compute cluster details
- Copy the HTTP path from the connection details section

### Personal Access Token
- In Databricks workspace, click your username → User settings → Developer → Personal access tokens
- Generate a new token and copy it
- **Keep this token secure!**

## Project Structure

```
databricks-stock_app/
├── .github/
│   └── workflows/                    # GitHub Actions CI/CD pipelines
│       ├── lint-and-test.yml        # Code quality & testing
│       ├── deploy-databricks.yml    # Databricks deployment
│       └── security-scan.yml        # Security scanning
├── .streamlit/
│   └── config.toml                  # Streamlit UI configuration
├── scripts/                         # Deployment & utility scripts
│   ├── deploy_to_databricks.py     # Deploy script
│   ├── verify_deployment.py        # Verify deployment
│   ├── run_local.py                # Run app locally
│   └── test_connection.py          # Test DB connection
├── tests/                           # Unit & integration tests
│   ├── test_app.py
│   ├── test_integration.py
│   └── conftest.py
├── app.py                          # Main Streamlit application
├── app_env.py                      # Environment-based app
├── config.py                       # Configuration module
├── requirements.txt                # Python dependencies
├── CI-CD-DEPLOYMENT.md            # Detailed CI/CD setup guide
├── QUICKSTART.md                  # Quick start guide
├── readme.md                      # This file
├── .env.example                   # Environment variables template
├── .databrickscfg.example         # Databricks CLI config template
└── .gitignore                     # Git ignore rules
```

## Troubleshooting

### Connection Errors
- Verify your server hostname is correct
- Check that your HTTP path matches your SQL warehouse/cluster
- Ensure your PAT token is valid and not expired

### Table Not Found
- Verify the table name follows the format: `catalog.schema.table_name`
- Check that the table exists in your Databricks workspace
- Ensure you have permissions to access the table

### No Data Displayed
- Check that the table contains data
- Try increasing the max rows setting
- Verify the SQL warehouse/cluster is running

## Deploying to Databricks

### Automated Deployment with CI/CD (GitHub Actions)

This project includes automated CI/CD pipelines for continuous deployment to Databricks. See [CI-CD-DEPLOYMENT.md](CI-CD-DEPLOYMENT.md) for detailed setup instructions.

**Quick Setup:**
1. Configure GitHub Secrets (see [CI-CD-DEPLOYMENT.md](CI-CD-DEPLOYMENT.md))
2. Push to `main` branch
3. Workflows run automatically:
   - 🧪 Lint & Test
   - 🔒 Security Scan
   - 🚀 Deploy to Databricks

**What it does:**
- Validates code quality (flake8, black, isort, pylint)
- Runs security scans (bandit, safety, pip-audit)
- Automatically uploads files to Databricks workspace
- Verifies deployment success
- Sends Slack notifications

**Workflows included:**
- `lint-and-test.yml` - Code quality on every push/PR
- `security-scan.yml` - Security vulnerabilities daily
- `deploy-databricks.yml` - Deploy to Databricks on main branch

### Manual Deployment to Databricks

To deploy this app to Databricks Workspace manually:

1. Create a new app in your workspace
2. Upload the `app.py` file
3. Set up the required dependencies
4. Deploy and share the app URL

### Local Testing

```bash
# Test deployment scripts locally
python scripts/run_local.py

# Verify Databricks connection
python scripts/test_connection.py
```

## Security Notes

- **Never commit your PAT token** to version control
- Consider using environment variables or `.streamlit/secrets.toml` for sensitive data
- Store credentials securely and rotate tokens regularly

## Contributing

### Development Workflow

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make your changes and commit:**
   ```bash
   git add .
   git commit -m "Add my feature"
   ```

3. **Push to GitHub:**
   ```bash
   git push origin feature/my-feature
   ```

4. **Create a Pull Request**
   - GitHub Actions will automatically run tests and security scans
   - Address any failing checks before merging

5. **Merge to main**
   - After PR approval, merge to main branch
   - CI/CD pipeline automatically deploys to Databricks

### Code Quality Standards

All code must pass:
- ✅ `flake8` linting (PEP8)
- ✅ `black` formatting
- ✅ `isort` import sorting
- ✅ `pylint` code analysis
- ✅ Security scans (bandit, safety)

### Pre-commit Checks

Run locally before pushing:

```bash
# Format code
black . && isort .

# Run linting
flake8 . && pylint app.py

# Run tests
pytest tests/ -v

# Security scan
bandit -r . && safety check
```

## License

MIT License