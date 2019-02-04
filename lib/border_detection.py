import cv2
import numpy as np

WORKING_WIDTH = 300
WORKING_HEIGHT = 400


def border_detection(img):
    """
        Detects the margins of a given image by detecting its inner text.
        Returns an object describing the coordinates of this
        box of text.
    """
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ih, iw = img.shape
    x_factor = iw / WORKING_WIDTH
    y_factor = ih / WORKING_HEIGHT
    img = cv2.resize(img, (WORKING_WIDTH, WORKING_HEIGHT))
    img = 255 - img
    img = _threshold(img)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, np.ones((27, 27)))
    rect = _largest_rect(img)
    if rect is None:
        return rect
    x, y, w, h = rect
    return {
        "left": int(x*x_factor),
        "top": int(y*y_factor),
        "right": int(iw-((x+w)*x_factor)),
        "bottom": int(ih-((y+h)*y_factor)),
        "inner_height": int(h*y_factor),
        "inner_width": int(w*x_factor),
        "image_width": iw,
        "image_height": ih
    }


def _threshold(img):
    threshold = np.mean(img, axis=(0, 1))
    _, img = cv2.threshold(
        img, threshold, 255, cv2.THRESH_TOZERO + cv2.THRESH_OTSU)
    return img


def _largest_rect(img):
    im, contours, hierarchy = cv2.findContours(img,
                                               cv2.RETR_CCOMP,
                                               cv2.CHAIN_APPROX_SIMPLE)
    max_rect = None
    max_area = 0
    for cnt in contours:
        rect = cv2.boundingRect(cnt)
        x, y, w, h = rect
        if w*h > max_area:
            max_rect = rect
            max_area = w*h
    return max_rect
