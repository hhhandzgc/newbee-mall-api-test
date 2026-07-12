"""
商品模块接口测试（修复版）
"""

import pytest
import allure
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@allure.feature("商品模块")
class TestGoods:
    """商品模块测试类"""

    @allure.story("搜索商品")
    @allure.title("关键词搜索商品")
    def test_search_goods(self, logged_in_client):
        """
        测试搜索商品
        """
        client = logged_in_client

        keyword = "手机"

        # 修正路径：加上 /api/v1 前缀
        response = client.get("/api/v1/search", params={
            "keyword": keyword,
            "pageNumber": 1,
            "pageSize": 10
        })

        # 断言
        assert response["resultCode"] == 200, f"搜索接口失败：{response}"
        
        # 安全获取商品列表
        data = response.get("data", {})
        if isinstance(data, dict):
            goods_list = data.get("list", [])
        else:
            goods_list = data or []

        assert len(goods_list) > 0, f"搜索'{keyword}'未返回任何商品"

        first_goods = goods_list[0]
        assert "goodsId" in first_goods
        assert "goodsName" in first_goods
        print(f"[通过] 搜索'{keyword}'成功，返回{len(goods_list)}件商品")

    @allure.story("商品详情")
    @allure.title("获取商品详情")
    def test_get_goods_detail(self, logged_in_client):
        """
        测试获取商品详情
        """
        client = logged_in_client

        goods_id = 10893

        # 修正路径：加上 /api/v1 前缀
        response = client.get(f"/api/v1/goods/detail/{goods_id}")

        assert response["resultCode"] == 200, f"商品详情接口失败：{response}"

        goods = response.get("data", {})
        assert goods.get("goodsId") == goods_id or goods.get("goods_id") == goods_id
        assert goods.get("goodsName") or goods.get("goods_name")
        print(f"[通过] 商品详情查询成功：{goods.get('goodsName') or goods.get('goods_name')}")

    @allure.story("商品分类")
    @allure.title("获取商品分类列表")
    def test_get_category_list(self, logged_in_client):
        """
        测试获取商品分类列表
        """
        client = logged_in_client

        # 修正路径：加上 /api/v1 前缀
        response = client.get("/api/v1/categories")

        assert response["resultCode"] == 200, f"分类接口失败：{response}"

        categories = response.get("data", [])
        if not isinstance(categories, list):
            categories = categories.get("list", []) if isinstance(categories, dict) else []

        assert len(categories) > 0, "商品分类列表为空"
        print(f"[通过] 商品分类查询成功，共{len(categories)}个分类")

    @allure.story("搜索无结果")
    @allure.title("搜索不存在的商品")
    def test_search_no_result(self, logged_in_client):
        """
        测试搜索无结果
        """
        client = logged_in_client

        keyword = "abcdefg12345不存在"

        # 修正路径：加上 /api/v1 前缀
        response = client.get("/api/v1/search", params={
            "keyword": keyword,
            "pageNumber": 1,
            "pageSize": 10
        })

        assert response.get("resultCode") == 200
        data = response.get("data", {})
        goods_list = data.get("list", []) if isinstance(data, dict) else []
        assert len(goods_list) == 0
        print("[通过] 无结果搜索处理正确")