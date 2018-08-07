def blend(x, y, w, h, target, copy):
    th, tw = target.shape[:2]
    if x >= tw or y >= th:
        return
    cx = -min(0, x)
    cy = -min(0, y)
    cw = w - (max(tw, x+w)-tw)
    ch = h - (max(th, y+h)-th)
    if max(ch-cy, 0) == 0 or max(cw-cx, 0) == 0:
        return False
    target[max(0, y):y+ch, max(0, x):x+cw, :] &= copy[cy:ch, cx:cw, :]
    return True
