from pixelart import new_grid, rect, px, render

W, H = 15, 15

LEAF = "#2d6a4f"
LEAF_DK = "#1b4332"
THORN = "#40916c"
MOUTH = "#5c1a2e"
MOUTH_OPEN = "#ff6f3c"
EYE = "#ffe066"


def build(open_mouth):
    g = new_grid(W, H)
    # round bush body
    rect(g, 3, 2, 11, 12, LEAF)
    rect(g, 2, 4, 12, 10, LEAF)
    rect(g, 4, 1, 10, 1, LEAF)
    rect(g, 3, 12, 11, 13, LEAF_DK)

    # thorn spikes poking out
    for x in (1, 5, 9, 13):
        px(g, x, 6, THORN)
        px(g, x, 7, THORN)
    px(g, 7, 0, THORN)

    # angry eyes
    px(g, 5, 6, EYE)
    px(g, 9, 6, EYE)

    # mouth
    color = MOUTH_OPEN if open_mouth else MOUTH
    rect(g, 6, 8, 8, 9, color)
    if open_mouth:
        px(g, 7, 10, MOUTH_OPEN)

    return g


render(build(False), "thorn-bush-idle.svg", scale=2)
render(build(True), "thorn-bush-fire.svg", scale=2)
