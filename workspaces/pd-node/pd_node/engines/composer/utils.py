import cv2

def draw_bboxes(frame, boxes, names):
    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        conf = float(box.conf[0])
        cls = int(box.cls[0])
        track_id = None
        if box.id is not None:
            track_id = int(box.id[0]) if hasattr(box.id, "__len__") else int(box.id)
        else:
            track_id = "N/A"

        label = f"#{track_id}: {names[cls]} ({conf:.2f})"
        color = map_confidence_to_color(conf)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 1)
        cv2.putText(frame, label, (x1, max(20, y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 1, cv2.LINE_AA)


def map_confidence_to_color(confidence):
    if confidence < 0.2:
        return (0, 0, 0)

    if confidence > 0.75:
        return (0, 255, 0)

    return (0, int(255 * confidence), 0)
