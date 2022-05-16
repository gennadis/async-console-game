import curses
import time

from animations.stars import create_stars, blink
from animations.fire import fire
from animations.spaceship import animate_spaceship, load_frames

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
    frame_one, frame_two = load_frames(
        frame_one_filepath="animations/rocket_frame_1.txt",
        frame_two_filepath="animations/rocket_frame_2.txt",
    )

    spacechip = animate_spaceship(
        canvas,
        row=canvas_height - 15,
        column=int(canvas_width / 2),
        frame_one=frame_one,
        frame_two=frame_two,
    )
    coroutines.append(spacechip)

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
