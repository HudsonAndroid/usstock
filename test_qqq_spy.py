import yfinance as yf

qqq = yf.Ticker('QQQ')
qqq_info = qqq.info
print('QQQ trailingPE:', qqq_info.get('trailingPE'))
print('QQQ forwardPE:', qqq_info.get('forwardPE'))
print('QQQ regularMarketPE:', qqq_info.get('regularMarketPE'))

spy = yf.Ticker('SPY')
spy_info = spy.info
print('SPY trailingPE:', spy_info.get('trailingPE'))
print('SPY forwardPE:', spy_info.get('forwardPE'))
print('SPY regularMarketPE:', spy_info.get('regularMarketPE'))
