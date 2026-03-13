from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


def add_middleware(asgi_app: FastAPI) -> None:
    origins = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]

    asgi_app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
