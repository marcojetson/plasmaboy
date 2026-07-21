"""House-biome sprite set (see src/config/themes.ts 'house') — the FINAL biome.

A cozy indoor room overrun by houseplants: warm wood-plank floor, furniture + potted plants
as obstacles, a toddling potted-plant walker, and a potted-cactus straight-shooter. Other foes
reuse forest (sunflower), swamp (leech, dragonfly) and cave (fungus) skins. The final boss is
the Monstera Monstruo — a Swiss-cheese plant with the signature split, fenestrated leaves,
whipping vines in a shockwave slam.
"""
from pixelart import new_grid, rect, px, render

# ======================================================================================
# Tile (scale 2, no outline) — warm wooden plank floor, flush at the top
# ======================================================================================
WOOD = "#b5885a"
WOOD_DK = "#8a6238"
WOOD_LT = "#c99f6e"
GRAIN = "#a2764a"
g = new_grid(16, 16)
rect(g, 0, 0, 15, 15, WOOD)
rect(g, 0, 0, 15, 0, WOOD_LT)              # lit top edge
rect(g, 0, 7, 15, 7, WOOD_DK)              # plank seam
rect(g, 7, 0, 7, 6, WOOD_DK)               # staggered vertical joints
rect(g, 3, 8, 3, 15, WOOD_DK)
rect(g, 11, 8, 11, 15, WOOD_DK)
for (x, y) in [(2, 3), (9, 4), (13, 11), (5, 12)]:
    px(g, x, y, GRAIN)                      # grain flecks
for (x, y) in [(6, 2), (12, 5), (4, 10)]:
    px(g, x, y, WOOD_LT)
render(g, "tile-house.svg", scale=2, outline=None)

# ======================================================================================
# Obstacles (scale 2/3, outline)
# ======================================================================================
TERRA = "#c0693a"
TERRA_DK = "#8f4a26"
TERRA_LT = "#d98a5a"
SOIL = "#4a3320"
LEAF = "#3f8f4a"
LEAF_DK = "#2a6b35"
LEAF_LT = "#63bf5f"

# potted fiddle-leaf fig (tall potted plant obstacle)
def potted_fig():
    g = new_grid(20, 28)
    # pot
    rect(g, 5, 20, 14, 27, TERRA)
    rect(g, 4, 19, 15, 21, TERRA_LT)
    rect(g, 5, 25, 14, 27, TERRA_DK)
    rect(g, 6, 18, 13, 20, SOIL)
    # thin trunk
    rect(g, 9, 10, 10, 19, "#6b4a2a")
    # big round fig leaves
    for (cx, cy) in [(9, 6), (5, 10), (14, 9), (11, 3)]:
        rect(g, cx - 2, cy - 2, cx + 2, cy + 2, LEAF)
        px(g, cx - 2, cy - 2, LEAF_LT)
        px(g, cx + 2, cy + 2, LEAF_DK)
        px(g, cx, cy, LEAF_DK)
    return g

render(potted_fig(), "potted-fig.svg", scale=3, outline="#132a16")

# cozy sofa (blocky furniture, top-down-ish)
def sofa():
    g = new_grid(26, 16)
    UP = "#5f7fa8"; UP_DK = "#42597a"; UP_LT = "#7f9cc0"
    rect(g, 1, 4, 24, 14, UP)              # seat block
    rect(g, 1, 2, 24, 5, UP_DK)            # backrest
    rect(g, 0, 5, 3, 14, UP_DK)            # left arm
    rect(g, 22, 5, 25, 14, UP_DK)          # right arm
    rect(g, 4, 6, 12, 12, UP_LT)           # cushion 1
    rect(g, 13, 6, 21, 12, UP_LT)          # cushion 2
    rect(g, 4, 6, 21, 6, "#93aed0")        # cushion highlight
    rect(g, 2, 14, 23, 15, "#2f3f56")      # base shadow
    return g

render(sofa(), "sofa.svg", scale=3, outline="#20293a")

# ======================================================================================
# Decor (scale 2)
# ======================================================================================
# small succulent in a cup
g = new_grid(10, 10)
rect(g, 3, 6, 6, 9, TERRA)
rect(g, 3, 6, 6, 6, TERRA_LT)
rect(g, 4, 2, 5, 6, LEAF)                  # rosette
rect(g, 2, 4, 7, 5, LEAF)
px(g, 2, 4, LEAF_LT); px(g, 7, 4, LEAF_DK)
px(g, 4, 2, LEAF_LT); px(g, 5, 3, "#a8f0a0")
render(g, "small-succulent.svg", scale=2, outline="#132a16")

# decorative floor rug (visual patch)
g = new_grid(16, 10)
R = "#b0524f"; R_DK = "#8a3a38"; R_LT = "#d0908e"
rect(g, 1, 1, 14, 8, R)
rect(g, 1, 1, 14, 1, R_DK); rect(g, 1, 8, 14, 8, R_DK)
rect(g, 1, 1, 1, 8, R_DK); rect(g, 14, 1, 14, 8, R_DK)
rect(g, 4, 3, 11, 6, R_DK)
rect(g, 6, 4, 9, 5, R_LT)
for x in (2, 13):
    for y in (2, 7):
        px(g, x, y, R_LT)
render(g, "floor-rug.svg", scale=2, outline=None)

# ======================================================================================
# WALKER (NEW signature) — "pot-crawler": a potted plant that toddles. anim pot-walk
# ======================================================================================
PAD = 2
BW, BH = 14 + PAD * 2, 16

def pot_crawler(step):
    g = new_grid(BW, BH)
    o = PAD
    # terracotta pot
    rect(g, 4 + o, 8, 9 + o, 13, TERRA)
    rect(g, 3 + o, 7, 10 + o, 9, TERRA_LT)
    rect(g, 4 + o, 12, 9 + o, 13, TERRA_DK)
    rect(g, 5 + o, 6, 8 + o, 7, SOIL)
    # leafy sprout with a face
    rect(g, 6 + o, 2, 7 + o, 6, LEAF)
    rect(g, 4 + o, 3, 6 + o, 5, LEAF); rect(g, 7 + o, 2, 9 + o, 4, LEAF)
    px(g, 4 + o, 3, LEAF_LT); px(g, 9 + o, 3, LEAF_DK)
    px(g, 5 + o, 9, "#1a1a2e"); px(g, 8 + o, 9, "#1a1a2e")   # eyes on the pot
    rect(g, 6 + o, 11, 7 + o, 11, TERRA_DK)                  # mouth
    # little legs, alternating per frame
    if step == 0:
        px(g, 5 + o, 14, TERRA_DK); px(g, 8 + o, 15, TERRA_DK)
    else:
        px(g, 5 + o, 15, TERRA_DK); px(g, 8 + o, 14, TERRA_DK)
    return g

render(pot_crawler(0), "pot-crawler-0.svg", scale=2, outline="#2a1810")
render(pot_crawler(1), "pot-crawler-1.svg", scale=2, outline="#2a1810")

# ======================================================================================
# STRAIGHT SHOOTER (NEW signature) — potted cactus. reuses the desert 'cactus-needle' bolt
# ======================================================================================
CAC = "#4faa4a"
CAC_DK = "#2f7a30"
CAC_LT = "#7ed957"

def potted_cactus(firing):
    g = new_grid(14, 15)
    # pot
    rect(g, 3, 10, 10, 14, TERRA)
    rect(g, 2, 9, 11, 11, TERRA_LT)
    rect(g, 3, 13, 10, 14, TERRA_DK)
    # cactus body + arms
    rect(g, 5, 2, 8, 10, CAC)
    rect(g, 5, 2, 5, 10, CAC_LT); rect(g, 8, 2, 8, 10, CAC_DK)
    rect(g, 2, 5, 4, 6, CAC); rect(g, 2, 3, 3, 6, CAC)      # left arm
    rect(g, 9, 6, 11, 7, CAC); rect(g, 10, 4, 11, 7, CAC)   # right arm
    for (x, y) in [(4, 4), (9, 3), (6, 8), (3, 4), (11, 5)]:
        px(g, x, y, "#e8f0c0")                              # spines
    px(g, 5, 5, "#ffe066"); px(g, 8, 5, "#ffe066")          # eyes
    if firing:
        rect(g, 6, 7, 7, 8, "#ff6f3c")
    else:
        px(g, 6, 7, "#1a3a1a"); px(g, 7, 7, "#1a3a1a")
    return g

render(potted_cactus(False), "potted-cactus-idle.svg", scale=2, outline="#132a16")
render(potted_cactus(True), "potted-cactus-fire.svg", scale=2, outline="#132a16")

# ======================================================================================
# BOSS (NEW, FINAL) — "Monstera Monstruo": Swiss-cheese plant with split leaves. special = slam
# ======================================================================================
M = "#2f8a3f"
M_DK = "#1f6b2c"
M_LT = "#54b45a"
VEIN = "#8fe07a"
POT = "#c0693a"
POT_DK = "#8f4a26"
POT_LT = "#d98a5a"
MOUTH = "#7a1f2e"
TOOTH = "#fff2e0"

def punch(g, x, y, w, h):
    """Cut a rectangular hole (background shows through) — a Monstera fenestration."""
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            if 0 <= yy < len(g) and 0 <= xx < len(g[0]):
                g[yy][xx] = None

def monstera_leaf(g, cx, cy, w, h, tip_dy, holes, slit_rows):
    """A BROAD fenestrated Monstera leaf: a wide heart/teardrop with a pointed tip, a bright
    midrib, a few big punched holes, and deep marginal slits — the traits that read as Monstera
    rather than a generic leaf. tip_dy shifts the pointed tip up (-) so the leaf angles."""
    for yy in range(cy - h, cy + h + 1):
        t = 1 - abs(yy - cy) / (h + 1)
        half = max(0, round(w * (t ** 0.6)))          # broad, full-bodied ellipse
        rect(g, cx - half, yy, cx + half, yy, M)
        rect(g, cx - half, yy, cx - half + 1, yy, M_LT)   # lit left rim
        rect(g, cx + half - 1, yy, cx + half, yy, M_DK)   # shaded right rim
    # pointed tip
    rect(g, cx, cy - h + tip_dy, cx, cy - h, M)
    px(g, cx, cy - h + tip_dy, M_LT)
    # bright central midrib + herringbone veins
    for yy in range(cy - h + tip_dy, cy + h + 1):
        px(g, cx, yy, VEIN)
    for vy in range(cy - h + 2, cy + h, 3):
        px(g, cx - 2, vy + 1, VEIN); px(g, cx + 2, vy + 1, VEIN)
    # big oval fenestration holes
    for (hx, hy, hw, hh) in holes:
        punch(g, hx, hy, hw, hh)
    # deep marginal slits: cut a wedge from each rim toward the midrib
    for yy in slit_rows:
        t = 1 - abs(yy - cy) / (h + 1)
        half = max(0, round(w * (t ** 0.6)))
        if half >= 3:
            punch(g, cx - half, yy, 3, 1)               # left notch
            punch(g, cx + half - 2, yy, 3, 1)           # right notch

def monstera():
    g = new_grid(34, 40)
    # terracotta pot at the base
    rect(g, 8, 31, 25, 39, POT)
    rect(g, 7, 30, 26, 32, POT_LT)
    rect(g, 8, 37, 25, 39, POT_DK)
    rect(g, 10, 29, 23, 31, SOIL)
    # arching stems
    for sx in (12, 17, 22):
        rect(g, sx, 20, sx + 1, 30, M_DK)
    # two broad side leaves first (behind), then the big central leaf (front)
    monstera_leaf(g, 6, 19, 6, 6, -1, [(4, 16, 2, 2), (7, 20, 2, 2)], [15, 21])
    monstera_leaf(g, 27, 19, 6, 6, -1, [(25, 16, 2, 2), (28, 20, 2, 2)], [15, 21])
    monstera_leaf(g, 17, 11, 11, 9, -2,
                  [(11, 8, 3, 2), (20, 7, 3, 2), (13, 13, 2, 2), (21, 13, 2, 2), (16, 16, 3, 2)],
                  [8, 11, 14, 17])
    # menacing face on the stem base, just above the pot rim
    rect(g, 12, 24, 15, 27, "#ffe066"); rect(g, 19, 24, 22, 27, "#ffe066")
    px(g, 13, 25, "#2a1a00"); px(g, 20, 25, "#2a1a00")
    rect(g, 13, 28, 20, 30, MOUTH)
    rect(g, 13, 29, 20, 30, "#4a0f18")
    for tx in range(13, 20, 2):
        px(g, tx, 28, TOOTH)
    return g

def all_white(src):
    g = [row[:] for row in src]
    for row in g:
        for x in range(len(row)):
            if row[x] is not None:
                row[x] = "#ffffff"
    return g

boss = monstera()
render(boss, "boss-monstera.svg", scale=3, outline="#0f2a16")
render(all_white(boss), "boss-monstera-flash.svg", scale=3, outline="#0f2a16")

# ---- boss seed (leafy pod) ----
g = new_grid(5, 5)
rect(g, 0, 0, 4, 4, M_DK)
rect(g, 1, 1, 3, 3, M_LT)
px(g, 2, 2, VEIN)
render(g, "monstera-seed.svg", scale=2, outline="#0f2a16")

# ---- boss heavy orb: a leafy green shockwave orb (used by the slam special) ----
g = new_grid(16, 16)
rect(g, 4, 1, 11, 14, M_DK)
rect(g, 1, 4, 14, 11, M_DK)
rect(g, 3, 3, 12, 12, M_DK)
rect(g, 5, 3, 10, 12, M)
rect(g, 3, 5, 12, 10, M)
rect(g, 6, 5, 9, 10, VEIN)
rect(g, 5, 6, 10, 9, VEIN)
for (x, y) in [(0, 7), (0, 8), (15, 7), (15, 8), (7, 0), (8, 0), (7, 15), (8, 15)]:
    px(g, x, y, M_LT)
render(g, "monstera-orb.svg", scale=2, outline="#0a2010")

# ---- boss spike (part of the variant; slam bosses don't fire it, but keep it themed) ----
g = new_grid(9, 5)
rect(g, 0, 2, 6, 2, M)
rect(g, 1, 2, 4, 2, M_LT)
rect(g, 6, 1, 8, 3, VEIN)
px(g, 6, 0, M_LT); px(g, 6, 4, M_LT)
render(g, "monstera-spike.svg", scale=2, outline="#0a2010")

print("house done")
