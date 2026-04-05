from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

print("=== Testing Selenium with Edge Browser ===")

# 配置Edge无头浏览器
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.binary_location = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

driver = webdriver.Edge(options=options)

def get_pe_value(index_code):
    """使用Selenium获取蛋卷基金PE值"""
    url = f"https://danjuanfunds.com/dj-valuation-table-detail/{index_code}"
    
    try:
        driver.get(url)
        
        # 等待页面加载完成
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "dj-valuation-table-detail"))
        )
        
        # 获取页面渲染后的HTML
        html = driver.page_source
        
        # 使用正则提取 value-text 中的数字
        matches = re.findall(r'<div[^>]*class="value-text"[^>]*>(\d+\.?\d*)</div>', html)
        
        # 过滤合理范围的PE值 (15-50)
        pe_values = [float(m) for m in matches if 15 <= float(m) <= 50]
        
        if pe_values:
            return pe_values[0]
        
        return None
        
    except Exception as e:
        print(f"Error getting {index_code}: {e}")
        return None

# 测试
for name, code in [("NDX", "NDX"), ("SP500", "SP500")]:
    pe = get_pe_value(code)
    print(f"{name}: PE = {pe}")

driver.quit()
print("\n=== Complete ===")
