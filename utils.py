import cv2
import numpy as np

IMG_SIZE = 128

def preprocess_image(image):
    image = image.convert("RGB")
    img = np.array(image)
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img
