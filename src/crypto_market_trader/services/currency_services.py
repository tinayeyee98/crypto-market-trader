from typing import List

import httpx
import structlog
from fastapi import HTTPException

from ..config import Settings, get_settings

log = structlog.get_logger()
settings: Settings = get_settings()


async def get_exchange_price(exchange: str):
    endpoint = settings.market_endpoint.format(exchange=exchange)
    async with httpx.AsyncClient() as client:
        response = await client.get(endpoint)
        response_data = response.json()

    return response_data.get("result")


async def get_best_market(exchanges: List):
    """Find the best market through exchange list"""
    try:
        best_exchange = None
        max_price = 0.0

        for exchange in exchanges:
            exchange_data = await get_exchange_price(exchange)
            price = exchange_data.get("price")

            if isinstance(price, (int, float)) and price > max_price:
                max_price = price
                best_exchange = exchange

        return {"exchange": best_exchange, "price": max_price}

    except Exception as e:
        log.error(e)
