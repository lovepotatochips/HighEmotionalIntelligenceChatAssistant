from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from models.database import get_db, Position, ScriptCategory
from models.schemas import PositionResponse, CategoryResponse
from datetime import datetime

# 创建系统API路由器，前缀为/api/system，标签为"系统"
router = APIRouter(prefix="/api/system", tags=["系统"])


@router.get("/positions", response_model=List[PositionResponse])
async def get_positions(db: Session = Depends(get_db)):
    """获取所有激活的职位列表
    
    Returns:
        List[PositionResponse]: 职位列表，按sort_order排序
    """
    positions = db.query(Position).filter(
        Position.is_active == True
    ).order_by(Position.sort_order).all()
    
    return [PositionResponse.model_validate(pos) for pos in positions]


@router.get("/categories", response_model=List[CategoryResponse])
async def get_categories(
    position_id: int = None,
    db: Session = Depends(get_db)
):
    """获取脚本分类列表
    
    Args:
        position_id: 可选，按职位ID筛选分类
        db: 数据库会话
    
    Returns:
        List[CategoryResponse]: 分类列表，按sort_order排序
    """
    query = db.query(ScriptCategory).filter(ScriptCategory.is_active == True)
    
    if position_id:
        query = query.filter(ScriptCategory.position_id == position_id)
    
    categories = query.order_by(ScriptCategory.sort_order).all()
    
    return [CategoryResponse.model_validate(cat) for cat in categories]


@router.get("/health")
async def health_check():
    """健康检查接口
    
    Returns:
        dict: 包含应用状态、名称、版本和时间戳的字典
    """
    return {
        "status": "ok",
        "app_name": "VibeCoding高情商聊天助手",
        "version": "1.0.0",
        "timestamp": datetime.now()
    }
