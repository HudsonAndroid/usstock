import streamlit as st
import requests
import fear_greed as fg
from datetime import datetime
import yfinance as yf
import time

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


@st.cache_data(ttl=300)
def get_stock_info(ticker_symbol):
    try:
        tk = yf.Ticker(ticker_symbol)
        info = tk.info or {}
        return info
    except Exception as e:
        return {}


def get_pe_gauge_html(pe_value, max_pe=60):
    if pe_value is None:
        percentage = 0
    else:
        percentage = min(pe_value / max_pe * 100, 100)
    
    svg = f"""
    <svg viewBox="0 0 200 120" style="width: 100%; max-width: 200px;">
        <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="16" stroke-linecap="round"/>
        <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="#78c864" stroke-width="16" stroke-linecap="round" stroke-dasharray="{percentage * 2.51} 251"/>
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
                    <div style="width:{pe_pct}%;height:100%;background:linear-gradient(90deg,#00c864,#78c864,#ffc800,#ff8c00,#ff3232);border-radius:5px;"></div>
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
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="title-section">
        <div class="main-title">📈 美股Dashboard</div>
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
    
    col_search, col_btn = st.columns([4, 1])
    with col_search:
        search_ticker = st.text_input("输入股票代码", value=st.session_state.search_stock, key="search_ticker")
    with col_btn:
        if st.button("🔍 查询", key="search_btn"):
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
    
    col_g1, col_g2, col_g3, col_g4 = st.columns(4)
    with col_g1:
        st.markdown(f'<div class="gauge-wrapper">{get_pe_gauge_html(pe)}</div>', unsafe_allow_html=True)
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
    if page == 'detail':
        symbol = query_params.get('symbol', 'MSFT') if query_params else 'MSFT'
        render_detail_page(symbol)
    else:
        render_home_page()


if __name__ == "__main__":
    main()