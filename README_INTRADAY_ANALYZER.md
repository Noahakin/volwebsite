# Intraday Swing Analyzer

A comprehensive Python tool that analyzes NASDAQ, NYSE, and major ETF stocks to identify those with the largest and most consistent intraday percentage swings.

## Features

- 📊 **Comprehensive Analysis**: Scans 1000+ NASDAQ, NYSE, and major ETF tickers
- 📈 **Multiple Time Windows**: Analyzes today, 3-day, 7-day, and 30-day periods
- 📉 **Advanced Metrics**: 
  - Average intraday % range
  - Realized volatility (annualized)
  - Consistency scores
  - Swing day counts (>2%, >3%)
  - Extreme move detection (>2 standard deviations)
- 🏆 **Multiple Rankings**:
  - Highest average intraday movers
  - Most consistent intraday volatility
  - Most >2% swing days
  - Most >3% swing days
  - Most extreme move days
- 💾 **CSV Export**: All rankings exported to CSV files
- ⚡ **Efficient Processing**: Batch processing with caching for performance
- 🎨 **Colored Output**: Real-time colored console output

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Script

```bash
python intraday_swing_analyzer.py
```

## How It Works

### Data Collection

1. **Ticker Lists**: Fetches NASDAQ and NYSE tickers from APIs, with fallback to static lists
2. **Major ETFs**: Includes 50+ major ETFs (SPY, QQQ, sector ETFs, leveraged ETFs, etc.)
3. **Data Fetching**: Uses yfinance to get intraday (5-minute) and daily price data

### Calculations

For each ticker, the script computes:

1. **Intraday % Range**: `(High - Low) / Open * 100`
   - Measures the percentage swing within each trading day

2. **Realized Volatility**: Annualized standard deviation of log returns
   - Calculated using rolling windows

3. **Consistency Score**: `Average Range / Standard Deviation of Range`
   - Higher score = more consistent intraday swings

4. **Swing Day Counts**: Number of days with swings exceeding thresholds
   - >2% swing days
   - >3% swing days
   - >2 standard deviation moves (extreme days)

### Time Windows

Analysis is performed for four time windows:

- **Today**: Most recent trading day
- **Last 3 Days**: Last 3 trading days
- **Last 7 Days**: Last 7 trading days  
- **Last 30 Days**: Last 30 trading days

### Rankings Generated

For each time window, the script generates 5 ranking tables:

1. **Highest Average Intraday % Movers**: Stocks with largest average daily ranges
2. **Most Consistent**: Highest consistency score (low std / high avg)
3. **Most >2% Swing Days**: Stocks with most days exceeding 2% intraday range
4. **Most >3% Swing Days**: Stocks with most days exceeding 3% intraday range
5. **Most Extreme Move Days**: Stocks with most >2σ moves

Each ranking is generated for:
- **All Tickers**: Combined stocks and ETFs
- **Stocks Only**: NASDAQ and NYSE stocks
- **ETFs Only**: Exchange-traded funds

## Output

### Console Output

The script prints formatted tables to the console with colored output:

```
================================================================================
INTRADAY SWING RANKINGS - LAST 30 DAYS
================================================================================

────────────────────────────────────────────────────────────────────────────────
ALL
────────────────────────────────────────────────────────────────────────────────

Top 20: Highest Avg Range
────────────────────────────────────────────────────────────────────────────────
ticker  avg_intraday_range  std_intraday_range  consistency_score  ...
AAPL    2.45                0.32                7.65               ...
...
```

### CSV Files

All rankings are exported to the `output/` directory:

```
output/
├── all_highest_avg_range_last_30_days.csv
├── all_most_consistent_last_30_days.csv
├── all_most_2pct_swings_last_30_days.csv
├── all_most_3pct_swings_last_30_days.csv
├── all_most_extreme_moves_last_30_days.csv
├── stocks_highest_avg_range_last_30_days.csv
├── stocks_most_consistent_last_30_days.csv
├── ...
└── etfs_most_extreme_moves_today.csv
```

Each CSV contains the top 20 tickers for that ranking with all relevant metrics.

## Configuration

Edit constants in `intraday_swing_analyzer.py`:

```python
MIN_DAYS_REQUIRED = 5          # Minimum days of data required
SWING_THRESHOLDS = [2.0, 3.0]  # Percentage thresholds for swing days
BATCH_SIZE = 100               # Process tickers in batches
CACHE_EXPIRY_HOURS = 1         # Cache expires after 1 hour
```

## Performance

- **Processing Speed**: ~50-100 tickers per minute (depends on API rate limits)
- **Full Analysis Time**: ~10-20 minutes for 1000+ tickers
- **Memory Usage**: ~500 MB - 1 GB
- **Cache**: Results cached for 1 hour to speed up re-runs

## Understanding the Metrics

### Average Intraday Range

The mean percentage swing within a trading day. Higher values indicate more volatile intraday price action.

**Example**: If a stock has an average intraday range of 3%, it typically swings 3% from high to low each day.

### Consistency Score

`Average Range / Standard Deviation of Range`

- **High Score (>5)**: Consistent intraday swings (predictable volatility)
- **Low Score (<2)**: Inconsistent swings (unpredictable volatility)

**Example**: A stock with avg=3% and std=0.5% has consistency=6.0 (very consistent)

### Realized Volatility

Annualized standard deviation of log returns. Measures overall price volatility.

- **Low (<20%)**: Stable stock
- **Medium (20-40%)**: Moderate volatility
- **High (>40%)**: High volatility

### Swing Days

Count of days where intraday range exceeded thresholds:

- **>2% Swing Days**: Days with >2% intraday range
- **>3% Swing Days**: Days with >3% intraday range
- **Extreme Move Days**: Days where range > mean + 2*std (statistical outliers)

## Use Cases

1. **Day Trading**: Identify stocks with consistent intraday volatility for day trading
2. **Volatility Trading**: Find stocks with high realized volatility for options strategies
3. **Risk Management**: Identify stocks with extreme move potential
4. **Market Research**: Understand intraday behavior patterns across markets
5. **ETF Analysis**: Compare ETF intraday characteristics

## Troubleshooting

### "No data for ticker" warnings

Some tickers may not have sufficient historical data. This is normal and the script will skip them.

### Rate Limiting

If you see many errors, yfinance may be rate-limiting. The script includes:
- Batch processing to limit concurrent requests
- Caching to avoid redundant API calls
- Automatic retries

### Insufficient Data

Some tickers may not have enough data for all time windows. The script requires:
- Minimum 5 days for any analysis
- 30 days for full 30-day window analysis

### Cache Issues

If you want to force a fresh data fetch:
```bash
rm intraday_cache.json
python intraday_swing_analyzer.py
```

## Limitations

1. **Data Delay**: yfinance data may have 15-20 minute delays
2. **Market Hours**: Best results during/after market hours when data is complete
3. **Ticker Coverage**: Some tickers may not be available or have insufficient data
4. **API Limits**: Free APIs have rate limits (script handles this automatically)

## Advanced Usage

### Custom Ticker Lists

Modify the `get_tickers()` function to add custom ticker lists:

```python
def get_tickers():
    # Add your custom tickers
    custom_tickers = ['YOUR', 'TICKERS', 'HERE']
    ...
```

### Different Time Windows

Modify the `windows` list in `main()`:

```python
windows = ['today', 'last_3_days', 'last_7_days', 'last_30_days', 'last_60_days']
```

### Custom Swing Thresholds

Edit `SWING_THRESHOLDS`:

```python
SWING_THRESHOLDS = [1.5, 2.0, 2.5, 3.0, 5.0]  # Multiple thresholds
```

## Example Output Interpretation

```
Top 20: Highest Avg Range
ticker  avg_intraday_range  consistency_score  swing_2pct_days
TSLA    4.23                3.45               18
NVDA    3.87                4.12               15
...
```

This shows:
- TSLA has the highest average intraday range (4.23%)
- It's relatively consistent (score 3.45)
- It had 18 days with >2% swings in the period

## License

This project is provided as-is for educational and personal use.

## Disclaimer

This tool is for informational purposes only. It does not constitute financial advice. Always do your own research before making investment decisions. Past performance does not guarantee future results.

---

**Happy Analyzing! 📊📈**

