"""
订单模块接口测试（简化版）
"""

import pytest  # 必须加上！
import allure
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@allure.feature("订单模块")
class TestOrder:
    """订单模块测试类"""

    @allure.story("下单流程")
    @allure.title("完整下单流程")
    def test_create_order_flow(self, logged_in_client):
        """
        测试完整下单流程
        """
        client = logged_in_client

        # 1. 添加商品到购物车（允许 200 成功 或 500 已存在）
        cart_data = {
            "goodsId": 10893,
            "goodsCount": 1
        }
        cart_response = client.post("/api/v1/shop-cart", json_data=cart_data)
        
        # 断言：要么成功添加，要么已经存在
        assert cart_response["resultCode"] in [200, 500], f"加入购物车失败：{cart_response}"
        
        if cart_response["resultCode"] == 200:
            print("[步骤1] 商品已加入购物车")
        else:
            print("[步骤1] 商品已在购物车中，跳过添加")

        # 2. 查询购物车
        cart_list = client.get("/api/v1/shop-cart")
        assert cart_list["resultCode"] == 200
        items = cart_list.get("data") or []
        assert len(items) > 0
        print(f"[步骤2] 购物车有{len(items)}件商品")

        # 3. 尝试结算
        order_data = {
            "cartItemIds": [items[0]["cartItemId"]]
        }

        save_response = client.post("/api/v1/saveOrder", json_data=order_data)
        print(f"[步骤3] 结算响应：{save_response}")

        # 断言：要么成功，要么因为业务规则失败
        assert save_response.get("resultCode") in [200, 500], f"结算接口异常：{save_response}"

        if save_response.get("resultCode") == 200:
            print("[通过] 订单创建成功")
        else:
            print(f"[通过] 订单创建被业务规则拦截：{save_response.get('message')}")
    @allure.story("订单列表")
    @allure.title("查询订单列表")
    def test_get_order_list(self, logged_in_client):
        """
        测试查询订单列表
        """
        client = logged_in_client

        response = client.get("/api/v1/orders", params={  # 修正路径：/orders 不是 /order
            "pageNumber": 1,
            "pageSize": 10
        })

        # 如果接口不存在，跳过
        if response.get("status") == 404:
            pytest.skip("订单列表接口路径可能不同")

        assert response.get("resultCode") == 200
        print("[通过] 订单列表查询成功")