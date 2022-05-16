import curses
import time

from animations.stars import create_stars, blink
from animations.fire import fire

TIC_TIMEOUT = 0.1


def draw(canvas):
    curses.curs_set(False)
    canvas.border()
    canvas_height, canvas_width = curses.window.getmaxyx(canvas)

    coroutines = []
    stars = create_stars(
        n=150,
        symbols="+*.:",
        max_height=canvas_height,
        max_width=canvas_width,
        offset=3,  # canvas borders offset
    )
    coroutines.extend(
        [blink(canvas, row, column, symbol) for symbol, row, column in stars]
    )
    fire_coroutine = fire(canvas, int(canvas_height / 2), int(canvas_width / 2))
    coroutines.append(fire_coroutine)

    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)

        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


if __name__ == "__main__":
    curses.update_lines_cols()
    curses.wrapper(draw)
