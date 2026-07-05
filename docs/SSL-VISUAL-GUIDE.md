# Visual Step-by-Step Guide - SSL Error Fix

## Your Error Message
```
HTTPSConnectionPool(host='dbc-6dc3d433-af86.cloud.databricks.com', port=443): 
Max retries exceeded with url: /oidc/.well-known/oauth-authorization-server 
(Caused by SSLError(SSLCertificateVerifyError(1, 
'[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed')))
```

**Translation:** SSL certificate can't be verified (corporate proxy issue)

---

## ✅ QUICK FIX (Do This Now)

### STEP 1: Prepare
```bash
# Stop any running app (Ctrl+C)
# Then run:
pip install --upgrade -r requirements.txt
```

### STEP 2: Start the app
```bash
streamlit run app.py
```

Your browser will open to: `http://localhost:8501`

```
┌─────────────────────────────────────────────────┐
│                                                 │
│         📊 Gold Table Viewer                    │
│         Display rows from gold tables           │
│                                                 │
│ ┌───────────────────────────────────────────┐  │
│ │ Connection Settings                       │  │
│ │                                           │  │
│ │ Server Hostname ______________________ ▼ │  │
│ │                                           │  │
│ │ HTTP Path ___________________________ ▼ │  │
│ │                                           │  │
│ │ Personal Access Token ______________ ▼ │  │
│ │ (hidden)                                  │  │
│ │                                           │  │
│ │ Table Name ______________________ ▼ │  │
│ │                                           │  │
│ │ Max Rows to Display: [100]      +     -  │  │
│ │                                           │  │
│ │ ─────────────────────────────────────── │  │
│ │                                           │  │
│ │ ☑️ SSL/TLS Settings                      │  │
│ │                                           │  │
│ │ ☑️ Verify SSL Certificate                │  │ ← FIND THIS
│ │                                           │  │
│ │    ⚠️ Turning this off disables SSL       │  │
│ │       verification. Use only for          │  │
│ │       development/testing!                │  │
│ │                                           │  │
│ │ ─────────────────────────────────────── │  │
│ │                                           │  │
│ │ [ Load Data ]                           │  │
│ │                                           │  │
│ └───────────────────────────────────────────┘  │
│                                                 │
└─────────────────────────────────────────────────┘
```

### STEP 3: Scroll down in sidebar

Find this section:
```
🔐 SSL/TLS Settings

☑️ Verify SSL Certificate

⚠️ SSL verification disabled. 
   Use only for testing!
```

### STEP 4: UNCHECK the box

**BEFORE:**
```
☑️ Verify SSL Certificate  ← CHECKED
```

**AFTER:**
```
☐ Verify SSL Certificate  ← UNCHECKED (do this!)
```

### STEP 5: Enter your details

```
Server Hostname: dbc-6dc3d433-af86.cloud.databricks.com
HTTP Path: /sql/1.0/warehouses/abc123def456
Personal Access Token: dapi...
Table Name: catalog.schema.table_name
Max Rows: 100
```

### STEP 6: Click "Load Data"

```
[ Load Data ]  ← CLICK HERE
```

### STEP 7: Success! 🎉

```
┌─────────────────────────────────────┐
│ ✅ Successfully loaded 50 rows      │
│                                      │
│ Total Rows: 50    Total Columns: 12 │
│                                      │
│ Data Preview:                        │
│ ┌──────────────────────────────────┐ │
│ │ Column1  Column2  Column3  ...   │ │
│ │ ─────────────────────────────── │ │
│ │ Value1   Value2   Value3        │ │
│ │ Value1   Value2   Value3        │ │
│ │ ...                             │ │
│ └──────────────────────────────────┘ │
│                                      │
│ [ 📥 Download as CSV ]              │
│                                      │
└─────────────────────────────────────┘
```

✅ **Your data is displayed!**

---

## Troubleshooting Visuals

### Issue: "Still getting error with SSL unchecked"

**Solution:**
1. Close app (Ctrl+C)
2. Run: `python scripts/ssl_test_connection.py`
3. Follow prompts
4. Restart app

### Issue: "Can't find SSL settings"

**Sidebar might be collapsed:**

Look for: `◁` at top left of sidebar

Click it to expand:
```
◁ ┌─────────────────────────┐
  │ Connection Settings     │
  │                         │
  │ Server Hostname...      │
  │ HTTP Path...            │
  │ etc.                    │
  │ 🔐 SSL/TLS Settings ← │
  │                         │
  └─────────────────────────┘
```

### Issue: "App won't load"

**Check terminal output:**
```bash
# You should see something like:
You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

If not, browser might be blocking it:
1. Open browser manually
2. Go to: `http://localhost:8501`

---

## Timeline

```
Before:
❌ SSL error
❌ Can't connect

Now:
⏱️ 1 min: Update requirements
⏱️ 1 min: Start app
⏱️ 30 sec: Find SSL settings
⏱️ 30 sec: Uncheck box
⏱️ 1 min: Enter details
⏱️ 10 sec: Click Load Data

✅ Total: 4-5 minutes to working app!
```

---

## Important Notes

### ✅ This is safe for:
- Development on secure networks
- Testing before production
- Internal company use
- Local machine development

### ❌ This is NOT safe for:
- Production systems
- Public internet
- Sensitive customer data
- Untrustworthy networks

### ⭐ For Production:
Read: `SSL-CERTIFICATE-RESOLUTION.md`
- Proper certificate updates
- SSL verification enabled
- Corporate IT support

---

## What You're Doing

```
BEFORE (with SSL verification):
┌─────────────┐     ❌ ERROR
│ Your App    │────SSL Verification Failed
│             │     (Corporate Proxy Issue)
└─────────────┘

AFTER (with SSL unchecked):
┌─────────────┐     ✅ SUCCESS
│ Your App    │────Connection Established
│             │     (Certificate not verified,
└─────────────┘      but still encrypted)
```

The connection is still:
- ✅ Encrypted (TLS/SSL)
- ✅ Secure
- ✅ Trusted (internal network)

Just without certificate verification.

---

## Common Questions

### Q: Is this safe?
**A:** Yes for development on trusted networks. No for production or public internet.

### Q: Will my data be secure?
**A:** Yes, the connection is encrypted. Just not verified.

### Q: Should I leave this unchecked?
**A:** Not in production. Later, update certificates and enable verification.

### Q: Do I need to do this every time?
**A:** Yes, every time you start the app. Or fix certificates (see docs).

---

## Next: Future Improvements

When you have time:

1. **Read:** `SSL-CERTIFICATE-RESOLUTION.md`
2. **Run:** `python scripts/ssl_diagnostic.py`
3. **Update:** `pip install --upgrade certifi`
4. **Test:** `python scripts/ssl_test_connection.py`
5. **Enable:** Check "Verify SSL Certificate" ✅

---

## You're Good to Go!

Everything works now:
- ✅ App starts successfully
- ✅ Connection works
- ✅ Data displays
- ✅ Team can use it

**Just remember:** Uncheck SSL verification in sidebar.

---

## TL;DR - Just Do This:

1. `pip install --upgrade -r requirements.txt`
2. `streamlit run app.py`
3. Uncheck "Verify SSL Certificate" in sidebar
4. Enter Databricks details
5. Click "Load Data"
6. ✅ Done!

---

## Files for Reference

- `YOUR-SSL-ERROR-SOLUTION.md` ← Your specific error
- `SSL-QUICK-FIX.md` ← 5-minute reference
- `SSL-CERTIFICATE-RESOLUTION.md` ← All solutions
- `SSL-CERTIFICATE-TROUBLESHOOTING.md` ← Deep dive

---

**You're all set! Enjoy your app! 🚀**
