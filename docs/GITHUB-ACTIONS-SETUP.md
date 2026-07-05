# GitHub Actions Setup Guide

Complete instructions for setting up GitHub Actions CI/CD for the Databricks Gold Table Viewer.

## Prerequisites

- GitHub repository (public or private)
- Databricks workspace with PAT token
- (Optional) Slack workspace for notifications

## Step 1: Create GitHub Secrets

GitHub Secrets are encrypted environment variables used by CI/CD workflows. They're never exposed in logs.

### 1.1 Get Your Databricks Credentials

**Databricks Host:**
- Go to your Databricks workspace
- Copy the hostname from URL: `https://example.cloud.databricks.com`
- Keep only: `example.cloud.databricks.com`

**Databricks Token:**
- In Databricks: Click username → User settings → Developer → Personal access tokens
- Click "Generate new token"
- Copy the token (you won't see it again!)

**Workspace Path:**
- In Databricks: Click username → Account settings
- Your home directory path, e.g., `/Users/your.email@company.com`

### 1.2 Add Secrets to GitHub

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**

Add these secrets:

| Secret Name | Value | Example |
|-----------|-------|---------|
| `DATABRICKS_HOST` | Databricks hostname (no https://) | `example.cloud.databricks.com` |
| `DATABRICKS_TOKEN` | Your PAT token | `dapi123abc456xyz...` |
| `DATABRICKS_WORKSPACE_PATH` | Your workspace path | `/Users/your.email@company.com` |

**Optional Secrets:**

| Secret Name | Value | Get From |
|-----------|-------|----------|
| `SLACK_WEBHOOK_URL` | Slack incoming webhook | Slack workspace settings |

### 1.3 Using GitHub CLI

Alternative: Set secrets using GitHub CLI:

```bash
# Install GitHub CLI if needed
# https://cli.github.com/

# Authenticate
gh auth login

# Set secrets
gh secret set DATABRICKS_HOST --body "example.cloud.databricks.com"
gh secret set DATABRICKS_TOKEN --body "dapi..."
gh secret set DATABRICKS_WORKSPACE_PATH --body "/Users/your.email@company.com"
gh secret set SLACK_WEBHOOK_URL --body "https://hooks.slack.com/..."
```

## Step 2: Verify Workflows

Check that GitHub Actions workflows are enabled:

1. Go to **Actions** tab in GitHub
2. Confirm workflows are visible:
   - ✅ Lint and Test
   - ✅ Deploy to Databricks
   - ✅ Security Scan

## Step 3: Trigger First Deployment

### Option A: Automatic (on Push)

```bash
# Make a change to app code
echo "# Updated" >> readme.md

# Commit and push
git add readme.md
git commit -m "Test CI/CD"
git push origin main
```

Workflows will automatically trigger.

### Option B: Manual Trigger

1. Go to **Actions** tab
2. Select **Deploy to Databricks** workflow
3. Click **Run workflow** button
4. Select environment: `dev`, `staging`, or `prod`
5. Click **Run workflow**

## Step 4: Monitor Workflow Execution

1. Go to **Actions** tab
2. Click the workflow run
3. View real-time logs
4. Check status badges in README

### Successful Workflow

```
✅ Set up job                          1s
✅ Set up Python                       15s
✅ Cache pip packages                  5s
✅ Install Databricks CLI              12s
✅ Configure Databricks CLI            2s
✅ Deploy to Databricks Workspace      30s
✅ Verify Deployment                   8s
✅ Slack Notification on Success       3s
```

### Failed Workflow

If workflow fails:
1. Click the failed step
2. Read error message
3. Common issues:
   - Invalid Databricks credentials
   - Workspace path doesn't exist
   - File permissions
   - Network connectivity

## Step 5: Post-Deployment Verification

### In Databricks

1. Go to your Databricks workspace
2. Navigate to workspace path (e.g., `/Users/your.email@company.com`)
3. Find `databricks-gold-table-viewer` directory
4. Verify files are uploaded:
   - `app.py`
   - `app_env.py`
   - `config.py`
   - `requirements.txt`
   - `config.toml`

### Create Databricks App

1. In workspace, right-click `app.py`
2. Select "Create app"
3. Configure:
   - **Name:** Databricks Gold Table Viewer
   - **Entrypoint:** `app.py`
   - **Compute:** Select SQL warehouse or cluster
4. Deploy and launch

## Workflow Configuration

### Lint and Test Workflow

**Triggers:** Every push and pull request

**Tests on Python versions:** 3.8, 3.9, 3.10, 3.11

**Checks:**
- flake8 (PEP8 linting)
- black (code formatting)
- isort (import organization)
- pylint (code quality)
- pytest (unit tests)

### Deploy Workflow

**Triggers:** Pushes to main branch OR manual trigger

**Steps:**
1. Install Databricks CLI
2. Configure credentials
3. Upload files
4. Verify deployment
5. Send Slack notification

**Environments:**
- `dev` (default, on every main push)
- `staging` (manual trigger)
- `prod` (manual trigger)

### Security Scan Workflow

**Triggers:** Every push, PR, and daily at 2 AM UTC

**Scans:**
- bandit (security vulnerabilities)
- safety (dependency vulnerabilities)
- pip-audit (package vulnerabilities)

## Advanced Configuration

### Adding Branch Protection

Require checks to pass before merging:

1. Go to **Settings** → **Branches**
2. Click **Add rule** under "Branch protection rules"
3. Enter branch name: `main`
4. Enable:
   - ✅ Require a pull request
   - ✅ Dismiss stale pull request approvals
   - ✅ Require status checks to pass
   - ✅ Select checks: Lint, Security, Tests

### Multi-Environment Deployment

Extend workflows for staging/production:

```yaml
# In deploy-databricks.yml
environment:
  name: ${{ github.event.inputs.environment || 'dev' }}
  approval_required: ${{ github.event.inputs.environment == 'prod' }}
```

Requires manual approval for production deploys.

### Slack Notifications

Setup includes Slack notifications for:
- ✅ Deployment success
- ❌ Deployment failure

#### Get Slack Webhook URL

1. Go to Slack workspace
2. Create incoming webhook:
   - **Workspace settings** → **Apps and integrations**
   - Find Incoming Webhooks
   - Create new webhook
   - Copy webhook URL
   - Add to GitHub secrets as `SLACK_WEBHOOK_URL`

## Troubleshooting

### Workflow Not Running

**Problem:** Workflows don't trigger on push

**Solutions:**
- Check GitHub Actions is enabled (Settings → Actions → General)
- Verify workflow file syntax (check for YAML errors)
- Ensure you're on the correct branch (main)

### Deployment Failed

**Problem:** Deploy step fails with authentication error

**Solutions:**
- Verify secrets are set correctly (no typos)
- Check DATABRICKS_TOKEN is not expired
- Regenerate token in Databricks and update secret

### Files Not Uploading

**Problem:** Files don't appear in Databricks workspace

**Solutions:**
- Check DATABRICKS_WORKSPACE_PATH is correct
- Verify workspace path exists
- Check token has workspace write permissions
- Check HTTP connection to Databricks

### Tests Failing

**Problem:** Lint or test checks fail

**Solutions:**
- Run locally: `flake8 .` and `black --check .`
- Auto-fix formatting: `black . && isort .`
- Run tests: `pytest tests/ -v`

## Security Best Practices

1. **Rotate Tokens**
   - Regenerate Databricks PAT every 90 days
   - Update GitHub secret after rotation

2. **Limit Permissions**
   - Use workspace-scoped tokens when possible
   - Avoid admin-level tokens

3. **Audit Logs**
   - Monitor GitHub Actions logs
   - Review Databricks audit trail
   - Set up Slack alerts

4. **Secure Secrets**
   - Never log secrets
   - Don't add secrets to commit messages
   - Use GitHub's secret masking

## Testing Locally Before Push

Avoid failed CI/CD runs:

```bash
# Test all checks locally
bash scripts/check-all.sh

# Or individually:
flake8 .
black --check .
isort --check .
pylint app.py
pytest tests/ -v
```

## Next Steps

1. ✅ Add GitHub Secrets
2. ✅ Push code to trigger first workflow
3. ✅ Monitor workflow execution
4. ✅ Verify files in Databricks
5. ✅ Create Databricks app
6. ✅ Test deployed app
7. ✅ Share with team
8. ✅ Monitor ongoing deployments

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Databricks API Documentation](https://docs.databricks.com/api/)
- [Streamlit Deployment](https://docs.streamlit.io/knowledge-base/tutorials/deploy)
- [Our CI/CD Documentation](CI-CD-DEPLOYMENT.md)
