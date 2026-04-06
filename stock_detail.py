import streamlit as st
from datetime import datetime
import yfinance as yf

st.set_page_config(
    page_title="美股个股分析",
    page_icon="📊",
    layout="wide"
)


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


@st.cache_data(ttl=300)
def get_stock_info(ticker_symbol):
    try:
        tk = yf.Ticker(ticker_symbol)
        info = tk.info or {}
        return info
    except Exception as e:
        return {}


def main():
    query_params = st.query_params
    default_symbol = query_params.get('symbol', 'MSFT') if query_params else 'MSFT'
    
    if 'search_stock' not in st.session_state:
        st.session_state.search_stock = default_symbol

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

    st.markdown(f"""
    <div style="text-align: center; margin: 20px 0;">
        <a href="/" style="color: #00a4ff; text-decoration: none; font-size: 0.9rem;">← 返回首页</a>
    </div>
    """, unsafe_allow_html=True)

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


if __name__ == "__main__":
    main()