# Quick Start Guide

## Setup Instructions

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Configure Your Connection

#### Option A: Using Manual Input (Quick Start)
Run the app and enter your credentials in the sidebar:

```bash
streamlit run app.py
```

#### Option B: Using Environment Variables (Recommended)
1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your Databricks credentials:
   ```
   SERVER_HOSTNAME=your_workspace.cloud.databricks.com
   HTTP_PATH=/sql/1.0/warehouses/your_warehouse_id
   PERSONAL_ACCESS_TOKEN=your_pat_token_here
   TABLE_NAME=your_catalog.your_schema.your_table
   MAX_ROWS=100
   ```

3. Run the environment-based app:
   ```bash
   streamlit run app_env.py
   ```

### Step 3: Access the App

The app will automatically open in your browser at `http://localhost:8501`

---

## Finding Your Connection Details

### 1. Server Hostname
- Go to your Databricks workspace
- Look at the URL: `https://example.cloud.databricks.com`
- Copy just the hostname part: `example.cloud.databricks.com`

### 2. HTTP Path
- **For SQL Warehouse:**
  - Go to SQL Warehouses
  - Select your warehouse
  - Click "Connection details"
  - Copy the "HTTP path" value
  
- **For Compute Cluster:**
  - Go to Compute
  - Select your cluster
  - Click "Connection details"
  - Copy the "HTTP path" value

### 3. Personal Access Token (PAT)
- Click your username → User settings
- Go to Developer → Personal access tokens
- Click "Generate new token"
- Give it a name and expiration (e.g., 90 days)
- Copy the token immediately (you won't see it again!)

### 4. Table Name
- Format: `catalog_name.schema_name.table_name`
- Example: `main.default.gold_sales`
- You can find this in the Databricks workspace by browsing tables

---

## App Features

### Data Display
- View any table from your Databricks workspace
- See data in an interactive, sortable table
- Display up to 10,000 rows at a time

### Data Export
- Download displayed data as CSV
- Use for further analysis in Excel, Python, etc.

### Data Statistics
- View column information
- See data types
- Count non-null values per column

---

## Troubleshooting

### Error: "Could not connect to Databricks"
- Check your server hostname (no trailing slashes)
- Verify your HTTP path starts with `/sql/1.0/...`
- Ensure your PAT token is valid (not expired)

### Error: "Table not found"
- Use full path: `catalog.schema.table_name`
- Verify the table exists in your workspace
- Check spelling and capitalization

### Error: "Permission denied"
- Verify your PAT token has appropriate permissions
- Check table access permissions in your workspace

### App runs slowly
- Reduce the "Max Rows to Display" setting
- Run a query on a smaller table first to test
- Check your SQL warehouse/cluster is running

---

## Tips & Best Practices

1. **Keep credentials secure**
   - Never commit `.env` to Git
   - `.env` is already in `.gitignore`
   - Rotate your PAT tokens regularly

2. **Performance**
   - Use reasonable row limits for large tables
   - Filter data at the Databricks level if possible

3. **Testing**
   - Start with small tables first
   - Test connectivity before deploying

4. **Production Deployment**
   - Use Databricks Apps feature for sharing
   - Use workspace-level secrets for credentials
   - Enable SSL/TLS for all connections

---

## Next Steps

- Explore other tables in your workspace
- Share the app with team members
- Deploy to Databricks Apps for wider access
- Customize the app for specific use cases
