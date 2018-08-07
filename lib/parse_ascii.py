import os


def load_ascii(asciifolder):
    line_offsets = {}
    groups = {}
    last_x_end = 0
    last_line = ""
    with open(os.path.join(asciifolder, "ascii/words.txt"), "r") as lines:
        while True:
            line = lines.readline().strip()
            if not line:
                break
            if line[0] != "#":
                lsplit = line.split(" ")
                if lsplit[1] != "err":
                    path,  line = _get_image_path(lsplit[0])
                    groups[line] = [] if line not in groups else groups[line]
                    line_offsets[line] = int(
                        lsplit[4]) if line not in line_offsets else line_offsets[line]
                    text = ' '.join(lsplit[8:])
                    width = int(lsplit[5])
                    height = int(lsplit[6])
                    graylvl = int(lsplit[2])
                    spacing = int(lsplit[3]) - \
                        last_x_end if line == last_line else -1
                    last_line = line
                    last_x_end = int(lsplit[3]) + width
                    groups[line].append(
                        _word(path, text, int(lsplit[4]) - line_offsets[line], spacing, height, width, graylvl))
    return groups


def _get_image_path(identifier):
    idsplit = identifier.split("-")
    page = "-".join(idsplit[0:2])
    line = "-".join(idsplit[0:3])
    return os.path.join("words", "-".join(idsplit[0:1]), page, identifier + ".png"), line


def _word(filepath, truth, offset, spacing, height, width, graylevel):
    return {
        "file": filepath,
        "truth": truth,
        "height": height,
        "width": width,
        "offset": offset,
        "spacing": spacing,
        "graylevel": int(graylevel)
    }


if __name__ == "__main__":
    import cv2
    words = load_ascii("./data/iam")
    print(words)
    cv2.imshow("img", cv2.imread(
        os.path.join("data", "iam", words[0]["file"])))
    cv2.waitKey(0)
