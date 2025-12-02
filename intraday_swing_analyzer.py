#!/usr/bin/env python3
"""
Intraday Swing Analyzer
Analyzes NASDAQ, NYSE, and major ETFs to identify stocks with largest and most consistent intraday swings.
"""

import os
import sys
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
import json
import warnings

# Suppress numpy warnings
warnings.filterwarnings('ignore', category=RuntimeWarning)
warnings.filterwarnings('ignore', category=UserWarning)

# Initialize colorama
init(autoreset=True)

# Configuration
MIN_DAYS_REQUIRED = 5  # Minimum days of data required
SWING_THRESHOLDS = [2.0, 3.0]  # Percentage thresholds for swing days
BATCH_SIZE = 100  # Process tickers in batches
CACHE_FILE = 'intraday_cache.json'
CACHE_EXPIRY_HOURS = 1  # Cache expires after 1 hour

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('intraday_analyzer.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def get_tickers() -> Dict[str, List[str]]:
    """
    Fetch tickers for NASDAQ, NYSE, and major ETFs.
    
    Returns:
        Dictionary with keys: 'nasdaq', 'nyse', 'etfs'
    """
    tickers = {
        'nasdaq': [],
        'nyse': [],
        'etfs': []
    }
    
    logger.info(f"{Fore.CYAN}Fetching ticker lists...{Style.RESET_ALL}")
    
    # Import comprehensive ticker lists
    try:
        from comprehensive_tickers import get_all_volatile_tickers
        ticker_data = get_all_volatile_tickers()
        tickers['etfs'] = ticker_data['etfs']
        tickers['nasdaq'] = ticker_data['stocks']
        logger.info(f"{Fore.GREEN}[OK] Loaded {len(ticker_data['etfs'])} ETFs and {len(ticker_data['stocks'])} stocks{Style.RESET_ALL}")
    except ImportError:
        # Fallback to basic lists if module not found
        logger.warning(f"{Fore.YELLOW}comprehensive_tickers.py not found, using basic lists{Style.RESET_ALL}")
        tickers['etfs'] = ['SPY', 'QQQ', 'TQQQ', 'SQQQ', 'SOXL', 'SOXS', 'BITO', 'GBTC']
        tickers['nasdaq'] = _get_static_nasdaq_list()
    
    # Try to fetch additional NASDAQ tickers and merge
    try:
        nasdaq_tickers = _fetch_nasdaq_tickers()
        if nasdaq_tickers:
            # Merge with existing, removing duplicates
            tickers['nasdaq'] = list(set(tickers['nasdaq'] + nasdaq_tickers))
            logger.info(f"{Fore.GREEN}[OK] Merged NASDAQ tickers: {len(tickers['nasdaq'])} total{Style.RESET_ALL}")
    except Exception as e:
        logger.warning(f"{Fore.YELLOW}Could not fetch NASDAQ tickers: {e}{Style.RESET_ALL}")
    
    # Try to fetch NYSE tickers and merge
    try:
        nyse_tickers = _fetch_nyse_tickers()
        if nyse_tickers:
            tickers['nyse'] = list(set(tickers.get('nyse', []) + nyse_tickers))
            logger.info(f"{Fore.GREEN}[OK] Loaded {len(nyse_tickers)} NYSE tickers{Style.RESET_ALL}")
    except Exception as e:
        logger.warning(f"{Fore.YELLOW}Could not fetch NYSE tickers: {e}{Style.RESET_ALL}")
        tickers['nyse'] = _get_static_nyse_list()
    
    # Combine all tickers
    all_tickers = list(set(tickers['nasdaq'] + tickers.get('nyse', []) + tickers['etfs']))
    logger.info(f"{Fore.GREEN}[OK] Total tickers to analyze: {len(all_tickers)}{Style.RESET_ALL}")
    
    return tickers


def _fetch_nasdaq_tickers() -> List[str]:
    """Fetch NASDAQ tickers from API"""
    try:
        response = requests.get(
            "https://api.nasdaq.com/api/screener/stocks",
            params={"tableonly": "true", "limit": "10000", "offset": "0"},
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and 'rows' in data['data']:
                tickers = [row.get('symbol', '').strip() for row in data['data']['rows'] if row.get('symbol')]
                return [t for t in tickers if t and len(t) <= 5]
    except:
        pass
    return []


def _fetch_nyse_tickers() -> List[str]:
    """Fetch NYSE tickers - similar approach"""
    # NYSE doesn't have as easy an API, so we'll use a combination
    # For now, return empty and use static list
    return []


def _get_static_nasdaq_list() -> List[str]:
    """Fallback static list of major NASDAQ tickers"""
    return [
        'AAPL', 'MSFT', 'GOOGL', 'GOOG', 'AMZN', 'META', 'TSLA', 'NVDA', 'NFLX', 'AMD',
        'INTC', 'CMCSA', 'ADBE', 'PYPL', 'COST', 'AVGO', 'PEP', 'CSCO', 'TMUS', 'QCOM',
        'TXN', 'AMGN', 'ISRG', 'INTU', 'BKNG', 'AMAT', 'VRSK', 'ADI', 'GILD', 'ADP',
        'FISV', 'KLAC', 'CDNS', 'SNPS', 'CTSH', 'NXPI', 'MCHP', 'PAYX', 'FTNT', 'IDXX',
        'FAST', 'CTAS', 'WDAY', 'ODFL', 'DXCM', 'ROST', 'PCAR', 'BKR', 'ANSS', 'TEAM',
        'ALGN', 'VRTX', 'CPRT', 'CDW', 'ZS', 'CRWD', 'MRNA', 'DOCN', 'OKTA', 'NET',
        'DDOG', 'FROG', 'ASAN', 'ESTC', 'ZM', 'PTON', 'RBLX', 'HOOD', 'SOFI', 'UPST',
        'LCID', 'RIVN', 'F', 'PLTR', 'SNOW', 'COIN', 'SQ', 'SHOP', 'TWLO', 'SPOT'
    ]


def _get_static_nyse_list() -> List[str]:
    """Fallback static list of major NYSE tickers"""
    return [
        'JPM', 'BAC', 'WFC', 'C', 'GS', 'MS', 'V', 'MA', 'AXP', 'COF',
        'JNJ', 'PG', 'KO', 'PEP', 'WMT', 'HD', 'MCD', 'NKE', 'DIS', 'VZ',
        'T', 'XOM', 'CVX', 'COP', 'SLB', 'BA', 'CAT', 'GE', 'MMM', 'HON',
        'UNH', 'CVS', 'CI', 'ANTM', 'LLY', 'ABBV', 'MRK', 'PFE', 'TMO', 'DHR',
        'NEE', 'DUK', 'SO', 'AEP', 'SRE', 'EXC', 'XEL', 'WEC', 'ES', 'ETR',
        'IBM', 'ORCL', 'CRM', 'ADP', 'FIS', 'FISV', 'ADSK', 'ANSS', 'CDNS', 'SNPS'
    ]


def get_intraday_data(ticker: str, period: str = "1mo") -> Optional[pd.DataFrame]:
    """
    Fetch intraday data for a ticker.
    
    Args:
        ticker: Stock symbol
        period: Period to fetch (1d, 5d, 1mo, 3mo, etc.)
    
    Returns:
        DataFrame with OHLCV data or None if failed
    """
    try:
        yf_ticker = yf.Ticker(ticker)
        # For intraday data, yfinance only allows up to 60 days
        # Try 5-minute data with max 60 days
        if period in ["2mo", "3mo"]:
            intraday_period = "60d"  # Max allowed for intraday
        else:
            intraday_period = period
        
        # Suppress yfinance errors
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                data = yf_ticker.history(interval="5m", period=intraday_period, prepost=False, raise_errors=False)
            except:
                data = pd.DataFrame()
        
        if data.empty:
            # Try daily data as fallback (daily data allows longer periods)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                try:
                    data = yf_ticker.history(period=period, prepost=False, raise_errors=False)
                except:
                    data = pd.DataFrame()
            if data.empty:
                return None
        
        # Ensure required columns exist
        required_cols = ['Open', 'High', 'Low', 'Close']
        if not all(col in data.columns for col in required_cols):
            return None
        
        return data
        
    except Exception as e:
        logger.debug(f"Error fetching {ticker}: {e}")
        return None


def compute_intraday_stats(data: pd.DataFrame, ticker: str) -> Optional[Dict]:
    """
    Compute intraday statistics for a ticker.
    
    Args:
        data: DataFrame with OHLCV data
        ticker: Stock symbol
    
    Returns:
        Dictionary with statistics or None if insufficient data
    """
    if data is None or len(data) < MIN_DAYS_REQUIRED:
        return None
    
    try:
        # Resample to daily if we have intraday data
        # Check if data is intraday (has time component) or daily
        if isinstance(data.index, pd.DatetimeIndex):
            # If we have intraday data, resample to daily
            # Check if this looks like intraday data (many bars per day)
            time_diffs = data.index.to_series().diff()
            avg_diff_minutes = time_diffs.median().total_seconds() / 60
            
            if avg_diff_minutes < 60:  # Likely intraday (bars < 1 hour apart)
                # Resample to business days, keeping only trading days
                daily_data = data.resample('B').agg({
                    'Open': 'first',
                    'High': 'max',
                    'Low': 'min',
                    'Close': 'last',
                    'Volume': 'sum'
                }).dropna()
            else:
                # Already daily or longer timeframe
                daily_data = data.copy()
        else:
            daily_data = data.copy()
        
        if len(daily_data) < MIN_DAYS_REQUIRED:
            return None
        
        # Calculate daily intraday % range: (high - low) / open
        daily_data['IntradayRange'] = ((daily_data['High'] - daily_data['Low']) / daily_data['Open']) * 100
        
        # Calculate log returns for realized volatility
        daily_data['LogReturn'] = np.log(daily_data['Close'] / daily_data['Close'].shift(1))
        # Calculate realized vol with division by zero protection
        rolling_std = daily_data['LogReturn'].rolling(window=min(20, len(daily_data))).std()
        daily_data['RealizedVol'] = rolling_std.replace([np.inf, -np.inf], np.nan).fillna(0) * np.sqrt(252) * 100
        # Replace any remaining invalid values
        daily_data['RealizedVol'] = daily_data['RealizedVol'].replace([np.inf, -np.inf, np.nan], 0)
        
        # Remove NaN values
        daily_data = daily_data.dropna(subset=['IntradayRange'])
        
        if len(daily_data) < MIN_DAYS_REQUIRED:
            return None
        
        # Get today's data (most recent)
        today_data = daily_data.iloc[-1] if len(daily_data) > 0 else None
        
        # Calculate statistics for different windows
        stats = {
            'ticker': ticker,
            'total_days': len(daily_data),
            'today': _compute_window_stats(daily_data.iloc[-1:]) if today_data is not None else None,
            'last_3_days': _compute_window_stats(daily_data.iloc[-3:]) if len(daily_data) >= 3 else None,
            'last_7_days': _compute_window_stats(daily_data.iloc[-7:]) if len(daily_data) >= 7 else None,
            'last_30_days': _compute_window_stats(daily_data.iloc[-30:]) if len(daily_data) >= 30 else None,
            'last_3_months': _compute_window_stats(daily_data.iloc[-90:]) if len(daily_data) >= 60 else None,
            'last_1_year': _compute_window_stats(daily_data.iloc[-252:]) if len(daily_data) >= 180 else None,
        }
        
        return stats
        
    except Exception as e:
        logger.debug(f"Error computing stats for {ticker}: {e}")
        return None


def _compute_window_stats(window_data: pd.DataFrame) -> Dict:
    """
    Compute statistics for a specific time window.
    
    Args:
        window_data: DataFrame with daily data for the window
    
    Returns:
        Dictionary with statistics
    """
    if window_data.empty or 'IntradayRange' not in window_data.columns:
        return None
    
    ranges = window_data['IntradayRange'].values
    log_returns = window_data['LogReturn'].dropna().values
    
    # Basic statistics with error handling
    if len(ranges) == 0:
        return None
    
    avg_range = np.mean(ranges)
    std_range = np.std(ranges, ddof=1) if len(ranges) > 1 else 0.0
    median_range = np.median(ranges)
    max_range = np.max(ranges)
    min_range = np.min(ranges)
    
    # Check for invalid values
    if np.isnan(avg_range) or np.isinf(avg_range):
        avg_range = 0.0
    if np.isnan(std_range) or np.isinf(std_range):
        std_range = 0.0
    
    # Daily standard deviation (std dev of daily ranges)
    daily_std = std_range if not (np.isnan(std_range) or np.isinf(std_range)) else 0.0
    
    # Standard deviation ranges (percentiles) with error handling
    if len(ranges) > 0:
        try:
            std_dev_ranges = {
                'std_dev_25th': float(np.percentile(ranges, 25)) if len(ranges) > 0 else 0.0,
                'std_dev_50th': float(np.percentile(ranges, 50)) if len(ranges) > 0 else 0.0,  # median
                'std_dev_75th': float(np.percentile(ranges, 75)) if len(ranges) > 0 else 0.0,
                'std_dev_90th': float(np.percentile(ranges, 90)) if len(ranges) > 0 else 0.0,
                'std_dev_95th': float(np.percentile(ranges, 95)) if len(ranges) > 0 else 0.0,
                'std_dev_99th': float(np.percentile(ranges, 99)) if len(ranges) > 0 else 0.0
            }
            # Replace any NaN or Inf values
            for key, value in std_dev_ranges.items():
                if np.isnan(value) or np.isinf(value):
                    std_dev_ranges[key] = 0.0
        except:
            std_dev_ranges = {
                'std_dev_25th': 0.0, 'std_dev_50th': 0.0, 'std_dev_75th': 0.0,
                'std_dev_90th': 0.0, 'std_dev_95th': 0.0, 'std_dev_99th': 0.0
            }
    else:
        std_dev_ranges = {
            'std_dev_25th': 0.0, 'std_dev_50th': 0.0, 'std_dev_75th': 0.0,
            'std_dev_90th': 0.0, 'std_dev_95th': 0.0, 'std_dev_99th': 0.0
        }
    
    # Percentage ranges (min to max)
    percentage_ranges = {
        'min_range_pct': min_range,
        'max_range_pct': max_range,
        'range_spread_pct': max_range - min_range
    }
    
    # Realized volatility (annualized)
    if len(log_returns) > 1:
        std_log = np.std(log_returns, ddof=1)
        if std_log > 0 and not np.isnan(std_log) and not np.isinf(std_log):
            realized_vol = std_log * np.sqrt(252) * 100
            # Check for invalid values
            if np.isnan(realized_vol) or np.isinf(realized_vol):
                realized_vol = 0.0
        else:
            realized_vol = 0.0
    else:
        realized_vol = 0.0
    
    # Consistency metric: low std / high avg (higher is more consistent)
    # Avoid division by zero
    if std_range > 0 and not np.isnan(std_range) and not np.isinf(std_range):
        consistency = avg_range / std_range
        # Handle infinity cases
        if np.isinf(consistency) or np.isnan(consistency):
            consistency = 0.0
    else:
        consistency = 0.0
    
    # Count days with swings > thresholds
    swing_counts = {}
    for threshold in SWING_THRESHOLDS:
        swing_counts[f'swing_{int(threshold)}pct'] = np.sum(ranges > threshold)
    
    # Define extreme move days: > 2 standard deviations from mean
    # OR > 3 standard deviations (ultra-extreme)
    if std_range > 0 and not np.isnan(std_range) and not np.isinf(std_range) and len(ranges) > 0:
        mean_range = np.mean(ranges)
        if not (np.isnan(mean_range) or np.isinf(mean_range)):
            two_sigma_threshold = mean_range + 2 * std_range
            three_sigma_threshold = mean_range + 3 * std_range
            extreme_days = int(np.sum(ranges > two_sigma_threshold))
            ultra_extreme_days = int(np.sum(ranges > three_sigma_threshold))
        else:
            extreme_days = 0
            ultra_extreme_days = 0
    else:
        extreme_days = 0
        ultra_extreme_days = 0
    
    return {
        'avg_intraday_range': avg_range,
        'std_intraday_range': std_range,
        'daily_std_dev': daily_std,
        'median_intraday_range': median_range,
        'max_intraday_range': max_range,
        'min_intraday_range': min_range,
        'realized_volatility': realized_vol,
        'consistency_score': consistency,
        'swing_2pct_days': swing_counts.get('swing_2pct', 0),
        'swing_3pct_days': swing_counts.get('swing_3pct', 0),
        'extreme_move_days': extreme_days,  # > 2σ moves
        'ultra_extreme_move_days': ultra_extreme_days,  # > 3σ moves
        'days_in_window': len(window_data),
        **std_dev_ranges,
        **percentage_ranges
    }


def process_ticker(ticker: str, cache: Dict = None) -> Optional[Dict]:
    """
    Process a single ticker and return its statistics.
    
    Args:
        ticker: Stock symbol
        cache: Optional cache dictionary
    
    Returns:
        Statistics dictionary or None
    """
    # Check cache first
    if cache and ticker in cache:
        cached_data = cache[ticker]
        cache_time = datetime.fromisoformat(cached_data.get('timestamp', '2000-01-01'))
        if (datetime.now() - cache_time).total_seconds() < CACHE_EXPIRY_HOURS * 3600:
            return cached_data.get('stats')
    
    try:
        # Fetch data
        data = get_intraday_data(ticker, period="2mo")  # Get 2 months to ensure 30 days
        
        if data is None:
            return None
        
        # Compute statistics
        stats = compute_intraday_stats(data, ticker)
        
        # Update cache
        if cache is not None:
            cache[ticker] = {
                'timestamp': datetime.now().isoformat(),
                'stats': stats
            }
        
        return stats
        
    except Exception as e:
        logger.debug(f"Error processing {ticker}: {e}")
        return None


def aggregate_results(all_stats: List[Dict], ticker_types: Dict[str, List[str]]) -> Dict:
    """
    Aggregate results by time window and ticker type.
    
    Args:
        all_stats: List of statistics dictionaries
        ticker_types: Dictionary mapping ticker types to ticker lists
    
    Returns:
        Aggregated results dictionary
    """
    # Separate ETFs from stocks
    etf_tickers = set(ticker_types.get('etfs', []))
    
    results = {
        'all': [],
        'stocks': [],
        'etfs': []
    }
    
    for stats in all_stats:
        if stats is None:
            continue
        
        ticker = stats.get('ticker')
        if not ticker:
            continue
        
        results['all'].append(stats)
        
        if ticker in etf_tickers:
            results['etfs'].append(stats)
        else:
            results['stocks'].append(stats)
    
    return results


def rank_results(aggregated_results: Dict, window: str = 'last_30_days') -> Dict[str, pd.DataFrame]:
    """
    Rank results for a specific time window.
    
    Args:
        aggregated_results: Aggregated results dictionary
        window: Time window to rank ('today', 'last_3_days', 'last_7_days', 'last_30_days')
    
    Returns:
        Dictionary of ranked DataFrames
    """
    rankings = {}
    
    for category in ['all', 'stocks', 'etfs']:
        stats_list = aggregated_results.get(category, [])
        
        # Filter stats that have data for this window
        valid_stats = []
        for stat in stats_list:
            window_data = stat.get(window)
            if window_data is not None:
                valid_stats.append({
                    'ticker': stat['ticker'],
                    **window_data
                })
        
        if not valid_stats:
            continue
        
        df = pd.DataFrame(valid_stats)
        
        # Create rankings
        category_rankings = {}
        
        # 1. Top average intraday % movers (ALL tickers, sorted)
        if 'avg_intraday_range' in df.columns:
            # Sort all tickers by avg_intraday_range descending
            sorted_df = df.sort_values('avg_intraday_range', ascending=False)
            category_rankings['highest_avg_range'] = sorted_df[
                ['ticker', 'avg_intraday_range', 'std_intraday_range', 'consistency_score', 
                 'swing_2pct_days', 'swing_3pct_days', 'extreme_move_days']
            ]
        
        # 2. Most consistent (high consistency score) - ALL tickers
        if 'consistency_score' in df.columns:
            # Filter out infinite/NaN consistency scores and sort
            consistency_df = df[df['consistency_score'].notna() & (df['consistency_score'] != np.inf)]
            sorted_df = consistency_df.sort_values('consistency_score', ascending=False)
            category_rankings['most_consistent'] = sorted_df[
                ['ticker', 'consistency_score', 'avg_intraday_range', 'std_intraday_range',
                 'swing_2pct_days', 'swing_3pct_days']
            ]
        
        # 3. Most >2% swing days - ALL tickers
        if 'swing_2pct_days' in df.columns:
            sorted_df = df.sort_values('swing_2pct_days', ascending=False)
            category_rankings['most_2pct_swings'] = sorted_df[
                ['ticker', 'swing_2pct_days', 'swing_3pct_days', 'avg_intraday_range',
                 'extreme_move_days', 'days_in_window']
            ]
        
        # 4. Most >3% swing days - ALL tickers
        if 'swing_3pct_days' in df.columns:
            sorted_df = df.sort_values('swing_3pct_days', ascending=False)
            category_rankings['most_3pct_swings'] = sorted_df[
                ['ticker', 'swing_3pct_days', 'swing_2pct_days', 'avg_intraday_range',
                 'extreme_move_days', 'days_in_window']
            ]
        
        # 5. Most extreme move days (>2 std dev) - ALL tickers
        if 'extreme_move_days' in df.columns:
            sorted_df = df.sort_values('extreme_move_days', ascending=False)
            category_rankings['most_extreme_moves'] = sorted_df[
                ['ticker', 'extreme_move_days', 'avg_intraday_range', 'std_intraday_range',
                 'swing_2pct_days', 'swing_3pct_days']
            ]
        
        rankings[category] = category_rankings
    
    return rankings


def print_rankings(rankings: Dict, window: str):
    """Print formatted rankings to console"""
    print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}INTRADAY SWING RANKINGS - {window.upper().replace('_', ' ')}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
    
    for category in ['all', 'stocks', 'etfs']:
        if category not in rankings:
            continue
        
        category_name = category.upper() if category == 'all' else category.capitalize()
        print(f"\n{Fore.YELLOW}{'-'*80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{category_name}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'-'*80}{Style.RESET_ALL}\n")
        
        cat_rankings = rankings[category]
        
        for ranking_type, df in cat_rankings.items():
            if df.empty:
                continue
            
            ranking_name = ranking_type.replace('_', ' ').title()
            print(f"\n{Fore.GREEN}{ranking_name} ({len(df)} tickers){Style.RESET_ALL}")
            print(f"{Fore.GREEN}{'-'*80}{Style.RESET_ALL}")
            # Print first 20 for console display, but CSV will have all
            display_df = df.head(20) if len(df) > 20 else df
            print(display_df.to_string(index=False))
            if len(df) > 20:
                print(f"\n{Fore.CYAN}... and {len(df) - 20} more tickers (see CSV for full list){Style.RESET_ALL}")
            print()


def export_to_csv(rankings: Dict, window: str, output_dir: str = 'output'):
    """Export rankings to CSV files"""
    os.makedirs(output_dir, exist_ok=True)
    
    for category in ['all', 'stocks', 'etfs']:
        if category not in rankings:
            continue
        
        cat_rankings = rankings[category]
        
        for ranking_type, df in cat_rankings.items():
            if df.empty:
                continue
            
            # Create filename
            filename = f"{category}_{ranking_type}_{window}.csv"
            filepath = os.path.join(output_dir, filename)
            
            # Export
            df.to_csv(filepath, index=False)
            logger.info(f"{Fore.GREEN}[OK] Exported {filepath}{Style.RESET_ALL}")


def load_cache() -> Dict:
    """Load cache from file"""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_cache(cache: Dict):
    """Save cache to file"""
    try:
        # Convert numpy types to native Python types for JSON serialization
        cache_serializable = {}
        for key, value in cache.items():
            if isinstance(value, dict):
                cache_serializable[key] = {}
                for k, v in value.items():
                    if isinstance(v, (np.integer, np.int64, np.int32)):
                        cache_serializable[key][k] = int(v)
                    elif isinstance(v, (np.floating, np.float64, np.float32)):
                        cache_serializable[key][k] = float(v)
                    elif isinstance(v, dict):
                        # Recursively handle nested dicts
                        cache_serializable[key][k] = _convert_numpy_types(v)
                    else:
                        cache_serializable[key][k] = v
            else:
                cache_serializable[key] = value
        
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache_serializable, f, indent=2, default=str)
    except Exception as e:
        logger.warning(f"Could not save cache: {e}")


def _convert_numpy_types(obj):
    """Recursively convert numpy types to native Python types"""
    if isinstance(obj, dict):
        return {k: _convert_numpy_types(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [_convert_numpy_types(item) for item in obj]
    elif isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64, np.float32)):
        return float(obj)
    else:
        return obj


def main():
    """Main execution function"""
    print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}INTRADAY SWING ANALYZER{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
    
    start_time = time.time()
    
    # Load cache
    cache = load_cache()
    logger.info(f"{Fore.CYAN}Cache loaded: {len(cache)} tickers{Style.RESET_ALL}")
    
    # Get tickers
    ticker_types = get_tickers()
    all_tickers = ticker_types['nasdaq'] + ticker_types['nyse'] + ticker_types['etfs']
    
    logger.info(f"{Fore.CYAN}Processing {len(all_tickers)} tickers...{Style.RESET_ALL}")
    
    # Process tickers in batches
    all_stats = []
    processed = 0
    
    for i in range(0, len(all_tickers), BATCH_SIZE):
        batch = all_tickers[i:i + BATCH_SIZE]
        logger.info(f"{Fore.CYAN}Processing batch {i//BATCH_SIZE + 1}/{(len(all_tickers) + BATCH_SIZE - 1)//BATCH_SIZE} ({len(batch)} tickers)...{Style.RESET_ALL}")
        
        for ticker in batch:
            stats = process_ticker(ticker, cache)
            if stats:
                all_stats.append(stats)
                processed += 1
            
            # Progress update
            if processed % 50 == 0:
                logger.info(f"{Fore.GREEN}Processed {processed}/{len(all_tickers)} tickers...{Style.RESET_ALL}")
        
        # Save cache periodically
        if (i // BATCH_SIZE) % 5 == 0:
            save_cache(cache)
    
    # Final cache save
    save_cache(cache)
    
    logger.info(f"{Fore.GREEN}[OK] Processed {processed} tickers successfully{Style.RESET_ALL}")
    
    # Aggregate results
    aggregated = aggregate_results(all_stats, ticker_types)
    
    # Generate rankings for each window
    windows = ['today', 'last_3_days', 'last_7_days', 'last_30_days', 'last_3_months', 'last_1_year']
    
    for window in windows:
        logger.info(f"{Fore.CYAN}Generating rankings for {window}...{Style.RESET_ALL}")
        
        rankings = rank_results(aggregated, window)
        
        # Print to console
        print_rankings(rankings, window)
        
        # Export to CSV
        export_to_csv(rankings, window)
    
    elapsed = time.time() - start_time
    logger.info(f"{Fore.GREEN}[OK] Analysis complete in {elapsed:.1f} seconds{Style.RESET_ALL}")
    logger.info(f"{Fore.CYAN}Results exported to 'output/' directory{Style.RESET_ALL}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info(f"{Fore.YELLOW}Analysis interrupted by user{Style.RESET_ALL}")
    except Exception as e:
        logger.error(f"{Fore.RED}Fatal error: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

