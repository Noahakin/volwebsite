# Intraday Swing Analyzer - Web Dashboard

A comprehensive, shareable web application for analyzing intraday price swings in stocks and ETFs.

## Features

- 📊 **Interactive Rankings**: View top performers across multiple metrics
- 📈 **Detailed Metrics**: Deep dive into individual ticker performance
- 📉 **Visualizations**: Charts and graphs for data exploration
- 🔍 **Ticker Explorer**: Compare multiple tickers side-by-side
- ⚙️ **Analysis Tools**: Run new analyses directly from the web interface

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Web App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

### Running Analysis

1. First, run the analysis script to generate data:
   ```bash
   python intraday_swing_analyzer.py
   ```

2. Or use the "Analysis" tab in the web app to run it directly

### Exploring Data

1. **Rankings Tab**: View top performers by various metrics
   - Select time window (today, 3-day, 7-day, 30-day)
   - Choose category (all, stocks, ETFs)
   - Pick ranking type (highest range, most consistent, etc.)

2. **Detailed Metrics Tab**: 
   - Select any ticker to see comprehensive metrics
   - View metrics across all time windows
   - See all available statistics

3. **Visualizations Tab**:
   - Top 20 charts
   - Consistency vs volatility scatter plots
   - Swing days comparisons
   - Distribution histograms

4. **Ticker Explorer Tab**:
   - Compare multiple tickers
   - See performance across time windows
   - Detailed comparison tables

## Deployment

### Streamlit Cloud (Recommended)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Set main file to `app.py`
5. Deploy!

### Other Platforms

#### Heroku

1. Create `Procfile`:
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. Deploy:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

#### Railway

1. Connect your GitHub repository
2. Set start command: `streamlit run app.py --server.port=$PORT`
3. Deploy automatically

#### Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t intraday-analyzer .
docker run -p 8501:8501 intraday-analyzer
```

## File Structure

```
.
├── app.py                          # Streamlit web application
├── intraday_swing_analyzer.py     # Analysis engine
├── requirements.txt                # Python dependencies
├── output/                         # Generated CSV files
│   ├── all_highest_avg_range_*.csv
│   ├── all_most_consistent_*.csv
│   └── ...
└── README_WEB_APP.md              # This file
```

## Features in Detail

### Rankings

- **Highest Average Range**: Tickers with largest intraday swings
- **Most Consistent**: Tickers with high consistency scores
- **Most >2% Swings**: Tickers with most days exceeding 2% range
- **Most >3% Swings**: Tickers with most days exceeding 3% range
- **Most Extreme Moves**: Tickers with most >2σ moves

### Metrics Available

- Average Intraday Range (%)
- Standard Deviation of Range
- Consistency Score (avg/std)
- Realized Volatility (annualized)
- Number of >2% swing days
- Number of >3% swing days
- Number of extreme move days (>2σ)
- Days in analysis window

### Time Windows

- **Today**: Most recent trading day
- **Last 3 Days**: Last 3 trading days
- **Last 7 Days**: Last 7 trading days
- **Last 30 Days**: Last 30 trading days

## Customization

### Adding New Metrics

Edit `intraday_swing_analyzer.py` to add new calculations, then update `app.py` to display them.

### Changing Visualizations

Modify the Plotly charts in the "Visualizations" tab to customize charts.

### Styling

Edit the CSS in the `st.markdown()` section at the top of `app.py`.

## Troubleshooting

### "No data available"

- Run the analysis script first: `python intraday_swing_analyzer.py`
- Check that CSV files exist in the `output/` directory
- Refresh the page or clear cache

### Analysis takes too long

- Reduce the number of tickers in `get_tickers()`
- Increase cache TTL in `@st.cache_data(ttl=3600)`
- Run analysis in background and load results

### Charts not displaying

- Ensure Plotly is installed: `pip install plotly`
- Check browser console for errors
- Try clearing browser cache

## Performance Tips

1. **Caching**: Results are cached for 1 hour by default
2. **Lazy Loading**: Data is only loaded when needed
3. **Batch Processing**: Analysis processes tickers in batches
4. **CSV Storage**: Results stored as CSV for fast loading

## Support

For issues or questions:
1. Check the console output for errors
2. Verify all dependencies are installed
3. Ensure analysis has been run successfully
4. Check that output files exist

## License

This project is provided as-is for educational and personal use.

---

**Happy Analyzing! 📊📈**

