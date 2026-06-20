from datetime import datetime, timedelta, timezone

import httpx

_cached_rate: float | None = None
_cached_at: datetime | None = None
_CACHE_TTL = timedelta(hours=1)


async def fetch_eur_rate() -> float:
    global _cached_rate, _cached_at
    now = datetime.now(timezone.utc)
    if (
        _cached_rate is not None
        and _cached_at is not None
        and now - _cached_at < _CACHE_TTL
    ):
        return _cached_rate

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://api.frankfurter.dev/v1/latest",
            params={"from": "USD", "to": "EUR"},
            timeout=5,
        )
        resp.raise_for_status()
        data = resp.json()

    _cached_rate = float(data["rates"]["EUR"])
    _cached_at = now
    return _cached_rate
