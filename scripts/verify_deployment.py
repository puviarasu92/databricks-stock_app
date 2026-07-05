#!/usr/bin/env python3
"""
Verify Databricks app deployment
Check if all files were uploaded correctly
"""
import argparse
import sys

from databricks.sdk import WorkspaceClient


def verify_deployment(
    host: str,
    token: str,
    workspace_path: str,
    app_name: str = "databricks-gold-table-viewer"
) -> bool:
    """Verify that the app was deployed correctly"""
    try:
        print("=" * 70)
        print("🔍 Verifying Databricks App Deployment")
        print("=" * 70)
        
        print(f"\n🔌 Connecting to Databricks workspace...")
        print(f"   Host: {host}")
        print(f"   Workspace path: {workspace_path}")
        
        # Initialize Databricks client
        client = WorkspaceClient(host=f"https://{host}", token=token)
        
        # Test connection with SDK-compatible current user endpoint
        user = client.current_user.me()
        print(f"✅ Connected as: {user.user_name}")
        
        # Check uploaded files
        workspace_app_path = f"/Workspace/Users/{workspace_path}/{app_name}"
        print(f"\n📂 Checking workspace path: {workspace_app_path}")
        
        required_files = [
            "app.py",
            "app_env.py",
            "config.py",
            "requirements.txt",
            "config.toml",
        ]
        
        files_found = 0
        files_missing = []
        
        for file in required_files:
            file_path = f"{workspace_app_path}/{file}"
            try:
                # Try to get file status
                status = client.workspace.get_status(file_path)
                if status:
                    print(f"  ✓ {file} (size: {status.size} bytes)")
                    files_found += 1
            except Exception:
                files_missing.append(file)
        
        print(f"\n📊 Deployment Status:")
        print(f"   Files found: {files_found}/{len(required_files)}")
        
        if files_missing:
            print(f"   ⚠ Missing files: {', '.join(files_missing)}")
        
        # Success if all required files are found
        if files_found == len(required_files):
            print("\n" + "=" * 70)
            print("✅ Deployment verification successful!")
            print("=" * 70)
            print(f"\n📋 Next steps:")
            print(f"   1. Navigate to your Databricks workspace")
            print(f"   2. Create a Databricks app from {workspace_app_path}")
            print(f"   3. Configure the app to use app.py or app_env.py")
            print(f"   4. Deploy and test the app")
            return True
        else:
            print("\n" + "=" * 70)
            print("⚠ Partial deployment - some files are missing")
            print("=" * 70)
            return False
        
    except Exception as e:
        print(f"\n❌ Verification failed: {str(e)}")
        print("=" * 70)
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Verify Databricks Gold Table Viewer deployment"
    )
    parser.add_argument("--host", required=True, help="Databricks host")
    parser.add_argument("--token", required=True, help="Databricks API token")
    parser.add_argument("--workspace-path", required=True, help="Databricks workspace path")
    parser.add_argument("--app-name", default="databricks-gold-table-viewer", help="App name")
    
    args = parser.parse_args()
    
    success = verify_deployment(
        host=args.host,
        token=args.token,
        workspace_path=args.workspace_path,
        app_name=args.app_name
    )
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
