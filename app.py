import streamlit as st
import requests
import fear_greed as fg
from datetime import datetime
import yfinance as yf
import time

st.set_page_config(
    page_title="美股估值器",
    page_icon="📈",
    layout="wide"
)

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
    return get_ticker_pe("SPY")

@st.cache_data(ttl=3600)
def get_ndx_valuation():
    return get_ticker_pe("QQQ")

@st.cache_data(ttl=3600)
def get_fear_greed():
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

def main():
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
        backdrop-filter: blur(10px);
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
    .refresh-icon {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    .stButton > button {
        background: transparent !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: #888 !important;
    }
    .stButton > button:hover {
        background: rgba(255,255,255,0.05) !important;
    }
    .fg-meter-container {
        margin: 16px 0;
    }
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
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="title-section">
        <div class="main-title">📈 美股估值器</div>
        <div class="subtitle">纳斯达克100 · 标普500 · CNN恐惧贪婪指数</div>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_center, col_right = st.columns([1, 1, 1])
    with col_center:
        if st.button("🔄"):
            st.rerun()

    st.markdown(f'<div class="last-update">最后更新: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)

    sp500_pe = get_sp500_pe()
    ndx_pe = get_ndx_valuation()
    fear_greed_value = get_fear_greed()

    sp500_historical = (15, 18, 22, 28)
    ndx_historical = (20, 25, 35, 45)

    sp500_status, sp500_color = get_valuation_status(sp500_pe, sp500_historical)
    ndx_status, ndx_color = get_valuation_status(ndx_pe, ndx_historical)

    sp500_display = f"{sp500_pe:.2f}" if sp500_pe else "—"
    ndx_display = f"{ndx_pe:.2f}" if ndx_pe else "—"
    fg_display = f"{fear_greed_value:.2f}" if fear_greed_value else "—"

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">纳斯达克100 (QQQ ETF) <a href="https://finance.yahoo.com/quote/QQQ" target="_blank">[来源]</a></div>
            <div class="big-value" style="color: #00a4ff;">{ndx_display}</div>
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
            <div class="big-value" style="color: #00c864;">{sp500_display}</div>
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

    meter_position = fear_greed_value if fear_greed_value else 50
    
    with col3:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">CNN恐惧贪婪指数 <a href="https://edition.cnn.com/markets/fear-and-greed" target="_blank">[来源]</a></div>
            <div class="big-value" style="color: #ff6b6b;">{fg_display}</div>
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
    st.markdown("""
    <div style="text-align: center; color: #555; font-size: 0.8rem; padding: 20px;">
        估值仅供参考，投资有风险，入市需谨慎
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
