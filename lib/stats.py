import cv2
import numpy as np
import os
import json

test = "./data/final/test"
train = "./data/final/train"
dev = "./data/final/dev"
punctuatin = ",.;:!?\"'"

"""
    Generates a couple of stats on the Paper Notes dataset
"""


def get_sizes(base):
    sizes = []
    files = os.listdir(base)
    for file in files:
        if file.endswith("-paper.png"):
            file = cv2.imread(os.path.join(base, file))
            sizes.append(file.shape[0:2])
    return sizes


def average_size():
    sizes = []
    sizes.extend(get_sizes(test))
    print("Finished test")
    sizes.extend(get_sizes(train))
    print("Finished train")
    sizes.extend(get_sizes(dev))
    print("Finished dev")
    print("Average size:", np.average(sizes, axis=0))
    print("Minimum size:", np.min(sizes, axis=0))
    print("Maximum size:", np.max(sizes, axis=0))


f = {}


def filter_punct(entry):
    #print(entry["text"], entry["text"] in punctuatin)
    return entry["text"] not in punctuatin


def json_stats(folder):
    lines = 0
    paragraphs = 0
    words = 0
    words_wo_p = 0
    empty = 0
    total = 0
    files = os.listdir(folder)
    for file in files:
        if file.endswith("json"):
            with open(os.path.join(folder, file), 'r') as f:
                d = json.load(f)
                words += len(d)
                words_wo_p += len([item for item in d if filter_punct(item)])
                lines += len(set(map(lambda x: x["line"], d)))
                paragraphs += len(set(map(lambda x: x["side"], d)))
                if len(d) == 0:
                    empty += 1
                total += 1
    return lines, paragraphs, words, words_wo_p, empty, total


def full_json_stats():
    t_lines = 0
    t_paragraphs = 0
    t_words = 0
    t_words_wo_p = 0
    t_empty = 0
    t_total = 0
    lines, paragraphs, words, words_wo_p, empty, total = json_stats(test)
    t_lines += lines
    t_paragraphs += paragraphs
    t_words += words
    t_words_wo_p += words_wo_p
    t_empty += empty
    t_total += total
    lines, paragraphs, words, words_wo_p, empty, total = json_stats(train)
    t_lines += lines
    t_paragraphs += paragraphs
    t_words += words
    t_words_wo_p += words_wo_p
    t_empty += empty
    t_total += total
    lines, paragraphs, words, words_wo_p, empty, total = json_stats(dev)
    t_lines += lines
    t_paragraphs += paragraphs
    t_words_wo_p += words_wo_p
    t_words += words
    t_empty += empty
    t_total += total

    print("Lines", t_lines)
    print("Paragraphs", t_paragraphs)
    print("Words", t_words)
    print("Words w.o. Puncation", t_words_wo_p)
    print("Words per line", t_words_wo_p / t_lines)
    print("Empty", t_empty)
    print("Total", t_total)


if __name__ == "__main__":
    average_size()
    full_json_stats()
