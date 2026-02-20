from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    phone: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = "user"
    avatar_url: Optional[str] = None
    tone_preference: Optional[str] = "温和"
    length_preference: Optional[str] = "简洁版"
    
    model_config = {"from_attributes": True}


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    phone: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    avatar_url: Optional[str] = None
    tone_preference: Optional[str] = None
    length_preference: Optional[str] = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    is_vip: bool
    vip_expire_time: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenData(BaseModel):
    username: Optional[str] = None


class PositionResponse(BaseModel):
    id: int
    name: str
    code: str
    description: Optional[str] = None
    sort_order: int
    
    class Config:
        from_attributes = True


class CategoryResponse(BaseModel):
    id: int
    name: str
    code: str
    parent_id: int
    position_id: Optional[int] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    sort_order: int
    
    class Config:
        from_attributes = True


class ScriptBase(BaseModel):
    title: str
    content: str
    brief_content: Optional[str] = None
    category_id: int
    position_id: Optional[int] = None
    scene_type: str
    tone: Optional[str] = "温和"
    target_audience: Optional[str] = None
    tags: Optional[str] = None


class ScriptCreate(ScriptBase):
    pass


class ScriptUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    brief_content: Optional[str] = None
    tone: Optional[str] = None
    tags: Optional[str] = None


class ScriptResponse(ScriptBase):
    id: int
    usage_count: int
    like_count: int
    is_free: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class ScriptDetail(ScriptResponse):
    category: Optional[CategoryResponse] = None
    position: Optional[PositionResponse] = None
    is_favorite: bool = False


class UserFavoriteBase(BaseModel):
    script_id: int
    custom_content: Optional[str] = None


class UserFavoriteCreate(UserFavoriteBase):
    pass


class UserFavoriteResponse(UserFavoriteBase):
    id: int
    user_id: int
    script: Optional[ScriptResponse] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class ConversationBase(BaseModel):
    session_id: str
    message_type: str
    content: str


class ConversationCreate(ConversationBase):
    context_data: Optional[dict] = None
    intent: Optional[str] = None
    referenced_script_id: Optional[int] = None


class ConversationResponse(ConversationBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    position: Optional[str] = None
    tone: Optional[str] = None
    length: Optional[str] = None


class ChatResponse(BaseModel):
    reply: str
    scripts: List[ScriptResponse] = []
    session_id: str
    intent: Optional[str] = None


class ScriptAdjustRequest(BaseModel):
    script_id: int
    tone: Optional[str] = None
    length_type: Optional[str] = None


class ScriptAdjustResponse(BaseModel):
    original_content: str
    adjusted_content: str
    tone: Optional[str] = None
    length_type: Optional[str] = None


class SearchRequest(BaseModel):
    keyword: str
    position_id: Optional[int] = None
    category_id: Optional[int] = None
    tone: Optional[str] = None
    scene_type: Optional[str] = None
    page: int = 1
    page_size: int = 10


class SearchResponse(BaseModel):
    scripts: List[ScriptResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str
    timestamp: datetime
