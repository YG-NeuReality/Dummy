# Bitfinex Trading Tool - Examples

This directory contains practical examples showing how to use the Bitfinex Crypto Short Trading Tool effectively.

## 📁 Available Examples

### 1. **basic_analysis.py** - Getting Started
Perfect for beginners who want to understand the basic analysis features.

```bash
python examples/basic_analysis.py
```

**What it demonstrates:**
- Basic cryptocurrency analysis on default symbols
- Analysis of specific symbols (Bitcoin, Ethereum)
- Detailed analysis with technical indicators

**Use when:** You're new to the tool and want to understand the analysis features.

---

### 2. **dry_run_trading.py** - Safe Trading Simulation
Learn trading without risking real money using simulation mode.

```bash
python examples/dry_run_trading.py
```

**What it demonstrates:**
- Safe trading simulation (no real trades)
- Trading analysis on specific symbols
- Position monitoring
- Account information retrieval

**Use when:** You want to test trading strategies safely before using real money.

---

### 3. **configuration_examples.py** - Setup for Different Risk Profiles
Learn how to configure the tool for different trading styles and risk levels.

```bash
python examples/configuration_examples.py
```

**What it demonstrates:**
- Conservative configuration (low risk)
- Basic configuration (moderate risk)
- Aggressive configuration (high risk)
- Parameter explanations and best practices

**Use when:** You need to set up the tool for your specific risk tolerance and trading goals.

---

### 4. **advanced_usage.py** - Power User Features
Advanced features for experienced traders and developers.

```bash
python examples/advanced_usage.py
```

**What it demonstrates:**
- JSON output for programmatic processing
- Detailed single-symbol analysis
- Alternative cryptocurrency analysis
- Workflow automation scripts
- Continuous monitoring setup

**Use when:** You want to integrate the tool into automated workflows or build custom solutions.

---

## 🚀 Getting Started

### Prerequisites
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API credentials:**
   ```bash
   cp .env.example .env
   # Edit .env with your Bitfinex API credentials
   ```

3. **Get Bitfinex API keys:** https://www.bitfinex.com/api

### Quick Start
1. **Run basic analysis:** `python examples/basic_analysis.py`
2. **Try safe trading:** `python examples/dry_run_trading.py`
3. **Configure for your needs:** `python examples/configuration_examples.py`
4. **Explore advanced features:** `python examples/advanced_usage.py`

## 📊 Example Workflow

### For Beginners:
1. Start with `basic_analysis.py` to understand the tool
2. Run `configuration_examples.py` to set up your risk profile
3. Practice with `dry_run_trading.py` until comfortable
4. Gradually move to real trading with `python main.py trade --execute`

### For Experienced Traders:
1. Jump to `advanced_usage.py` for power features
2. Use JSON output to integrate with your existing tools
3. Set up automated monitoring and trading workflows
4. Build custom notification and analysis systems

## ⚠️ Safety Notes

- **Always start with dry-run mode** - Never risk real money until you understand the tool
- **Start with small amounts** - Use conservative configurations initially
- **Test thoroughly** - Run examples multiple times to understand behavior
- **Monitor actively** - Don't leave automated trading unattended
- **Understand risks** - Cryptocurrency trading involves significant risk

## 🔧 Configuration Risk Levels

| Risk Level | RISK_PERCENTAGE | MAX_TRADE_VOLUME | Description |
|------------|----------------|------------------|-------------|
| Conservative | 0.005 (0.5%) | $50 | Safe for learning |
| Basic | 0.01 (1%) | $100 | Moderate risk |
| Aggressive | 0.05 (5%) | $1000 | High risk/reward |

## 📈 Command Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `analyze` | Market analysis | `python main.py analyze --symbols tBTCUSD` |
| `trade --dry-run` | Safe simulation | `python main.py trade --dry-run` |
| `trade --execute` | Real trading | `python main.py trade --execute` |
| `positions` | Check positions | `python main.py positions` |
| `account` | Account info | `python main.py account` |

## 🆘 Troubleshooting

**"Configuration validation failed"**
- Check your .env file exists
- Verify API credentials are correct
- Ensure API keys have trading permissions

**"Analysis timed out"**
- Check internet connection
- Verify Bitfinex API is accessible
- Try with fewer symbols

**"Import errors"**
- Run `pip install -r requirements.txt`
- Check Python version (3.7+ required)

## 📞 Support

- Check the main [README.md](../README.md) for detailed documentation
- Review error messages carefully - they usually indicate the issue
- Test with dry-run mode first to isolate problems
- Ensure API credentials have the required permissions

---

**Happy Trading! 🚀**

*Remember: Only trade what you can afford to lose, and always understand the tools you're using.*