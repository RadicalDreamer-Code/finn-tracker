from datetime import datetime, timezone

import aiosqlite

from app.domain.models import Quote, QuoteSnapshot
from app.domain.ports import QuoteHistoryRepository


class SqliteQuoteHistoryRepository(QuoteHistoryRepository):
    def __init__(self, db_path: str) -> None:
        self._db_path = db_path

    async def _ensure_table(self, conn: aiosqlite.Connection) -> None:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS quote_history (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol      TEXT NOT NULL,
                current_price REAL NOT NULL,
                change      REAL NOT NULL,
                change_percent REAL NOT NULL,
                high        REAL NOT NULL,
                low         REAL NOT NULL,
                open        REAL NOT NULL,
                prev_close  REAL NOT NULL,
                timestamp   TEXT NOT NULL,
                eur_rate    REAL NOT NULL,
                fetched_at  TEXT NOT NULL
            )
            """
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_qh_symbol_fetched "
            "ON quote_history (symbol, fetched_at DESC)"
        )
        await conn.commit()

    async def save(self, snapshot: QuoteSnapshot) -> None:
        async with aiosqlite.connect(self._db_path) as conn:
            await self._ensure_table(conn)
            # Skip duplicate: same Finnhub trade timestamp means no new tick
            async with conn.execute(
                "SELECT 1 FROM quote_history "
                "WHERE symbol = ? AND timestamp = ? LIMIT 1",
                (snapshot.symbol, snapshot.timestamp.isoformat()),
            ) as cur:
                if await cur.fetchone() is not None:
                    return
            await conn.execute(
                """
                INSERT INTO quote_history
                    (symbol, current_price, change, change_percent,
                     high, low, open, prev_close, timestamp,
                     eur_rate, fetched_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    snapshot.symbol,
                    snapshot.current_price,
                    snapshot.change,
                    snapshot.change_percent,
                    snapshot.high,
                    snapshot.low,
                    snapshot.open,
                    snapshot.prev_close,
                    snapshot.timestamp.isoformat(),
                    snapshot.eur_rate,
                    snapshot.fetched_at.isoformat(),
                ),
            )
            await conn.commit()

    async def get_latest(self, symbol: str) -> QuoteSnapshot | None:
        async with aiosqlite.connect(self._db_path) as conn:
            await self._ensure_table(conn)
            conn.row_factory = aiosqlite.Row
            async with conn.execute(
                "SELECT * FROM quote_history "
                "WHERE symbol = ? "
                "ORDER BY fetched_at DESC LIMIT 1",
                (symbol.upper(),),
            ) as cur:
                row = await cur.fetchone()
        return _row_to_snapshot(row) if row else None

    async def get_history(
        self, symbol: str, limit: int = 500
    ) -> list[QuoteSnapshot]:
        async with aiosqlite.connect(self._db_path) as conn:
            await self._ensure_table(conn)
            conn.row_factory = aiosqlite.Row
            async with conn.execute(
                "SELECT * FROM quote_history "
                "WHERE symbol = ? "
                "ORDER BY fetched_at DESC LIMIT ?",
                (symbol.upper(), limit),
            ) as cur:
                rows = await cur.fetchall()
        return [_row_to_snapshot(r) for r in rows]


def _row_to_snapshot(row: aiosqlite.Row) -> QuoteSnapshot:
    return QuoteSnapshot(
        symbol=row["symbol"],
        current_price=row["current_price"],
        change=row["change"],
        change_percent=row["change_percent"],
        high=row["high"],
        low=row["low"],
        open=row["open"],
        prev_close=row["prev_close"],
        timestamp=datetime.fromisoformat(row["timestamp"]),
        eur_rate=row["eur_rate"],
        fetched_at=datetime.fromisoformat(row["fetched_at"]),
    )
