"""
newbee-mall 接口测试配置文件
"""

# 后端API基础地址
BASE_URL = "http://localhost:28019"

# API版本前缀
API_PREFIX = "/api/v1"

# 完整的API基础URL
BASE_API_URL = f"{BASE_URL}{API_PREFIX}"

# 请求头（Content-Type为JSON）
HEADERS = {
    "Content-Type": "application/json"
}

# 数据库配置（用于数据校验）
DB_CONFIG = {
    "host": "localhost",
    "port": 4000,
    "user": "root",
    "password": "123456",  # 改成你的MySQL密码
    "database": "newbee_mall_db_v2",
    "charset": "utf8mb4"
}