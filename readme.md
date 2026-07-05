# 📊 Databricks Gold Table Viewer

> A Streamlit application for displaying rows from Databricks gold tables in interactive table format

## 📚 Documentation

See the complete documentation in the [`docs/`](docs/) folder:

- **[readme.md](docs/readme.md)** - Full project documentation
- **[QUICKSTART.md](docs/QUICKSTART.md)** - 5-minute quick start guide  
- **[CI-CD-DEPLOYMENT.md](docs/CI-CD-DEPLOYMENT.md)** - CI/CD pipeline documentation
- **[DEPLOYMENT-ARCHITECTURE.md](docs/DEPLOYMENT-ARCHITECTURE.md)** - Architecture and deployment guides
- **[SSL-QUICK-FIX.md](docs/SSL-QUICK-FIX.md)** - SSL certificate troubleshooting

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run src/app.py
```

## 📁 Project Structure

```
databricks-stock_app/
├── src/                          # Main application code
│   ├── app.py                    # Main Streamlit app (manual credentials)
│   ├── app_env.py                # Alternative app (env-based config)
│   └── config.py                 # Configuration module
├── scripts/                      # Deployment and utility scripts
│   ├── deploy_to_databricks.py   # Deploy to Databricks workspace
│   ├── verify_deployment.py      # Verify deployment
│   ├── run_local.py              # Run app locally
│   ├── ssl_test_connection.py    # Test SSL connection
│   ├── ssl_diagnostic.py         # Diagnose SSL issues
│   ├── check-all.sh/.bat         # Pre-commit validation
├── tests/                        # Test suite
│   ├── test_app.py              # Application tests
│   ├── test_integration.py      # Integration tests
│   ├── conftest.py              # pytest configuration
├── config/                       # Configuration templates
│   ├── .env.example              # Environment variable template
│   └── .databrickscfg.example    # Databricks CLI config template
├── docs/                         # Complete documentation
│   ├── readme.md                 # Full documentation
│   ├── QUICKSTART.md             # Quick start guide
│   ├── CI-CD-DEPLOYMENT.md       # CI/CD documentation
│   └── ... (more docs)
├── .github/workflows/            # GitHub Actions CI/CD
├── .streamlit/                   # Streamlit configuration
├── requirements.txt              # Python dependencies
└── .gitignore                    # Git ignore rules
```

## ✨ Features

- ✅ Real-time data display from Databricks gold tables
- ✅ Interactive table with filtering and sorting
- ✅ CSV export functionality
- ✅ Configurable row display limits
- ✅ SSL certificate verification toggle
- ✅ Environment-based and manual credential modes
- ✅ Comprehensive CI/CD pipeline with GitHub Actions
- ✅ Complete test coverage
- ✅ Security scanning and code quality checks

## 🔧 Requirements

- Python 3.8+
- Databricks workspace with SQL Warehouse
- Personal Access Token (PAT) for authentication

## 🚀 Deployment

### Local Development
```bash
streamlit run src/app.py
```

### Databricks Workspace
```bash
python scripts/deploy_to_databricks.py \
  --host your-workspace.cloud.databricks.com \
  --token your_token \
  --workspace-path /your/path
```

### GitHub Actions (Automated)
Push to `main` branch - automatically runs CI/CD pipeline with testing and deployment.

## 📖 Full Documentation

For complete documentation, troubleshooting, and advanced setup, see [docs/readme.md](docs/readme.md)

---

**Need help?** Check the [docs/](docs/) folder or see [QUICKSTART.md](docs/QUICKSTART.md) to get started in 5 minutes.
