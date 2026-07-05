# SSL Certificate Error - Complete Resolution Guide

## Problem Summary

You're getting this error when connecting to Databricks:
```
SSL: CERTIFICATE_VERIFY_FAILED
Basic Constraints of CA cert not marked critical
```

This is typically caused by:
- ✅ Corporate firewall/proxy with SSL inspection
- ✅ Missing CA certificates in Python environment
- ✅ Network security appliance intercepting SSL

**Good news:** We've added tools to fix this!

---

## Solution 1: ✅ QUICK FIX (Use This First)

### For Immediate Testing - Use the App Toggle

**Step 1:** Run the app
```bash
pip install -r requirements.txt
streamlit run app.py
```

**Step 2:** Look for this in the sidebar:
```
🔐 SSL/TLS Settings
☐ Verify SSL Certificate
```

**Step 3:** UNCHECK the box

**Step 4:** Click "Load Data"

✅ **Done!** App works immediately without SSL verification.

---

## Solution 2: ✅ DIAGNOSE (Find Out More)

### Run the SSL Diagnostic Tool

```bash
python scripts/ssl_diagnostic.py
```

This will:
1. Show your Python SSL configuration
2. Check CA certificate locations
3. Test HTTPS connectivity
4. Suggest fixes
5. Offer to update certificates

---

## Solution 3: ✅ TEST (Verify Connectivity)

### Run the Enhanced Test Script

```bash
python scripts/ssl_test_connection.py
```

This script:
1. Tests WITH SSL verification
2. If fails, tests WITHOUT SSL verification
3. Shows which method works
4. Provides recommendations

---

## Solution 4: ⭐ PERMANENT FIX (For Production)

### Update CA Certificates (Recommended)

```bash
# Update certifi package
pip install --upgrade certifi

# Verify it worked
python -c "import certifi; print(certifi.where())"
```

**macOS specific:**
```bash
/Applications/Python\ 3.11/Install\ Certificates.command
```

**Windows (as Administrator):**
```powershell
python -m pip install --upgrade certifi
```

**Linux:**
```bash
sudo apt-get install ca-certificates
```

---

## Solution 5: ⚠️ TEMPORARY WORKAROUND (Session Only)

### Disable SSL Verification for Current Session

**Windows PowerShell:**
```powershell
$env:PYTHONHTTPSVERIFY = "0"
streamlit run app.py
```

**Windows CMD:**
```cmd
set PYTHONHTTPSVERIFY=0
streamlit run app.py
```

**macOS/Linux:**
```bash
export PYTHONHTTPSVERIFY=0
streamlit run app.py
```

---

## Solution 6: 🏢 CORPORATE ENVIRONMENT (Work with IT)

### If Behind Corporate Proxy

Contact your IT department and ask for:

1. **CA Certificate Bundle**
   - Ask for PEM-formatted certificate
   - Location to install it

2. **Proxy Configuration**
   - Proxy hostname
   - Port number
   - Authentication (if needed)

3. **Add to Python:**
   ```python
   import os
   os.environ['SSL_CERT_FILE'] = '/path/to/ca-bundle.crt'
   ```

---

## Files We've Added

### Scripts:
- `scripts/ssl_diagnostic.py` - Diagnostic tool
- `scripts/ssl_test_connection.py` - Connection tester

### Documentation:
- `SSL-QUICK-FIX.md` - Quick reference
- `SSL-CERTIFICATE-TROUBLESHOOTING.md` - Detailed guide
- `SSL-CERTIFICATE-RESOLUTION.md` - This file

### Updated:
- `app.py` - Added SSL toggle
- `app_env.py` - Added SSL toggle
- `requirements.txt` - Added urllib3, certifi

---

## Step-by-Step Workflow

### 1. Try Immediate Fix (2 min)
```bash
streamlit run app.py
# Uncheck "Verify SSL Certificate" in sidebar
```
✅ If works → Done! Use this for development.

### 2. Run Diagnostics (5 min)
```bash
python scripts/ssl_diagnostic.py
# Follow the menu options
```
✅ Identifies your environment issues.

### 3. Test Connection (3 min)
```bash
python scripts/ssl_test_connection.py
# Follow prompts
```
✅ Confirms which SSL method works.

### 4. Update Certificates (2 min)
```bash
pip install --upgrade certifi
python scripts/ssl_test_connection.py
# Test again
```
✅ If works → Use this in production.

### 5. Still Not Working?
```bash
# Contact IT with this info:
python -c "import ssl; print(ssl.OPENSSL_VERSION)"
python -c "import certifi; print(certifi.where())"
python -c "import platform; print(platform.platform())"
```

---

## Understanding Your Error

### Why This Happens

Your computer → Proxy/Firewall → Databricks

The proxy intercepts SSL connections and re-signs them with its own certificate.

Python doesn't recognize the proxy's certificate, so it fails.

### Why Disabling SSL Works

The connection is still encrypted (TLS), but we skip verification.

Safe for:
- ✅ Internal networks
- ✅ Development/testing
- ✅ Trusted environments

Not recommended for:
- ❌ Public internet
- ❌ Production systems
- ❌ Sensitive data

---

## Recommended Approach

### For Development/Testing:
1. Use app toggle (quick and easy)
2. Or use test script to verify

### For Production:
1. Update certifi properly
2. Work with IT on CA certificates
3. Implement OAuth if possible
4. Never disable SSL verification

---

## Troubleshooting

### "Still getting SSL error with toggle unchecked"
- Make sure to restart the Streamlit app after unchecking
- Clear browser cache
- Try incognito/private mode

### "Certifi update didn't help"
- You may have corporate proxy
- Try `python scripts/ssl_diagnostic.py`
- Contact IT about CA certificate

### "Test script hangs"
- You may be behind proxy without credentials
- Stop the script (Ctrl+C)
- Contact IT about proxy settings

---

## Quick Reference

| Situation | Solution | Time |
|-----------|----------|------|
| Just testing | App toggle | 1 min |
| Need details | Run ssl_diagnostic.py | 5 min |
| Want permanent fix | pip install --upgrade certifi | 2 min |
| Still stuck | Contact IT | varies |

---

## Next Steps

1. ✅ Try Solution 1 (app toggle)
2. ✅ Run Solution 2 (diagnostic)
3. ✅ Test Solution 3 (connection test)
4. ✅ Apply Solution 4 (update certifi)
5. ✅ Use app!

---

## Getting Help

If issues persist:

**Check:**
1. Run: `python scripts/ssl_diagnostic.py`
2. Read: `SSL-CERTIFICATE-TROUBLESHOOTING.md`
3. Try: `python scripts/ssl_test_connection.py`

**Contact IT with:**
```bash
# Run these and share output
python --version
pip show certifi
python -c "import ssl; print(ssl.OPENSSL_VERSION)"
```

**Databricks Support:**
- Include full error message
- Include Python version
- Include platform info
- Mention proxy environment

---

## Security Note

⚠️ **For Testing/Development Only:**
- Don't disable SSL verification for sensitive data
- Don't commit code with SSL disabled to production
- Update certificates when possible

✅ **Best Practice:**
- Use proper certificate updates
- Enable SSL verification in production
- Regularly update certifi and Python
- Follow your organization's security policies

---

## Summary

We've made it easy:

1. **Quick test?** Use app toggle ✅
2. **Want details?** Run diagnostic ✅
3. **Need permanent?** Update certifi ✅
4. **Still stuck?** We have tools to help ✅

Choose your path above and enjoy your Databricks app! 🚀
