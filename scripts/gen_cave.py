"""Cave-theme sprite set for level 4 (see src/config/themes.ts 'cave').

Same conventions as the other gen_*.py scripts. The cave is dark, so enemies and props carry
bioluminescent glow accents to stay readable. Enemy skins keep the shared archetype
silhouettes (walker / straight-shooter / aimer / burrow-charger / spore), reskinned as cave
moss/lichen/fungus, plus a rocky worm. Also the tiles, rock scenery, glowing decor, and the
falling-rock hazard art.
"""
from pixelart import new_grid, rect, px, render

# ======================================================================================
# Palette
# ======================================================================================
ROCK = "#464150"
ROCK_DK = "#2c2836"
ROCK_LT = "#5f5a70"
# Muted, dark gray-green so the moss creatures read as cave dwellers rather than lush jungle
# plants; the small GLOW accents keep them visible against the near-black background.
MOSS = "#535a4f"
MOSS_DK = "#30352c"
MOSS_LT = "#71786a"
GLOW = "#82d8b4"
CRYS = "#5fd0ff"
CRYS_DK = "#2f90c8"
CRYS_LT = "#c8f2ff"
MUSH = "#8a5aa8"
MUSH_LT = "#c090e0"
MUSH_GLOW = "#e0b0ff"
EYE = "#0e1418"

# ======================================================================================
# Tiles (scale 2, no outline) — filled edge-to-edge so things rest flush on the surface
# ======================================================================================
g = new_grid(16, 16)
rect(g, 0, 0, 15, 15, ROCK)
rect(g, 0, 5, 15, 5, ROCK_DK)
for x in (1, 4, 5, 9, 12, 13):
    px(g, x, 0, ROCK_LT)
for (x, y) in [(3, 7), (9, 9), (12, 7), (6, 12), (2, 13), (14, 11)]:
    px(g, x, y, ROCK_DK)
for (x, y) in [(5, 10), (10, 13), (7, 6)]:
    px(g, x, y, ROCK_LT)
px(g, 8, 1, MOSS_LT)  # faint moss speck catching light on the surface
render(g, "tile-cave.svg", scale=2, outline=None)

g = new_grid(16, 16)
rect(g, 0, 0, 15, 15, ROCK_DK)
rect(g, 0, 0, 15, 0, "#211e2c")
for (x, y) in [(2, 3), (9, 5), (6, 9), (12, 12), (3, 13), (14, 7)]:
    px(g, x, y, "#211e2c")
for (x, y) in [(5, 6), (11, 3), (8, 11)]:
    px(g, x, y, ROCK)
render(g, "tile-cave-sub.svg", scale=2, outline=None)

g = new_grid(16, 16)
rect(g, 0, 0, 15, 15, ROCK)
rect(g, 0, 0, 15, 1, ROCK_LT)
for y in (4, 5, 9, 10, 14):
    rect(g, 0, y, 15, y, ROCK_DK)
px(g, 8, 2, MOSS_LT)
px(g, 3, 7, ROCK_LT)
render(g, "tile-cave-rock.svg", scale=2, outline=None)

# ======================================================================================
# Background scenery (scale 3, dark outline), origin bottom
# ======================================================================================
def column():
    g = new_grid(24, 34)
    rect(g, 7, 2, 16, 33, ROCK)
    rect(g, 7, 2, 9, 33, ROCK_LT)
    rect(g, 14, 2, 16, 33, ROCK_DK)
    rect(g, 11, 6, 11, 30, ROCK_DK)  # crack
    px(g, 9, 10, MOSS_LT)
    px(g, 14, 20, CRYS)
    px(g, 10, 25, CRYS_DK)
    return g

render(column(), "cave-column.svg", scale=3, outline="#0a0812")

def stalagmite():
    g = new_grid(24, 34)
    cx = 11
    for y in range(4, 34):
        half = int((y - 4) / 2.2) + 1
        rect(g, cx - half, y, cx + half + 1, y, ROCK)
        px(g, cx - half, y, ROCK_LT)
        px(g, cx + half + 1, y, ROCK_DK)
    px(g, cx, 4, CRYS_LT)  # glowing tip
    px(g, cx + 1, 5, CRYS)
    return g

render(stalagmite(), "stalagmite.svg", scale=3, outline="#0a0812")

# ======================================================================================
# Ground decor (scale 2, outline)
# ======================================================================================
g = new_grid(12, 8)
rect(g, 1, 3, 10, 7, ROCK)
rect(g, 2, 2, 8, 3, ROCK_LT)
rect(g, 1, 6, 10, 7, ROCK_DK)
px(g, 4, 4, ROCK_LT)
px(g, 8, 5, ROCK_DK)
render(g, "boulder-small.svg", scale=2)

g = new_grid(10, 12)
rect(g, 4, 5, 5, 11, "#d8d0c0")  # pale stalk
rect(g, 1, 2, 8, 6, MUSH)
rect(g, 2, 1, 7, 2, MUSH)
rect(g, 1, 5, 8, 6, MUSH_LT)
px(g, 3, 3, MUSH_GLOW)
px(g, 6, 4, MUSH_GLOW)
render(g, "cave-mushroom.svg", scale=2)

g = new_grid(10, 12)
rect(g, 3, 4, 5, 11, CRYS)
rect(g, 4, 1, 5, 4, CRYS_LT)
rect(g, 6, 6, 7, 11, CRYS)
rect(g, 1, 7, 2, 11, CRYS_DK)
px(g, 4, 2, CRYS_LT)
render(g, "crystal.svg", scale=2)

g = new_grid(10, 6)
for x in (1, 3, 5, 7, 8):
    px(g, x, 5, MOSS_DK)
    px(g, x, 4, MOSS)
px(g, 2, 3, MOSS_LT)
px(g, 6, 3, GLOW)
render(g, "moss-patch.svg", scale=2, outline=None)

# ======================================================================================
# WALKER — crawling moss clump (2 frames)
# ======================================================================================
PAD = 2
MW, MH = 14 + PAD * 2, 14

def moss_clump(sway):
    g = new_grid(MW, MH)
    o = PAD
    top = 3 - sway
    rect(g, 2 + o, top + 2, 13 + o, 13, MOSS)
    rect(g, 1 + o, 6, 14 + o, 11, MOSS)
    rect(g, 1 + o, 6, 2 + o, 11, MOSS_LT)
    rect(g, 13 + o, 6, 14 + o, 11, MOSS_DK)
    rect(g, 2 + o, 12, 13 + o, 13, MOSS_DK)
    for fx, base in ((4, top), (8, top - 1), (11, top)):
        rect(g, fx + o + sway, base, fx + o + sway, top + 2, MOSS)
        px(g, fx + o + sway, base, MOSS_LT)
    for (x, y) in [(5, 8), (10, 9), (7, 6)]:
        px(g, x + o, y, GLOW)
    px(g, 6 + o, 8, EYE)
    px(g, 9 + o, 8, EYE)
    return g

render(moss_clump(0), "moss-crawl-0.svg", scale=2)
render(moss_clump(1), "moss-crawl-1.svg", scale=2)

# ======================================================================================
# STRAIGHT SHOOTER — spiny lichen
# ======================================================================================
def lichen(firing):
    g = new_grid(15, 15)
    rect(g, 5, 1, 9, 13, MOSS)
    rect(g, 3, 4, 11, 11, MOSS)
    rect(g, 5, 1, 6, 13, MOSS_LT)
    rect(g, 9, 1, 9, 13, MOSS_DK)
    rect(g, 3, 11, 11, 12, MOSS_DK)
    for y in (4, 7, 10):
        px(g, 1, y, GLOW)
        px(g, 13, y, GLOW)
    px(g, 7, 0, GLOW)
    px(g, 5, 5, "#ffe066")
    px(g, 9, 5, "#ffe066")
    if firing:
        rect(g, 6, 7, 8, 9, GLOW)
    else:
        rect(g, 6, 8, 8, 8, MOSS_DK)
    return g

render(lichen(False), "moss-shooter-idle.svg", scale=2)
render(lichen(True), "moss-shooter-fire.svg", scale=2)

g = new_grid(6, 3)
rect(g, 0, 1, 4, 1, MOSS_DK)
px(g, 5, 0, GLOW)
px(g, 5, 2, GLOW)
px(g, 0, 1, GLOW)
render(g, "moss-spine.svg", scale=2)

# ======================================================================================
# AIMER — glowing cave bloom (rotates to track)
# ======================================================================================
def bloom(firing):
    g = new_grid(14, 14)
    rect(g, 6, 0, 7, 13, MOSS)
    rect(g, 0, 6, 13, 7, MOSS)
    rect(g, 2, 2, 4, 4, MOSS)
    rect(g, 9, 2, 11, 4, MOSS)
    rect(g, 2, 9, 4, 11, MOSS)
    rect(g, 9, 9, 11, 11, MOSS)
    for (x, y) in [(6, 0), (7, 0), (0, 6), (0, 7), (13, 6), (13, 7), (6, 13), (7, 13),
                   (2, 2), (11, 2), (2, 11), (11, 11)]:
        px(g, x, y, GLOW)
    core = "#c8ffe0" if firing else MOSS_DK
    rect(g, 4, 4, 9, 9, core)
    rect(g, 4, 8, 9, 9, MOSS_DK if not firing else "#8fffc0")
    px(g, 5, 6, EYE)
    px(g, 8, 6, EYE)
    return g

render(bloom(False), "cave-bloom-idle.svg", scale=2)
render(bloom(True), "cave-bloom-fire.svg", scale=2)

g = new_grid(4, 4)
rect(g, 0, 0, 3, 3, MOSS_LT)
px(g, 1, 1, GLOW)
px(g, 2, 2, MOSS_DK)
render(g, "moss-seed.svg", scale=2)

# ======================================================================================
# BURROW-CHARGER — rock-worm
# ======================================================================================
WMOUTH = "#7a2f3f"
# mound (rubble hole)
g = new_grid(15, 6)
rect(g, 2, 3, 12, 5, ROCK)
rect(g, 4, 2, 10, 3, ROCK)
rect(g, 2, 5, 12, 5, ROCK_DK)
rect(g, 6, 3, 8, 5, "#1a1824")
render(g, "rockworm-mound.svg", scale=2)

# emerging
g = new_grid(12, 15)
rect(g, 3, 4, 8, 14, ROCK)
rect(g, 4, 4, 7, 14, ROCK_LT)
rect(g, 3, 12, 8, 14, ROCK_DK)
for sy in (7, 10, 13):
    rect(g, 3, sy, 8, sy, ROCK_DK)
px(g, 4, 6, "#ffe066")
px(g, 7, 6, "#ffe066")
rect(g, 4, 8, 7, 9, WMOUTH)
render(g, "rockworm-emerge.svg", scale=2)

# charging
g = new_grid(13, 13)
rect(g, 1, 5, 11, 11, ROCK)
rect(g, 1, 5, 11, 7, ROCK_LT)
rect(g, 1, 10, 11, 11, ROCK_DK)
for sx in (4, 7):
    rect(g, sx, 5, sx, 11, ROCK_DK)
px(g, 9, 5, "#ffe066")
px(g, 9, 8, "#ffe066")
rect(g, 10, 6, 12, 8, WMOUTH)
render(g, "rockworm-charge.svg", scale=2)

# ======================================================================================
# SPORE — glowing fungus
# ======================================================================================
g = new_grid(12, 12)
rect(g, 4, 7, 7, 11, "#d8d0c0")
rect(g, 2, 2, 9, 8, MUSH)
rect(g, 3, 1, 8, 2, MUSH)
rect(g, 2, 2, 3, 8, MUSH_LT)
rect(g, 8, 2, 9, 8, "#5a3a78")
for (x, y) in [(5, 0), (1, 4), (10, 4)]:
    px(g, x, y, MUSH_GLOW)
render(g, "fungus-closed.svg", scale=2)

g = new_grid(16, 16)
rect(g, 6, 11, 9, 15, "#d8d0c0")
rect(g, 2, 4, 13, 10, MUSH)
rect(g, 3, 2, 12, 4, MUSH)
rect(g, 2, 9, 13, 10, "#5a3a78")
rect(g, 2, 4, 3, 10, MUSH_LT)
rect(g, 5, 5, 10, 9, "#3a2452")
px(g, 6, 6, "#ffe066")
px(g, 9, 6, "#ffe066")
for (x, y) in [(7, 7), (8, 8), (4, 3), (11, 3)]:
    px(g, x, y, MUSH_GLOW)
render(g, "fungus-open.svg", scale=2)

g = new_grid(4, 4)
rect(g, 0, 0, 3, 3, MUSH_LT)
px(g, 1, 1, MUSH_GLOW)
render(g, "moss-spore.svg", scale=2)

# ======================================================================================
# FALLER — the falling rock hazard (new in level 4)
# ======================================================================================
g = new_grid(16, 14)
rect(g, 2, 3, 13, 12, ROCK)
rect(g, 3, 1, 12, 3, ROCK)
rect(g, 2, 3, 4, 12, ROCK_LT)
rect(g, 12, 3, 13, 12, ROCK_DK)
rect(g, 3, 11, 12, 12, ROCK_DK)
rect(g, 7, 4, 7, 9, ROCK_DK)  # crack
px(g, 5, 6, ROCK_LT)
px(g, 10, 8, ROCK_DK)
px(g, 6, 2, ROCK_LT)
render(g, "falling-rock.svg", scale=2, outline="#15121c")

# ======================================================================================
# BOSS — dry resurrection plant (Selaginella lepidophylla), curled into a spiky brown ball
# with a face peering from the centre.
# ======================================================================================
DRY = "#8a6a3a"
DRY_DK = "#5a4426"
DRY_LT = "#b89a5a"
DRY_TIP = "#c9b078"
REYE = "#ffcf3a"
RMAW = "#3a1e12"
RMAW_DK = "#24120a"

def build_rez():
    g = new_grid(40, 40)
    cx, cy, R = 19, 21, 16

    def edge_half(y):
        dy = y - cy
        return int((R * R - dy * dy) ** 0.5) if abs(dy) <= R else -1

    # rounded ball body
    for y in range(cy - R, cy + R + 1):
        h = edge_half(y)
        if h >= 0:
            rect(g, cx - h, y, cx + h, y, DRY)
    # left highlight / right shade
    for y in range(cy - R, cy + R + 1):
        h = edge_half(y)
        if h >= 0:
            px(g, cx - h, y, DRY_LT)
            px(g, cx - h + 1, y, DRY_LT)
            px(g, cx + h, y, DRY_DK)
            px(g, cx + h - 1, y, DRY_DK)
    # concentric curled-frond rings (dry cracks)
    for rr in (7, 11, 15):
        for y in range(cy - rr, cy + rr + 1):
            dy = y - cy
            hx = int((rr * rr - dy * dy) ** 0.5) if abs(dy) <= rr else -1
            if hx >= 0:
                px(g, cx - hx, y, DRY_DK)
                px(g, cx + hx, y, DRY_DK)
    # radial cracks fanning out from the centre
    for (dx, dy) in [(-1, -1), (1, -1), (-1, 1), (1, 1), (0, -1), (0, 1), (-1, 0), (1, 0)]:
        for s in range(5, R):
            px(g, cx + dx * s, cy + dy * s, DRY_DK)
    # spiky frond tips poking out around the rim
    for y in range(cy - R, cy + R + 1, 3):
        h = edge_half(y)
        if h >= 2:
            px(g, cx - h - 1, y, DRY_TIP)
            px(g, cx + h + 1, y, DRY_TIP)
    for (sx, sy) in [(cx, cy - R - 1), (cx, cy + R + 1), (cx - 2, cy - R), (cx + 2, cy + R)]:
        px(g, sx, sy, DRY_TIP)
    # centre hollow: maw + amber eyes peering out
    rect(g, cx - 5, cy - 4, cx + 5, cy + 5, RMAW)
    rect(g, cx - 5, cy + 2, cx + 5, cy + 5, RMAW_DK)
    rect(g, cx - 3, cy - 2, cx - 2, cy - 1, REYE)
    rect(g, cx + 2, cy - 2, cx + 3, cy - 1, REYE)
    for tx in (cx - 4, cx - 1, cx + 2):
        px(g, tx, cy + 2, DRY_TIP)
    return g

def _whiten(src):
    g = [row[:] for row in src]
    for row in g:
        for x in range(len(row)):
            if row[x] is not None:
                row[x] = "#ffffff"
    return g

_rez = build_rez()
render(_rez, "boss-resurrection.svg", scale=3, outline="#1e1408")
render(_whiten(_rez), "boss-resurrection-flash.svg", scale=3, outline="#1e1408")

# seed volley (dry spore mote)
g = new_grid(5, 5)
rect(g, 0, 0, 4, 4, DRY_DK)
rect(g, 1, 1, 3, 3, DRY)
px(g, 2, 2, DRY_LT)
render(g, "spore-dust.svg", scale=2)

# heavy orb (dust ball)
_DCORE = "#e6d2a0"
_DMID = "#b89a5a"
_DOUT = "#7a5a2e"
_DSPK = "#c9b078"
g = new_grid(16, 16)
rect(g, 4, 1, 11, 14, _DOUT)
rect(g, 1, 4, 14, 11, _DOUT)
rect(g, 3, 3, 12, 12, _DOUT)
rect(g, 5, 3, 10, 12, _DMID)
rect(g, 3, 5, 12, 10, _DMID)
rect(g, 6, 5, 9, 10, _DCORE)
rect(g, 5, 6, 10, 9, _DCORE)
for (x, y) in [(0, 7), (0, 8), (15, 7), (15, 8), (7, 0), (8, 0), (7, 15), (8, 15)]:
    px(g, x, y, _DSPK)
render(g, "dust-orb.svg", scale=2, outline="#2a1c0c")
