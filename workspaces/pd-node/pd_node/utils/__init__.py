from pathlib import Path
import datetime
import sys
import time

import cv2
from linuxpy.video.device import iter_video_capture_devices

def get_base_path():
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS).resolve()
    return Path(__file__).parent.parent.resolve()

def draw_bboxes(frame, boxes, names):
    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        conf = float(box.conf[0])
        cls = int(box.cls[0])
        label = f"{names[cls]} {conf:.2f}"
        #if not names[cls] == "bird":
        #    continue
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, label, (x1, max(20, y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)

def get_webcams():
    webcams = []

    for device in iter_video_capture_devices():

        with device:
            caps = dir(device.info.capabilities)

            if "bcm2835" in str(device.info.card):
                continue

            if "VIDEO_CAPTURE" in caps or "VIDEO_CAPTURE_MPLANE" in caps:
                webcams.append(device)

    return webcams

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

# Compatibility check for running the same code on non-Rpi devices
detection_pin = 23
try:
    import RPi.GPIO as GPIO

    PIN = 37

    MIN_DUTY = 1.8
    MAX_DUTY = 13.05

    # ---- servo setup (global) ----
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PIN, GPIO.OUT)

    pwm = GPIO.PWM(PIN, 50)
    pwm.start(0)

    def set_angle(angle: float):
        angle = max(0, min(100, angle))
        duty = MIN_DUTY + (angle / 100.0) * (MAX_DUTY - MIN_DUTY)

        pwm.ChangeDutyCycle(duty)
        time.sleep(0.4)
        pwm.ChangeDutyCycle(0)

    def set_led(on):
        GPIO.output(detection_pin, GPIO.HIGH if on else GPIO.LOW)

except Exception as e:
    print("Failed to probe rpi stuff", e)

    def set_led(on):
        print(f"Turning LED {'ON' if on else 'OFF'}") 

    def set_angle(angle: float):
        print(f"Setting angle {angle}")



