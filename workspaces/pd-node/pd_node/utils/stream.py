import time

import cv2

def stream_video(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    delay = 1 / fps if fps and fps > 0 else 1 / 10

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        ok, jpg = cv2.imencode(".jpg", frame)
        if not ok:
            continue

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + jpg.tobytes() + b"\r\n"
        )

        time.sleep(delay)
    cap.release()
    
