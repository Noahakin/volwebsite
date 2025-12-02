#!/usr/bin/env python3
"""
NASDAQ Volatility Scanner
Continuously monitors all NASDAQ-listed tickers for intraday price moves > 2 standard deviations.
Sends Telegram alerts when significant moves are detected.
"""

import os
import sys
import asyncio
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
import numpy as np
import pandas as pd
import yfinance as yf
import requests
from colorama import init, Fore, Style

# Initialize colorama for Windows compatibility
init(autoreset=True)

# Configuration
SCAN_INTERVAL = 60  # seconds
VOLATILITY_WINDOW_DAYS = 20  # days of historical data for volatility calculation
MIN_BARS_REQUIRED = 100  # minimum bars needed for reliable volatility calculation
Z_SCORE_THRESHOLD = 2.0  # alert when |Z| > 2
ALERT_COOLDOWN_HOURS = 1  # don't re-alert same ticker within this time
BATCH_SIZE = 50  # number of tickers to fetch in parallel
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

# Telegram API
TELEGRAM_API_URL = "https://api.telegram.org/bot{token}/sendMessage"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('nasdaq_scanner.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for console output"""
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT,
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, '')
        record.levelname = f"{log_color}{record.levelname}{Style.RESET_ALL}"
        return super().format(record)


# Apply colored formatter to console handler
for handler in logger.handlers:
    if isinstance(handler, logging.StreamHandler) and not isinstance(handler, logging.FileHandler):
        handler.setFormatter(ColoredFormatter('%(asctime)s - %(levelname)s - %(message)s'))


def get_nasdaq_tickers() -> List[str]:
    """
    Fetch list of all NASDAQ-listed tickers from a free source.
    Falls back to a static list if web scraping fails.
    """
    tickers = []
    
    # Method 1: Try to fetch from NASDAQ website via pandas
    try:
        logger.info(f"{Fore.CYAN}Fetching NASDAQ ticker list...{Style.RESET_ALL}")
        # Use pandas to read NASDAQ ticker list
        url = "https://old.nasdaq.com/creening/company-list.aspx"
        
        # Alternative: Use a CSV from NASDAQ or a reliable source
        # For now, we'll use a combination of methods
        
        # Try fetching from a static source
        nasdaq_url = "https://www.nasdaq.com/api/v1/screener"
        
        # Since direct API might not work, we'll use yfinance to get a comprehensive list
        # or fetch from a known CSV source
        
        # Method 2: Use a known CSV source (backup)
        csv_url = "https://www.nasdaq.com/api/v1/screener"
        
        # For reliability, we'll fetch from multiple sources or use a static list
        # Let's try using yfinance to get tickers from QQQ and expand
        
        logger.info(f"{Fore.YELLOW}Using alternative method to get NASDAQ tickers...{Style.RESET_ALL}")
        
        # Get tickers from NASDAQ website using requests
        try:
            # NASDAQ provides a company list endpoint
            response = requests.get(
                "https://api.nasdaq.com/api/screener/stocks",
                params={"tableonly": "true", "limit": "10000", "offset": "0"},
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and 'rows' in data['data']:
                    tickers = [row.get('symbol', '').strip() for row in data['data']['rows'] if row.get('symbol')]
                    tickers = [t for t in tickers if t and len(t) <= 5]  # Filter valid tickers
                    logger.info(f"{Fore.GREEN}✓ Fetched {len(tickers)} tickers from NASDAQ API{Style.RESET_ALL}")
                    return tickers
        except Exception as e:
            logger.warning(f"{Fore.YELLOW}NASDAQ API failed: {e}{Style.RESET_ALL}")
        
        # Fallback: Use a static list of major NASDAQ tickers
        # This is a backup - in production, you'd want a more comprehensive list
        logger.warning(f"{Fore.YELLOW}Using fallback method: fetching from known NASDAQ ETFs...{Style.RESET_ALL}")
        
        # Get tickers from major NASDAQ ETFs
        etf_tickers = ['QQQ', 'ONEQ', 'QQQM']
        all_tickers = set()
        
        for etf in etf_tickers:
            try:
                ticker = yf.Ticker(etf)
                # Try to get holdings (may not always work)
                info = ticker.info
                # Alternative: use a known list
            except:
                pass
        
        # Use a comprehensive static list as ultimate fallback
        # For demo, we'll use a curated list, but in production you'd maintain this better
        if not tickers:
            logger.warning(f"{Fore.YELLOW}Using static NASDAQ ticker list (limited){Style.RESET_ALL}")
            # This would be a comprehensive list - for now using a sample
            tickers = _get_static_nasdaq_list()
            
    except Exception as e:
        logger.error(f"{Fore.RED}Error fetching NASDAQ tickers: {e}{Style.RESET_ALL}")
        tickers = _get_static_nasdaq_list()
    
    if not tickers:
        logger.error(f"{Fore.RED}No tickers found! Using minimal fallback list.{Style.RESET_ALL}")
        tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA', 'NFLX']
    
    logger.info(f"{Fore.GREEN}✓ Using {len(tickers)} NASDAQ tickers{Style.RESET_ALL}")
    return tickers


def _get_static_nasdaq_list() -> List[str]:
    """
    Fallback static list of NASDAQ tickers.
    In production, maintain a comprehensive CSV file.
    """
    # Major NASDAQ companies - this is a sample
    # For full implementation, you'd load from a CSV file
    major_tickers = [
        'AAPL', 'MSFT', 'GOOGL', 'GOOG', 'AMZN', 'META', 'TSLA', 'NVDA', 'NFLX', 'AMD',
        'INTC', 'CMCSA', 'ADBE', 'PYPL', 'COST', 'AVGO', 'PEP', 'CSCO', 'TMUS', 'QCOM',
        'TXN', 'AMGN', 'ISRG', 'INTU', 'BKNG', 'AMAT', 'VRSK', 'ADI', 'GILD', 'ADP',
        'FISV', 'KLAC', 'CDNS', 'SNPS', 'CTSH', 'NXPI', 'MCHP', 'PAYX', 'FTNT', 'IDXX',
        'FAST', 'CTAS', 'WDAY', 'ODFL', 'DXCM', 'ROST', 'PCAR', 'BKR', 'ANSS', 'TEAM',
        'ALGN', 'VRTX', 'CPRT', 'CDW', 'ZS', 'CRWD', 'MRNA', 'DOCN', 'OKTA', 'NET',
        'DDOG', 'FROG', 'ASAN', 'ESTC', 'ZM', 'PTON', 'RBLX', 'HOOD', 'SOFI', 'UPST'
    ]
    
    # Try to load from a CSV if it exists
    csv_path = 'nasdaq_tickers.csv'
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            if 'Symbol' in df.columns:
                return df['Symbol'].dropna().astype(str).tolist()
            elif 'Ticker' in df.columns:
                return df['Ticker'].dropna().astype(str).tolist()
        except Exception as e:
            logger.warning(f"Could not load CSV: {e}")
    
    return major_tickers


async def get_intraday_data(ticker: str, interval: str = "5m", period: str = "5d") -> Optional[pd.DataFrame]:
    """
    Fetch intraday price data for a ticker using yfinance.
    
    Args:
        ticker: Stock symbol
        interval: Data interval (1m, 5m, 15m, etc.)
        period: Period to fetch (1d, 5d, 1mo, etc.)
    
    Returns:
        DataFrame with OHLCV data or None if failed
    """
    for attempt in range(MAX_RETRIES):
        try:
            yf_ticker = yf.Ticker(ticker)
            data = yf_ticker.history(interval=interval, period=period, prepost=False)
            
            if data.empty:
                logger.debug(f"No data for {ticker}")
                return None
            
            # Ensure we have required columns
            if 'Close' not in data.columns:
                return None
            
            return data
            
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(RETRY_DELAY * (attempt + 1))
                continue
            logger.debug(f"Error fetching {ticker}: {e}")
            return None
    
    return None


def compute_zscore(data: pd.DataFrame) -> Optional[Tuple[float, float, Dict]]:
    """
    Compute Z-score for the most recent price move.
    
    Args:
        data: DataFrame with OHLCV data
    
    Returns:
        Tuple of (zscore, percent_move, stats_dict) or None if insufficient data
    """
    if data is None or len(data) < MIN_BARS_REQUIRED:
        return None
    
    try:
        # Calculate log returns
        closes = data['Close'].values
        log_returns = np.diff(np.log(closes))
        
        if len(log_returns) < MIN_BARS_REQUIRED:
            return None
        
        # Calculate rolling statistics
        # Use the last 20-30 days worth of data
        window_size = min(len(log_returns), VOLATILITY_WINDOW_DAYS * 78)  # ~78 5-min bars per day
        
        if window_size < 50:  # Need minimum data
            return None
        
        # Get recent returns for volatility calculation
        recent_returns = log_returns[-window_size:]
        
        # Calculate mean and standard deviation
        mean_return = np.mean(recent_returns)
        std_return = np.std(recent_returns, ddof=1)  # Sample std dev
        
        if std_return == 0 or np.isnan(std_return):
            return None
        
        # Current return (most recent)
        current_return = log_returns[-1]
        
        # Calculate Z-score
        zscore = (current_return - mean_return) / std_return
        
        # Calculate percent move
        if len(closes) >= 2:
            percent_move = ((closes[-1] - closes[-2]) / closes[-2]) * 100
        else:
            percent_move = 0.0
        
        stats = {
            'mean_return': mean_return,
            'std_return': std_return,
            'current_return': current_return,
            'current_price': closes[-1],
            'previous_price': closes[-2] if len(closes) >= 2 else closes[-1],
            'bars_used': len(recent_returns)
        }
        
        return (zscore, percent_move, stats)
        
    except Exception as e:
        logger.debug(f"Error computing Z-score: {e}")
        return None


async def send_telegram_message(message: str) -> bool:
    """
    Send a message via Telegram Bot API.
    
    Args:
        message: Message text to send
    
    Returns:
        True if successful, False otherwise
    """
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if not token or not chat_id:
        logger.error(f"{Fore.RED}Telegram credentials not set!{Style.RESET_ALL}")
        return False
    
    url = TELEGRAM_API_URL.format(token=token)
    
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except Exception as e:
        logger.error(f"{Fore.RED}Failed to send Telegram message: {e}{Style.RESET_ALL}")
        return False


class VolatilityScanner:
    """Main scanner class that manages the monitoring loop"""
    
    def __init__(self):
        self.tickers: List[str] = []
        self.alert_history: Dict[str, datetime] = {}  # ticker -> last alert time
        self.volatility_cache: Dict[str, Dict] = {}  # ticker -> cached stats
        self.scan_count = 0
        self.alerts_sent = 0
        self.errors = 0
        
    async def initialize(self):
        """Initialize the scanner by fetching ticker list"""
        logger.info(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        logger.info(f"{Fore.CYAN}Initializing NASDAQ Volatility Scanner{Style.RESET_ALL}")
        logger.info(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        self.tickers = get_nasdaq_tickers()
        logger.info(f"{Fore.GREEN}✓ Loaded {len(self.tickers)} tickers{Style.RESET_ALL}")
        
        # Verify Telegram credentials
        if not os.getenv('TELEGRAM_BOT_TOKEN') or not os.getenv('TELEGRAM_CHAT_ID'):
            logger.warning(f"{Fore.YELLOW}⚠ Telegram credentials not set. Alerts will not be sent.{Style.RESET_ALL}")
        else:
            logger.info(f"{Fore.GREEN}✓ Telegram credentials configured{Style.RESET_ALL}")
    
    async def process_ticker(self, ticker: str) -> Optional[Dict]:
        """
        Process a single ticker: fetch data, compute Z-score, check for alerts.
        
        Returns:
            Alert dict if signal detected, None otherwise
        """
        try:
            # Fetch intraday data
            data = await get_intraday_data(ticker, interval="5m", period="5d")
            
            if data is None:
                return None
            
            # Compute Z-score
            result = compute_zscore(data)
            
            if result is None:
                return None
            
            zscore, percent_move, stats = result
            
            # Check if Z-score exceeds threshold
            if abs(zscore) > Z_SCORE_THRESHOLD:
                # Check cooldown
                last_alert = self.alert_history.get(ticker)
                if last_alert and (datetime.now() - last_alert) < timedelta(hours=ALERT_COOLDOWN_HOURS):
                    return None  # Still in cooldown
                
                # Prepare alert
                alert = {
                    'ticker': ticker,
                    'zscore': zscore,
                    'percent_move': percent_move,
                    'stats': stats,
                    'timestamp': datetime.now()
                }
                
                # Update alert history
                self.alert_history[ticker] = datetime.now()
                
                return alert
            
            return None
            
        except Exception as e:
            self.errors += 1
            logger.debug(f"Error processing {ticker}: {e}")
            return None
    
    async def process_ticker_batch(self, tickers: List[str]) -> List[Dict]:
        """Process a batch of tickers concurrently"""
        tasks = [self.process_ticker(ticker) for ticker in tickers]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        alerts = []
        for result in results:
            if isinstance(result, Exception):
                self.errors += 1
                continue
            if result is not None:
                alerts.append(result)
        
        return alerts
    
    async def send_alert(self, alert: Dict):
        """Format and send a Telegram alert"""
        ticker = alert['ticker']
        zscore = alert['zscore']
        percent_move = alert['percent_move']
        timestamp = alert['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        
        direction = "📈 UP" if percent_move > 0 else "📉 DOWN"
        emoji = "🚨" if abs(zscore) > 3 else "⚠️"
        
        message = f"""{emoji} <b>2σ+ Intraday Move Detected</b>

<b>Ticker:</b> {ticker}
<b>Z-score:</b> {zscore:.2f}
<b>Price Move:</b> {percent_move:+.2f}%
<b>Direction:</b> {direction}
<b>Time:</b> {timestamp}
<b>Current Price:</b> ${alert['stats']['current_price']:.2f}"""
        
        success = await send_telegram_message(message)
        if success:
            self.alerts_sent += 1
            logger.info(f"{Fore.GREEN}✓ Alert sent: {ticker} (Z={zscore:.2f}, {percent_move:+.2f}%){Style.RESET_ALL}")
        else:
            logger.error(f"{Fore.RED}✗ Failed to send alert for {ticker}{Style.RESET_ALL}")
    
    async def scan_cycle(self):
        """Perform one complete scan cycle of all tickers"""
        start_time = time.time()
        self.scan_count += 1
        
        logger.info(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        logger.info(f"{Fore.CYAN}Scan #{self.scan_count} - Processing {len(self.tickers)} tickers...{Style.RESET_ALL}")
        logger.info(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        all_alerts = []
        
        # Process tickers in batches to avoid overwhelming the API
        for i in range(0, len(self.tickers), BATCH_SIZE):
            batch = self.tickers[i:i + BATCH_SIZE]
            logger.info(f"{Fore.CYAN}Processing batch {i//BATCH_SIZE + 1}/{(len(self.tickers) + BATCH_SIZE - 1)//BATCH_SIZE} ({len(batch)} tickers)...{Style.RESET_ALL}")
            
            alerts = await self.process_ticker_batch(batch)
            all_alerts.extend(alerts)
            
            # Small delay between batches to avoid rate limits
            if i + BATCH_SIZE < len(self.tickers):
                await asyncio.sleep(1)
        
        # Send all alerts
        for alert in all_alerts:
            await self.send_alert(alert)
        
        elapsed = time.time() - start_time
        
        # Cleanup old alert history (older than cooldown period)
        cutoff_time = datetime.now() - timedelta(hours=ALERT_COOLDOWN_HOURS + 1)
        self.alert_history = {
            k: v for k, v in self.alert_history.items()
            if v > cutoff_time
        }
        
        logger.info(f"{Fore.GREEN}✓ Scan complete in {elapsed:.1f}s - {len(all_alerts)} alerts, {self.errors} errors{Style.RESET_ALL}")
        logger.info(f"{Fore.CYAN}Total stats: {self.scan_count} scans, {self.alerts_sent} alerts sent{Style.RESET_ALL}")
    
    async def run(self):
        """Main run loop"""
        await self.initialize()
        
        logger.info(f"{Fore.GREEN}Starting continuous monitoring (scan every {SCAN_INTERVAL}s)...{Style.RESET_ALL}")
        logger.info(f"{Fore.YELLOW}Press Ctrl+C to stop{Style.RESET_ALL}")
        
        try:
            while True:
                await self.scan_cycle()
                
                logger.info(f"{Fore.CYAN}Waiting {SCAN_INTERVAL} seconds until next scan...{Style.RESET_ALL}")
                await asyncio.sleep(SCAN_INTERVAL)
                
        except KeyboardInterrupt:
            logger.info(f"{Fore.YELLOW}Shutting down gracefully...{Style.RESET_ALL}")
        except Exception as e:
            logger.error(f"{Fore.RED}Fatal error: {e}{Style.RESET_ALL}")
            raise


async def main():
    """Entry point"""
    scanner = VolatilityScanner()
    await scanner.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info(f"{Fore.YELLOW}Scanner stopped by user{Style.RESET_ALL}")
    except Exception as e:
        logger.error(f"{Fore.RED}Fatal error: {e}{Style.RESET_ALL}")
        sys.exit(1)

