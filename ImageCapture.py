import cv2
import numpy as np
from PIL import Image

cap = cv2.VideoCapture(0)
size = (640, 480)

if not cap.isOpened():
    raise Exception("Could not open video device")

ret, frame = cap.read()

if not ret:
    raise Exception("Could not read frame from video device")

grayscale16 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

print(grayscale16.size)

grayscale16 = cv2.resize(grayscale16, size)
print(grayscale16.shape)

grayscale16 = np.reshape(grayscale16, (np.product(grayscale16.shape),))
print(grayscale16.shape)

stringsend = grayscale16.tobytes()

stringrecv = np.fromstring(stringsend, dtype=int)

grayscale16 = np.reshape(grayscale16, (480, 640))
print(grayscale16.shape)





cv2.imwrite('grayscale.png', grayscale16)

# Release the webcam
cap.release()
