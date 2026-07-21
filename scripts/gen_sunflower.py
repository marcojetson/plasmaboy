from pixelart import new_grid, rect, px, render

W, H = 14, 14

PETAL = "#ffd23f"
PETAL_DK = "#e0a800"
CENTER = "#6b4423"
CENTER_DK = "#4a2f18"
BROW = "#3a2410"
EYE = "#1a1a2e"
GLOW = "#ff914d"


def build(angry_glow):
    g = new_grid(W, H)
    # petals ring
    rect(g, 4, 0, 9, 1, PETAL)
    rect(g, 4, 12, 9, 13, PETAL_DK)
    rect(g, 0, 4, 1, 9, PETAL)
    rect(g, 12, 4, 13, 9, PETAL_DK)
    rect(g, 1, 1, 3, 3, PETAL)
    rect(g, 10, 1, 12, 3, PETAL)
    rect(g, 1, 10, 3, 12, PETAL_DK)
    rect(g, 10, 10, 12, 12, PETAL_DK)

    # center face
    center = GLOW if angry_glow else CENTER
    rect(g, 3, 3, 10, 10, center)
    rect(g, 3, 8, 10, 10, CENTER_DK if not angry_glow else GLOW)

    # angry brows + eyes
    px(g, 4, 5, BROW)
    px(g, 5, 4, BROW)
    px(g, 8, 4, BROW)
    px(g, 9, 5, BROW)
    px(g, 5, 6, EYE)
    px(g, 8, 6, EYE)

    return g


render(build(False), "sunflower-idle.svg", scale=2)
render(build(True), "sunflower-fire.svg", scale=2)
