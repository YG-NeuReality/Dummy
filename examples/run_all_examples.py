#!/usr/bin/env python3
"""
Run All Examples

This script runs all example files in sequence to demonstrate
the complete functionality of the Bitfinex trading tool.

Requirements:
- Configured .env file with Bitfinex API credentials (for API-dependent examples)
- Installed dependencies (pip install -r requirements.txt)
"""

import subprocess
import sys
import os

def run_example(script_name, description):
    """Run a single example script."""
    
    print(f"\n{'='*60}")
    print(f"🚀 Running: {script_name}")
    print(f"📝 Description: {description}")
    print('='*60)
    
    if not os.path.exists(f"examples/{script_name}"):
        print(f"❌ Example file not found: examples/{script_name}")
        return False
    
    try:
        # For configuration example, provide 'n' input to skip file creation
        stdin_input = "n\n" if "configuration" in script_name else None
        
        result = subprocess.run([
            sys.executable, f"examples/{script_name}"
        ], input=stdin_input, text=True, timeout=120, capture_output=True)
        
        if result.returncode == 0:
            print("✅ Example completed successfully!")
            print("\nOutput:")
            print(result.stdout)
            return True
        else:
            print("⚠️  Example finished with warnings/errors:")
            print("\nOutput:")
            print(result.stdout)
            if result.stderr:
                print("\nErrors:")
                print(result.stderr)
            # Don't treat as failure if it's just missing credentials
            return "configuration validation failed" in result.stderr.lower()
            
    except subprocess.TimeoutExpired:
        print("⏰ Example timed out")
        return False
    except Exception as e:
        print(f"❌ Error running example: {e}")
        return False

def main():
    """Main function to run all examples."""
    
    print("🌟 Bitfinex Trading Tool - All Examples Runner")
    print("=" * 60)
    print()
    print("This script will run all available examples in sequence.")
    print("Some examples may show errors if API credentials are not configured.")
    print("This is normal and expected for demonstration purposes.")
    print()
    
    examples = [
        ("configuration_examples.py", "Configuration setup for different risk profiles"),
        ("basic_analysis.py", "Basic cryptocurrency analysis examples"),
        ("dry_run_trading.py", "Safe trading simulation examples"),
        ("advanced_usage.py", "Advanced features and power user examples")
    ]
    
    success_count = 0
    total_count = len(examples)
    
    for script_name, description in examples:
        if run_example(script_name, description):
            success_count += 1
    
    print(f"\n{'='*60}")
    print("📊 FINAL SUMMARY")
    print('='*60)
    print(f"Examples completed: {success_count}/{total_count}")
    
    if success_count == total_count:
        print("🎉 All examples ran successfully!")
    elif success_count > 0:
        print("✅ Most examples ran successfully!")
        print("Note: Some failures may be due to missing API credentials,")
        print("which is expected for demonstration purposes.")
    else:
        print("❌ No examples completed successfully.")
        print("This may indicate a configuration or installation issue.")
    
    print("\n📚 Next Steps:")
    print("1. Set up your .env file with real Bitfinex API credentials")
    print("2. Run individual examples: python examples/basic_analysis.py")
    print("3. Start with configuration: python examples/configuration_examples.py")
    print("4. Try safe trading: python examples/dry_run_trading.py")
    
    print("\n⚠️  Remember:")
    print("- Always start with dry-run mode")
    print("- Only trade what you can afford to lose")
    print("- Test thoroughly before using real money")
    
    return success_count > 0

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)