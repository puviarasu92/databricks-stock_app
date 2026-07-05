"""
Databricks Gold Table Viewer - Environment Variables Version
This version uses .env file for configuration (more secure for production)
"""
import os
import ssl
import urllib3
import streamlit as st
import pandas as pd
from databricks import sql
from config import (
    DATABRICKS_SERVER_HOSTNAME,
    DATABRICKS_HTTP_PATH,
    DATABRICKS_PAT,
    TABLE_NAME,
    APP_TITLE,
    APP_DESCRIPTION,
    DEFAULT_MAX_ROWS,
    MAX_ALLOWED_ROWS,
    MIN_ALLOWED_ROWS
)

# Suppress SSL warnings if verification is disabled
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title(f"📊 {APP_TITLE}")
st.markdown(APP_DESCRIPTION)
st.markdown("---")

st.subheader("Filter Controls (UI Only)")
ui_col1, ui_col2, ui_col3 = st.columns(3)
with ui_col1:
    st.selectbox("Symbol", ["All", "NIFTY", "BANKNIFTY", "RELIANCE"], key="ui_symbol")
with ui_col2:
    st.selectbox("Instrument", ["All", "EQ", "FUT", "OPT"], key="ui_instrument")
with ui_col3:
    st.selectbox("Exchange Segment", ["All", "NSE", "BSE", "NFO"], key="ui_exchange_segment")

date_col1, date_col2 = st.columns(2)
with date_col1:
    st.date_input("From Date", key="ui_from_date")
with date_col2:
    st.date_input("To Date", key="ui_to_date")

st.caption("These controls are UI-only and do not filter backend query results.")
st.markdown("---")

# Sidebar configuration
st.sidebar.header("Connection Settings")

# Use environment variables with fallback to input fields
server_hostname = st.sidebar.text_input(
    "Server Hostname",
    value=DATABRICKS_SERVER_HOSTNAME,
    placeholder="example.cloud.databricks.com",
    help="Your Databricks workspace hostname"
)

http_path = st.sidebar.text_input(
    "HTTP Path",
    value=DATABRICKS_HTTP_PATH,
    placeholder="/sql/1.0/warehouses/xxxxxxx",
    help="SQL Warehouse or cluster HTTP path"
)

personal_access_token = st.sidebar.text_input(
    "Personal Access Token",
    value=DATABRICKS_PAT,
    type="password",
    help="Your Databricks PAT (keep this secret!)"
)

table_name = st.sidebar.text_input(
    "Table Name",
    value=TABLE_NAME,
    placeholder="gold_table",
    help="Enter the full table path (e.g., catalog.schema.table)"
)

max_rows = st.sidebar.number_input(
    "Max Rows to Display",
    min_value=MIN_ALLOWED_ROWS,
    max_value=MAX_ALLOWED_ROWS,
    value=DEFAULT_MAX_ROWS,
    step=10
)

# SSL/TLS Configuration
st.sidebar.markdown("---")
st.sidebar.subheader("🔐 SSL/TLS Settings")
verify_ssl = st.sidebar.checkbox(
    "Verify SSL Certificate",
    value=True,
    help="Disable if you get SSL certificate errors (corporate proxy)"
)

if not verify_ssl:
    st.sidebar.warning(
        "⚠️ SSL verification disabled. Use only for testing!"
    )

st.sidebar.markdown("---")

# Keep loaded data across reruns so filters remain interactive.
if "loaded_df" not in st.session_state:
    st.session_state.loaded_df = None
if "loaded_table" not in st.session_state:
    st.session_state.loaded_table = ""

# Query and store data
if st.sidebar.button("Load Data", use_container_width=True):
    if not all([server_hostname, http_path, personal_access_token, table_name]):
        st.error("❌ Please fill in all connection settings.")
    else:
        try:
            # Configure SSL verification
            if not verify_ssl:
                # Disable SSL verification for testing
                os.environ['PYTHONHTTPSVERIFY'] = '0'
                import ssl
                ssl._create_default_https_context = ssl._create_unverified_context
            
            with st.spinner("Connecting to Databricks..."):
                connection = sql.connect(
                    server_hostname=server_hostname,
                    http_path=http_path,
                    personal_access_token=personal_access_token,
                    _tls_no_verify=not verify_ssl,
                )
            
            with st.spinner(f"Loading data from {table_name}..."):
                cursor = connection.cursor()
                cursor.execute(f"SELECT * FROM {table_name} LIMIT {max_rows}")
                results = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                cursor.close()
                connection.close()
            st.session_state.loaded_df = pd.DataFrame(results, columns=columns)
            st.session_state.loaded_table = table_name

            st.success(f"✅ Successfully loaded {len(results)} rows")
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("Please check your connection settings and try again.")

# Display loaded data
if st.session_state.loaded_df is not None:
    df = st.session_state.loaded_df.copy()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Rows", len(df))
    with col2:
        st.metric("Total Columns", len(df.columns))

    st.markdown("### Data Preview")
    st.dataframe(df, use_container_width=True)

    with st.expander("📈 Data Statistics"):
        st.write("**Column Information:**")
        col_info = pd.DataFrame({
            "Column": df.columns,
            "Type": [str(df[col].dtype) for col in df.columns],
            "Non-Null": [df[col].notna().sum() for col in df.columns]
        })
        st.dataframe(col_info, use_container_width=True)

    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name=f"{st.session_state.loaded_table.replace('.', '_')}_data.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.sidebar.markdown(
    """
    ### 📖 Help
    1. Enter your Databricks connection details (or use .env file)
    2. Specify the table name (catalog.schema.table)
    3. Click "Load Data" to fetch rows
    4. UI-only filters are shown above the table preview
    5. Use the download button to export data as CSV
    
    ### Configuration
    - Use `.env` file for secure credential storage
    - Copy `.env.example` to `.env` and fill in your values
    """
)
