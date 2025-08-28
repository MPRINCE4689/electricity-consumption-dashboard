#!/usr/bin/env python3
"""
Test Script for Electricity Dashboard Setup
This script tests if all required packages are installed correctly.
"""

import sys
import subprocess

def test_package_import(package_name, import_name=None):
    """Test if a package can be imported"""
    if import_name is None:
        import_name = package_name

    try:
        __import__(import_name)
        print(f"✅ {package_name} - Successfully imported")
        return True
    except ImportError as e:
        print(f"❌ {package_name} - Import failed: {e}")
        return False

def test_python_version():
    """Test Python version compatibility"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 7:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Not compatible (Need 3.7+)")
        return False

def test_streamlit_command():
    """Test if streamlit command is available"""
    try:
        result = subprocess.run(['streamlit', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ Streamlit command - Available ({result.stdout.strip()})")
            return True
        else:
            print("❌ Streamlit command - Not available")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Streamlit command - Not found in PATH")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Electricity Dashboard Setup")
    print("=" * 50)

    all_tests_passed = True

    # Test Python version
    if not test_python_version():
        all_tests_passed = False

    print()

    # Test package imports
    packages = [
        ('streamlit', 'streamlit'),
        ('pandas', 'pandas'),
        ('plotly', 'plotly'),
        ('numpy', 'numpy'),
        ('openpyxl', 'openpyxl')
    ]

    print("Testing package imports:")
    for package, import_name in packages:
        if not test_package_import(package, import_name):
            all_tests_passed = False

    print()

    # Test streamlit command
    print("Testing Streamlit command:")
    if not test_streamlit_command():
        all_tests_passed = False

    print()
    print("=" * 50)

    if all_tests_passed:
        print("🎉 All tests passed! Your setup is ready.")
        print("\nTo run the dashboard:")
        print("streamlit run electricity_dashboard.py")
    else:
        print("❌ Some tests failed. Please check the installation guide.")
        print("\nCommon solutions:")
        print("1. Make sure virtual environment is activated")
        print("2. Run: pip install -r requirements.txt")
        print("3. Check Python PATH configuration")

if __name__ == "__main__":
    main()
