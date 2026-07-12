"""
首页 Page 类
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import logger
import allure


class HomePage(BasePage):
    """newbee-mall 首页"""
    
    # ==================== 元素定位器（根据实际页面结构）====================
    
    # 搜索框
    SEARCH_INPUT = (By.CSS_SELECTOR, ".header-search input")
    
    # 搜索按钮（在搜索框旁边）
    SEARCH_BUTTON = (By.CSS_SELECTOR, ".header-search button")
    
    # 商品列表
    GOODS_ITEMS = (By.CSS_SELECTOR, ".good")
    
    # 商品名称（根据实际结构调整）
    GOODS_NAME = (By.CSS_SELECTOR, ".good-name")
    
    # 登录按钮
    LOGIN_BUTTON = (By.CSS_SELECTOR, ".login")
    
    # 分类列表
    CATEGORY_LIST = (By.CSS_SELECTOR, ".category-list")
    
    # 导航栏
    NAV_BAR = (By.CSS_SELECTOR, ".nav-bar")
    
    # ==================== URL ====================
    
    URL = "http://localhost:8080"
    
    # ==================== 业务方法 ====================
    
    @allure.step("打开首页")
    def open(self):
        """打开首页"""
        self.open_url(self.URL)
        import time
        time.sleep(3)
        logger.info("【首页】已打开")
        return self
    
    @allure.step("搜索商品：{keyword}")
    def search_goods(self, keyword: str):
        """
        搜索商品
        """
        self.send_keys(self.SEARCH_INPUT, keyword)
        # 如果有搜索按钮就点击，否则按回车
        try:
            self.click(self.SEARCH_BUTTON)
        except Exception:
            from selenium.webdriver.common.keys import Keys
            self.find_element(self.SEARCH_INPUT).send_keys(Keys.ENTER)
        logger.info(f"【首页】搜索商品：{keyword}")
        return self
    
    @allure.step("获取商品数量")
    def get_goods_count(self) -> int:
        """
        获取当前页面商品数量
        """
        try:
            items = self.find_elements(self.GOODS_ITEMS)
            count = len(items)
            logger.info(f"【首页】商品数量：{count}")
            return count
        except Exception:
            logger.warning("【首页】未找到商品元素")
            return 0
    
    @allure.step("点击登录按钮")
    def click_login(self):
        """点击登录按钮"""
        self.click(self.LOGIN_BUTTON)
        logger.info("【首页】点击登录")
        return self
    
    @allure.step("检查分类列表是否显示")
    def is_category_list_displayed(self) -> bool:
        """
        检查分类列表是否显示
        """
        try:
            nav = self.find_element(self.CATEGORY_LIST)
            displayed = nav.is_displayed()
            logger.info(f"【首页】分类列表显示状态：{displayed}")
            return displayed
        except Exception:
            logger.warning("【首页】分类列表未找到")
            return False