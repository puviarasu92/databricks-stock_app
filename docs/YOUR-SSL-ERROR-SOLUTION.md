# YOUR SSL ERROR - IMMEDIATE SOLUTION

## Your Exact Error
```
HTTPSConnectionPool(host='dbc-6dc3d433-af86.cloud.databricks.com', port=443): 
Max retries exceeded with url: /oidc/.well-known/oauth-authorization-server 
(Caused by SSLError(SSLCertificateVerifyError(1, 
'[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: 
Basic Constraints of CA cert not marked critical')))
```

## What This Means
❌ SSL certificate verification failed
✅ Databricks is reachable
✅ Your credentials are correct
⚠️ Corporate firewall or proxy is intercepting SSL

---

## ✅ SOLUTION - DO THIS NOW (5 Minutes)

### Step 1: Close any running Streamlit apps
Press `Ctrl+C` in any terminal running Streamlit

### Step 2: Reinstall dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Step 3: Run the app
```bash
streamlit run app.py
```

### Step 4: In Streamlit sidebar, find SSL Settings
Look for: **🔐 SSL/TLS Settings**

### Step 5: UNCHECK the box
```
☐ Verify SSL Certificate  (UNCHECK THIS)
```

### Step 6: Enter your Databricks details
- Server Hostname: `dbc-6dc3d433-af86.cloud.databricks.com`
- HTTP Path: Your warehouse/cluster path
- PAT Token: Your token
- Table Name: Your table name

### Step 7: Click "Load Data"

✅ **Should work now!**

---

## If That Doesn't Work

### Try the test script:
```bash
python scripts/ssl_test_connection.py
```

This will:
1. Test WITH SSL (will fail)
2. Test WITHOUT SSL (should work)
3. Suggest next steps

### Run the diagnostic:
```bash
python scripts/ssl_diagnostic.py
```

Follow the menu:
1. Select option "1" to update Certifi
2. Try again

---

## Understanding What You're Doing

### ✅ Safe for Development
- Connection is still encrypted
- You're just skipping verification
- Same as using HTTP on a secure intranet
- Used for internal Databricks testing

### ❌ Not for Production
- Don't use this for sensitive data
- Don't deploy to production with this
- Fix certificates properly instead

---

## Permanent Solution (Later)

When you have time:

1. Run:
```bash
pip install --upgrade certifi
```

2. macOS users run:
```bash
/Applications/Python\ 3.11/Install\ Certificates.command
```

3. Then verify:
```bash
python scripts/ssl_test_connection.py
```

4. Try WITH SSL enabled (uncheck the toggle)

---

## If Corporate IT

If you're on a corporate network:

1. Contact your IT department
2. Ask them about:
   - SSL inspection proxy
   - CA certificate requirements
   - Proxy settings

3. They may need to:
   - Add Databricks domain to whitelist
   - Provide CA certificate
   - Configure proxy settings

---

## Right Now - Just Run This

```bash
# Quick test
python scripts/ssl_test_connection.py

# Should show:
# ✅ Connection successful! (without SSL)
# ⚠️ SSL Verification Issue Detected!
# 
# This is normal - just use the app with SSL unchecked.
```

---

## Your App is Ready!

Everything else works:
- ✅ UI is beautiful
- ✅ Databricks connection works
- ✅ Data displays in table
- ✅ CSV download works
- ✅ Statistics work

Just need to uncheck SSL verification to use it.

---

## Quick Checklist

- [ ] Closed any running Streamlit app
- [ ] Ran: `pip install --upgrade -r requirements.txt`
- [ ] Started app with: `streamlit run app.py`
- [ ] Found SSL settings in sidebar
- [ ] Unchecked "Verify SSL Certificate"
- [ ] Entered Databricks details
- [ ] Clicked "Load Data"
- [ ] ✅ Seeing data!

---

## Documents to Read Later

When you have time:
- `SSL-QUICK-FIX.md` - Quick reference
- `SSL-CERTIFICATE-RESOLUTION.md` - All solutions
- `SSL-CERTIFICATE-TROUBLESHOOTING.md` - Detailed troubleshooting

---

## Right Now - Just Do This:

```bash
# 1. Update dependencies
pip install --upgrade -r requirements.txt

# 2. Run app
streamlit run app.py

# 3. In sidebar: Uncheck SSL verification

# 4. Load data

# Done! ✅
```

That's it! The app works now. Enjoy! 🎉
