from mivolo.detector import PersonAndFaceDetector
import cv2
import numpy as np
import requests

resp = requests.get('https://www.tu-chemnitz.de/tu/aktuelles/2024/1707405601-12298-1.jpg')
arr = np.asarray(bytearray(resp.content), dtype=np.uint8)
image = cv2.imdecode(arr, -1)

detector = PersonAndFaceDetector(
    detector_path="yolov8n_face.pt",
    device="cpu",      # oder "cpu"
    verbose=False,
)
detected = detector.predict(image)   # liefert u. a. faces_crops und bodies_crops
