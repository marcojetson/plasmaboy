"""Beach-biome sprite set (see src/config/themes.ts 'beach').

Sunny seaside: warm sand underfoot, big impassable pools of sea (the extraObstacles:'seaWater'
branch in HuntScene draws + blocks those), clustered coconut palms, and a rolling-coconut
walker. Regular foes reuse the underwater biome's skins (urchin / anemone / eel / bloom / fish)
since a beach IS the sea's edge. The boss is a giant carnivorous pineapple.

Palm trees are authored on a 24x34 grid at scale 3 (72x102) to match the forest bg-trees, so
the shared treeLike trunk-collider in HuntScene.placeObstacles lands on the trunk.
"""
from pixelart import new_grid, rect, px, render

# ======================================================================================
# Tile (scale 2, no outline) — warm beach sand, flush at the top
# ======================================================================================
SAND = "#f0d9a0"
SAND_DK = "#dcc07e"
SAND_LT = "#faedc4"
GRAIN = "#c9a866"
g = new_grid(16, 16)
rect(g, 0, 0, 15, 15, SAND)
rect(g, 0, 0, 15, 0, SAND_LT)             # bright sunlit crest
rect(g, 0, 6, 15, 6, SAND_DK)             # soft seam
for (x, y) in [(3, 4), (10, 8), (13, 3), (6, 11), (2, 13), (14, 10)]:
    px(g, x, y, GRAIN)
for (x, y) in [(8, 2), (5, 9), (12, 13)]:
    px(g, x, y, SAND_LT)
px(g, 11, 5, "#e8f0ff")                   # a tiny shell fleck
render(g, "tile-beach.svg", scale=2, outline=None)

# ======================================================================================
# Obstacle — coconut palm (SIGNATURE, treeLike so it clusters). 24x34 grid, scale 3.
# ======================================================================================
TRUNK = "#a9743e"
TRUNK_DK = "#7c5228"
TRUNK_LT = "#c79157"
FROND = "#3f9a4a"
FROND_DK = "#2c6e35"
FROND_LT = "#63bf5f"
COCO = "#6b4324"

def palm():
    g = new_grid(24, 34)
    # gently leaning trunk, base at bottom-center
    for y in range(13, 34):
        lean = (33 - y) // 6            # curve toward the top
        x0 = 10 - lean
        rect(g, x0, y, x0 + 3, y, TRUNK)
        px(g, x0, y, TRUNK_LT)
        px(g, x0 + 3, y, TRUNK_DK)
        if y % 3 == 0:
            rect(g, x0, y, x0 + 3, y, TRUNK_DK)   # ring segments
    # crown knob
    rect(g, 6, 10, 11, 13, TRUNK_DK)
    # coconuts under the crown
    for (cx, cy) in [(6, 11), (11, 11), (8, 13)]:
        rect(g, cx, cy, cx + 1, cy + 1, COCO)
    # drooping fronds radiating from the crown (~8,10)
    fronds = [
        [(8, 9), (5, 7), (1, 6), (0, 8)],          # far left, drooping
        [(8, 9), (5, 5), (2, 2), (1, 1)],          # up-left
        [(9, 8), (9, 4), (10, 1), (11, 0)],        # up
        [(10, 9), (14, 5), (18, 3), (21, 3)],      # up-right
        [(10, 10), (15, 8), (20, 8), (23, 10)],    # right, drooping
        [(9, 10), (6, 12), (3, 14), (1, 15)],      # low-left frond
        [(10, 11), (14, 12), (18, 14), (22, 15)],  # low-right frond
    ]
    for path in fronds:
        for i in range(len(path) - 1):
            (x0, y0), (x1, y1) = path[i], path[i + 1]
            steps = max(abs(x1 - x0), abs(y1 - y0)) or 1
            for s in range(steps + 1):
                x = round(x0 + (x1 - x0) * s / steps)
                y = round(y0 + (y1 - y0) * s / steps)
                rect(g, x, y, x + 1, y, FROND)
                px(g, x, y, FROND_LT if y0 <= y1 else FROND_DK)
    # frond tips
    for (x, y) in [(0, 8), (1, 1), (11, 0), (21, 3), (23, 10)]:
        px(g, x, y, FROND_DK)
    return g

render(palm(), "palm-tree.svg", scale=3, outline="#123010")

# ======================================================================================
# Decor (scale 2)
# ======================================================================================
# starfish
SF = "#ff8c42"
SF_DK = "#d96a20"
g = new_grid(11, 11)
rect(g, 4, 0, 6, 3, SF); rect(g, 4, 7, 6, 10, SF)      # vertical arms
rect(g, 0, 4, 3, 6, SF); rect(g, 7, 4, 10, 6, SF)      # horizontal arms
rect(g, 3, 3, 7, 7, SF)                                 # body
rect(g, 4, 5, 6, 6, SF_DK)
for (x, y) in [(5, 1), (5, 9), (1, 5), (9, 5)]:
    px(g, x, y, "#ffd0a0")                              # arm tips
px(g, 5, 4, "#ffe0c0")
render(g, "starfish.svg", scale=2, outline="#7a3a10")

# tuft of beach grass
g = new_grid(10, 10)
BG = "#8fb04a"; BG_DK = "#5f7a2a"
for (x, base) in [(2, 9), (4, 9), (6, 9), (8, 9)]:
    rect(g, x, base - 6, x, base, BG)
px(g, 2, 3, BG_DK); px(g, 4, 2, BG_DK); px(g, 6, 3, BG); px(g, 8, 4, BG_DK)
rect(g, 1, 9, 9, 9, "#c9a866")                         # sand base
render(g, "beach-grass.svg", scale=2, outline="#3a4a18")

# ======================================================================================
# WALKER (NEW signature) — "coco": a rolling coconut with a sprout + face. anim coco-roll
# ======================================================================================
PAD = 2
BW, BH = 14 + PAD * 2, 15
CO = "#7a4a26"
CO_DK = "#563318"
CO_LT = "#9c6636"
SPROUT = "#4faa4a"

def coco(spin):
    g = new_grid(BW, BH)
    o = PAD
    # round hairy coconut
    rect(g, 3 + o, 3, 10 + o, 12, CO)
    rect(g, 2 + o, 5, 11 + o, 10, CO)
    rect(g, 4 + o, 2, 9 + o, 13, CO)
    rect(g, 2 + o, 5, 4 + o, 9, CO_LT)              # lit side
    rect(g, 9 + o, 6, 11 + o, 11, CO_DK)            # shaded side
    # fibrous hairs, offset per frame so it reads as rolling
    for hx in range(3, 12, 2):
        px(g, hx + o + (spin % 2), 12, CO_DK)
        px(g, hx + o, 3, CO_LT)
    # three coconut "eyes" (the germination pores) used as a face
    px(g, 5 + o, 7, CO_DK); px(g, 8 + o, 7, CO_DK)
    px(g, 6 + o, 6, "#1a1a2e"); px(g, 8 + o, 6, "#1a1a2e")   # angry eyes
    rect(g, 6 + o, 9, 8 + o, 9, CO_DK)              # mouth
    # little sprout on top
    rect(g, 7 + o, 0, 7 + o, 2, SPROUT)
    px(g, 6 + o, 1, SPROUT); px(g, 8 + o, 0, "#7ed957")
    return g

render(coco(0), "coco-0.svg", scale=2, outline="#2a1810")
render(coco(1), "coco-1.svg", scale=2, outline="#2a1810")

# ======================================================================================
# BOSS (NEW) — "Piña Monstruo": a giant carnivorous pineapple. special = spikeBurst
# ======================================================================================
PINE = "#f2c744"
PINE_DK = "#c99a26"
PINE_LT = "#ffe680"
LAT = "#a8781e"          # brown lattice seams
CROWN = "#4faa4a"
CROWN_DK = "#2c6e35"
CROWN_LT = "#7ed957"
MOUTH = "#8a1f2e"
TOOTH = "#fff2e0"

def pineapple():
    g = new_grid(30, 40)
    # spiky leaf crown
    crown_leaves = [(11, 6, 12, 0), (14, 6, 14, -1), (17, 6, 18, 0),
                    (9, 7, 6, 2), (20, 7, 24, 2), (13, 6, 11, 1), (16, 6, 19, 1)]
    for (x0, y0, x1, y1) in crown_leaves:
        steps = max(abs(x1 - x0), abs(y1 - y0)) or 1
        for s in range(steps + 1):
            x = round(x0 + (x1 - x0) * s / steps)
            y = round(y0 + (y1 - y0) * s / steps)
            rect(g, x, max(0, y), x + 1, max(0, y) + 1, CROWN)
            px(g, x, max(0, y), CROWN_LT if x < 15 else CROWN_DK)
    # oval body
    rect(g, 6, 9, 23, 36, PINE)
    rect(g, 8, 7, 21, 9, PINE)
    rect(g, 7, 34, 22, 37, PINE)
    rect(g, 6, 9, 8, 36, PINE_LT)              # lit left
    rect(g, 21, 9, 23, 36, PINE_DK)            # shaded right
    rect(g, 7, 34, 22, 36, PINE_DK)            # bottom shade
    # diamond lattice (the pineapple crosshatch)
    for yy in range(10, 36, 4):
        for xx in range(7, 23, 4):
            off = 2 if ((yy // 4) % 2) else 0
            px(g, xx + off, yy, LAT)
            px(g, xx + off - 1, yy + 1, LAT); px(g, xx + off + 1, yy + 1, LAT)
    # big fanged maw
    rect(g, 10, 22, 19, 30, MOUTH)
    rect(g, 10, 28, 19, 30, "#5c1420")
    for tx in range(10, 19, 2):
        rect(g, tx, 22, tx, 23, TOOTH)         # top teeth
        rect(g, tx + 1, 29, tx + 1, 30, TOOTH) # bottom teeth
    # angry eyes above the maw
    rect(g, 9, 14, 12, 17, "#fff2e0"); rect(g, 17, 14, 20, 17, "#fff2e0")
    px(g, 10, 15, "#1a1a2e"); px(g, 18, 15, "#1a1a2e")
    rect(g, 9, 13, 12, 13, PINE_DK); rect(g, 17, 13, 20, 13, PINE_DK)  # brows
    return g

def all_white(src):
    g = [row[:] for row in src]
    for row in g:
        for x in range(len(row)):
            if row[x] is not None:
                row[x] = "#ffffff"
    return g

boss = pineapple()
render(boss, "boss-pineapple.svg", scale=3, outline="#4a2f0a")
render(all_white(boss), "boss-pineapple-flash.svg", scale=3, outline="#4a2f0a")

# ---- boss seed (spiky golden pod; part of the variant) ----
g = new_grid(5, 5)
rect(g, 0, 0, 4, 4, PINE_DK)
rect(g, 1, 1, 3, 3, PINE_LT)
px(g, 2, 2, LAT)
render(g, "pineapple-seed.svg", scale=2, outline="#4a2f0a")

# ---- boss heavy orb: a spiked tropical energy ball (gold core, green shell) ----
g = new_grid(16, 16)
rect(g, 4, 1, 11, 14, CROWN_DK)
rect(g, 1, 4, 14, 11, CROWN_DK)
rect(g, 3, 3, 12, 12, CROWN_DK)
rect(g, 5, 3, 10, 12, CROWN)
rect(g, 3, 5, 12, 10, CROWN)
rect(g, 6, 5, 9, 10, PINE_LT)
rect(g, 5, 6, 10, 9, PINE_LT)
for (x, y) in [(0, 7), (0, 8), (15, 7), (15, 8), (7, 0), (8, 0), (7, 15), (8, 15)]:
    px(g, x, y, PINE)
render(g, "pineapple-orb.svg", scale=2, outline="#173a1a")

# ---- boss spike-burst leaf-shard (bright, high-contrast against sand) ----
g = new_grid(9, 5)
rect(g, 0, 2, 6, 2, CROWN)                   # green shaft
rect(g, 1, 2, 4, 2, CROWN_LT)                # bright core
rect(g, 6, 1, 8, 3, "#eaffea")               # pale tip
px(g, 6, 0, CROWN_LT); px(g, 6, 4, CROWN_LT) # barbs
render(g, "pineapple-spike.svg", scale=2, outline="#173a1a")

print("beach done")
