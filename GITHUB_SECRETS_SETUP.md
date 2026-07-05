# 🔑 GitHub Actions Secrets & Variables Setup

## What You Need to Do

You need to add **4 secrets** to GitHub so your CI/CD workflows can deploy to Databricks. Here's the step-by-step guide:

---

## 📋 Required Secrets

| Secret Name | Where to Find | Example |
|-------------|---------------|---------|
| `DATABRICKS_HOST` | Databricks workspace URL | `dbc-6dc3d433-af86.cloud.databricks.com` |
| `DATABRICKS_TOKEN` | Personal Access Token (PAT) | `dapi123456789abcdef...` |
| `DATABRICKS_WORKSPACE_PATH` | Your workspace path | `/Users/your.email@company.com` |
| `SLACK_WEBHOOK_URL` | Slack (optional) | `https://hooks.slack.com/services/...` |

---

## 🚀 Step-by-Step: Add Secrets to GitHub

### **Step 1: Go to GitHub Repository Settings**

1. Open your GitHub repository in browser
2. Click **Settings** (top right area)
   ```
   Your repo → Settings
   ```

### **Step 2: Find "Secrets and variables"**

1. In left sidebar, look for: **Secrets and variables**
2. Click on it to expand
3. Select: **Actions**
   ```
   Settings
   └── Secrets and variables
       └── Actions ← Click here
   ```

### **Step 3: Add Each Secret**

Click **"New repository secret"** button

#### **Secret 1: DATABRICKS_HOST**
- **Name:** `DATABRICKS_HOST`
- **Value:** Your Databricks workspace hostname (without `https://`)
  - From URL: `https://dbc-6dc3d433-af86.cloud.databricks.com/...`
  - Use: `dbc-6dc3d433-af86.cloud.databricks.com`
- Click **Add secret**

#### **Secret 2: DATABRICKS_TOKEN**
- **Name:** `DATABRICKS_TOKEN`
- **Value:** Your Personal Access Token
  - Generate in Databricks: Settings → User Settings → Access Tokens → Generate New Token
  - Copy the full token (starts with `dapi`)
  - Example: `dapi123456789abcdefghijklmnopqrst`
- **⚠️ IMPORTANT:** This is sensitive! GitHub hides it after you save
- Click **Add secret**

#### **Secret 3: DATABRICKS_WORKSPACE_PATH**
- **Name:** `DATABRICKS_WORKSPACE_PATH`
- **Value:** Your Databricks workspace path
  - Usually: `/Users/your.email@company.com`
  - Or: `/Users/12345678901234567890`
  - Check in Databricks workspace sidebar
- Click **Add secret**

#### **Secret 4: SLACK_WEBHOOK_URL (Optional)**
- **Name:** `SLACK_WEBHOOK_URL`
- **Value:** Your Slack webhook URL (if you want notifications)
  - Generate at: https://api.slack.com/apps → Create App → Incoming Webhooks
   - Example: `https://hooks.slack.com/services/<TEAM_ID>/<CHANNEL_ID>/<WEBHOOK_TOKEN>`
- If you skip this, just don't add it - workflows will continue anyway
- Click **Add secret**

---

## 📍 Visual Guide: Where to Find Values

### **Finding DATABRICKS_HOST**

```
Databricks URL: https://dbc-6dc3d433-af86.cloud.databricks.com/workspace/...
                        ▲
                        └─ Use THIS part only
                           (without https://)

DATABRICKS_HOST = dbc-6dc3d433-af86.cloud.databricks.com
```

### **Finding DATABRICKS_TOKEN**

1. In Databricks workspace, click your **profile icon** (top right)
2. Select **Settings**
3. Click **Developer**
4. Click **Access tokens**
5. Click **Generate new token**
6. Copy the token (it looks like: `dapi...`)
7. **⚠️ Copy immediately** - you can only see it once!

### **Finding DATABRICKS_WORKSPACE_PATH**

1. In Databricks workspace, look at left sidebar
2. Find **Workspace** section
3. Your path is shown next to your username
   - Usually: `/Users/your.email@company.com`
4. Or go to: Settings → User Settings → look for workspace path

---

## ✅ Verification Checklist

After adding secrets, verify they work:

- [ ] `DATABRICKS_HOST` added (without `https://`)
- [ ] `DATABRICKS_TOKEN` added (full token, starts with `dapi`)
- [ ] `DATABRICKS_WORKSPACE_PATH` added (starts with `/Users/`)
- [ ] `SLACK_WEBHOOK_URL` added (optional, for notifications)
- [ ] All secrets show as masked (black dots) in GitHub

---

## 🔄 How Secrets Are Used

### **When you push to GitHub:**

```
1. You push to main branch
   ↓
2. GitHub Actions runs the workflow
   ↓
3. Workflow uses the secrets:
   - DATABRICKS_HOST    → Connect to workspace
   - DATABRICKS_TOKEN   → Authenticate
   - DATABRICKS_WORKSPACE_PATH → Deploy location
   - SLACK_WEBHOOK_URL  → Send notifications
   ↓
4. Your app deploys to Databricks!
```

---

## 📂 Environment-Specific Secrets (Advanced)

For different environments (dev, staging, prod), you can also set up **environments**:

1. Go to: Settings → **Environments**
2. Create: **dev**, **staging**, **prod**
3. Add different secrets for each
4. Workflow automatically uses the right secrets

Example:
```
dev environment:
  - DATABRICKS_HOST: dev-workspace.cloud.databricks.com
  - DATABRICKS_WORKSPACE_PATH: /Users/your.email@company.com/dev

prod environment:
  - DATABRICKS_HOST: prod-workspace.cloud.databricks.com
  - DATABRICKS_WORKSPACE_PATH: /Users/your.email@company.com/prod
```

---

## 🚨 Important Security Notes

✅ **DO:**
- Keep tokens secret and private
- Regenerate tokens if compromised
- Use separate tokens for different environments
- Store backup of token in secure password manager

❌ **DON'T:**
- Share tokens in chat or emails
- Commit tokens to Git (GitHub will catch this)
- Reuse tokens across multiple projects
- Leave old tokens active

---

## 🧪 Test Your Setup

After adding secrets, push a small change to main branch:

```bash
git add .
git commit -m "Test CI/CD setup"
git push origin main
```

Then check if workflow runs:
1. Go to: **Actions** tab in GitHub
2. You should see your workflow running
3. Wait for it to complete
4. Check Slack for notification (if configured)

---

## ❓ Troubleshooting

### **"Workflow failed - authentication error"**
- Check `DATABRICKS_TOKEN` is correct
- Check `DATABRICKS_HOST` doesn't have `https://`
- Regenerate token and update secret

### **"Workspace path not found"**
- Verify `DATABRICKS_WORKSPACE_PATH` is correct
- Check it starts with `/Users/`
- Try: `/Users/your.email@company.com`

### **"Slack notification not sending"**
- This is optional - you can skip it
- Or verify webhook URL is correct
- Make sure webhook is active in Slack

### **Secret not being used**
- Refresh the page after adding secret
- Wait 30 seconds for GitHub to update
- Try pushing again

---

## 📚 Reference

**Workflow Files that Use Secrets:**
- `.github/workflows/deploy-databricks.yml` - Uses all 4 secrets
- `.github/workflows/lint-and-test.yml` - No secrets needed
- `.github/workflows/security-scan.yml` - No secrets needed

**Secrets Used:**
- `deploy-databricks.yml`: DATABRICKS_HOST, DATABRICKS_TOKEN, DATABRICKS_WORKSPACE_PATH, SLACK_WEBHOOK_URL

---

## 🎯 Next Steps

1. ✅ Add all 4 secrets to GitHub
2. ✅ Verify they show in Settings → Secrets
3. ✅ Make a small commit to main branch
4. ✅ Check Actions tab to see workflow run
5. ✅ Verify deployment appears in Databricks workspace

---

## 💡 Quick Checklist

- [ ] I've added `DATABRICKS_HOST` secret
- [ ] I've added `DATABRICKS_TOKEN` secret
- [ ] I've added `DATABRICKS_WORKSPACE_PATH` secret
- [ ] I've added `SLACK_WEBHOOK_URL` secret (optional)
- [ ] Secrets are visible in Settings → Secrets → Actions
- [ ] I've tested by pushing to main branch
- [ ] Workflow ran successfully (check Actions tab)

---

**Once secrets are added, your CI/CD pipeline is ready to go!** 🚀

Push to main branch and watch your app deploy automatically to Databricks!
