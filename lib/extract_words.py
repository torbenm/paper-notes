import cv2
import os
import json
from .logger import set_prefix, progress
from .regionextractor import RegionExtractor


def calc_iou(boxA, boxB):
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA["x"], boxB["x"])
    yA = max(boxA["y"], boxB["y"])
    xB = min(boxA["w"]+boxA["x"], boxB["w"]+boxB["x"])
    yB = min(boxA["h"]+boxA["y"], boxB["h"]+boxB["y"])

    # compute the area of intersection rectangle
    interArea = max(0, xB - xA) * max(0, yB - yA)

    # compute the area of both the prediction and ground-truth
    # rectangles
    boxAArea = (boxA["w"] * boxA["h"])
    boxBArea = (boxB["w"] * boxB["h"])

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = interArea / float(boxAArea + boxBArea - interArea)

    # return the intersection over union value
    return iou


def loadJson(path, name=None):
    filepath = os.path.join(path, "{}.json".format(
        name)) if name is not None else path
    with open(filepath, 'r') as f:
        return json.load(f)


def extract_words(indir, outdir, pure=False):
    files = os.listdir(indir)
    os.makedirs(outdir, exist_ok=True)
    words = {}
    for idx, file in enumerate(files):
        if file.endswith("-paper.png"):
            num = file.split("-")[0]
            words.update(process_file_for_words(indir, num, outdir, pure))
            progress(idx, len(files))
    dumpJson(outdir, words, "words")


def extract_print(indir, outdir):
    files = os.listdir(indir)
    os.makedirs(outdir, exist_ok=True)
    progress(0, len(files))
    for idx, file in enumerate(files):
        if file.endswith("-paper.png"):
            num = file.split("-")[0]
            process_file_for_print(indir, num, outdir)
            progress(idx, len(files))


def dumpJson(path, data, name):
    with open(os.path.join(path, "{}.json".format(name)), 'w+') as f:
        json.dump(data, f)


def process_file_for_words(path, num, outdir, pure):
    ending = "paper" if not pure else "stripped"
    img = cv2.imread(os.path.join(path, "{}-{}.png".format(num, ending)))
    gts = loadJson(path, "{}-truth".format(num))
    words = {}
    for i, gt in enumerate(gts):
        x = max(0, gt["x"])
        y = max(0, gt["y"])
        w = gt["w"]
        h = gt["h"]
        words["{}-{}".format(num, i)] = gt["text"]
        cv2.imwrite(os.path.join(outdir, "{}-{}.png".format(num, i)),
                    img[y:y+h, x:x+w, :])
    return words


def process_file_for_print(path, num, outdir):
    img = cv2.imread(os.path.join(path, "{}-paper.png".format(num)))
    gts = loadJson(path, "{}-truth".format(num))
    regions = RegionExtractor(img).extract()
    i = 0
    for region in regions:
        x, y = region.pos
        w, h = region.size
        reg_box = {
            "x": x,
            "y": y,
            "w":  w,
            "h":  h
        }
        max_iou = 0
        for gt in gts:
            max_iou = max(max_iou, calc_iou(reg_box, gt))
        if max_iou == 0:
            cv2.imwrite(os.path.join(
                outdir, "{}-{}.png".format(num, i)), region.img)
            i += 1


if __name__ == "__main__":
    set_prefix("Dev  Words")
    extract_words("./data/final/dev", "./data/words/dev")
    set_prefix("Test Words")
    extract_words("./data/final/test", "./data/words/test")
    set_prefix("Train Words")
    extract_words("./data/final/train", "./data/words/train")
    set_prefix("Dev  Pure")
    extract_words("./data/final/dev", "./data/words/pure_dev", True)
    set_prefix("Test Pure")
    extract_words("./data/final/test", "./data/words/pure_test", True)
    set_prefix("Train Pure")
    extract_words("./data/final/train", "./data/words/pure_train", True)
    set_prefix("Dev  Print")
    extract_print("./data/final/dev", "./data/words/print_dev")
    set_prefix("Test Print")
    extract_print("./data/final/test", "./data/words/print_test")
    set_prefix("Train Print")
    extract_print("./data/final/train", "./data/words/print_train")
