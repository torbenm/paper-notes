import os
from random import shuffle
from shutil import copy2


OUTPUT_PATH = "data/final"

TRAIN_PATH = os.path.join(OUTPUT_PATH, "train")
DEV_PATH = os.path.join(OUTPUT_PATH, "dev")
TEST_PATH = os.path.join(OUTPUT_PATH, "test")

DEV_SIZE = 0.1
TEST_SIZE = 0.1


def get_num(name: str):
    return name.split(".")[0].split("-")[0]


def filename(suffix: str, num: int, typ: str):
    return "{}-{}.{}".format(num, suffix, typ)


def copy_all(files, basepath):
    for file in files:
        n = get_num(file)
        copy2(os.path.join(PAPER_PATH, file), basepath)
        copy2(os.path.join(TRUTH_PATH, filename("truth", n, "json")), basepath)
        copy2(os.path.join(STRIPPED_PATH, filename("stripped", n, "png")), basepath)


def split(data, dev_frac, test_frac):
    shuffle(data)
    dev_end = int(len(data) * dev_frac)
    test_end = int(dev_end + len(data) * test_frac)
    return data[test_end:], data[:dev_end], data[dev_end:test_end]


if __name__ == "__main__":
    from lib.generate import PAPER_PATH, TRUTH_PATH, STRIPPED_PATH

    os.makedirs(TRAIN_PATH, exist_ok=True)
    os.makedirs(DEV_PATH, exist_ok=True)
    os.makedirs(TEST_PATH, exist_ok=True)

    files = os.listdir(PAPER_PATH)

    train, dev, test = split(files, DEV_SIZE, TEST_SIZE)

    copy_all(dev, DEV_PATH)
    copy_all(test, TEST_PATH)
    copy_all(train, TRAIN_PATH)
