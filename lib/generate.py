import cv2
import numpy as np
import os
import json
from lib.split import split
from lib.augment import augment
from lib.parse_ascii import load_ascii
from random import shuffle

PNG_PATH = "data/paper/png"
OUTPUT_PATH = "data/final"
TRUTH_PATH = os.path.join(OUTPUT_PATH, "truth")
PAPER_PATH = os.path.join(OUTPUT_PATH, "paper")
STRIPPED_PATH = os.path.join(OUTPUT_PATH, "stripped")

DEV_FRAC = 0.1
TEST_FRAC = 0.1

paths = {
    "dev": os.path.join(OUTPUT_PATH, "dev"),
    "train": os.path.join(OUTPUT_PATH, "train"),
    "test": os.path.join(OUTPUT_PATH, "test")
}


def get_output_path(base, num, suffix):
    return os.path.join(base, "{}-{}.png".format(str(num).zfill(5), suffix))


def dumpTruthJson(path, data, num):
    with open(os.path.join(path, "{}-truth.json".format(str(num).zfill(5))), 'w+') as f:
        json.dump(data, f)


def dumpJson(path, data, name):
    with open(os.path.join(path, "{}.json".format(name)), 'w+') as f:
        json.dump(data, f)


def create_set(subset, files, words, total):
    global index
    for file in files:
        if file.endswith(".png"):
            print("file {} ({} %)".format(file, int(index/total*100)))
            img = cv2.imread(file, 1)
            img, stripped, ground_truth = augment(img, words)
            if img is not None:
                cv2.imwrite(get_output_path(
                    paths[subset], index, "paper"), img)
                cv2.imwrite(get_output_path(
                    paths[subset], index, "stripped"), stripped)
                dumpTruthJson(paths[subset], ground_truth, index)
                index += 1


if __name__ == "__main__":

    os.makedirs(paths["dev"], exist_ok=True)
    os.makedirs(paths["train"], exist_ok=True)
    os.makedirs(paths["test"], exist_ok=True)

    files = [os.path.join(PNG_PATH, file) for file in os.listdir(PNG_PATH)]

    word_dict = load_ascii("data/iam")
    key_train, key_dev, key_test = split(
        list(word_dict.keys()), DEV_FRAC, TEST_FRAC)
    word_train = [word_dict[key] for key in key_train]
    word_dev = [word_dict[key] for key in key_dev]
    word_test = [word_dict[key] for key in key_test]
    dumpJson(OUTPUT_PATH, key_dev, "dev")
    dumpJson(OUTPUT_PATH, key_train, "train")
    dumpJson(OUTPUT_PATH, key_test, "test")
    print("Words loaded!")

    LOOPS = 2
    index = 0

    for l in range(LOOPS):
        train, dev, test = split(files, DEV_FRAC, TEST_FRAC)
        create_set("train", train, word_train, len(files)*2)
        create_set("dev", dev, word_dev, len(files)*2)
        create_set("test", test, word_test, len(files)*2)
