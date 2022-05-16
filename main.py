import asyncio
import time
import curses


def draw(canvas):
    row, column = (5, 20)
    curses.curs_set(False)
    canvas.border()

    coroutine = blink(canvas, row, column)

    coroutine.send(None)
    canvas.refresh()
    time.sleep(2)

    coroutine.send(None)
    canvas.refresh()
    time.sleep(0.3)

    coroutine.send(None)
    canvas.refresh()
    time.sleep(0.5)

    coroutine.send(None)
    canvas.refresh()
    time.sleep(0.3)

    time.sleep(3)


async def blink(canvas, row, column, symbol="*"):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)


if __name__ == "__main__":
    curses.update_lines_cols()
    curses.wrapper(draw)
