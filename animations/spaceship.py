import asyncio
from itertools import cycle

from curses_tools import draw_frame, get_frame_size


def load_frames(
    frame_one_filepath: str,
    frame_two_filepath: str,
):
    with open(frame_one_filepath, "r") as file_one:
        frame_one = file_one.read()

    with open(frame_two_filepath, "r") as file_two:
        frame_two = file_two.read()

    return frame_one, frame_two


async def animate_spaceship(
    canvas, row: int, column: int, frame_one: str, frame_two: str
):
    frames = cycle([frame_one, frame_two])

    while True:
        frame = next(frames)

        frame_columns, frame_rows = get_frame_size(frame)
        frame_x_coordinate = column - round(frame_rows / 2)
        frame_y_coordinate = row - round(frame_columns / 2)

        draw_frame(canvas, frame_y_coordinate, frame_x_coordinate, frame)
        canvas.refresh()
        for _ in range(5):
            await asyncio.sleep(0)
        draw_frame(canvas, frame_y_coordinate, frame_x_coordinate, frame, negative=True)
