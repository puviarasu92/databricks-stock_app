# Deployment Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     GitHub Repository                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  Source Code                                            │  │
│  │  ├── app.py                 (Streamlit application)    │  │
│  │  ├── app_env.py             (Environment-based app)     │  │
│  │  ├── config.py              (Configuration)             │  │
│  │  ├── requirements.txt       (Dependencies)              │  │
│  │  └── .streamlit/            (Streamlit config)          │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  CI/CD Pipelines (.github/workflows/)                  │  │
│  │  ├── lint-and-test.yml      (Code quality)             │  │
│  │  ├── deploy-databricks.yml  (Deployment)               │  │
│  │  └── security-scan.yml      (Security)                 │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  Deployment Scripts (scripts/)                         │  │
│  │  ├── deploy_to_databricks.py                           │  │
│  │  ├── verify_deployment.py                              │  │
│  │  ├── run_local.py                                      │  │
│  │  └── check-all.sh / check-all.bat                      │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  Tests (tests/)                                        │  │
│  │  ├── test_app.py                                       │  │
│  │  └── test_integration.py                               │  │
│  └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
         ▲                                      ▼
         │                                      │
         │ git push                             │ GitHub Actions
         │                                      ▼ Triggered
         │                    ┌────────────────────────────┐
         │                    │  Lint & Test Workflow      │
         │                    │  - flake8, black, isort    │
         │                    │  - pylint, pytest          │
         │                    │  - Coverage reports        │
         │                    └────────┬───────────────────┘
         │                             │
         │                             ▼
         │                    ┌────────────────────────────┐
         │                    │  Security Scan Workflow    │
         │                    │  - bandit                  │
         │                    │  - safety                  │
         │                    │  - pip-audit               │
         │                    └────────┬───────────────────┘
         │                             │
         │                             ▼
         │                    ┌────────────────────────────┐
         │                    │  Deploy Workflow           │
         │                    │  (if main branch)          │
         │                    └────────┬───────────────────┘
         │                             │
         │                             ▼
         │        ┌────────────────────────────────────┐
         │        │ Databricks Workspace               │
         │        ├────────────────────────────────────┤
         │        │ /Users/your.email@company.com/    │
         │        │   databricks-gold-table-viewer/   │
         │        │   ├── app.py                      │
         │        │   ├── app_env.py                  │
         │        │   ├── config.py                   │
         │        │   ├── requirements.txt            │
         │        │   └── config.toml                 │
         │        │                                   │
         │        │ Available as Databricks App       │
         │        └────────────────────────────────────┘
         │
         └─── Verify deployment & test locally
```

## Deployment Flow

### 1. Development Phase
```
Developer makes changes
  │
  ├─ Edit app.py
  ├─ Update requirements.txt
  ├─ Write tests
  │
  ▼
Run local checks (scripts/check-all.sh)
  │
  ├─ ✅ Code formatting (black)
  ├─ ✅ Import sorting (isort)
  ├─ ✅ Linting (flake8, pylint)
  ├─ ✅ Tests (pytest)
  │
  ▼
Commit & push to main branch
  git push origin main
```

### 2. CI/CD Execution Phase
```
GitHub Actions Triggered
  │
  ├─ Lint & Test Workflow
  │   └─ Runs on Python 3.8-3.11
  │       ├─ Linting (flake8, pylint)
  │       ├─ Formatting (black, isort)
  │       ├─ Tests (pytest)
  │       └─ Coverage report
  │
  ├─ Security Scan Workflow (parallel)
  │   └─ Code vulnerability scan
  │       ├─ bandit (code security)
  │       ├─ safety (dependencies)
  │       └─ pip-audit (packages)
  │
  └─ Deploy Workflow (if main)
      └─ Upload to Databricks
          ├─ Connect to workspace
          ├─ Upload files
          ├─ Verify upload
          └─ Send notification
```

### 3. Deployment Phase
```
Deploy Workflow
  │
  ├─ Install Databricks CLI
  │
  ├─ Configure credentials
  │   └─ Use GitHub Secrets
  │       ├─ DATABRICKS_HOST
  │       ├─ DATABRICKS_TOKEN
  │       └─ DATABRICKS_WORKSPACE_PATH
  │
  ├─ Upload files
  │   ├─ app.py
  │   ├─ app_env.py
  │   ├─ config.py
  │   ├─ requirements.txt
  │   └─ config.toml
  │
  ├─ Verify deployment
  │   └─ Check all files uploaded
  │
  ├─ Slack notification
  │   └─ Send success/failure
  │
  ▼
Available in Databricks workspace
  ├─ Create app from files
  ├─ Configure entrypoint
  ├─ Deploy app
  └─ Share URL with team
```

### 4. Production Phase
```
Databricks Workspace
  │
  ├─ Create Databricks App
  │   ├─ Select app.py
  │   ├─ Configure warehouse/cluster
  │   └─ Deploy
  │
  ├─ User Access
  │   ├─ Share app link
  │   ├─ Users access web UI
  │   └─ Streamlit connects to gold table
  │
  ├─ Monitoring
  │   ├─ App usage logs
  │   ├─ Performance metrics
  │   └─ Error tracking
  │
  ▼
Gold Table Data Display
  └─ Interactive table UI
      ├─ View data
      ├─ Sort & filter
      ├─ Download CSV
      └─ Statistics
```

## Multi-Environment Setup

```
┌──────────────────────────────────────────────────────┐
│           GitHub Repository Branches                 │
├──────────────────────────────────────────────────────┤
│                                                       │
│  ┌────────────┐    ┌────────────┐    ┌────────────┐ │
│  │  Develop   │    │   Main     │    │ Production │ │
│  │  Branch    │    │  Branch    │    │  Branch    │ │
│  └────────────┘    └────────────┘    └────────────┘ │
│         │                  │                 │       │
│         │ Merge when      │ Merge when      │       │
│         │ ready for test  │ ready for prod  │       │
│         ▼                  ▼                 ▼       │
│    ┌─────────────────────────────────────────────┐  │
│    │     GitHub Actions Workflows                │  │
│    └─────────────────────────────────────────────┘  │
│         │                  │                 │       │
│         ▼                  ▼                 ▼       │
│    ┌──────────┐      ┌──────────┐      ┌──────────┐ │
│    │  Dev App │      │ Staging  │      │   Prod   │ │
│    │ Workspace│      │ Workspace│      │Workspace │ │
│    └──────────┘      └──────────┘      └──────────┘ │
└──────────────────────────────────────────────────────┘
```

## GitHub Secrets Configuration

```
GitHub Organization
  │
  └─ Repository Settings
      │
      └─ Secrets & Variables
          │
          ├─ DATABRICKS_HOST
          │   └─ Encrypted: example.cloud.databricks.com
          │
          ├─ DATABRICKS_TOKEN
          │   └─ Encrypted: dapi...
          │
          ├─ DATABRICKS_WORKSPACE_PATH
          │   └─ Encrypted: /Users/deployer@company.com
          │
          └─ SLACK_WEBHOOK_URL (optional)
              └─ Encrypted: https://hooks.slack.com/...
```

## File Deployment Structure

```
Databricks Workspace
  │
  └─ /Workspace/Users/deployer@company.com/
      │
      └─ databricks-gold-table-viewer/
          │
          ├─ app.py .......................... Main app (Streamlit)
          ├─ app_env.py ..................... Env-based app
          ├─ config.py ..................... Configuration module
          ├─ requirements.txt .............. Dependencies
          │
          └─ config.toml ................... Streamlit config


Databricks App (Created from files)
  │
  └─ gold-table-viewer
      │
      ├─ Entrypoint: app.py
      ├─ Cluster: SQL Warehouse XYZ
      ├─ Access: Public/Shared
      │
      └─ Runtime
          ├─ Python environment
          ├─ Required packages
          └─ Streamlit server
```

## Security & Access Control

```
┌─────────────────────────────────────────────────────┐
│         Security Layers                             │
├─────────────────────────────────────────────────────┤
│                                                      │
│  Layer 1: GitHub Security                          │
│  ├─ Repository access control                      │
│  ├─ Branch protection rules                        │
│  ├─ Required status checks                         │
│  └─ Secret encryption                              │
│                                                      │
│  Layer 2: CI/CD Security                           │
│  ├─ Secrets not logged                             │
│  ├─ Code quality checks                            │
│  ├─ Security scanning                              │
│  └─ Audit logging                                  │
│                                                      │
│  Layer 3: Databricks Security                      │
│  ├─ PAT token authentication                       │
│  ├─ Workspace isolation                            │
│  ├─ Access control lists                           │
│  └─ Audit trail                                    │
│                                                      │
│  Layer 4: Application Security                     │
│  ├─ Input validation                               │
│  ├─ Connection pooling                             │
│  ├─ Timeout handling                               │
│  └─ Error handling                                 │
│                                                      │
└─────────────────────────────────────────────────────┘
```

## Rollback & Recovery

```
Issue detected after deployment
  │
  ├─ Option 1: Revert code
  │   ├─ git revert <commit>
  │   ├─ git push origin main
  │   ├─ Workflows re-run
  │   └─ Files re-deployed
  │
  ├─ Option 2: Manual rollback
  │   ├─ Update Databricks files manually
  │   ├─ Or delete and re-deploy
  │   └─ Or switch to previous version
  │
  └─ Option 3: Disable deployment
      └─ Remove secrets / disable workflow
```

## Performance & Optimization

```
Optimization Opportunities:

├─ Caching
│   └─ GitHub Actions caches pip packages
│       └─ Speeds up workflow by ~40%
│
├─ Parallelization
│   ├─ Lint & Test on multiple Python versions
│   ├─ Security Scan runs in parallel
│   └─ Reduces time from 3min → ~2min
│
├─ Conditional Deployment
│   ├─ Only deploy on app code changes
│   ├─ Skip deployment for doc-only changes
│   └─ Reduces unnecessary uploads
│
└─ Resource Optimization
    ├─ Ubuntu runners (faster than Windows)
    ├─ Minimal dependencies
    └─ Efficient caching strategy
```

## Monitoring & Logging

```
┌─────────────────────────────────────────────────────┐
│         Monitoring Points                           │
├─────────────────────────────────────────────────────┤
│                                                      │
│  GitHub Actions Dashboard                          │
│  ├─ Workflow execution status                      │
│  ├─ Job logs & output                              │
│  ├─ Artifact downloads                             │
│  └─ Deployment history                             │
│                                                      │
│  Databricks Audit Logs                             │
│  ├─ File uploads/modifications                     │
│  ├─ User access                                    │
│  ├─ App deployments                                │
│  └─ Query execution                                │
│                                                      │
│  Slack Notifications                               │
│  ├─ Deployment success/failure                     │
│  ├─ Build status changes                           │
│  └─ Team alerts                                    │
│                                                      │
│  External Monitoring (optional)                    │
│  ├─ Codecov coverage                               │
│  ├─ Bandit security reports                        │
│  └─ Custom dashboards                              │
│                                                      │
└─────────────────────────────────────────────────────┘
```

## Scalability Considerations

```
Current Setup (1 app, 1 workspace):
  └─ Works well for small teams
  └─ Simple configuration
  └─ Low maintenance

Scaling Options:

Option 1: Multiple Apps
  └─ Create separate repos/branches
  └─ Multiple GitHub workflows
  └─ Independent deployments

Option 2: Multiple Workspaces
  └─ Use GitHub environments
  └─ Different secrets per environment
  └─ Dev, Staging, Prod setup

Option 3: Multiple Teams
  └─ Organization-level secrets
  └─ Team-based access control
  └─ Shared GitHub Actions templates

Option 4: Enterprise
  └─ Self-hosted GitHub Actions runners
  └─ Private registry for packages
  └─ Advanced audit logging
  └─ Integration with existing tools
```

---

For detailed setup, see:
- [CI-CD-DEPLOYMENT.md](CI-CD-DEPLOYMENT.md)
- [GITHUB-ACTIONS-SETUP.md](GITHUB-ACTIONS-SETUP.md)
- [QUICKSTART.md](QUICKSTART.md)
