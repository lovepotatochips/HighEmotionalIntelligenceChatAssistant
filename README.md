# VibeCoding高情商聊天助手

专为研发团队打造的高情商聊天话术助手，通过AI智能对话帮助团队成员高效沟通。

## 项目简介

高情商聊天助手是一款专为移动端软件研发项目团队打造的智能话术助手应用，聚焦研发全岗位沟通场景，通过AI智能对话和岗位专属话术库，帮助团队成员提升沟通效率和职场情商。

### 核心特性
- **AI智能对话**：基于自然语言理解的智能对话系统，自动识别场景和意图
- **岗位专属话术**：针对7类研发岗位提供专业化的沟通话术库
- **多维度搜索**：支持关键词、岗位、语气、场景等多维度话术检索
- **话术调整**：支持语气和长度的灵活调整（温和/专业/委婉/活泼，简洁版/详细版）
- **个性化收藏**：收藏常用话术，支持自定义修改
- **对话历史**：保存对话记录，方便回溯和学习

## 技术栈

### 后端
- **Python 3.8+**：核心开发语言
- **FastAPI**：高性能异步Web框架
- **SQLAlchemy 2.0**：ORM数据库操作框架
- **Pydantic 2.x**：数据验证和序列化
- **Pydantic Settings**：配置管理
- **PyMySQL**：MySQL数据库驱动
- **Python-Jose**：JWT令牌认证
- **PassLib + Bcrypt**：密码加密
- **Uvicorn**：ASGI服务器

### 前端
- **Vue 3**：渐进式JavaScript框架
- **Element Plus**：基于Vue 3的UI组件库
- **Vite**：下一代前端构建工具
- **Vue Router 4**：官方路由管理器
- **Pinia**：Vue 3官方状态管理库
- **Axios**：HTTP客户端
- **Day.js**：轻量级日期处理库

### 数据库
- **SQLite**：默认数据库，开箱即用
- **MySQL 5.7+**：可选的生产环境数据库

## 项目结构

```
Highemotionalintelligencechatassistant/
├── backend/                      # 后端项目
│   ├── main.py                  # FastAPI应用入口
│   ├── config.py                # 应用配置管理
│   ├── .env                     # 环境变量配置
│   ├── .env.example             # 环境变量模板
│   ├── requirements.txt         # Python依赖清单
│   ├── vibe_chat.db            # SQLite数据库文件（使用SQLite时生成）
│   ├── models/                  # 数据模型层
│   │   ├── database.py          # SQLAlchemy数据库模型
│   │   └── schemas.py           # Pydantic请求/响应模型
│   ├── routers/                 # API路由层
│   │   ├── auth.py              # 用户认证路由（注册/登录）
│   │   ├── scripts.py           # 话术管理路由（搜索/详情/收藏）
│   │   ├── chat.py              # 聊天对话路由（AI对话/话术调整）
│   │   └── system.py            # 系统配置路由
│   ├── services/                # 业务逻辑层
│   │   ├── ai_service.py        # 基础AI服务
│   │   └── ai_service_enhanced.py  # 增强AI服务（意图识别/场景匹配）
│   └── utils/                   # 工具函数层
│       └── auth.py              # 认证工具函数（JWT/密码）
├── frontend/                    # 前端项目
│   ├── src/
│   │   ├── main.js             # 应用入口
│   │   ├── App.vue             # 根组件
│   │   ├── views/              # 页面组件
│   │   │   ├── Login.vue       # 登录页
│   │   │   ├── Home.vue        # 首页
│   │   │   ├── Chat.vue        # AI对话页
│   │   │   ├── Scripts.vue     # 话术库页
│   │   │   ├── Favorites.vue   # 收藏页
│   │   │   └── Profile.vue     # 个人中心
│   │   ├── stores/             # Pinia状态管理
│   │   │   └── user.js         # 用户状态
│   │   ├── api/                # API接口封装
│   │   │   ├── request.js      # Axios封装
│   │   │   ├── user.js         # 用户接口
│   │   │   ├── chat.js         # 聊天接口
│   │   │   ├── script.js       # 话术接口
│   │   │   └── system.js       # 系统接口
│   │   ├── router/             # 路由配置
│   │   │   └── index.js        # 路由定义
│   │   └── styles/             # 全局样式
│   │       └── index.scss      # 主样式文件
│   ├── index.html              # HTML模板
│   ├── package.json            # 前端依赖配置
│   └── vite.config.js          # Vite构建配置
├── database/                    # 数据库脚本
│   └── init.sql                # MySQL初始化脚本
├── docs/                       # 项目文档
│   ├── 01-需求说明.md
│   ├── 02-用户手册.md
│   ├── 03-前端说明.md
│   ├── 04-接口说明.md
│   ├── 05-建设方案.md
│   ├── 06-功能清单.md
│   └── README.md
└── README.md                   # 本文件
```

## 快速开始

### 前置要求

- **Python 3.8+**：后端开发语言
- **Node.js 16+**：前端开发环境
- **数据库**（任选其一）：
  - SQLite：默认数据库，无需安装
  - MySQL 5.7+：生产环境推荐

### 数据库配置

项目支持两种数据库模式，根据需求选择：

#### 方式一：使用SQLite（推荐开发环境）

SQLite是默认配置，无需额外安装，开箱即用。首次启动后会自动创建 `vibe_chat.db` 数据库文件。

#### 方式二：使用MySQL（推荐生产环境）

1. 创建数据库并执行初始化脚本

```bash
mysql -u root -p < database/init.sql
```

2. 修改后端配置文件 `backend/.env`：

```bash
DATABASE_TYPE=mysql
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_USER=root
DATABASE_PASSWORD=your_password
DATABASE_NAME=vibe_chat
```

### 默认账户

系统初始化后会创建一个默认管理员账户：

- **用户名**: `admin`
- **密码**: `admin123`
- **角色**: 管理员
- **权限**: 拥有系统所有功能访问权限

首次登录后，建议立即修改默认密码以确保安全。

### 后端启动

1. 进入后端目录

```bash
cd backend
```

2. 创建虚拟环境并安装依赖

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

3. 配置环境变量

复制 `.env.example` 为 `.env` 并根据需要修改配置

```bash
cp .env.example .env  # Linux/Mac
copy .env.example .env  # Windows
```

主要配置项说明：
- `SECRET_KEY`：JWT密钥，生产环境务必修改
- `DATABASE_TYPE`：数据库类型（`sqlite` 或 `mysql`）
- `CORS_ORIGINS`：允许跨域的前端地址

4. 初始化数据库（SQLite模式可选，MySQL模式必须执行）

```bash
# 使用SQLite时，首次启动会自动创建数据库
# 使用MySQL时，需要先执行上面的 database/init.sql
```

5. 启动后端服务

```bash
python main.py
```

后端服务将在 http://localhost:8000 启动

6. 访问API文档

启动成功后，访问 http://localhost:8000/docs 查看交互式API文档

### 前端启动

1. 进入前端目录

```bash
cd frontend
```

2. 安装依赖

```bash
npm install
```

3. 启动开发服务器

```bash
npm run dev
```

前端服务将在 http://localhost:5173 启动

4. 构建生产版本（可选）

```bash
npm run build
```

构建产物将生成在 `frontend/dist` 目录

## 功能特性

### 核心功能

#### 1. AI智能对话
基于自然语言理解的智能对话系统，提供流畅的交互体验：
- **场景识别**：自动识别用户描述的沟通场景（需求沟通、项目推进、Bug处理、客户对接等）
- **意图理解**：智能分析用户意图，提供精准的话术推荐
- **上下文管理**：保持对话连续性，支持多轮对话
- **个性化适配**：根据用户岗位、语气偏好生成个性化话术

#### 2. 岗位专属话术库
针对7类研发岗位提供专业化的沟通话术：

| 岗位 | 主要场景 | 分类示例 |
|------|---------|---------|
| 售前人员 | 客户对接、需求咨询、方案讲解、异议处理、合同洽谈 | 客户对接、需求咨询、方案讲解、异议处理、合同洽谈 |
| 项目经理 | 项目统筹、任务分配、进度同步、风险同步、向上汇报 | 项目统筹、任务分配、进度同步、风险同步、向上汇报 |
| 产品经理 | 需求沟通、需求传递、需求变更、需求答疑 | 需求沟通、需求传递、需求变更、需求答疑 |
| 前端开发 | 技术对接、需求确认、接口联调、Bug处理 | 需求确认、接口联调、Bug处理 |
| 后端开发 | 技术沟通、接口设计、数据库沟通、Bug处理 | 接口设计、数据库沟通、Bug处理 |
| UI设计师 | 需求对接、设计沟通、设计交付 | 设计沟通、设计交付 |
| 测试工程师 | 测试沟通、Bug反馈、测试异议 | Bug反馈、测试异议 |

#### 3. 话术搜索与筛选
支持多维度话术检索：
- **关键词搜索**：在标题、内容、标签中全文检索
- **岗位筛选**：按特定岗位过滤话术
- **场景筛选**：按沟通场景（需求对接、项目推进、Bug处理等）筛选
- **语气筛选**：按话术语气（温和、专业、委婉、活泼）筛选
- **分类筛选**：按话术分类进行精确查找
- **分页查询**：支持分页加载，提升大数据量下的查询性能

#### 4. 话术调整
支持话术的灵活调整：
- **语气调整**：
  - 温和：适合日常协作，语气亲切
  - 专业：适合正式沟通，语言规范
  - 委婉：适合敏感话题，表达含蓄
  - 活泼：适合轻松氛围，语言生动
- **长度调整**：
  - 简洁版：精简内容，直奔主题
  - 详细版：丰富细节，全面阐述

#### 5. 话术收藏与个性化
- **收藏功能**：将常用话术添加到个人收藏夹
- **自定义修改**：基于现有话术进行个性化修改
- **收藏管理**：查看和管理个人收藏列表

#### 6. 对话历史
- **会话记录**：保存所有对话历史，支持按会话ID查询
- **上下文追溯**：查看对话上下文，便于理解场景
- **学习参考**：回顾历史对话，提升沟通技巧

#### 7. 用户认证与管理
- **用户注册/登录**：支持用户名密码登录，JWT令牌认证
- **个人信息管理**：修改头像、角色、语气偏好、长度偏好
- **角色选择**：用户可选择自己的岗位角色

### 话术分类体系

#### 按岗位分类
每个岗位都有专属的话术分类体系，涵盖该岗位的主要工作场景。

#### 按场景类型分类
- **需求对接**：需求调研、需求确认、需求变更、需求传递
- **项目推进**：项目启动、任务分配、进度同步、风险汇报
- **问题沟通**：Bug反馈、Bug处理、技术沟通、异议处理
- **协同配合**：请教问题、请求帮助、感谢帮忙、拒绝请求
- **对外衔接**：客户对接、方案讲解、异议处理、合同洽谈
- **会议沟通**：会议开场、会议讨论、会议总结

#### 按语气分类
- **温和**：语气亲切，适合日常协作
- **专业**：语言规范，适合正式沟通
- **委婉**：表达含蓄，适合敏感话题
- **活泼**：语言生动，适合轻松氛围

#### 按目标对象分类
- **客户**：对外沟通话术
- **领导**：向上汇报话术
- **同事**：团队协作话术
- **新人**：指导帮助话术

## API文档

后端启动后，访问 http://localhost:8000/docs 查看完整API文档（Swagger UI）。

### 主要API端点

#### 认证相关 (`/api/auth`)
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `GET /api/auth/me` - 获取当前用户信息
- `PUT /api/auth/me` - 更新当前用户信息

#### 聊天相关 (`/api/chat`)
- `POST /api/chat/message` - 发送消息，获取AI回复
- `POST /api/chat/adjust` - 调整话术语气和长度
- `GET /api/chat/history/{session_id}` - 获取聊天历史

#### 话术相关 (`/api/scripts`)
- `GET /api/scripts/` - 获取话术列表（支持筛选和分页）
- `GET /api/scripts/{script_id}` - 获取话术详情
- `POST /api/scripts/{script_id}/like` - 点赞话术
- `POST /api/scripts/favorites` - 添加收藏
- `DELETE /api/scripts/favorites/{script_id}` - 取消收藏
- `GET /api/scripts/favorites/list` - 获取收藏列表

#### 系统相关 (`/api/system`)
- 获取系统配置和版本信息

## 数据库结构

### 主要数据表

#### 用户表 (users)
存储用户基本信息和偏好设置：
- 用户名、密码哈希、手机号、邮箱
- 岗位角色、头像URL
- 语气偏好、长度偏好
- VIP状态、激活状态

#### 岗位表 (positions)
定义系统支持的岗位类型：
- 岗位名称、代码、描述
- 排序、启用状态

#### 话术分类表 (script_categories)
定义话术的分类体系：
- 分类名称、代码、描述
- 父分类ID、关联岗位ID
- 排序、启用状态

#### 话术表 (scripts)
存储所有话术内容：
- 标题、内容、简洁版内容
- 关联分类ID、岗位ID
- 场景类型、语气、目标对象
- 标签、使用次数、点赞次数
- 免费/付费标识、启用状态

#### 用户收藏表 (user_favorites)
记录用户的话术收藏：
- 用户ID、话术ID
- 自定义话术内容
- 创建时间

#### 对话记录表 (conversations)
存储AI对话历史：
- 用户ID、会话ID
- 消息类型（user/assistant）
- 消息内容、意图识别
- 关联话术ID

#### 话术调整记录表 (script_adjustments)
记录话术调整历史：
- 用户ID、话术ID
- 原始内容、调整后内容
- 语气、长度类型、用户反馈

## 开发指南

### 添加新话术

1. **直接数据库插入**：在数据库 `scripts` 表中插入新话术
   ```sql
   INSERT INTO scripts (title, content, brief_content, category_id, position_id, scene_type, tone, target_audience, tags, is_free)
   VALUES ('话术标题', '完整话术内容', '简洁版内容', 分类ID, 岗位ID, '场景类型', '语气', '目标对象', '标签1,标签2', 1);
   ```

2. **关联分类和岗位**：确保 `category_id` 和 `position_id` 在对应表中存在

3. **设置属性**：
   - `scene_type`：场景类型（需求对接/项目推进/Bug处理等）
   - `tone`：语气（温和/专业/委婉/活泼）
   - `target_audience`：目标对象（客户/领导/同事/新人）
   - `tags`：标签，逗号分隔

### 扩展AI服务

#### 添加新的意图识别

在 `backend/services/ai_service_enhanced.py` 的 `INTENT_PATTERNS` 中添加新意图：

```python
INTENT_PATTERNS = {
    # ... 现有意图
    'new_intent': ['关键词1', '关键词2', '关键词3']
}
```

#### 添加新的场景类型

在 `SCENE_PATTERNS` 中添加新场景：

```python
SCENE_PATTERNS = {
    # ... 现有场景
    '新场景': {
        'keywords': ['关键词1', '关键词2'],
        'scenarios': ['场景描述1', '场景描述2']
    }
}
```

#### 扩展关键词提取

在 `extract_keywords` 方法的 `core_words` 集合中添加新关键词。

### 前端页面开发

#### 新增页面

1. 在 `frontend/src/views/` 下创建新的Vue组件
2. 在 `frontend/src/router/index.js` 中注册路由
3. 根据需要添加对应的API接口封装（在 `frontend/src/api/` 下）

#### 状态管理

使用Pinia进行状态管理，示例：
```javascript
// stores/example.js
import { defineStore } from 'pinia'

export const useExampleStore = defineStore('example', {
  state: () => ({
    data: []
  }),
  actions: {
    async fetchData() {
      // 异步获取数据
    }
  }
})
```

### 代码规范

#### 后端
- 遵循PEP 8代码风格
- 使用类型注解（Type Hints）
- 函数和类添加文档字符串
- 异常处理要有明确的错误信息

#### 前端
- 使用Vue 3 Composition API
- 组件命名采用PascalCase
- 遵循Vue官方风格指南
- 使用ESLint进行代码检查

## 部署说明

### 生产环境配置

1. **修改安全配置**
   - 修改 `.env` 中的 `SECRET_KEY` 为随机生成的密钥
   - 设置合适的 `ACCESS_TOKEN_EXPIRE_MINUTES`

2. **数据库选择**
   - 推荐使用MySQL生产环境数据库
   - 配置数据库连接池参数

3. **CORS配置**
   - 设置正确的 `CORS_ORIGINS`，只允许可信域名

4. **构建前端**
   ```bash
   cd frontend
   npm run build
   ```

5. **部署后端**
   - 使用Gunicorn + Uvicorn部署FastAPI
   - 配置反向代理（Nginx）
   - 配置HTTPS

### Docker部署（可选）

可以创建Dockerfile和docker-compose.yml进行容器化部署。

## 常见问题

### Q: 如何切换数据库？
A: 修改 `backend/.env` 文件中的 `DATABASE_TYPE` 为 `sqlite` 或 `mysql`，然后重启后端服务。

### Q: 前端无法连接后端怎么办？
A: 检查以下几点：
- 后端服务是否正常启动（访问 http://localhost:8000）
- CORS配置是否正确（检查 `.env` 中的 `CORS_ORIGINS`）
- 浏览器控制台是否有跨域错误

### Q: 如何添加新的岗位？
A: 在 `backend/services/ai_service_enhanced.py` 的 `POSITION_KEYWORDS` 中添加新岗位，并在数据库 `positions` 表中插入记录。

### Q: AI回复不准确怎么办？
A: 可以通过以下方式优化：
- 添加更多话术数据到数据库
- 扩展AI服务的关键词和场景匹配规则
- 调整用户岗位和语气偏好设置

## 项目文档

详细的项目文档位于 `docs/` 目录：
- [需求说明](docs/01-需求说明.md) - 项目需求和功能描述
- [用户手册](docs/02-用户手册.md) - 用户使用指南
- [前端说明](docs/03-前端说明.md) - 前端开发文档
- [接口说明](docs/04-接口说明.md) - API接口详细说明
- [建设方案](docs/05-建设方案.md) - 项目建设方案
- [功能清单](docs/06-功能清单.md) - 功能清单列表

## 许可证

MIT License
