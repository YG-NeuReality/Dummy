#!/usr/bin/env python3
"""
Configuration Examples

This example shows different configuration setups for various trading scenarios
with the Bitfinex trading tool.

Requirements:
- Bitfinex API credentials
- Installed dependencies (pip install -r requirements.txt)
"""

import os
import shutil
import sys

def show_basic_config():
    """Show basic configuration example."""
    
    print("⚙️  Basic Configuration Example")
    print("=" * 50)
    
    basic_config = """
# Bitfinex API Configuration
BITFINEX_API_KEY=your_api_key_here
BITFINEX_API_SECRET=your_api_secret_here

# Basic Trading Configuration
MIN_TRADE_VOLUME=10.0
MAX_TRADE_VOLUME=100.0
RISK_PERCENTAGE=0.01
"""
    
    print("This is a conservative configuration suitable for beginners:")
    print(basic_config)
    
    print("Key points:")
    print("- MIN_TRADE_VOLUME: $10 minimum per trade")
    print("- MAX_TRADE_VOLUME: $100 maximum per trade")
    print("- RISK_PERCENTAGE: 1% of account balance per trade")
    print()

def show_aggressive_config():
    """Show aggressive configuration example."""
    
    print("⚙️  Aggressive Configuration Example")
    print("=" * 50)
    
    aggressive_config = """
# Bitfinex API Configuration
BITFINEX_API_KEY=your_api_key_here
BITFINEX_API_SECRET=your_api_secret_here

# Aggressive Trading Configuration
MIN_TRADE_VOLUME=50.0
MAX_TRADE_VOLUME=1000.0
RISK_PERCENTAGE=0.05
"""
    
    print("This is an aggressive configuration for experienced traders:")
    print(aggressive_config)
    
    print("Key points:")
    print("- MIN_TRADE_VOLUME: $50 minimum per trade")
    print("- MAX_TRADE_VOLUME: $1000 maximum per trade")
    print("- RISK_PERCENTAGE: 5% of account balance per trade")
    print("- ⚠️  WARNING: Higher risk, higher potential rewards!")
    print()

def show_conservative_config():
    """Show conservative configuration example."""
    
    print("⚙️  Conservative Configuration Example")
    print("=" * 50)
    
    conservative_config = """
# Bitfinex API Configuration
BITFINEX_API_KEY=your_api_key_here
BITFINEX_API_SECRET=your_api_secret_here

# Conservative Trading Configuration
MIN_TRADE_VOLUME=5.0
MAX_TRADE_VOLUME=50.0
RISK_PERCENTAGE=0.005
"""
    
    print("This is a very conservative configuration for risk-averse traders:")
    print(conservative_config)
    
    print("Key points:")
    print("- MIN_TRADE_VOLUME: $5 minimum per trade")
    print("- MAX_TRADE_VOLUME: $50 maximum per trade")
    print("- RISK_PERCENTAGE: 0.5% of account balance per trade")
    print("- 💡 Perfect for learning and testing strategies")
    print()

def create_example_configs():
    """Create example configuration files."""
    
    print("📁 Creating Example Configuration Files")
    print("=" * 50)
    
    configs = {
        '.env.basic': """# Bitfinex API Configuration
BITFINEX_API_KEY=your_api_key_here
BITFINEX_API_SECRET=your_api_secret_here

# Basic Trading Configuration
MIN_TRADE_VOLUME=10.0
MAX_TRADE_VOLUME=100.0
RISK_PERCENTAGE=0.01""",
        
        '.env.aggressive': """# Bitfinex API Configuration
BITFINEX_API_KEY=your_api_key_here
BITFINEX_API_SECRET=your_api_secret_here

# Aggressive Trading Configuration
MIN_TRADE_VOLUME=50.0
MAX_TRADE_VOLUME=1000.0
RISK_PERCENTAGE=0.05""",
        
        '.env.conservative': """# Bitfinex API Configuration
BITFINEX_API_KEY=your_api_key_here
BITFINEX_API_SECRET=your_api_secret_here

# Conservative Trading Configuration
MIN_TRADE_VOLUME=5.0
MAX_TRADE_VOLUME=50.0
RISK_PERCENTAGE=0.005"""
    }
    
    try:
        for filename, content in configs.items():
            with open(filename, 'w') as f:
                f.write(content)
            print(f"✅ Created {filename}")
        
        print("\nTo use one of these configurations:")
        print("1. Copy your preferred config: cp .env.basic .env")
        print("2. Edit .env with your actual API credentials")
        print("3. Run the trading tool: python main.py analyze")
        
    except Exception as e:
        print(f"❌ Error creating config files: {e}")
        return False
    
    return True

def explain_parameters():
    """Explain configuration parameters in detail."""
    
    print("📖 Configuration Parameters Explained")
    print("=" * 50)
    
    explanations = {
        "BITFINEX_API_KEY": "Your Bitfinex API key - get from https://www.bitfinex.com/api",
        "BITFINEX_API_SECRET": "Your Bitfinex API secret - keep this secure!",
        "MIN_TRADE_VOLUME": "Minimum USD value per trade (prevents tiny trades)",
        "MAX_TRADE_VOLUME": "Maximum USD value per trade (caps position size)",
        "RISK_PERCENTAGE": "Percentage of account balance to risk per trade (0.01 = 1%)"
    }
    
    for param, explanation in explanations.items():
        print(f"• {param}:")
        print(f"  {explanation}")
        print()
    
    print("Risk Management Guidelines:")
    print("- Conservative: 0.5-1% risk per trade")
    print("- Moderate: 1-2% risk per trade")
    print("- Aggressive: 2-5% risk per trade")
    print("- ⚠️  Never risk more than you can afford to lose!")

def main():
    """Main function to show configuration examples."""
    
    print("🔧 Bitfinex Trading Tool - Configuration Examples")
    print("=" * 60)
    print()
    print("This example demonstrates:")
    print("- Different risk profile configurations")
    print("- Parameter explanations")
    print("- Example configuration files")
    print()
    
    # Show different configurations
    show_basic_config()
    show_aggressive_config()
    show_conservative_config()
    
    # Explain parameters
    explain_parameters()
    
    print("\n" + "=" * 60)
    
    # Ask if user wants to create example files
    try:
        response = input("Create example configuration files? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            if create_example_configs():
                print("🎉 Example configuration files created successfully!")
            else:
                print("❌ Failed to create configuration files")
        else:
            print("👍 Skipped creating configuration files")
    except (EOFError, KeyboardInterrupt):
        print("\n👍 Skipped creating configuration files")
    
    print("\nNext steps:")
    print("- Choose a configuration that matches your risk tolerance")
    print("- Set up your .env file with real API credentials")
    print("- Test with: python examples/basic_analysis.py")
    print("- Start trading with: python examples/dry_run_trading.py")

if __name__ == '__main__':
    main()