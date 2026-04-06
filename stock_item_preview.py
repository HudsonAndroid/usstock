import streamlit as st
import urllib.parse

st.set_page_config(page_title="个股卡片预览", page_icon="📋", layout="wide")

pe_value = 35.6
pb_value = 12.5
pe_pct = min(pe_value / 60 * 100, 100)
pb_pct = min(pb_value / 20 * 100, 100)

query_params = st.query_params
if 'symbol' in query_params:
    st.session_state.selected_symbol = query_params['symbol']
    st.query_params.clear()

html = f"""
<style>
.stApp {{ background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); }}
.stMarkdown a {{ text-decoration: none; }}
</style>
<h2 style="color:white;text-align:center;margin:30px 0;">📋 个股卡片预览</h2>

<div style="display: flex; gap: 20px; justify-content: center; flex-wrap: wrap; padding: 20px;">
    <div style="background: rgba(255,255,255,0.08); padding: 20px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.1); flex: 0 0 320px; max-width: 350px; cursor: pointer;" onclick="window.location.href='?symbol=MSFT'">
        
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.1);">
            <div>
                <div style="color:white;font-size:1rem;font-weight:600">Microsoft</div>
                <a href="?symbol=MSFT" style="color:#00a4ff;font-size:0.75rem;text-decoration:none;">MSFT ↗</a>
            </div>
            <div style="color:#00c864;font-size:1.4rem;font-weight:700">$412.56</div>
        </div>
        
        <div style="display: flex; gap: 24px; margin: 16px 0;">
            <div style="flex:1">
                <div style="color:#888;font-size:0.7rem;margin-bottom:6px">PE</div>
                <div style="height:10px;background:rgba(255,255,255,0.1);border-radius:5px;overflow:hidden;">
                    <div style="width:{pe_pct}%;height:100%;background:linear-gradient(90deg,#00c864,#78c864,#ffc800,#ff8c00,#ff3232);border-radius:5px;"></div>
                </div>
                <div style="color:white;font-size:0.95rem;font-weight:600;margin-top:4px">{pe_value}</div>
            </div>
            <div style="flex:1">
                <div style="color:#888;font-size:0.7rem;margin-bottom:6px">PB</div>
                <div style="height:10px;background:rgba(255,255,255,0.1);border-radius:5px;overflow:hidden;">
                    <div style="width:{pb_pct}%;height:100%;background:#00a4ff;border-radius:5px;"></div>
                </div>
                <div style="color:white;font-size:0.95rem;font-weight:600;margin-top:4px">{pb_value}</div>
            </div>
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 12px;">
            <div style="background: rgba(255,255,255,0.05); padding: 8px; border-radius: 6px;">
                <div style="color:#888;font-size:0.6rem">52周最高</div>
                <div style="color:#ff6b6b;font-size:0.85rem;font-weight:600">$430.82</div>
            </div>
            <div style="background: rgba(255,255,255,0.05); padding: 8px; border-radius: 6px;">
                <div style="color:#888;font-size:0.6rem">52周最低</div>
                <div style="color:#00c864;font-size:0.85rem;font-weight:600">$309.45</div>
            </div>
            <div style="background: rgba(255,255,255,0.05); padding: 8px; border-radius: 6px;">
                <div style="color:#888;font-size:0.6rem">目标价</div>
                <div style="color:#ffc800;font-size:0.85rem;font-weight:600">$450.00</div>
            </div>
            <div style="background: rgba(255,255,255,0.05); padding: 8px; border-radius: 6px;">
                <div style="color:#888;font-size:0.6rem">上涨空间</div>
                <div style="color:#00c864;font-size:0.85rem;font-weight:600">+9.1%</div>
            </div>
        </div>
        
        <div style="margin-top: 12px; padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.1); display: flex; align-items: center; gap: 8px;">
            <span style="color:#888;font-size:0.7rem">净利润</span>
            <span style="background: rgba(0,200,100,0.15); color:#00c864; padding: 3px 10px; border-radius: 4px; font-size: 0.8rem; font-weight: 600;">77.3B</span>
        </div>
        
    </div>
</div>
"""

st.html(html)

if 'selected_symbol' in st.session_state:
    st.success(f"已选择股票: {st.session_state.selected_symbol}，可跳转至详情页")

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #555; font-size: 0.8rem; padding: 20px;">
    点击股票代码 MSFT 可跳转
</div>
""", unsafe_allow_html=True)