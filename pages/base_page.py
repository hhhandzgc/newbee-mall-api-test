"""
BasePage 基类
封装所有 Page 类的通用方法
"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils.logger import logger
import allure


class BasePage:
    """
    Page 基类
    
    所有 Page 类都继承此类，复用通用方法
    """
    
    # 默认超时时间（秒）
    DEFAULT_TIMEOUT = 10
    
    def __init__(self, driver: WebDriver):
        """
        初始化
        
        参数:
            driver: WebDriver 实例
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, self.DEFAULT_TIMEOUT)
        logger.info(f"【Page初始化】{self.__class__.__name__}")
    
    # ==================== 元素定位方法 ====================
    
    def find_element(self, locator: tuple) -> WebElement:
        """
        查找单个元素（显式等待）
        
        参数:
            locator: 定位器元组，如 (By.ID, "username")
        返回:
            WebElement 元素对象
        """
        by, value = locator
        logger.info(f"【查找元素】{by} = {value}")
        
        try:
            element = self.wait.until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            logger.error(f"【查找失败】元素未找到：{by} = {value}")
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="查找元素失败截图",
                attachment_type=allure.attachment_type.PNG
            )
            raise
    
    def find_elements(self, locator: tuple) -> list:
        """
        查找多个元素
        """
        by, value = locator
        logger.info(f"【查找元素】{by} = {value} (多个)")
        return self.wait.until(
            EC.presence_of_all_elements_located(locator)
        )
    
    # ==================== 元素操作方法 ====================
    
    def click(self, locator: tuple):
        """
        点击元素
        """
        element = self.find_element(locator)
        logger.info(f"【点击】{locator}")
        element.click()
    
    def send_keys(self, locator: tuple, text: str):
        """
        输入文本
        """
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
        logger.info(f"【输入】{locator} -> {text}")
    
    def get_text(self, locator: tuple) -> str:
        """
        获取元素文本
        """
        element = self.find_element(locator)
        text = element.text
        logger.info(f"【获取文本】{locator} -> {text}")
        return text
    
    def get_attribute(self, locator: tuple, attribute: str) -> str:
        """
        获取元素属性
        """
        element = self.find_element(locator)
        value = element.get_attribute(attribute)
        logger.info(f"【获取属性】{locator}.{attribute} = {value}")
        return value
    
    # ==================== 页面操作方法 ====================
    
    def open_url(self, url: str):
        """
        打开 URL
        """
        logger.info(f"【打开页面】{url}")
        self.driver.get(url)
    
    def get_title(self) -> str:
        """
        获取页面标题
        """
        title = self.driver.title
        logger.info(f"【页面标题】{title}")
        return title
    
    def get_current_url(self) -> str:
        """
        获取当前 URL
        """
        url = self.driver.current_url
        logger.info(f"【当前URL】{url}")
        return url
    
    def take_screenshot(self, name: str = "screenshot"):
        """
        截图并附加到 Allure 报告
        """
        screenshot = self.driver.get_screenshot_as_png()
        allure.attach(
            screenshot,
            name=name,
            attachment_type=allure.attachment_type.PNG
        )
        logger.info(f"【截图】{name}")
    
    # ==================== 等待方法 ====================
    
    def wait_for_element_visible(self, locator: tuple, timeout: int = None):
        """
        等待元素可见
        """
        wait_time = timeout or self.DEFAULT_TIMEOUT
        by, value = locator
        logger.info(f"【等待可见】{by} = {value}，超时{wait_time}秒")
        return WebDriverWait(self.driver, wait_time).until(
            EC.visibility_of_element_located(locator)
        )
    
    def wait_for_element_clickable(self, locator: tuple, timeout: int = None):
        """
        等待元素可点击
        """
        wait_time = timeout or self.DEFAULT_TIMEOUT
        by, value = locator
        logger.info(f"【等待可点击】{by} = {value}，超时{wait_time}秒")
        return WebDriverWait(self.driver, wait_time).until(
            EC.element_to_be_clickable(locator)
        )