# FastAPI Perfectionist Starter

一个现代化、生产就绪的 FastAPI 模板项目，内置最佳实践。支持快速构建可扩展的 REST API，包含身份验证、数据库集成和完善的工具链。

## 🚀 如何使用这个模板

**本项目是一个可转变的模板，不需要手动修改代码，让你的 AI Agent 来完成项目转变！**

### 使用步骤

1. **克隆或下载本仓库到你的工作目录**
   ```bash
   git clone <repo-url>
   cd fastapi-perfectionist-starter
   ```

2. **告诉你的 Agent（如 OpenCode、Cursor、Windsurf 等）**
   ```
   请帮我基于这个模板创建一个新项目
   ```

3. **回答 Agent 的问题**
   - Agent 会询问你的项目名称、描述、需要的功能模块等
   - 如果不确定需要什么模块，可以保留现有的示例模块

4. **Agent 会自动完成**
   - 重命名项目
   - 更新所有配置和导入
   - 根据你的需求调整模块
   - 清理模板标记

5. **开始开发你的项目！**

> **注意**：本 README 下方包含了详细的 Agent 指令，你的 Agent 会自动读取并执行。转变完成后，这些指令会被自动删除。

---

## 核心特性

- **现代 FastAPI 架构**: 基于 FastAPI 和 async/await 模式构建
- **数据库集成**: SQLAlchemy 2.1 异步支持和 Alembic 数据库迁移
- **身份验证**: 基于 JWT 的身份验证，使用安全的密码哈希（Argon2）
- **代码质量**: 使用 Ruff 进行代码检查和格式化，严格的类型提示
- **测试**: Pytest 异步测试支持和覆盖率报告
- **结构化架构**: 清晰的关注点分离，包含模块、服务和依赖注入

## 项目结构

```
fastapi-perfectionist-starter/
├── src/
│   └── fastapi_perfectionist_starter/
│       ├── api/                    # API 层
│       │   └── v1/
│       │       ├── router/         # API 端点
│       │       └── schema/         # 请求/响应模式
│       ├── modules/                # 业务逻辑模块
│       │   ├── auth/              # 身份验证模块
│       │   ├── note/              # 笔记管理模块（示例）
│       │   └── user/              # 用户管理模块
│       ├── infra/                 # 基础设施层
│       │   ├── middleware/        # 自定义中间件
│       │   ├── engine.py          # 数据库引擎
│       │   ├── models.py          # SQLAlchemy 模型
│       │   ├── pagination.py     # 分页工具
│       │   ├── response.py        # 响应处理器
│       │   ├── settings.py        # 配置
│       │   └── logging.py         # 日志设置
│       └── main.py                # 应用程序入口点
├── alembic/                       # 数据库迁移
├── tests/                         # 测试套件
├── pyproject.toml                 # 项目配置
└── .env.example                   # 环境变量模板
```

<!-- TEMPLATE_INSTRUCTIONS_START -->

## 🤖 Agent 使用指南

**本项目是一个模板项目，Agent 需要协助用户在当前目录中将其转变为新项目。**

### 转变前信息收集

**必须收集的信息：**

1. **项目包名** (Python包名，蛇形命名，如：`blog_api`, `task_manager`)
2. **项目显示名称** (用于API文档，如：`Blog API`, `Task Manager`)
3. **项目描述** (简短描述项目用途)
4. **作者信息** (姓名和邮箱)
5. **业务模块需求**：
   - 询问用户需要什么功能模块
   - 如果用户不确定或说"不知道"，**保留现有的 auth 和 note 模块作为参考示例**
   - 如果用户明确说明需要特定模块，记录下来（转变后可基于现有模式创建新模块）

**可选收集的信息：**

- 初始版本号（默认 `0.1.0`）
- Python 版本要求（默认 `>=3.14,<3.15`）
- 数据库类型偏好（默认支持 SQLite 开发 + PostgreSQL 生产）

---

### 转变执行步骤

**请严格按照以下顺序执行：**

#### 第 1 步：重命名包目录

```bash
mv src/fastapi_perfectionist_starter src/{新包名}
```

#### 第 2 步：更新 pyproject.toml

修改以下字段：
```toml
[project]
name = "{新包名}"  # 注意：pyproject.toml中使用连字符，如 "blog-api"
description = "{项目描述}"
authors = [{name = "{作者姓名}", email = "{作者邮箱}"}]
version = "{版本号}"  # 如有需要
```

#### 第 3 步：批量替换所有导入语句

在所有 Python 文件中，将 `fastapi_perfectionist_starter` 替换为 `{新包名}`：

**需要修改的文件类型：**
- `src/{新包名}/` 下的所有 Python 文件
- `alembic/env.py`
- `tests/` 下的所有测试文件

**使用全局替换：**
```bash
# 使用 sed 或编辑器的全局替换功能
find . -type f -name "*.py" -exec sed -i '' 's/fastapi_perfectionist_starter/{新包名}/g' {} +
```

#### 第 4 步：更新 main.py 中的应用标题

修改 `src/{新包名}/main.py`：
```python
asgi_app = FastAPI(
    title="{项目显示名称}",  # 例如："Blog API"
    version="{版本号}",      # 例如："0.1.0"
    lifespan=lifespan,
    openapi_url=openapi_url,
)
```

#### 第 5 步：处理业务模块

**情况 A：用户不确定需要什么模块**
- **保留所有现有模块**（auth, note, user）
- 告知用户这些是示例模块，可以后续修改或删除

**情况 B：用户明确不需要 note 模块**

执行以下删除操作：

```bash
# 删除 note 模块
rm -rf src/{新包名}/modules/note/

# 删除 note 相关的 API
rm src/{新包名}/api/v1/router/note.py
rm src/{新包名}/api/v1/schema/note.py

# 删除 note 测试
rm tests/test_note.py
```

然后编辑以下文件：

**`src/{新包名}/infra/models.py`**
- 删除 `Note` 模型类定义

**`src/{新包名}/api/v1/router/__init__.py`**
- 移除 `from .note import router as note_router`
- 从路由列表中移除 `note_router`

**情况 C：用户需要其他新模块**
- 基于现有的 note 模块模式创建新模块
- 包含：`modules/{模块名}/services.py`、`dependencies.py`
- 包含：`api/v1/router/{模块名}.py`、`api/v1/schema/{模块名}.py`
- 在 `infra/models.py` 中添加对应的数据库模型

#### 第 6 步：清理 README.md

**删除 Agent 指令部分：**
- 删除从 `<!-- TEMPLATE_INSTRUCTIONS_START -->` 到 `<!-- TEMPLATE_INSTRUCTIONS_END -->` 之间的所有内容
- 保留上方的项目结构、架构设计、快速开始指南

**更新项目信息：**
- 将标题改为：`# {项目显示名称}`
- 更新描述为用户提供的项目描述
- 更新快速开始中的启动命令：
  ```bash
  uvicorn {新包名}.main:asgi_app --reload
  ```

#### 第 7 步：验证转变结果

**运行以下命令确保转变成功：**

```bash
# 代码格式检查
ruff check .

# 运行测试
pytest

# 尝试启动应用（确认无导入错误）
uvicorn {新包名}.main:asgi_app --help
```

如果出现错误，检查导入语句是否完全替换。

#### 第 8 步：（可选）Git 历史处理

询问用户是否需要：
- 重置 Git 历史（`git reset` 到初始状态）
- 创建新的初始提交
- 保持现有 Git 历史

---

### 关键注意事项

1. **包名格式差异**：
   - Python 导入使用下划线：`blog_api`
   - pyproject.toml 中 name 字段使用连字符：`blog-api`
   - 目录名使用下划线：`src/blog_api/`

2. **必须保留的模块**：
   - `infra/` - 基础设施层（数据库、日志、响应处理等）必须保留
   - `auth/` 和 `user/` - 认证和用户模块通常需要保留
   - `note/` - 仅作为示例，可根据用户需求删除

3. **数据库模型同步**：
   - 删除业务模块时，必须同步删除 `infra/models.py` 中对应的模型类
   - 删除后需要创建新的 Alembic 迁移

4. **导入语句检查**：
   - 所有 `from fastapi_perfectionist_starter` 必须替换
   - 使用 grep 检查遗漏：`grep -r "fastapi_perfectionist_starter" .`

5. **测试文件同步**：
   - 删除业务模块时，同步删除对应的测试文件
   - 确保 `tests/conftest.py` 中没有引用已删除的模块

---

### 转变完成标志

当以下条件全部满足时，转变完成：

- ✅ 包目录已重命名
- ✅ `pyproject.toml` 已更新项目信息
- ✅ 所有导入语句已替换
- ✅ `main.py` 中应用标题已更新
- ✅ 业务模块已按需删除/保留
- ✅ README.md 中 Agent 指令已删除
- ✅ README.md 项目信息已更新
- ✅ `ruff check .` 无错误
- ✅ `pytest` 测试通过
- ✅ 应用可以成功启动

**最后，告知用户：**

```
✅ 项目转变完成！

项目名称：{项目显示名称}
包名：{新包名}
作者：{作者信息}

下一步：
1. 查看 .env.example，配置环境变量
2. 运行 alembic upgrade head 初始化数据库
3. 运行 uvicorn {新包名}.main:asgi_app --reload 启动服务
4. 访问 http://127.0.0.1:8000/docs 查看API文档

{如果保留了note模块}
注意：当前保留了 note 模块作为示例，你可以：
- 参考该模块实现自己的业务逻辑
- 或删除它并创建自己的模块

祝开发顺利！
```

---

### 文件修改清单（快速参考）

| 文件类型   | 文件路径                      | 修改内容            |
|------------|-------------------------------|---------------------|
| 配置文件   | `pyproject.toml`              | 项目元信息          |
| 主应用     | `src/*/main.py`               | 导入 + 标题         |
| API层      | `src/*/api/v1/**/*.py`        | 导入语句            |
| 业务模块   | `src/*/modules/**/*.py`       | 导入语句            |
| 基础设施   | `src/*/infra/**/*.py`         | 导入语句            |
| 数据库迁移 | `alembic/env.py`              | 导入语句            |
| 测试文件   | `tests/**/*.py`               | 导入语句            |
| 文档       | `README.md`                   | 删除指令 + 更新信息 |

**总计：所有包含 `fastapi_perfectionist_starter` 的 Python 文件**

<!-- TEMPLATE_INSTRUCTIONS_END -->

---

## 许可证

MIT 许可证 - 详见 [LICENSE](LICENSE) 文件
