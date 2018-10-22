import os
import cv2
import numpy as np
BASE = "./data/final/train"
files = os.listdir(BASE)
avgs = []
for idx, file in enumerate(files):
    if file.endswith("-stripped.png"):
        stripped = cv2.imread(os.path.join(BASE, file), cv2.IMREAD_GRAYSCALE)
        _, stripped = cv2.threshold(stripped, 250, 255, cv2.THRESH_BINARY)
        avgs.append(np.average(stripped))
        print(np.average(avgs))
