import cv2
import numpy as np
from lib.augment import augment
from lib.parse_ascii import load_ascii

org = cv2.imread("data/paper/png/10.1.1.716.6158-0.png", 1)
words = load_ascii("data/iam")
while True:
    img = org.copy()
    img, truth = augment(img, list(words.values()))
    cv2.imwrite("output.png", img)
    # cv2.imshow('', cv2.resize(img, (500, 700)))
    # cv2.waitKey(0)
    break
