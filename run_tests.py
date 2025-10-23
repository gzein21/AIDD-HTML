#!/usr/bin/env python3
"""
Test runner script for the Flask application.
This script runs all tests and provides detailed output.
"""

import sys
import subprocess
import os
from pathlib import Path


def run_tests():
    """Run all tests using pytest"""
    print("=" * 60)
    print("Running Automated Tests for Flask Application")
    print("=" * 60)
    
    # Check if pytest is installed
    try:
        import pytest
    except ImportError:
        print("ERROR: pytest is not installed. Please install it first:")
        print("pip install pytest")
        return False
    
    # Get the directory containing this script
    script_dir = Path(__file__).parent
    
    # Run tests with verbose output
    test_files = [
        str(script_dir / "test_dal.py"),
        str(script_dir / "test_app.py")
    ]
    
    # Check if test files exist
    missing_files = [f for f in test_files if not os.path.exists(f)]
    if missing_files:
        print(f"ERROR: Test files not found: {missing_files}")
        return False
    
    # Run pytest
    cmd = [
        sys.executable, "-m", "pytest",
        "-v",  # verbose output
        "--tb=short",  # shorter traceback format
        "--color=yes",  # colored output
        *test_files
    ]
    
    print(f"Running command: {' '.join(cmd)}")
    print("-" * 60)
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print("-" * 60)
        print("✅ All tests passed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print("-" * 60)
        print(f"❌ Tests failed with exit code {e.returncode}")
        return False
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False


def run_coverage():
    """Run tests with coverage report"""
    print("\n" + "=" * 60)
    print("Running Tests with Coverage Report")
    print("=" * 60)
    
    # Check if coverage is installed
    try:
        import coverage
    except ImportError:
        print("Coverage not installed. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "coverage"], check=True)
    
    # Run tests with coverage
    cmd = [
        sys.executable, "-m", "coverage", "run", "-m", "pytest",
        "test_dal.py", "test_app.py", "-v"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        
        # Generate coverage report
        subprocess.run([sys.executable, "-m", "coverage", "report"], check=True)
        subprocess.run([sys.executable, "-m", "coverage", "html"], check=True)
        
        print("\n✅ Coverage report generated successfully!")
        print("📊 HTML coverage report available in htmlcov/index.html")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Coverage tests failed: {e}")
        return False


def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == "--coverage":
        success = run_coverage()
    else:
        success = run_tests()
    
    if success:
        print("\n🎉 Test execution completed successfully!")
        sys.exit(0)
    else:
        print("\n💥 Test execution failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
