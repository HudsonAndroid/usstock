import streamlit as st
import requests
import fear_greed as fg
from datetime import datetime
import yfinance as yf
import time
import logging
import traceback
import os

log_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(log_dir, 'app.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

query_params = st.query_params
page = query_params.get('page', 'home') if query_params else 'home'

if page == 'detail':
    st.set_page_config(page_title="美股个股分析", page_icon="📊", layout="wide")
else:
    st.set_page_config(page_title="美股Dashboard", page_icon="📈", layout="wide")


def format_number(num):
    if num is None:
        return "N/A"
    if abs(num) >= 1e12:
        return f"{num/1e12:.2f}T"
    elif abs(num) >= 1e9:
        return f"{num/1e9:.2f}B"
    elif abs(num) >= 1e6:
        return f"{num/1e6:.2f}M"
    elif abs(num) >= 1e3:
        return f"{num/1e3:.2f}K"
    else:
        return f"{num:.2f}"


def get_ticker_pe(ticker, max_retries=3):
    for i in range(max_retries):
        try:
            time.sleep(1)
            tk = yf.Ticker(ticker)
            info = tk.info or {}
            pe = info.get('trailingPE')
            if pe and 10 < float(pe) < 100:
                return float(pe)
            if i < max_retries - 1:
                time.sleep(2)
        except Exception as e:
            if i < max_retries - 1:
                time.sleep(2)
            else:
                print(f"{ticker} Error: {e}")
    return None


@st.cache_data(ttl=3600)
def get_sp500_pe():
    MOCK_MODE = False
    if MOCK_MODE:
        return 24.5
    return get_ticker_pe("SPY")


@st.cache_data(ttl=3600)
def get_ndx_valuation():
    MOCK_MODE = False
    if MOCK_MODE:
        return 32.8
    return get_ticker_pe("QQQ")


@st.cache_data(ttl=3600)
def get_fear_greed():
    MOCK_MODE = False
    if MOCK_MODE:
        return 45.0
    try:
        score = fg.get_score()
        return score
    except:
        return None


def get_valuation_status(pe, pe_historical):
    if pe is None:
        return "无数据", "gray"
    if pe < pe_historical[0]:
        return "极低", "green"
    elif pe < pe_historical[1]:
        return "偏低", "lightgreen"
    elif pe < pe_historical[2]:
        return "适中", "yellow"
    elif pe < pe_historical[3]:
        return "偏高", "orange"
    else:
        return "极高", "red"


def get_index_color(pe, pe_historical):
    if pe is None:
        return "#888888"
    if pe < pe_historical[0]:
        return "#00c864"
    elif pe < pe_historical[1]:
        return "#78c864"
    elif pe < pe_historical[2]:
        return "#ffc800"
    elif pe < pe_historical[3]:
        return "#ff8c00"
    else:
        return "#ff3232"


@st.cache_data(ttl=300)
def get_stock_info(ticker_symbol):
    MOCK_MODE = False
    
    if MOCK_MODE:
        mock_data = {
            'MSFT': {'shortName': 'Microsoft Corporation', 'currentPrice': 425.50, 'trailingPE': 35.2, 'priceToBook': 12.5, 'forwardPE': 28.1, 'pegRatio': 2.1, 'marketCap': 3160000000000, 'sector': 'Technology', 'industry': 'Software', 'beta': 0.91, 'fiftyTwoWeekHigh': 468.35, 'fiftyTwoWeekLow': 309.45, 'fiftyDayAverage': 418.20, 'twoHundredDayAverage': 398.50, 'dividendYield': 0.0072, 'dividendRate': 3.00, 'volume': 24500000, 'averageVolume': 22300000, 'recommendKey': 'Buy', 'targetMeanPrice': 480.00, 'priceToSalesForward': 12.3, 'totalRevenue': 211000000000, 'grossProfit': 135000000000, 'operatingIncome': 89000000000, 'ebitda': 105000000000, 'profitMargins': 0.36, 'operatingMargins': 0.42, 'returnOnEquity': 0.38, 'returnOnAssets': 0.15, 'totalDebt': 42000000000, 'totalCash': 81000000000},
            'GOOGL': {'shortName': 'Alphabet Inc.', 'currentPrice': 175.80, 'trailingPE': 25.8, 'priceToBook': 6.8, 'forwardPE': 20.5, 'pegRatio': 1.4, 'marketCap': 2180000000000, 'sector': 'Technology', 'industry': 'Internet', 'beta': 1.05, 'fiftyTwoWeekHigh': 191.75, 'fiftyTwoWeekLow': 120.21, 'fiftyDayAverage': 168.50, 'twoHundredDayAverage': 155.30, 'dividendYield': 0, 'dividendRate': 0, 'volume': 18900000, 'averageVolume': 21500000, 'recommendKey': 'Buy', 'targetMeanPrice': 190.00, 'priceToSalesForward': 5.8, 'totalRevenue': 305000000000, 'grossProfit': 177000000000, 'operatingIncome': 84000000000, 'ebitda': 99000000000, 'profitMargins': 0.24, 'operatingMargins': 0.28, 'returnOnEquity': 0.25, 'returnOnAssets': 0.14, 'totalDebt': 15000000000, 'totalCash': 113000000000},
            'AAPL': {'shortName': 'Apple Inc.', 'currentPrice': 192.50, 'trailingPE': 31.2, 'priceToBook': 45.2, 'forwardPE': 26.8, 'pegRatio': 2.3, 'marketCap': 2980000000000, 'sector': 'Technology', 'industry': 'Consumer Electronics', 'beta': 1.28, 'fiftyTwoWeekHigh': 199.62, 'fiftyTwoWeekLow': 124.17, 'fiftyDayAverage': 185.40, 'twoHundredDayAverage': 172.80, 'dividendYield': 0.0051, 'dividendRate': 0.96, 'volume': 51200000, 'averageVolume': 48500000, 'recommendKey': 'Buy', 'targetMeanPrice': 210.00, 'priceToSalesForward': 8.5, 'totalRevenue': 385000000000, 'grossProfit': 203000000000, 'operatingIncome': 114000000000, 'ebitda': 128000000000, 'profitMargins': 0.26, 'operatingMargins': 0.30, 'returnOnEquity': 1.52, 'returnOnAssets': 0.28, 'totalDebt': 110000000000, 'totalCash': 67000000000},
            'NVDA': {'shortName': 'NVIDIA Corporation', 'currentPrice': 875.30, 'trailingPE': 65.8, 'priceToBook': 48.5, 'forwardPE': 42.3, 'pegRatio': 1.8, 'marketCap': 2160000000000, 'sector': 'Technology', 'industry': 'Semiconductors', 'beta': 1.65, 'fiftyTwoWeekHigh': 974.00, 'fiftyTwoWeekLow': 222.97, 'fiftyDayAverage': 820.50, 'twoHundredDayAverage': 650.20, 'dividendYield': 0.0003, 'dividendRate': 0.16, 'volume': 38500000, 'averageVolume': 41200000, 'recommendKey': 'Buy', 'targetMeanPrice': 950.00, 'priceToSalesForward': 25.2, 'totalRevenue': 61000000000, 'grossProfit': 33000000000, 'operatingIncome': 28000000000, 'ebitda': 30000000000, 'profitMargins': 0.45, 'operatingMargins': 0.46, 'returnOnEquity': 0.72, 'returnOnAssets': 0.35, 'totalDebt': 8000000000, 'totalCash': 16000000000},
            'META': {'shortName': 'Meta Platforms Inc.', 'currentPrice': 505.20, 'trailingPE': 28.5, 'priceToBook': 6.2, 'forwardPE': 18.2, 'pegRatio': 1.2, 'marketCap': 1290000000000, 'sector': 'Technology', 'industry': 'Internet', 'beta': 1.22, 'fiftyTwoWeekHigh': 531.49, 'fiftyTwoWeekLow': 274.38, 'fiftyDayAverage': 485.60, 'twoHundredDayAverage': 420.30, 'dividendYield': 0, 'dividendRate': 0, 'volume': 15200000, 'averageVolume': 14500000, 'recommendKey': 'Buy', 'targetMeanPrice': 550.00, 'priceToSalesForward': 6.8, 'totalRevenue': 134000000000, 'grossProfit': 75000000000, 'operatingIncome': 47000000000, 'ebitda': 55000000000, 'profitMargins': 0.35, 'operatingMargins': 0.35, 'returnOnEquity': 0.32, 'returnOnAssets': 0.18, 'totalDebt': 18000000000, 'totalCash': 41000000000},
            'TSLA': {'shortName': 'Tesla Inc.', 'currentPrice': 178.50, 'trailingPE': 52.3, 'priceToBook': 9.8, 'forwardPE': 38.5, 'pegRatio': 1.5, 'marketCap': 567000000000, 'sector': 'Consumer Cyclical', 'industry': 'Auto Manufacturers', 'beta': 2.05, 'fiftyTwoWeekHigh': 299.29, 'fiftyTwoWeekLow': 152.89, 'fiftyDayAverage': 195.80, 'twoHundredDayAverage': 225.40, 'dividendYield': 0, 'dividendRate': 0, 'volume': 98000000, 'averageVolume': 105000000, 'recommendKey': 'Hold', 'targetMeanPrice': 200.00, 'priceToSalesForward': 6.2, 'totalRevenue': 96000000000, 'grossProfit': 17000000000, 'operatingIncome': 4000000000, 'ebitda': 11000000000, 'profitMargins': 0.15, 'operatingMargins': 0.04, 'returnOnEquity': 0.25, 'returnOnAssets': 0.10, 'totalDebt': 43000000000, 'totalCash': 29000000000},
            'AMZN': {'shortName': 'Amazon.com Inc.', 'currentPrice': 185.20, 'trailingPE': 42.5, 'priceToBook': 8.2, 'forwardPE': 32.1, 'pegRatio': 1.6, 'marketCap': 1920000000000, 'sector': 'Consumer Cyclical', 'industry': 'Internet', 'beta': 1.15, 'fiftyTwoWeekHigh': 201.20, 'fiftyTwoWeekLow': 118.35, 'fiftyDayAverage': 175.80, 'twoHundredDayAverage': 162.50, 'dividendYield': 0, 'dividendRate': 0, 'volume': 42500000, 'averageVolume': 38500000, 'recommendKey': 'Buy', 'targetMeanPrice': 210.00, 'priceToSalesForward': 2.5, 'totalRevenue': 575000000000, 'grossProfit': 201000000000, 'operatingIncome': 61000000000, 'ebitda': 76000000000, 'profitMargins': 0.06, 'operatingMargins': 0.11, 'returnOnEquity': 0.25, 'returnOnAssets': 0.08, 'totalDebt': 73000000000, 'totalCash': 73000000000},
            'AVGO': {'shortName': 'Broadcom Inc.', 'currentPrice': 1285.40, 'trailingPE': 58.2, 'priceToBook': 15.8, 'forwardPE': 25.5, 'pegRatio': 1.9, 'marketCap': 598000000000, 'sector': 'Technology', 'industry': 'Semiconductors', 'beta': 1.18, 'fiftyTwoWeekHigh': 1438.17, 'fiftyTwoWeekLow': 796.42, 'fiftyDayAverage': 1220.50, 'twoHundredDayAverage': 1050.20, 'dividendYield': 0.0098, 'dividendRate': 21.00, 'volume': 2800000, 'averageVolume': 3200000, 'recommendKey': 'Buy', 'targetMeanPrice': 1400.00, 'priceToSalesForward': 14.5, 'totalRevenue': 52000000000, 'grossProfit': 30000000000, 'operatingIncome': 14000000000, 'ebitda': 17000000000, 'profitMargins': 0.25, 'operatingMargins': 0.27, 'returnOnEquity': 0.55, 'returnOnAssets': 0.22, 'totalDebt': 24000000000, 'totalCash': 12000000000},
            'TSM': {'shortName': 'Taiwan Semiconductor', 'currentPrice': 142.80, 'trailingPE': 22.5, 'priceToBook': 4.8, 'forwardPE': 18.2, 'pegRatio': 1.1, 'marketCap': 742000000000, 'sector': 'Technology', 'industry': 'Semiconductors', 'beta': 1.08, 'fiftyTwoWeekHigh': 173.56, 'fiftyTwoWeekLow': 93.96, 'fiftyDayAverage': 138.50, 'twoHundredDayAverage': 125.30, 'dividendYield': 0.0158, 'dividendRate': 1.82, 'volume': 8500000, 'averageVolume': 9200000, 'recommendKey': 'Buy', 'targetMeanPrice': 160.00, 'priceToSalesForward': 6.2, 'totalRevenue': 75000000000, 'grossProfit': 38000000000, 'operatingIncome': 29000000000, 'ebitda': 33000000000, 'profitMargins': 0.38, 'operatingMargins': 0.39, 'returnOnEquity': 0.35, 'returnOnAssets': 0.20, 'totalDebt': 18000000000, 'totalCash': 42000000000},
        }
        ticker = ticker_symbol.upper()
        if ticker in mock_data:
            return mock_data[ticker]
        return {}
    
    try:
        tk = yf.Ticker(ticker_symbol)
        info = tk.info or {}
        return info
    except Exception as e:
        return {}


def get_pe_color(pe, max_pe=60):
    if pe is None:
        return "#888888"
    pct = min(pe / max_pe * 100, 100)
    if pct < 30:
        return "#00c864"
    elif pct < 50:
        return "#78c864"
    elif pct < 70:
        return "#ffc800"
    elif pct < 85:
        return "#ff8c00"
    else:
        return "#ff3232"


def get_pe_gauge_html(pe_value, max_pe=60, color=None):
    if pe_value is None:
        percentage = 0
    else:
        percentage = min(pe_value / max_pe * 100, 100)
    
    if color is None:
        color = "#78c864"
    
    svg = f"""
    <svg viewBox="0 0 200 120" style="width: 100%; max-width: 200px;">
        <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="16" stroke-linecap="round"/>
        <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="{color}" stroke-width="16" stroke-linecap="round" stroke-dasharray="{percentage * 2.51} 251"/>
        <text x="100" y="85" text-anchor="middle" fill="white" font-size="24" font-weight="bold">{pe_value if pe_value else "--"}</text>
        <text x="100" y="105" text-anchor="middle" fill="#888" font-size="12">PE</text>
    </svg>
    """
    return svg


def get_pb_gauge_html(pb_value, max_pb=20):
    if pb_value is None:
        percentage = 0
    else:
        percentage = min(pb_value / max_pb * 100, 100)
    
    svg = f"""
    <svg viewBox="0 0 200 120" style="width: 100%; max-width: 200px;">
        <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="16" stroke-linecap="round"/>
        <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="#00a4ff" stroke-width="16" stroke-linecap="round" stroke-dasharray="{percentage * 2.51} 251"/>
        <text x="100" y="85" text-anchor="middle" fill="white" font-size="24" font-weight="bold">{pb_value if pb_value else "--"}</text>
        <text x="100" y="105" text-anchor="middle" fill="#888" font-size="12">PB</text>
    </svg>
    """
    return svg


def render_stock_card(stock, symbol):
    price = stock.get('price', 0)
    price_str = f"${price:.2f}" if price else "--"
    pe = stock.get('pe')
    pb = stock.get('pb')
    pe_pct = min((pe / 60 * 100) if pe else 0, 100)
    pb_pct = min((pb / 20 * 100) if pb else 0, 100)
    pe_color = get_pe_color(pe)
    
    target = stock.get('target')
    upside = 0
    if target and price:
        upside = (target - price) / price * 100
    
    profit_val = stock.get('profit')
    profit_str = f"${profit_val/1e9:.1f}B" if profit_val and profit_val > 0 else "N/A"
    
    pe_str = f"{pe:.1f}" if pe else "--"
    pb_str = f"{pb:.1f}" if pb else "--"
    target_str = f"${target:.2f}" if target else "--"
    upside_str = f"+{upside:.1f}%" if upside > 0 else (f"{upside:.1f}%" if upside else "--")
    high_str = f"${stock.get('52w_high', 0):.2f}" if stock.get('52w_high') else "--"
    low_str = f"${stock.get('52w_low', 0):.2f}" if stock.get('52w_low') else "--"
    
    html = f"""
    <div style="background: rgba(255,255,255,0.08); padding: 20px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.1); flex: 0 0 320px; max-width: 350px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.1);">
            <div>
                <div style="color:white;font-size:1rem;font-weight:600">{stock.get('name', symbol)}</div>
                <a href="?page=detail&symbol={symbol}" style="color:#00a4ff;font-size:0.75rem;text-decoration:none;">{symbol} ↗</a>
            </div>
            <div style="color:#00c864;font-size:1.4rem;font-weight:700">{price_str}</div>
        </div>
        
        <div style="display: flex; gap: 24px; margin: 16px 0;">
            <div style="flex:1">
                <div style="color:#888;font-size:0.7rem;margin-bottom:6px">PE</div>
                <div style="height:10px;background:rgba(255,255,255,0.1);border-radius:5px;overflow:hidden;">
                    <div style="width:{pe_pct}%;height:100%;background:{pe_color};border-radius:5px;"></div>
                </div>
                <div style="color:white;font-size:0.95rem;font-weight:600;margin-top:4px">{pe_str}</div>
            </div>
            <div style="flex:1">
                <div style="color:#888;font-size:0.7rem;margin-bottom:6px">PB</div>
                <div style="height:10px;background:rgba(255,255,255,0.1);border-radius:5px;overflow:hidden;">
                    <div style="width:{pb_pct}%;height:100%;background:#00a4ff;border-radius:5px;"></div>
                </div>
                <div style="color:white;font-size:0.95rem;font-weight:600;margin-top:4px">{pb_str}</div>
            </div>
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
            <div style="background: rgba(255,255,255,0.05); padding: 8px; border-radius: 6px;">
                <div style="color:#888;font-size:0.6rem">52周区间</div>
                <div style="color:#ff6b6b;font-size:0.85rem">{high_str}</div>
                <div style="color:#00c864;font-size:0.85rem">{low_str}</div>
            </div>
            <div style="background: rgba(255,255,255,0.05); padding: 8px; border-radius: 6px;">
                <div style="color:#888;font-size:0.6rem">目标价/空间</div>
                <div style="color:#ffc800;font-size:0.85rem">{target_str}</div>
                <div style="color:#00c864;font-size:0.85rem">{upside_str}</div>
            </div>
        </div>
        
        <div style="margin-top: 12px; padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.1); display: flex; align-items: center; gap: 8px;">
            <span style="color:#888;font-size:0.7rem">净利润</span>
            <span style="background: rgba(0,200,100,0.15); color:#00c864; padding: 3px 10px; border-radius: 4px; font-size: 0.8rem; font-weight: 600;">{profit_str}</span>
        </div>
    </div>
    """
    return html


def render_home_page():
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        min-height: 100vh;
    }
    .card {
        background: rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 24px;
        margin: 12px 0;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .card-title {
        font-size: 1.1rem;
        color: #a0a0a0;
        margin-bottom: 16px;
        font-weight: 500;
    }
    .card-title a {
        color: #666;
        text-decoration: none;
        font-size: 0.8rem;
    }
    .card-title a:hover {
        color: #00a4ff;
    }
    .big-value {
        font-size: 2.8rem;
        font-weight: 700;
        margin: 8px 0;
    }
    .status-label {
        font-size: 1.2rem;
        padding: 6px 16px;
        border-radius: 8px;
        display: inline-block;
    }
    .status-green { background: rgba(0,200,100,0.2); color: #00c864; }
    .status-lightgreen { background: rgba(120,200,100,0.2); color: #78c864; }
    .status-yellow { background: rgba(255,200,0,0.2); color: #ffc800; }
    .status-orange { background: rgba(255,140,0,0.2); color: #ff8c00; }
    .status-red { background: rgba(255,50,50,0.2); color: #ff3232; }
    .status-gray { background: rgba(128,128,128,0.2); color: #808080; }
    .metric-row {
        display: flex;
        justify-content: space-between;
        padding: 8px 0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    .metric-label { color: #888; }
    .metric-value { color: #fff; font-weight: 500; }
    .title-section {
        text-align: center;
        padding: 30px 0 20px;
    }
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00c864, #00a4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }
    .subtitle {
        color: #666;
        font-size: 0.95rem;
    }
    .last-update {
        text-align: center;
        color: #444;
        font-size: 0.85rem;
        margin-bottom: 20px;
    }
    .stButton > button {
        background: transparent !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: #888 !important;
    }
    .stButton > button:hover {
        background: rgba(255,255,255,0.05) !important;
    }
    .fg-meter-container { margin: 16px 0; }
    .fg-meter {
        height: 20px;
        border-radius: 10px;
        background: linear-gradient(to right, 
            #00c864 0%, #00c864 25%, 
            #78c864 25%, #78c864 45%, 
            #ffc800 45%, #ffc800 55%, 
            #ff8c00 55%, #ff8c00 75%, 
            #ff3232 75%, #ff3232 100%);
        position: relative;
    }
    .fg-indicator {
        position: absolute;
        top: -6px;
        width: 4px;
        height: 32px;
        background: white;
        border-radius: 2px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.5);
        transition: left 0.3s ease;
    }
    .fg-labels {
        display: flex;
        justify-content: space-between;
        font-size: 0.65rem;
        color: #888;
        margin-top: 2px;
    }
    .fg-ticks {
        display: flex;
        justify-content: space-between;
        font-size: 0.6rem;
        color: #666;
        margin-top: -12px;
        padding-bottom: 8px;
    }
    .section-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #fff;
        margin: 24px 0 16px;
        padding-bottom: 8px;
        border-bottom: 2px solid rgba(0,164,255,0.3);
    }
    #MainMenu {visibility: hidden;}
    .stDeployButton {display: none;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="title-section">
        <div class="main-title">📈 美股Dashboard</div>
        <div class="subtitle">纳斯达克100 · 标普500 · CNN恐惧贪婪指数</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="last-update">最后更新: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)

    sp500_pe = get_sp500_pe()
    ndx_pe = get_ndx_valuation()
    fear_greed_value = get_fear_greed()
    meter_position = fear_greed_value if fear_greed_value else 50
    
    sp500_historical = (15, 18, 22, 28)
    ndx_historical = (20, 25, 35, 45)

    sp500_status, sp500_color = get_valuation_status(sp500_pe, sp500_historical)
    ndx_status, ndx_color = get_valuation_status(ndx_pe, ndx_historical)

    sp500_display = f"{sp500_pe:.2f}" if sp500_pe else "—"
    ndx_display = f"{ndx_pe:.2f}" if ndx_pe else "—"
    fg_display = f"{fear_greed_value:.2f}" if fear_greed_value else "—"
    
    ndx_color_val = get_index_color(ndx_pe, ndx_historical)
    sp500_color_val = get_index_color(sp500_pe, sp500_historical)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">纳斯达克100 (QQQ ETF) <a href="https://finance.yahoo.com/quote/QQQ" target="_blank">[来源]</a></div>
            <div class="big-value" style="color: {ndx_color_val};">{ndx_display}</div>
            <div class="status-label status-{ndx_color}">{ndx_status}</div>
            <div style="margin-top: 16px;">
                <div class="metric-row"><span class="metric-label">当前PE</span><span class="metric-value">{ndx_display}</span></div>
                <div class="metric-row"><span class="metric-label">极低估值</span><span class="metric-value">&lt; {ndx_historical[0]}</span></div>
                <div class="metric-row"><span class="metric-label">偏低估值</span><span class="metric-value">&lt; {ndx_historical[1]}</span></div>
                <div class="metric-row"><span class="metric-label">适中估值</span><span class="metric-value">{ndx_historical[1]} - {ndx_historical[2]}</span></div>
                <div class="metric-row"><span class="metric-label">偏高估值</span><span class="metric-value">&gt; {ndx_historical[2]}</span></div>
                <div class="metric-row"><span class="metric-label">极高估值</span><span class="metric-value">&gt; {ndx_historical[3]}</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">标普500 (SPY ETF) <a href="https://finance.yahoo.com/quote/SPY" target="_blank">[来源]</a></div>
            <div class="big-value" style="color: {sp500_color_val};">{sp500_display}</div>
            <div class="status-label status-{sp500_color}">{sp500_status}</div>
            <div style="margin-top: 16px;">
                <div class="metric-row"><span class="metric-label">CAPE估值</span><span class="metric-value">{sp500_display}</span></div>
                <div class="metric-row"><span class="metric-label">极低估值</span><span class="metric-value">&lt; {sp500_historical[0]}</span></div>
                <div class="metric-row"><span class="metric-label">偏低估值</span><span class="metric-value">&lt; {sp500_historical[1]}</span></div>
                <div class="metric-row"><span class="metric-label">适中估值</span><span class="metric-value">{sp500_historical[1]} - {sp500_historical[2]}</span></div>
                <div class="metric-row"><span class="metric-label">偏高估值</span><span class="metric-value">&gt; {sp500_historical[2]}</span></div>
                <div class="metric-row"><span class="metric-label">极高估值</span><span class="metric-value">&gt; {sp500_historical[3]}</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    fg_label = "无数据"
    fg_color_code = "gray"
    if fear_greed_value is not None:
        if fear_greed_value <= 25:
            fg_label = "极度恐惧"
            fg_color_code = "green"
        elif fear_greed_value <= 45:
            fg_label = "恐惧"
            fg_color_code = "lightgreen"
        elif fear_greed_value <= 55:
            fg_label = "中性"
            fg_color_code = "yellow"
        elif fear_greed_value <= 75:
            fg_label = "贪婪"
            fg_color_code = "orange"
        else:
            fg_label = "极度贪婪"
            fg_color_code = "red"

    fg_color_map = {
        'green': '#00c864',
        'lightgreen': '#78c864',
        'yellow': '#ffc800',
        'orange': '#ff8c00',
        'red': '#ff3232',
        'gray': '#888888'
    }
    fg_value_color = fg_color_map.get(fg_color_code, '#888888')
    
    with col3:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">CNN恐惧贪婪指数 <a href="https://edition.cnn.com/markets/fear-and-greed" target="_blank">[来源]</a></div>
            <div class="big-value" style="color: {fg_value_color};">{fg_display}</div>
            <div class="status-label status-{fg_color_code}">{fg_label}</div>
            <div class="fg-meter-container">
                <div class="fg-meter">
                    <div class="fg-indicator" style="left: calc({meter_position}% - 2px);"></div>
                </div>
                <div class="fg-ticks">
                    <span>0</span>
                    <span>25</span>
                    <span>45</span>
                    <span>55</span>
                    <span>75</span>
                    <span>100</span>
                </div>
                <div class="fg-labels">
                    <span>极度恐惧</span>
                    <span>恐惧</span>
                    <span>中性</span>
                    <span>贪婪</span>
                    <span>极度贪婪</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    WATCH_LIST = ["MSFT", "GOOGL", "AAPL", "NVDA", "META", "TSLA", "AMZN", "AVGO", "TSM"]

    st.markdown('<div class="section-title">⭐ 核心个股</div>', unsafe_allow_html=True)

    cards_html = ""
    for symbol in WATCH_LIST:
        info = get_stock_info(symbol)
        if info and info.get('shortName'):
            stock = {
                'name': info.get('shortName', info.get('longName', symbol)),
                'price': info.get('currentPrice'),
                'pe': info.get('trailingPE'),
                'pb': info.get('priceToBook'),
                '52w_high': info.get('fiftyTwoWeekHigh'),
                '52w_low': info.get('fiftyTwoWeekLow'),
                'target': info.get('targetMeanPrice'),
                'profit': info.get('netIncomeToCommon'),
            }
            cards_html += render_stock_card(stock, symbol)
    
    st.html(f"""
    <div style="display: flex; gap: 20px; justify-content: center; flex-wrap: wrap; padding: 20px;">
        {cards_html}
    </div>
    """)

    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #555; font-size: 0.8rem; padding: 20px;">
        估值仅供参考，投资有风险，入市需谨慎
    </div>
    """, unsafe_allow_html=True)


def render_detail_page(symbol):
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        min-height: 100vh;
    }
    .card {
        background: rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 24px;
        margin: 12px 0;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .card-title {
        font-size: 1.1rem;
        color: #a0a0a0;
        margin-bottom: 16px;
        font-weight: 500;
    }
    .big-value {
        font-size: 2.8rem;
        font-weight: 700;
        margin: 8px 0;
    }
    .stock-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 24px;
    }
    .stock-name {
        font-size: 2rem;
        font-weight: 700;
        color: white;
    }
    .stock-symbol {
        font-size: 1.2rem;
        color: #00a4ff;
        margin-left: 12px;
    }
    .stock-price {
        font-size: 2.5rem;
        font-weight: 700;
        color: #00c864;
    }
    .section-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #fff;
        margin: 24px 0 16px;
        padding-bottom: 8px;
        border-bottom: 2px solid rgba(0,164,255,0.3);
    }
    .gauge-wrapper {
        text-align: center;
    }
    .data-item {
        background: rgba(255,255,255,0.05);
        padding: 12px;
        border-radius: 8px;
    }
    .data-item-label {
        font-size: 0.75rem;
        color: #888;
        margin-bottom: 4px;
    }
    .data-item-value {
        font-size: 1.1rem;
        font-weight: 600;
        color: #fff;
    }
    .positive { color: #00c864 !important; }
    .negative { color: #ff3232 !important; }
    </style>
    """, unsafe_allow_html=True)

    if st.button("← 返回首页"):
        st.query_params.clear()
        st.rerun()

    if 'search_stock' not in st.session_state:
        st.session_state.search_stock = symbol
    
    with st.form("search_form"):
        col_search, col_btn = st.columns([5, 1])
        with col_search:
            search_ticker = st.text_input("输入股票代码", value=st.session_state.search_stock, key="search_ticker")
        with col_btn:
            submitted = st.form_submit_button("🔍 查询")
            if submitted:
                st.session_state.search_stock = search_ticker.upper()
                st.rerun()
    
    if not st.session_state.search_stock:
        st.session_state.search_stock = "MSFT"
    
    with st.spinner(f"加载 {st.session_state.search_stock} 数据..."):
        info = get_stock_info(st.session_state.search_stock)
    
    if not info or not info.get('shortName'):
        st.error(f"未找到股票: {st.session_state.search_stock}")
        return

    st.markdown(f"""
    <div class="stock-header">
        <div>
            <span class="stock-name">{info.get('shortName', info.get('longName', st.session_state.search_stock))}</span>
            <span class="stock-symbol">{st.session_state.search_stock}</span>
        </div>
        <div class="stock-price">${info.get('currentPrice', 'N/A')}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">📊 估值指标</div>', unsafe_allow_html=True)
    
    pe = info.get('trailingPE')
    pb = info.get('priceToBook')
    forward_pe = info.get('forwardPE')
    peg = info.get('pegRatio')
    pe_color = get_pe_color(pe)
    
    col_g1, col_g2, col_g3, col_g4 = st.columns(4)
    with col_g1:
        st.markdown(f'<div class="gauge-wrapper">{get_pe_gauge_html(pe, color=pe_color)}</div>', unsafe_allow_html=True)
    with col_g2:
        st.markdown(f'<div class="gauge-wrapper">{get_pb_gauge_html(pb)}</div>', unsafe_allow_html=True)
    with col_g3:
        st.markdown(f"""
        <div class="gauge-wrapper">
            <svg viewBox="0 0 200 120" style="width: 100%; max-width: 200px;">
                <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="16" stroke-linecap="round"/>
                <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="#00a4ff" stroke-width="16" stroke-linecap="round" stroke-dasharray="50 251"/>
                <text x="100" y="85" text-anchor="middle" fill="white" font-size="24" font-weight="bold">{forward_pe if forward_pe else '--'}</text>
                <text x="100" y="105" text-anchor="middle" fill="#888" font-size="12">Forward PE</text>
            </svg>
        </div>
        """, unsafe_allow_html=True)
    with col_g4:
        st.markdown(f"""
        <div class="gauge-wrapper">
            <svg viewBox="0 0 200 120" style="width: 100%; max-width: 200px;">
                <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="16" stroke-linecap="round"/>
                <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="#78c864" stroke-width="16" stroke-linecap="round" stroke-dasharray="30 251"/>
                <text x="100" y="85" text-anchor="middle" fill="white" font-size="24" font-weight="bold">{peg if peg else '--'}</text>
                <text x="100" y="105" text-anchor="middle" fill="#888" font-size="12">PEG</text>
            </svg>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">📈 基本信息</div>', unsafe_allow_html=True)
    
    col_b1, col_b2, col_b3, col_b4 = st.columns(4)
    with col_b1:
        st.markdown(f"""
        <div class="data-item">
            <div class="data-item-label">总市值</div>
            <div class="data-item-value">{format_number(info.get('marketCap'))}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_b2:
        st.markdown(f"""
        <div class="data-item">
            <div class="data-item-label">Sector</div>
            <div class="data-item-value" style="font-size: 0.9rem;">{info.get('sector', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_b3:
        st.markdown(f"""
        <div class="data-item">
            <div class="data-item-label">Industry</div>
            <div class="data-item-value" style="font-size: 0.9rem;">{info.get('industry', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_b4:
        st.markdown(f"""
        <div class="data-item">
            <div class="data-item-label">Beta</div>
            <div class="data-item-value">{info.get('beta', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)
    
    col_b5, col_b6, col_b7, col_b8 = st.columns(4)
    with col_b5:
        st.markdown(f"""
        <div class="data-item">
            <div class="data-item-label">52周最高</div>
            <div class="data-item-value negative">${info.get('fiftyTwoWeekHigh', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_b6:
        st.markdown(f"""
        <div class="data-item">
            <div class="data-item-label">52周最低</div>
            <div class="data-item-value positive">${info.get('fiftyTwoWeekLow', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_b7:
        st.markdown(f"""
        <div class="data-item">
            <div class="data-item-label">50日均线</div>
            <div class="data-item-value">${info.get('fiftyDayAverage', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_b8:
        st.markdown(f"""
        <div class="data-item">
            <div class="data-item-label">200日均线</div>
            <div class="data-item-value">${info.get('twoHundredDayAverage', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)
    
    col_b9, col_b10, col_b11, col_b12 = st.columns(4)
    with col_b9:
        dy = info.get('dividendYield')
        st.markdown(f"""
        <div class="data-item">
            <div class="data-item-label">股息率</div>
            <div class="data-item-value">{f"{dy*100:.2f}%" if dy else 'N/A'}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_b10:
        st.markdown(f"""
        <div class="data-item">
            <div class="data-item-label">股息</div>
            <div class="data-item-value">${info.get('dividendRate', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_b11:
        st.markdown(f"""
        <div class="data-item">
            <div class="data-item-label">成交量</div>
            <div class="data-item-value">{format_number(info.get('volume'))}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_b12:
        st.markdown(f"""
        <div class="data-item">
            <div class="data-item-label">平均成交量</div>
            <div class="data-item-value">{format_number(info.get('averageVolume'))}</div>
        </div>
        """, unsafe_allow_html=True)
    
    rec = info.get('recommendKey', '')
    if rec:
        rec_class = 'rec-buy' if 'Buy' in rec else ('rec-sell' if 'Sell' in rec else 'rec-hold')
        st.markdown(f"""
        <div style="text-align: center; margin: 20px 0;">
            <span style="font-size: 1.2rem; padding: 8px 20px; border-radius: 8px; background: rgba(0,200,100,0.2); color: #00c864;">{rec}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">🎯 分析师数据</div>', unsafe_allow_html=True)
    
    col_a1, col_a2, col_a3 = st.columns(3)
    with col_a1:
        target = info.get('targetMeanPrice')
        current = info.get('currentPrice')
        if target and current:
            upside = (target - current) / current * 100
            upside_class = 'positive' if upside > 0 else 'negative'
            st.markdown(f"""
            <div class="data-item">
                <div class="data-item-label">目标价</div>
                <div class="data-item-value">${target:.2f}</div>
                <div class="data-item-label" style="margin-top: 8px;">上涨空间</div>
                <div class="data-item-value {upside_class}">{upside:+.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="data-item">
                <div class="data-item-label">目标价</div>
                <div class="data-item-value">N/A</div>
            </div>
            """, unsafe_allow_html=True)
    with col_a2:
        st.markdown(f"""
        <div class="data-item">
            <div class="data-item-label">分析师数量</div>
            <div class="data-item-value">{info.get('recommendMean', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_a3:
        st.markdown(f"""
        <div class="data-item">
            <div class="data-item-label">PS</div>
            <div class="data-item-value">{info.get('priceToSalesForward', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">💰 财务数据</div>', unsafe_allow_html=True)
    
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    with col_f1:
        st.markdown(f"""
        <div class="data-item">
            <div class="data-item-label">营收</div>
            <div class="data-item-value">{format_number(info.get('totalRevenue'))}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_f2:
        st.markdown(f"""
        <div class="data-item">
            <div class="data-item-label">毛利</div>
            <div class="data-item-value">{format_number(info.get('grossProfit'))}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_f3:
        st.markdown(f"""
        <div class="data-item">
            <div class="data-item-label">营业利润</div>
            <div class="data-item-value">{format_number(info.get('operatingIncome'))}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_f4:
        st.markdown(f"""
        <div class="data-item">
            <div class="data-item-label">EBITDA</div>
            <div class="data-item-value">{format_number(info.get('ebitda'))}</div>
        </div>
        """, unsafe_allow_html=True)
    
    col_f5, col_f6, col_f7, col_f8 = st.columns(4)
    with col_f5:
        pm = info.get('profitMargins')
        st.markdown(f"""
        <div class="data-item">
            <div class="data-item-label">净利润率</div>
            <div class="data-item-value">{f"{pm*100:.2f}%" if pm else 'N/A'}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_f6:
        om = info.get('operatingMargins')
        st.markdown(f"""
        <div class="data-item">
            <div class="data-item-label">营业利润率</div>
            <div class="data-item-value">{f"{om*100:.2f}%" if om else 'N/A'}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_f7:
        roe = info.get('returnOnEquity')
        st.markdown(f"""
        <div class="data-item">
            <div class="data-item-label">ROE</div>
            <div class="data-item-value">{f"{roe*100:.2f}%" if roe else 'N/A'}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_f8:
        roa = info.get('returnOnAssets')
        st.markdown(f"""
        <div class="data-item">
            <div class="data-item-label">ROA</div>
            <div class="data-item-value">{f"{roa*100:.2f}%" if roa else 'N/A'}</div>
        </div>
        """, unsafe_allow_html=True)
    
    col_f9, col_f10 = st.columns(2)
    with col_f9:
        st.markdown(f"""
        <div class="data-item">
            <div class="data-item-label">总债务</div>
            <div class="data-item-value">{format_number(info.get('totalDebt'))}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_f10:
        st.markdown(f"""
        <div class="data-item">
            <div class="data-item-label">总现金</div>
            <div class="data-item-value">{format_number(info.get('totalCash'))}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #555; font-size: 0.8rem; padding: 20px;">
        最后更新: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | 估值仅供参考，投资有风险，入市需谨慎
    </div>
    """, unsafe_allow_html=True)


def main():
    try:
        logger.info(f"Starting app - page: {page}")
        if page == 'detail':
            symbol = query_params.get('symbol', 'MSFT') if query_params else 'MSFT'
            logger.info(f"Rendering detail page for symbol: {symbol}")
            render_detail_page(symbol)
        else:
            logger.info("Rendering home page")
            render_home_page()
    except Exception as e:
        logger.error(f"App error: {str(e)}")
        logger.error(traceback.format_exc())
        st.error(f"发生错误: {str(e)}")


if __name__ == "__main__":
    main()