from fastapi import FastAPI
from fastapi_versioning import VersionedFastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api.routers import api_router
from app.core.config import get_settings
from app.core.db import init_db

settings = get_settings()

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(api_router)
app = VersionedFastAPI(app, version_format="{major}", prefix_format="/api/v{major}")
init_db(app)
