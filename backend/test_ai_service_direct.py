import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.ai_service_enhanced import EnhancedAIService
from models.database import SessionLocal

def test_ai_service():
    print("=" * 60)
    print("直接测试AI服务的搜索方法")
    print("=" * 60)
    
    db = SessionLocal()
    try:
        ai_service = EnhancedAIService(db)
        
        # 测试搜索需求沟通的产品经理话术
        print("\n1. 搜索需求沟通的产品经理话术:")
        keywords = ['需求', '变更', '沟通']
        scripts = ai_service.search_scripts(
            keywords=keywords,
            position='产品经理',
            scene_type='需求沟通',
            limit=5
        )
        print(f"   找到 {len(scripts)} 条话术")
        for i, script in enumerate(scripts, 1):
            print(f"   {i}. {script.title} - {script.scene_type}")
        
        # 测试搜索项目推进的项目经理话术
        print("\n2. 搜索项目推进的项目经理话术:")
        keywords = ['项目', '启动', '风险']
        scripts = ai_service.search_scripts(
            keywords=keywords,
            position='项目经理',
            scene_type='项目推进',
            limit=5
        )
        print(f"   找到 {len(scripts)} 条话术")
        for i, script in enumerate(scripts, 1):
            print(f"   {i}. {script.title} - {script.scene_type}")
        
        # 测试搜索Bug处理的测试工程师话术
        print("\n3. 搜索Bug处理的测试工程师话术:")
        keywords = ['bug', '反馈', '修复']
        scripts = ai_service.search_scripts(
            keywords=keywords,
            position='测试工程师',
            scene_type='Bug处理',
            limit=5
        )
        print(f"   找到 {len(scripts)} 条话术")
        for i, script in enumerate(scripts, 1):
            print(f"   {i}. {script.title} - {script.scene_type}")
        
        # 测试搜索客户对接的售前人员话术
        print("\n4. 搜索客户对接的售前人员话术:")
        keywords = ['客户', '接待', '投诉']
        scripts = ai_service.search_scripts(
            keywords=keywords,
            position='售前人员',
            scene_type='客户对接',
            limit=5
        )
        print(f"   找到 {len(scripts)} 条话术")
        for i, script in enumerate(scripts, 1):
            print(f"   {i}. {script.title} - {script.scene_type}")
        
        # 测试完整对话流程
        print("\n5. 测试完整对话流程:")
        test_messages = [
            "客户提出需求变更，怎么沟通影响",
            "项目启动会应该怎么开场",
            "发现了一个严重的Bug，需要反馈给后端开发",
            "初次接待客户应该怎么说"
        ]
        
        for msg in test_messages:
            print(f"\n   用户消息: {msg}")
            detected_scene = ai_service.detect_scene(msg)
            print(f"   检测到场景: {detected_scene}")
            
            keywords = ai_service.extract_keywords(msg)
            print(f"   提取关键词: {keywords}")
            
            scripts = ai_service.search_scripts(
                keywords=keywords,
                scene_type=detected_scene,
                limit=3
            )
            print(f"   找到 {len(scripts)} 条话术")
            for i, script in enumerate(scripts, 1):
                print(f"   {i}. {script.title}")
    
    finally:
        db.close()
        print("\n" + "=" * 60)
        print("测试完成")
        print("=" * 60)

if __name__ == '__main__':
    test_ai_service()
