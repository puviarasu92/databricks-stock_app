# CI/CD Deployment Guide

## Overview

This project uses GitHub Actions to automate:
- **Code Quality**: Linting, formatting, and testing
- **Security**: Vulnerability scanning
- **Deployment**: Automated deployment to Databricks workspace

## GitHub Actions Workflows

### 1. Lint and Test Workflow (`.github/workflows/lint-and-test.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

**Steps:**
- Installs dependencies
- Runs `flake8` for Python linting
- Checks code formatting with `black`
- Validates import organization with `isort`
- Runs `pylint` for code quality
- Executes pytest (if tests exist)
- Uploads coverage reports to Codecov

### 2. Deploy to Databricks Workflow (`.github/workflows/deploy-databricks.yml`)

**Triggers:**
- Push to `main` branch (when app files change)
- Manual trigger via `workflow_dispatch`

**Steps:**
- Sets up Python environment
- Configures Databricks CLI
- Uploads app files to Databricks workspace
- Verifies deployment
- Sends Slack notifications

### 3. Security Scan Workflow (`.github/workflows/security-scan.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests
- Daily schedule at 2 AM UTC

**Steps:**
- Runs `bandit` for security vulnerabilities
- Checks dependencies with `safety`
- Runs `pip-audit` for package vulnerabilities
- Uploads security reports

## GitHub Secrets Configuration

To enable CI/CD deployment, configure these GitHub secrets in your repository:

### Required Secrets for Databricks Deployment

1. **`DATABRICKS_HOST`**
   - Your Databricks workspace hostname
   - Format: `example.cloud.databricks.com` (no https://)
   - Get from: Databricks workspace URL

2. **`DATABRICKS_TOKEN`**
   - Databricks Personal Access Token (PAT)
   - Get from: Databricks workspace → User settings → Developer → Personal access tokens
   - **Never commit this token!**

3. **`DATABRICKS_WORKSPACE_PATH`**
   - Path where your app will be deployed in workspace
   - Format: `/Users/your.email@company.com`
   - Get from: Databricks workspace → User settings → User home

### Optional Secrets for Notifications

4. **`SLACK_WEBHOOK_URL`** (optional)
   - Slack incoming webhook URL
   - Get from: Slack workspace → Apps → Incoming Webhooks
   - Format: `https://hooks.slack.com/services/...`

## Setting Up GitHub Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret:
   - Name: `DATABRICKS_HOST`
   - Value: Your Databricks hostname
5. Repeat for other secrets

### Example Setup

```bash
# If you're setting up via GitHub CLI:
gh secret set DATABRICKS_HOST --body "example.cloud.databricks.com"
gh secret set DATABRICKS_TOKEN --body "dapi..."
gh secret set DATABRICKS_WORKSPACE_PATH --body "/Users/your.email@company.com"
gh secret set SLACK_WEBHOOK_URL --body "https://hooks.slack.com/..."
```

## Deployment Environments

The deploy workflow supports multiple environments:

### Development (dev) - Default
- Triggered on every push to `main`
- Deploys to dev workspace path

### Staging (staging)
- Triggered manually with `workflow_dispatch`
- Deploys to staging workspace path

### Production (prod)
- Triggered manually with `workflow_dispatch`
- Deploys to production workspace path
- Requires additional approvals (optional)

## Local Deployment

### Option 1: Run Locally with Streamlit
```bash
python scripts/run_local.py
```

### Option 2: Manual Deployment
```bash
python scripts/deploy_to_databricks.py \
  --host example.cloud.databricks.com \
  --token dapi... \
  --workspace-path /Users/your.email@company.com \
  --app-name databricks-gold-table-viewer
```

## Deployment Process

### 1. Development → GitHub

```bash
# Make changes to your app
git add app.py requirements.txt
git commit -m "Update app features"
git push origin main
```

### 2. GitHub Actions Workflow

```
┌─────────────────────────────────┐
│  Push to main branch            │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│  Lint and Test workflow runs    │
│  - flake8                       │
│  - black                        │
│  - isort                        │
│  - pylint                       │
│  - pytest                       │
└──────────────┬──────────────────┘
               │
        ┌──────┴──────┐
        │             │
        ▼             ▼
    ✅ Pass      ❌ Fail
        │             │
        ▼             │
┌─────────────────┐   │
│ Security Scan   │   │
│ workflow runs   │   │
└────────┬────────┘   │
         │            │
         ▼            │
┌─────────────────┐   │
│ Deploy workflow │   │
│ - Upload files  │   │
│ - Verify        │   │
│ - Notify        │   │
└────────┬────────┘   │
         │            │
    ✅ Success    ❌ Rejected
```

### 3. Databricks Workspace

Once deployed:

1. Go to your Databricks workspace
2. Navigate to your workspace path
3. Find the `databricks-gold-table-viewer` directory
4. Create a new App from the uploaded files
5. Configure and launch the app

## Troubleshooting

### Deployment Failed
- Check GitHub Actions logs: Repository → Actions → Recent workflows
- Verify secrets are configured correctly
- Ensure Databricks API token is valid and not expired

### Files Not Uploading
- Check `DATABRICKS_WORKSPACE_PATH` is correct
- Verify token has workspace write permissions
- Check workspace filesystem limits

### Slack Notifications Not Working
- Verify `SLACK_WEBHOOK_URL` is correct and active
- Check Slack workspace permissions

### Code Quality Checks Failing
- Run locally: `flake8 . && black --check .`
- Auto-fix: `black . && isort .`
- Check linting rules in workflow file

## Performance Optimization

### Caching
- GitHub Actions caches pip packages
- Significantly speeds up workflow runs
- Cache is invalidated when `requirements.txt` changes

### Parallel Testing
- Workflow tests on Python 3.8, 3.9, 3.10, 3.11
- Runs in parallel for faster feedback

## Security Best Practices

1. **Never commit secrets**
   - Use GitHub Secrets for sensitive data
   - `.env` files are in `.gitignore`

2. **Rotate tokens regularly**
   - Update Databricks PAT tokens every 90 days
   - Use workspace-scoped tokens when possible

3. **Monitor deployments**
   - Review deployment logs
   - Enable audit logging in Databricks

4. **Access control**
   - Limit who can trigger deployments
   - Use GitHub branch protection rules

## Advanced Configuration

### Adding Custom Environment Variables

Edit `.github/workflows/deploy-databricks.yml`:

```yaml
- name: Deploy to Databricks Workspace
  env:
    CUSTOM_VAR: value
  run: |
    python scripts/deploy_to_databricks.py ...
```

### Adding Approval Steps

For production deployments, add environment-specific approvals:

```yaml
environment:
  name: prod
  reviewers:
    - team-lead-username
```

### Integration with Other Tools

- **Terraform**: Manage Databricks infrastructure as code
- **Ansible**: Orchestrate multi-environment deployments
- **AWS/Azure/GCP**: Deploy to cloud platforms alongside Databricks

## Monitoring & Logging

### GitHub Actions Logs
- Repository → Actions → Workflow runs
- Click a run to see detailed logs
- Download artifacts (deployment packages, reports)

### Databricks Logs
- Workspace → Admin Console → Workspace Settings
- View deployment audit trail
- Monitor app usage

## Next Steps

1. ✅ Configure GitHub Secrets
2. ✅ Push changes to trigger first deployment
3. ✅ Monitor workflow execution
4. ✅ Test deployed app in Databricks
5. ✅ Set up Slack notifications for team
