# 话术管理相关路由
# 提供话术的搜索、详情查看、点赞、收藏等功能

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Optional

# 数据库模型导入
from models.database import get_db, Script, ScriptCategory, UserFavorite, User
# 数据模型/响应模型导入
from models.schemas import (
    ScriptResponse,    # 话术列表项响应模型
    ScriptDetail,     # 话术详情响应模型
    SearchResponse,   # 搜索结果响应模型
    UserFavoriteCreate,  # 创建收藏请求模型
    UserFavoriteResponse # 收藏响应模型
)
# 认证工具
from utils.auth import get_current_active_user

# 创建话术路由器，指定前缀和标签
router = APIRouter(prefix="/api/scripts", tags=["话术"])


@router.get("/", response_model=SearchResponse)
async def get_scripts(
    position_id: Optional[int] = Query(None, description="岗位ID"),
    category_id: Optional[int] = Query(None, description="分类ID"),
    scene_type: Optional[str] = Query(None, description="场景类型"),
    tone: Optional[str] = Query(None, description="语气"),
    keyword: Optional[str] = Query(None, description="关键词"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=50, description="每页数量"),
    db: Session = Depends(get_db)
):
    """
    获取话术列表接口
    
    支持多维度筛选和分页查询，包括岗位、分类、场景类型、语气、关键词等筛选条件。
    
    Args:
        position_id: 岗位ID，可选，用于筛选特定岗位的话术
        category_id: 分类ID，可选，用于筛选特定分类下的话术
        scene_type: 场景类型，可选，如：需求沟通、项目推进、Bug处理等
        tone: 语气，可选，如：温和、专业、强硬、活泼、委婉
        keyword: 关键词，可选，在标题、内容、标签中搜索
        page: 页码，默认为1，最小值为1
        page_size: 每页数量，默认为10，范围1-50
        db: 数据库会话
    
    Returns:
        SearchResponse: 包含话术列表、总数、分页信息的响应
    
    Example:
        GET /api/scripts?position_id=3&scene_type=需求沟通&page=1&page_size=10
    """
    query = db.query(Script).filter(Script.is_active == True)
    
    if position_id:
        query = query.filter(Script.position_id == position_id)
    
    if category_id:
        query = query.filter(Script.category_id == category_id)
    
    if scene_type:
        query = query.filter(Script.scene_type == scene_type)
    
    if tone:
        query = query.filter(Script.tone == tone)
    
    if keyword:
        query = query.filter(
            or_(
                Script.title.like(f'%{keyword}%'),
                Script.content.like(f'%{keyword}%'),
                Script.tags.like(f'%{keyword}%')
            )
        )
    
    total = query.count()
    scripts = query.order_by(Script.usage_count.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    return SearchResponse(
        scripts=[ScriptResponse.model_validate(script) for script in scripts],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size
    )


@router.get("/{script_id}", response_model=ScriptDetail)
async def get_script(
    script_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取话术详情接口
    
    返回话术的完整信息，包括分类、是否已收藏等。
    查看话术时会自动增加使用次数。
    
    Args:
        script_id: 话术ID
        db: 数据库会话
        current_user: 当前登录用户
    
    Returns:
        ScriptDetail: 话术详情，包含分类信息和收藏状态
    
    Raises:
        HTTPException: 话术不存在时返回404
    
    Example:
        GET /api/scripts/123
    """
    script = db.query(Script).filter(Script.id == script_id).first()
    if not script:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="话术不存在"
        )
    
    category = db.query(ScriptCategory).filter(ScriptCategory.id == script.category_id).first()
    
    favorite = db.query(UserFavorite).filter(
        and_(
            UserFavorite.user_id == current_user.id,
            UserFavorite.script_id == script_id
        )
    ).first()
    
    script.usage_count += 1
    db.commit()
    
    return ScriptDetail(
        id=script.id,
        title=script.title,
        content=script.content,
        brief_content=script.brief_content,
        category_id=script.category_id,
        position_id=script.position_id,
        scene_type=script.scene_type,
        tone=script.tone,
        target_audience=script.target_audience,
        tags=script.tags,
        usage_count=script.usage_count,
        like_count=script.like_count,
        is_free=script.is_free,
        created_at=script.created_at,
        category=category,
        is_favorite=favorite is not None
    )


@router.post("/{script_id}/like", status_code=status.HTTP_200_OK)
async def like_script(
    script_id: int,
    db: Session = Depends(get_db)
):
    """
    点赞话术接口
    
    为指定的话术增加点赞次数，用于统计用户对话术的喜爱程度。
    
    Args:
        script_id: 话术ID
        db: 数据库会话
    
    Returns:
        dict: 包含成功消息和当前点赞数的响应
    
    Raises:
        HTTPException: 话术不存在时返回404
    
    Example:
        POST /api/scripts/123/like
        Response: {"message": "点赞成功", "like_count": 10}
    """
    script = db.query(Script).filter(Script.id == script_id).first()
    if not script:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="话术不存在"
        )
    
    script.like_count += 1
    db.commit()
    
    return {"message": "点赞成功", "like_count": script.like_count}


@router.post("/favorites", response_model=UserFavoriteResponse, status_code=status.HTTP_201_CREATED)
async def add_favorite(
    favorite: UserFavoriteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    添加收藏接口
    
    将指定话术添加到用户的收藏列表，支持自定义话术内容。
    每个用户对同一话术只能收藏一次。
    
    Args:
        favorite: 收藏创建信息，包含话术ID和自定义内容
        db: 数据库会话
        current_user: 当前登录用户
    
    Returns:
        UserFavoriteResponse: 创建的收藏记录
    
    Raises:
        HTTPException: 话术不存在返回404，已收藏返回400
    
    Example:
        POST /api/scripts/favorites
        Body: {"script_id": 123, "custom_content": "自定义内容"}
    """
    script = db.query(Script).filter(Script.id == favorite.script_id).first()
    if not script:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="话术不存在"
        )
    
    existing = db.query(UserFavorite).filter(
        and_(
            UserFavorite.user_id == current_user.id,
            UserFavorite.script_id == favorite.script_id
        )
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="已经收藏过该话术"
        )
    
    db_favorite = UserFavorite(
        user_id=current_user.id,
        script_id=favorite.script_id,
        custom_content=favorite.custom_content
    )
    
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    
    return db_favorite


@router.delete("/favorites/{script_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_favorite(
    script_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    取消收藏接口
    
    从用户的收藏列表中移除指定话术。
    
    Args:
        script_id: 话术ID
        db: 数据库会话
        current_user: 当前登录用户
    
    Returns:
        None: 成功删除时返回204状态码
    
    Raises:
        HTTPException: 收藏不存在时返回404
    
    Example:
        DELETE /api/scripts/favorites/123
    """
    favorite = db.query(UserFavorite).filter(
        and_(
            UserFavorite.user_id == current_user.id,
            UserFavorite.script_id == script_id
        )
    ).first()
    
    if not favorite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="收藏不存在"
        )
    
    db.delete(favorite)
    db.commit()
    
    return None


@router.get("/favorites/list", response_model=List[UserFavoriteResponse])
async def get_favorites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取收藏列表接口
    
    返回当前用户的所有收藏记录，按创建时间倒序排列。
    包含话术的完整信息和用户自定义内容。
    
    Args:
        db: 数据库会话
        current_user: 当前登录用户
    
    Returns:
        List[UserFavoriteResponse]: 收藏列表
    
    Example:
        GET /api/scripts/favorites/list
    """
    favorites = db.query(UserFavorite).filter(
        UserFavorite.user_id == current_user.id
    ).order_by(UserFavorite.created_at.desc()).all()
    
    result = []
    for favorite in favorites:
        script = db.query(Script).filter(Script.id == favorite.script_id).first()
        if script:
            result.append(UserFavoriteResponse(
                id=favorite.id,
                user_id=favorite.user_id,
                script_id=favorite.script_id,
                custom_content=favorite.custom_content,
                script=script,
                created_at=favorite.created_at
            ))
    
    return result
