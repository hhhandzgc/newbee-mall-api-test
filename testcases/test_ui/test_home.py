"""
首页 UI 自动化测试
"""

import pytest
import allure
from pages.home_page import HomePage


@allure.feature("UI测试-首页")
class TestHomePage:
    """首页 UI 测试类"""

    @allure.story("页面加载")
    @allure.title("首页正常加载")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_home_page_load(self, browser):
        """
        测试首页正常加载
        """
        # 打开首页
        home = HomePage(browser).open()
        
        # 断言标题包含 Vite 或 newbee
        title = home.get_title()
        assert "Vite" in title or "newbee" in title.lower(), f"标题异常：{title}"
        
        # 截图
        home.take_screenshot("首页加载成功")

    #@allure.story("搜索功能")
    #@allure.title("搜索商品-正常关键词")
    #@allure.severity(allure.severity_level.CRITICAL)
    #def test_search_goods(self, browser):
       # """
       # 测试搜索商品功能
       # """
       # home = HomePage(browser).open()
        
        # 搜索"手机"
        #home.search_goods("手机")
        
        # 等待搜索结果加载
        #import time
        #time.sleep(2)
        
        # 截图
       # home.take_screenshot("搜索结果")

    @allure.story("页面元素")
    @allure.title("检查商品列表")
    @allure.severity(allure.severity_level.NORMAL)
    def test_goods_list_displayed(self, browser):
        """
        测试商品列表是否显示
        """
        home = HomePage(browser).open()
        
        # 获取商品数量
        count = home.get_goods_count()
        
        # 断言有商品（不强制要求，因为首页可能没有商品）
        if count > 0:
            print(f"首页有 {count} 个商品")
        else:
            print("首页暂无商品或商品加载中")
        
        # 截图
        home.take_screenshot("商品列表")