import random
import re
from typing import List, Optional, Tuple, Dict
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from models.database import Script, User, Position, Conversation, ScriptCategory
from models.schemas import ChatResponse, ScriptResponse, ScriptAdjustResponse


class EnhancedAIService:
    
    INTENT_PATTERNS = {
        'search': ['找', '搜索', '查询', '有什么', '话术', '怎么', '如何', '帮忙', '给', '要', '想'],
        'adjust_tone': ['改', '调整', '换个', '语气', '温和', '专业', '强硬', '活泼', '委婉'],
        'adjust_length': ['简洁', '详细', '短一点', '长一点', '简单', '完整'],
        'ask_position': ['岗位', '角色', '职位', '我是'],
        'ask_category': ['分类', '类别', '场景'],
        'greeting': ['你好', '您好', 'hi', 'hello', '嗨'],
        'thank': ['谢谢', '感谢', '感谢'],
        'goodbye': ['再见', '拜拜', 'exit']
    }
    
    SCENE_PATTERNS = {
        '需求沟通': {
            'keywords': ['需求', '产品', '功能', '用户', '调研', '访谈', '问卷', '分析', '确认', '评审', '变更', '传递', '答疑', '文档', 'PRD', '用户故事', '验收'],
            'scenarios': ['需求调研', '需求定义', '需求确认', '需求变更', '需求评审']
        },
        '项目推进': {
            'keywords': ['项目', '进度', '计划', '任务', '里程碑', '风险', '团队', '协调', '分配', '汇报', '总结', '启动', '收尾', '监控', '预算', '资源', 'WBS', '甘特图'],
            'scenarios': ['项目启动', '项目规划', '项目执行', '项目监控', '项目收尾']
        },
        'Bug处理': {
            'keywords': ['bug', '错误', '问题', '故障', '修复', '测试', '验收', '回归', '提交', '优先级', '严重', '定位', '排查', '复现', '质量'],
            'scenarios': ['Bug提交', 'Bug修复', 'Bug验证', 'Bug分析', 'Bug沟通']
        },
        '客户对接': {
            'keywords': ['客户', '销售', '售前', '方案', '异议', '合同', '洽谈', '投诉', '培训', '跟进', '维护', '满意度', '回访', '签约', '推荐'],
            'scenarios': ['客户接待', '需求咨询', '方案讲解', '异议处理', '合同洽谈', '客户跟进', '客户维护']
        },
        '协同配合': {
            'keywords': ['请教', '帮忙', '感谢', '拒绝', '请求', '配合', '协作', '同事', '支持', '协调'],
            'scenarios': ['请教问题', '请求帮助', '感谢帮忙', '拒绝请求']
        },
        '会议沟通': {
            'keywords': ['会议', '开会', '讨论', '决策', '评审', '总结'],
            'scenarios': ['会议开场', '会议讨论', '会议总结']
        }
    }
    
    POSITION_KEYWORDS = {
        '售前人员': ['售前', '销售', '客户', 'pre_sales', '对接客户', '客户沟通'],
        '项目经理': ['项目经理', 'pm', '项目', '统筹', 'project_manager', '项目管理'],
        '产品经理': ['产品', 'pm', '需求', 'product_manager', '产品经理'],
        '前端开发': ['前端', '前端开发', 'vue', 'react', 'frontend', '界面', '页面'],
        '后端开发': ['后端', '后端开发', '接口', 'api', 'backend', '数据库', '服务端'],
        'UI设计师': ['ui', '设计', '界面', '设计师', 'ui_designer', '交互', '视觉'],
        '测试工程师': ['测试', 'qa', 'bug', '测试工程师', 'tester', '质量']
    }
    
    TONE_ADJUSTMENTS = {
        '温和': {
            '您': '您',
            '请': '请',
            '谢谢': '非常感谢',
            '麻烦': '麻烦您',
            '理解': '非常理解',
            'prefix': '您好，',
            'suffix': '谢谢！'
        },
        '专业': {
            '您': '您',
            '请': '请',
            '谢谢': '感谢',
            '麻烦': '劳烦',
            '理解': '理解',
            'prefix': '',
            'suffix': ''
        },
        '委婉': {
            '您': '您',
            '请': '麻烦',
            '谢谢': '感谢',
            '麻烦': '打扰一下',
            '理解': '理解您的想法',
            'prefix': '不好意思，',
            'suffix': '给您添麻烦了'
        },
        '活泼': {
            '您': '你',
            '请': '请哈',
            '谢谢': '谢啦',
            '麻烦': '帮忙',
            '理解': 'get到',
            'prefix': 'Hi~',
            'suffix': '感谢支持~'
        }
    }
    
    LENGTH_ADJUSTMENTS = {
        '简洁版': {
            'ratio': 0.5,
            'suffix': '（简洁版）'
        },
        '标准版': {
            'ratio': 1.0,
            'suffix': ''
        },
        '详细版': {
            'ratio': 1.5,
            'suffix': '（详细版）'
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
    
    def detect_scene(self, message: str) -> Optional[str]:
        message = message.lower()
        
        scene_scores = {}
        for scene, pattern in self.SCENE_PATTERNS.items():
            score = 0
            for keyword in pattern['keywords']:
                if keyword in message:
                    score += 1
            if score > 0:
                scene_scores[scene] = score
        
        if scene_scores:
            return max(scene_scores, key=scene_scores.get)
        
        return None
    
    def detect_position(self, message: str, user: User = None) -> Optional[str]:
        if user and user.role:
            role = user.role
            for position_name, keywords in self.POSITION_KEYWORDS.items():
                if role in keywords:
                    return position_name
        
        message = message.lower()
        for position, keywords in self.POSITION_KEYWORDS.items():
            for keyword in keywords:
                if keyword in message:
                    return position
        
        return None
    
    def extract_keywords(self, message: str) -> List[str]:
        # 优化的关键词提取逻辑
        keywords = []
        
        # 预定义的核心词汇表
        core_words = {
            '需求', '沟通', '变更', '传递', '确认', '评审', '调研', '访谈', '对接', '咨询', '反馈', '澄清', '优先级',
            '项目', '推进', '启动', '风险', '进度', '里程碑', '汇报', '任务', '分配', '协调', '资源', '计划', '目标',
            'bug', 'Bug', '问题', '反馈', '修复', '验收', '分配', '协助', '异议', '优先级', '发现', '提交流程',
            '客户', '接待', '投诉', '异议', '跟进', '寒暄', '拜访', '维护', '服务', '咨询', '沟通', '异议处理',
            '售前', '产品经理', '项目经理', '前端', '后端', '测试', 'ui', '设计师',
            '开发', '团队', '领导', '同事', '用户', '公司', '价格', '方案'
        }
        
        # 移除标点符号和特殊字符
        clean_message = re.sub(r'[，。！？、；：""''（）【】《》\s]', ' ', message)
        
        # 先尝试匹配核心词汇
        for core_word in core_words:
            if core_word in message:
                keywords.append(core_word)
        
        # 按空格分割其他词汇
        words = clean_message.split()
        
        # 过滤停用词
        stop_words = {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这', '如何', '应该', '怎么', '什么', '哪里', '可以', '需要', '想要', '希望', '了解', '知道', '觉得', '认为', '发现', '告诉', '提出', '描述', '开场', '结束'}
        
        for word in words:
            if len(word) >= 2 and len(word) <= 6 and word not in stop_words and word not in keywords:
                keywords.append(word)
        
        return keywords
    
    def search_scripts(
        self, 
        keywords: List[str], 
        position: str = None,
        scene_type: str = None,
        tone: str = None,
        limit: int = 5
    ) -> List[Script]:
        query = self.db.query(Script).filter(Script.is_active == True)
        
        if position:
            pos = self.db.query(Position).filter(Position.name == position).first()
            if pos:
                query = query.filter(Script.position_id == pos.id)
            else:
                # 如果岗位名称不匹配，尝试使用position_id
                try:
                    position_id = int(position)
                    query = query.filter(Script.position_id == position_id)
                except ValueError:
                    pass
        
        if scene_type:
            # 如果scene_type精确匹配不到，尝试模糊匹配
            scene_match = query.filter(Script.scene_type == scene_type).first()
            if scene_match:
                query = query.filter(Script.scene_type == scene_type)
            else:
                # 尝试模糊匹配场景类型
                scene_conditions = (
                    Script.scene_type.like(f'%{scene_type}%') |
                    Script.scene_type.contains(scene_type)
                )
                query = query.filter(scene_conditions)
        
        if tone:
            query = query.filter(Script.tone == tone)
        
        if keywords:
            keyword_conditions = []
            for kw in keywords:
                if len(kw) >= 2:
                    keyword_conditions.append(
                        (Script.title.like(f'%{kw}%') | 
                         Script.content.like(f'%{kw}%') | 
                         Script.tags.like(f'%{kw}%') |
                         Script.brief_content.like(f'%{kw}%'))
                    )
            
            if keyword_conditions:
                query = query.filter(or_(*keyword_conditions))
        
        # 先按照使用次数排序，如果没有结果，就移除限制
        scripts = query.order_by(Script.usage_count.desc()).limit(limit * 3).all()
        
        if not scripts:
            # 如果没有结果，移除岗位和场景限制，只按关键词搜索
            query = self.db.query(Script).filter(Script.is_active == True)
            if keywords:
                keyword_conditions = []
                for kw in keywords:
                    if len(kw) >= 2:
                        keyword_conditions.append(
                            (Script.title.like(f'%{kw}%') | 
                             Script.content.like(f'%{kw}%') | 
                             Script.tags.like(f'%{kw}%') |
                             Script.brief_content.like(f'%{kw}%'))
                        )
                
                if keyword_conditions:
                    query = query.filter(or_(*keyword_conditions))
            
            scripts = query.order_by(Script.usage_count.desc()).limit(limit).all()
        
        return scripts[:limit]
    
    def generate_response_based_on_scene(
        self,
        message: str,
        detected_scene: str,
        position: str = None,
        tone: str = None,
        length: str = None
    ) -> Tuple[str, List[Script]]:
        
        keywords = self.extract_keywords(message)
        
        # 先尝试匹配场景
        scripts = self.search_scripts(
            keywords=keywords,
            position=position,
            scene_type=detected_scene,
            tone=tone,
            limit=5
        )
        
        # 如果没有找到，尝试只根据关键词搜索，不限制场景
        if not scripts:
            scripts = self.search_scripts(
                keywords=keywords,
                position=position,
                tone=tone,
                limit=5
            )
        
        # 如果还是没有找到，尝试不限制岗位
        if not scripts:
            scripts = self.search_scripts(
                keywords=keywords,
                tone=tone,
                limit=5
            )
        
        if scripts:
            reply = self._generate_scene_response(detected_scene, scripts, position)
            return reply, scripts
        else:
            reply = self._generate_no_match_response(detected_scene, position)
            return reply, []
    
    def _generate_scene_response(
        self, 
        scene: str, 
        scripts: List[Script], 
        position: str = None
    ) -> str:
        scene_messages = {
            '需求沟通': f"为您找到了{len(scripts)}条需求沟通相关的话术：",
            '项目推进': f"为您找到了{len(scripts)}条项目推进相关的话术：",
            'Bug处理': f"为您找到了{len(scripts)}条Bug处理相关的话术：",
            '客户对接': f"为您找到了{len(scripts)}条客户对接相关的话术：",
            '协同配合': f"为您找到了{len(scripts)}条协同配合相关的话术：",
            '会议沟通': f"为您找到了{len(scripts)}条会议沟通相关的话术："
        }
        
        reply = scene_messages.get(scene, f"为您找到了{len(scripts)}条相关话术：")
        
        if position:
            reply += f"\n\n针对【{position}】岗位："
        
        return reply
    
    def _generate_no_match_response(
        self, 
        scene: str = None, 
        position: str = None
    ) -> str:
        if scene and position:
            return f"抱歉，暂时没有找到{scene}相关的{position}话术。\n\n您可以尝试：\n1. 描述更具体的沟通场景\n2. 告诉我您的岗位\n3. 尝试其他关键词"
        elif scene:
            return f"抱歉，暂时没有找到{scene}相关的话术。\n\n您可以尝试：\n1. 描述更具体的沟通场景\n2. 告诉我您的岗位\n3. 尝试其他关键词"
        else:
            return "抱歉，没有找到完全匹配的话术。\n\n您可以：\n1. 描述具体的沟通场景（如：需求沟通、项目推进、Bug处理、客户对接）\n2. 告诉我您的岗位\n3. 尝试更详细的关键词"
    
    def generate_greeting(self, user: User = None) -> str:
        greetings = [
            "您好！我是高情商聊天助手，我可以帮您：\n\n💬 需求沟通话术\n📋 项目推进话术\n🐛 Bug处理话术\n👥 客户对接话术\n\n请告诉我您的沟通场景，我会为您推荐合适的话术！",
            "你好！我是您的专属沟通搭子，无论是需求对接、项目推进还是客户沟通，都可以找我聊聊~\n\n我可以帮您生成各种场景的高情商话术，让工作沟通更顺畅！",
            "Hi~ 我是高情商聊天助手！\n\n我能为您提供：\n✅ 专业的沟通话术\n✅ 多种语气调整\n✅ 场景智能匹配\n✅ 话术个性化定制\n\n有什么需要帮助的吗？"
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
                if old not in ['prefix', 'suffix']:
                    adjusted_content = adjusted_content.replace(old, new)
            
            prefix = tone_rules.get('prefix', '')
            suffix = tone_rules.get('suffix', '')
            
            if prefix and not adjusted_content.startswith(prefix):
                adjusted_content = prefix + adjusted_content
            if suffix and not adjusted_content.endswith(suffix):
                adjusted_content = adjusted_content + suffix
        
        if length_type and length_type in self.LENGTH_ADJUSTMENTS:
            length_rule = self.LENGTH_ADJUSTMENTS[length_type]
            ratio = length_rule['ratio']
            suffix = length_rule['suffix']
            
            if ratio < 1.0:
                sentences = re.split(r'[。！？\n]', adjusted_content)
                adjusted_content = sentences[0] + '。' + suffix
            elif ratio > 1.0:
                adjusted_content += "\n\n补充说明：如果您需要更详细的沟通方案，可以根据具体情况调整话术的细节部分，确保沟通效果最佳。" + suffix
            else:
                if suffix:
                    adjusted_content += suffix
        
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
            reply = "不客气！还有其他需要帮助的吗？我可以帮您生成各种沟通话术~"
            return ChatResponse(
                reply=reply,
                scripts=[],
                session_id=session_id or '',
                intent='thank'
            )
        
        if intent == 'goodbye':
            reply = "好的，再见！有问题随时找我，祝您工作顺利~"
            return ChatResponse(
                reply=reply,
                scripts=[],
                session_id=session_id or '',
                intent='goodbye'
            )
        
        if intent == 'ask_position':
            reply = "您可以选择以下岗位，我会为您推荐更精准的话术：\n\n👤 售前人员\n📊 项目经理\n📱 产品经理\n🎨 前端开发\n⚙️ 后端开发\n🖼️ UI设计师\n🔍 测试工程师\n\n请告诉我您的岗位，或者描述具体的沟通场景！"
            return ChatResponse(
                reply=reply,
                scripts=[],
                session_id=session_id or '',
                intent='ask_position'
            )
        
        detected_position = self.detect_position(message, user) or position
        detected_scene = self.detect_scene(message)
        
        user_tone = user.tone_preference if user else '温和'
        user_length = user.length_preference if user else '标准版'
        
        if detected_scene:
            reply, scripts = self.generate_response_based_on_scene(
                message=message,
                detected_scene=detected_scene,
                position=detected_position,
                tone=tone or user_tone,
                length=length or user_length
            )
            
            if scripts:
                script_list = [
                    ScriptResponse.model_validate(script) 
                    for script in scripts
                ]
                
                return ChatResponse(
                    reply=reply,
                    scripts=script_list,
                    session_id=session_id or '',
                    intent='search'
                )
            else:
                return ChatResponse(
                    reply=reply,
                    scripts=[],
                    session_id=session_id or '',
                    intent='search'
                )
        else:
            keywords = self.extract_keywords(message)
            scripts = self.search_scripts(
                keywords=keywords,
                position=detected_position,
                tone=tone or user_tone,
                limit=5
            )
            
            if scripts:
                script_list = [
                    ScriptResponse.model_validate(script) 
                    for script in scripts
                ]
                
                reply = f"为您找到了{len(scripts)}条相关话术："
                if detected_position:
                    reply += f"\n\n针对【{detected_position}】岗位："
                
                return ChatResponse(
                    reply=reply,
                    scripts=script_list,
                    session_id=session_id or '',
                    intent='search'
                )
            else:
                reply = self._generate_no_match_response(detected_scene, detected_position)
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
    
    def get_recommended_scripts(
        self,
        user: User = None,
        scene_type: str = None,
        limit: int = 5
    ) -> List[Script]:
        query = self.db.query(Script).filter(Script.is_active == True)
        
        if user and user.role:
            pos = self.db.query(Position).filter(Position.name == user.role).first()
            if pos:
                query = query.filter(Script.position_id == pos.id)
        
        if scene_type:
            query = query.filter(Script.scene_type == scene_type)
        
        return query.order_by(Script.usage_count.desc(), Script.like_count.desc()).limit(limit).all()
