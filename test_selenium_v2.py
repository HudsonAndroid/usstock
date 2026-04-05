from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import re
import time

print("=== Testing Selenium with webdriver-manager ===")

# 使用webdriver-manager自动下载和安装正确的WebDriver
service = Service(EdgeChromiumDriverManager().install())

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

try:
    driver = webdriver.Edge(service=service, options=options)
    print("Edge browser started successfully!")
    
    def get_pe_value(index_code):
        url = f"https://danjuanfunds.com/dj-valuation-table-detail/{index_code}"
        driver.get(url)
        time.sleep(3)  # 等待JS渲染
        
        html = driver.page_source
        matches = re.findall(r'<div[^>]*class="value-text"[^>]*>(\d+\.?\d*)</div>', html)
        pe_values = [float(m) for m in matches if 15 <= float(m) <= 50]
        
        return pe_values[0] if pe_values else None
    
    for name, code in [("NDX", "NDX"), ("SP500", "SP500")]:
        pe = get_pe_value(code)
        print(f"{name}: PE = {pe}")
    
    driver.quit()
    print("\n=== Complete ===")
    
except Exception as e:
    print(f"Error: {e}")
