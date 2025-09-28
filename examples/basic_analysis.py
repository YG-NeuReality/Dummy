#!/usr/bin/env python3
"""
Basic Analysis Example

This example shows how to perform basic cryptocurrency analysis
for short trading opportunities using the Bitfinex trading tool.

Requirements:
- Configured .env file with Bitfinex API credentials
- Installed dependencies (pip install -r requirements.txt)
"""

import subprocess
import sys
import os

def run_basic_analysis():
    """Run basic analysis on default cryptocurrency symbols."""
    
    print("🔍 Basic Cryptocurrency Analysis Example")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('main.py'):
        print("❌ Please run this script from the project root directory")
        return False
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠️  No .env file found. Please copy .env.example to .env and configure it.")
        print("Example: cp .env.example .env")
        return False
    
    try:
        print("\n1. Analyzing default symbols (major cryptocurrencies)...")
        result = subprocess.run([
            sys.executable, 'main.py', 'analyze'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Analysis completed successfully!")
            print("\nOutput:")
            print(result.stdout)
        else:
            print("❌ Analysis failed:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Analysis timed out - this might indicate API connection issues")
        return False
    except Exception as e:
        print(f"❌ Error running analysis: {e}")
        return False
    
    return True

def run_specific_symbol_analysis():
    """Run analysis on specific cryptocurrency symbols."""
    
    print("\n2. Analyzing specific symbols (Bitcoin and Ethereum)...")
    
    try:
        result = subprocess.run([
            sys.executable, 'main.py', 'analyze', 
            '--symbols', 'tBTCUSD', 'tETHUSD'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Specific symbol analysis completed!")
            print("\nOutput:")
            print(result.stdout)
        else:
            print("❌ Specific symbol analysis failed:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Analysis timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

def run_detailed_analysis():
    """Run detailed analysis with additional technical indicators."""
    
    print("\n3. Running detailed analysis with technical indicators...")
    
    try:
        result = subprocess.run([
            sys.executable, 'main.py', 'analyze', 
            '--symbols', 'tBTCUSD', '--detailed'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Detailed analysis completed!")
            print("\nOutput:")
            print(result.stdout)
        else:
            print("❌ Detailed analysis failed:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Analysis timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

def main():
    """Main function to run all basic analysis examples."""
    
    print("📊 Bitfinex Trading Tool - Basic Analysis Examples")
    print("=" * 60)
    print()
    print("This example demonstrates:")
    print("- Basic analysis of default cryptocurrency symbols")
    print("- Analysis of specific symbols")
    print("- Detailed analysis with technical indicators")
    print()
    
    success_count = 0
    
    # Run basic analysis
    if run_basic_analysis():
        success_count += 1
    
    # Run specific symbol analysis
    if run_specific_symbol_analysis():
        success_count += 1
    
    # Run detailed analysis
    if run_detailed_analysis():
        success_count += 1
    
    print("\n" + "=" * 60)
    print(f"📈 Analysis Examples Summary: {success_count}/3 completed successfully")
    
    if success_count == 3:
        print("🎉 All analysis examples completed successfully!")
        print("\nNext steps:")
        print("- Review the analysis results above")
        print("- Try running: python examples/dry_run_trading.py")
        print("- Check account info: python main.py account")
    else:
        print("⚠️  Some examples failed. Please check:")
        print("- Your .env file configuration")
        print("- Your Bitfinex API credentials")
        print("- Your internet connection")
    
    return success_count == 3

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)