from fastapi import APIRouter

from app.api.v1 import stocks, watchlist

router = APIRouter(prefix="/api/v1")
router.include_router(watchlist.router)
router.include_router(stocks.router)
