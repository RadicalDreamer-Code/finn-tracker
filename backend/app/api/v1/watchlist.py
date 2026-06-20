from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.core.dependencies import get_watchlist_service
from app.domain.models import WatchlistEntryWithQuote
from app.services.watchlist_service import WatchlistService

router = APIRouter(prefix="/watchlist", tags=["watchlist"])


class AddSymbolRequest(BaseModel):
    symbol: str


@router.get("", response_model=list[WatchlistEntryWithQuote])
async def list_watchlist(
    service: WatchlistService = Depends(get_watchlist_service),
):
    return await service.list_with_quotes()


@router.post("", response_model=WatchlistEntryWithQuote, status_code=status.HTTP_201_CREATED)
async def add_to_watchlist(
    body: AddSymbolRequest,
    service: WatchlistService = Depends(get_watchlist_service),
):
    try:
        entry = await service.add_symbol(body.symbol)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return WatchlistEntryWithQuote(entry=entry, quote=None)


@router.delete("/{symbol}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_from_watchlist(
    symbol: str,
    service: WatchlistService = Depends(get_watchlist_service),
):
    try:
        await service.remove_symbol(symbol)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
