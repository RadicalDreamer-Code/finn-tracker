from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.dependencies import (
    get_market_data_service,
    get_quote_history_repository,
)
from app.domain.models import (
    CompanyProfile,
    Quote,
    QuoteSnapshot,
    SymbolSearchResult,
)
from app.domain.ports import QuoteHistoryRepository
from app.services.market_data_service import MarketDataService

router = APIRouter(prefix="/stocks", tags=["stocks"])


@router.get("/search", response_model=list[SymbolSearchResult])
async def search_symbols(
    q: str = Query(..., min_length=1),
    service: MarketDataService = Depends(get_market_data_service),
):
    return await service.search_symbols(q)


@router.get("/{symbol}/quote", response_model=Quote)
async def get_quote(
    symbol: str,
    service: MarketDataService = Depends(get_market_data_service),
):
    try:
        return await service.get_quote(symbol)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Failed to fetch quote: {e}",
        )


@router.get("/{symbol}/history", response_model=list[QuoteSnapshot])
async def get_quote_history(
    symbol: str,
    limit: int = 500,
    repo: QuoteHistoryRepository = Depends(get_quote_history_repository),
):
    return await repo.get_history(symbol, limit=limit)


@router.get("/{symbol}/profile", response_model=CompanyProfile)
async def get_company_profile(
    symbol: str,
    service: MarketDataService = Depends(get_market_data_service),
):
    try:
        return await service.get_company_profile(symbol)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Failed to fetch profile: {e}",
        )
