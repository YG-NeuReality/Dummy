"""
Analysis module for identifying short opportunities in cryptocurrency markets.
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from ..api.client import BitfinexClient


class ShortsAnalyzer:
    """Analyze market data to identify short trading opportunities."""
    
    def __init__(self, client: BitfinexClient):
        """Initialize analyzer with Bitfinex client."""
        self.client = client
    
    def analyze_funding_rates(self, symbol: str) -> Dict:
        """Analyze funding rates to identify high short interest."""
        try:
            funding_book = self.client.get_funding_book(f"f{symbol}")
            
            if not funding_book:
                return {'error': 'No funding data available'}
            
            # Parse funding book data
            bids = [item for item in funding_book if float(item[2]) > 0]  # Lenders
            asks = [item for item in funding_book if float(item[2]) < 0]  # Borrowers
            
            if not asks:
                return {'short_pressure': 'LOW', 'signal': 'NEUTRAL'}
            
            # Calculate metrics
            total_borrow_demand = sum(abs(float(item[2])) for item in asks)
            avg_borrow_rate = np.mean([float(item[0]) for item in asks[:10]])  # Top 10 rates
            
            # Determine short pressure level
            if avg_borrow_rate > 0.0001:  # 0.01% daily
                pressure = 'HIGH' if avg_borrow_rate > 0.0005 else 'MEDIUM'
            else:
                pressure = 'LOW'
            
            return {
                'symbol': symbol,
                'short_pressure': pressure,
                'avg_borrow_rate': avg_borrow_rate,
                'total_demand': total_borrow_demand,
                'signal': 'SHORT' if pressure == 'HIGH' else 'NEUTRAL'
            }
            
        except Exception as e:
            return {'error': f'Analysis failed: {str(e)}'}
    
    def analyze_price_momentum(self, symbol: str, timeframe: str = "1h") -> Dict:
        """Analyze price momentum for short entry signals."""
        try:
            # Get historical data
            candles = self.client.get_market_data(symbol, timeframe, limit=50)
            
            if len(candles) < 20:
                return {'error': 'Insufficient data for analysis'}
            
            # Convert to DataFrame for analysis
            df = pd.DataFrame(candles, columns=[
                'timestamp', 'open', 'close', 'high', 'low', 'volume'
            ])
            df = df.astype(float)
            df = df.sort_values('timestamp')
            
            # Calculate technical indicators
            df['sma_20'] = df['close'].rolling(window=20).mean()
            df['rsi'] = self._calculate_rsi(df['close'])
            df['price_change'] = df['close'].pct_change(periods=5)  # 5-period change
            
            latest = df.iloc[-1]
            
            # Determine momentum signals
            signals = []
            if latest['close'] < latest['sma_20']:
                signals.append('BELOW_SMA20')
            if latest['rsi'] > 70:
                signals.append('OVERBOUGHT')
            if latest['price_change'] < -0.05:  # 5% decline
                signals.append('STRONG_DECLINE')
            
            momentum_score = len(signals)
            signal = 'SHORT' if momentum_score >= 2 else 'NEUTRAL'
            
            return {
                'symbol': symbol,
                'current_price': latest['close'],
                'sma_20': latest['sma_20'],
                'rsi': latest['rsi'],
                'price_change_5p': latest['price_change'],
                'momentum_signals': signals,
                'momentum_score': momentum_score,
                'signal': signal
            }
            
        except Exception as e:
            return {'error': f'Momentum analysis failed: {str(e)}'}
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate Relative Strength Index."""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def get_comprehensive_analysis(self, symbol: str) -> Dict:
        """Get comprehensive short analysis combining multiple factors."""
        funding_analysis = self.analyze_funding_rates(symbol)
        momentum_analysis = self.analyze_price_momentum(symbol)
        
        # Get current ticker data
        try:
            ticker = self.client.get_ticker(symbol)
            current_price = float(ticker[6])  # Last price
            volume_24h = float(ticker[7])  # 24h volume
        except:
            current_price = None
            volume_24h = None
        
        # Combine signals
        signals = []
        if funding_analysis.get('signal') == 'SHORT':
            signals.append('HIGH_SHORT_INTEREST')
        if momentum_analysis.get('signal') == 'SHORT':
            signals.append('BEARISH_MOMENTUM')
        
        # Overall recommendation
        if len(signals) >= 2:
            recommendation = 'STRONG_SHORT'
        elif len(signals) == 1:
            recommendation = 'MODERATE_SHORT'
        else:
            recommendation = 'NO_SHORT'
        
        return {
            'symbol': symbol,
            'current_price': current_price,
            'volume_24h': volume_24h,
            'funding_analysis': funding_analysis,
            'momentum_analysis': momentum_analysis,
            'combined_signals': signals,
            'recommendation': recommendation,
            'timestamp': pd.Timestamp.now().isoformat()
        }