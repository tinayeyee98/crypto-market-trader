from typing import Any, Dict, List

import structlog
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorDatabase

from .__init__ import __name__ as app_name
from .__init__ import __version__ as app_version
from .config import Settings, get_settings
from .models.base_model import AppInfo
from .repositories.db import get_db
from .routes import trade_orders

log: structlog.BoundLogger = structlog.get_logger()
settings: Settings = get_settings()


class CryptoMarketTraderAPI(FastAPI):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


async def startup() -> None:
    log.msg("application startup complete")


async def shutdown() -> None:
    log.msg("application is shutting down")


def create_app(
    app_name: str = app_name, app_version: str = app_version
) -> CryptoMarketTraderAPI:
    app = CryptoMarketTraderAPI(
        root_path=settings.app_root_path,
        title=app_name,
        version=app_version,
    )
    init_db()  # Initialize Database

    # Initial variable to incliude extra information for openapi tags
    openapi_tags: List[Dict[str, Any]] = []

    # Routes and additional information for openapi
    app.info = AppInfo(app_name=app.title, app_version=app.version)

    app.include_router(trade_orders.router, prefix=settings.api_prefix)

    # Additional information for openapi docs
    app.openapi_tags = openapi_tags

    # Register application lifecycle envents
    app.add_event_handler("startup", startup)
    app.add_event_handler("shutdown", shutdown)
    return app


def init_db(db_uri: str = settings.db_uri, db_name: str = settings.db_name):
    db: AsyncIOMotorDatabase = get_db(db_uri, db_name)
