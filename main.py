import asyncio
import curses
import random
import time
from typing import Coroutine

TIC_TIMEOUT = 0.1


def get_stars(
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


def get_courutines(canvas, stars: list[tuple]) -> list[Coroutine]:
    coroutines = []
    for star in stars:
        symbol, row, column = star
        coroutines.append(blink(canvas, row, column, symbol))
    return coroutines


def draw(canvas):
    curses.curs_set(False)
    canvas.border()

    canvas_height, canvas_width = curses.window.getmaxyx(canvas)
    stars = get_stars(
        n=150,
        symbols="+*.:",
        max_height=canvas_height,
        max_width=canvas_width,
        offset=3,  # offset from canvas borders
    )
    coroutines = get_courutines(canvas, stars)

    while True:
        for coroutine in coroutines:
            coroutine.send(None)
            canvas.refresh()
        time.sleep(TIC_TIMEOUT)


async def blink(canvas, row, column, symbol="*") -> Coroutine:
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(20):
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


if __name__ == "__main__":
    curses.update_lines_cols()
    curses.wrapper(draw)
