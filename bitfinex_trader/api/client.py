"""
Bitfinex API client for account integration and trading operations.
"""
import hashlib
import hmac
import json
import time
from typing import Dict, List, Optional, Any
import requests
from ..utils.config import get_config


class BitfinexClient:
    """Bitfinex API client for authenticated requests."""
    
    BASE_URL = "https://api-pub.bitfinex.com"
    API_VERSION = "v2"
    
    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None):
        """Initialize Bitfinex client with API credentials."""
        config = get_config()
        self.api_key = api_key or config.get('BITFINEX_API_KEY')
        self.api_secret = api_secret or config.get('BITFINEX_API_SECRET')
        
        if not self.api_key or not self.api_secret:
            raise ValueError("Bitfinex API credentials are required")
    
    def _generate_signature(self, path: str, nonce: str, body: str = '') -> str:
        """Generate authentication signature for API requests."""
        message = f'/api/{path}{nonce}{body}'
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha384
        ).hexdigest()
        return signature
    
    def _make_authenticated_request(self, method: str, path: str, params: Dict = None) -> Dict:
        """Make authenticated request to Bitfinex API."""
        url = f"{self.BASE_URL}/{self.API_VERSION}/{path}"
        nonce = str(int(time.time() * 1000000))
        body = json.dumps(params or {})
        
        signature = self._generate_signature(path, nonce, body)
        
        headers = {
            'bfx-nonce': nonce,
            'bfx-apikey': self.api_key,
            'bfx-signature': signature,
            'content-type': 'application/json'
        }
        
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers, params=params)
        else:
            response = requests.post(url, headers=headers, data=body)
        
        response.raise_for_status()
        return response.json()
    
    def get_account_info(self) -> Dict:
        """Get account information."""
        return self._make_authenticated_request('POST', 'auth/r/info/user')
    
    def get_wallet_balances(self) -> List[Dict]:
        """Get wallet balances."""
        return self._make_authenticated_request('POST', 'auth/r/wallets')
    
    def get_active_positions(self) -> List[Dict]:
        """Get active trading positions."""
        return self._make_authenticated_request('POST', 'auth/r/positions')
    
    def get_ticker(self, symbol: str) -> Dict:
        """Get ticker information for a symbol."""
        url = f"{self.BASE_URL}/{self.API_VERSION}/ticker/{symbol}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_funding_book(self, symbol: str, precision: str = "P0") -> Dict:
        """Get funding book for a symbol to analyze short interest."""
        url = f"{self.BASE_URL}/{self.API_VERSION}/book/{symbol}/{precision}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_market_data(self, symbol: str, timeframe: str = "1h", limit: int = 100) -> List:
        """Get historical market data."""
        url = f"{self.BASE_URL}/{self.API_VERSION}/candles/trade:{timeframe}:{symbol}/hist"
        params = {'limit': limit, 'sort': -1}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def submit_order(self, symbol: str, amount: float, price: float, order_type: str = "EXCHANGE LIMIT") -> Dict:
        """Submit a trading order."""
        params = {
            'type': order_type,
            'symbol': symbol,
            'amount': str(amount),
            'price': str(price)
        }
        return self._make_authenticated_request('POST', 'auth/w/order/submit', params)