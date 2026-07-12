"""
数据库工具类
用于测试后验证数据库数据，确保接口返回和数据库一致
"""

import pymysql
from config.settings import DB_CONFIG


class DBUtils:
    """
    数据库工具类
    
    使用上下文管理器（with语句），确保连接用完自动关闭
    避免内存泄漏和连接池耗尽
    """
    
    def __init__(self):
        self.conn = None
        self.cursor = None
    
    def __enter__(self):
        """
        上下文管理器入口：建立数据库连接
        
        为什么用上下文管理器？
        企业里数据库连接是稀缺资源，用完必须关闭。
        with 语句能保证即使出异常也会关闭连接。
        """
        self.conn = pymysql.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"],
            charset=DB_CONFIG["charset"],
            cursorclass=pymysql.cursors.DictCursor  # 返回字典格式，方便断言
        )
        self.cursor = self.conn.cursor()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        上下文管理器出口：关闭连接
        
        参数说明：
            exc_type: 异常类型
            exc_val: 异常值
            exc_tb: 异常追踪
        如果有异常，先回滚事务，再关闭连接
        """
        if exc_type:
            self.conn.rollback()  # 出异常时回滚，保证数据一致性
        else:
            self.conn.commit()     # 正常时提交
            
        self.cursor.close()
        self.conn.close()
    
    def query_one(self, sql, params=None):
        """
        查询单条记录
        
        参数:
            sql: SQL语句
            params: 参数元组，防止SQL注入
        """
        self.cursor.execute(sql, params)
        return self.cursor.fetchone()
    
    def query_all(self, sql, params=None):
        """查询多条记录"""
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()
    
    def execute(self, sql, params=None):
        """
        执行增删改操作
        
        返回受影响的行数，用于断言
        """
        result = self.cursor.execute(sql, params)
        self.conn.commit()
        return result
    
    def delete_user_by_login_name(self, login_name):
        """
        清理测试数据：根据用户名删除用户
        
        为什么需要清理？
        测试不能污染生产/测试环境，每次测试完要清理自己产生的数据
        这是企业测试的基本素养
        """
        sql = "DELETE FROM tb_newbee_mall_user WHERE login_name = %s"
        return self.execute(sql, (login_name,))
    
    def delete_cart_by_user_id(self, user_id):
        """清理购物车数据"""
        sql = "DELETE FROM tb_newbee_mall_shopping_cart_item WHERE user_id = %s"
        return self.execute(sql, (user_id,))