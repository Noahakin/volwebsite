import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By from selenium.webdriver.chrome.options import Options from selenium.webdriver.chrome.service import Service from selenium.webdriver.support.ui import WebDriverWait from selenium.webdriver.support import expected_conditions as EC from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import yfinance as yf
from datetime import datetime


download_dir = "/Users/noahakin/Desktop/etf_downloads"
downloaded_excel_path = os.path.join(download_dir, "TargetOutcomeFundList.xlsx") fallback_excel_path = os.path.abspath("Targetbufferss.xlsx")
upload_excel_path = os.path.abspath("TargetOutcomeFundList.xlsx")


os.makedirs(download_dir, exist_ok=True)


if "zoom_level" not in st.session_state:
    st.session_state.zoom_level = 1.0
if "excel_file_path" not in st.session_state:
    st.session_state.excel_file_path = None

# Upload Excel File
st.sidebar.header("📂 Upload Excel File") uploaded_file = st.sidebar.file_uploader("Choose an Excel file", type=["xlsx"]) if uploaded_file:
    with open(upload_excel_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.sidebar.success("✅ Uploaded.")
    st.session_state.excel_file_path = upload_excel_path

# Selenium
def run_selenium_download():
   
    for f in os.listdir(download_dir):
        path = os.path.join(download_dir, f)
        try:
            os.remove(path)
        except Exception as e:
            st.warning(f"⚠️ Could not delete {f}: {e}")

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  
    chrome_options.add_argument("--disable-gpu")
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "directory_upgrade": True,
        "safebrowsing.enabled": True,
    }
    chrome_options.add_experimental_option("prefs", prefs)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        url = "https://www.ftportfolios.com/retail/etf/targetoutcomefundlist.aspx"
        driver.get(url)
        st.info("🌐 Opened First Trust ETF page")
        time.sleep(3)
        driver.save_screenshot(os.path.join(download_dir, "debug_ftpage.png"))
        st.info("📸 Screenshot saved")

        wait = WebDriverWait(driver, 20)
        download_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Download to Excel")))
        download_link.click()
        st.info("📥 Clicked download link...")

        
        timeout = time.time() + 30
        downloaded_file = None
        while time.time() < timeout:
            files = [f for f in os.listdir(download_dir) if f.endswith(".xlsx") and not f.endswith(".crdownload")]
            if files:
                downloaded_file = files[0]
                break
            time.sleep(1)

        if not downloaded_file:
            st.error("❌ Download did not complete.")
            return False

        src = os.path.join(download_dir, downloaded_file)
        dst = os.path.join(download_dir, "TargetOutcomeFundList.xlsx")
        os.rename(src, dst)
        st.success(f"✅ Downloaded and saved to: {dst}")
        return True

    finally:
        driver.quit()
        st.info("👋 Chrome closed")

# Refresh Excel File
if st.button("🔄 Refresh Excel File"):
    st.info("🚀 Running Selenium downloader...")

    success = run_selenium_download()  

    if success:
        st.session_state.excel_file_path = downloaded_excel_path
        st.success("✅ Download complete! Please manually refresh the page to load the new data.")
        st.stop()
    else:
        st.error("❌ Download failed.")


# Determine Excel file path to use
if st.session_state.excel_file_path and os.path.exists(st.session_state.excel_file_path):
    excel_path = st.session_state.excel_file_path elif os.path.exists(downloaded_excel_path):
    excel_path = downloaded_excel_path
    st.session_state.excel_file_path = downloaded_excel_path elif os.path.exists(fallback_excel_path):
    excel_path = fallback_excel_path
    st.session_state.excel_file_path = fallback_excel_path
else:
    st.error("❌ No Excel file available. Please upload or refresh.")
    st.stop()

# Confirm file exists
if not os.path.exists(excel_path):
    st.error(f"❌ Excel file not found at: {excel_path}")
    st.stop()

st.success(f"📄 Using Excel file: {excel_path}")

# Read Excel with header detection
try:
    df_raw = pd.read_excel(excel_path, header=None)
    possible_ticker_columns = ['Ticker', 'Symbol', 'ETF Ticker', 'Fund Ticker']
    header_row = None
    for i in range(20):
        row_values = df_raw.iloc[i].astype(str).str.strip()
        for col in possible_ticker_columns:
            if col in row_values.values:
                header_row = i
                break
        if header_row is not None:
            break
    if header_row is None:
        st.error("❌ Could not find header row with 'Ticker' or similar column.")
        st.write(df_raw.head(20))
        st.stop()

    df = pd.read_excel(excel_path, header=header_row)
    for col in possible_ticker_columns:
        if col in df.columns and col != 'Ticker':
            df.rename(columns={col: 'Ticker'}, inplace=True)
    if 'Ticker' not in df.columns:
        st.error("❌ 'Ticker' column not found after renaming.")
        st.write(df.columns.tolist())
        st.stop()

except Exception as e:
    st.error(f"❌ Error reading Excel file: {e}")
    st.stop()



# App Title
st.title("📊 Buffered ETF Payoff Visualizer")

# Layout
col1, col2, col3 = st.columns([1.5, 1.5, 2])

# Optional filters
with col1:
    selected_strategy = st.selectbox(
        "Optional Filter: Buffer Type",
        options=["All"] + sorted(df['Strategy Type'].dropna().unique()),
        index=0
    )

with col2:
    selected_asset = st.selectbox(
        "Optional Filter: Underlying Asset",
        options=["All"] + sorted(df['Reference Asset'].dropna().unique()),
        index=0
    )

# Filter dataset conditionally
filtered_df = df.copy()
if selected_strategy != "All":
    filtered_df = filtered_df[filtered_df['Strategy Type'] == selected_strategy] if selected_asset != "All":
    filtered_df = filtered_df[filtered_df['Reference Asset'] == selected_asset]

# ETF selection based on filtered data
with col3:
    selected_etf = st.selectbox("Select ETF:", filtered_df['Ticker'].dropna().unique())

# Retrieve selected fund row
fund = filtered_df[filtered_df['Ticker'] == selected_etf].iloc[0]


# Extract Key Variable
start = float(fund['Starting Fund Value (USD)']) cap = float(fund['Fund Cap Net']) buffer_start = float(fund['Buffer Start']) buffer_end = float(fund['Buffer End']) ref_price = float(fund['Starting Reference Asset Value (USD)']) ref_return = float(fund['Reference Asset Return']) etf_data = yf.Ticker(selected_etf).history(period="2d")
if len(etf_data) >= 2:
    prev_close = etf_data['Close'].iloc[-2]
    live_etf_price = etf_data['Close'].iloc[-1]
    today_return = (live_etf_price / start) - 1
else:
    live_etf_price = etf_data['Close'].iloc[-1]
    today_return = 0.0  


known_assets = {"GLD": "GLD", "SPY": "SPY", "QQQ": "QQQ", "RSP": "RSP", "IWM": "IWM", "EEM": "EEM", "EFA": "EFA"} reference_col = next((c for c in ['Reference Asset', 'Underlying Asset', 'Underlying Index'] if pd.notna(fund.get(c))), 'Not Provided') underlying_asset = fund.get(reference_col, 'Not Provided').strip() underlying_ticker = known_assets.get(underlying_asset, None)


# === Live Prices ===

live_etf_price = etf_intraday['Close'].iloc[-1] if not etf_intraday.empty else float(fund['Fund Value (USD)']) live_underlying_price = underlying_intraday['Close'].iloc[-1] if not underlying_intraday.empty else float(fund['Reference Asset Value (USD)'])

# Returns based on outcome period start values 
today_return = (live_etf_price / start) - 1 live_underlying_return = ((live_underlying_price / ref_price) - 1) * 100


cap_value = start * (1 + cap)
buffer_start_value = start * (1 + buffer_start) buffer_end_value = start * (1 + buffer_start) 
outcome_start = pd.to_datetime(fund['Outcome Period Start Date']) outcome_end = pd.to_datetime(fund['Outcome Period End Date']) today = pd.Timestamp.today().normalize() days_remaining = max((outcome_end - today).days, 0)


st.markdown("### 🧾 Summary of Structure") cols = st.columns(2)
cols[0].markdown(f"**🎯 Starting Price**\n${start:.2f}")
cols[1].markdown(f"**💰 Live ETF Price**\n{today_return*100:+.2f}% →\n${live_etf_price:.2f}")


cols = st.columns(2)
cols[0].markdown(f"**🔍 Underlying Asset** ({(underlying_asset)})\n{live_underlying_return:+.2f}% →\n${live_underlying_price:.2f}")
cols[1].markdown(f"**📈 Cap Level**\n+{cap*100:.2f}% → **${cap_value:.2f}**")

cols = st.columns(2)
cols[0].markdown(f"**🛡️ Buffer Start**\n{buffer_start*100:.2f}% → **${buffer_start_value:.2f}**")
cols[1].markdown(f"**🛡️ Buffer End**\n{buffer_end*100:.2f}% → **${buffer_end_value:.2f}**")

cols = st.columns(2)
cols[0].markdown(f"**📆 Period**\n{outcome_start.strftime('%b %d, %Y')} → {outcome_end.strftime('%b %d, %Y')}") cols[1].markdown(f"**⏳ Days Remaining**\n**{days_remaining}**")
st.markdown("---")


st.subheader("🔧 Scenario Simulator")
test_return = st.slider("Select underlying asset return (%)", -100, 100, 0) / 100 if test_return > cap:
    test_payoff = start * (1 + cap)
elif test_return > 0 or test_return > buffer_start:
    test_payoff = start * (1 + test_return) elif test_return > buffer_end:
    test_payoff = start * (1 + buffer_start)
else:
    test_payoff = start * (1 + (test_return - buffer_end + buffer_start))

col1, spacer, col2 = st.columns([5, 11, 3])  

with col1:
    st.metric(
        "Underlying Asset Final Value",
        f"${ref_price * (1 + test_return):.2f}",
        f"{test_return * 100:+.2f}%"
    )

with col2:
    st.metric(
        "ETF Final Value",
        f"${test_payoff:.2f}",
        f"{(test_payoff / start - 1):+.2%}"
    )


col_zoom_out, spacer, col_zoom_in = st.columns([2, 8, 2])

with col_zoom_out:
    if st.button("🔍 - Zoom Out"):
        st.session_state.zoom_level *= 1.2

with col_zoom_in:
    if st.button("🔍 + Zoom In"):
        st.session_state.zoom_level /= 1.2


# Zoom
default_range = (buffer_end - 0.20, cap + 0.15) range_width = (default_range[1] - default_range[0]) * st.session_state.zoom_level x_center = (default_range[0] + default_range[1]) / 2 lower_bound = x_center - range_width / 2 upper_bound = x_center + range_width / 2

x = np.linspace(lower_bound, upper_bound, 500)  # underlying asset return in decimals

y = []
for r in x:
    if r > cap:
        y.append(start * (1 + cap))
    elif r > 0:
        y.append(start * (1 + r))
    elif r > buffer_start:
        y.append(start * (1 + r))
    elif r > buffer_end:
        y.append(start * (1 + buffer_start))
    else:
        y.append(start * (1 + (r - buffer_end + buffer_start)))

y = np.array(y)
x_pct = x * 100

fig, ax = plt.subplots(figsize=(12, 7))
ax.plot(x_pct, y, color='black', linewidth=3, label='ETF Payoff') ax.plot(x_pct, start * (1 + x), color='gray', linestyle='dashed', linewidth=2, label='Underlying Asset')

# Fill zones
ax.fill_between(x_pct, start, y, where=(x > 0) & (x <= cap), color='green', alpha=0.2) ax.fill_between(x_pct, start, y, where=(x > cap), color='green', alpha=0.2) ax.fill_between(x_pct, y, start, where=(x < 0) & (x >= buffer_start), color='red', alpha=0.2) ax.fill_between(x_pct, y, start, where=(x < buffer_start) & (x >= buffer_end), color='red', alpha=0.2) ax.fill_between(x_pct, y, start, where=(x < buffer_end), color='red', alpha=0.2)

# Annotations
ax.axhline(start, linestyle='dashed', color='black', alpha=0.6)
ax.annotate(f"Start: ${start:.2f}", xy=(0, start), xytext=(-60, 20), textcoords='offset points',
            arrowprops=dict(arrowstyle="->"), fontsize=10, bbox=dict(boxstyle="round", fc="white"))

ax.annotate(f"Cap: +{cap*100:.1f}%\n${cap_value:.2f}", xy=(cap*100, cap_value), xytext=(-10, 40), textcoords='offset points',
            arrowprops=dict(arrowstyle="->"), fontsize=10, bbox=dict(boxstyle="round", fc="white"))

ax.annotate(f"Buffer Start\n{buffer_start*100:.1f}%", xy=(buffer_start*100, buffer_start_value), xytext=(-20, -50),
            textcoords='offset points', arrowprops=dict(arrowstyle="->"), fontsize=10, bbox=dict(boxstyle="round", fc="white"))

ax.annotate(f"Buffer End\n{buffer_end*100:.1f}%", xy=(buffer_end*100, buffer_end_value), xytext=(-60, 25),
            textcoords='offset points', arrowprops=dict(arrowstyle="->"), fontsize=10, bbox=dict(boxstyle="round", fc="white"))

# Simulated Point
ax.plot(test_return * 100, test_payoff, marker='*', color='black', markersize=12, label='Simulated Point')

ax.set_xlabel('Underlying Asset Return (%)') ax.set_ylabel('ETF Value ($)') ax.set_title(f'Buffered ETF Payoff — {selected_etf}', fontsize=15) ax.grid(True, linestyle='--', alpha=0.4)
ax.legend()



st.pyplot(fig)

# Historical
st.subheader("📈 Normalized Performance Chart") etf_hist = yf.Ticker(selected_etf).history(start=outcome_start, end=today)[['Close']].rename(columns={'Close': selected_etf}) asset_hist = yf.Ticker(underlying_ticker).history(start=outcome_start, end=today)[['Close']].rename(columns={'Close': underlying_asset}) if underlying_ticker else pd.DataFrame()

if not etf_hist.empty and not asset_hist.empty:
    combined = pd.merge(etf_hist, asset_hist, left_index=True, right_index=True)
    norm = pd.DataFrame(index=combined.index)
    norm[selected_etf] = (combined[selected_etf] / start - 1) * 100
    norm[underlying_asset] = (combined[underlying_asset] / ref_price - 1) * 100
    norm.iloc[0] = [0, 0]
    
    norm.iloc[-1, norm.columns.get_loc(selected_etf)] = (live_etf_price / start - 1) * 100
    norm.iloc[-1, norm.columns.get_loc(underlying_asset)] = (live_underlying_price / ref_price - 1) * 100


    fig2, ax2 = plt.subplots(figsize=(12, 6))
    ax2.plot(norm.index, norm[selected_etf], label=selected_etf, linewidth=2)
    ax2.plot(norm.index, norm[underlying_asset], label=underlying_asset, linewidth=2, linestyle='--')
    ax2.axhline(0, linestyle='--', color='black', linewidth=1)

    for idx, label in [(norm[underlying_asset].idxmax(), 'High'), (norm[underlying_asset].idxmin(), 'Low'), (norm.index[-1], 'Today')]:
        etf_ret = norm.loc[idx, selected_etf]
        under_ret = norm.loc[idx, underlying_asset]
        delta = under_ret - etf_ret
        ax2.annotate(f"{label}:\n{under_ret:.2f}%\nETF: {etf_ret:.2f}%\nΔ: {delta:.2f}%", 
                     xy=(idx, under_ret), xytext=(-80, 10), textcoords='offset points',
                     arrowprops=dict(arrowstyle='->'), fontsize=10, bbox=dict(boxstyle="round", fc="white"))

    ax2.set_title(f"{selected_etf} vs {underlying_asset} — % Return Since Start", fontsize=14)
    ax2.set_ylabel("Return (%)")
    ax2.set_xlabel("Date")
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.4)
    fig2.tight_layout()
    st.pyplot(fig2)
else:
    st.info("ℹ️ Not enough data to plot normalized performance.")



