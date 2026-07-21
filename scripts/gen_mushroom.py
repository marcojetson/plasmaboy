from pixelart import new_grid, rect, px, render

# 2px of horizontal padding on each side so the head-shake tilt (and its 1px outline) never
# clips against the canvas edge.
PAD = 2
W, H = 14 + PAD * 2, 12

CAP = "#d6453c"
CAP_DK = "#a8332c"
SPOT = "#fff2e0"
STEM = "#f2d9a8"
STEM_DK = "#d9b87e"
EYE = "#1a1a2e"
BROW = "#5c1a1a"


def build(tilt=0):
    g = new_grid(W, H)
    o = PAD + tilt  # base x offset (padding) plus the head-shake tilt
    # cap dome
    rect(g, 1 + o, 1, 12 + o, 5, CAP)
    rect(g, 0 + o, 3, 13 + o, 5, CAP)
    px(g, 2 + o, 1, CAP_DK)
    px(g, 11 + o, 1, CAP_DK)
    # spots
    px(g, 3 + o, 2, SPOT)
    px(g, 9 + o, 2, SPOT)
    px(g, 6 + o, 3, SPOT)
    px(g, 2 + o, 4, SPOT)
    px(g, 11 + o, 4, SPOT)
    # cap shadow rim
    rect(g, 0 + o, 5, 13 + o, 5, CAP_DK)

    # stem/body (stays centered; only the cap/head shakes)
    b = PAD
    rect(g, 3 + b, 6, 10 + b, 11, STEM)
    rect(g, 3 + b, 10, 10 + b, 11, STEM_DK)

    # angry eyebrows + eyes
    px(g, 4 + b, 7, BROW)
    px(g, 5 + b, 7, BROW)
    px(g, 8 + b, 7, BROW)
    px(g, 9 + b, 7, BROW)
    px(g, 5 + b, 8, EYE)
    px(g, 8 + b, 8, EYE)

    return g


render(build(tilt=0), "mushroom-0.svg", scale=2)
render(build(tilt=1), "mushroom-1.svg", scale=2)
