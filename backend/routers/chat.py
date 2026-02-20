# 导入FastAPI相关组件
from fastapi import APIRouter, Depends
# 导入SQLAlchemy会话类型
from sqlalchemy.orm import Session
# 导入可选类型
from typing import Optional
# 导入UUID生成模块
import uuid
# 导入数据库相关模块和用户模型
from models.database import get_db, User
# 导入请求和响应的数据模型
from models.schemas import ChatRequest, ChatResponse, ScriptAdjustResponse, ScriptAdjustRequest
# 导入增强的AI服务
from services.ai_service_enhanced import EnhancedAIService
# 导入认证工具
from utils.auth import get_current_active_user

# 创建API路由器，设置前缀和标签
router = APIRouter(prefix="/api/chat", tags=["聊天"])


@router.post("/message", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    处理用户聊天消息请求
    
    参数:
        request: 聊天请求对象，包含用户消息、会话ID、语气、长度等参数
        db: 数据库会话依赖
        current_user: 当前激活用户依赖
    
    返回:
        ChatResponse: AI生成的回复，包含回复内容和意图
    """
    # 初始化增强的AI服务
    ai_service = EnhancedAIService(db)
    
    # 获取或生成会话ID，用于跟踪对话上下文
    session_id = request.session_id or str(uuid.uuid4())
    
    # 获取历史对话上下文，限制最近5条记录，用于理解对话上下文
    context = ai_service.get_conversation_history(
        current_user.id, 
        session_id, 
        limit=5
    )
    
    # 保存用户的消息到数据库
    ai_service.save_conversation(
        user_id=current_user.id,
        session_id=session_id,
        message_type='user',
        content=request.message,
        intent=None
    )
    
    # 生成AI回复，传入用户消息、用户信息、会话ID、语气、长度等参数
    response = ai_service.generate_chat_response(
        message=request.message,
        user=current_user,
        session_id=session_id,
        position=request.position,
        tone=request.tone,
        length=request.length,
        context=context
    )
    
    # 保存AI助手的回复到数据库
    ai_service.save_conversation(
        user_id=current_user.id,
        session_id=session_id,
        message_type='assistant',
        content=response.reply,
        intent=response.intent,
        referenced_script_id=None
    )
    
    # 返回AI生成的回复
    return response


@router.post("/adjust", response_model=ScriptAdjustResponse)
async def adjust_script(
    request: ScriptAdjustRequest,
    db: Session = Depends(get_db)
):
    """
    调整脚本的语气和长度
    
    参数:
        request: 脚本调整请求对象，包含脚本ID、目标语气和长度类型
        db: 数据库会话依赖
    
    返回:
        ScriptAdjustResponse: 调整后的脚本内容
    
    异常:
        HTTPException: 当脚本不存在时返回404错误
    """
    # 初始化增强的AI服务
    ai_service = EnhancedAIService(db)
    
    try:
        # 调用AI服务调整脚本
        result = ai_service.adjust_script(
            script_id=request.script_id,
            tone=request.tone,
            length_type=request.length_type
        )
        return result
    except ValueError as e:
        # 处理脚本不存在的情况，返回404错误
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/history/{session_id}")
async def get_chat_history(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取指定会话的聊天历史记录
    
    参数:
        session_id: 会话ID字符串
        db: 数据库会话依赖
        current_user: 当前激活用户依赖
    
    返回:
        List[Dict]: 聊天历史记录列表，按时间倒序排列，每条记录包含:
            - id: 消息ID
            - message_type: 消息类型(user/assistant)
            - content: 消息内容
            - intent: 意图
            - referenced_script_id: 引用的脚本ID
            - created_at: 创建时间
    """
    # 初始化增强的AI服务
    ai_service = EnhancedAIService(db)
    # 获取该会话的对话历史
    history = ai_service.get_conversation_history(current_user.id, session_id)
    
    # 将历史记录转换为字典格式，并按时间倒序排列
    return [
        {
            "id": conv.id,
            "message_type": conv.message_type,
            "content": conv.content,
            "intent": conv.intent,
            "referenced_script_id": conv.referenced_script_id,
            "created_at": conv.created_at
        }
        for conv in reversed(history)
    ]
