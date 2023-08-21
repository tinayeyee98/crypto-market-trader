import structlog
from fastapi import APIRouter, HTTPException

from ..config import Settings, get_settings
from ..models.base_model import default_responses
from ..services.currency_services import search_market_n_place_order

log = structlog.get_logger()

router = APIRouter(
    tags=["Trading Orders Endpoints"],
    responses=default_responses,
)


@router.get("/trades/{side}/{quantity}")
async def excute_trade(side: str, quantity: float):
    if side not in ("buy", "sell"):
        raise HTTPException(status_code=400, detail="Invalid side{buy/sell}.")
    try:
        place_an_order = await search_market_n_place_order(side, quantity)

        return

    except Exception as e:
        log.error(e)
