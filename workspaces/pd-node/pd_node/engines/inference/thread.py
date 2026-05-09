import time
from datetime import datetime

from ultralytics import YOLO
import numpy as np

from pd_node.utils import get_base_path
import pd_node.db as db

model = YOLO(get_base_path() / "models/yolo11n_ncnn_model", task="detect")

session = db.create_session()

def thread(state):

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

        results = model.track(
            frame,
            persist=True,
            tracker="bytetrack.yaml",
            verbose=False
        )[0]

        state.inference.set_results(results)

        for box in results.boxes:
            pass
            #name = model.names[int(box.cls[0])]
            #confidence = float(box.conf[0])
            #record = db.models.ObjectDetection(name=name, confidence=confidence, model="yolo11n")
            #session.add(record)
        session.commit()

        time.sleep(1/15)

def log(msg):
    print("[inference_thread]:" + msg)
