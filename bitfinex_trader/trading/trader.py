"""
Trading module for executing short positions based on analysis.
"""
from typing import Dict, Optional, List
import time
from ..api.client import BitfinexClient
from ..analysis.shorts_analyzer import ShortsAnalyzer
from ..utils.config import get_config


class BitfinexTrader:
    """Execute trading operations based on short analysis."""
    
    def __init__(self, client: BitfinexClient):
        """Initialize trader with Bitfinex client."""
        self.client = client
        self.analyzer = ShortsAnalyzer(client)
        self.config = get_config()
    
    def calculate_position_size(self, symbol: str, risk_percentage: float = None) -> float:
        """Calculate appropriate position size based on account balance and risk."""
        if risk_percentage is None:
            risk_percentage = self.config['RISK_PERCENTAGE']
        
        try:
            # Get account balances
            wallets = self.client.get_wallet_balances()
            
            # Find USD balance (or relevant base currency)
            usd_balance = 0
            for wallet in wallets:
                if wallet[1] == 'USD' and wallet[0] == 'exchange':
                    usd_balance = float(wallet[2])  # Available balance
                    break
            
            if usd_balance == 0:
                return 0
            
            # Calculate position size based on risk percentage
            risk_amount = usd_balance * risk_percentage
            
            # Get current price
            ticker = self.client.get_ticker(symbol)
            current_price = float(ticker[6])
            
            # Calculate position size in base currency
            position_size = risk_amount / current_price
            
            # Apply min/max limits
            min_volume = self.config['MIN_TRADE_VOLUME']
            max_volume = self.config['MAX_TRADE_VOLUME']
            
            position_size = max(min_volume, min(position_size, max_volume))
            
            return round(position_size, 6)
            
        except Exception as e:
            print(f"Error calculating position size: {e}")
            return 0
    
    def execute_short_trade(self, symbol: str, analysis: Dict, dry_run: bool = True) -> Dict:
        """Execute a short trade based on analysis results."""
        
        if analysis.get('recommendation') not in ['STRONG_SHORT', 'MODERATE_SHORT']:
            return {
                'success': False,
                'message': 'No short signal detected',
                'recommendation': analysis.get('recommendation')
            }
        
        try:
            # Calculate position size
            position_size = self.calculate_position_size(symbol)
            
            if position_size <= 0:
                return {
                    'success': False,
                    'message': 'Insufficient balance or invalid position size'
                }
            
            # Get current price for order
            current_price = analysis.get('current_price')
            if not current_price:
                ticker = self.client.get_ticker(symbol)
                current_price = float(ticker[6])
            
            # Calculate short sell price (slightly below current for market entry)
            short_price = current_price * 0.999  # 0.1% below current price
            
            if dry_run:
                return {
                    'success': True,
                    'dry_run': True,
                    'symbol': symbol,
                    'action': 'SHORT_SELL',
                    'size': -position_size,  # Negative for short
                    'price': short_price,
                    'recommendation': analysis.get('recommendation'),
                    'signals': analysis.get('combined_signals', []),
                    'message': f'DRY RUN: Would short {position_size} {symbol} at {short_price}'
                }
            
            # Execute actual short order
            order_result = self.client.submit_order(
                symbol=symbol,
                amount=-position_size,  # Negative amount for short
                price=short_price,
                order_type="EXCHANGE LIMIT"
            )
            
            return {
                'success': True,
                'dry_run': False,
                'symbol': symbol,
                'action': 'SHORT_SELL',
                'size': -position_size,
                'price': short_price,
                'order_id': order_result.get('id'),
                'recommendation': analysis.get('recommendation'),
                'signals': analysis.get('combined_signals', []),
                'message': f'Short order placed: {position_size} {symbol} at {short_price}'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Trade execution failed: {str(e)}'
            }
    
    def scan_and_trade(self, symbols: List[str], dry_run: bool = True) -> List[Dict]:
        """Scan multiple symbols and execute trades where signals are found."""
        results = []
        
        for symbol in symbols:
            print(f"Analyzing {symbol}...")
            
            # Get comprehensive analysis
            analysis = self.analyzer.get_comprehensive_analysis(symbol)
            
            # Execute trade if signal is strong enough
            trade_result = self.execute_short_trade(symbol, analysis, dry_run)
            
            results.append({
                'symbol': symbol,
                'analysis': analysis,
                'trade_result': trade_result
            })
            
            # Add delay between API calls to respect rate limits
            time.sleep(1)
        
        return results
    
    def get_active_positions_summary(self) -> Dict:
        """Get summary of active trading positions."""
        try:
            positions = self.client.get_active_positions()
            
            total_unrealized_pnl = 0
            short_positions = []
            
            for pos in positions:
                if float(pos[2]) < 0:  # Negative amount = short position
                    position_info = {
                        'symbol': pos[0],
                        'amount': float(pos[2]),
                        'base_price': float(pos[3]),
                        'pnl': float(pos[6]) if len(pos) > 6 else 0
                    }
                    short_positions.append(position_info)
                    total_unrealized_pnl += position_info['pnl']
            
            return {
                'total_positions': len(positions),
                'short_positions': len(short_positions),
                'positions': short_positions,
                'total_unrealized_pnl': total_unrealized_pnl
            }
            
        except Exception as e:
            return {
                'error': f'Failed to get positions: {str(e)}'
            }