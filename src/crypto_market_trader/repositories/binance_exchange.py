import asyncio

import structlog
from binance.client import AsyncClient

from ..config import Settings, get_settings

log = structlog.get_logger()
settings: Settings = get_settings()


class BinanceTrader:
    @classmethod
    async def __aenter__(cls):
        cls.client = AsyncClient(
            api_key=settings.binance_apikey, api_secret=settings.binance_secret
        )
        return cls

    @classmethod
    async def __aexit__(cls, exc_type, exc_value, traceback):
        pass

    @classmethod
    async def place_buy_order(cls, pair: str, buy_price: float, quantity: float):
        try:
            async with cls() as trader:
                order = await cls.client.create_order(
                    symbol=pair,
                    side=AsyncClient.SIDE_BUY,
                    type=AsyncClient.ORDER_TYPE_LIMIT,
                    timeInForce=AsyncClient.TIME_IN_FORCE_GTC,
                    price=str(buy_price),
                    quantity=str(quantity),
                )
                return order
        except Exception as e:
            log.error(e)

    @classmethod
    async def place_sell_order(cls, pair: str, quantity: float):
        try:
            async with cls() as trader:
                order = await cls.client.create_order(
                    symbol=pair,
                    side=AsyncClient.SIDE_SELL,
                    type=AsyncClient.ORDER_TYPE_MARKET,
                    quantity=str(quantity),
                )
                return order
        except Exception as e:
            log.error(e)
