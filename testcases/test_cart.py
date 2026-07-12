"""
购物车模块接口测试（修复版）
"""

import pytest
import allure
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@allure.feature("购物车模块")  # ← 类上面加
@allure.severity(allure.severity_level.CRITICAL)  # ← 类上面加

class TestCart:
    """购物车模块测试类"""

    @allure.story("添加购物车")
    @allure.title("添加商品到购物车")
    def test_add_to_cart(self, logged_in_client, db):
        """
        测试添加商品到购物车
        """
        client = logged_in_client

        # ===== 测试前清理购物车，确保测试独立性 =====
        login_name = "13800138000"
        user_sql = "SELECT user_id FROM tb_newbee_mall_user WHERE login_name = %s"
        user = db.query_one(user_sql, (login_name,))
        if user:
            db.delete_cart_by_user_id(user["user_id"])
            print("[清理] 已清空用户购物车")

        data = {
            "goodsId": 10893,
            "goodsCount": 1
        }

        # 调用加入购物车接口
        response = client.post("/api/v1/shop-cart", json_data=data)

        # 断言接口调用成功
        assert response["resultCode"] == 200, f"加入购物车失败：{response.get('message')}"
        print("[步骤1] 加入购物车接口调用成功")

        # 用 GET 查询购物车验证数据真的写入了
        cart_response = client.get("/api/v1/shop-cart")
        assert cart_response["resultCode"] == 200

        cart_items = cart_response.get("data") or []
        assert len(cart_items) > 0, "购物车查询结果为空"

        # 验证商品信息
        first_item = cart_items[0]
        assert first_item["goodsId"] == 10893
        print(f"[通过] 商品添加成功，购物车ID：{first_item['cartItemId']}")

    @allure.story("查询购物车")
    @allure.title("获取购物车列表")
    def test_get_cart_list(self, logged_in_client, db):
        """
        测试获取购物车列表
        """
        client = logged_in_client

        # 先确保购物车有数据（添加或已存在）
        add_data = {
            "goodsId": 10893,
            "goodsCount": 1
        }
        add_response = client.post("/api/v1/shop-cart", json_data=add_data)
        # 允许 200（成功）或 500（已存在）
        assert add_response["resultCode"] in [200, 500], f"添加购物车失败：{add_response}"

        # 查询购物车
        response = client.get("/api/v1/shop-cart")

        assert response["resultCode"] == 200

        cart_items = response.get("data") or []
        assert len(cart_items) > 0

        print(f"[通过] 购物车查询成功，共{len(cart_items)}件商品")

    @allure.story("添加购物车并数据库校验")
    @allure.title("添加购物车并验证数据库")
    def test_add_cart_and_verify_db(self, logged_in_client, db):
        """
        测试添加购物车并验证数据库
        """
        client = logged_in_client

        # ===== 测试前清理购物车，确保测试独立性 =====
        login_name = "13800138000"
        user_sql = "SELECT user_id FROM tb_newbee_mall_user WHERE login_name = %s"
        user = db.query_one(user_sql, (login_name,))
        if user:
            db.delete_cart_by_user_id(user["user_id"])
            print("[清理] 已清空用户购物车")

        # 添加商品
        data = {
            "goodsId": 10893,
            "goodsCount": 2
        }
        response = client.post("/api/v1/shop-cart", json_data=data)
        assert response["resultCode"] == 200, f"添加购物车失败：{response}"

        # 查询用户ID
        user = db.query_one(user_sql, (login_name,))
        assert user is not None, "数据库中未找到用户"
        user_id = user["user_id"]

        # 查询购物车数据
        cart_sql = """
            SELECT * FROM tb_newbee_mall_shopping_cart_item 
            WHERE user_id = %s AND goods_id = %s
        """
        cart_item = db.query_one(cart_sql, (user_id, 10893))

        assert cart_item is not None, "数据库中未找到购物车记录"
        assert cart_item["goods_count"] == 2
        print(f"[通过] 数据库校验成功：购物车已写入，数量={cart_item['goods_count']}")

        # 清理购物车数据
        db.delete_cart_by_user_id(user_id)