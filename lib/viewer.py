import os
import cv2
import numpy as np

from lib.generate import PAPER_PATH

if __name__ == "__main__":
    files = [os.path.join(PAPER_PATH, file) for file in os.listdir(PAPER_PATH)]

    while True:
        img_path = np.random.choice(files)
        img = cv2.imread(img_path)
        cv2.imshow(img_path, cv2.resize(img, (600, 800)))
        cv2.waitKey(0)
