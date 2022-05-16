import asyncio
import curses
import random
from typing import Coroutine


def create_stars(
    n: int, symbols: str, max_height: int, max_width: int, offset: int
) -> list[tuple]:
    return [
        (
            random.choice(list(symbols)),
            random.randint(offset, max_height - offset),
            random.randint(offset, max_width - offset),
        )
        for _ in range(n)
    ]


async def blink(canvas, row, column, symbol="*") -> Coroutine:
    while True:
        dimmed_tics = random.randint(0, 20)
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(dimmed_tics):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(3):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(5):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(3):
            await asyncio.sleep(0)
