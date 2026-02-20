import random
import re
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from models.database import Script, User, Position, Conversation
from models.schemas import ChatResponse, ScriptResponse, ScriptAdjustResponse


class AIService:
    
    INTENT_PATTERNS = {
        'search': ['找', '搜索', '查询', '有什么', '话术', '怎么', '如何', '帮忙'],
        'adjust_tone': ['改', '调整', '换个', '语气', '温和', '专业', '强硬', '活泼', '委婉'],
        'adjust_length': ['简洁', '详细', '短一点', '长一点', '简单', '完整'],
        'ask_position': ['岗位', '角色', '职位', '我是'],
        'ask_category': ['分类', '类别', '场景'],
        'greeting': ['你好', '您好', 'hi', 'hello', '嗨'],
        'thank': ['谢谢', '感谢', '感谢'],
        'goodbye': ['再见', '拜拜', 'exit']
    }
    
    POSITION_KEYWORDS = {
        '售前': ['售前', '销售', '客户', 'pre_sales'],
        '项目经理': ['项目经理', 'pm', '项目', '统筹', 'project_manager'],
        '产品经理': ['产品', 'pm', '需求', 'product_manager'],
        '前端': ['前端', '前端开发', 'vue', 'react', 'frontend'],
        '后端': ['后端', '后端开发', '接口', 'api', 'backend'],
        'ui': ['ui', '设计', '界面', '设计师', 'ui_designer'],
        '测试': ['测试', 'qa', 'bug', '测试工程师', 'tester']
    }
    
    TONE_ADJUSTMENTS = {
        '温和': {
            '您': '您',
            '请': '请',
            '谢谢': '非常感谢',
            '麻烦': '麻烦您',
            '理解': '非常理解'
        },
        '专业': {
            '您': '您',
            '请': '请',
            '谢谢': '感谢',
            '麻烦': '劳烦',
            '理解': '理解'
        },
        '强硬': {
            '您': '你',
            '请': '',
            '谢谢': '',
            '麻烦': '',
            '理解': '明白'
        },
        '活泼': {
            '您': '你',
            '请': '请哈',
            '谢谢': '谢啦',
            '麻烦': '帮忙',
            '理解': 'get到'
        },
        '委婉': {
            '您': '您',
            '请': '麻烦',
            '谢谢': '感谢',
            '麻烦': '打扰一下',
            '理解': '理解您的想法'
        }
    }
    
    def __init__(self, db: Session):
        self.db = db
    
    def detect_intent(self, message: str, context: List[dict] = None) -> Tuple[str, Optional[str]]:
        message = message.lower()
        
        for intent, keywords in self.INTENT_PATTERNS.items():
            for keyword in keywords:
                if keyword in message:
                    return intent, None
        
        return 'search', None
    
    def detect_position(self, message: str, user: User = None) -> Optional[str]:
        if user and user.role:
            return user.role
        
        message = message.lower()
        for position, keywords in self.POSITION_KEYWORDS.items():
            for keyword in keywords:
                if keyword in message:
                    return position
        
        return None
    
    def extract_keywords(self, message: str) -> List[str]:
        keywords = []
        patterns = [
            r'([A-Za-z0-9]+)',
            r'([\u4e00-\u9fa5]{2,})',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, message)
            keywords.extend(matches)
        
        return list(set([k for k in keywords if len(k) >= 2]))
    
    def search_scripts(
        self, 
        keywords: List[str], 
        position: str = None,
        tone: str = None,
        limit: int = 5
    ) -> List[Script]:
        query = self.db.query(Script).filter(Script.is_active == True)
        
        if position:
            pos = self.db.query(Position).filter(Position.name == position).first()
            if pos:
                query = query.filter(Script.position_id == pos.id)
        
        if tone:
            query = query.filter(Script.tone == tone)
        
        if keywords:
            keyword_conditions = []
            for kw in keywords:
                keyword_conditions.append(
                    (Script.title.like(f'%{kw}%') | 
                     Script.content.like(f'%{kw}%') | 
                     Script.tags.like(f'%{kw}%'))
                )
            
            if keyword_conditions:
                from sqlalchemy import or_
                query = query.filter(or_(*keyword_conditions))
        
        return query.order_by(Script.usage_count.desc()).limit(limit).all()
    
    def generate_greeting(self, user: User = None) -> str:
        greetings = [
            "您好！我是VibeCoding高情商聊天助手，有什么我可以帮您的吗？",
            "你好！我是你的专属沟通搭子，无论是需求对接、项目推进还是团队协作，都可以找我聊聊~",
            "Hi~ 我是VibeCoding助手，帮你解决各种沟通难题，让工作更顺畅！",
        ]
        return random.choice(greetings)
    
    def adjust_script_content(
        self, 
        content: str, 
        tone: str = None, 
        length_type: str = None
    ) -> str:
        adjusted_content = content
        
        if tone and tone in self.TONE_ADJUSTMENTS:
            tone_rules = self.TONE_ADJUSTMENTS[tone]
            for old, new in tone_rules.items():
                adjusted_content = adjusted_content.replace(old, new)
        
        if length_type == '简洁版' and len(adjusted_content) > 50:
            sentences = re.split(r'[。！？\n]', adjusted_content)
            adjusted_content = sentences[0] + '。'
        elif length_type == '详细版' and len(adjusted_content) < 100:
            adjusted_content += " 如果需要更详细的沟通方案，我可以进一步为您优化。"
        
        return adjusted_content
    
    def generate_chat_response(
        self,
        message: str,
        user: User = None,
        session_id: str = None,
        position: str = None,
        tone: str = None,
        length: str = None,
        context: List[dict] = None
    ) -> ChatResponse:
        intent, _ = self.detect_intent(message, context)
        
        if intent == 'greeting':
            reply = self.generate_greeting(user)
            return ChatResponse(
                reply=reply,
                scripts=[],
                session_id=session_id or '',
                intent='greeting'
            )
        
        if intent == 'thank':
            reply = "不客气！还有其他需要帮助的吗？"
            return ChatResponse(
                reply=reply,
                scripts=[],
                session_id=session_id or '',
                intent='thank'
            )
        
        if intent == 'goodbye':
            reply = "好的，再见！有问题随时找我~"
            return ChatResponse(
                reply=reply,
                scripts=[],
                session_id=session_id or '',
                intent='goodbye'
            )
        
        if intent == 'ask_position':
            reply = "您可以选择以下岗位：\n- 售前人员\n- 项目经理\n- 产品经理\n- 前端开发\n- 后端开发\n- UI设计师\n- 测试工程师\n\n请告诉我您的岗位，我会为您推荐更精准的话术。"
            return ChatResponse(
                reply=reply,
                scripts=[],
                session_id=session_id or '',
                intent='ask_position'
            )
        
        detected_position = self.detect_position(message, user) or position
        user_tone = user.tone_preference if user else '温和'
        user_length = user.length_preference if user else '简洁版'
        
        keywords = self.extract_keywords(message)
        scripts = self.search_scripts(keywords, detected_position, tone or user_tone)
        
        if scripts:
            script_list = [
                ScriptResponse.model_validate(script) 
                for script in scripts
            ]
            
            reply = f"为您找到了{len(scripts)}条相关话术："
            if detected_position:
                reply += f"\n\n岗位：{detected_position}"
            
            return ChatResponse(
                reply=reply,
                scripts=script_list,
                session_id=session_id or '',
                intent='search'
            )
        else:
            reply = "抱歉，没有找到完全匹配的话术。您可以：\n1. 尝试更换关键词\n2. 告诉我您的岗位\n3. 描述更具体的沟通场景"
            return ChatResponse(
                reply=reply,
                scripts=[],
                session_id=session_id or '',
                intent='search'
            )
    
    def adjust_script(
        self,
        script_id: int,
        tone: str = None,
        length_type: str = None
    ) -> ScriptAdjustResponse:
        script = self.db.query(Script).filter(Script.id == script_id).first()
        if not script:
            raise ValueError("话术不存在")
        
        original_content = script.content
        if length_type == '简洁版' and script.brief_content:
            original_content = script.brief_content
        
        adjusted_content = self.adjust_script_content(original_content, tone, length_type)
        
        return ScriptAdjustResponse(
            original_content=original_content,
            adjusted_content=adjusted_content,
            tone=tone,
            length_type=length_type
        )
    
    def save_conversation(
        self,
        user_id: int,
        session_id: str,
        message_type: str,
        content: str,
        context_data: dict = None,
        intent: str = None,
        referenced_script_id: int = None
    ) -> Conversation:
        conversation = Conversation(
            user_id=user_id,
            session_id=session_id,
            message_type=message_type,
            content=content,
            context_data=context_data,
            intent=intent,
            referenced_script_id=referenced_script_id
        )
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation
    
    def get_conversation_history(
        self,
        user_id: int,
        session_id: str,
        limit: int = 10
    ) -> List[Conversation]:
        return (
            self.db.query(Conversation)
            .filter(
                Conversation.user_id == user_id,
                Conversation.session_id == session_id
            )
            .order_by(Conversation.created_at.desc())
            .limit(limit)
            .all()
        )
