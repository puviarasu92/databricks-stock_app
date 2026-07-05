"""
Test script to verify Databricks connection
Run this before running the main app to ensure your credentials are correct
"""
import sys
from databricks import sql


def test_connection(server_hostname, http_path, personal_access_token):
    """Test connection to Databricks"""
    try:
        print(f"🔗 Testing connection to: {server_hostname}")
        connection = sql.connect(
            server_hostname=server_hostname,
            http_path=http_path,
            personal_access_token=personal_access_token,
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
        print(f"❌ Connection failed: {str(e)}")
        return False


def test_table_access(server_hostname, http_path, personal_access_token, table_name):
    """Test access to a specific table"""
    try:
        print(f"\n📋 Testing access to table: {table_name}")
        connection = sql.connect(
            server_hostname=server_hostname,
            http_path=http_path,
            personal_access_token=personal_access_token,
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
        print(f"❌ Table access failed: {str(e)}")
        return False


def main():
    """Main test function"""
    print("=" * 60)
    print("Databricks Connection Test")
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
    
    # Test connection
    print("\n" + "-" * 60)
    if not test_connection(server_hostname, http_path, personal_access_token):
        sys.exit(1)
    
    # Test table access (optional)
    print("\n" + "-" * 60)
    test_table_access_opt = input("\nTest table access? (y/n): ").strip().lower()
    if test_table_access_opt == 'y':
        table_name = input("Enter table name (catalog.schema.table): ").strip()
        if table_name:
            test_table_access(server_hostname, http_path, personal_access_token, table_name)
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
