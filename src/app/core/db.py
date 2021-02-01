from app.core.config import get_settings
from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI

settings = get_settings()


tortoise_orm = {
    "connections": {
        "default": settings.DATABASE_URI,
    },
    "apps": {
        "models": {
            "models": settings.MODELS + ["aerich.models"],
            "default_connection": "default",
        },
    },
}


def init_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        db_url=settings.DATABASE_URI,
        modules={"models": settings.MODELS},
        generate_schemas=True,
        add_exception_handlers=True,
    )
