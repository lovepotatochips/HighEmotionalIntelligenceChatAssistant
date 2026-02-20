import sqlite3

def debug_positions():
    conn = sqlite3.connect('vibe_chat.db')
    cursor = conn.cursor()
    
    print("=" * 60)
    print("检查岗位数据和匹配逻辑")
    print("=" * 60)
    
    # 检查positions表
    print("\n1. Positions表数据:")
    cursor.execute('SELECT * FROM positions')
    positions = cursor.fetchall()
    for pos in positions:
        print(f"   ID: {pos[0]}, Name: {pos[1]}, Code: {pos[2]}")
    
    # 检查scripts表中的position_id
    print("\n2. Scripts表position_id分布:")
    cursor.execute('''
        SELECT position_id, COUNT(*) as count
        FROM scripts
        GROUP BY position_id
        ORDER BY position_id
    ''')
    for row in cursor.fetchall():
        print(f"   position_id {row[0]}: {row[1]}条")
    
    # 测试岗位匹配逻辑
    print("\n3. 测试岗位匹配:")
    
    test_inputs = [
        "产品经理",
        "项目经理", 
        "售前人员",
        "前端开发",
        "后端开发",
        "UI设计师",
        "测试工程师"
    ]
    
    POSITION_KEYWORDS = {
        '售前人员': ['售前', '销售', '客户', 'pre_sales'],
        '项目经理': ['项目经理', 'pm', '项目', '统筹', 'project_manager'],
        '产品经理': ['产品', 'pm', '需求', 'product_manager'],
        '前端开发': ['前端', '前端开发', 'vue', 'react', 'frontend', '界面', '页面'],
        '后端开发': ['后端', '后端开发', '接口', 'api', 'backend', '数据库', '服务端'],
        'UI设计师': ['ui', '设计', '界面', '设计师', 'ui_designer', '交互', '视觉'],
        '测试工程师': ['测试', 'qa', 'bug', '测试工程师', 'tester', '质量']
    }
    
    for input_str in test_inputs:
        input_lower = input_str.lower()
        matched_position = None
        
        for position, keywords in POSITION_KEYWORDS.items():
            for keyword in keywords:
                if keyword in input_lower:
                    matched_position = position
                    break
            if matched_position:
                break
        
        print(f"   输入: '{input_str}' -> 匹配到: '{matched_position}'")
    
    # 检查直接匹配
    print("\n4. 检查直接岗位匹配:")
    for input_str in test_inputs:
        cursor.execute('SELECT id, name FROM positions WHERE name = ?', (input_str,))
        result = cursor.fetchone()
        if result:
            print(f"   '{input_str}' -> ID: {result[0]}, Name: {result[1]}")
        else:
            print(f"   '{input_str}' -> 未找到")
    
    conn.close()

if __name__ == '__main__':
    debug_positions()
