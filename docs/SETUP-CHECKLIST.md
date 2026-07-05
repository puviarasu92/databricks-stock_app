🚀 CI/CD SETUP CHECKLIST
======================

Follow these steps to complete your CI/CD setup:

[ ] STEP 1: Prepare Databricks Credentials (5 min)
    ├─ [ ] Go to Databricks workspace
    ├─ [ ] Get hostname from URL (e.g., example.cloud.databricks.com)
    ├─ [ ] Create Personal Access Token:
    │   ├─ Click username → User settings
    │   ├─ Developer → Personal access tokens
    │   ├─ Click "Generate new token"
    │   └─ Copy the token (save it securely!)
    ├─ [ ] Get workspace path:
    │   ├─ Click username → Account settings
    │   └─ Copy your home path (e.g., /Users/your.email@company.com)
    └─ [ ] Have these 3 values ready:
        ├─ DATABRICKS_HOST
        ├─ DATABRICKS_TOKEN
        └─ DATABRICKS_WORKSPACE_PATH

[ ] STEP 2: Configure GitHub Secrets (5 min)
    ├─ [ ] Go to your GitHub repository
    ├─ [ ] Click Settings → Secrets and variables → Actions
    ├─ [ ] Click "New repository secret"
    ├─ [ ] Add Secret #1:
    │   ├─ Name: DATABRICKS_HOST
    │   └─ Value: example.cloud.databricks.com
    ├─ [ ] Add Secret #2:
    │   ├─ Name: DATABRICKS_TOKEN
    │   └─ Value: dapi... (your token)
    ├─ [ ] Add Secret #3:
    │   ├─ Name: DATABRICKS_WORKSPACE_PATH
    │   └─ Value: /Users/your.email@company.com
    └─ [ ] (Optional) Add Secret #4:
        ├─ Name: SLACK_WEBHOOK_URL
        └─ Value: https://hooks.slack.com/... (if using Slack)

[ ] STEP 3: Install Local Dependencies (2 min)
    ├─ [ ] Open terminal in project directory
    └─ [ ] Run: pip install -r requirements.txt

[ ] STEP 4: Test Locally (3 min)
    ├─ [ ] macOS/Linux: bash scripts/check-all.sh
    ├─ [ ] Windows: scripts\check-all.bat
    └─ [ ] Fix any issues reported

[ ] STEP 5: Commit & Push Changes (2 min)
    ├─ [ ] git add .
    ├─ [ ] git commit -m "Add CI/CD pipelines"
    └─ [ ] git push origin main

[ ] STEP 6: Monitor First Deployment (3-5 min)
    ├─ [ ] Go to GitHub repo → Actions
    ├─ [ ] Watch for three workflows:
    │   ├─ [ ] Lint and Test workflow (should complete in 2-3 min)
    │   ├─ [ ] Security Scan workflow (should complete in 1-2 min)
    │   └─ [ ] Deploy to Databricks workflow (should complete in 2-3 min)
    └─ [ ] Verify all three show ✅ (green checkmarks)

[ ] STEP 7: Verify Deployment in Databricks (3 min)
    ├─ [ ] Log into Databricks workspace
    ├─ [ ] Navigate to your workspace path
    │   └─ /Workspace/Users/your.email@company.com/
    ├─ [ ] Look for "databricks-gold-table-viewer" folder
    ├─ [ ] Open the folder and verify files:
    │   ├─ [ ] app.py
    │   ├─ [ ] app_env.py
    │   ├─ [ ] config.py
    │   ├─ [ ] requirements.txt
    │   └─ [ ] config.toml
    └─ [ ] Take a screenshot for your records

[ ] STEP 8: Create Databricks App (5 min)
    ├─ [ ] In your Databricks workspace
    ├─ [ ] Right-click on app.py
    ├─ [ ] Select "Create app"
    ├─ [ ] Configure:
    │   ├─ [ ] Name: Databricks Gold Table Viewer
    │   ├─ [ ] Entrypoint: app.py
    │   └─ [ ] Cluster: Select your SQL warehouse
    ├─ [ ] Click "Deploy"
    └─ [ ] Wait for app to start

[ ] STEP 9: Test the App (5 min)
    ├─ [ ] Get app URL from Databricks
    ├─ [ ] Open in browser
    ├─ [ ] Enter test connection details:
    │   ├─ [ ] Server Hostname
    │   ├─ [ ] HTTP Path
    │   ├─ [ ] PAT Token
    │   └─ [ ] Table Name
    ├─ [ ] Click "Load Data"
    └─ [ ] Verify data displays in table

[ ] STEP 10: Share with Team (5 min)
    ├─ [ ] Copy app URL from Databricks
    ├─ [ ] Share with team members
    ├─ [ ] Provide documentation link
    └─ [ ] Ask for feedback

[ ] STEP 11: (Optional) Configure Slack Notifications (3 min)
    ├─ [ ] Go to Slack workspace settings
    ├─ [ ] Create Incoming Webhook
    ├─ [ ] Copy webhook URL
    ├─ [ ] Add to GitHub Secrets as SLACK_WEBHOOK_URL
    └─ [ ] Test by triggering a deployment

[ ] STEP 12: (Optional) Set Up Branch Protection (2 min)
    ├─ [ ] Go to GitHub repo → Settings → Branches
    ├─ [ ] Add branch protection rule for "main"
    ├─ [ ] Enable:
    │   ├─ Require pull requests
    │   ├─ Require status checks to pass
    │   ├─ Require branches to be up to date
    │   └─ Dismiss stale pull request approvals
    └─ [ ] Save

TOTAL ESTIMATED TIME: 45-60 minutes

═══════════════════════════════════════════════════════════════

📚 DOCUMENTATION REFERENCE

If you need help with any step:

Quick Start:
→ Read: QUICKSTART.md (5 min)

GitHub Setup Details:
→ Read: GITHUB-ACTIONS-SETUP.md (15 min)

Complete CI/CD Guide:
→ Read: CI-CD-DEPLOYMENT.md (20 min)

System Architecture:
→ Read: DEPLOYMENT-ARCHITECTURE.md (10 min)

Feature Summary:
→ Read: CI-CD-SETUP.md (10 min)

═══════════════════════════════════════════════════════════════

🆘 TROUBLESHOOTING

If workflows don't run:
1. Check GitHub Actions is enabled
2. Verify branch is "main"
3. Check for YAML syntax errors in workflow files

If deployment fails:
1. Verify secrets are correct (no typos)
2. Check Databricks token isn't expired
3. Verify workspace path exists
4. Review GitHub Actions logs for error message

If app doesn't appear in Databricks:
1. Go to GitHub Actions and check Deploy workflow logs
2. Verify credentials in secrets are correct
3. Try manual deployment: python scripts/deploy_to_databricks.py

═══════════════════════════════════════════════════════════════

✅ SUCCESS CRITERIA

You're done when:
✓ All GitHub Secrets are configured
✓ First deployment workflow completed successfully
✓ Files appear in Databricks workspace
✓ Databricks App is created and running
✓ You can view data in the app
✓ Team can access the app via shared URL

═══════════════════════════════════════════════════════════════

🎉 CONGRATULATIONS!

You now have:
✅ Automated code quality checks
✅ Automated security scanning
✅ Automated deployment to Databricks
✅ Automated notifications
✅ Production-ready CI/CD pipeline

Every time you push code, it will automatically:
1. Test the code
2. Scan for security issues
3. Deploy to Databricks
4. Notify your team

Enjoy automated deployments! 🚀

═══════════════════════════════════════════════════════════════
