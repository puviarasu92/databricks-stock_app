# SSL Certificate Error - Quick Fix (5 minutes)

## Your Error
```
SSL: CERTIFICATE_VERIFY_FAILED
Basic Constraints of CA cert not marked critical
```

This usually means: **Corporate firewall/proxy with SSL inspection**

---

## ✅ QUICK FIX (Choose One)

### Option 1: Use the App Toggle (Easiest - Recommended for Testing)

1. Run the app:
   ```bash
   streamlit run app.py
   ```

2. In the **Streamlit sidebar**, find:
   ```
   🔐 SSL/TLS Settings
   ☐ Verify SSL Certificate
   ```

3. **UNCHECK** the box ✅

4. Enter your Databricks details

5. Click "Load Data" ✅

**This works immediately!** No restarts needed.

---

### Option 2: Test Script (Diagnose the Issue)

Run our enhanced test script:

```bash
python scripts/ssl_test_connection.py
```

This will:
1. Try WITH SSL verification
2. Try WITHOUT SSL verification  
3. Tell you which works
4. Suggest next steps

---

### Option 3: Environment Variable (For Session)

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

**macOS/Linux:**
```bash
export PYTHONHTTPSVERIFY=0
streamlit run app.py
```

---

## 🎯 Recommended Flow

1. **Immediate use:** Use Option 1 (app toggle)
2. **Diagnose:** Run Option 2 (test script)
3. **Longer term:** See SSL-CERTIFICATE-TROUBLESHOOTING.md

---

## 📋 What This Means

- ✅ Your credentials are correct
- ✅ Databricks is reachable
- ❌ SSL certificate verification is failing (likely corporate proxy)
- ✅ Disabling verification makes it work

This is **safe for development/testing**. The connection is still encrypted, just not verified.

---

## If It Still Doesn't Work

1. Run test script: `python scripts/ssl_test_connection.py`
2. Check output messages
3. Read: SSL-CERTIFICATE-TROUBLESHOOTING.md
4. Contact your IT department about SSL proxy

---

## Next Steps

✅ Use the app with SSL unchecked
✅ Enjoy your Databricks app!
✅ Share with your team

**For production/permanent fix:** See SSL-CERTIFICATE-TROUBLESHOOTING.md for certificate updates.
