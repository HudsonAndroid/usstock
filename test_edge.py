from selenium import webdriver
from selenium.webdriver.edge.options import Options

print("Testing Edge browser connection...")

options = Options()
options.add_argument("--headless")
options.binary_location = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

try:
    driver = webdriver.Edge(options=options)
    print("Edge browser started successfully!")
    driver.get("https://www.baidu.com")
    print(f"Page title: {driver.title}")
    driver.quit()
    print("Test complete!")
except Exception as e:
    print(f"Error: {e}")
