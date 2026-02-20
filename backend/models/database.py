"""
数据库模型模块

本模块定义了系统的所有数据库模型，使用SQLAlchemy ORM框架实现。

主要包含以下模型：
- User: 用户表模型，存储用户基本信息、权限配置和个性化偏好设置
- Position: 岗位表模型，存储研发团队不同岗位的信息
- ScriptCategory: 话术分类表模型，存储话术的分类信息，支持层级结构
- Script: 话术表模型，存储高情商沟通话术的核心数据
- UserFavorite: 用户收藏表模型，存储用户收藏的话术记录
- Conversation: 对话记录表模型，存储用户与AI助手的对话历史
- ScriptAdjustment: 话术调整记录表模型，存储用户调整话术的历史记录
- SystemConfig: 系统配置表模型，存储系统的动态配置项

依赖项：
- sqlalchemy: ORM框架，用于数据库操作
- config: 配置模块，用于获取数据库连接配置

函数：
- get_db(): 数据库会话依赖注入函数，用于FastAPI路由中获取数据库会话
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, BigInteger, ForeignKey, Index, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from config import get_settings

settings = get_settings()

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, pool_recycle=3600)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    """用户表模型 - 存储用户基本信息、权限配置和个性化偏好设置"""
    __tablename__ = "users"
    
    # 基础字段
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="用户ID，主键自增")
    username = Column(String(50), unique=True, nullable=False, comment="用户名，登录标识，全局唯一")
    password_hash = Column(String(255), nullable=False, comment="密码哈希值，使用bcrypt加密存储")
    
    # 联系方式
    phone = Column(String(20), comment="手机号，用于找回密码和通知")
    email = Column(String(100), comment="邮箱地址，用于接收通知")
    
    # 用户属性
    role = Column(String(20), nullable=False, default="user", comment="用户角色：user-普通用户，admin-管理员")
    avatar_url = Column(String(255), comment="用户头像URL地址")
    is_active = Column(Boolean, default=True, comment="账户是否激活，True-正常，False-禁用")
    
    # VIP相关
    is_vip = Column(Boolean, default=False, comment="是否VIP会员用户")
    vip_expire_time = Column(DateTime, comment="VIP会员过期时间，NULL表示非会员或未过期")
    
    # 个性化偏好
    tone_preference = Column(String(20), default="温和", comment="话术语气偏好：温和-默认，专业，亲切等")
    length_preference = Column(String(20), default="简洁版", comment="话术长度偏好：简洁版-默认，详细版")
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.now, comment="账户创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="账户信息最后更新时间")
    
    # 索引定义
    __table_args__ = (
        Index('idx_username', 'username'),
        Index('idx_phone', 'phone'),
        Index('idx_role', 'role'),
    )


class Position(Base):
    """岗位表模型 - 存储研发团队不同岗位的信息"""
    __tablename__ = "positions"
    
    # 基础字段
    id = Column(Integer, primary_key=True, autoincrement=True, comment="岗位ID，主键自增")
    name = Column(String(50), nullable=False, comment="岗位名称，如：售前人员、项目经理、产品经理等")
    code = Column(String(20), unique=True, nullable=False, comment="岗位代码，全局唯一，用于程序内部标识")
    description = Column(String(200), comment="岗位描述，说明该岗位的职责范围")
    
    # 显示配置
    sort_order = Column(Integer, default=0, comment="排序字段，数字越小越靠前")
    is_active = Column(Boolean, default=True, comment="是否启用，True-启用，False-停用")
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.now, comment="岗位创建时间")


class ScriptCategory(Base):
    """话术分类表模型 - 存储话术的分类信息，支持层级结构"""
    __tablename__ = "script_categories"
    
    # 基础字段
    id = Column(Integer, primary_key=True, autoincrement=True, comment="分类ID，主键自增")
    name = Column(String(50), nullable=False, comment="分类名称，如：需求沟通、项目推进、Bug处理等")
    code = Column(String(50), unique=True, nullable=False, comment="分类代码，全局唯一，用于程序内部标识")
    
    # 分类层级
    parent_id = Column(Integer, default=0, comment="父分类ID，0表示顶级分类，支持多级分类结构")
    position_id = Column(Integer, comment="关联岗位ID，NULL表示通用分类，非NULL表示该岗位专属分类")
    
    # 描述和显示
    description = Column(String(200), comment="分类描述，说明该分类下话术的应用场景")
    icon = Column(String(100), comment="分类图标，前端展示使用")
    
    # 显示配置
    sort_order = Column(Integer, default=0, comment="排序字段，数字越小越靠前")
    is_active = Column(Boolean, default=True, comment="是否启用，True-启用，False-停用")
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.now, comment="分类创建时间")
    
    # 索引定义
    __table_args__ = (
        Index('idx_position_id', 'position_id'),
        Index('idx_parent_id', 'parent_id'),
    )


class Script(Base):
    """话术表模型 - 存储高情商沟通话术的核心数据"""
    __tablename__ = "scripts"
    
    # 基础字段
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="话术ID，主键自增")
    title = Column(String(100), nullable=False, comment="话术标题，简洁描述话术的应用场景")
    
    # 话术内容
    content = Column(Text, nullable=False, comment="完整话术内容，标准版")
    brief_content = Column(Text, comment="简洁版话术内容，用于快速沟通场景")
    
    # 分类关联
    category_id = Column(Integer, nullable=False, comment="所属分类ID，关联script_categories表")
    position_id = Column(Integer, comment="适用岗位ID，关联positions表，NULL表示通用话术")
    
    # 话术属性
    scene_type = Column(String(50), nullable=False, comment="场景类型，如：需求沟通、项目推进、Bug处理、客户对接等")
    tone = Column(String(20), default="温和", comment="话术语气，如：温和、专业、强硬、活泼、委婉")
    target_audience = Column(String(50), comment="目标对象，如：客户、领导、同事等")
    tags = Column(String(200), comment="标签，多个标签用逗号分隔，用于搜索和筛选")
    
    # 统计数据
    usage_count = Column(Integer, default=0, comment="使用次数，用户查看或使用该话术的次数")
    like_count = Column(Integer, default=0, comment="点赞次数，用户点赞该话术的次数")
    
    # 权限和状态
    is_free = Column(Boolean, default=True, comment="是否免费，True-所有用户可用，False-VIP专属")
    is_active = Column(Boolean, default=True, comment="是否启用，True-启用，False-停用")
    
    # 创建者信息
    created_by = Column(BigInteger, comment="创建者ID，关联users表，NULL表示系统默认话术")
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.now, comment="话术创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="话术最后更新时间")
    
    # 索引定义
    __table_args__ = (
        Index('idx_category_id', 'category_id'),
        Index('idx_position_id', 'position_id'),
        Index('idx_scene_type', 'scene_type'),
    )


class UserFavorite(Base):
    """用户收藏表模型 - 存储用户收藏的话术记录"""
    __tablename__ = "user_favorites"
    
    # 基础字段
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="收藏ID，主键自增")
    user_id = Column(BigInteger, nullable=False, comment="用户ID，关联users表")
    script_id = Column(BigInteger, nullable=False, comment="话术ID，关联scripts表")
    
    # 自定义内容
    custom_content = Column(Text, comment="用户自定义的话术内容，用户可以对收藏的话术进行个性化修改")
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.now, comment="收藏创建时间")
    
    # 索引定义
    __table_args__ = (
        Index('uk_user_script', 'user_id', 'script_id', unique=True),
        Index('idx_user_id', 'user_id'),
        Index('idx_script_id', 'script_id'),
    )


class Conversation(Base):
    """对话记录表模型 - 存储用户与AI助手的对话历史"""
    __tablename__ = "conversations"
    
    # 基础字段
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="对话ID，主键自增")
    user_id = Column(BigInteger, nullable=False, comment="用户ID，关联users表")
    session_id = Column(String(64), nullable=False, comment="会话ID，用于关联同一轮对话中的多条消息")
    
    # 消息内容
    message_type = Column(String(20), nullable=False, comment="消息类型：user-用户消息，assistant-AI回复")
    content = Column(Text, nullable=False, comment="消息内容，用户输入或AI回复的文本")
    
    # AI相关数据
    context_data = Column(JSON, comment="上下文数据，存储AI识别的场景、意图等元数据")
    intent = Column(String(50), comment="意图识别，AI识别出的用户意图，如：search、adjust_tone等")
    referenced_script_id = Column(BigInteger, comment="关联话术ID，AI回复时引用的话术ID")
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.now, comment="消息创建时间")
    
    # 索引定义
    __table_args__ = (
        Index('idx_user_id', 'user_id'),
        Index('idx_session_id', 'session_id'),
        Index('idx_created_at', 'created_at'),
    )


class ScriptAdjustment(Base):
    """话术调整记录表模型 - 存储用户调整话术的历史记录"""
    __tablename__ = "script_adjustments"
    
    # 基础字段
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="调整记录ID，主键自增")
    user_id = Column(BigInteger, nullable=False, comment="用户ID，关联users表")
    script_id = Column(BigInteger, nullable=False, comment="话术ID，关联scripts表")
    
    # 调整内容
    original_content = Column(Text, comment="调整前的话术原始内容")
    adjusted_content = Column(Text, comment="调整后的话术内容")
    
    # 调整参数
    tone = Column(String(20), comment="调整后的语气，如：温和、专业等")
    length_type = Column(String(20), comment="调整后的长度类型，如：简洁版、详细版")
    
    # 用户反馈
    feedback = Column(String(200), comment="用户反馈，记录用户对调整结果的评价或建议")
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.now, comment="调整记录创建时间")
    
    # 索引定义
    __table_args__ = (
        Index('idx_user_id', 'user_id'),
        Index('idx_script_id', 'script_id'),
    )


class SystemConfig(Base):
    """系统配置表模型 - 存储系统的动态配置项"""
    __tablename__ = "system_configs"
    
    # 基础字段
    id = Column(Integer, primary_key=True, autoincrement=True, comment="配置ID，主键自增")
    config_key = Column(String(100), unique=True, nullable=False, comment="配置键，全局唯一，如：max_concurrent_users、ai_model_version等")
    config_value = Column(Text, comment="配置值，存储具体的配置数据，可以是JSON格式")
    description = Column(String(200), comment="配置描述，说明该配置项的用途和取值范围")
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.now, comment="配置创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="配置最后更新时间")


def get_db():
    """
    数据库会话依赖注入函数
    
    这是一个FastAPI的依赖注入函数，用于在路由处理函数中获取数据库会话。
    使用yield语句确保会话在使用完毕后正确关闭，避免连接泄漏。
    
    Yields:
        Session: SQLAlchemy数据库会话对象
        
    Example:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
