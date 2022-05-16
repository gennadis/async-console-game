import asyncio
import time
import curses


def draw(canvas):
    row, column = (5, 20)
    curses.curs_set(False)
    canvas.border()

    coroutines = [blink(canvas, row, column + i) for i in range(0, 25, 5)]

    while True:
        for coroutine in coroutines:
            coroutine.send(None)
            canvas.refresh()
        time.sleep(1)


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
