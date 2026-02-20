import sqlite3

def check_scripts():
    conn = sqlite3.connect('vibe_chat.db')
    cursor = conn.cursor()
    
    print("=" * 60)
    print("检查话术数据库分布")
    print("=" * 60)
    
    # 检查岗位分布
    print("\n1. 按岗位分布:")
    cursor.execute('''
        SELECT p.name, COUNT(s.id) as count
        FROM positions p
        LEFT JOIN scripts s ON p.id = s.position_id
        GROUP BY p.id, p.name
        ORDER BY count DESC
    ''')
    for row in cursor.fetchall():
        print(f"   {row[0]}: {row[1]}条")
    
    # 检查场景类型分布
    print("\n2. 按场景类型分布:")
    cursor.execute('''
        SELECT scene_type, COUNT(*) as count
        FROM scripts
        GROUP BY scene_type
        ORDER BY count DESC
    ''')
    for row in cursor.fetchall():
        print(f"   {row[0]}: {row[1]}条")
    
    # 检查具体的话术内容
    print("\n3. 需求沟通相关话术示例:")
    cursor.execute('''
        SELECT s.title, s.content, p.name, s.scene_type
        FROM scripts s
        JOIN positions p ON s.position_id = p.id
        WHERE s.scene_type LIKE '%需求%' OR s.content LIKE '%需求%'
        LIMIT 5
    ''')
    for row in cursor.fetchall():
        print(f"   标题: {row[0]}")
        print(f"   岗位: {row[2]}")
        print(f"   场景: {row[3]}")
        print(f"   内容: {row[1][:50]}...")
        print()
    
    print("\n4. 项目推进相关话术示例:")
    cursor.execute('''
        SELECT s.title, s.content, p.name, s.scene_type
        FROM scripts s
        JOIN positions p ON s.position_id = p.id
        WHERE s.scene_type LIKE '%项目%' OR s.content LIKE '%项目%'
        LIMIT 5
    ''')
    for row in cursor.fetchall():
        print(f"   标题: {row[0]}")
        print(f"   岗位: {row[2]}")
        print(f"   场景: {row[3]}")
        print(f"   内容: {row[1][:50]}...")
        print()
    
    print("\n5. Bug处理相关话术示例:")
    cursor.execute('''
        SELECT s.title, s.content, p.name, s.scene_type
        FROM scripts s
        JOIN positions p ON s.position_id = p.id
        WHERE s.scene_type LIKE '%Bug%' OR s.content LIKE '%Bug%'
        LIMIT 5
    ''')
    for row in cursor.fetchall():
        print(f"   标题: {row[0]}")
        print(f"   岗位: {row[2]}")
        print(f"   场景: {row[3]}")
        print(f"   内容: {row[1][:50]}...")
        print()
    
    print("\n6. 客户对接相关话术示例:")
    cursor.execute('''
        SELECT s.title, s.content, p.name, s.scene_type
        FROM scripts s
        JOIN positions p ON s.position_id = p.id
        WHERE s.scene_type LIKE '%客户%' OR s.content LIKE '%客户%'
        LIMIT 5
    ''')
    for row in cursor.fetchall():
        print(f"   标题: {row[0]}")
        print(f"   岗位: {row[2]}")
        print(f"   场景: {row[3]}")
        print(f"   内容: {row[1][:50]}...")
        print()
    
    print("=" * 60)
    
    conn.close()

if __name__ == '__main__':
    check_scripts()
