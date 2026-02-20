from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from config import get_settings
from models.database import get_db, User

settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码是否正确
    
    Args:
        plain_password: 用户输入的明文密码
        hashed_password: 数据库中存储的密码哈希值
    
    Returns:
        bool: 密码是否匹配，True-匹配，False-不匹配
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    对密码进行哈希加密
    
    Args:
        password: 用户输入的明文密码
    
    Returns:
        str: 加密后的密码哈希值
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    创建JWT访问令牌
    
    Args:
        data: 要编码到令牌中的数据，通常包含用户名
        expires_delta: 令牌过期时间增量，None则使用默认过期时间
    
    Returns:
        str: 编码后的JWT令牌字符串
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[str]:
    """
    验证并解析JWT令牌
    
    Args:
        token: JWT令牌字符串
    
    Returns:
        Optional[str]: 解析出的用户名，验证失败返回None
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    从JWT令牌中获取当前用户
    
    这是一个FastAPI依赖函数，用于在路由中自动获取当前登录用户。
    
    Args:
        token: JWT令牌，从Authorization头部自动提取
        db: 数据库会话
    
    Returns:
        User: 当前用户对象
    
    Raises:
        HTTPException: 令牌无效或用户不存在时抛出401错误
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的认证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    username = verify_token(token)
    if username is None:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    获取当前激活的用户
    
    这是一个FastAPI依赖函数，依赖于get_current_user，
    并额外检查用户是否处于激活状态。
    
    Args:
        current_user: 当前用户对象，从get_current_user依赖获取
    
    Returns:
        User: 当前激活的用户对象
    
    Raises:
        HTTPException: 用户被禁用时抛出400错误
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="用户已被禁用")
    return current_user
