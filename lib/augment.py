import cv2
import numpy as np
from lib.border_detection import border_detection
from lib.starting_point import pick_starting_point, REGIONS, REGION_LEFT, REGION_TOP, REGION_BOTTOM, REGION_RIGHT
from lib.blend import blend
from lib.preprocess import preprocess_paper, preprocess_word
import pprint

pp = pprint.PrettyPrinter(indent=4)

BASEPATH = "data/iam"

DEFAULT_NUM_WORDS = {"center": 7, "stdv": 2}
DEFAULT_NUM_PARAGRAPHS = {"center": 3, "stdv": 1}

OVERFLOW_HORIZ_FACTOR = {
    REGION_LEFT: 1.1,
    REGION_TOP: 1,
    REGION_BOTTOM: 1,
    REGION_RIGHT: 1
}

OVERFLOW_VERT_FACTOR = {
    REGION_LEFT: 1,
    REGION_TOP: 1.1,
    REGION_BOTTOM: 0.75,
    REGION_RIGHT: 1
}

LEGAL_SHORT_WORDS = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
                     "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]


def augment(paper_img, words, num_words=DEFAULT_NUM_WORDS, region_prob=0.7):
    truth = np.full(paper_img.shape, 255, dtype=paper_img.dtype)
    paper_img = preprocess_paper(paper_img)
    borders = border_detection(paper_img)
    if borders is None:
        return None, None, None
    ground_truth = []
    for region in REGIONS:
        if np.random.uniform() < region_prob:
            ground_truth.extend(_augment_paragraph(truth, np.random.choice(
                words), borders, region, num_words))
    paper_img[:, :, :] &= truth
    return paper_img, truth, ground_truth


def _augment_paragraph(truth, words, borders, side, num_words):
    text_rect = pick_starting_point(borders, side=side)
    ground_truth = []
    x = text_rect["x"]
    y = text_rect["y"]
    max_y = 0
    n_words = _random(**num_words)
    start = int(np.random.uniform(0, len(words)-n_words))
    line_offset = None
    positions = []
    i = 0
    scaling = 1
    line_overheads = [0]
    new_line = False
    for word in words:
        # Load word
        word_img = preprocess_word(BASEPATH, word)
        if word_img is None:
            continue
        if line_offset == None:
            line_offset = word["offset"]
        # Calculate spacing between this and previous word
        if x != text_rect["x"]:
            spacing = word["spacing"] if word["spacing"] > - \
                1 else int(np.random.normal(word["height"]/2.0, 1.0))
            x += spacing
            if (x + word["width"]-text_rect["x"]) > (text_rect["w"]*OVERFLOW_HORIZ_FACTOR[side]) and (len(word["truth"]) > 1 or word["truth"] in LEGAL_SHORT_WORDS):
                y = y + max_y + int(max_y/5.0)
                x = int(abs(np.random.normal(text_rect["x"], 3.0)))
                max_y = 0
                line_offset = word["offset"]
                line_overheads.append(0)
        if side == REGION_RIGHT or side == REGION_BOTTOM:
            line_overheads[len(line_overheads)-1] = int(abs(np.random.normal(max(
                line_overheads[len(line_overheads)-1], (x + word["width"]-text_rect["x"])-text_rect["w"]), 3.0)))
        if (y + word["height"] + word["offset"] - line_offset - text_rect["y"]) / OVERFLOW_VERT_FACTOR[side] > text_rect["h"]:
            continue
        positions.append({
            "line": len(line_overheads)-1,
            "truth": word["truth"],
            "img": word_img,
            "x": x,
            "y": y+word["offset"]-line_offset,
            "width": word["width"],
            "height": word["height"]
        })
        max_y = max(max_y, word["offset"]+word["height"]-line_offset)
        x += word["width"]
        i += 1
    for position in positions:
        if not blend(position["x"]-line_overheads[position["line"]], position["y"], int(position["width"]),
                     int(position["height"]), truth, position["img"]):
            continue
        ground_truth.append(_truth(position["truth"], position["x"]-line_overheads[position["line"]], position["y"],
                                   position["height"], position["width"], side, position["line"]))
    return ground_truth


def _random(center, stdv=2):
    return int(np.random.normal(center, stdv))


def _scale(img, factor):
    h, w = img.shape[:2]
    h = int(h * factor)
    w = int(w * factor)
    return cv2.resize(img, (w, h))


def _truth(text, x, y, h, w, side, line):
    return {
        "text": text,
        "x": x,
        "y": y,
        "h": h,
        "w": w,
        "side": side,
        "line": line
    }
