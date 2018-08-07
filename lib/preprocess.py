import cv2
import os


def preprocess_word(basepath, word):
    img = cv2.imread(os.path.join(basepath, word["file"]))
    if img is None:
        return None
    img = threshold(img, word["graylevel"])
    return img


def threshold(img, graylevel):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = 255 - img
    _, img = cv2.threshold(
        img, graylevel, 255, cv2.THRESH_TOZERO + cv2.THRESH_OTSU)
    img = 255 - img
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    return img


def preprocess_paper(img):
    return img
