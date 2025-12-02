# NASDAQ Volatility Scanner

A real-time monitoring system that scans all NASDAQ-listed stocks for intraday price moves exceeding 2 standard deviations and sends Telegram alerts.

## Features

- 🔍 **Comprehensive Scanning**: Monitors 3,000+ NASDAQ-listed tickers
- 📊 **Statistical Analysis**: Uses rolling volatility and Z-score calculations
- 📱 **Telegram Alerts**: Instant notifications when 2σ+ moves are detected
- ⚡ **Efficient Processing**: Concurrent batch processing with asyncio
- 🛡️ **Rate Limiting**: Built-in protection against API limits
- 🎨 **Colored Logging**: Real-time colored console output for monitoring
- 🔄 **Cooldown System**: Prevents duplicate alerts within 1 hour

## How It Works

1. **Data Collection**: Fetches 5-minute intraday price data for all NASDAQ tickers using yfinance
2. **Volatility Calculation**: Computes rolling standard deviation of log returns over the last 20-30 days
3. **Z-Score Detection**: Calculates Z-score = (current return - mean) / volatility
4. **Alert Trigger**: Sends Telegram notification when |Z-score| > 2.0
5. **Continuous Monitoring**: Scans every 60 seconds during operation

## Prerequisites

- Python 3.8 or higher
- Telegram Bot Token and Chat ID
- Internet connection for data fetching

## Installation

### 1. Clone or Download

```bash
# Download the script
# nasdaq_volatility_scanner.py
# requirements.txt
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Telegram Bot

#### Step 1: Create a Telegram Bot

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` command
3. Follow the instructions to name your bot
4. Copy the **Bot Token** (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

#### Step 2: Get Your Chat ID

1. Search for [@userinfobot](https://t.me/userinfobot) on Telegram
2. Start a conversation - it will reply with your Chat ID (a number like `123456789`)
3. Alternatively, send a message to your bot, then visit:
   ```
   https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
   ```
   Look for `"chat":{"id":123456789}` in the response

### 4. Set Environment Variables

#### Windows (PowerShell)

```powershell
$env:TELEGRAM_BOT_TOKEN="your_bot_token_here"
$env:TELEGRAM_CHAT_ID="your_chat_id_here"
```

#### Windows (Command Prompt)

```cmd
set TELEGRAM_BOT_TOKEN=your_bot_token_here
set TELEGRAM_CHAT_ID=your_chat_id_here
```

#### Linux/Mac

```bash
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
export TELEGRAM_CHAT_ID="your_chat_id_here"
```

#### Permanent Setup (Windows)

1. Open System Properties → Environment Variables
2. Add new User variables:
   - `TELEGRAM_BOT_TOKEN` = your bot token
   - `TELEGRAM_CHAT_ID` = your chat ID

#### Permanent Setup (Linux/Mac)

Add to `~/.bashrc` or `~/.zshrc`:

```bash
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
export TELEGRAM_CHAT_ID="your_chat_id_here"
```

Then reload:
```bash
source ~/.bashrc
```

## Usage

### Basic Usage

```bash
python nasdaq_volatility_scanner.py
```

### Running in Background

#### Windows

```powershell
# Run in background
Start-Process python -ArgumentList "nasdaq_volatility_scanner.py" -WindowStyle Hidden

# Or use Task Scheduler for automatic startup
```

#### Linux/Mac

```bash
# Run in background with nohup
nohup python nasdaq_volatility_scanner.py > scanner.log 2>&1 &

# Or use screen/tmux
screen -S scanner
python nasdaq_volatility_scanner.py
# Press Ctrl+A then D to detach
```

## Configuration

Edit the configuration constants in `nasdaq_volatility_scanner.py`:

```python
SCAN_INTERVAL = 60              # Seconds between scans
VOLATILITY_WINDOW_DAYS = 20     # Days of history for volatility
MIN_BARS_REQUIRED = 100        # Minimum bars needed
Z_SCORE_THRESHOLD = 2.0        # Alert threshold (2 = 2 standard deviations)
ALERT_COOLDOWN_HOURS = 1       # Hours before re-alerting same ticker
BATCH_SIZE = 50                # Tickers processed concurrently
```

## Deployment Options

### Option 1: Local Machine

Simply run the script on your computer. It will continue monitoring as long as the computer is on and connected to the internet.

### Option 2: Cloud Platforms (Free Tiers)

#### Railway

1. Sign up at [railway.app](https://railway.app)
2. Create a new project
3. Deploy from GitHub or upload files
4. Set environment variables in Railway dashboard
5. Deploy and run

#### Render

1. Sign up at [render.com](https://render.com)
2. Create a new Web Service
3. Connect your repository or upload files
4. Set environment variables
5. Use "Background Worker" type
6. Deploy

#### PythonAnywhere

1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload files via Files tab
3. Set environment variables in Web → Environment variables
4. Run via Tasks or Always-on task

### Option 3: VPS (DigitalOcean, AWS, etc.)

1. Set up a Linux VPS
2. Install Python and dependencies
3. Use `screen` or `tmux` to run in background
4. Or set up as a systemd service

## Understanding the Alerts

When a 2σ+ move is detected, you'll receive a Telegram message like:

```
🚨 2σ+ Intraday Move Detected

Ticker: AAPL
Z-score: 2.45
Price Move: +3.21%
Direction: 📈 UP
Time: 2024-01-15 14:32:15
Current Price: $185.23
```

- **Z-score**: Number of standard deviations from the mean
  - |Z| > 2.0 = Significant move (95% confidence)
  - |Z| > 3.0 = Extreme move (99.7% confidence)
- **Price Move**: Percentage change in the current period
- **Direction**: Whether price moved up or down

## Logging

The script creates two log outputs:

1. **Console Output**: Colored real-time logs
   - 🟢 Green: Success messages
   - 🔵 Cyan: Info messages
   - 🟡 Yellow: Warnings
   - 🔴 Red: Errors

2. **File Log**: `nasdaq_scanner.log` - Complete log history

## Troubleshooting

### "No data for ticker" warnings

Some tickers may not have sufficient intraday data. This is normal and the script will skip them.

### Rate Limiting

If you see many errors, yfinance may be rate-limiting. The script includes:
- Batch processing to limit concurrent requests
- Automatic retries with exponential backoff
- Delays between batches

### Telegram Not Sending

1. Verify environment variables are set:
   ```bash
   echo $TELEGRAM_BOT_TOKEN
   echo $TELEGRAM_CHAT_ID
   ```

2. Test your bot token:
   ```bash
   curl "https://api.telegram.org/bot<YOUR_TOKEN>/getMe"
   ```

3. Make sure you've started a conversation with your bot

### Getting NASDAQ Ticker List

The script tries multiple methods to get NASDAQ tickers:
1. NASDAQ API (primary)
2. Fallback to static list

For a more comprehensive list, you can:
- Download NASDAQ company list CSV from nasdaq.com
- Save as `nasdaq_tickers.csv` with a "Symbol" or "Ticker" column
- The script will automatically use it

## Performance

- **Processing Speed**: ~50 tickers per second (with batching)
- **Full Scan Time**: ~60-120 seconds for 3,000+ tickers
- **Memory Usage**: ~200-500 MB
- **CPU Usage**: Low to moderate (depends on batch size)

## Limitations

1. **Data Delay**: yfinance intraday data may have 15-20 minute delays
2. **Rate Limits**: Free APIs have rate limits (script handles this)
3. **Market Hours**: Best results during market hours (9:30 AM - 4:00 PM ET)
4. **Ticker Coverage**: Some tickers may not have sufficient historical data

## Advanced Usage

### Custom Ticker List

Create a file `nasdaq_tickers.csv` with a "Symbol" column:

```csv
Symbol
AAPL
MSFT
GOOGL
...
```

The script will automatically detect and use it.

### Running During Market Hours Only

Modify the main loop to check market hours:

```python
from datetime import datetime, time

def is_market_hours():
    now = datetime.now()
    market_open = time(9, 30)  # 9:30 AM ET
    market_close = time(16, 0)  # 4:00 PM ET
    # Add timezone handling as needed
    return market_open <= now.time() <= market_close
```

## License

This project is provided as-is for educational and personal use.

## Disclaimer

This tool is for informational purposes only. It does not constitute financial advice. Always do your own research before making investment decisions. Past performance does not guarantee future results.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the logs in `nasdaq_scanner.log`
3. Verify your Telegram bot setup
4. Ensure all dependencies are installed

## Contributing

Feel free to improve:
- Better ticker list fetching
- More sophisticated volatility models
- Additional alert channels (email, Discord, etc.)
- Performance optimizations

---

**Happy Trading! 📈📉**

