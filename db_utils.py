import sqlite3
from pathlib import Path

class DatabaseManager:
    def __init__(self):
        db_path = Path("user_data.db")
        self.conn = sqlite3.connect(str(db_path))
        self.cursor = self.conn.cursor()
        self.init_tables()
        
    def init_tables(self):
        """初始化数据库表"""
        # 创建guest表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS guest (
                name TEXT,
                id TEXT PRIMARY KEY,
                password TEXT,
                admic TEXT,
                filename TEXT,
                data BLOB
            )
        ''')
        
        # 创建admin表 
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS admin (
                name TEXT,
                id TEXT PRIMARY KEY,
                password TEXT,
                admic TEXT
            )
        ''')
        self.conn.commit()
        
    def query(self, sql, params=()):
        """执行查询"""
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()
        
    def exec(self, sql, params=()):
        """执行更新操作"""
        self.cursor.execute(sql, params)
        self.conn.commit()
        
    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close() 