import numpy as np

REGION_LEFT = 0
REGION_RIGHT = 1
REGION_TOP = 2
REGION_BOTTOM = 3
REGIONS = [REGION_LEFT, REGION_BOTTOM, REGION_RIGHT, REGION_TOP]

STDV_WIDE = 2.5
STDV_NARROW = 2.0


def pick_starting_point(borders, filled=[], side=None):
    """
        Helps to pick random starting points in the four margins
    """
    rect = {
        "x": 0,
        "y": 0,
        "h": 0,
        "w": 0
    }
    ranges = _get_ranges(borders, side=side)
    rect["side"] = ranges["side"]
    rect["x"] = _random(ranges["xrange"])
    rect["y"] = _random(ranges["yrange"])
    rect["w"] = ranges["width"]-rect["x"]
    rect["h"] = ranges["height"]-rect["y"]
    return rect


def _narrow(center, add=0):
    return {
        "center": center,
        "stdv": center/STDV_NARROW,
        "add": add
    }


def _wide(center, add=0):
    return {
        "center": center,
        "stdv": center/STDV_WIDE,
        "add": add
    }


def _get_ranges(borders, side=None):
    side = np.random.choice(REGIONS) if side is None else side
    if side == REGION_LEFT:
        xrange = _narrow(borders["left"]/20.0)
        yrange = _wide(borders["inner_height"]/2.0, borders["top"])
        width = borders["left"]
        height = borders["top"]+borders["inner_height"]
    elif side == REGION_TOP:
        xrange = _wide(borders["image_width"]/2.0)
        yrange = _narrow(borders["top"]/10)
        width = borders["image_width"]
        height = borders["top"]
    elif side == REGION_BOTTOM:
        xrange = _wide(borders["image_width"]/2.0)
        yrange = _narrow(borders["bottom"] /
                         20.0, borders["top"]+borders["inner_height"])
        width = borders["image_width"]
        height = borders["image_height"]
    elif side == REGION_RIGHT:
        xrange = _narrow(borders["right"] /
                         20.0, borders["left"]+borders["inner_width"])
        yrange = _wide(borders["inner_height"]/2.0, borders["top"])
        width = borders["image_width"]
        height = borders["top"]+borders["inner_height"]
    return {
        "side": side,
        "xrange": xrange,
        "yrange": yrange,
        "width": width,
        "height": height
    }


def _random(rng):
    return max(int(rng["add"]+np.random.normal(rng["center"], rng["stdv"])), 0)


if __name__ == "__main__":
    borders = {'left': 229, 'top': 189, 'right': 238, 'bottom': 140, 'inner_height': 2970,
               'inner_width': 2082, 'image_width': 2550, 'image_height': 3300}

    print(pick_starting_point(borders))
