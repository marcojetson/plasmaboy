"""Greenhouse / botanical-conservatory sprite set for level 6 (the internal theme key is still
'museum'). A Victorian glass-and-white-iron palm house: slate-tile floor, glass wall panels and
tall potted palms behind, a glass roof overhead, and plant beds / ferns / benches along the floor.
The enemies are reused from every biome (via skinTheme); this only adds the set dressing plus the
corpse-flower (Rafflesia) end boss — exactly the kind of specimen a real botanical greenhouse
shows off.

Regenerate with:  python3 scripts/gen_museum.py
"""
from pixelart import new_grid, rect, px, render

# ======================================================================================
# Palette
# ======================================================================================
GLASS = "#bfe0dd"
GLASS_LT = "#e6f4f1"
GLASS_DK = "#8fbdb8"
FRAME = "#e2e8e2"       # white-painted iron
FRAME_DK = "#aab4a8"
FRAME_SH = "#8a968a"
TILE = "#b8c4b4"        # pale slate floor
TILE_LT = "#d0dccb"
TILE_DK = "#93a08f"
GROUT = "#79877a"
WOOD = "#8a5a38"
WOOD_DK = "#5f3d24"
SOIL = "#4e3722"
LEAF = "#3a8f4f"
LEAF_LT = "#5fbf6f"
LEAF_DK = "#2b6a39"
POT = "#bd6a3c"
POT_LT = "#d6864f"
POT_DK = "#8f4c28"
FL_PINK = "#e8628a"
FL_YEL = "#ffd54f"
FL_BLU = "#7a9cff"
FL_RED = "#e5563f"
MOSS = "#6f8f5a"

# ======================================================================================
# Tiles (scale 2, no outline)
# ======================================================================================
# slate floor — grid grout + a little moss so it reads as a well-trodden conservatory floor
g = new_grid(16, 16)
rect(g, 0, 0, 15, 15, TILE)
rect(g, 0, 0, 15, 0, TILE_LT)
rect(g, 0, 15, 15, 15, GROUT)   # grout lines (bottom + right) form a grid when tiled
rect(g, 15, 0, 15, 15, GROUT)
for (x, y) in [(4, 5), (11, 10), (7, 3)]:
    px(g, x, y, TILE_DK)
px(g, 15, 15, MOSS)
render(g, "tile-greenhouse.svg", scale=2, outline=None)

g = new_grid(16, 16)
rect(g, 0, 0, 15, 15, TILE_DK)
rect(g, 0, 0, 15, 0, "#8f9c8b")
for (x, y) in [(3, 6), (10, 9), (6, 12)]:
    px(g, x, y, "#7d8a79")
render(g, "tile-greenhouse-sub.svg", scale=2, outline=None)

# planter ledge — a raised wooden bed of soil with sprouts on top (the platforms)
g = new_grid(16, 16)
rect(g, 0, 0, 15, 15, WOOD)
rect(g, 0, 0, 15, 2, SOIL)       # soil band
rect(g, 0, 0, 15, 0, LEAF_DK)    # green fringe
for x in (2, 6, 10, 14):
    px(g, x, 0, LEAF_LT)         # sprouts
for x in range(2, 15, 4):
    rect(g, x, 4, x, 14, "#7a4e30")  # plank seams
rect(g, 0, 3, 0, 15, WOOD_DK)
rect(g, 15, 3, 15, 15, WOOD_DK)
rect(g, 0, 15, 15, 15, WOOD_DK)
render(g, "tile-planter.svg", scale=2, outline=None)

# ======================================================================================
# Background scenery (scale 3, outline), origin bottom
# ======================================================================================
def glass_frame():
    """A tall glass wall panel in a white iron frame."""
    g = new_grid(24, 34)
    rect(g, 3, 0, 20, 33, GLASS)
    rect(g, 3, 0, 20, 0, GLASS_LT)
    rect(g, 0, 0, 3, 33, FRAME)          # left post
    rect(g, 20, 0, 23, 33, FRAME)        # right post
    rect(g, 0, 0, 0, 33, FRAME_SH)
    rect(g, 23, 0, 23, 33, FRAME_SH)
    rect(g, 11, 0, 12, 33, FRAME)        # centre mullion
    for yy in (7, 15, 23, 30):
        rect(g, 3, yy, 20, yy, FRAME_DK)  # glazing bars -> panes
    for i in range(6):
        px(g, 5 + i, 2 + i, GLASS_LT)    # diagonal glint
    return g

render(glass_frame(), "glass-frame.svg", scale=3, outline="#8fa89a")

def palm():
    """A tall potted palm in a terracotta urn."""
    g = new_grid(24, 34)
    rect(g, 7, 28, 16, 33, POT)          # urn
    rect(g, 7, 28, 16, 29, POT_LT)
    rect(g, 7, 33, 16, 33, POT_DK)
    rect(g, 11, 14, 13, 28, WOOD)        # trunk
    rect(g, 11, 14, 11, 28, "#9a6a42")
    px(g, 12, 20, WOOD_DK)
    rect(g, 9, 11, 15, 15, LEAF_DK)      # crown base
    fronds = [(-9, 0), (-8, -4), (-5, -7), (0, -9), (5, -7), (8, -4), (9, 0)]
    for (dx, dy) in fronds:
        steps = max(abs(dx), abs(dy))
        for s in range(steps + 1):
            x = round(12 + dx * s / steps)
            y = round(12 + dy * s / steps)
            rect(g, x - 1, y, x + 1, y, LEAF)
        px(g, 12 + dx, 12 + dy, LEAF_LT)
    rect(g, 10, 9, 14, 12, LEAF)
    px(g, 12, 10, LEAF_LT)
    return g

render(palm(), "palm-tree.svg", scale=3, outline="#245033")

# ======================================================================================
# Overhead glass roof — hung via the "cloud" layer up high (scale 3, outline)
# ======================================================================================
def glass_roof():
    g = new_grid(24, 18)
    rect(g, 0, 0, 23, 17, GLASS)
    rect(g, 0, 0, 23, 1, GLASS_LT)
    rect(g, 0, 17, 23, 17, FRAME_DK)
    rect(g, 0, 0, 0, 17, FRAME)
    rect(g, 23, 0, 23, 17, FRAME)
    for xx in (6, 12, 18):
        rect(g, xx, 0, xx, 17, FRAME)     # rafters
    rect(g, 0, 8, 23, 9, FRAME_DK)        # ridge bar
    for i in range(5):
        px(g, 2 + i, 2 + i, GLASS_LT)
    return g

render(glass_roof(), "glass-roof.svg", scale=3, outline="#8fa89a")

# ======================================================================================
# Ground decor (scale 2)
# ======================================================================================
# leafy potted plant
g = new_grid(10, 14)
rect(g, 2, 9, 7, 13, POT)
rect(g, 2, 9, 7, 9, POT_LT)
rect(g, 2, 12, 7, 13, POT_DK)
rect(g, 3, 3, 6, 9, LEAF)
rect(g, 2, 5, 7, 7, LEAF)
rect(g, 4, 1, 5, 4, LEAF_LT)
px(g, 3, 4, LEAF_LT)
px(g, 6, 6, LEAF_DK)
render(g, "potted-plant.svg", scale=2)

# potted fern
g = new_grid(10, 14)
rect(g, 3, 10, 6, 13, POT)
rect(g, 3, 10, 6, 10, POT_LT)
rect(g, 3, 13, 6, 13, POT_DK)
rect(g, 3, 4, 6, 10, LEAF)
for (x, y) in [(2, 6), (7, 6), (1, 8), (8, 8), (2, 9), (7, 9)]:
    px(g, x, y, LEAF)
for (x, y) in [(4, 2), (5, 2), (3, 3), (6, 3), (1, 7), (8, 7)]:
    px(g, x, y, LEAF_LT)
render(g, "fern.svg", scale=2)

# flower bed
g = new_grid(12, 10)
rect(g, 0, 6, 11, 9, SOIL)
rect(g, 0, 6, 11, 6, "#5f4630")
for x in range(2, 11, 2):
    px(g, x, 5, LEAF)
for (x, c) in [(2, FL_PINK), (5, FL_YEL), (8, FL_BLU), (10, FL_RED)]:
    rect(g, x, 3, x, 5, LEAF)     # stem
    px(g, x, 2, c)
    px(g, x - 1, 3, c)
    px(g, x + 1, 3, c)
    px(g, x, 3, "#ffffff")
render(g, "flower-bed.svg", scale=2)

# wrought-iron garden bench
g = new_grid(14, 8)
rect(g, 1, 3, 12, 4, FRAME)       # seat
rect(g, 1, 3, 12, 3, "#f2f6f2")
rect(g, 1, 1, 12, 1, FRAME_DK)    # top rail
rect(g, 2, 1, 2, 3, FRAME_DK)
rect(g, 11, 1, 11, 3, FRAME_DK)
rect(g, 2, 5, 3, 7, FRAME_SH)     # legs
rect(g, 10, 5, 11, 7, FRAME_SH)
render(g, "garden-bench.svg", scale=2)

# ======================================================================================
# BOSS — the corpse flower (Rafflesia): a huge fleshy 5-lobe bloom, cream-speckled, with a
# dark central pit that belches spores. (Kept from before — it belongs in a greenhouse.)
# ======================================================================================
RAFF = "#a83a3a"
RAFF_DK = "#7a2626"
RAFF_LT = "#c85a4a"
SPECK = "#e8d0a0"
PIT = "#3a1414"
KNOB = "#d8b070"

def build_corpse():
    g = new_grid(40, 38)
    cx, cy = 20, 20
    petals = [(20, 6, 10), (8, 15, 9), (32, 15, 9), (12, 31, 9), (28, 31, 9)]
    for (pxc, pyc, r) in petals:
        for y in range(pyc - r, pyc + r + 1):
            dy = y - pyc
            half = int((r * r - dy * dy) ** 0.5) if abs(dy) <= r else -1
            if half >= 0:
                rect(g, pxc - half, y, pxc + half, y, RAFF)
        px(g, pxc - r, pyc, RAFF_LT)
        px(g, pxc + r, pyc, RAFF_DK)
    for (pxc, pyc, r) in petals:
        for (sx, sy) in [(pxc - 3, pyc - 2), (pxc + 2, pyc + 1), (pxc, pyc - 3), (pxc + 3, pyc + 3)]:
            px(g, sx, sy, SPECK)
    # central pit
    for y in range(cy - 8, cy + 9):
        dy = y - cy
        half = int((64 - dy * dy) ** 0.5) if abs(dy) <= 8 else -1
        if half >= 0:
            rect(g, cx - half, y, cx + half, y, PIT)
    rect(g, cx - 7, cy - 8, cx + 7, cy - 7, RAFF_DK)  # rim
    for (kx, ky) in [(cx - 5, cy - 4), (cx + 5, cy - 4), (cx - 6, cy + 3), (cx + 6, cy + 3), (cx, cy - 6)]:
        px(g, kx, ky, KNOB)
    # menacing face in the pit
    rect(g, cx - 4, cy - 2, cx - 2, cy, "#ffe066")
    px(g, cx - 4, cy - 1, "#3a2a00")
    rect(g, cx + 2, cy - 2, cx + 4, cy, "#ffe066")
    px(g, cx + 4, cy - 1, "#3a2a00")
    rect(g, cx - 3, cy + 3, cx + 3, cy + 6, "#160606")  # maw
    for tx in (cx - 2, cx, cx + 2):
        px(g, tx, cy + 3, SPECK)
    return g

def _whiten(src):
    g = [row[:] for row in src]
    for row in g:
        for x in range(len(row)):
            if row[x] is not None:
                row[x] = "#ffffff"
    return g

_corpse = build_corpse()
render(_corpse, "boss-corpse.svg", scale=3, outline="#2a0e0e")
render(_whiten(_corpse), "boss-corpse-flash.svg", scale=3, outline="#2a0e0e")

# seed volley (spore mote)
g = new_grid(5, 5)
rect(g, 1, 1, 3, 3, KNOB)
px(g, 0, 2, "#8a6a3a")
px(g, 4, 2, "#8a6a3a")
px(g, 2, 0, "#8a6a3a")
px(g, 2, 4, "#8a6a3a")
px(g, 2, 2, "#f0e0c0")
render(g, "corpse-spore.svg", scale=2)

# heavy orb (pollen ball)
_CORE = "#f4e6c8"
_MID = "#d8b070"
_OUT = "#a87a3a"
_SPK = "#ffe8c0"
g = new_grid(16, 16)
rect(g, 4, 1, 11, 14, _OUT)
rect(g, 1, 4, 14, 11, _OUT)
rect(g, 3, 3, 12, 12, _OUT)
rect(g, 5, 3, 10, 12, _MID)
rect(g, 3, 5, 12, 10, _MID)
rect(g, 6, 5, 9, 10, _CORE)
rect(g, 5, 6, 10, 9, _CORE)
for (x, y) in [(0, 6), (0, 9), (15, 6), (15, 9), (6, 0), (9, 0), (6, 15), (9, 15), (2, 2), (13, 2), (2, 13), (13, 13)]:
    px(g, x, y, _SPK)
render(g, "corpse-orb.svg", scale=2, outline="#6a4a1a")

# spikeBurst spore puff
g = new_grid(7, 7)
rect(g, 2, 1, 4, 5, _MID)
rect(g, 1, 2, 5, 4, _MID)
px(g, 3, 3, _CORE)
px(g, 0, 3, _OUT)
px(g, 6, 3, _OUT)
px(g, 3, 0, _OUT)
px(g, 3, 6, _OUT)
render(g, "corpse-spike.svg", scale=2, outline="#6a4a1a")
