import sqlite3

def debug_scenes():
    conn = sqlite3.connect('vibe_chat.db')
    cursor = conn.cursor()
    
    print("=" * 60)
    print("检查场景检测逻辑")
    print("=" * 60)
    
    # 检查scripts表中的scene_type分布
    print("\n1. Scripts表scene_type分布:")
    cursor.execute('''
        SELECT scene_type, COUNT(*) as count
        FROM scripts
        GROUP BY scene_type
        ORDER BY count DESC
    ''')
    scenes = cursor.fetchall()
    for scene in scenes:
        print(f"   {scene[0]}: {scene[1]}条")
    
    # 测试场景检测逻辑
    print("\n2. 测试场景检测:")
    
    SCENE_KEYWORDS = {
        '需求沟通': ['需求', '需求沟通', '需求调研', '需求确认', '需求评审', '需求变更', '需求传递', '用户访谈', '需求对接', '需求咨询', '需求反馈'],
        '项目推进': ['项目', '项目推进', '项目启动', '项目评审', '项目风险', '项目里程碑', '项目进度', '项目总结', '项目验收', '项目汇报', '项目协调', '项目任务'],
        'Bug处理': ['bug', 'bug处理', 'bug反馈', 'bug修复', 'bug验收', 'bug分配', 'bug协助', 'bug异议', 'bug优先级', '问题沟通', '问题反馈', '问题修复'],
        '客户对接': ['客户', '客户对接', '客户接待', '客户投诉', '客户异议', '客户跟进', '客户维护', '客户寒暄', '客户拜访', '客户沟通', '客户咨询', '客户服务']
    }
    
    test_messages = [
        "我需要向产品经理反馈一个需求变更的问题",
        "项目进度滞后了，我需要向团队催促进度",
        "发现了一个严重的Bug，需要反馈给后端开发",
        "客户对我们的价格有异议，我需要处理",
        "如何进行用户访谈，了解用户需求",
        "项目启动会应该怎么开场",
        "怎么向开发团队提交Bug",
        "初次接待客户应该怎么说",
        "客户提出需求变更，怎么沟通影响",
        "需要向领导汇报项目风险"
    ]
    
    for message in test_messages:
        message_lower = message.lower()
        detected_scene = None
        
        for scene, keywords in SCENE_KEYWORDS.items():
            for keyword in keywords:
                if keyword in message_lower:
                    detected_scene = scene
                    break
            if detected_scene:
                break
        
        print(f"   消息: '{message}'")
        print(f"   检测到场景: '{detected_scene}'")
        print()
    
    # 测试数据库中是否包含对应场景的话术
    print("3. 检查各场景的话术数量:")
    test_scenes = ['需求沟通', '项目推进', 'Bug处理', '客户对接']
    for scene in test_scenes:
        cursor.execute('SELECT COUNT(*) FROM scripts WHERE scene_type LIKE ?', (f'%{scene}%',))
        count = cursor.fetchone()[0]
        print(f"   '{scene}': {count}条")
    
    conn.close()

if __name__ == '__main__':
    debug_scenes()
