"""Swamp-theme sprite set for level 5 (see src/config/themes.ts 'swamp').

Same conventions as the other gen_*.py scripts. Enemy archetypes reskinned as bog life (bog
crawler / shooting reed / bog flower / leech / swamp mushroom) plus a dragonfly (the flyer),
the mud/log tiles, murky decor, and the lesser-bulrush (cattail) end boss.
"""
from pixelart import new_grid, rect, px, render

# ======================================================================================
# Palette
# ======================================================================================
MUD = "#5a4a32"
MUD_DK = "#3e321f"
MUD_LT = "#77613e"
GR_D = "#332815"
GR_L = "#836a44"
RG = "#5a7a3a"        # reed/plant green
RG_DK = "#3e5626"
RG_LT = "#84a552"
FLW = "#b6c24e"       # sickly bog-flower yellow-green
LEECH = "#4a6a5a"
LEECH_DK = "#31473c"
LEECH_BELLY = "#83ae9a"
SEED = "#7a5326"      # cattail seed-head brown
SEED_DK = "#573a19"
SEED_LT = "#9a6f3a"
FLUFF = "#e8dcc0"
FLUFF_DK = "#c9b88a"
EYEY = "#ffe066"
EYE_DK = "#3a2a00"

# ======================================================================================
# Tiles (scale 2, no outline) — filled edge-to-edge so things rest flush
# ======================================================================================
g = new_grid(16, 16)
rect(g, 0, 0, 15, 15, MUD)
rect(g, 0, 0, 15, 1, MUD_LT)       # wet sheen on top
rect(g, 0, 5, 15, 5, MUD_DK)
for x in (2, 6, 11, 14):
    px(g, x, 0, RG_DK)             # bits of algae on the surface
for (x, y) in [(3, 7), (9, 9), (12, 7), (6, 12), (2, 13), (14, 11)]:
    px(g, x, y, GR_D)
for (x, y) in [(5, 10), (10, 13), (7, 6)]:
    px(g, x, y, GR_L)
render(g, "tile-mud.svg", scale=2, outline=None)

g = new_grid(16, 16)
rect(g, 0, 0, 15, 15, MUD_DK)
rect(g, 0, 0, 15, 0, "#2c2417")
for (x, y) in [(2, 3), (9, 5), (6, 9), (12, 12), (3, 13), (14, 7)]:
    px(g, x, y, GR_D)
for (x, y) in [(5, 6), (11, 3), (8, 11)]:
    px(g, x, y, MUD)
render(g, "tile-mud-sub.svg", scale=2, outline=None)

# bog ledge: a mossy half-sunk log
g = new_grid(16, 16)
rect(g, 0, 0, 15, 15, "#5a4a2e")
rect(g, 0, 0, 15, 1, "#6f5a38")
for y in (4, 5, 9, 10, 14):
    rect(g, 0, y, 15, y, "#463722")
moss = [1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0]
for x, m in enumerate(moss):
    if m:
        px(g, x, 0, RG_LT)
        px(g, x, 1, RG)
render(g, "tile-bog.svg", scale=2, outline=None)

# ======================================================================================
# Background scenery (scale 3, dark outline), origin bottom
# ======================================================================================
def dead_tree():
    g = new_grid(24, 34)
    TR = "#4a3a26"
    TR_DK = "#31261a"
    TR_LT = "#5f4c32"
    rect(g, 10, 8, 13, 33, TR)
    rect(g, 10, 8, 11, 33, TR_LT)
    rect(g, 12, 8, 13, 33, TR_DK)
    # bare branches
    rect(g, 5, 10, 10, 11, TR)
    rect(g, 4, 6, 6, 11, TR)
    rect(g, 13, 13, 19, 14, TR)
    rect(g, 18, 8, 20, 14, TR)
    rect(g, 11, 3, 12, 8, TR)
    px(g, 6, 14, RG_DK)  # a bit of clinging moss
    return g

render(dead_tree(), "dead-tree.svg", scale=3, outline="#161009")

def reed_clump():
    g = new_grid(24, 34)
    for bx, top in ((5, 6), (9, 2), (13, 8), (17, 4)):
        rect(g, bx, top, bx + 1, 33, RG)
        px(g, bx, top, RG_LT)
    # a couple of brown seed-heads
    rect(g, 8, 4, 10, 9, SEED)
    rect(g, 16, 6, 18, 11, SEED)
    px(g, 9, 5, SEED_LT)
    return g

render(reed_clump(), "reed-clump.svg", scale=3, outline="#16240e")

# ======================================================================================
# Ground decor (scale 2)
# ======================================================================================
# lily pad
g = new_grid(14, 7)
rect(g, 1, 2, 12, 5, RG)
rect(g, 2, 1, 11, 2, RG)
rect(g, 1, 4, 12, 5, RG_DK)
rect(g, 6, 3, 8, 5, MUD_DK)   # the pad's wedge notch
px(g, 3, 2, RG_LT)
px(g, 9, 2, "#ff9ecf")        # tiny lily flower
render(g, "lily-pad.svg", scale=2)

# reeds
g = new_grid(10, 12)
for x in (2, 4, 6, 8):
    rect(g, x, 3, x, 11, RG)
    px(g, x, 3, RG_LT)
rect(g, 4, 1, 5, 4, SEED)     # a little seed-head
render(g, "reed.svg", scale=2, outline=None)

# swamp mushroom
g = new_grid(10, 12)
rect(g, 4, 5, 5, 11, "#c8c0a0")
rect(g, 1, 2, 8, 6, "#7a8a3a")
rect(g, 2, 1, 7, 2, "#7a8a3a")
rect(g, 1, 5, 8, 6, "#5c6a28")
px(g, 3, 3, "#b6c24e")
px(g, 6, 4, "#b6c24e")
render(g, "swamp-mushroom.svg", scale=2)

# bog rock (mossy)
g = new_grid(12, 8)
rect(g, 1, 3, 10, 7, "#6a6a5a")
rect(g, 2, 2, 8, 3, "#7f7f6c")
rect(g, 1, 6, 10, 7, "#4a4a3c")
px(g, 3, 3, RG)
px(g, 8, 4, RG_DK)
render(g, "bog-rock.svg", scale=2)

# ======================================================================================
# WALKER — bog crawler (2 frames)
# ======================================================================================
PAD = 2
BW, BH = 14 + PAD * 2, 14
BG = "#6a7a4a"
BG_DK = "#48592f"
BG_LT = "#8fa464"

def bog_crawl(sway):
    g = new_grid(BW, BH)
    o = PAD
    top = 3 - sway
    rect(g, 2 + o, top + 2, 13 + o, 13, BG)
    rect(g, 1 + o, 6, 14 + o, 11, BG)
    rect(g, 1 + o, 6, 2 + o, 11, BG_LT)
    rect(g, 13 + o, 6, 14 + o, 11, BG_DK)
    rect(g, 2 + o, 12, 13 + o, 13, BG_DK)
    for (x, y) in [(5, 8), (10, 9), (7, 6)]:
        px(g, x + o, y, "#c8d89a")   # slimy speckles
    px(g, 6 + o, 8, "#1a1a12")
    px(g, 9 + o, 8, "#1a1a12")
    return g

render(bog_crawl(0), "bog-crawl-0.svg", scale=2)
render(bog_crawl(1), "bog-crawl-1.svg", scale=2)

# ======================================================================================
# STRAIGHT SHOOTER — shooting reed clump
# ======================================================================================
def reed_shooter(firing):
    g = new_grid(15, 15)
    rect(g, 5, 1, 9, 13, RG)
    rect(g, 3, 4, 11, 11, RG)
    rect(g, 5, 1, 6, 13, RG_LT)
    rect(g, 9, 1, 9, 13, RG_DK)
    rect(g, 3, 11, 11, 12, RG_DK)
    for y in (3, 6, 9):
        px(g, 1, y, RG_LT)
        px(g, 13, y, RG_LT)
    px(g, 7, 0, SEED)
    px(g, 5, 5, EYEY)
    px(g, 9, 5, EYEY)
    if firing:
        rect(g, 6, 7, 8, 9, "#c8d84a")
    else:
        rect(g, 6, 8, 8, 8, RG_DK)
    return g

render(reed_shooter(False), "reed-idle.svg", scale=2)
render(reed_shooter(True), "reed-fire.svg", scale=2)

g = new_grid(6, 3)
rect(g, 0, 1, 4, 1, RG_DK)
px(g, 5, 0, RG_LT)
px(g, 5, 2, RG_LT)
px(g, 0, 1, "#c8d84a")
render(g, "reed-dart.svg", scale=2)

# ======================================================================================
# AIMER — bog flower (rotates to track)
# ======================================================================================
def bogflower(firing):
    g = new_grid(14, 14)
    rect(g, 6, 0, 7, 13, FLW)
    rect(g, 0, 6, 13, 7, FLW)
    rect(g, 2, 2, 4, 4, FLW)
    rect(g, 9, 2, 11, 4, FLW)
    rect(g, 2, 9, 4, 11, FLW)
    rect(g, 9, 9, 11, 11, FLW)
    for (x, y) in [(6, 0), (7, 0), (0, 6), (0, 7), (13, 6), (13, 7), (6, 13), (7, 13),
                   (2, 2), (11, 2), (2, 11), (11, 11)]:
        px(g, x, y, "#e0ec9a")
    core = "#fff0a0" if firing else "#4a5626"
    rect(g, 4, 4, 9, 9, core)
    px(g, 5, 6, "#1a1a12")
    px(g, 8, 6, "#1a1a12")
    return g

render(bogflower(False), "bogflower-idle.svg", scale=2)
render(bogflower(True), "bogflower-fire.svg", scale=2)

g = new_grid(4, 4)
rect(g, 0, 0, 3, 3, FLW)
px(g, 1, 1, "#eef7b0")
px(g, 2, 2, "#4a5626")
render(g, "bog-seed.svg", scale=2)

# ======================================================================================
# BURROW-CHARGER — leech
# ======================================================================================
LMOUTH = "#7a1f2f"
# mound (mud hole)
g = new_grid(15, 6)
rect(g, 2, 3, 12, 5, MUD)
rect(g, 4, 2, 10, 3, MUD)
rect(g, 2, 5, 12, 5, MUD_DK)
rect(g, 6, 3, 8, 5, "#20180e")
render(g, "leech-mound.svg", scale=2)

# emerging
g = new_grid(12, 15)
rect(g, 3, 4, 8, 14, LEECH)
rect(g, 4, 4, 7, 14, LEECH_BELLY)
rect(g, 3, 12, 8, 14, LEECH_DK)
for sy in (7, 10, 13):
    rect(g, 3, sy, 8, sy, LEECH_DK)
px(g, 4, 6, "#1a1a12")
px(g, 7, 6, "#1a1a12")
rect(g, 4, 8, 7, 9, LMOUTH)
render(g, "leech-emerge.svg", scale=2)

# charging
g = new_grid(13, 13)
rect(g, 1, 5, 11, 11, LEECH)
rect(g, 1, 5, 11, 7, LEECH_BELLY)
rect(g, 1, 10, 11, 11, LEECH_DK)
for sx in (4, 7):
    rect(g, sx, 5, sx, 11, LEECH_DK)
px(g, 9, 5, "#1a1a12")
px(g, 9, 8, "#1a1a12")
rect(g, 10, 6, 12, 8, LMOUTH)
render(g, "leech-charge.svg", scale=2)

# ======================================================================================
# SPORE — swamp mushroom
# ======================================================================================
SM = "#7a8a3a"
SM_DK = "#566327"
SM_LT = "#a4b45a"
g = new_grid(12, 12)
rect(g, 4, 7, 7, 11, "#c8c0a0")
rect(g, 2, 2, 9, 8, SM)
rect(g, 3, 1, 8, 2, SM)
rect(g, 2, 2, 3, 8, SM_LT)
rect(g, 8, 2, 9, 8, SM_DK)
for (x, y) in [(5, 0), (1, 4), (10, 4)]:
    px(g, x, y, SM_LT)
render(g, "swampshroom-closed.svg", scale=2)

g = new_grid(16, 16)
rect(g, 6, 11, 9, 15, "#c8c0a0")
rect(g, 2, 4, 13, 10, SM)
rect(g, 3, 2, 12, 4, SM)
rect(g, 2, 9, 13, 10, SM_DK)
rect(g, 2, 4, 3, 10, SM_LT)
rect(g, 5, 5, 10, 9, "#3a4418")
px(g, 6, 6, EYEY)
px(g, 9, 6, EYEY)
for (x, y) in [(7, 7), (8, 8), (4, 3), (11, 3)]:
    px(g, x, y, "#d6e29a")
render(g, "swampshroom-open.svg", scale=2)

g = new_grid(4, 4)
rect(g, 0, 0, 3, 3, SM_LT)
px(g, 1, 1, "#d6e29a")
render(g, "swamp-spore.svg", scale=2)

# ======================================================================================
# FLYER — dragonfly (2-frame wing beat). Drawn facing LEFT (the Flyer flips it going right).
# ======================================================================================
DR = "#3a9a8a"
DR_DK = "#2a6f64"
DR_LT = "#6fd0c0"
WING = "#cfe8e0"
WING_DK = "#a0c8be"

def dragonfly(wings_up):
    g = new_grid(20, 12)
    # head (left) with eyes
    rect(g, 1, 4, 4, 7, DR)
    px(g, 1, 4, "#12242a")
    px(g, 1, 7, "#12242a")
    # thorax
    rect(g, 5, 4, 8, 7, DR)
    rect(g, 5, 4, 8, 4, DR_LT)
    # long abdomen to the right
    rect(g, 9, 5, 18, 6, DR)
    rect(g, 15, 5, 18, 6, DR_DK)
    # two wing pairs off the thorax
    if wings_up:
        rect(g, 5, 0, 9, 2, WING)
        rect(g, 8, 0, 12, 2, WING)
        rect(g, 5, 0, 12, 0, WING_DK)
    else:
        rect(g, 5, 8, 9, 10, WING)
        rect(g, 8, 8, 12, 10, WING)
        rect(g, 5, 10, 12, 10, WING_DK)
    return g

render(dragonfly(True), "dragon-0.svg", scale=2, outline="#0e1c1a")
render(dragonfly(False), "dragon-1.svg", scale=2, outline="#0e1c1a")

# ======================================================================================
# BOSS — lesser bulrush / cattail (Typha). Tall reed with a fanged brown seed-head.
# ======================================================================================
def build_bulrush():
    g = new_grid(30, 44)
    cx = 15
    # leaf blades from the base
    rect(g, 4, 20, 6, 43, RG)
    rect(g, 3, 24, 5, 43, RG_DK)
    rect(g, 23, 20, 25, 43, RG)
    rect(g, 24, 24, 26, 43, RG_DK)
    rect(g, 8, 28, 9, 43, RG_LT)
    rect(g, 20, 28, 21, 43, RG_LT)
    # main stalk
    rect(g, cx - 2, 6, cx + 2, 43, RG)
    rect(g, cx - 2, 6, cx - 1, 43, RG_LT)
    rect(g, cx + 1, 6, cx + 2, 43, RG_DK)
    # thin tip above the head
    rect(g, cx - 1, 1, cx, 8, RG_LT)
    # brown seed-head (the "cigar")
    rect(g, cx - 5, 12, cx + 5, 30, SEED)
    rect(g, cx - 5, 12, cx - 3, 30, SEED_LT)
    rect(g, cx + 3, 12, cx + 5, 30, SEED_DK)
    rect(g, cx - 5, 12, cx + 5, 13, SEED_DK)
    rect(g, cx - 5, 29, cx + 5, 30, SEED_DK)
    for (x, y) in [(cx - 3, 16), (cx + 2, 19), (cx - 1, 24), (cx + 3, 27), (cx - 4, 28)]:
        px(g, x, y, SEED_LT)
    # fanged face on the seed-head
    rect(g, cx - 3, 16, cx - 1, 18, EYEY)
    px(g, cx - 3, 17, EYE_DK)
    rect(g, cx + 1, 16, cx + 3, 18, EYEY)
    px(g, cx + 3, 17, EYE_DK)
    rect(g, cx - 3, 15, cx - 1, 15, SEED_DK)
    rect(g, cx + 1, 15, cx + 3, 15, SEED_DK)
    rect(g, cx - 3, 21, cx + 3, 25, "#5a1a1a")
    rect(g, cx - 3, 24, cx + 3, 25, "#360f0f")
    for tx in (cx - 2, cx, cx + 2):
        px(g, tx, 21, "#fff2e0")
    return g

def _whiten(src):
    g = [row[:] for row in src]
    for row in g:
        for x in range(len(row)):
            if row[x] is not None:
                row[x] = "#ffffff"
    return g

_bul = build_bulrush()
render(_bul, "boss-bulrush.svg", scale=3, outline="#14200c")
render(_whiten(_bul), "boss-bulrush-flash.svg", scale=3, outline="#14200c")

# seed volley (fluffy seed)
g = new_grid(5, 5)
rect(g, 1, 1, 3, 3, FLUFF)
px(g, 0, 2, FLUFF_DK)
px(g, 4, 2, FLUFF_DK)
px(g, 2, 0, FLUFF_DK)
px(g, 2, 4, FLUFF_DK)
px(g, 2, 2, "#ffffff")
render(g, "bulrush-seed.svg", scale=2)

# heavy orb (big fuzzy seed ball)
g = new_grid(16, 16)
rect(g, 4, 1, 11, 14, FLUFF_DK)
rect(g, 1, 4, 14, 11, FLUFF_DK)
rect(g, 3, 3, 12, 12, FLUFF_DK)
rect(g, 5, 3, 10, 12, FLUFF)
rect(g, 3, 5, 12, 10, FLUFF)
rect(g, 6, 5, 9, 10, "#ffffff")
rect(g, 5, 6, 10, 9, "#ffffff")
for (x, y) in [(0, 6), (0, 9), (15, 6), (15, 9), (6, 0), (9, 0), (6, 15), (9, 15), (2, 2), (13, 2), (2, 13), (13, 13)]:
    px(g, x, y, "#fff8e8")
render(g, "bulrush-orb.svg", scale=2, outline="#9a8a5a")

# spikeBurst fluff tuft
g = new_grid(7, 7)
rect(g, 2, 1, 4, 5, FLUFF)
rect(g, 1, 2, 5, 4, FLUFF)
px(g, 3, 3, "#ffffff")
px(g, 0, 3, FLUFF_DK)
px(g, 6, 3, FLUFF_DK)
px(g, 3, 0, FLUFF_DK)
px(g, 3, 6, FLUFF_DK)
render(g, "bulrush-fluff.svg", scale=2, outline="#9a8a5a")
