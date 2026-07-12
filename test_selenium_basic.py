from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

# 使用本地 ChromeDriver
driver_path = r"C:\Users\ydn26\Desktop\python_test\newbee_mall_api_test\drivers\chromedriver.exe"
service = Service(driver_path)

driver = webdriver.Chrome(service=service)

# 打开 newbee-mall 前端
driver.get("http://localhost:8080")
print(f"页面标题: {driver.title}")

time.sleep(3)
driver.quit()
print("测试完成")