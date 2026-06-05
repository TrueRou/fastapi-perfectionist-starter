# fastapi-perfectionist-starter

> A Cookiecutter template for production-grade FastAPI applications — opinionated, complete, and wired correctly from day one.

![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688)
![uv](https://img.shields.io/badge/uv-managed-blueviolet)
![License: MIT](https://img.shields.io/badge/license-MIT-green)

## Overview

Most starters give you a hello-world skeleton and leave the hard parts to you. This one doesn't. Every layer is deliberately chosen and correctly integrated: async ORM with migrations, structured logging that intercepts uvicorn output, uniform response envelopes, argon2id password hashing, stateless JWT auth with proper expiry, and a test suite that runs against a real (in-memory) database.

The goal is to spend zero time on boilerplate and immediately start writing domain logic.

## Tech Stack

| Tool | Role |
|---|---|
| [FastAPI](https://fastapi.tiangolo.com) | ASGI web framework |
| [SQLModel](https://sqlmodel.tiangolo.com) | ORM (SQLAlchemy + Pydantic in one) |
| [Alembic](https://alembic.sqlalchemy.org) | Database migrations |
| [Pydantic v2](https://docs.pydantic.dev) | Data validation & settings management |
| [Loguru](https://loguru.readthedocs.io) | Structured logging |
| [argon2-cffi](https://argon2-cffi.readthedocs.io) | Password hashing (argon2id) |
| [PyJWT](https://pyjwt.readthedocs.io) | JWT token generation and verification |
| [uv](https://docs.astral.sh/uv) | Dependency management and packaging |

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (`brew install uv` or `pip install uv`)
- PostgreSQL (optional — SQLite works out of the box for development)

## Quick Start

Generate a new project:

```bash
uvx cookiecutter gh:your-org/fastapi-perfectionist-starter
```

Then set up the generated project:

```bash
cd your_project_slug
cp .env.example .env          # review and edit as needed
uv sync                        # install all dependencies
uv run alembic upgrade head    # run migrations
uv run uvicorn your_project_slug.main:asgi_app --reload
```

The API will be available at `http://127.0.0.1:8000`. OpenAPI docs are at `/openapi.json` (only when `APP_DEBUG=true`).

## Project Structure

```
your_project_slug/
├── alembic/                   # migration scripts
│   └── versions/
├── src/
│   └── your_project_slug/
│       ├── api/
│       │   └── v1/
│       │       ├── auth.py    # register, login, /users/me
│       │       ├── note.py    # notes CRUD
│       │       └── schema/    # Pydantic request/response schemas
│       ├── infra/
│       │   ├── engine.py      # async DB engine, session factory, migrations
│       │   ├── logging.py     # Loguru setup with uvicorn interception
│       │   ├── middleware/
│       │   │   ├── cors.py    # CORS configuration
│       │   │   └── error.py   # global exception handling
│       │   ├── models.py      # SQLModel table definitions
│       │   ├── pagination.py  # generic cursor pagination
│       │   ├── response.py    # AppResponse[T] uniform envelope
│       │   └── settings.py    # Pydantic-settings configuration
│       ├── modules/
│       │   ├── note/          # Note domain (service + dependencies)
│       │   └── user/          # User domain (service + dependencies)
│       └── main.py            # FastAPI app factory
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_note.py
├── .env.example
├── alembic.ini
└── pyproject.toml
```

## Environment Variables

Copy `.env.example` to `.env` and configure for your environment.

| Variable | Default | Description |
|---|---|---|
| `APP_HOST` | `127.0.0.1` | Bind address |
| `APP_PORT` | `8000` | Bind port (1–65535) |
| `APP_DEBUG` | `true` | Enables OpenAPI docs; disables JWT secret guard |
| `LOG_LEVEL` | `INFO` | One of `DEBUG` / `INFO` / `WARNING` / `ERROR` / `CRITICAL` |
| `DATABASE_URL` | `sqlite+aiosqlite:///./dev.db` | SQLAlchemy async URL |
| `JWT_SECRET` | — | **Required in production.** Must differ from the default when `APP_DEBUG=false` |
| `JWT_EXPIRATION_DAYS` | `90` | Token lifetime in days |
| `JWT_ALGORITHM` | `HS256` | JWT signing algorithm |
| `CORS_ORIGINS` | `["http://localhost:3000","http://localhost:5173"]` | JSON list of allowed CORS origins |

For PostgreSQL, set:
```
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
```

## API Endpoints

All responses (except login) are wrapped in a uniform envelope:
```json
{"data": ..., "code": 200, "message": "success", "timestamp": "..."}
```

**Auth**

| Method | Path | Description |
|---|---|---|
| `POST` | `/v1/auth/register` | Create a new user account |
| `POST` | `/v1/auth/token` | Login with username/password, returns JWT |
| `GET` | `/v1/users/me` | Get current user (requires `Authorization: Bearer <token>`) |

**Notes**

| Method | Path | Description |
|---|---|---|
| `POST` | `/v1/notes` | Create a note |
| `GET` | `/v1/notes` | List notes (paginated: `?page_number=1&page_size=10`) |
| `GET` | `/v1/notes/{note_id}` | Get a note by ID |
| `PATCH` | `/v1/notes/{note_id}` | Update a note's title or content |
| `DELETE` | `/v1/notes/{note_id}` | Delete a note |

## Running Tests

```bash
uv run pytest
```

With coverage:

```bash
uv run pytest --cov --cov-report=term-missing
```

Tests use an in-memory SQLite database and roll back after each test case, so they are fast and fully isolated.

## Development

Lint and format with ruff:

```bash
uv run ruff check .
uv run ruff format .
```

For strict static type checking, add mypy:

```bash
uv add --dev mypy
uv run mypy src/
```

## Architecture Decisions

**SQLModel over raw SQLAlchemy** — SQLModel unifies the ORM layer and the validation layer. A single class definition serves as both the database table schema and the Pydantic model, eliminating the duplication between SQLAlchemy `Column` definitions and separate schema classes.

**Loguru over stdlib logging** — Loguru requires zero handler configuration, intercepts uvicorn's output through `InterceptHandler`, and supports structured patching (overriding the `name`/`function`/`line` fields in log records). The result is a single consistent log stream from all components.

**argon2-cffi over bcrypt** — argon2id won the Password Hashing Competition. It is memory-hard, resistant to GPU cracking, and is the current OWASP recommendation. The `PasswordHasher` default parameters are calibrated for a good cost/performance tradeoff.

**uv** — uv resolves and installs dependencies significantly faster than pip, manages virtual environments, supports workspaces, and produces a lockfile. It replaces pip, pip-tools, virtualenv, and setuptools in one tool.

**`AppResponse[T]` envelope** — all endpoints return a consistent JSON shape with `data`, `code`, `message`, and `timestamp`. This makes client-side response handling uniform and allows middleware to inspect or transform responses without inspecting individual endpoint return types.

## Contributing

1. Fork the repository and create a feature branch.
2. Run `uv sync` to install all dependencies.
3. Make your changes. Run `uv run ruff check .` and `uv run pytest` before opening a PR.
4. Open a pull request against `main`.

## License

MIT — see [LICENSE](LICENSE).
