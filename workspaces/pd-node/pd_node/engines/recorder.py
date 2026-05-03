from pathlib import Path
import datetime
import os
import subprocess
import threading
import time

import cv2

VIDEO_DIR = "/var/lib/pd-node/videos"
os.makedirs(VIDEO_DIR, exist_ok=True)

def thread(state):

    writer = None

    video_name = None
    while True:
        if not state.recorder.is_running():
            if writer is not None:
                write_frames(state, writer)
                writer.release()
                writer = None
                convert_to_mp4_async(Path(video_name))
                print("Saved video")
            time.sleep(5)
            continue


        if writer is None:
            video_name = new_video_name()
            writer = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*"MJPG"), 15, (640, 480))

        write_frames(state, writer)
        
        time.sleep(2)

def write_frames(state, writer):

    frames = state.recorder.get_frames()

    for frame in frames:
        writer.write(frame)

def new_video_name():
    date_string = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") 
    return VIDEO_DIR + "/" + date_string + ".avi"

def convert_to_mp4_async(input_path):
    input_path = Path(input_path)
    output_path = input_path.with_suffix(".mp4")

    def worker():
        result = subprocess.Popen([
            "nice", "-n", "10",
            "ionice", "-c", "3",
            "ffmpeg",
            "-y",
            "-i", str(input_path),
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            str(output_path),
        ])

        if result.returncode == 0:
            input_path.unlink(missing_ok=True)
            print(f"Converted video: {output_path}")
        else:
            print(f"FFmpeg failed, kept original: {input_path}")

    threading.Thread(target=worker, daemon=True).start()
