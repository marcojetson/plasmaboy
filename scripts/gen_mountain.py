"""Mountain-biome sprite set (see src/config/themes.ts 'mountain').

Cold alpine peaks: grey stone underfoot dusted with snow, clustered fir/pine trees, edelweiss
and snow-patch decor, and a rolling-pinecone walker. Regular foes reuse forest (thorn-bush,
sunflower) and cave (rockworm, fungus) skins; rockfall reuses the cave faller. The boss is a
giant gnarled ancient pinecone that flings a needle burst.

Pines are on a 24x34 grid at scale 3 (72x102) to match the forest bg-trees so the shared
treeLike trunk-collider lands correctly.
"""
from pixelart import new_grid, rect, px, render

# ======================================================================================
# Tile (scale 2, no outline) — grey alpine stone with snow, flush at the top
# ======================================================================================
ROCK = "#8a94a6"
ROCK_DK = "#6b7688"
ROCK_LT = "#a7b0c0"
SNOW = "#eef4fb"
SNOW_DK = "#cdd8e6"
g = new_grid(16, 16)
rect(g, 0, 0, 15, 15, ROCK)
rect(g, 0, 0, 15, 1, SNOW)                 # snow crest along the top
rect(g, 0, 2, 15, 2, SNOW_DK)
for y in (7, 12):
    rect(g, 0, y, 15, y, ROCK_DK)          # strata seams
for (x, y) in [(3, 5), (11, 9), (7, 13), (13, 6)]:
    px(g, x, y, ROCK_DK)
for (x, y) in [(5, 4), (9, 3), (2, 10)]:
    px(g, x, y, ROCK_LT)
px(g, 12, 1, "#ffffff")
render(g, "tile-mountain.svg", scale=2, outline=None)

# ======================================================================================
# Obstacle — fir/pine tree (SIGNATURE, treeLike). 24x34 grid, scale 3.
# ======================================================================================
PINE = "#2c6141"
PINE_DK = "#1c4a2e"
PINE_LT = "#3f8f52"
BARK = "#6b4a2a"
BARK_DK = "#4a3018"

def fir():
    g = new_grid(24, 34)
    # trunk
    rect(g, 10, 26, 13, 33, BARK)
    rect(g, 10, 26, 10, 33, "#7c5a34")
    rect(g, 13, 26, 13, 33, BARK_DK)
    # stacked triangular tiers (widest at the bottom), top-left lit
    tiers = [(3, 20, 20, 27), (5, 14, 18, 21), (6, 9, 17, 15), (8, 4, 15, 10)]
    for (x0, y0, x1, y1) in tiers:
        for yy in range(y0, y1 + 1):
            t = (yy - y0) / max(1, (y1 - y0))
            half = int((x1 - x0) / 2 * t)
            cx = (x0 + x1) // 2
            rect(g, cx - half, yy, cx + half, yy, PINE)
            px(g, cx - half, yy, PINE_LT)
            px(g, cx + half, yy, PINE_DK)
        rect(g, x0, y1, x1, y1, PINE_DK)         # shaded base of each tier
    # pointed top
    rect(g, 11, 2, 12, 4, PINE)
    px(g, 11, 2, PINE_LT)
    # snow dabs on the tier tips
    for (x, y) in [(11, 2), (6, 15), (17, 15), (4, 27), (19, 27), (8, 10), (15, 10)]:
        px(g, x, y, "#ffffff")
    return g

render(fir(), "pine-tree.svg", scale=3, outline="#0f2a1a")

# ======================================================================================
# Decor (scale 2)
# ======================================================================================
# edelweiss (white star flower)
g = new_grid(11, 11)
WOOL = "#f4f4ea"; WOOL_DK = "#cfcfc0"; CTR = "#e0b83a"
for (x, y) in [(5, 0), (5, 1), (0, 5), (1, 5), (9, 5), (10, 5), (5, 9), (5, 10),
               (2, 2), (8, 2), (2, 8), (8, 8)]:
    px(g, x, y, WOOL)
rect(g, 3, 3, 7, 7, WOOL)
rect(g, 4, 4, 6, 6, CTR)
px(g, 5, 5, "#fff3b0")
px(g, 3, 7, WOOL_DK); px(g, 7, 7, WOOL_DK)
render(g, "edelweiss.svg", scale=2, outline="#7a7a6a")

# snow patch (visual mound)
g = new_grid(12, 6)
rect(g, 1, 3, 10, 5, "#eef4fb")
rect(g, 2, 2, 8, 3, "#ffffff")
rect(g, 1, 5, 10, 5, "#cdd8e6")
px(g, 4, 4, "#dbe4f0"); px(g, 8, 4, "#ffffff")
render(g, "snow-patch.svg", scale=2, outline=None)

# ======================================================================================
# WALKER (NEW signature) — "pinecone": a rolling pinecone with a face. anim pinecone-roll
# ======================================================================================
PAD = 2
BW, BH = 14 + PAD * 2, 16
CONE = "#8a5a2e"
CONE_DK = "#5f3c18"
CONE_LT = "#ab7440"
SCALE = "#6b4522"

def pinecone(step):
    g = new_grid(BW, BH)
    o = PAD
    # egg-shaped body
    rect(g, 4 + o, 2, 9 + o, 13, CONE)
    rect(g, 3 + o, 4, 10 + o, 11, CONE)
    rect(g, 5 + o, 1, 8 + o, 2, CONE)
    rect(g, 3 + o, 4, 4 + o, 10, CONE_LT)          # lit left
    rect(g, 9 + o, 5, 10 + o, 11, CONE_DK)         # shaded right
    # overlapping scale chevrons, shifted per frame so it reads as rolling
    for row, yy in enumerate(range(3, 13, 2)):
        off = (row + step) % 2
        for xx in range(4, 10, 2):
            px(g, xx + o + off, yy, SCALE)
            px(g, xx + o + off - 1, yy + 1, CONE_DK)
            px(g, xx + o + off + 1, yy + 1, CONE_DK)
    # face + little feet
    px(g, 5 + o, 6, "#1a1a2e"); px(g, 8 + o, 6, "#1a1a2e")
    rect(g, 6 + o, 8, 7 + o, 8, CONE_DK)
    px(g, 4 + o, 14, CONE_DK); px(g, 9 + o, 14, CONE_DK)
    # top nub
    px(g, 6 + o, 0, "#7c5a34"); px(g, 8 + o, 0, "#7c5a34")
    return g

render(pinecone(0), "pinecone-0.svg", scale=2, outline="#2a1a0a")
render(pinecone(1), "pinecone-1.svg", scale=2, outline="#2a1a0a")

# ======================================================================================
# BOSS (NEW) — "Piñón Colosal": a giant ancient pinecone. special = spikeBurst (needles)
# ======================================================================================
BC = "#9c6832"
BC_DK = "#6b4522"
BC_LT = "#c48c4e"
BSCALE = "#7a4e26"
BMOUTH = "#4a2a12"
TOOTH = "#fff2e0"
NEEDLE = "#3f8f52"

def big_cone():
    g = new_grid(30, 40)
    # a fan of pine needles bursting from the crown
    for (x0, y0, x1, y1) in [(13, 8, 8, 1), (15, 8, 15, 0), (17, 8, 22, 1),
                             (11, 8, 4, 4), (19, 8, 26, 4)]:
        steps = max(abs(x1 - x0), abs(y1 - y0)) or 1
        for s in range(steps + 1):
            x = round(x0 + (x1 - x0) * s / steps)
            y = round(y0 + (y1 - y0) * s / steps)
            rect(g, x, max(0, y), x + 1, max(0, y), NEEDLE)
    # big egg-shaped cone body
    rect(g, 7, 9, 22, 37, BC)
    rect(g, 9, 7, 20, 9, BC)
    rect(g, 8, 34, 21, 37, BC)
    rect(g, 7, 9, 9, 37, BC_LT)                # lit left
    rect(g, 20, 9, 22, 37, BC_DK)              # shaded right
    rect(g, 8, 35, 21, 37, BC_DK)
    # overlapping scale chevron rows
    for row, yy in enumerate(range(10, 36, 3)):
        off = 2 if (row % 2) else 0
        for xx in range(8, 22, 4):
            rect(g, xx + off, yy, xx + off, yy, BSCALE)
            px(g, xx + off - 1, yy + 1, BC_DK)
            px(g, xx + off + 1, yy + 1, BC_DK)
    # snow dusting on the shoulders
    for (x, y) in [(9, 9), (12, 8), (16, 8), (19, 9), (11, 11), (18, 11)]:
        px(g, x, y, "#ffffff")
    # fanged maw
    rect(g, 11, 22, 18, 29, BMOUTH)
    rect(g, 11, 27, 18, 29, "#301a0a")
    for tx in range(11, 18, 2):
        rect(g, tx, 22, tx, 23, TOOTH)
        rect(g, tx + 1, 28, tx + 1, 29, TOOTH)
    # angry eyes
    rect(g, 10, 14, 13, 17, "#ffe066"); rect(g, 16, 14, 19, 17, "#ffe066")
    px(g, 11, 15, "#3a2a00"); px(g, 17, 15, "#3a2a00")
    rect(g, 10, 13, 13, 13, BC_DK); rect(g, 16, 13, 19, 13, BC_DK)   # brows
    return g

def all_white(src):
    g = [row[:] for row in src]
    for row in g:
        for x in range(len(row)):
            if row[x] is not None:
                row[x] = "#ffffff"
    return g

boss = big_cone()
render(boss, "boss-pinecone.svg", scale=3, outline="#241708")
render(all_white(boss), "boss-pinecone-flash.svg", scale=3, outline="#241708")

# ---- boss seed (woody pod) ----
g = new_grid(5, 5)
rect(g, 0, 0, 4, 4, BC_DK)
rect(g, 1, 1, 3, 3, BC_LT)
px(g, 2, 2, BSCALE)
render(g, "pinecone-boss-seed.svg", scale=2, outline="#241708")

# ---- boss heavy orb: an icy woody energy ball ----
g = new_grid(16, 16)
rect(g, 4, 1, 11, 14, BC_DK)
rect(g, 1, 4, 14, 11, BC_DK)
rect(g, 3, 3, 12, 12, BC_DK)
rect(g, 5, 3, 10, 12, BC)
rect(g, 3, 5, 12, 10, BC)
rect(g, 6, 5, 9, 10, "#eef4fb")
rect(g, 5, 6, 10, 9, "#eef4fb")
for (x, y) in [(0, 7), (0, 8), (15, 7), (15, 8), (7, 0), (8, 0), (7, 15), (8, 15)]:
    px(g, x, y, "#cdd8e6")
render(g, "pinecone-orb.svg", scale=2, outline="#241708")

# ---- boss spike-burst pine needle (bright green, reads against grey stone) ----
g = new_grid(9, 5)
rect(g, 0, 2, 6, 2, NEEDLE)
rect(g, 1, 2, 4, 2, "#63bf5f")
rect(g, 6, 1, 8, 3, "#d8f0d0")
px(g, 6, 0, "#63bf5f"); px(g, 6, 4, "#63bf5f")
render(g, "pinecone-needle.svg", scale=2, outline="#173a1a")

print("mountain done")
