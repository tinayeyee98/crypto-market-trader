from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application runtime settings which can be configured via command line or .env file."""

    app_root_path: str = Field(
        default="", title="Application Root Path", description="ASGI root_path variable"
    )
    internal_routes_prefix: str = Field(
        default="/internal", title="Internal Routes Prefix"
    )
    healthcheck_response: str = Field(
        default="T0sK",
        title="Healthcheck Response",
        description="The response content for healthcheck requests",
    )
    api_prefix: str = Field(default="/api/v1", title="API Prefix")
    db_uri: str = Field(default="mongodb://localhost:27017/", title="Database URI")
    db_name: str = Field(default="crypto_trading_db", title="DB Name")

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
