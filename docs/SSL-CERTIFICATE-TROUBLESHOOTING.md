# SSL Certificate Verification Error - Troubleshooting Guide

## Error Message

```
HTTPSConnectionPool(host='dbc-xxxxx.cloud.databricks.com', port=443): 
Max retries exceeded with url: /oidc/.well-known/oauth-authorization-server
(Caused by SSLError(SSLCertificateVerifyError(1, 
'[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: 
Basic Constraints of CA cert not marked critical (_ssl.c:1032)')))
```

## Common Causes

1. **Corporate Firewall/Proxy** - Most common
   - Proxy intercepting SSL connections
   - Missing CA certificates

2. **Outdated SSL Certificates**
   - System CA bundle not updated
   - Python's certifi package outdated

3. **Network Configuration**
   - VPN with custom SSL proxy
   - Company network security appliances

4. **Python Environment**
   - Virtual environment certificate issues
   - Incorrect Python configuration

## Solutions (In Order of Preference)

### ✅ Solution 1: Use the Updated App with SSL Toggle (RECOMMENDED)

We've updated both `app.py` and `app_env.py` with an SSL verification checkbox.

**Steps:**
1. In the Streamlit sidebar, look for "🔐 SSL/TLS Settings"
2. **Uncheck "Verify SSL Certificate"**
3. Click "Load Data"

**Pros:**
- Easy toggle without code changes
- Works immediately
- No environment variable modifications needed

**Cons:**
- Should only be used for testing/development
- Not recommended for production

---

### ✅ Solution 2: Update CA Certificates (RECOMMENDED FOR PRODUCTION)

Update Python's certificate bundle:

```bash
# macOS
/Applications/Python\ 3.x/Install\ Certificates.command

# Windows - Run PowerShell as Administrator
# In Python installation directory:
cd "C:\Users\YOUR_USER\AppData\Local\Programs\Python\Python3x"
python -m pip install --upgrade certifi

# Then run update script:
python -c "
import ssl
import certifi
print(f'Certificates location: {certifi.where()}')
"
```

**Verify:**
```bash
python -c "import certifi; print(certifi.where())"
```

---

### ✅ Solution 3: Disable SSL Verification via Environment Variables

#### Option A: Temporary (Current Session Only)

**macOS/Linux:**
```bash
export PYTHONHTTPSVERIFY=0
streamlit run app.py
```

**Windows PowerShell:**
```powershell
$env:PYTHONHTTPSVERIFY = "0"
streamlit run app.py
```

**Windows Command Prompt:**
```cmd
set PYTHONHTTPSVERIFY=0
streamlit run app.py
```

#### Option B: Permanent (.env File)

Create or edit `.env` file:
```env
PYTHONHTTPSVERIFY=0
PYTHONWARNINGS=ignore::DeprecationWarning
```

---

### ✅ Solution 4: Configure Python's SSL Context

Create `ssl_config.py`:

```python
import ssl
import urllib3

# Disable SSL verification warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# For Python 3.10+
ssl.create_default_context().check_hostname = False
ssl.create_default_context().verify_mode = ssl.CERT_NONE
```

Then import in your script:
```python
import ssl_config  # Add this at the top of app.py
```

---

### ✅ Solution 5: Use System Proxy Settings

If behind corporate proxy, configure proxy:

```python
import os
import requests

# Configure proxy
proxies = {
    'http': 'http://proxy.company.com:8080',
    'https': 'http://proxy.company.com:8080',
}

# Set environment variables
os.environ['HTTP_PROXY'] = 'http://proxy.company.com:8080'
os.environ['HTTPS_PROXY'] = 'http://proxy.company.com:8080'
os.environ['NO_PROXY'] = 'localhost,127.0.0.1'
```

---

### ✅ Solution 6: Use Requests Library with Custom CA

```python
import requests
import certifi

# Create session with custom CA
session = requests.Session()
session.verify = certifi.where()

# Or use Databricks with proxy
from databricks import sql

connection = sql.connect(
    server_hostname='your-workspace.cloud.databricks.com',
    http_path='/sql/1.0/warehouses/your-id',
    personal_access_token='dapi...',
    session=session
)
```

---

## Testing Connectivity

Use the included test script:

```bash
python scripts/test_connection.py
```

This will:
1. Attempt connection with SSL verification enabled
2. If failed, attempt with SSL verification disabled
3. Show which method works for your environment

---

## For Production Environments

### ❌ DO NOT use SSL verification disabled in production!

**Instead:**

1. **Install Corporate CA Certificates:**
   - Get certificate from IT department
   - Add to Python's certifi bundle
   - Or use system certificate store

2. **Use Databricks Unity Catalog:**
   - Supports OAuth without SSL issues
   - More secure than PAT tokens
   - Ask Databricks support for help

3. **Configure Properly:**
   - Add CA bundle path to environment
   - Update certifi package regularly
   - Use HTTPS with verified certificates

4. **Network Level:**
   - Work with IT to whitelist Databricks domain
   - Ensure SSL inspection is compatible
   - Use SSL/TLS 1.2 or higher

---

## Environment-Specific Solutions

### Corporate Network (Most Common)

```python
import os
import ssl

# Set proxy
os.environ['HTTPS_PROXY'] = 'http://proxy.company.com:8080'
os.environ['HTTP_PROXY'] = 'http://proxy.company.com:8080'

# Disable SSL verification for testing only
ssl._create_default_https_context = ssl._create_unverified_context
```

### VPN Connection

```python
# Usually works fine, but sometimes needs:
import urllib3
urllib3.disable_warnings()

# Then disable verification if needed
```

### Development Machine

```python
# Use the app.py toggle:
# - Uncheck "Verify SSL Certificate" in sidebar
# - OR use test_connection.py which handles both cases
```

---

## Verification Steps

After applying a solution, verify:

```bash
# Test 1: Direct connection
python -c "
from databricks import sql
connection = sql.connect(
    server_hostname='your-host.cloud.databricks.com',
    http_path='/sql/1.0/warehouses/your-id',
    personal_access_token='dapi...'
)
print('✅ Connection successful!')
"

# Test 2: Run app
streamlit run app.py
```

---

## Debugging Information

Enable verbose logging:

```bash
# Set debug environment variables
export CURL_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
export REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

# Run with verbose output
python -vvv scripts/test_connection.py
```

---

## Frequently Asked Questions

**Q: Is disabling SSL verification safe?**
A: Only for testing/development with known endpoints. Never in production.

**Q: Why do I get this error in app but not in terminal?**
A: Different environments may have different certificate stores or proxy settings.

**Q: How do I know if I'm behind a corporate proxy?**
A: Contact IT or check system proxy settings (Settings → Network → Proxy).

**Q: Will this be fixed by updating Databricks SDK?**
A: Sometimes. Try: `pip install --upgrade databricks-sdk databricks-sql-connector`

**Q: Should I upgrade Python?**
A: Yes, newer Python versions have better certificate handling.

---

## Getting Help

If you continue to experience issues:

1. **Collect Information:**
   ```bash
   python --version
   pip show databricks-sql-connector
   python -c "import certifi; print(certifi.where())"
   ```

2. **Check Network:**
   ```bash
   # Verify you can reach Databricks
   curl -v https://your-host.cloud.databricks.com
   ```

3. **Contact Support:**
   - Databricks Support: support.databricks.com
   - Your IT Department: Network/Proxy settings
   - Include the full error message

---

## Quick Reference

| Method | Use Case | Difficulty |
|--------|----------|-----------|
| App Toggle | Development/Testing | ✅ Easy |
| Update Certifi | Production | ⭐ Medium |
| Environment Variable | Quick Fix | ✅ Easy |
| Test Script | Diagnosis | ✅ Easy |
| Corporate CA | Compliance | ⭐ Medium |
| OAuth/Unity Catalog | Long-term | ⭐⭐ Hard |

---

## Summary

1. **For immediate testing:** Use the app toggle ✅
2. **For production:** Update certificates properly ⭐
3. **For debugging:** Use test_connection.py ✅
4. **For corporate:** Work with IT on CA certificates ⭐

---

**Still having issues?** Make sure to:
- Use the latest version of the app
- Try multiple solutions above
- Contact Databricks support with full error details
