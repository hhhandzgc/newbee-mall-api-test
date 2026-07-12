"""
用户模块接口测试
"""

import allure
import pytest
import time
import hashlib
from utils.http_client import HttpClient
from utils.db_utils import DBUtils
from utils.logger import logger


def md5_encode(text):
    """MD5 加密"""
    return hashlib.md5(text.encode('utf-8')).hexdigest()


@allure.feature("用户模块")
@allure.severity(allure.severity_level.CRITICAL)
class TestUser:
    """用户相关接口测试"""

    @allure.story("用户注册")
    @allure.title("注册成功-正常场景")
    @allure.description("验证用户注册接口在正常参数下的返回结果和数据库写入")
    def test_register_success(self, db):
        client = HttpClient()
        # 使用时间戳生成唯一用户名，避免重复运行失败
        unique_name = f"138{int(time.time()) % 100000000:08d}"
        
        payload = {
            "loginName": unique_name,
            "password": "123456"
        }
        logger.info(f"【用例开始】test_register_success，手机号: {unique_name}")
        
        with allure.step("步骤1：调用注册接口"):
            response = client.post("/api/v1/user/register", json_data=payload)
            allure.attach(
                body=str(response),
                name="接口响应",
                attachment_type=allure.attachment_type.JSON
            )
        
        with allure.step("步骤2：断言响应结果"):
            assert response["resultCode"] == 200
        
        with allure.step("步骤3：数据库校验"):
            sql = f"SELECT * FROM tb_newbee_mall_user WHERE login_name = '{unique_name}'"
            result = db.query_all(sql)
            allure.attach(
                body=str(result),
                name="数据库查询结果",
                attachment_type=allure.attachment_type.TEXT
            )
            assert len(result) == 1
        
        logger.info("【用例通过】test_register_success")

    @allure.story("用户注册")
    @allure.title("注册失败-用户名已存在")
    @allure.severity(allure.severity_level.NORMAL)
    def test_register_duplicate(self):
        client = HttpClient()
        unique_name = f"138{int(time.time()) % 100000000:08d}"
        payload = {
            "loginName": unique_name,
            "password": "123456"
        }
        # 第一次注册成功
        client.post("/api/v1/user/register", json_data=payload)
        # 第二次注册同样的手机号，应该失败
        response = client.post("/api/v1/user/register", json_data=payload)
        assert response["resultCode"] == 500
        # 错误提示可能是"已存在"或"请输入正确的手机号"等
        assert any(keyword in response["message"] for keyword in ["已存在", "手机号", "重复"])

    @allure.story("用户登录")
    @allure.title("登录成功")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_success(self):
        client = HttpClient()
        # 先确保用户存在（手机号格式）
        login_name = "13800138001"
        password = "123456"
        
        client.post("/api/v1/user/register", json_data={
            "loginName": login_name,
            "password": password
        })
        
        # 登录用 passwordMd5
        response = client.post("/api/v1/user/login", json_data={
            "loginName": login_name,
            "passwordMd5": md5_encode(password)
        })
        assert response["resultCode"] == 200
        assert "data" in response
        token = response["data"]
        allure.attach(body=token, name="登录Token", attachment_type=allure.attachment_type.TEXT)

    @allure.story("用户登录")
    @allure.title("登录失败-密码错误")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_wrong_password(self):
        client = HttpClient()
        # 先确保用户存在
        login_name = "13800138001"
        password = "123456"

        client.post("/api/v1/user/register", json_data={
            "loginName": login_name,
            "password": password
        })

        # 用错误的密码登录
        response = client.post("/api/v1/user/login", json_data={
            "loginName": login_name,
            "passwordMd5": md5_encode("wrong_password")
        })
        assert response["resultCode"] == 500

    # ===== 重试测试用例 =====
        
    