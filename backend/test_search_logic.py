import sqlite3

def test_search_logic():
    conn = sqlite3.connect('vibe_chat.db')
    cursor = conn.cursor()
    
    print("=" * 60)
    print("测试搜索逻辑")
    print("=" * 60)
    
    # 测试需求沟通场景的产品经理话术
    print("\n1. 测试需求沟通场景的产品经理话术:")
    cursor.execute('''
        SELECT s.id, s.title, s.scene_type, p.name 
        FROM scripts s
        JOIN positions p ON s.position_id = p.id
        WHERE p.name = '产品经理' 
        AND (s.scene_type LIKE '%需求%' OR s.content LIKE '%需求%')
        LIMIT 5
    ''')
    results = cursor.fetchall()
    print(f"   找到 {len(results)} 条话术")
    for r in results:
        print(f"   ID: {r[0]}, 标题: {r[1]}, 场景: {r[2]}, 岗位: {r[3]}")
    
    # 测试项目推进场景的项目经理话术
    print("\n2. 测试项目推进场景的项目经理话术:")
    cursor.execute('''
        SELECT s.id, s.title, s.scene_type, p.name 
        FROM scripts s
        JOIN positions p ON s.position_id = p.id
        WHERE p.name = '项目经理' 
        AND (s.scene_type LIKE '%项目%' OR s.content LIKE '%项目%')
        LIMIT 5
    ''')
    results = cursor.fetchall()
    print(f"   找到 {len(results)} 条话术")
    for r in results:
        print(f"   ID: {r[0]}, 标题: {r[1]}, 场景: {r[2]}, 岗位: {r[3]}")
    
    # 测试Bug处理场景的测试工程师话术
    print("\n3. 测试Bug处理场景的测试工程师话术:")
    cursor.execute('''
        SELECT s.id, s.title, s.scene_type, p.name 
        FROM scripts s
        JOIN positions p ON s.position_id = p.id
        WHERE p.name = '测试工程师' 
        AND (s.scene_type LIKE '%Bug%' OR s.content LIKE '%Bug%')
        LIMIT 5
    ''')
    results = cursor.fetchall()
    print(f"   找到 {len(results)} 条话术")
    for r in results:
        print(f"   ID: {r[0]}, 标题: {r[1]}, 场景: {r[2]}, 岗位: {r[3]}")
    
    # 测试客户对接场景的售前人员话术
    print("\n4. 测试客户对接场景的售前人员话术:")
    cursor.execute('''
        SELECT s.id, s.title, s.scene_type, p.name 
        FROM scripts s
        JOIN positions p ON s.position_id = p.id
        WHERE p.name = '售前人员' 
        AND (s.scene_type LIKE '%客户%' OR s.content LIKE '%客户%')
        LIMIT 5
    ''')
    results = cursor.fetchall()
    print(f"   找到 {len(results)} 条话术")
    for r in results:
        print(f"   ID: {r[0]}, 标题: {r[1]}, 场景: {r[2]}, 岗位: {r[3]}")
    
    conn.close()

if __name__ == '__main__':
    test_search_logic()
