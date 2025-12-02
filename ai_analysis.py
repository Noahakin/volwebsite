"""
AI-Driven Analysis Module
Provides intelligent insights and trading signals based on volatility metrics
"""

def analyze_ticker_metrics(ticker: str, metrics: dict, window: str) -> dict:
    """
    Generate AI-driven analysis of ticker metrics.
    
    Args:
        ticker: Stock symbol
        metrics: Dictionary of computed metrics
        window: Time window being analyzed
    
    Returns:
        Dictionary with analysis insights and trading signals
    """
    analysis = {
        'ticker': ticker,
        'window': window,
        'risk_assessment': '',
        'volatility_profile': '',
        'trading_signals': [],
        'key_insights': [],
        'warnings': [],
        'opportunities': []
    }
    
    if not metrics:
        return analysis
    
    # Extract key metrics
    avg_range = metrics.get('avg_intraday_range', 0)
    std_range = metrics.get('std_intraday_range', 0)
    consistency = metrics.get('consistency_score', 0)
    swing_2pct = metrics.get('swing_2pct_days', 0)
    swing_3pct = metrics.get('swing_3pct_days', 0)
    extreme_days = metrics.get('extreme_move_days', 0)
    ultra_extreme = metrics.get('ultra_extreme_move_days', 0)
    realized_vol = metrics.get('realized_volatility', 0)
    days_in_window = metrics.get('days_in_window', 0)
    
    # Risk Assessment
    if avg_range > 5:
        analysis['risk_assessment'] = 'VERY HIGH - Extreme volatility'
        analysis['warnings'].append('⚠️ This ticker exhibits extreme intraday volatility (>5% avg range). High risk of significant price swings.')
    elif avg_range > 3:
        analysis['risk_assessment'] = 'HIGH - Elevated volatility'
        analysis['warnings'].append('⚠️ Elevated volatility detected. Monitor closely for sudden moves.')
    elif avg_range > 1.5:
        analysis['risk_assessment'] = 'MODERATE - Normal volatility'
    else:
        analysis['risk_assessment'] = 'LOW - Stable price action'
        analysis['opportunities'].append('✅ Low volatility suggests stable price action. Suitable for conservative strategies.')
    
    # Volatility Profile
    if consistency > 5:
        analysis['volatility_profile'] = 'CONSISTENT - Predictable volatility patterns'
        analysis['key_insights'].append(f'📊 High consistency score ({consistency:.2f}) indicates predictable volatility patterns. Good for systematic trading strategies.')
    elif consistency > 2:
        analysis['volatility_profile'] = 'MODERATELY CONSISTENT - Some predictability'
    else:
        analysis['volatility_profile'] = 'INCONSISTENT - Unpredictable volatility'
        analysis['warnings'].append('⚠️ Low consistency indicates unpredictable volatility. Difficult to model or predict.')
    
    # Trading Signals
    # Signal 1: High frequency of large swings
    if days_in_window > 0 and swing_2pct > days_in_window * 0.5:  # More than 50% of days
        pct_swing = (swing_2pct / days_in_window * 100) if days_in_window > 0 else 0.0
        analysis['trading_signals'].append({
            'type': 'SWING_TRADING',
            'strength': 'STRONG',
            'signal': f'🔄 Strong swing trading opportunity: {swing_2pct}/{days_in_window} days with >2% swings ({pct_swing:.1f}%)',
            'action': 'Consider swing trading strategies. High probability of daily 2%+ moves.'
        })
    
    # Signal 2: Extreme move frequency
    if days_in_window > 0 and extreme_days > days_in_window * 0.1:  # More than 10% of days
        pct_extreme = (extreme_days / days_in_window * 100) if days_in_window > 0 else 0.0
        analysis['trading_signals'].append({
            'type': 'EXTREME_MOVE',
            'strength': 'MODERATE',
            'signal': f'⚡ Extreme move frequency: {extreme_days} days with >2σ moves ({pct_extreme:.1f}%)',
            'action': 'Monitor for breakout/breakdown opportunities. Set wider stop-losses.'
        })
    
    # Signal 3: Consistency-based signals
    if consistency > 4 and avg_range > 2:
        analysis['trading_signals'].append({
            'type': 'MEAN_REVERSION',
            'strength': 'STRONG',
            'signal': f'📈 High consistency ({consistency:.2f}) with moderate volatility ({avg_range:.2f}%)',
            'action': 'Mean reversion strategies may work well. Price tends to revert to average range.'
        })
    
    # Signal 4: Low volatility opportunity
    if avg_range < 1 and consistency > 3:
        analysis['trading_signals'].append({
            'type': 'LOW_VOLATILITY',
            'strength': 'MODERATE',
            'signal': f'📉 Low volatility ({avg_range:.2f}%) with high consistency',
            'action': 'Suitable for income strategies (covered calls, cash-secured puts). Low risk of large moves.'
        })
    
    # Signal 5: High volatility momentum
    if days_in_window > 0 and avg_range > 4 and swing_3pct > days_in_window * 0.3:
        analysis['trading_signals'].append({
            'type': 'MOMENTUM',
            'strength': 'STRONG',
            'signal': f'🚀 High momentum volatility: {avg_range:.2f}% avg range, {swing_3pct} days with >3% swings',
            'action': 'Momentum trading strategies recommended. High probability of continuation moves.'
        })
    
    # Key Insights
    if realized_vol > 50:
        analysis['key_insights'].append(f'📊 High realized volatility ({realized_vol:.1f}% annualized) suggests significant price uncertainty.')
    
    if ultra_extreme > 0:
        analysis['key_insights'].append(f'⚡ {ultra_extreme} ultra-extreme move days (>3σ) detected. These are rare events indicating major market shifts.')
    
    if std_range > avg_range * 0.5:
        analysis['key_insights'].append(f'📈 High standard deviation ({std_range:.2f}%) relative to average ({avg_range:.2f}%) indicates variable volatility.')
    
    # Percentage of days with swings
    if days_in_window > 0:
        pct_2pct_days = (swing_2pct / days_in_window) * 100
        pct_3pct_days = (swing_3pct / days_in_window) * 100
        
        if pct_2pct_days > 70:
            analysis['key_insights'].append(f'🔄 Very active: {pct_2pct_days:.1f}% of days have >2% swings. High trading activity expected.')
        
        if pct_3pct_days > 40:
            analysis['key_insights'].append(f'⚡ Extremely active: {pct_3pct_days:.1f}% of days have >3% swings. Major moves are common.')
    
    return analysis


def generate_summary_report(ticker: str, all_window_metrics: dict) -> str:
    """
    Generate a comprehensive summary report across all time windows.
    
    Args:
        ticker: Stock symbol
        all_window_metrics: Dictionary of metrics for each time window
    
    Returns:
        Formatted summary report string
    """
    report = f"# 📊 Comprehensive Analysis Report: {ticker}\n\n"
    
    # Trend analysis across windows
    windows_order = ['today', 'last_3_days', 'last_7_days', 'last_30_days', 'last_3_months', 'last_1_year']
    avg_ranges = []
    
    for window in windows_order:
        if window in all_window_metrics and all_window_metrics[window]:
            metrics = all_window_metrics[window]
            avg_range = metrics.get('avg_intraday_range', 0)
            if avg_range > 0:
                avg_ranges.append((window, avg_range))
    
    if len(avg_ranges) > 1:
        # Check trend
        recent_avg = avg_ranges[0][1] if avg_ranges else 0
        longer_avg = avg_ranges[-1][1] if len(avg_ranges) > 1 else 0
        
        if recent_avg > longer_avg * 1.2:
            report += "## ⚠️ Volatility Trend: INCREASING\n"
            report += f"Recent volatility ({recent_avg:.2f}%) is significantly higher than longer-term average ({longer_avg:.2f}%).\n\n"
        elif recent_avg < longer_avg * 0.8:
            report += "## ✅ Volatility Trend: DECREASING\n"
            report += f"Recent volatility ({recent_avg:.2f}%) is lower than longer-term average ({longer_avg:.2f}%).\n\n"
        else:
            report += "## 📊 Volatility Trend: STABLE\n"
            report += "Volatility levels are consistent across timeframes.\n\n"
    
    # Add analysis for each window
    for window in windows_order:
        if window in all_window_metrics and all_window_metrics[window]:
            metrics = all_window_metrics[window]
            analysis = analyze_ticker_metrics(ticker, metrics, window)
            
            report += f"## {window.replace('_', ' ').title()}\n\n"
            report += f"**Risk Assessment:** {analysis['risk_assessment']}\n\n"
            report += f"**Volatility Profile:** {analysis['volatility_profile']}\n\n"
            
            if analysis['trading_signals']:
                report += "### Trading Signals:\n"
                for signal in analysis['trading_signals']:
                    report += f"- **{signal['type']}** ({signal['strength']}): {signal['signal']}\n"
                    report += f"  → {signal['action']}\n\n"
            
            if analysis['key_insights']:
                report += "### Key Insights:\n"
                for insight in analysis['key_insights']:
                    report += f"- {insight}\n\n"
            
            if analysis['warnings']:
                report += "### ⚠️ Warnings:\n"
                for warning in analysis['warnings']:
                    report += f"- {warning}\n\n"
            
            if analysis['opportunities']:
                report += "### ✅ Opportunities:\n"
                for opp in analysis['opportunities']:
                    report += f"- {opp}\n\n"
            
            report += "---\n\n"
    
    return report

