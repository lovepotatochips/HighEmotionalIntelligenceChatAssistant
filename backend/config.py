"""
配置管理模块

使用 Pydantic Settings 进行应用配置管理，支持从环境变量和 .env 文件读取配置。
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import List, Union
import os


class Settings(BaseSettings):
    """
    应用配置类

    继承自 BaseSettings，自动从环境变量和 .env 文件加载配置。
    使用 lru_cache 缓存配置实例，避免重复读取。
    """
    
    # 应用基础配置
    APP_NAME: str = "高情商聊天助手"  # 应用名称
    APP_VERSION: str = "1.0.0"  # 应用版本号
    
    # JWT 认证配置
    SECRET_KEY: str = "your-secret-key-change-in-production"  # JWT 密钥，生产环境必须修改
    ALGORITHM: str = "HS256"  # JWT 算法
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 访问令牌过期时间（分钟），默认7天
    
    # 数据库配置
    DATABASE_TYPE: str = "sqlite"  # 数据库类型：sqlite 或 mysql
    DATABASE_HOST: str = "localhost"  # MySQL 数据库主机地址
    DATABASE_PORT: int = 3306  # MySQL 数据库端口
    DATABASE_USER: str = "root"  # MySQL 数据库用户名
    DATABASE_PASSWORD: str = "password"  # MySQL 数据库密码
    DATABASE_NAME: str = "vibe_chat"  # MySQL 数据库名称
    DATABASE_PATH: str = "vibe_chat.db"  # SQLite 数据库文件路径
    
    # CORS 跨域配置
    CORS_ORIGINS: Union[str, List[str]] = ["http://localhost:5173", "http://localhost:8080", "http://127.0.0.1:5173"]  # 允许跨域的源列表
    
    # AI 聊天配置
    MAX_CONTEXT_TURNS: int = 10  # 最大上下文轮次
    RESPONSE_TIMEOUT: int = 2  # 响应超时时间（秒）
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        env_prefix=""
    )
    
    @property
    def DATABASE_URL(self) -> str:
        """
        生成数据库连接 URL
        
        根据 DATABASE_TYPE 返回对应类型的数据库连接 URL：
        - sqlite: 返回 SQLite 文件路径连接字符串
        - mysql: 返回 MySQL 连接字符串
        """
        if self.DATABASE_TYPE == "sqlite":
            db_path = os.path.abspath(self.DATABASE_PATH)
            return f"sqlite:///{db_path}"
        return f"mysql+pymysql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}?charset=utf8mb4"
    
    def get_cors_origins(self) -> List[str]:
        """
        获取 CORS 允许的源列表
        
        支持字符串格式（逗号分隔）和列表格式
        """
        if isinstance(self.CORS_ORIGINS, str):
            return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
        return self.CORS_ORIGINS


@lru_cache()
def get_settings():
    """
    获取配置实例（带缓存）
    
    使用 lru_cache 装饰器缓存配置实例，
    避免每次调用都重新创建 Settings 对象。
    
    Returns:
        Settings: 配置实例
    """
    return Settings()
