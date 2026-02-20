# 导入FastAPI相关模块
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
# 导入数据库会话管理
from sqlalchemy.orm import Session
# 导入时间相关模块
from datetime import timedelta
# 导入数据库模型和工具函数
from models.database import get_db, User
from models.schemas import UserCreate, UserResponse, Token
# 导入认证相关工具函数
from utils.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_active_user
)
# 导入配置
from config import get_settings

# 获取应用配置
settings = get_settings()
# 创建认证路由器，设置前缀和标签
router = APIRouter(prefix="/api/auth", tags=["认证"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    用户注册接口
    
    Args:
        user: 用户创建信息，包含用户名、密码等
        db: 数据库会话
    
    Returns:
        UserResponse: 创建成功的用户信息
    
    Raises:
        HTTPException: 用户名或手机号已存在、或其他注册错误
    """
    try:
        # 调试日志：输出注册信息
        print(f"Registering user: {user.username}")
        print(f"User data: {user}")
        
        # 检查用户名是否已存在
        db_user = db.query(User).filter(User.username == user.username).first()
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已存在"
            )
        
        # 检查手机号是否已被注册
        if user.phone:
            phone_user = db.query(User).filter(User.phone == user.phone).first()
            if phone_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="手机号已被注册"
                )
        
        # 对密码进行哈希加密
        hashed_password = get_password_hash(user.password)
        print(f"Password hashed successfully")
        
        # 创建用户对象
        db_user = User(
            username=user.username,
            password_hash=hashed_password,
            phone=user.phone,
            email=user.email,
            role=user.role,
            avatar_url=user.avatar_url,
            tone_preference=user.tone_preference,
            length_preference=user.length_preference
        )
        
        # 保存到数据库
        print(f"Creating user object: {db_user}")
        db.add(db_user)
        print(f"User added to session")
        db.commit()
        print(f"User committed to database")
        db.refresh(db_user)
        print(f"User refreshed: {db_user.id}")
        
        return db_user
    except HTTPException:
        raise
    except Exception as e:
        # 错误处理和日志记录
        print(f"Registration error: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"注册失败: {str(e)}"
        )


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    用户登录接口
    
    Args:
        form_data: OAuth2密码请求表单，包含用户名和密码
        db: 数据库会话
    
    Returns:
        Token: 包含访问令牌和用户信息的响应
    
    Raises:
        HTTPException: 用户名或密码错误、用户已被禁用
    """
    # 根据用户名查询用户
    user = db.query(User).filter(User.username == form_data.username).first()
    
    # 验证用户是否存在以及密码是否正确
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 检查用户是否处于激活状态
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户已被禁用"
        )
    
    # 设置访问令牌过期时间
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # 创建访问令牌
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    user_response = UserResponse.model_validate(user)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_response
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """
    获取当前登录用户信息接口
    
    Args:
        current_user: 当前激活的用户（通过JWT令牌自动获取）
    
    Returns:
        UserResponse: 当前用户信息
    """
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_update: dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    更新当前用户信息接口
    
    Args:
        user_update: 需要更新的用户信息字典
        current_user: 当前激活的用户（通过JWT令牌自动获取）
        db: 数据库会话
    
    Returns:
        UserResponse: 更新后的用户信息
    """
    # 遍历更新字段
    for field, value in user_update.items():
        # 检查字段是否存在且值不为空
        if hasattr(current_user, field) and value is not None:
            setattr(current_user, field, value)
    
    # 提交更改到数据库
    db.commit()
    # 刷新用户对象以获取最新数据
    db.refresh(current_user)
    return current_user
