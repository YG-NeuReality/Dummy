#!/usr/bin/env python3
"""
Test script to validate Bitfinex trading implementation.
This script tests the modules without requiring real API credentials.
"""
import os
import sys
from unittest.mock import Mock, patch

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported successfully."""
    print("Testing module imports...")
    
    try:
        from bitfinex_trader.api.client import BitfinexClient
        from bitfinex_trader.analysis.shorts_analyzer import ShortsAnalyzer
        from bitfinex_trader.trading.trader import BitfinexTrader
        from bitfinex_trader.utils.config import get_config, validate_config
        print("✅ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_config():
    """Test configuration management."""
    print("\nTesting configuration...")
    
    try:
        from bitfinex_trader.utils.config import get_config, validate_config
        
        # Test config loading (should work even without .env)
        config = get_config()
        assert isinstance(config, dict)
        assert 'BITFINEX_API_KEY' in config
        print("✅ Configuration loading works")
        
        # Test validation (should fail without real credentials)
        is_valid = validate_config()
        print(f"✅ Configuration validation: {'Valid' if is_valid else 'Invalid (expected without credentials)'}")
        
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_client_initialization():
    """Test Bitfinex client initialization."""
    print("\nTesting client initialization...")
    
    try:
        from bitfinex_trader.api.client import BitfinexClient
        
        # Test that client requires credentials
        try:
            client = BitfinexClient()
            print("❌ Client should require credentials")
            return False
        except ValueError:
            print("✅ Client correctly requires credentials")
        
        # Test with mock credentials
        client = BitfinexClient(api_key="test_key", api_secret="test_secret")
        assert client.api_key == "test_key"
        assert client.api_secret == "test_secret"
        print("✅ Client initialization with credentials works")
        
        return True
    except Exception as e:
        print(f"❌ Client initialization test failed: {e}")
        return False

def test_analyzer_with_mock():
    """Test analyzer with mocked API responses."""
    print("\nTesting analyzer with mock data...")
    
    try:
        from bitfinex_trader.api.client import BitfinexClient
        from bitfinex_trader.analysis.shorts_analyzer import ShortsAnalyzer
        
        # Create mock client
        mock_client = Mock(spec=BitfinexClient)
        
        # Mock funding book response
        mock_client.get_funding_book.return_value = [
            [0.0001, 1000, 5000],  # rate, period, amount (positive = lender)
            [0.0002, 1000, -3000], # negative = borrower
            [0.0003, 1000, -2000]
        ]
        
        # Mock market data response
        mock_client.get_market_data.return_value = [
            [1640995200000, 47000, 47100, 47200, 46900, 1000],  # OHLCV data
            [1640991600000, 46800, 47000, 47100, 46700, 1100],
            # ... more candles would be here
        ] * 30  # Simulate 30 candles
        
        # Mock ticker response
        mock_client.get_ticker.return_value = [0, 0, 0, 0, 0, 0, 47000, 1000000]
        
        analyzer = ShortsAnalyzer(mock_client)
        
        # Test funding analysis
        funding_result = analyzer.analyze_funding_rates("BTC")
        assert 'short_pressure' in funding_result
        print("✅ Funding rate analysis works")
        
        # Test comprehensive analysis
        comprehensive = analyzer.get_comprehensive_analysis("tBTCUSD")
        assert 'recommendation' in comprehensive
        print("✅ Comprehensive analysis works")
        
        return True
    except Exception as e:
        print(f"❌ Analyzer test failed: {e}")
        return False

def test_trader_with_mock():
    """Test trader with mocked dependencies."""
    print("\nTesting trader with mock data...")
    
    try:
        from bitfinex_trader.api.client import BitfinexClient
        from bitfinex_trader.trading.trader import BitfinexTrader
        
        # Create mock client
        mock_client = Mock(spec=BitfinexClient)
        
        # Mock wallet balances
        mock_client.get_wallet_balances.return_value = [
            ['exchange', 'USD', '1000.0', '1000.0']
        ]
        
        # Mock ticker
        mock_client.get_ticker.return_value = [0, 0, 0, 0, 0, 0, 47000, 1000000]
        
        trader = BitfinexTrader(mock_client)
        
        # Test position size calculation
        with patch.object(trader, 'config', {'RISK_PERCENTAGE': 0.02, 'MIN_TRADE_VOLUME': 0.001, 'MAX_TRADE_VOLUME': 1.0}):
            position_size = trader.calculate_position_size("tBTCUSD")
            assert position_size > 0
            print(f"✅ Position size calculation works: {position_size}")
        
        # Test dry run trade execution
        mock_analysis = {
            'recommendation': 'STRONG_SHORT',
            'current_price': 47000,
            'combined_signals': ['HIGH_SHORT_INTEREST', 'BEARISH_MOMENTUM']
        }
        
        trade_result = trader.execute_short_trade("tBTCUSD", mock_analysis, dry_run=True)
        assert trade_result['success'] is True
        assert trade_result['dry_run'] is True
        print("✅ Dry run trade execution works")
        
        return True
    except Exception as e:
        print(f"❌ Trader test failed: {e}")
        return False

def test_cli_structure():
    """Test that the CLI main module is properly structured."""
    print("\nTesting CLI structure...")
    
    try:
        # Import main module
        import main
        
        # Check that main function exists
        assert hasattr(main, 'main')
        assert callable(main.main)
        
        # Check default symbols
        assert hasattr(main, 'DEFAULT_SYMBOLS')
        assert isinstance(main.DEFAULT_SYMBOLS, list)
        assert len(main.DEFAULT_SYMBOLS) > 0
        
        print("✅ CLI structure is correct")
        return True
    except Exception as e:
        print(f"❌ CLI structure test failed: {e}")
        return False

def run_all_tests():
    """Run all tests."""
    print("🚀 Running Bitfinex Trading Implementation Tests")
    print("="*60)
    
    tests = [
        test_imports,
        test_config,
        test_client_initialization,
        test_analyzer_with_mock,
        test_trader_with_mock,
        test_cli_structure
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! Implementation is ready for use.")
    else:
        print("⚠️  Some tests failed. Please review the implementation.")
    
    return failed == 0

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)