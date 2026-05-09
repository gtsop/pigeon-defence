import os
import time

from pd_node.utils import get_base_path
from ultralytics import YOLO
import numpy as np

model = YOLO(get_base_path() / "models/yolo11n_ncnn_model", task="detect")

def thread(state):
    last_frame = None

    state.inference.set_names(model.names)

    while True:
        
        if not state.inference.is_running():
            state.inference.set_results(None)
            time.sleep(5)
            continue

        frame = state.video.get_frame()

        if frame is None:
            time.sleep(1/15)
            continue

        if np.array_equal(frame, last_frame):
            log("same frame, skipping")
            time.sleep(1/15)
            continue

        last_frame = frame

        results = model(frame, verbose=False)[0]

        state.inference.set_results(results)

        time.sleep(1/15)

def log(msg):
    print("[inference_thread]:" + msg)
