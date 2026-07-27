# FastAPI Perfectionist Starter

[English Documentation](README_en.md)

一个现代化、生产就绪的 FastAPI 模板，内置最佳实践。这个启动套件为构建可扩展的 REST API 提供了坚实的基础，包含身份验证、数据库集成和完善的工具链。

## 特性

- **现代 FastAPI 架构**: 基于 FastAPI 和 async/await 模式构建
- **数据库集成**: SQLAlchemy 2.1 异步支持和 Alembic 数据库迁移
- **身份验证**: 基于 JWT 的身份验证，使用安全的密码哈希（Argon2）
- **代码质量**: 使用 Ruff 进行代码检查和格式化，严格的类型提示
- **测试**: Pytest 异步测试支持和覆盖率报告
- **结构化架构**: 清晰的关注点分离，包含模块、服务和依赖注入
- **中间件**: 内置 CORS 和错误处理中间件
- **日志**: 集成 Loguru 实现美观、结构化的日志
- **分页**: 内置基于游标的分页支持
- **响应处理**: 标准化的 API 响应格式
- **开发友好**: 开发环境使用 SQLite，生产环境使用 PostgreSQL

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
│       │   ├── note/              # 笔记管理模块
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

## 环境要求

- Python 3.14+
- [uv](https://docs.astral.sh/uv/)（推荐）或 pip

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/yourusername/fastapi-perfectionist-starter.git
cd fastapi-perfectionist-starter
```

### 2. 安装依赖

使用 uv（推荐）:
```bash
uv sync
```

或使用 pip:
```bash
pip install -e .
```

### 3. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env` 文件并配置你的设置:
```env
# 应用配置
APP_HOST=127.0.0.1
APP_PORT=8000
APP_DEBUG=true
LOG_LEVEL=INFO

# 数据库
DATABASE_URL=sqlite+aiosqlite:///./dev.db

# JWT（重要：生产环境必须修改！）
JWT_SECRET=change-this-in-production-at-least-32-bytes
JWT_EXPIRATION_DAYS=90
JWT_ALGORITHM=HS256

# CORS
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
```

### 4. 运行数据库迁移

```bash
alembic upgrade head
```

### 5. 启动开发服务器

```bash
uvicorn fastapi_perfectionist_starter.main:asgi_app --reload
```

API 将在 `http://127.0.0.1:8000` 上运行

当 `APP_DEBUG=true` 时，API 文档（Swagger UI）可在 `http://127.0.0.1:8000/docs` 访问

## API 端点

### 身份验证

- `POST /api/v1/auth/token` - 获取访问令牌（OAuth2 密码流程）
- `POST /api/v1/auth/me` - 获取当前用户信息

### 笔记

- `POST /api/v1/notes` - 创建新笔记
- `GET /api/v1/notes` - 列出笔记（分页）
- `GET /api/v1/notes/{note_id}` - 获取特定笔记
- `PATCH /api/v1/notes/{note_id}` - 更新笔记
- `DELETE /api/v1/notes/{note_id}` - 删除笔记

## 开发

### 运行测试

```bash
pytest
```

查看覆盖率:
```bash
pytest --cov
```

### 代码格式化和检查

```bash
ruff check .
ruff format .
```

### 创建数据库迁移

```bash
alembic revision --autogenerate -m "变更描述"
alembic upgrade head
```

## 生产环境部署

### 1. 配置生产环境

在生产环境的 `.env` 文件中设置以下内容:

```env
APP_DEBUG=false
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
JWT_SECRET=<生成一个至少32字节的安全随机字符串>
```

**重要提示**: 当 `APP_DEBUG=false` 时，必须修改 `JWT_SECRET` 的默认值。否则应用程序将拒绝启动。

### 2. 运行迁移

```bash
alembic upgrade head
```

### 3. 使用生产服务器启动

```bash
uvicorn fastapi_perfectionist_starter.main:asgi_app --host 0.0.0.0 --port 8000 --workers 4
```

或使用进程管理器如 systemd 或 Docker。

## 配置说明

所有配置通过环境变量或 `.env` 文件管理:

| 变量 | 描述 | 默认值 |
|------|------|--------|
| `APP_HOST` | 服务器主机地址 | `127.0.0.1` |
| `APP_PORT` | 服务器端口 | `8000` |
| `APP_DEBUG` | 调试模式 | `false` |
| `LOG_LEVEL` | 日志级别 | `INFO` |
| `DATABASE_URL` | 数据库连接字符串 | `sqlite+aiosqlite:///./dev.db` |
| `JWT_SECRET` | JWT 令牌的密钥 | （生产环境必须修改） |
| `JWT_EXPIRATION_DAYS` | 令牌过期天数 | `90` |
| `JWT_ALGORITHM` | JWT 算法 | `HS256` |
| `CORS_ORIGINS` | 允许的 CORS 源（JSON 列表） | `["http://localhost:3000","http://localhost:5173"]` |

## 架构设计

### 服务层模式

业务逻辑封装在服务类中（例如 `AuthService`、`NoteService`），通过 FastAPI 的依赖注入系统注入。

### 依赖注入

FastAPI 依赖项用于:
- 身份验证/授权（`RequireAuthUser`）
- 资源验证（`RequireNote`）
- 服务注入

### 响应标准化

所有 API 响应通过 `ResponseHandler` 遵循一致的格式:
```json
{
  "data": {...},
  "message": "成功",
  "code": 200
}
```

### 数据库模型

使用 SQLAlchemy 2.1 的异步支持和声明式模型。每个模型包含标准字段，如 `id`、`created_at` 和 `updated_at`。

## 测试

项目包含全面的测试覆盖:
- 身份验证流程测试
- 笔记 CRUD 操作测试
- 依赖注入测试
- 错误处理测试

运行测试:
```bash
pytest
```

## 许可证

MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 贡献

1. Fork 本仓库
2. 创建功能分支
3. 进行修改
4. 运行测试和代码检查
5. 提交 Pull Request

## 作者

TrueRou - [you@example.com](mailto:you@example.com)
