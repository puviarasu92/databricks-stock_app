#!/usr/bin/env python3
"""
SSL Certificate Update & Diagnostic Script
Helps fix SSL certificate verification errors
"""
import os
import sys
import platform
import subprocess
import ssl


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def get_python_info():
    """Get Python installation information"""
    print_section("Python Environment Information")
    
    print(f"Python Version: {sys.version}")
    print(f"Python Executable: {sys.executable}")
    print(f"Platform: {platform.platform()}")
    print(f"Architecture: {platform.machine()}")
    
    # Check certifi
    try:
        import certifi
        print(f"Certifi Location: {certifi.where()}")
        print(f"Certifi Version: {certifi.__version__}")
    except ImportError:
        print("⚠️  certifi not installed")
    
    # Check SSL
    print(f"\nSSL Version: {ssl.OPENSSL_VERSION}")
    print(f"SSL Version Info: {ssl.OPENSSL_VERSION_INFO}")


def check_ssl_context():
    """Check SSL context configuration"""
    print_section("SSL Context Information")
    
    try:
        ctx = ssl.create_default_context()
        print(f"Default Context Check Hostname: {ctx.check_hostname}")
        print(f"Default Context Verify Mode: {ctx.verify_mode}")
        print(f"Default Context CA Certs: {ctx.ca_certs}")
        
        # Try to load default certificates
        default_certs = ssl.get_default_verify_paths()
        print(f"\nDefault CA File: {default_certs.cafile}")
        print(f"Default CA Path: {default_certs.capath}")
        print(f"OpenSSL CA File Env: {default_certs.openssl_cafile_env}")
        print(f"OpenSSL CA Path Env: {default_certs.openssl_capath_env}")
        
    except Exception as e:
        print(f"⚠️  Error checking SSL context: {str(e)}")


def update_certifi():
    """Update certifi package"""
    print_section("Updating Certifi (CA Certificates)")
    
    print("Installing/upgrading certifi...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "certifi"],
            check=True
        )
        print("✅ Certifi updated successfully")
        
        # Show new location
        import certifi
        print(f"New Certifi Location: {certifi.where()}")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to update certifi: {str(e)}")
        return False


def update_system_certificates():
    """Guide for updating system certificates"""
    print_section("System Certificate Updates")
    
    system = platform.system()
    
    if system == "Darwin":  # macOS
        print("macOS - Run the following command:")
        print("/Applications/Python\\ 3.x/Install\\ Certificates.command")
        print("\nOr:")
        print("python -m pip install --upgrade certifi")
        
    elif system == "Windows":
        print("Windows - Run as Administrator:")
        print("python -m pip install --upgrade certifi")
        print("\nOr download from: https://www.python.org/downloads/")
        
    elif system == "Linux":
        print("Linux - Run:")
        print("sudo apt-get install ca-certificates")
        print("# or")
        print("python -m pip install --upgrade certifi")


def test_connection_simple():
    """Test simple connection"""
    print_section("Testing HTTPS Connection")
    
    try:
        import urllib3
        http = urllib3.PoolManager()
        r = http.request('GET', 'https://www.python.org', timeout=10)
        print(f"✅ HTTPS connection successful (Status: {r.status})")
        return True
    except Exception as e:
        error = str(e)
        if "SSL" in error or "CERTIFICATE" in error:
            print(f"❌ SSL Certificate Error: {error[:100]}")
        else:
            print(f"❌ Connection failed: {error[:100]}")
        return False


def set_ssl_env_vars():
    """Print environment variable settings"""
    print_section("SSL Environment Variables")
    
    print("To temporarily disable SSL verification (testing only):")
    
    if platform.system() == "Windows":
        if sys.platform == "win32" and "PowerShell" in os.environ.get("PROMPT", ""):
            print("\nPowerShell:")
            print("$env:PYTHONHTTPSVERIFY = '0'")
        else:
            print("\nCommand Prompt:")
            print("set PYTHONHTTPSVERIFY=0")
    else:
        print("\nBash/Zsh:")
        print("export PYTHONHTTPSVERIFY=0")
    
    print("\n⚠️  Note: Only for testing. Fix certificates for production.")


def diagnose_ssl():
    """Run complete SSL diagnostic"""
    print_section("SSL Diagnostic Report")
    
    # Get certificate paths
    cert_paths = ssl.get_default_verify_paths()
    print("Certificate Paths:")
    print(f"  CA File: {cert_paths.cafile}")
    print(f"  CA Path: {cert_paths.capath}")
    
    # Check if paths exist
    if cert_paths.cafile and os.path.exists(cert_paths.cafile):
        print(f"  ✅ CA File exists")
    else:
        print(f"  ❌ CA File missing")
    
    if cert_paths.capath and os.path.exists(cert_paths.capath):
        print(f"  ✅ CA Path exists")
    else:
        print(f"  ❌ CA Path missing")
    
    # Environment variables
    print("\nEnvironment Variables:")
    cafile_env = os.environ.get('SSL_CERT_FILE', 'Not set')
    capath_env = os.environ.get('SSL_CERT_DIR', 'Not set')
    print(f"  SSL_CERT_FILE: {cafile_env}")
    print(f"  SSL_CERT_DIR: {capath_env}")


def main():
    """Main function"""
    print("\n" + "🔐" * 35)
    print("SSL CERTIFICATE DIAGNOSTIC & FIX TOOL")
    print("🔐" * 35)
    
    # Collect diagnostics
    get_python_info()
    check_ssl_context()
    diagnose_ssl()
    test_connection_simple()
    
    # Show options
    print_section("Available Actions")
    print("""
1. Update Certifi (CA Certificates)
2. View System Certificate Update Instructions
3. View Environment Variable Settings
4. Exit
    """)
    
    try:
        choice = input("Select an option (1-4): ").strip()
        
        if choice == "1":
            update_certifi()
            print("\n✅ Run this to verify fix:")
            print("   python scripts/ssl_test_connection.py")
            
        elif choice == "2":
            update_system_certificates()
            
        elif choice == "3":
            set_ssl_env_vars()
            
        elif choice == "4":
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid option")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    
    print_section("Next Steps")
    print("""
1. Test the connection:
   python scripts/ssl_test_connection.py

2. Try the app:
   streamlit run app.py

3. If still having issues:
   - Uncheck 'Verify SSL Certificate' in app sidebar
   - Read: SSL-CERTIFICATE-TROUBLESHOOTING.md
   - Contact your IT department
    """)


if __name__ == "__main__":
    main()
