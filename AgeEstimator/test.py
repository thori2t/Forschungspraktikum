# %%
import cv2
import numpy as np
import requests
import torch
from transformers import AutoConfig, AutoImageProcessor, AutoModelForImageClassification
from matplotlib import pyplot as plt

# load model and image processor
config = AutoConfig.from_pretrained(
    "iitolstykh/mivolo_v2", trust_remote_code=True
)
mivolo_model = AutoModelForImageClassification.from_pretrained(
    "iitolstykh/mivolo_v2", trust_remote_code=True, torch_dtype=torch.float16
)
image_processor = AutoImageProcessor.from_pretrained(
    "iitolstykh/mivolo_v2", trust_remote_code=True
)

# download test image
resp = requests.get('https://www.tu-chemnitz.de/tu/aktuelles/2024/1707405601-12298-1.jpg')
arr = np.asarray(bytearray(resp.content), dtype=np.uint8)
image = cv2.imdecode(arr, -1)

# face crops
x1, y1, x2, y2 = [625,  46, 686, 121]
faces_crops = [image[y1:y2, x1:x2]]  # may be [None] if bodies_crops is not None

# body crops
x1, y1, x2, y2 = [534,  16, 790, 559]
bodies_crops = [image[y1:y2, x1:x2]]  # may be [None] if faces_crops is not None

# prepare BGR inputs
faces_input = image_processor(images=faces_crops)["pixel_values"]
body_input = image_processor(images=bodies_crops)["pixel_values"]

faces_input = faces_input.to(dtype=mivolo_model.dtype, device=mivolo_model.device)
body_input = body_input.to(dtype=mivolo_model.dtype, device=mivolo_model.device)

# inference
output = mivolo_model(faces_input=faces_input, body_input=body_input)

# print results
age = output.age_output[0].item()
print(f"age: {round(age, 2)}")

id2label = config.gender_id2label
gender = id2label[output.gender_class_idx[0].item()]
gender_prob = output.gender_probs[0].item()
print(f"gender: {gender} [{int(gender_prob * 100)}%]")
