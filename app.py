#!/usr/bin/env python3
"""
Volatility Insights Pro - Web Dashboard
Advanced interactive platform for exploring intraday swing and volatility metrics
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import json
from datetime import datetime
import asyncio
import warnings
warnings.filterwarnings('ignore')

# Try to import analysis functions
try:
    from intraday_swing_analyzer import get_tickers, process_ticker, aggregate_results, rank_results, load_cache, save_cache
    ANALYSIS_AVAILABLE = True
except ImportError:
    ANALYSIS_AVAILABLE = False
    st.error("Analysis module not available. Please ensure intraday_swing_analyzer.py is in the same directory.")

# Page configuration
st.set_page_config(
    page_title="Volatility Insights Pro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stMetric {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .info-box {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2196f3;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def load_cached_results(force_refresh=False):
    """Load results from CSV files if they exist"""
    if force_refresh:
        st.cache_data.clear()
    
    results = {}
    windows = ['today', 'last_3_days', 'last_7_days', 'last_30_days', 'last_3_months', 'last_1_year']
    categories = ['all', 'stocks', 'etfs']
    ranking_types = ['highest_avg_range', 'most_consistent', 'most_2pct_swings', 'most_3pct_swings', 'most_extreme_moves']
    
    for window in windows:
        results[window] = {}
        for category in categories:
            results[window][category] = {}
            for ranking_type in ranking_types:
                filepath = f'output/{category}_{ranking_type}_{window}.csv'
                if os.path.exists(filepath):
                    try:
                        df = pd.read_csv(filepath)
                        if not df.empty:
                            results[window][category][ranking_type] = df
                    except Exception as e:
                        pass
    return results

def get_all_tickers_from_results(results):
    """Extract all unique tickers from results"""
    all_tickers = set()
    for window in results.keys():
        for category in results[window].keys():
            for ranking_type in results[window][category].keys():
                df = results[window][category][ranking_type]
                if not df.empty and 'ticker' in df.columns:
                    all_tickers.update(df['ticker'].unique())
    return sorted(list(all_tickers))

def get_ticker_metrics(ticker, results):
    """Get all metrics for a specific ticker across all windows"""
    ticker_metrics = {}
    for window in results.keys():
        ticker_metrics[window] = {}
        for category in results[window].keys():
            for ranking_type in results[window][category].keys():
                df = results[window][category][ranking_type]
                if not df.empty and 'ticker' in df.columns:
                    ticker_row = df[df['ticker'] == ticker]
                    if not ticker_row.empty:
                        ticker_metrics[window][ranking_type] = ticker_row.iloc[0].to_dict()
    return ticker_metrics

def main():
    # Header
    st.markdown('<h1 class="main-header">📈 Volatility Insights Pro</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666; font-size: 1.1rem;">Professional Intraday Swing & Volatility Analytics</p>', unsafe_allow_html=True)
    
    # Show ticker count
    try:
        from comprehensive_tickers import get_all_volatile_tickers
        ticker_data = get_all_volatile_tickers()
        st.caption(f"Analyzing {len(ticker_data['all'])} tickers: {len(ticker_data['etfs'])} ETFs • {len(ticker_data['stocks'])} Stocks")
    except:
        pass
    
    st.markdown("---")
    
    # Load cached results (no caching decorator - refresh button clears cache)
    cached_results = load_cached_results()
    has_data = any(cached_results.values())
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Time window selection
        time_window = st.selectbox(
            "📅 Time Window",
            ["last_1_year", "last_3_months", "last_30_days", "last_7_days", "last_3_days", "today"],
            index=2,
            format_func=lambda x: x.replace("_", " ").title()
        )
        
        # Refresh button
        if st.button("🔄 Refresh Data", type="primary", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        
        # Category selection
        category = st.selectbox(
            "📂 Category",
            ["all", "stocks", "etfs"],
            index=0,
            format_func=lambda x: x.upper() if x == "all" else x.capitalize()
        )
        
        # Ranking type
        ranking_type = st.selectbox(
            "🏆 Ranking Type",
            ["highest_avg_range", "most_consistent", "most_2pct_swings", "most_3pct_swings", "most_extreme_moves"],
            index=0,
            format_func=lambda x: {
                "highest_avg_range": "Highest Avg Range",
                "most_consistent": "Most Consistent",
                "most_2pct_swings": "Most >2% Swings",
                "most_3pct_swings": "Most >3% Swings",
                "most_extreme_moves": "Most Extreme Moves"
            }.get(x, x.replace("_", " ").title())
        )
        
        st.markdown("---")
        
        if has_data:
            all_tickers = get_all_tickers_from_results(cached_results)
            st.success(f"✅ {len(all_tickers)} tickers loaded")
        else:
            st.warning("⚠️ No data. Run analysis first.")
    
    # Main content tabs - streamlined
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Rankings", 
        "📊 Ticker Analysis", 
        "🤖 AI Insights",
        "⚙️ Run Analysis"
    ])
    
    # Tab 1: Rankings
    with tab1:
        st.header(f"🏆 {ranking_type.replace('_', ' ').title()}")
        st.subheader(f"📅 {time_window.replace('_', ' ').title()} | 📂 {category.upper()}")
        
        if has_data and time_window in cached_results and category in cached_results[time_window]:
            if ranking_type in cached_results[time_window][category]:
                df = cached_results[time_window][category][ranking_type].copy()
                
                if not df.empty:
                    # Check if this is old data with only 20 tickers
                    if len(df) == 20:
                        st.warning("⚠️ This data appears to be from an old analysis with only 20 tickers. Please run a new analysis from the 'Run Analysis' tab to see all tickers.")
                    # Display summary metrics
                    col1, col2, col3, col4, col5 = st.columns(5)
                    
                    with col1:
                        st.metric("Total Tickers", len(df))
                    
                    if 'avg_intraday_range' in df.columns:
                        with col2:
                            st.metric("Avg Range", f"{df['avg_intraday_range'].mean():.2f}%")
                        with col3:
                            st.metric("Max Range", f"{df['avg_intraday_range'].max():.2f}%")
                    
                    if 'swing_2pct_days' in df.columns:
                        with col4:
                            st.metric("Total >2% Days", int(df['swing_2pct_days'].sum()))
                    
                    if 'swing_3pct_days' in df.columns:
                        with col5:
                            st.metric("Total >3% Days", int(df['swing_3pct_days'].sum()))
                    
                    st.markdown("---")
                    
                    # Show all tickers by default, with option to limit
                    st.caption(f"Showing all {len(df)} tickers (sorted by ranking)")
                    num_tickers = st.slider("Limit display to top N tickers (0 = show all)", 0, min(1000, len(df)), 0, key="num_tickers")
                    if num_tickers > 0:
                        display_df = df.head(num_tickers)
                    else:
                        display_df = df  # Show all
                    
                    # Display table with formatting
                    st.dataframe(
                        display_df.style.format({
                            'avg_intraday_range': '{:.2f}%',
                            'std_intraday_range': '{:.2f}%',
                            'consistency_score': '{:.2f}',
                            'swing_2pct_days': '{:.0f}',
                            'swing_3pct_days': '{:.0f}',
                            'extreme_move_days': '{:.0f}',
                        }, na_rep='N/A') if hasattr(display_df.style, 'format') else display_df,
                        use_container_width=True,
                        hide_index=True,
                        height=600
                    )
                    
                    # Download button
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv,
                        file_name=f"{category}_{ranking_type}_{time_window}.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("No data available for this selection.")
            else:
                st.info(f"No {ranking_type} ranking available for this selection.")
        else:
            st.info("No data available. Please run an analysis first.")
    
    # Tab 2: Ticker Analysis
    with tab2:
        st.header("📊 Ticker Analysis")
        
        if has_data:
            all_tickers = get_all_tickers_from_results(cached_results)
            
            if all_tickers:
                col1, col2 = st.columns([1, 3])
                with col1:
                    selected_ticker = st.selectbox("Select Ticker", all_tickers, key="ticker_select")
                with col2:
                    selected_window = st.selectbox(
                        "Time Window",
                        ["last_1_year", "last_3_months", "last_30_days", "last_7_days", "last_3_days", "today"],
                        index=2,
                        key="ticker_window"
                    )
                
                ticker_metrics = get_ticker_metrics(selected_ticker, cached_results)
                
                if ticker_metrics and selected_window in ticker_metrics:
                    metrics_dict = ticker_metrics[selected_window]
                    if metrics_dict:
                        # Get metrics from any ranking type
                        all_metrics = {}
                        for ranking_data in metrics_dict.values():
                            all_metrics.update(ranking_data)
                        
                        if all_metrics:
                            # Key metrics display
                            st.subheader(f"📈 {selected_ticker} - {selected_window.replace('_', ' ').title()}")
                            
                            cols = st.columns(5)
                            with cols[0]:
                                st.metric("Avg Range", f"{all_metrics.get('avg_intraday_range', 0):.2f}%")
                                st.metric("Std Dev", f"{all_metrics.get('std_intraday_range', 0):.2f}%")
                            with cols[1]:
                                st.metric("Consistency", f"{all_metrics.get('consistency_score', 0):.2f}")
                                st.metric("Realized Vol", f"{all_metrics.get('realized_volatility', 0):.2f}%")
                            with cols[2]:
                                st.metric(">2% Days", int(all_metrics.get('swing_2pct_days', 0)))
                                st.metric(">3% Days", int(all_metrics.get('swing_3pct_days', 0)))
                            with cols[3]:
                                st.metric("Extreme Days", int(all_metrics.get('extreme_move_days', 0)))
                                st.metric("Ultra Extreme", int(all_metrics.get('ultra_extreme_move_days', 0)))
                            with cols[4]:
                                st.metric("Days Analyzed", int(all_metrics.get('days_in_window', 0)))
                                if 'std_dev_95th' in all_metrics:
                                    st.metric("95th %ile", f"{all_metrics.get('std_dev_95th', 0):.2f}%")
                            
                            st.markdown("---")
                            
                            # Standard Deviation Ranges
                            st.subheader("📊 Standard Deviation Ranges")
                            std_cols = st.columns(6)
                            std_metrics = {
                                '25th': 'std_dev_25th',
                                '50th': 'std_dev_50th',
                                '75th': 'std_dev_75th',
                                '90th': 'std_dev_90th',
                                '95th': 'std_dev_95th',
                                '99th': 'std_dev_99th'
                            }
                            for idx, (label, key) in enumerate(std_metrics.items()):
                                with std_cols[idx]:
                                    st.metric(f"{label} Percentile", f"{all_metrics.get(key, 0):.2f}%")
                            
                            # Percentage Ranges
                            st.subheader("📈 Percentage Ranges")
                            pct_cols = st.columns(3)
                            with pct_cols[0]:
                                st.metric("Min Range", f"{all_metrics.get('min_range_pct', 0):.2f}%")
                            with pct_cols[1]:
                                st.metric("Max Range", f"{all_metrics.get('max_range_pct', 0):.2f}%")
                            with pct_cols[2]:
                                st.metric("Range Spread", f"{all_metrics.get('range_spread_pct', 0):.2f}%")
                            
                            st.markdown("---")
                            
                            # All metrics table
                            st.subheader("Complete Metrics")
                            metrics_display = pd.DataFrame([all_metrics]).T
                            metrics_display.columns = ['Value']
                            metrics_display = metrics_display.sort_index()
                            st.dataframe(metrics_display, use_container_width=True, height=300)
                    else:
                        st.info(f"No metrics available for {selected_ticker} in {selected_window}")
                else:
                    st.warning(f"No data found for {selected_ticker}")
            else:
                st.warning("No ticker data available.")
        else:
            st.info("No data available. Please run an analysis first.")
    
    # Tab 3: AI Insights (computed on-the-fly)
    with tab3:
        st.header("🤖 AI-Driven Analysis & Trading Signals")
        st.caption("Analysis computed in real-time from current metrics")
        
        if has_data:
            all_tickers = get_all_tickers_from_results(cached_results)
            
            if all_tickers:
                col1, col2 = st.columns(2)
                with col1:
                    selected_ticker = st.selectbox("Select Ticker", all_tickers, key="ai_ticker_select")
                with col2:
                    selected_window = st.selectbox(
                        "Time Window",
                        ["last_1_year", "last_3_months", "last_30_days", "last_7_days", "last_3_days", "today"],
                        index=2,
                        key="ai_window"
                    )
                
                # Get metrics for selected ticker and window
                ticker_metrics = get_ticker_metrics(selected_ticker, cached_results)
                
                if ticker_metrics and selected_window in ticker_metrics:
                    metrics_dict = ticker_metrics[selected_window]
                    if metrics_dict:
                        # Get metrics from any ranking type
                        all_metrics = {}
                        for ranking_data in metrics_dict.values():
                            all_metrics.update(ranking_data)
                        
                        if all_metrics:
                            try:
                                from ai_analysis import analyze_ticker_metrics
                                
                                # Compute AI analysis on-the-fly
                                analysis = analyze_ticker_metrics(selected_ticker, all_metrics, selected_window)
                                
                                # Display analysis
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.subheader("📊 Risk Assessment")
                                    risk_level = analysis['risk_assessment']
                                    if 'VERY HIGH' in risk_level:
                                        st.error(f"**{risk_level}**")
                                    elif 'HIGH' in risk_level:
                                        st.warning(f"**{risk_level}**")
                                    elif 'MODERATE' in risk_level:
                                        st.info(f"**{risk_level}**")
                                    else:
                                        st.success(f"**{risk_level}**")
                                
                                with col2:
                                    st.subheader("📈 Volatility Profile")
                                    st.info(f"**{analysis['volatility_profile']}**")
                                
                                st.markdown("---")
                                
                                # Trading Signals
                                if analysis['trading_signals']:
                                    st.subheader("🎯 Trading Signals")
                                    for signal in analysis['trading_signals']:
                                        signal_type = signal['type'].replace('_', ' ').title()
                                        with st.expander(f"📌 {signal_type} - {signal['strength']}"):
                                            st.markdown(f"**{signal['signal']}**")
                                            st.markdown(f"💡 **Action:** {signal['action']}")
                                
                                # Key Insights
                                if analysis['key_insights']:
                                    st.subheader("💡 Key Insights")
                                    for insight in analysis['key_insights']:
                                        st.info(insight)
                                
                                # Warnings
                                if analysis['warnings']:
                                    st.subheader("⚠️ Warnings")
                                    for warning in analysis['warnings']:
                                        st.warning(warning)
                                
                                # Opportunities
                                if analysis['opportunities']:
                                    st.subheader("✅ Opportunities")
                                    for opp in analysis['opportunities']:
                                        st.success(opp)
                            except ImportError:
                                st.error("AI analysis module not available.")
                        else:
                            st.warning(f"No metrics found for {selected_ticker}")
                    else:
                        st.info(f"No metrics available for {selected_ticker} in {selected_window}")
                else:
                    st.warning(f"No data found for {selected_ticker}")
            else:
                st.warning("No ticker data available.")
        else:
            st.info("No data available. Please run an analysis first.")
    
    # Tab 4: Run Analysis
    with tab4:
        st.header("⚙️ Run Analysis")
        
        if ANALYSIS_AVAILABLE:
            # Show ticker info
            try:
                from comprehensive_tickers import get_all_volatile_tickers
                ticker_data = get_all_volatile_tickers()
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Tickers", len(ticker_data['all']))
                with col2:
                    st.metric("ETFs", len(ticker_data['etfs']))
                with col3:
                    st.metric("Stocks", len(ticker_data['stocks']))
            except:
                pass
            
            st.markdown("---")
            
            st.info("""
            **Run Analysis:**
            - Processes all tickers across 6 time windows (today, 3d, 7d, 30d, 3mo, 1y)
            - Calculates comprehensive volatility metrics including std dev ranges
            - Generates rankings and saves to CSV files
            - Analysis may take 15-30 minutes for 500+ tickers
            """)
            
            if st.button("🔄 Run New Analysis", type="primary", use_container_width=True):
                with st.spinner("Running analysis... This may take 15-30 minutes for 500+ tickers."):
                    try:
                        from intraday_swing_analyzer import main as run_analysis
                        run_analysis()
                        st.success("✅ Analysis complete! Click 'Refresh Data' in sidebar to load results.")
                        st.cache_data.clear()
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                        st.exception(e)
        else:
            st.error("Analysis module not available. Please ensure intraday_swing_analyzer.py is accessible.")

if __name__ == "__main__":
    main()
