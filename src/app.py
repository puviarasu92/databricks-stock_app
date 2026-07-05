import os
import ssl
import urllib3
import streamlit as st
import pandas as pd
from databricks import sql


def detect_date_column(columns):
    """Return the best matching date column name from the dataset."""
    preferred = ["date", "trade_date", "business_date", "timestamp", "event_time", "datetime"]
    col_map = {c.lower(): c for c in columns}
    for name in preferred:
        if name in col_map:
            return col_map[name]
    return None

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

# Filter and display loaded data
if st.session_state.loaded_df is not None:
    df = st.session_state.loaded_df.copy()

    st.sidebar.header("Data Filters")

    requested_filters = [
        ("symbol", "Symbol"),
        ("instrument", "Instrument"),
        ("exchange_segment", "Exchange Segment"),
    ]
    selected_values = {}
    column_map = {c.lower(): c for c in df.columns}

    for logical_name, label in requested_filters:
        actual_col = column_map.get(logical_name)
        if actual_col:
            options = ["All"] + sorted(df[actual_col].dropna().astype(str).unique().tolist())
            selected_values[actual_col] = st.sidebar.selectbox(
                label,
                options,
                key=f"filter_{logical_name}"
            )

    date_col = detect_date_column(df.columns)
    from_date = None
    to_date = None
    if date_col:
        parsed_dates = pd.to_datetime(df[date_col], errors="coerce").dropna()
        if not parsed_dates.empty:
            min_date = parsed_dates.min().date()
            max_date = parsed_dates.max().date()
            from_date = st.sidebar.date_input("From Date", value=min_date, min_value=min_date, max_value=max_date)
            to_date = st.sidebar.date_input("To Date", value=max_date, min_value=min_date, max_value=max_date)

    filtered_df = df
    for col, value in selected_values.items():
        if value != "All":
            filtered_df = filtered_df[filtered_df[col].astype(str) == value]

    if date_col and from_date and to_date:
        if from_date > to_date:
            st.warning("From Date is greater than To Date. Showing empty result.")
            filtered_df = filtered_df.iloc[0:0]
        else:
            parsed = pd.to_datetime(filtered_df[date_col], errors="coerce")
            filtered_df = filtered_df[parsed.dt.date.between(from_date, to_date)]

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Filtered Rows", len(filtered_df))
    with col2:
        st.metric("Total Columns", len(filtered_df.columns))

    st.markdown("### Data Preview")
    st.dataframe(filtered_df, use_container_width=True)

    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name=f"{st.session_state.loaded_table.replace('.', '_')}_filtered_data.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.sidebar.markdown(
    """
    ### 📖 Help
    1. Enter your Databricks connection details
    2. Specify the table name (catalog.schema.table)
    3. Click "Load Data" to fetch rows
    4. Use Symbol/Instrument/Exchange Segment/date filters
    5. Use the download button to export filtered data as CSV
    """
)
