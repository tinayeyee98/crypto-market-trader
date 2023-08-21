import requests
import structlog
from fastapi import APIRouter, FastAPI, HTTPException

from ..config import Settings, get_settings
from ..models.base_model import default_responses
from ..services.currency_services import get_best_market
from ..services.util import strtolist

log = structlog.get_logger()
settings: Settings = get_settings()

exchanges_list = strtolist(settings.exchanges)

router = APIRouter(
    tags=["Trading Orders Endpoints"],
    responses=default_responses,
)


@router.get("/orders/buy/{quantity}")
async def buy_order(quantity: float):
    try:
        best_market = await get_best_market(exchanges_list)
        log.info(
            "Best market: %s with price: %s",
            best_market["exchange"],
            best_market["price"],
        )

    except Exception as e:
        log.error(e)
