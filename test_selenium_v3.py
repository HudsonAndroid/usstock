from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
import re
import time

print("=== Testing Selenium with Edge ===")

# 尝试使用Edge的内置驱动支持
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# 使用selenium-manager自动处理driver
try:
    driver = webdriver.Edge(options=options)
    print("Edge started!")
    
    url = "https://danjuanfunds.com/dj-valuation-table-detail/SP500"
    driver.get(url)
    time.sleep(3)
    
    html = driver.page_source
    matches = re.findall(r'<div[^>]*class="value-text"[^>]*>(\d+\.?\d*)</div>', html)
    pe_values = [float(m) for m in matches if 15 <= float(m) <= 50]
    
    print(f"Found values: {matches}")
    print(f"PE candidates: {pe_values}")
    
    driver.quit()
    print("\n=== Complete ===")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
