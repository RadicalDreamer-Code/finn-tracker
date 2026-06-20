from datetime import datetime, timezone

import aiosqlite

from app.domain.models import WatchlistEntry
from app.domain.ports import WatchlistRepository


class SqliteWatchlistRepository(WatchlistRepository):
    def __init__(self, db_path: str) -> None:
        self._db_path = db_path

    async def _ensure_table(self, conn: aiosqlite.Connection) -> None:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS watchlist (
                symbol TEXT PRIMARY KEY,
                added_at TEXT NOT NULL
            )
            """
        )
        await conn.commit()

    async def add(self, symbol: str) -> WatchlistEntry:
        now = datetime.now(timezone.utc)
        async with aiosqlite.connect(self._db_path) as conn:
            await self._ensure_table(conn)
            await conn.execute(
                "INSERT OR IGNORE INTO watchlist (symbol, added_at) VALUES (?, ?)",
                (symbol.upper(), now.isoformat()),
            )
            await conn.commit()
        return WatchlistEntry(symbol=symbol.upper(), added_at=now)

    async def remove(self, symbol: str) -> None:
        async with aiosqlite.connect(self._db_path) as conn:
            await self._ensure_table(conn)
            await conn.execute(
                "DELETE FROM watchlist WHERE symbol = ?", (symbol.upper(),)
            )
            await conn.commit()

    async def list_all(self) -> list[WatchlistEntry]:
        async with aiosqlite.connect(self._db_path) as conn:
            await self._ensure_table(conn)
            conn.row_factory = aiosqlite.Row
            async with conn.execute(
                "SELECT symbol, added_at FROM watchlist ORDER BY added_at DESC"
            ) as cursor:
                rows = await cursor.fetchall()
        return [
            WatchlistEntry(
                symbol=row["symbol"],
                added_at=datetime.fromisoformat(row["added_at"]),
            )
            for row in rows
        ]

    async def exists(self, symbol: str) -> bool:
        async with aiosqlite.connect(self._db_path) as conn:
            await self._ensure_table(conn)
            async with conn.execute(
                "SELECT 1 FROM watchlist WHERE symbol = ?", (symbol.upper(),)
            ) as cursor:
                return await cursor.fetchone() is not None
