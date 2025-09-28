#!/usr/bin/env python3
"""
Bitfinex Crypto Short Trading CLI Tool

A command-line interface for identifying and trading cryptocurrency short positions
using Bitfinex API integration.
"""
import argparse
import json
import sys
from typing import List

from bitfinex_trader.api.client import BitfinexClient
from bitfinex_trader.analysis.shorts_analyzer import ShortsAnalyzer
from bitfinex_trader.trading.trader import BitfinexTrader
from bitfinex_trader.utils.config import validate_config


# Popular crypto symbols on Bitfinex
DEFAULT_SYMBOLS = [
    'tBTCUSD',   # Bitcoin
    'tETHUSD',   # Ethereum
    'tLTCUSD',   # Litecoin
    'tXRPUSD',   # Ripple
    'tADAUSD',   # Cardano
    'tDOTUSD',   # Polkadot
    'tLINKUSD',  # Chainlink
    'tUNIUSD',   # Uniswap
]


def print_analysis_results(results: List[dict], detailed: bool = False):
    """Print analysis results in formatted output."""
    print("\n" + "="*80)
    print("BITFINEX SHORT ANALYSIS RESULTS")
    print("="*80)
    
    for result in results:
        symbol = result['symbol']
        analysis = result['analysis']
        trade_result = result.get('trade_result', {})
        
        print(f"\n📊 {symbol}")
        print("-" * 40)
        
        if 'error' in analysis:
            print(f"❌ Error: {analysis['error']}")
            continue
        
        # Basic info
        if analysis.get('current_price'):
            print(f"💰 Current Price: ${analysis['current_price']:.4f}")
        
        recommendation = analysis.get('recommendation', 'UNKNOWN')
        signals = analysis.get('combined_signals', [])
        
        # Recommendation with emoji
        rec_emoji = {
            'STRONG_SHORT': '🔴',
            'MODERATE_SHORT': '🟡', 
            'NO_SHORT': '🟢'
        }.get(recommendation, '⚪')
        
        print(f"{rec_emoji} Recommendation: {recommendation}")
        
        if signals:
            print(f"📈 Signals: {', '.join(signals)}")
        
        # Trade result
        if trade_result:
            if trade_result.get('success'):
                action_emoji = '📉' if 'SHORT' in trade_result.get('action', '') else '📊'
                print(f"{action_emoji} {trade_result.get('message', 'Trade executed')}")
            elif trade_result.get('message'):
                print(f"⚠️  {trade_result['message']}")
        
        # Detailed analysis
        if detailed:
            funding = analysis.get('funding_analysis', {})
            momentum = analysis.get('momentum_analysis', {})
            
            if funding and 'error' not in funding:
                print(f"   📊 Short Pressure: {funding.get('short_pressure', 'Unknown')}")
                if funding.get('avg_borrow_rate'):
                    print(f"   💸 Avg Borrow Rate: {funding['avg_borrow_rate']:.6f}")
            
            if momentum and 'error' not in momentum:
                if momentum.get('rsi'):
                    print(f"   📈 RSI: {momentum['rsi']:.2f}")
                if momentum.get('momentum_signals'):
                    print(f"   🎯 Momentum Signals: {', '.join(momentum['momentum_signals'])}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Bitfinex Crypto Short Trading Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py analyze                          # Analyze default symbols
  python main.py analyze --symbols tBTCUSD       # Analyze specific symbol
  python main.py analyze --detailed              # Show detailed analysis
  python main.py trade --dry-run                 # Simulate trades
  python main.py trade --symbols tBTCUSD         # Trade specific symbol
  python main.py positions                       # Show active positions
  python main.py account                         # Show account info
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze symbols for short opportunities')
    analyze_parser.add_argument('--symbols', nargs='+', default=DEFAULT_SYMBOLS,
                               help='Symbols to analyze (default: major cryptos)')
    analyze_parser.add_argument('--detailed', action='store_true',
                               help='Show detailed analysis')
    analyze_parser.add_argument('--json', action='store_true',
                               help='Output results in JSON format')
    
    # Trade command
    trade_parser = subparsers.add_parser('trade', help='Execute trades based on analysis')
    trade_parser.add_argument('--symbols', nargs='+', default=DEFAULT_SYMBOLS,
                             help='Symbols to trade (default: major cryptos)')
    trade_parser.add_argument('--dry-run', action='store_true', default=True,
                             help='Simulate trades without executing (default)')
    trade_parser.add_argument('--execute', action='store_true',
                             help='Execute real trades (removes dry-run mode)')
    
    # Positions command
    positions_parser = subparsers.add_parser('positions', help='Show active positions')
    
    # Account command
    account_parser = subparsers.add_parser('account', help='Show account information')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Validate configuration
    if not validate_config():
        print("❌ Configuration validation failed!")
        print("Please check your .env file and ensure API credentials are set.")
        print("Copy .env.example to .env and fill in your Bitfinex API credentials.")
        sys.exit(1)
    
    try:
        # Initialize client
        client = BitfinexClient()
        
        if args.command == 'analyze':
            print("🔍 Starting short opportunity analysis...")
            analyzer = ShortsAnalyzer(client)
            
            results = []
            for symbol in args.symbols:
                print(f"Analyzing {symbol}...")
                analysis = analyzer.get_comprehensive_analysis(symbol)
                results.append({
                    'symbol': symbol,
                    'analysis': analysis
                })
            
            if args.json:
                print(json.dumps(results, indent=2, default=str))
            else:
                print_analysis_results(results, detailed=args.detailed)
        
        elif args.command == 'trade':
            dry_run = not args.execute  # Default is dry-run, unless --execute is specified
            
            mode_text = "DRY RUN" if dry_run else "LIVE TRADING"
            print(f"🚀 Starting trading scan - {mode_text} MODE")
            
            if not dry_run:
                confirm = input("⚠️  LIVE TRADING MODE! Are you sure? Type 'YES' to continue: ")
                if confirm != 'YES':
                    print("Trading cancelled.")
                    return
            
            trader = BitfinexTrader(client)
            results = trader.scan_and_trade(args.symbols, dry_run=dry_run)
            
            print_analysis_results(results, detailed=True)
            
            # Summary
            successful_trades = sum(1 for r in results if r.get('trade_result', {}).get('success'))
            print(f"\n📊 Summary: {successful_trades}/{len(results)} trades executed")
        
        elif args.command == 'positions':
            print("📋 Active Positions Summary")
            trader = BitfinexTrader(client)
            positions = trader.get_active_positions_summary()
            
            if 'error' in positions:
                print(f"❌ Error: {positions['error']}")
                return
            
            print(f"Total Positions: {positions['total_positions']}")
            print(f"Short Positions: {positions['short_positions']}")
            print(f"Total Unrealized P&L: ${positions['total_unrealized_pnl']:.2f}")
            
            if positions['positions']:
                print("\nShort Positions:")
                for pos in positions['positions']:
                    print(f"  {pos['symbol']}: {pos['amount']:.6f} @ ${pos['base_price']:.4f} (P&L: ${pos['pnl']:.2f})")
        
        elif args.command == 'account':
            print("👤 Account Information")
            account_info = client.get_account_info()
            wallets = client.get_wallet_balances()
            
            print(f"User ID: {account_info.get('id', 'Unknown')}")
            print(f"Email: {account_info.get('email', 'Unknown')}")
            
            print("\nWallet Balances:")
            for wallet in wallets:
                wallet_type, currency, balance, available = wallet[:4]
                if float(balance) > 0:
                    print(f"  {wallet_type.upper()} {currency}: {balance} (Available: {available})")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()