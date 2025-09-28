#!/usr/bin/env python3
"""
Advanced Usage Examples

This example demonstrates advanced features and use cases of the
Bitfinex trading tool for experienced users.

Requirements:
- Configured .env file with Bitfinex API credentials
- Installed dependencies (pip install -r requirements.txt)
"""

import subprocess
import sys
import os
import json

def run_json_analysis():
    """Run analysis with JSON output for programmatic processing."""
    
    print("📊 JSON Analysis Output Example")
    print("=" * 50)
    
    try:
        print("Running analysis with JSON output...")
        result = subprocess.run([
            sys.executable, 'main.py', 'analyze', 
            '--symbols', 'tBTCUSD', 'tETHUSD', '--json'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ JSON analysis completed!")
            print("\nRaw JSON Output:")
            print(result.stdout)
            
            # Try to parse and pretty-print JSON
            try:
                data = json.loads(result.stdout)
                print("\nParsed JSON Structure:")
                for item in data[:1]:  # Show structure of first item
                    print(f"Symbol: {item.get('symbol')}")
                    analysis = item.get('analysis', {})
                    print(f"- Recommendation: {analysis.get('recommendation')}")
                    print(f"- Current Price: {analysis.get('current_price')}")
                    print(f"- Signals: {analysis.get('combined_signals', [])}")
                    
            except json.JSONDecodeError:
                print("Note: Output is not valid JSON (might be error message)")
                
        else:
            print("❌ JSON analysis failed:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Analysis timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

def run_single_symbol_detailed():
    """Run detailed analysis on a single symbol."""
    
    print("\n🔍 Single Symbol Detailed Analysis")
    print("=" * 50)
    
    try:
        print("Running detailed analysis on Bitcoin...")
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

def demonstrate_altcoins():
    """Demonstrate analysis on alternative cryptocurrencies."""
    
    print("\n🚀 Alternative Cryptocurrencies Analysis")
    print("=" * 50)
    
    altcoin_symbols = ['tADAUSD', 'tDOTUSD', 'tLINKUSD', 'tUNIUSD']
    
    try:
        print(f"Analyzing altcoins: {', '.join(altcoin_symbols)}")
        result = subprocess.run([
            sys.executable, 'main.py', 'analyze', 
            '--symbols'] + altcoin_symbols,
            capture_output=True, text=True, timeout=45)
        
        if result.returncode == 0:
            print("✅ Altcoin analysis completed!")
            print("\nOutput:")
            print(result.stdout)
        else:
            print("❌ Altcoin analysis failed:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Analysis timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

def show_workflow_automation():
    """Show how to automate trading workflows."""
    
    print("\n🤖 Workflow Automation Example")
    print("=" * 50)
    
    workflow_script = """#!/bin/bash

# Automated Trading Workflow Script
echo "Starting automated trading workflow..."

# Step 1: Analyze market conditions
echo "1. Analyzing market conditions..."
python main.py analyze --json > analysis_results.json

# Step 2: Check if results contain strong signals
# (This would normally include more sophisticated parsing)
if grep -q "STRONG_SHORT" analysis_results.json; then
    echo "2. Strong short signals detected!"
    
    # Step 3: Execute dry-run trades
    echo "3. Executing dry-run trades..."
    python main.py trade --dry-run
    
    # Step 4: Check positions
    echo "4. Checking positions..."
    python main.py positions
else
    echo "2. No strong signals detected, skipping trades"
fi

# Step 5: Clean up
rm -f analysis_results.json
echo "Workflow completed!"
"""
    
    print("Here's an example bash script for workflow automation:")
    print(workflow_script)
    
    print("This script demonstrates:")
    print("- Automated market analysis")
    print("- Conditional trade execution based on signals")
    print("- Position monitoring")
    print("- Result cleanup")
    print()
    print("To use this script:")
    print("1. Save it as 'trading_workflow.sh'")
    print("2. Make it executable: chmod +x trading_workflow.sh")
    print("3. Run it: ./trading_workflow.sh")
    
    return True

def show_monitoring_setup():
    """Show how to set up continuous monitoring."""
    
    print("\n👁️  Continuous Monitoring Setup")
    print("=" * 50)
    
    monitoring_script = """#!/bin/bash

# Continuous Market Monitoring Script
while true; do
    echo "$(date): Checking market conditions..."
    
    # Run analysis and save results
    python main.py analyze --json > temp_analysis.json
    
    # Check for strong signals (simplified)
    if grep -q "STRONG_SHORT" temp_analysis.json; then
        echo "$(date): ⚠️  Strong short signal detected!"
        # Send notification (email, slack, etc.)
        # python notify.py "Strong short signal detected"
    fi
    
    # Clean up
    rm -f temp_analysis.json
    
    # Wait 15 minutes before next check
    sleep 900
done
"""
    
    print("Example continuous monitoring script:")
    print(monitoring_script)
    
    print("This monitoring setup:")
    print("- Runs analysis every 15 minutes")
    print("- Checks for strong trading signals")
    print("- Can be extended with notifications")
    print("- Logs activity with timestamps")
    print()
    print("To use for monitoring:")
    print("1. Save as 'monitor_markets.sh'")
    print("2. Make executable: chmod +x monitor_markets.sh")
    print("3. Run in background: nohup ./monitor_markets.sh &")
    
    return True

def main():
    """Main function to run advanced usage examples."""
    
    print("🎯 Bitfinex Trading Tool - Advanced Usage Examples")
    print("=" * 65)
    print()
    print("This example demonstrates:")
    print("- JSON output for programmatic processing")
    print("- Detailed single-symbol analysis")
    print("- Alternative cryptocurrency analysis")
    print("- Workflow automation")
    print("- Continuous monitoring setup")
    print()
    
    success_count = 0
    
    # Run JSON analysis
    if run_json_analysis():
        success_count += 1
    
    # Run detailed single symbol analysis
    if run_single_symbol_detailed():
        success_count += 1
    
    # Demonstrate altcoin analysis
    if demonstrate_altcoins():
        success_count += 1
    
    # Show automation examples (these don't fail)
    if show_workflow_automation():
        success_count += 1
    
    if show_monitoring_setup():
        success_count += 1
    
    print("\n" + "=" * 65)
    print(f"🔬 Advanced Examples Summary: {success_count}/5 completed successfully")
    
    if success_count >= 3:  # At least the analysis examples should work
        print("🎉 Advanced examples completed successfully!")
        print("\nNext steps for advanced users:")
        print("- Set up automated workflows using the bash scripts above")
        print("- Integrate JSON output with your own analysis tools")
        print("- Build custom notification systems")
        print("- Create portfolio management scripts")
    else:
        print("⚠️  Some analysis examples failed. Please check:")
        print("- Your .env file configuration")
        print("- Your Bitfinex API credentials")
        print("- Your internet connection")
    
    return success_count >= 3

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)