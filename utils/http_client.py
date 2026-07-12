import requests
import json
from utils.logger import logger
import hashlib

def md5_encode(text):
    """MD5 加密，与前端保持一致"""
    return hashlib.md5(text.encode('utf-8')).hexdigest()

# ========== 常量定义（必须保留）==========
BASE_API_URL = "http://localhost:28019"

HEADERS = {
    "Content-Type": "application/json"
}


class HttpClient:
    """HTTP客户端封装类"""

    def __init__(self):
        self.session = requests.Session()
        self.base_url = BASE_API_URL
        self.headers = HEADERS.copy()

    def get(self, path, params=None, **kwargs):
        url = f"{self.base_url}{path}"
        logger.info(f"[GET] {url}")
        if params:
            logger.info(f"Params: {params}")
        
        response = self.session.get(url, params=params, headers=self.headers, **kwargs)
        return self._handle_response(response)

    def post(self, path, data=None, json_data=None, **kwargs):
        url = f"{self.base_url}{path}"
        logger.info(f"[POST] {url}")
        if json_data:
            logger.info(f"Body: {json.dumps(json_data, ensure_ascii=False)}")
        
        response = self.session.post(
            url,
            data=data,
            json=json_data,
            headers=self.headers,
            **kwargs
        )
        return self._handle_response(response)

    def put(self, path, data=None, json_data=None, **kwargs):
        url = f"{self.base_url}{path}"
        logger.info(f"[PUT] {url}")
        if json_data:
            logger.info(f"Body: {json.dumps(json_data, ensure_ascii=False)}")
        
        response = self.session.put(
            url,
            data=data,
            json=json_data,
            headers=self.headers,
            **kwargs
        )
        return self._handle_response(response)

    def delete(self, path, **kwargs):
        url = f"{self.base_url}{path}"
        logger.info(f"[DELETE] {url}")
        
        response = self.session.delete(url, headers=self.headers, **kwargs)
        return self._handle_response(response)

    def _handle_response(self, response):
        logger.info(f"Status: {response.status_code}")
        try:
            result = response.json()
            result_str = json.dumps(result, ensure_ascii=False, indent=2)
            logger.info(f"Response: {result_str[:500]}")
            return result
        except Exception as e:
            logger.error(f"Response parse error: {response.text}")
            return {"error": str(e), "text": response.text}

    def set_token(self, token):
        """设置认证token"""
        self.headers["token"] = token
        logger.info(f"[Token已设置] {token[:20]}...")