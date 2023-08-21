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

    cryptowatch_apikey: str = Field(
        default="4EXB4F43HCI0PE7EMHLC", title="Cryptowatch API Key"
    )
    crypto_pair: str = Field(default="btcusdt", title="BTC/USDT pair")
    exchanges: str = Field(
        default="binance,kraken,coinbase,bitfinex", title="Exchange List"
    )
    binance_apikey: str = Field(
        default="fLcI7Un7I4PJY5mI3cRtaIjcpY5P9M", title="API Key for Binance Exchange"
    )
    binance_secret: str = Field(
        default="uUnNfIoM9AAtkj4ro8mxPL58", title="API Secret for Binance Exchange"
    )
    coinbase_apikey: str = Field(
        default="AyYNRF8AbdSG7JWQ", title="API Key for CoinBase Exchange"
    )
    market_endpoint: str = Field(
        default="https://api.cryptowat.ch/markets/:exchange/:pairs/price",
        title="Market Price Endpoint",
    )

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
