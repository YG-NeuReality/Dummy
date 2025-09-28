"""
Configuration management for Bitfinex trader.
"""
import os
from typing import Dict, Optional
from dotenv import load_dotenv


def get_config() -> Dict[str, str]:
    """Load configuration from environment variables."""
    # Load .env file if it exists
    load_dotenv()
    
    return {
        'BITFINEX_API_KEY': os.getenv('BITFINEX_API_KEY', ''),
        'BITFINEX_API_SECRET': os.getenv('BITFINEX_API_SECRET', ''),
        'MIN_TRADE_VOLUME': float(os.getenv('MIN_TRADE_VOLUME', '10.0')),
        'MAX_TRADE_VOLUME': float(os.getenv('MAX_TRADE_VOLUME', '1000.0')),
        'RISK_PERCENTAGE': float(os.getenv('RISK_PERCENTAGE', '0.02'))
    }


def validate_config() -> bool:
    """Validate that required configuration is present."""
    config = get_config()
    required_keys = ['BITFINEX_API_KEY', 'BITFINEX_API_SECRET']
    
    for key in required_keys:
        if not config.get(key):
            print(f"Missing required configuration: {key}")
            return False
    
    return True