# Bitfinex Crypto Short Trading Tool

A Python-based application for integrating with Bitfinex account to identify and trade cryptocurrency short positions based on market analysis.

## Features

- **Bitfinex API Integration**: Secure connection to Bitfinex trading platform
- **Short Position Analysis**: Identifies opportunities based on:
  - Funding rate analysis (short interest pressure)
  - Technical momentum indicators (RSI, moving averages)
  - Price action patterns
- **Automated Trading**: Execute short trades based on analysis signals
- **Risk Management**: Configurable position sizing and risk controls
- **CLI Interface**: Easy-to-use command-line interface
- **Dry Run Mode**: Test strategies without real money

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/YG-NeuReality/Dummy.git
cd Dummy

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your Bitfinex API credentials
# Get your API keys from: https://www.bitfinex.com/api
```

Required configuration in `.env`:
```
BITFINEX_API_KEY=your_api_key_here
BITFINEX_API_SECRET=your_api_secret_here
MIN_TRADE_VOLUME=10.0
MAX_TRADE_VOLUME=1000.0
RISK_PERCENTAGE=0.02
```

### 3. Basic Usage

```bash
# Analyze major cryptocurrencies for short opportunities
python main.py analyze

# Analyze specific symbols
python main.py analyze --symbols tBTCUSD tETHUSD

# Get detailed analysis
python main.py analyze --detailed

# Simulate trades (dry run)
python main.py trade --dry-run

# View account information
python main.py account

# Check active positions
python main.py positions
```

## Commands

### Analyze
Scan cryptocurrencies for short trading opportunities:

```bash
python main.py analyze [OPTIONS]

Options:
  --symbols     Symbols to analyze (default: major cryptos)
  --detailed    Show detailed technical analysis
  --json        Output results in JSON format
```

### Trade
Execute trades based on analysis:

```bash
python main.py trade [OPTIONS]

Options:
  --symbols     Symbols to trade (default: major cryptos)
  --dry-run     Simulate trades (default, safe mode)
  --execute     Execute real trades (requires confirmation)
```

### Positions
View active trading positions:

```bash
python main.py positions
```

### Account
Display account information and balances:

```bash
python main.py account
```

## Analysis Methodology

The tool identifies short opportunities using multiple factors:

1. **Funding Rate Analysis**
   - Monitors lending rates for high short interest
   - Identifies when borrowing costs indicate strong short pressure

2. **Technical Momentum**
   - RSI indicators for overbought conditions
   - Moving average trends
   - Price momentum analysis

3. **Combined Signals**
   - Requires multiple confirmations for trade signals
   - Risk-adjusted position sizing

## Risk Management

- **Position Sizing**: Based on account balance and configurable risk percentage
- **Volume Limits**: Minimum and maximum trade volumes
- **Dry Run Default**: All trades default to simulation mode
- **Confirmation Required**: Live trading requires explicit confirmation

## Security

- API credentials stored in environment variables
- No hardcoded secrets in code
- Rate limiting to respect Bitfinex API limits
- Error handling for API failures

## Supported Symbols

Default analysis covers major cryptocurrencies:
- Bitcoin (tBTCUSD)
- Ethereum (tETHUSD)
- Litecoin (tLTCUSD)
- Ripple (tXRPUSD)
- Cardano (tADAUSD)
- Polkadot (tDOTUSD)
- Chainlink (tLINKUSD)
- Uniswap (tUNIUSD)

Custom symbols can be specified using the `--symbols` parameter.

## Example Output

```
================================================================================
BITFINEX SHORT ANALYSIS RESULTS
================================================================================

📊 tBTCUSD
----------------------------------------
💰 Current Price: $43,250.0000
🔴 Recommendation: STRONG_SHORT
📈 Signals: HIGH_SHORT_INTEREST, BEARISH_MOMENTUM
📉 DRY RUN: Would short 0.023148 tBTCUSD at 43206.75
   📊 Short Pressure: HIGH
   💸 Avg Borrow Rate: 0.000850
   📈 RSI: 76.32
   🎯 Momentum Signals: OVERBOUGHT, BELOW_SMA20
```

## Architecture

```
bitfinex_trader/
├── api/                    # Bitfinex API client
│   ├── __init__.py
│   └── client.py          # REST API integration
├── analysis/              # Market analysis modules
│   ├── __init__.py
│   └── shorts_analyzer.py # Short opportunity detection
├── trading/               # Trading execution
│   ├── __init__.py
│   └── trader.py         # Order management
└── utils/                 # Utilities
    ├── __init__.py
    └── config.py         # Configuration management
```

## Development

### Testing
```bash
# Run with dry-run mode for safe testing
python main.py trade --dry-run

# Test specific symbols
python main.py analyze --symbols tBTCUSD --detailed
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit a pull request

## Disclaimer

⚠️ **Trading Risk Warning**

Cryptocurrency trading involves substantial risk of loss. This tool is for informational and educational purposes. Past performance does not guarantee future results. Always:

- Start with small position sizes
- Use dry-run mode extensively
- Understand the risks involved
- Never invest more than you can afford to lose
- Consider seeking professional financial advice

The authors are not responsible for any financial losses incurred through the use of this software.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
