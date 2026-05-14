from pathlib import Path
import datetime
import sys
import time

import cv2

from .stream import stream_video

def get_base_path():
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS).resolve()
    return Path(__file__).parent.parent.resolve()


def get_objects(object_name, boxes, names):
    objects = []

    for box in boxes:
        name = names[int(box.cls[0])]

        if name == object_name:
            objects.append(box)

    return objects

def now():
    return time.perf_counter() * 1000

fps_last_frame_time = now()
fps_frame_count = 0
fps = 0

def draw_fps(frame):
    global fps_last_frame_time
    global fps_frame_count
    global fps

    frame_time = now()
    fps_frame_count += 1

    ms_since_last_frame = frame_time - fps_last_frame_time

    if ms_since_last_frame >= 1000:
        fps = int(fps_frame_count / (ms_since_last_frame / 1000))
        fps_last_frame_time = frame_time
        fps_frame_count = 0

    height, width = frame.shape[:2]
    cv2.rectangle(frame, (0, height - 20), (65, height), (0,0,0), -1)
    cv2.putText(frame, f"FPS: {fps}", (0, height - 5), cv2.FONT_HERSHEY_SIMPLEX, .5, (140, 140, 140), 1, cv2.LINE_AA)

def draw_datetime(frame):
    height, width = frame.shape[:2]

    date_string = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") 
    cv2.rectangle(frame, (width - 185, height - 20), (width, height), (0,0,0), -1)
    cv2.putText(frame, date_string, (width - 185, height -5), cv2.FONT_HERSHEY_SIMPLEX, .5, (140, 140, 140), 1, cv2.LINE_AA)

def draw_recording_indicator(frame):
    height, width = frame.shape[:2]

    cv2.circle(frame, (10, 10), 4, (0, 0, 170), -1)
    cv2.putText(frame, "Rec", (20, 15), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 170), 1, cv2.LINE_AA)

def draw_move_left(frame):
    _draw_arrows(frame, active="left")


def draw_move_right(frame):
    _draw_arrows(frame, active="right")


def draw_move_up(frame):
    _draw_arrows(frame, active="up")


def draw_move_down(frame):
    _draw_arrows(frame, active="down")


def _draw_arrows(frame, active=None):
    height, width = frame.shape[:2]

    key_size = 24
    spacing = 8

    # Lower center placement
    base_x = width // 2
    base_y = height - 35

    inactive_bg = (40, 40, 40)
    active_bg = (255, 255, 255)

    inactive_fg = (180, 180, 180)
    active_fg = (0, 0, 0)

    positions = {
        "up": (
            base_x - key_size // 2,
            base_y - key_size - spacing,
        ),

        "left": (
            base_x - key_size - spacing - spacing,
            base_y,
        ),

        "down": (
            base_x - key_size // 2,
            base_y,
        ),

        "right": (
            base_x + key_size // 2 + spacing,
            base_y,
        ),
    }

    for direction, (x, y) in positions.items():

        is_active = direction == active

        bg = active_bg if is_active else inactive_bg
        fg = active_fg if is_active else inactive_fg

        cv2.rectangle(
            frame,
            (x, y),
            (x + key_size, y + key_size),
            bg,
            -1,
        )

        cv2.rectangle(
            frame,
            (x, y),
            (x + key_size, y + key_size),
            (120, 120, 120),
            1,
        )

        _draw_arrow_icon(
            frame,
            direction,
            x,
            y,
            key_size,
            fg,
        )


def _draw_arrow_icon(frame, direction, x, y, size, color):
    cx = x + size // 2
    cy = y + size // 2

    length = 5
    thickness = 1

    if direction == "left":
        start = (cx + length, cy)
        end = (cx - length, cy)

    elif direction == "right":
        start = (cx - length, cy)
        end = (cx + length, cy)

    elif direction == "up":
        start = (cx, cy + length)
        end = (cx, cy - length)

    else:
        start = (cx, cy - length)
        end = (cx, cy + length)

    cv2.arrowedLine(
        frame,
        start,
        end,
        color,
        thickness,
        tipLength=0.45,
        line_type=cv2.LINE_AA,
    )
