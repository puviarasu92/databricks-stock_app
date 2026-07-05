import os
import ssl
import urllib3
import streamlit as st
import pandas as pd
from databricks import sql

# Suppress SSL warnings if verification is disabled
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Page configuration
st.set_page_config(
    page_title="Databricks Gold Table Viewer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Gold Table Viewer")
st.markdown("---")

# Sidebar configuration
st.sidebar.header("Connection Settings")

server_hostname = st.sidebar.text_input(
    "Server Hostname",
    placeholder="example.cloud.databricks.com",
    help="Your Databricks workspace hostname"
)

http_path = st.sidebar.text_input(
    "HTTP Path",
    placeholder="/sql/1.0/warehouses/xxxxxxx",
    help="SQL Warehouse or cluster HTTP path"
)

personal_access_token = st.sidebar.text_input(
    "Personal Access Token",
    type="password",
    help="Your Databricks PAT (keep this secret!)"
)

table_name = st.sidebar.text_input(
    "Table Name",
    placeholder="gold_table",
    help="Enter the full table path (e.g., catalog.schema.table)"
)

max_rows = st.sidebar.number_input(
    "Max Rows to Display",
    min_value=10,
    max_value=10000,
    value=100,
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

# Query and display data
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
                )
            
            with st.spinner(f"Loading data from {table_name}..."):
                cursor = connection.cursor()
                cursor.execute(f"SELECT * FROM {table_name} LIMIT {max_rows}")
                results = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                cursor.close()
                connection.close()
            
            # Display data
            st.success(f"✅ Successfully loaded {len(results)} rows")
            
            # Display in table format
            df = pd.DataFrame(results, columns=columns)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Rows", len(results))
            with col2:
                st.metric("Total Columns", len(columns))
            
            st.markdown("### Data Preview")
            st.dataframe(df, use_container_width=True)
            
            # Download option
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name=f"{table_name.replace('.', '_')}_data.csv",
                mime="text/csv"
            )
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("Please check your connection settings and try again.")

# Footer
st.markdown("---")
st.sidebar.markdown(
    """
    ### 📖 Help
    1. Enter your Databricks connection details
    2. Specify the table name (catalog.schema.table)
    3. Click "Load Data" to fetch and display rows
    4. Use the download button to export as CSV
    """
)
