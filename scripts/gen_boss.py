from pixelart import new_grid, rect, px, render

W, H = 34, 40

LOBE = "#3a8f4f"
LOBE_LT = "#5fbf6f"
LOBE_DK = "#1f5c30"
STALK = "#2d6a4f"
STALK_DK = "#1b4332"
MOUTH = "#a01f3a"
MOUTH_DK = "#6e1226"
TOOTH = "#fff2e0"
EYE = "#ffe066"
EYE_DK = "#3a2a00"
VINE = "#40916c"


def build():
    g = new_grid(W, H)

    # --- root/stalk base ---
    rect(g, 13, 30, 20, 39, STALK)
    rect(g, 13, 30, 15, 39, STALK_DK)
    rect(g, 11, 37, 22, 39, STALK_DK)
    # root arms spreading out at the base
    rect(g, 4, 34, 12, 36, VINE)
    rect(g, 21, 34, 29, 36, VINE)
    rect(g, 2, 36, 6, 38, STALK_DK)
    rect(g, 27, 36, 31, 38, STALK_DK)

    # --- lower jaw lobe (the "cup") ---
    rect(g, 6, 20, 27, 31, LOBE)
    rect(g, 8, 30, 25, 32, LOBE_DK)
    rect(g, 6, 20, 8, 30, LOBE_LT)
    rect(g, 25, 20, 27, 30, LOBE_DK)
    # red gullet inside lower lobe
    rect(g, 9, 22, 24, 29, MOUTH)
    rect(g, 9, 27, 24, 29, MOUTH_DK)
    # trigger-hair speckles inside
    for (x, y) in [(12, 24), (16, 25), (20, 24)]:
        px(g, x, y, "#d46a80")

    # --- upper jaw lobe (opened up, hinged back) ---
    rect(g, 6, 6, 27, 16, LOBE)
    rect(g, 8, 4, 25, 6, LOBE)
    rect(g, 6, 6, 8, 16, LOBE_LT)
    rect(g, 25, 6, 27, 16, LOBE_DK)
    rect(g, 6, 15, 27, 16, LOBE_DK)
    # red interior of upper lobe
    rect(g, 9, 9, 24, 15, MOUTH)
    rect(g, 9, 9, 24, 10, MOUTH_DK)

    # --- interlocking spike teeth along both jaw rims ---
    for tx in range(7, 27, 3):
        # upper lobe teeth point DOWN toward the gap
        rect(g, tx, 16, tx, 18, TOOTH)
        px(g, tx, 18, "#e8d8c0")
        # lower lobe teeth point UP toward the gap
        rect(g, tx + 1, 18, tx + 1, 20, TOOTH)
        px(g, tx + 1, 18, "#e8d8c0")

    # --- menacing eyes on the upper lobe ---
    rect(g, 10, 7, 13, 10, EYE)
    rect(g, 20, 7, 23, 10, EYE)
    px(g, 11, 8, EYE_DK)
    px(g, 21, 8, EYE_DK)
    # angry brow ridges
    rect(g, 10, 6, 13, 6, LOBE_DK)
    rect(g, 20, 6, 23, 6, LOBE_DK)

    return g


def build_flash():
    g = build()
    for row in g:
        for x in range(len(row)):
            if row[x] is not None:
                row[x] = "#ffffff"
    return g


render(build(), "boss-body.svg", scale=3, outline="#0a2015")
render(build_flash(), "boss-body-flash.svg", scale=3, outline="#0a2015")

# ---- boss heavy projectile: a menacing spiked energy orb ----
CORE = "#eaffff"
MID = "#b5179e"
OUTER = "#6a1b6f"
SPIKE = "#ff6fb5"
g = new_grid(16, 16)
rect(g, 4, 1, 11, 14, OUTER)
rect(g, 1, 4, 14, 11, OUTER)
rect(g, 3, 3, 12, 12, OUTER)
rect(g, 5, 3, 10, 12, MID)
rect(g, 3, 5, 12, 10, MID)
rect(g, 6, 5, 9, 10, CORE)
rect(g, 5, 6, 10, 9, CORE)
for (x, y) in [(0, 7), (0, 8), (15, 7), (15, 8), (7, 0), (8, 0), (7, 15), (8, 15)]:
    px(g, x, y, SPIKE)
render(g, "boss-orb.svg", scale=2, outline="#2a0a2e")
