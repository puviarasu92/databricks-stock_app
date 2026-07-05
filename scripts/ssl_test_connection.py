"""
Test script to verify Databricks connection
Run this before running the main app to ensure your credentials are correct
Handles SSL certificate verification issues
"""
import os
import sys
import ssl
import urllib3
from databricks import sql


def test_connection_with_ssl(server_hostname, http_path, personal_access_token, verify_ssl=True):
    """Test connection to Databricks with optional SSL verification"""
    try:
        if not verify_ssl:
            # Disable SSL verification for this connection
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            os.environ['PYTHONHTTPSVERIFY'] = '0'
            ssl._create_default_https_context = ssl._create_unverified_context
            ssl_status = "WITHOUT SSL verification"
        else:
            ssl_status = "with SSL verification"
        
        print(f"🔗 Testing connection {ssl_status}...")
        print(f"   Host: {server_hostname}")
        
        connection = sql.connect(
            server_hostname=server_hostname,
            http_path=http_path,
            personal_access_token=personal_access_token,
            _tls_no_verify=not verify_ssl,
        )
        print("✅ Connection successful!")
        
        # Test query
        print("\n📊 Testing simple query...")
        cursor = connection.cursor()
        cursor.execute("SELECT 1 as test_column")
        result = cursor.fetchone()
        print(f"✅ Query successful! Result: {result}")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        error_msg = str(e)
        if "SSL" in error_msg or "CERTIFICATE" in error_msg:
            print(f"❌ SSL Certificate Error: {error_msg[:100]}...")
            return False
        else:
            print(f"❌ Connection failed: {error_msg[:100]}...")
            return False


def test_table_access(server_hostname, http_path, personal_access_token, table_name, verify_ssl=True):
    """Test access to a specific table"""
    try:
        if not verify_ssl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            os.environ['PYTHONHTTPSVERIFY'] = '0'
            ssl._create_default_https_context = ssl._create_unverified_context
        
        print(f"\n📋 Testing access to table: {table_name}")
        connection = sql.connect(
            server_hostname=server_hostname,
            http_path=http_path,
            personal_access_token=personal_access_token,
            _tls_no_verify=not verify_ssl,
        )
        
        cursor = connection.cursor()
        cursor.execute(f"SELECT COUNT(*) as row_count FROM {table_name}")
        result = cursor.fetchone()
        print(f"✅ Table access successful! Row count: {result[0]}")
        
        # Get column info
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
        columns = [desc[0] for desc in cursor.description]
        print(f"✅ Columns: {', '.join(columns)}")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Table access failed: {str(e)[:100]}...")
        return False


def main():
    """Main test function"""
    print("=" * 60)
    print("🔐 Databricks Connection Test (with SSL Troubleshooting)")
    print("=" * 60)
    
    # Get user input
    print("\nPlease enter your Databricks connection details:")
    print("(Leave empty to skip or load from environment variables)\n")
    
    server_hostname = input("Server Hostname: ").strip()
    http_path = input("HTTP Path: ").strip()
    personal_access_token = input("Personal Access Token (hidden): ").strip()
    
    if not all([server_hostname, http_path, personal_access_token]):
        print("\n⚠️  Missing required credentials. Exiting.")
        sys.exit(1)
    
    # Try with SSL verification first
    print("\n" + "-" * 60)
    print("ATTEMPT 1: Testing WITH SSL verification (recommended)")
    print("-" * 60)
    ssl_success = test_connection_with_ssl(
        server_hostname, 
        http_path, 
        personal_access_token, 
        verify_ssl=True
    )
    
    # If SSL fails, try without
    if not ssl_success:
        print("\n⚠️  SSL verification failed. Trying WITHOUT SSL verification...")
        print("\n" + "-" * 60)
        print("ATTEMPT 2: Testing WITHOUT SSL verification (for corporate proxy)")
        print("-" * 60)
        no_ssl_success = test_connection_with_ssl(
            server_hostname, 
            http_path, 
            personal_access_token, 
            verify_ssl=False
        )
        
        if no_ssl_success:
            print("\n" + "!" * 60)
            print("⚠️  SSL Verification Issue Detected!")
            print("!" * 60)
            print("\nYour environment has SSL certificate verification issues.")
            print("\nRECOMMENDED SOLUTIONS:")
            print("1. 🎯 Use the app with 'Verify SSL Certificate' unchecked")
            print("2. 📖 Read: SSL-CERTIFICATE-TROUBLESHOOTING.md")
            print("3. 🔧 Update Python certificates:")
            print("   pip install --upgrade certifi")
            print("4. 🏢 If corporate: Contact IT about CA certificates\n")
            return 1
    
    # Test table access if connection successful
    if ssl_success or no_ssl_success:
        print("\n" + "-" * 60)
        test_table_access_opt = input("\nTest table access? (y/n): ").strip().lower()
        if test_table_access_opt == 'y':
            table_name = input("Enter table name (catalog.schema.table): ").strip()
            if table_name:
                verify_ssl = ssl_success  # Use SSL if it worked
                test_table_access(
                    server_hostname, 
                    http_path, 
                    personal_access_token, 
                    table_name,
                    verify_ssl=verify_ssl
                )
    
    print("\n" + "=" * 60)
    print("✅ Connection tests completed!")
    print("=" * 60)
    print("\n📋 Next steps:")
    print("1. Run: streamlit run app.py")
    print("2. If SSL error: uncheck 'Verify SSL Certificate' in sidebar")
    print("3. Enter your connection details")
    print("4. Click 'Load Data'\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
