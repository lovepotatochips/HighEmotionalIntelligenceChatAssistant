import sqlite3
from datetime import datetime

def fix_database():
    conn = sqlite3.connect('vibe_chat.db')
    cursor = conn.cursor()
    
    print("=== 删除所有表 ===")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    for table in tables:
        if table[0] != 'sqlite_sequence':
            print(f"删除表: {table[0]}")
            cursor.execute(f"DROP TABLE IF EXISTS {table[0]}")
    
    print("\n=== 创建users表 ===")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            role TEXT NOT NULL DEFAULT 'user',
            avatar_url TEXT,
            is_active INTEGER DEFAULT 1,
            is_vip INTEGER DEFAULT 0,
            vip_expire_time TEXT,
            tone_preference TEXT DEFAULT '温和',
            length_preference TEXT DEFAULT '简洁版',
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now'))
        )
    ''')
    print("users表创建成功")
    
    print("\n=== 创建positions表 ===")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            code TEXT NOT NULL UNIQUE,
            description TEXT,
            sort_order INTEGER DEFAULT 0,
            is_active INTEGER DEFAULT 1,
            created_at TEXT DEFAULT (datetime('now'))
        )
    ''')
    print("positions表创建成功")
    
    print("\n=== 创建script_categories表 ===")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS script_categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            code TEXT NOT NULL UNIQUE,
            parent_id INTEGER DEFAULT 0,
            position_id INTEGER,
            description TEXT,
            icon TEXT,
            sort_order INTEGER DEFAULT 0,
            is_active INTEGER DEFAULT 1,
            created_at TEXT DEFAULT (datetime('now'))
        )
    ''')
    print("script_categories表创建成功")
    
    print("\n=== 创建scripts表 ===")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scripts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            brief_content TEXT,
            category_id INTEGER NOT NULL,
            position_id INTEGER,
            scene_type TEXT NOT NULL,
            tone TEXT DEFAULT '温和',
            target_audience TEXT,
            tags TEXT,
            usage_count INTEGER DEFAULT 0,
            like_count INTEGER DEFAULT 0,
            is_free INTEGER DEFAULT 1,
            is_active INTEGER DEFAULT 1,
            created_by INTEGER,
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now'))
        )
    ''')
    print("scripts表创建成功")
    
    print("\n=== 创建user_favorites表 ===")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            script_id INTEGER NOT NULL,
            custom_content TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            UNIQUE(user_id, script_id)
        )
    ''')
    print("user_favorites表创建成功")
    
    print("\n=== 创建conversations表 ===")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            session_id TEXT NOT NULL,
            message_type TEXT NOT NULL,
            content TEXT NOT NULL,
            context_data TEXT,
            intent TEXT,
            referenced_script_id INTEGER,
            created_at TEXT DEFAULT (datetime('now'))
        )
    ''')
    print("conversations表创建成功")
    
    print("\n=== 创建script_adjustments表 ===")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS script_adjustments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            script_id INTEGER NOT NULL,
            original_content TEXT,
            adjusted_content TEXT,
            tone TEXT,
            length_type TEXT,
            feedback TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        )
    ''')
    print("script_adjustments表创建成功")
    
    print("\n=== 创建system_configs表 ===")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_configs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            config_key TEXT NOT NULL UNIQUE,
            config_value TEXT,
            description TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now'))
        )
    ''')
    print("system_configs表创建成功")
    
    print("\n=== 插入初始数据 ===")
    
    positions = [
        ('售前人员', 'pre_sales', '负责客户对接、需求咨询、方案讲解', 1),
        ('项目经理', 'project_manager', '负责项目统筹、进度管理、团队协调', 2),
        ('产品经理', 'product_manager', '负责需求沟通、产品规划、需求变更', 3),
        ('前端开发', 'frontend', '负责前端开发、技术对接、UI实现', 4),
        ('后端开发', 'backend', '负责后端开发、接口设计、数据库设计', 5),
        ('UI设计师', 'ui_designer', '负责界面设计、交互设计、设计交付', 6),
        ('测试工程师', 'tester', '负责测试、bug反馈、质量保障', 7),
    ]
    cursor.executemany('INSERT OR IGNORE INTO positions (name, code, description, sort_order) VALUES (?, ?, ?, ?)', positions)
    print(f"插入{len(positions)}个岗位")
    
    categories = [
        ('客户对接', 'pre_sales_customer', 0, 1, '售前人员客户对接相关话术', 1),
        ('需求咨询', 'pre_sales_consultation', 1, 1, '需求咨询话术', 2),
        ('方案讲解', 'pre_sales_presentation', 1, 1, '方案讲解话术', 3),
        ('异议处理', 'pre_sales_objection', 1, 1, '异议处理话术', 4),
        ('合同洽谈', 'pre_sales_contract', 1, 1, '合同洽谈话术', 5),
        ('项目统筹', 'pm_coordination', 0, 2, '项目经理项目统筹相关话术', 6),
        ('任务分配', 'pm_task', 6, 2, '任务分配话术', 7),
        ('进度同步', 'pm_progress', 6, 2, '进度同步话术', 8),
        ('风险同步', 'pm_risk', 6, 2, '风险同步话术', 9),
        ('向上汇报', 'pm_report_up', 6, 2, '向上汇报话术', 10),
        ('需求沟通', 'pm_requirement', 0, 3, '产品经理需求沟通相关话术', 11),
        ('需求传递', 'pm_transfer', 11, 3, '需求传递话术', 12),
        ('需求变更', 'pm_change', 11, 3, '需求变更话术', 13),
        ('需求答疑', 'pm_qa', 11, 3, '需求答疑话术', 14),
        ('前端技术对接', 'frontend_tech', 0, 4, '前端开发技术对接相关话术', 15),
        ('需求确认', 'frontend_requirement', 15, 4, '需求确认话术', 16),
        ('接口联调', 'frontend_api', 15, 4, '接口联调话术', 17),
        ('Bug处理', 'frontend_bug', 15, 4, 'Bug处理话术', 18),
        ('后端技术沟通', 'backend_tech', 0, 5, '后端开发技术沟通相关话术', 19),
        ('接口设计', 'backend_api', 19, 5, '接口设计话术', 20),
        ('数据库沟通', 'backend_db', 19, 5, '数据库沟通话术', 21),
        ('Bug处理', 'backend_bug', 19, 5, 'Bug处理话术', 22),
        ('UI需求对接', 'ui_requirement', 0, 6, 'UI设计师需求对接相关话术', 23),
        ('设计沟通', 'ui_design', 23, 6, '设计沟通话术', 24),
        ('设计交付', 'ui_delivery', 23, 6, '设计交付话术', 25),
        ('测试沟通', 'tester_communication', 0, 7, '测试工程师沟通相关话术', 26),
        ('Bug反馈', 'tester_bug', 26, 7, 'Bug反馈话术', 27),
        ('测试异议', 'tester_objection', 26, 7, '测试异议处理话术', 28),
        ('日常协作', 'daily_collaboration', 0, None, '日常协作通用话术', 29),
        ('会议沟通', 'meeting', 0, None, '会议沟通通用话术', 30),
        ('职场礼仪', 'workplace_etiquette', 0, None, '职场礼仪通用话术', 31),
    ]
    cursor.executemany('INSERT OR IGNORE INTO script_categories (name, code, parent_id, position_id, description, sort_order) VALUES (?, ?, ?, ?, ?, ?)', categories)
    print(f"插入{len(categories)}个分类")
    
    scripts = [
        ('客户需求初步了解', '您好！非常感谢您对我们产品的关注。为了更好地为您提供服务，想先了解一下您的具体需求和期望，方便吗？', '您好！感谢关注，想了解一下您的具体需求。', 2, 1, '需求对接', '温和', '客户', '需求咨询,初步沟通', 1),
        ('方案讲解开场', '根据刚才沟通的需求，我为您准备了一个解决方案，主要包含以下几个核心模块...', '根据您的需求，我准备了一个解决方案，包含以下核心模块...', 3, 1, '需求对接', '专业', '客户', '方案讲解,开场', 1),
        ('价格异议处理', '我非常理解您对价格的顾虑。其实我们的定价是综合考虑了产品质量、服务保障和长期价值。如果您有预算限制，我们也可以探讨一些灵活的合作方案。', '理解您的顾虑，定价考虑了质量和价值，有灵活方案可选。', 4, 1, '需求对接', '委婉', '客户', '异议处理,价格', 1),
        ('任务分配提醒', '【温馨提醒】各位好，新一周的任务分配已更新，请查看附件。如果有任何疑问或需要支持，随时联系我，我们一起来协调。', '各位好，新任务已分配，有问题随时联系我。', 7, 2, '项目推进', '温和', '同事', '任务分配,提醒', 1),
        ('进度滞后沟通', '看到这个任务的进度有些滞后，我想了解一下遇到了什么困难吗？需要我协调什么资源来支持？', '进度有些滞后，遇到了什么困难吗？需要什么支持？', 8, 2, '项目推进', '委婉', '同事', '进度,滞后', 1),
        ('向上汇报项目风险', '领导，目前项目整体推进正常，但有一个风险点需要同步给您：[具体风险]。我们已经制定了应对方案，会密切跟进。', '领导，项目正常，有个风险点需要同步：[具体风险]，已有应对方案。', 10, 2, '项目推进', '专业', '领导', '风险,汇报', 1),
        ('需求传递给研发', '各位，这是本周新增的需求，主要涉及[模块/功能]。需求文档已发群里，如果有疑问或者不清楚的地方，随时沟通哈。', '各位，新增需求涉及[模块/功能]，文档已发，有疑问随时沟通。', 12, 3, '需求对接', '温和', '同事', '需求传递,研发', 1),
        ('需求变更说明', '由于[变更原因]，我们需要对[需求名称]做一些调整。主要变更是[具体变更]，给大家带来的不便先说声抱歉，我们一起配合完成。', '由于[原因]，需要对[需求]做调整，主要变更是[具体]，抱歉麻烦大家。', 13, 3, '需求对接', '委婉', '同事', '需求变更,说明', 1),
        ('与产品确认需求细节', '关于[功能名称]的交互细节，我有几个问题想确认一下：[具体问题]。这样可以避免后续返工，谢谢！', '关于[功能]的交互细节，有几个问题想确认：[问题]，避免返工。', 16, 4, '问题沟通', '专业', '同事', '需求确认,细节', 1),
        ('与后端接口联调沟通', '关于[接口名称]的接口，前端已经准备好了，什么时候方便联调一下？我这边随时可以配合。', '关于[接口]，前端已准备好，什么时候方便联调？随时配合。', 17, 4, '问题沟通', '温和', '同事', '接口,联调', 1),
        ('Bug异议处理', '关于这个Bug，我仔细检查了一下，可能存在一些理解偏差。具体情况是[说明]，我们是不是可以一起确认一下？', '关于这个Bug，检查后发现可能存在理解偏差，具体情况是[说明]，一起确认下？', 18, 4, '问题沟通', '委婉', '同事', 'Bug,异议', 1),
        ('接口问题沟通', '前端同事，关于[接口名称]这个接口，我发现可能存在一些问题：[具体问题]。建议我们尽快排查一下，避免影响后续开发。', '关于[接口]，发现一些问题：[问题]，建议尽快排查。', 20, 5, '问题沟通', '专业', '同事', '接口,问题', 1),
        ('需求可行性沟通', '关于[需求名称]，从技术实现角度来看，可能存在一些挑战：[具体挑战]。我们可以探讨一下替代方案，看看能否达到类似效果。', '关于[需求]，从技术角度看有挑战：[挑战]，可以探讨替代方案。', 19, 5, '需求对接', '专业', '同事', '需求,可行性', 1),
        ('设计修改沟通', '收到反馈意见了。关于[修改点]，我理解是要[具体要求]。我这边会尽快调整，大概[时间]可以出修改稿。', '收到反馈，关于[修改点]，理解是要[要求]，尽快调整，[时间]出修改稿。', 24, 6, '问题沟通', '温和', '同事', '设计,修改', 1),
        ('设计交付说明', '各位，这是[项目名称]的UI设计稿，包含[页面数量]个页面。设计规范已同步，如果有疑问随时沟通哈。', '各位，这是[项目]的UI设计稿，包含[数量]个页面，规范已同步。', 25, 6, '需求对接', '温和', '同事', '设计,交付', 1),
        ('Bug反馈话术', '在[测试场景]中发现了一个Bug，描述如下：[Bug描述]。已录屏/截图保存，请查收。', '在[场景]中发现Bug：[描述]，已录屏/截图保存。', 27, 7, '问题沟通', '专业', '同事', 'Bug,反馈', 1),
        ('测试异议处理', '关于这个Bug的优先级，我理解您的观点。不过从用户角度来看，这个问题可能会影响[影响范围]，所以建议优先处理。', '关于Bug优先级，理解您的观点。但从用户角度，会影响[范围]，建议优先处理。', 28, 7, '问题沟通', '委婉', '同事', 'Bug,异议', 1),
        ('请教问题', '你好，关于[问题主题]，想请教一下你，方便吗？', '你好，关于[问题]，想请教一下，方便吗？', 29, 1, '协同配合', '温和', '同事', '请教,问题', 1),
        ('感谢帮忙', '非常感谢你刚才的帮助，省了我不少时间，下次有机会请你喝咖啡！', '非常感谢你的帮助，省了我不少时间，下次请你喝咖啡！', 29, 1, '协同配合', '活泼', '同事', '感谢,帮忙', 1),
        ('拒绝不合理请求', '我理解你的需求，不过目前手头有几个紧急任务要处理，可能暂时无法配合。等这周忙完，如果还需要的话可以再联系我。', '理解你的需求，但手头有紧急任务，暂时无法配合，忙完再联系。', 29, 1, '协同配合', '委婉', '同事', '拒绝,请求', 1),
        ('会议开场', '各位好，今天的会议主要讨论[会议主题]。首先我简单介绍一下背景...', '各位好，今天主要讨论[主题]，先介绍一下背景...', 30, 2, '会议沟通', '专业', '同事', '会议,开场', 1),
        ('会议总结', '好，今天的会议就到这里。总结一下：1. [要点1] 2. [要点2] 3. [要点3]。散会！', '会议总结：1. [要点1] 2. [要点2] 3. [要点3]。散会！', 30, 2, '会议沟通', '专业', '同事', '会议,总结', 1),
    ]
    cursor.executemany('''
        INSERT INTO scripts (title, content, brief_content, category_id, position_id, scene_type, tone, target_audience, tags, is_free)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', scripts)
    print(f"插入{len(scripts)}条话术")
    
    configs = [
        ('app_name', '高情商聊天助手', '应用名称'),
        ('default_tone', '温和', '默认语气'),
        ('default_length', '简洁版', '默认长度'),
        ('max_context_turns', '10', '最大上下文轮次'),
        ('response_timeout', '2', '响应超时时间(秒)'),
    ]
    cursor.executemany('INSERT OR IGNORE INTO system_configs (config_key, config_value, description) VALUES (?, ?, ?)', configs)
    print(f"插入{len(configs)}个配置")
    
    conn.commit()
    
    print("\n=== 验证表结构 ===")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"总表数: {len(tables)}")
    for table in tables:
        print(f"  - {table[0]}")
    
    print("\n=== 验证users表 ===")
    cursor.execute("PRAGMA table_info(users)")
    columns = cursor.fetchall()
    print(f"users表字段数: {len(columns)}")
    for col in columns:
        print(f"  - {col[1]}: {col[2]}")
    
    print("\n=== 数据库修复完成！===")
    conn.close()

if __name__ == '__main__':
    fix_database()
