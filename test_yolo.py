from yolo_runner import run_inference

image_path = r"C:\Users\meero\Downloads\Demo.v3-v2_aug_light.yolov8\test\images\100_png_jpg.rf.82ebd897a086c22fca172fc1bef27774.jpg"

with open(image_path, "rb") as f:
    image_bytes = f.read()

result = run_inference(image_bytes, "100_png_jpg.jpg")

print("Filename:", result["filename"])
print("Detections found:", len(result["detections"]))
for d in result["detections"]:
    print(f"  → {d['class']} | confidence: {d['confidence']}")