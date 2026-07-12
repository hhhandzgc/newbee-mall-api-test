"""
conftest.py
Pytest 全局配置和共享 fixtures
"""

import pytest
import allure
import os
import hashlib
from datetime import datetime
from utils.db_utils import DBUtils
from utils.http_client import HttpClient
from utils.logger import logger

# ==================== 数据库 Fixture ====================

@pytest.fixture(scope="function")
def db():
    """
    数据库连接 fixture
    DBUtils 是上下文管理器，用 with 语句自动管理连接
    """
    with DBUtils() as db_utils:
        yield db_utils
    # with 语句退出时会自动调用 __exit__ 关闭连接


# ==================== API 测试 Fixtures ====================

def md5_encode(text):
    """MD5 加密"""
    return hashlib.md5(text.encode('utf-8')).hexdigest()


@pytest.fixture(scope="session")
def logged_in_client():
    """
    返回已登录的 HttpClient 实例
    购物车、订单等需要先登录的接口使用此 fixture
    """
    client = HttpClient()
    
    # 使用手机号格式作为用户名（符合后端校验）
    login_name = "13800138000"
    password = "123456"
    password_md5 = md5_encode(password)
    
    # 先注册（如果已存在会失败，忽略）
    register_payload = {
        "loginName": login_name,
        "password": password
    }
    try:
        client.post("/api/v1/user/register", json_data=register_payload)
    except Exception:
        pass
    
    # 登录获取 token（用 passwordMd5）
    login_payload = {
        "loginName": login_name,
        "passwordMd5": password_md5
    }
    result = client.post("/api/v1/user/login", json_data=login_payload)
    
    if result.get("resultCode") == 200:
        token = result["data"]
        client.set_token(token)
        return client
    else:
        pytest.fail(f"登录失败，无法获取 token: {result}")


# ==================== UI 测试 Fixture ====================

@pytest.fixture(scope="function")
def browser():
    """
    UI 测试浏览器 fixture
    
    每个测试函数结束后自动关闭浏览器
    """
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    
    # Chrome 配置
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # 无头模式（后台运行）
    chrome_options.add_argument("--window-size=1920,1080")  # 窗口大小
    chrome_options.add_argument("--no-sandbox")
    
    # ChromeDriver 路径
    driver_path = r"C:\Users\ydn26\Desktop\python_test\newbee_mall_api_test\drivers\chromedriver.exe"
    service = Service(driver_path)
    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(5)  # 隐式等待 5 秒
    
    yield driver
    
    # 测试结束后关闭浏览器
    driver.quit()
    logger.info("【浏览器】已关闭")


# ==================== Allure 日志附件 Fixture ====================

@pytest.fixture(autouse=True)
def attach_log_to_allure():
    """每个测试用例结束后，将当天日志附加到 Allure 报告"""
    yield
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    log_file = os.path.join(log_dir, f'{datetime.now().strftime("%Y-%m-%d")}.log')
    
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as f:
            log_content = f.read()[-5000:]
        allure.attach(
            log_content, 
            name="测试日志", 
            attachment_type=allure.attachment_type.TEXT
        )