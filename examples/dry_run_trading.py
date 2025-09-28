#!/usr/bin/env python3
"""
Dry Run Trading Example

This example demonstrates how to simulate cryptocurrency short trades
without risking real money using the Bitfinex trading tool's dry-run mode.

Requirements:
- Configured .env file with Bitfinex API credentials
- Installed dependencies (pip install -r requirements.txt)
"""

import subprocess
import sys
import os

def run_dry_run_trading():
    """Run dry-run trading simulation on default symbols."""
    
    print("🏃 Dry Run Trading Simulation")
    print("=" * 50)
    print("NOTE: This is a SIMULATION - no real trades will be executed")
    print()
    
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
        print("1. Running dry-run trading on default symbols...")
        result = subprocess.run([
            sys.executable, 'main.py', 'trade', '--dry-run'
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ Dry-run trading completed successfully!")
            print("\nOutput:")
            print(result.stdout)
        else:
            print("❌ Dry-run trading failed:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Trading simulation timed out")
        return False
    except Exception as e:
        print(f"❌ Error running dry-run trading: {e}")
        return False
    
    return True

def run_specific_symbols_dry_run():
    """Run dry-run trading on specific symbols."""
    
    print("\n2. Running dry-run trading on specific symbols (BTC, ETH)...")
    
    try:
        result = subprocess.run([
            sys.executable, 'main.py', 'trade', 
            '--symbols', 'tBTCUSD', 'tETHUSD', '--dry-run'
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ Specific symbol dry-run completed!")
            print("\nOutput:")
            print(result.stdout)
        else:
            print("❌ Specific symbol dry-run failed:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Trading simulation timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

def show_positions():
    """Show current positions (if any)."""
    
    print("\n3. Checking current positions...")
    
    try:
        result = subprocess.run([
            sys.executable, 'main.py', 'positions'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Position check completed!")
            print("\nOutput:")
            print(result.stdout)
        else:
            print("❌ Position check failed:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Position check timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

def show_account_info():
    """Show account information."""
    
    print("\n4. Checking account information...")
    
    try:
        result = subprocess.run([
            sys.executable, 'main.py', 'account'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Account info retrieved!")
            print("\nOutput:")
            print(result.stdout)
        else:
            print("❌ Account info retrieval failed:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Account info check timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

def main():
    """Main function to run all dry-run trading examples."""
    
    print("🔥 Bitfinex Trading Tool - Dry Run Trading Examples")
    print("=" * 65)
    print()
    print("This example demonstrates:")
    print("- Safe trading simulation (dry-run mode)")
    print("- Trading analysis on specific symbols")
    print("- Position monitoring")
    print("- Account information retrieval")
    print()
    print("⚠️  IMPORTANT: All trades are simulated - no real money is used!")
    print()
    
    success_count = 0
    
    # Run dry-run trading
    if run_dry_run_trading():
        success_count += 1
    
    # Run specific symbols dry-run
    if run_specific_symbols_dry_run():
        success_count += 1
    
    # Show positions
    if show_positions():
        success_count += 1
    
    # Show account info
    if show_account_info():
        success_count += 1
    
    print("\n" + "=" * 65)
    print(f"📊 Dry Run Examples Summary: {success_count}/4 completed successfully")
    
    if success_count == 4:
        print("🎉 All dry-run examples completed successfully!")
        print("\nNext steps:")
        print("- Review the simulation results above")
        print("- Try running: python examples/configuration_examples.py")
        print("- For REAL trading (⚠️ CAUTION): python main.py trade --execute")
    else:
        print("⚠️  Some examples failed. Please check:")
        print("- Your .env file configuration")
        print("- Your Bitfinex API credentials")
        print("- Your internet connection")
    
    return success_count == 4

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)