import asyncio
import curses
import random
import time
from types import coroutine
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


def get_stars_courutines(canvas, stars: list[tuple]) -> list[Coroutine]:
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
    stars_coroutines = get_stars_courutines(canvas, stars)
    rocket = fire(canvas, int(canvas_height / 2), int(canvas_width / 2))
    coroutines = [rocket, *stars_coroutines]

    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)

        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


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


async def fire(
    canvas,
    start_row: int,
    start_column: int,
    rows_speed: float = -0.3,
    columns_speed: int = 0,
):
    """Display animation of gun shot, direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), "*")
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), "O")
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), " ")

    row += rows_speed
    column += columns_speed

    symbol = "-" if columns_speed else "|"

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), " ")
        row += rows_speed
        column += columns_speed


if __name__ == "__main__":
    curses.update_lines_cols()
    curses.wrapper(draw)
