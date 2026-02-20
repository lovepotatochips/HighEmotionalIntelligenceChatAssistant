-- 数据库初始化脚本
CREATE DATABASE IF NOT EXISTS vibe_chat CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE vibe_chat;

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID',
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希',
    phone VARCHAR(20) COMMENT '手机号',
    email VARCHAR(100) COMMENT '邮箱',
    role VARCHAR(20) NOT NULL DEFAULT 'user' COMMENT '角色:售前/项目经理/产品经理/前端开发/后端开发/UI设计师/测试工程师',
    avatar_url VARCHAR(255) COMMENT '头像URL',
    is_active TINYINT(1) DEFAULT 1 COMMENT '是否激活',
    is_vip TINYINT(1) DEFAULT 0 COMMENT '是否VIP用户',
    vip_expire_time DATETIME COMMENT 'VIP过期时间',
    tone_preference VARCHAR(20) DEFAULT '温和' COMMENT '语气偏好:温和/专业/强硬/活泼/委婉',
    length_preference VARCHAR(20) DEFAULT '简洁版' COMMENT '长度偏好:简洁版/详细版',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_username (username),
    INDEX idx_phone (phone),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- 岗位表
CREATE TABLE IF NOT EXISTS positions (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '岗位ID',
    name VARCHAR(50) NOT NULL COMMENT '岗位名称',
    code VARCHAR(20) NOT NULL UNIQUE COMMENT '岗位代码:pre_sales/project_manager/product_manager/frontend/backend/ui_designer/tester',
    description VARCHAR(200) COMMENT '岗位描述',
    sort_order INT DEFAULT 0 COMMENT '排序',
    is_active TINYINT(1) DEFAULT 1 COMMENT '是否启用',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='岗位表';

-- 话术分类表
CREATE TABLE IF NOT EXISTS script_categories (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '分类ID',
    name VARCHAR(50) NOT NULL COMMENT '分类名称',
    code VARCHAR(50) NOT NULL UNIQUE COMMENT '分类代码',
    parent_id INT DEFAULT 0 COMMENT '父分类ID',
    position_id INT COMMENT '关联岗位ID',
    description VARCHAR(200) COMMENT '分类描述',
    icon VARCHAR(100) COMMENT '图标',
    sort_order INT DEFAULT 0 COMMENT '排序',
    is_active TINYINT(1) DEFAULT 1 COMMENT '是否启用',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_position_id (position_id),
    INDEX idx_parent_id (parent_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='话术分类表';

-- 话术表
CREATE TABLE IF NOT EXISTS scripts (
    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '话术ID',
    title VARCHAR(100) NOT NULL COMMENT '话术标题',
    content TEXT NOT NULL COMMENT '话术内容',
    brief_content TEXT COMMENT '简洁版内容',
    category_id INT NOT NULL COMMENT '分类ID',
    position_id INT COMMENT '岗位ID',
    scene_type VARCHAR(50) NOT NULL COMMENT '场景类型:需求对接/项目推进/问题沟通/协同配合/对外衔接',
    tone VARCHAR(20) DEFAULT '温和' COMMENT '语气:温和/专业/强硬/活泼/委婉',
    target_audience VARCHAR(50) COMMENT '目标对象:客户/领导/同事/新人',
    tags VARCHAR(200) COMMENT '标签,逗号分隔',
    usage_count INT DEFAULT 0 COMMENT '使用次数',
    like_count INT DEFAULT 0 COMMENT '点赞次数',
    is_free TINYINT(1) DEFAULT 1 COMMENT '是否免费',
    is_active TINYINT(1) DEFAULT 1 COMMENT '是否启用',
    created_by BIGINT COMMENT '创建者ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_category_id (category_id),
    INDEX idx_position_id (position_id),
    INDEX idx_scene_type (scene_type),
    INDEX idx_tags (tags(100)),
    FULLTEXT idx_content (title, content)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='话术表';

-- 用户收藏表
CREATE TABLE IF NOT EXISTS user_favorites (
    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '收藏ID',
    user_id BIGINT NOT NULL COMMENT '用户ID',
    script_id BIGINT NOT NULL COMMENT '话术ID',
    custom_content TEXT COMMENT '自定义话术内容',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    UNIQUE KEY uk_user_script (user_id, script_id),
    INDEX idx_user_id (user_id),
    INDEX idx_script_id (script_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户收藏表';

-- 对话记录表
CREATE TABLE IF NOT EXISTS conversations (
    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '对话ID',
    user_id BIGINT NOT NULL COMMENT '用户ID',
    session_id VARCHAR(64) NOT NULL COMMENT '会话ID',
    message_type VARCHAR(20) NOT NULL COMMENT '消息类型:user/assistant',
    content TEXT NOT NULL COMMENT '消息内容',
    context_data JSON COMMENT '上下文数据',
    intent VARCHAR(50) COMMENT '意图识别',
    referenced_script_id BIGINT COMMENT '关联话术ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_user_id (user_id),
    INDEX idx_session_id (session_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='对话记录表';

-- 话术调整记录表
CREATE TABLE IF NOT EXISTS script_adjustments (
    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '调整记录ID',
    user_id BIGINT NOT NULL COMMENT '用户ID',
    script_id BIGINT NOT NULL COMMENT '话术ID',
    original_content TEXT COMMENT '原始内容',
    adjusted_content TEXT COMMENT '调整后内容',
    tone VARCHAR(20) COMMENT '语气',
    length_type VARCHAR(20) COMMENT '长度类型:简洁版/详细版',
    feedback VARCHAR(200) COMMENT '用户反馈',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_user_id (user_id),
    INDEX idx_script_id (script_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='话术调整记录表';

-- 系统配置表
CREATE TABLE IF NOT EXISTS system_configs (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '配置ID',
    config_key VARCHAR(100) NOT NULL UNIQUE COMMENT '配置键',
    config_value TEXT COMMENT '配置值',
    description VARCHAR(200) COMMENT '配置描述',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统配置表';

-- 插入初始数据

-- 插入岗位数据
INSERT INTO positions (name, code, description, sort_order) VALUES
('售前人员', 'pre_sales', '负责客户对接、需求咨询、方案讲解', 1),
('项目经理', 'project_manager', '负责项目统筹、进度管理、团队协调', 2),
('产品经理', 'product_manager', '负责需求沟通、产品规划、需求变更', 3),
('前端开发', 'frontend', '负责前端开发、技术对接、UI实现', 4),
('后端开发', 'backend', '负责后端开发、接口设计、数据库设计', 5),
('UI设计师', 'ui_designer', '负责界面设计、交互设计、设计交付', 6),
('测试工程师', 'tester', '负责测试、bug反馈、质量保障', 7);

-- 插入话术分类数据
INSERT INTO script_categories (name, code, parent_id, position_id, description, sort_order) VALUES
-- 售前专属分类
('客户对接', 'pre_sales_customer', 0, 1, '售前人员客户对接相关话术', 1),
('需求咨询', 'pre_sales_consultation', 1, 1, '需求咨询话术', 2),
('方案讲解', 'pre_sales_presentation', 1, 1, '方案讲解话术', 3),
('异议处理', 'pre_sales_objection', 1, 1, '异议处理话术', 4),
('合同洽谈', 'pre_sales_contract', 1, 1, '合同洽谈话术', 5),
-- 项目经理专属分类
('项目统筹', 'pm_coordination', 0, 2, '项目经理项目统筹相关话术', 6),
('任务分配', 'pm_task', 6, 2, '任务分配话术', 7),
('进度同步', 'pm_progress', 6, 2, '进度同步话术', 8),
('风险同步', 'pm_risk', 6, 2, '风险同步话术', 9),
('向上汇报', 'pm_report_up', 6, 2, '向上汇报话术', 10),
-- 产品经理专属分类
('需求沟通', 'pm_requirement', 0, 3, '产品经理需求沟通相关话术', 11),
('需求传递', 'pm_transfer', 11, 3, '需求传递话术', 12),
('需求变更', 'pm_change', 11, 3, '需求变更话术', 13),
('需求答疑', 'pm_qa', 11, 3, '需求答疑话术', 14),
-- 前端开发专属分类
('前端技术对接', 'frontend_tech', 0, 4, '前端开发技术对接相关话术', 15),
('需求确认', 'frontend_requirement', 15, 4, '需求确认话术', 16),
('接口联调', 'frontend_api', 15, 4, '接口联调话术', 17),
('Bug处理', 'frontend_bug', 15, 4, 'Bug处理话术', 18),
-- 后端开发专属分类
('后端技术沟通', 'backend_tech', 0, 5, '后端开发技术沟通相关话术', 19),
('接口设计', 'backend_api', 19, 5, '接口设计话术', 20),
('数据库沟通', 'backend_db', 19, 5, '数据库沟通话术', 21),
('Bug处理', 'backend_bug', 19, 5, 'Bug处理话术', 22),
-- UI设计师专属分类
('UI需求对接', 'ui_requirement', 0, 6, 'UI设计师需求对接相关话术', 23),
('设计沟通', 'ui_design', 23, 6, '设计沟通话术', 24),
('设计交付', 'ui_delivery', 23, 6, '设计交付话术', 25),
-- 测试工程师专属分类
('测试沟通', 'tester_communication', 0, 7, '测试工程师沟通相关话术', 26),
('Bug反馈', 'tester_bug', 26, 7, 'Bug反馈话术', 27),
('测试异议', 'tester_objection', 26, 7, '测试异议处理话术', 28),
-- 通用分类
('日常协作', 'daily_collaboration', 0, NULL, '日常协作通用话术', 29),
('会议沟通', 'meeting', 0, NULL, '会议沟通通用话术', 30),
('职场礼仪', 'workplace_etiquette', 0, NULL, '职场礼仪通用话术', 31);

-- 插入初始话术数据（示例）
INSERT INTO scripts (title, content, brief_content, category_id, position_id, scene_type, tone, target_audience, tags, is_free) VALUES
-- 售前话术示例
('客户需求初步了解', '您好！非常感谢您对我们产品的关注。为了更好地为您提供服务，想先了解一下您的具体需求和期望，方便吗？', '您好！感谢关注，想了解一下您的具体需求。', 2, 1, '需求对接', '温和', '客户', '需求咨询,初步沟通', 1),
('方案讲解开场', '根据刚才沟通的需求，我为您准备了一个解决方案，主要包含以下几个核心模块...', '根据您的需求，我准备了一个解决方案，包含以下核心模块...', 3, 1, '需求对接', '专业', '客户', '方案讲解,开场', 1),
('价格异议处理', '我非常理解您对价格的顾虑。其实我们的定价是综合考虑了产品质量、服务保障和长期价值。如果您有预算限制，我们也可以探讨一些灵活的合作方案。', '理解您的顾虑，定价考虑了质量和价值，有灵活方案可选。', 4, 1, '需求对接', '委婉', '客户', '异议处理,价格', 1),
-- 项目经理话术示例
('任务分配提醒', '【温馨提醒】各位好，新一周的任务分配已更新，请查看附件。如果有任何疑问或需要支持，随时联系我，我们一起来协调。', '各位好，新任务已分配，有问题随时联系我。', 7, 2, '项目推进', '温和', '同事', '任务分配,提醒', 1),
('进度滞后沟通', '看到这个任务的进度有些滞后，我想了解一下遇到了什么困难吗？需要我协调什么资源来支持？', '进度有些滞后，遇到了什么困难吗？需要什么支持？', 8, 2, '项目推进', '委婉', '同事', '进度,滞后', 1),
('向上汇报项目风险', '领导，目前项目整体推进正常，但有一个风险点需要同步给您：[具体风险]。我们已经制定了应对方案，会密切跟进。', '领导，项目正常，有个风险点需要同步：[具体风险]，已有应对方案。', 10, 2, '项目推进', '专业', '领导', '风险,汇报', 1),
-- 产品经理话术示例
('需求传递给研发', '各位，这是本周新增的需求，主要涉及[模块/功能]。需求文档已发群里，如果有疑问或者不清楚的地方，随时沟通哈。', '各位，新增需求涉及[模块/功能]，文档已发，有疑问随时沟通。', 12, 3, '需求对接', '温和', '同事', '需求传递,研发', 1),
('需求变更说明', '由于[变更原因]，我们需要对[需求名称]做一些调整。主要变更是[具体变更]，给大家带来的不便先说声抱歉，我们一起配合完成。', '由于[原因]，需要对[需求]做调整，主要变更是[具体]，抱歉麻烦大家。', 13, 3, '需求对接', '委婉', '同事', '需求变更,说明', 1),
-- 前端开发话术示例
('与产品确认需求细节', '关于[功能名称]的交互细节，我有几个问题想确认一下：[具体问题]。这样可以避免后续返工，谢谢！', '关于[功能]的交互细节，有几个问题想确认：[问题]，避免返工。', 16, 4, '问题沟通', '专业', '同事', '需求确认,细节', 1),
('与后端接口联调沟通', '关于[接口名称]的接口，前端已经准备好了，什么时候方便联调一下？我这边随时可以配合。', '关于[接口]，前端已准备好，什么时候方便联调？随时配合。', 17, 4, '问题沟通', '温和', '同事', '接口,联调', 1),
('Bug异议处理', '关于这个Bug，我仔细检查了一下，可能存在一些理解偏差。具体情况是[说明]，我们是不是可以一起确认一下？', '关于这个Bug，检查后发现可能存在理解偏差，具体情况是[说明]，一起确认下？', 18, 4, '问题沟通', '委婉', '同事', 'Bug,异议', 1),
-- 后端开发话术示例
('接口问题沟通', '前端同事，关于[接口名称]这个接口，我发现可能存在一些问题：[具体问题]。建议我们尽快排查一下，避免影响后续开发。', '关于[接口]，发现一些问题：[问题]，建议尽快排查。', 20, 5, '问题沟通', '专业', '同事', '接口,问题', 1),
('需求可行性沟通', '关于[需求名称]，从技术实现角度来看，可能存在一些挑战：[具体挑战]。我们可以探讨一下替代方案，看看能否达到类似效果。', '关于[需求]，从技术角度看有挑战：[挑战]，可以探讨替代方案。', NULL, 5, '需求对接', '专业', '同事', '需求,可行性', 1),
-- UI设计师话术示例
('设计修改沟通', '收到反馈意见了。关于[修改点]，我理解是要[具体要求]。我这边会尽快调整，大概[时间]可以出修改稿。', '收到反馈，关于[修改点]，理解是要[要求]，尽快调整，[时间]出修改稿。', 24, 6, '问题沟通', '温和', '同事', '设计,修改', 1),
('设计交付说明', '各位，这是[项目名称]的UI设计稿，包含[页面数量]个页面。设计规范已同步，如果有疑问随时沟通哈。', '各位，这是[项目]的UI设计稿，包含[数量]个页面，规范已同步。', 25, 6, '需求对接', '温和', '同事', '设计,交付', 1),
-- 测试工程师话术示例
('Bug反馈话术', '在[测试场景]中发现了一个Bug，描述如下：[Bug描述]。已录屏/截图保存，请查收。', '在[场景]中发现Bug：[描述]，已录屏/截图保存。', 27, 7, '问题沟通', '专业', '同事', 'Bug,反馈', 1),
('测试异议处理', '关于这个Bug的优先级，我理解您的观点。不过从用户角度来看，这个问题可能会影响[影响范围]，所以建议优先处理。', '关于Bug优先级，理解您的观点。但从用户角度，会影响[范围]，建议优先处理。', 28, 7, '问题沟通', '委婉', '同事', 'Bug,异议', 1),
-- 通用协作话术
('请教问题', '你好，关于[问题主题]，想请教一下你，方便吗？', '你好，关于[问题]，想请教一下，方便吗？', 29, NULL, '协同配合', '温和', '同事', '请教,问题', 1),
('感谢帮忙', '非常感谢你刚才的帮助，省了我不少时间，下次有机会请你喝咖啡！', '非常感谢你的帮助，省了我不少时间，下次请你喝咖啡！', 29, NULL, '协同配合', '活泼', '同事', '感谢,帮忙', 1),
('拒绝不合理请求', '我理解你的需求，不过目前手头有几个紧急任务要处理，可能暂时无法配合。等这周忙完，如果还需要的话可以再联系我。', '理解你的需求，但手头有紧急任务，暂时无法配合，忙完再联系。', 29, NULL, '协同配合', '委婉', '同事', '拒绝,请求', 1),
('会议开场', '各位好，今天的会议主要讨论[会议主题]。首先我简单介绍一下背景...', '各位好，今天主要讨论[主题]，先介绍一下背景...', 30, NULL, '会议沟通', '专业', '同事', '会议,开场', 1),
('会议总结', '好，今天的会议就到这里。总结一下：1. [要点1] 2. [要点2] 3. [要点3]。散会！', '会议总结：1. [要点1] 2. [要点2] 3. [要点3]。散会！', 30, NULL, '会议沟通', '专业', '同事', '会议,总结', 1);

-- 插入系统配置
INSERT INTO system_configs (config_key, config_value, description) VALUES
('app_name', 'VibeCoding高情商聊天助手', '应用名称'),
('default_tone', '温和', '默认语气'),
('default_length', '简洁版', '默认长度'),
('max_context_turns', '10', '最大上下文轮次'),
('response_timeout', '2', '响应超时时间(秒)');
