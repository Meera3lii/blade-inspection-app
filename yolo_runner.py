from ultralytics import YOLO
from PIL import Image
import io


model = YOLO("best.pt")

def run_inference(image_bytes: bytes, filename: str) -> dict:
   

    image = Image.open(io.BytesIO(image_bytes))

    results = model(image)

    detections = []
    for box in results[0].boxes:
        detections.append({
            "class": "Defect",
            "confidence": round(float(box.conf), 3),
            "bbox": box.xyxy[0].tolist()
        })


    annotated_image = results[0].plot()

    return {
        "filename": filename,
        "detections": detections,
        "annotated_image": annotated_image
    }