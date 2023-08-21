from typing import List

import httpx
import structlog

from ..config import Settings, get_settings
from ..repositories.binance_exchange import BinanceTrader
from .util import lowertouppercase, strtolist

log = structlog.get_logger()
settings: Settings = get_settings()


async def search_market_n_place_order(side: str, quantity: float):
    best_market = await get_best_market(settings.exchanges)

    if best_market.get("exchange") == "binance" and side == "buy":
        trade_with_binance = await BinanceTrader.place_buy_order(
            pair=lowertouppercase(settings.crypto_pair),
            buy_price=best_market.get("price"),
            quantity=quantity,
        )
    else:
        trade_with_binance = await BinanceTrader.place_sell_order(
            pair=lowertouppercase(settings.crypto_pair), quantity=quantity
        )


async def get_exchange_price(exchange: str):
    endpoint = settings.market_endpoint.format(exchange=exchange)
    async with httpx.AsyncClient() as client:
        response = await client.get(endpoint)
        response_data = response.json()

    return response_data.get("result")


async def get_best_market(exchanges: List):
    """Find the best market through exchange list"""
    try:
        exchanges_list = strtolist(exchanges)
        best_exchange = None
        max_price = 0.0

        for exchange in exchanges_list:
            exchange_data = await get_exchange_price(exchange)
            price = exchange_data.get("price")

            if isinstance(price, (int, float)) and price > max_price:
                max_price = price
                best_exchange = exchange
        log.info(
            "Best market: %s with price: %s",
            best_exchange,
            max_price,
        )
        return {"exchange": best_exchange, "price": max_price}

    except Exception as e:
        log.error(e)
