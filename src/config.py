"""
Configuration module for Databricks Gold Table Viewer
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Databricks Configuration
DATABRICKS_SERVER_HOSTNAME = os.getenv("SERVER_HOSTNAME", "")
DATABRICKS_HTTP_PATH = os.getenv("HTTP_PATH", "")
DATABRICKS_PAT = os.getenv("PERSONAL_ACCESS_TOKEN", "")
TABLE_NAME = os.getenv("TABLE_NAME", "")
MAX_ROWS = int(os.getenv("MAX_ROWS", "100"))

# App Configuration
APP_TITLE = "Databricks Gold Table Viewer"
APP_DESCRIPTION = "Display rows from Databricks gold tables in interactive table format"
DEFAULT_MAX_ROWS = 100
MAX_ALLOWED_ROWS = 10000
MIN_ALLOWED_ROWS = 10

# Table Configuration
TABLES_CATALOG = os.getenv("CATALOG", "")
TABLES_SCHEMA = os.getenv("SCHEMA", "")
