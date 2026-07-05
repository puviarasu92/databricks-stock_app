#!/usr/bin/env python3
"""
Deploy Databricks Gold Table Viewer App to Databricks Workspace
This script uploads the app files to a Databricks workspace
"""
import argparse
import json
import os
import sys
import zipfile
from pathlib import Path

from databricks.sdk import WorkspaceClient


def build_workspace_app_path(workspace_path: str, app_name: str) -> str:
    """Build a stable Databricks workspace path for app uploads."""
    normalized = workspace_path.strip().strip("/")

    # Accept values like:
    # - your.email@company.com
    # - Users/your.email@company.com
    # - /Users/your.email@company.com
    # - /Workspace/Users/your.email@company.com
    if normalized.startswith("Workspace/"):
        normalized = normalized[len("Workspace/") :]
    if normalized.startswith("Users/"):
        normalized = normalized[len("Users/") :]

    return f"/Users/{normalized}/{app_name}"


def create_deployment_package(output_path: str) -> str:
    """Create a deployment package containing all necessary files"""
    print(f"📦 Creating deployment package...")
    
    package_path = Path(output_path) / "databricks-app.zip"
    
    # Files to include in the deployment package
    files_to_include = [
        "src/app.py",
        "src/app_env.py",
        "src/config.py",
        "requirements.txt",
        ".streamlit/config.toml",
    ]
    
    with zipfile.ZipFile(package_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files_to_include:
            if Path(file).exists():
                # Add file to zip with relative path (remove src/ prefix)
                arcname = file.replace('src/', '')
                zipf.write(file, arcname)
                print(f"  ✓ Added {file}")
            else:
                print(f"  ⚠ File not found: {file}")
    
    print(f"✅ Deployment package created: {package_path}")
    return str(package_path)


def upload_to_databricks(
    host: str,
    token: str,
    workspace_path: str,
    app_name: str
) -> bool:
    """Upload app files to Databricks workspace"""
    try:
        print(f"\n🔌 Connecting to Databricks workspace...")
        print(f"   Host: {host}")
        print(f"   Workspace path: {workspace_path}")
        
        # Initialize Databricks client
        client = WorkspaceClient(host=f"https://{host}", token=token)
        
        # Test connection with SDK-compatible current user endpoint
        user = client.current_user.me()
        print(f"✅ Connected as: {user.user_name}")
        
        # Upload directory structure
        print(f"\n📤 Uploading app to workspace...")
        
        workspace_app_path = build_workspace_app_path(workspace_path, app_name)
        print(f"   Destination path: {workspace_app_path}")

        # Ensure destination directory exists
        try:
            client.workspace.mkdirs(workspace_app_path)
        except Exception as e:
            print(f"  ⚠ Could not create directory {workspace_app_path}: {str(e)}")
        
        # Upload files
        files_to_upload = [
            ("src/app.py", "app.py"),
            ("src/app_env.py", "app_env.py"),
            ("src/config.py", "config.py"),
            ("requirements.txt", "requirements.txt"),
            (".streamlit/config.toml", "config.toml"),
        ]
        
        uploaded_count = 0

        for local_file, workspace_file in files_to_upload:
            if Path(local_file).exists():
                with open(local_file, 'rb') as f:
                    file_content = f.read()
                
                workspace_file_path = f"{workspace_app_path}/{workspace_file}"
                
                # Upload file using workspace filesystem
                try:
                    client.workspace.upload(
                        path=workspace_file_path,
                        contents=file_content,
                        overwrite=True
                    )
                    print(f"  ✓ Uploaded {local_file} → {workspace_file_path}")
                    uploaded_count += 1
                except Exception as e:
                    print(f"  ⚠ Could not upload {local_file}: {str(e)}")
        
        if uploaded_count == 0:
            print("❌ Upload failed: no files were uploaded")
            return False

        print(f"✅ App uploaded to Databricks workspace ({uploaded_count} files)")
        return True
        
    except Exception as e:
        print(f"❌ Upload failed: {str(e)}")
        return False


def create_deployment_info(
    host: str,
    workspace_path: str,
    app_name: str,
    output_dir: str = "."
) -> str:
    """Create a deployment info file"""
    info = {
        "app_name": app_name,
        "host": host,
        "workspace_path": workspace_path,
        "deployed_at": __import__('datetime').datetime.now().isoformat(),
        "instructions": {
            "launch_app": f"Visit: https://{host}/workspace{workspace_path}/{app_name}",
            "requirements": "Ensure your Databricks workspace has SQL Warehouse running"
        }
    }
    
    info_file = Path(output_dir) / "deployment_info.json"
    with open(info_file, 'w') as f:
        json.dump(info, f, indent=2)
    
    print(f"\n📋 Deployment info saved to: {info_file}")
    return str(info_file)


def main():
    parser = argparse.ArgumentParser(
        description="Deploy Databricks Gold Table Viewer to Databricks Workspace"
    )
    parser.add_argument("--host", required=True, help="Databricks host")
    parser.add_argument("--token", required=True, help="Databricks API token")
    parser.add_argument("--workspace-path", required=True, help="Databricks workspace path")
    parser.add_argument("--app-name", default="databricks-gold-table-viewer", help="App name")
    parser.add_argument("--output-dir", default=".", help="Output directory for artifacts")
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("🚀 Databricks App Deployment Script")
    print("=" * 70)
    
    # Create deployment package
    package_path = create_deployment_package(args.output_dir)
    
    # Upload to Databricks
    success = upload_to_databricks(
        host=args.host,
        token=args.token,
        workspace_path=args.workspace_path,
        app_name=args.app_name
    )
    
    if success:
        # Create deployment info
        create_deployment_info(
            host=args.host,
            workspace_path=args.workspace_path,
            app_name=args.app_name,
            output_dir=args.output_dir
        )
        print("\n" + "=" * 70)
        print("✅ Deployment completed successfully!")
        print("=" * 70)
        return 0
    else:
        print("\n" + "=" * 70)
        print("❌ Deployment failed!")
        print("=" * 70)
        return 1


if __name__ == "__main__":
    sys.exit(main())
