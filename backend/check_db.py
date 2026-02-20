import sqlite3

def check_database():
    conn = sqlite3.connect('vibe_chat.db')
    cursor = conn.cursor()
    
    print("=== 检查表结构 ===")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"表数量: {len(tables)}")
    for table in tables:
        print(f"表名: {table[0]}")
    
    print("\n=== 检查users表结构 ===")
    cursor.execute("PRAGMA table_info(users)")
    columns = cursor.fetchall()
    print(f"字段数量: {len(columns)}")
    for col in columns:
        print(f"字段: {col[1]}, 类型: {col[2]}, 是否为空: {col[3]}, 默认值: {col[4]}, 主键: {col[5]}")
    
    print("\n=== 检查现有用户 ===")
    cursor.execute("SELECT id, username, role, is_active FROM users")
    users = cursor.fetchall()
    print(f"用户数量: {len(users)}")
    for user in users:
        print(f"ID: {user[0]}, 用户名: {user[1]}, 角色: {user[2]}, 激活: {user[3]}")
    
    conn.close()

if __name__ == "__main__":
    check_database()
