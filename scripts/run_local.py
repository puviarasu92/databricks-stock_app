#!/usr/bin/env python3
"""
Local deployment script for testing
Deploy the app locally using Streamlit
"""
import argparse
import subprocess
import sys
from pathlib import Path


def check_dependencies():
    """Check if all dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    try:
        import streamlit
        print("✓ streamlit")
    except ImportError:
        print("✗ streamlit not found")
        return False
    
    try:
        from databricks import sql
        print("✓ databricks-sql-connector")
    except ImportError:
        print("✗ databricks-sql-connector not found")
        return False
    
    return True


def run_local_app(app_file: str = "src/app.py"):
    """Run the Streamlit app locally"""
    print(f"\n🚀 Starting Streamlit app: {app_file}")
    print("=" * 70)
    
    if not Path(app_file).exists():
        print(f"❌ File not found: {app_file}")
        print(f"   Current directory: {Path.cwd()}")
        print(f"   Expected file at: {Path(app_file).resolve()}")
        return False
    
    try:
        subprocess.run(
            ["streamlit", "run", app_file],
            check=False
        )
        return True
    except Exception as e:
        print(f"❌ Failed to start app: {str(e)}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Run Databricks Gold Table Viewer locally"
    )
    parser.add_argument(
        "--app",
        default="app.py",
        choices=["app.py", "app_env.py"],
        help="Which app file to run"
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("🎯 Local Deployment - Streamlit App")
    print("=" * 70)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Missing dependencies!")
        print("Install them with: pip install -r requirements.txt")
        return 1
    
    print("✅ All dependencies installed")
    
    # Run app
    if not run_local_app(args.app):
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
