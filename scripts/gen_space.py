"""Space-biome sprite set (see src/config/themes.ts 'space').

A botanical space-station / void garden where plants live sealed in glass bubbles (the
Little-Prince rose under its dome). Follows the forest/desert art conventions: small integer
grids, shared rect/px/render helpers, 1px cartoon outline on characters, no outline on tiles.

New art: the metal-deck floor, the signature glass-dome plant obstacle, star/glow decor, a
floating "orbling" walker (sprout in a bubble), a glass-pod spore plant, and the Cosmic Rose
boss. Every other enemy archetype reuses an existing biome's skin (the museum precedent).
"""
from pixelart import new_grid, rect, px, render

# ======================================================================================
# Tiles (scale 2, no outline — tessellate; full-fill so nothing looks like it floats)
# ======================================================================================
DECK = "#252c48"
DECK_DK = "#1b2138"
DECK_LT = "#333c5e"
STAR = "#eaf0ff"
GLOWC = "#5fe0ff"

# The void: an almost-black floor (NOT a grey panel deck — space, not a sidewalk). Two barely
# perceptible deep-blue specks keep a large tiled expanse from banding into one dead-flat colour.
# The actual stars are sparse non-obstacle decor placed on top, so the floor stays clean and dark.
VOID = "#070810"
g = new_grid(16, 16)
rect(g, 0, 0, 15, 15, VOID)
px(g, 4, 11, "#0d1122")
px(g, 12, 5, "#0d1122")
render(g, "tile-space.svg", scale=2, outline=None)

# ======================================================================================
# Obstacle — glass-dome plant (SIGNATURE): a rose sealed in a glass bubble on a metal base
# ======================================================================================
GLASS = "#bfe6ff"
GLASS_LT = "#eaffff"
GLASS_DK = "#7fb8e0"
BASE = "#4a5578"
BASE_DK = "#2f3852"
ROSE = "#ff5c7a"
ROSE_DK = "#c92a48"
ROSE_LT = "#ff9db0"
STEM = "#3f8f5a"

def glass_dome():
    g = new_grid(20, 24)
    # metal base pedestal
    rect(g, 4, 20, 15, 23, BASE)
    rect(g, 4, 20, 15, 20, "#5c688c")
    rect(g, 4, 22, 15, 23, BASE_DK)
    rect(g, 6, 18, 13, 20, BASE_DK)
    # rose inside
    rect(g, 9, 12, 10, 18, STEM)              # stem
    px(g, 8, 15, STEM)
    px(g, 11, 14, STEM)
    rect(g, 7, 8, 12, 12, ROSE)               # bloom
    rect(g, 8, 7, 11, 8, ROSE)
    rect(g, 7, 8, 8, 12, ROSE_LT)             # lit left
    rect(g, 11, 8, 12, 12, ROSE_DK)           # shaded right
    rect(g, 8, 9, 11, 11, ROSE_DK)            # spiral heart
    px(g, 9, 10, ROSE_LT)
    # glass dome over the top (thin translucent shell + big highlight arc)
    rect(g, 5, 3, 14, 4, GLASS)               # dome crown
    rect(g, 3, 5, 16, 6, GLASS)
    rect(g, 2, 7, 3, 18, GLASS)               # left wall
    rect(g, 16, 7, 17, 18, GLASS)             # right wall
    rect(g, 2, 18, 17, 19, GLASS_DK)          # dome foot ring
    rect(g, 6, 2, 13, 3, GLASS_LT)            # top highlight
    rect(g, 4, 5, 5, 12, GLASS_LT)            # streak highlight
    for (x, y) in [(14, 6), (15, 9), (16, 13)]:
        px(g, x, y, GLASS_DK)                 # shaded right curve
    return g

render(glass_dome(), "glass-dome.svg", scale=3, outline="#141830")

# ---- meteor rock (small asteroid obstacle) ----
MET = "#5a5f78"
MET_DK = "#3c4058"
MET_LT = "#767c98"
g = new_grid(16, 12)
rect(g, 2, 3, 13, 10, MET)
rect(g, 3, 2, 11, 3, MET_LT)
rect(g, 2, 9, 13, 10, MET_DK)
rect(g, 2, 3, 3, 9, MET_LT)
for (x, y) in [(5, 5), (9, 7), (11, 4)]:
    px(g, x, y, MET_DK)                        # craters
px(g, 6, 6, MET_LT)
render(g, "meteor-rock.svg", scale=2, outline="#191c2e")

# ---- asteroid (bigger space rock obstacle) ----
g = new_grid(22, 18)
rect(g, 3, 5, 18, 15, MET)
rect(g, 5, 3, 15, 5, MET)
rect(g, 4, 4, 6, 12, MET_LT)              # lit upper-left
rect(g, 3, 13, 18, 15, MET_DK)            # shaded underside
rect(g, 16, 6, 18, 14, MET_DK)
for (x, y) in [(8, 8), (13, 6), (11, 12), (15, 10)]:
    px(g, x, y, MET_DK)                    # craters
for (x, y) in [(6, 6), (10, 5), (9, 10)]:
    px(g, x, y, MET_LT)
render(g, "asteroid.svg", scale=2, outline="#191c2e")

# ======================================================================================
# Decor (scale 2, visual only)
# ======================================================================================
# twinkling star
g = new_grid(9, 9)
rect(g, 4, 1, 4, 7, STAR)
rect(g, 1, 4, 7, 4, STAR)
px(g, 4, 4, "#ffffff")
px(g, 3, 3, GLOWC); px(g, 5, 5, GLOWC)
render(g, "star-twinkle.svg", scale=2, outline=None)

# small dim far-off star (a faint 4-point speck)
g = new_grid(5, 5)
px(g, 2, 1, "#8aa0d0"); px(g, 2, 3, "#8aa0d0"); px(g, 1, 2, "#8aa0d0"); px(g, 3, 2, "#8aa0d0")
px(g, 2, 2, "#dfe8ff")
render(g, "star-far.svg", scale=2, outline=None)

# small glowing space bud
g = new_grid(9, 9)
rect(g, 3, 5, 5, 8, STEM)
rect(g, 2, 2, 6, 5, "#b06cff")
rect(g, 3, 1, 5, 2, "#d9a6ff")
px(g, 4, 3, "#f0e0ff")
px(g, 2, 3, "#8a4fd0"); px(g, 6, 4, "#8a4fd0")
render(g, "glow-bud.svg", scale=2, outline="#241a3a")

# ======================================================================================
# WALKER (NEW signature) — "orbling": a sprout floating inside a glass bubble. anim orbling-float
# ======================================================================================
PAD = 2
BW, BH = 14 + PAD * 2, 16
EYE = "#141830"

def orbling(bob):
    g = new_grid(BW, BH)
    o = PAD
    cy = 8 - bob
    # glass bubble
    rect(g, 3 + o, cy - 5, 10 + o, cy + 4, GLASS)
    rect(g, 2 + o, cy - 3, 11 + o, cy + 2, GLASS)
    rect(g, 4 + o, cy - 6, 9 + o, cy - 5, GLASS)
    rect(g, 4 + o, cy + 4, 9 + o, cy + 5, GLASS_DK)
    # inner void so the bubble reads hollow
    rect(g, 4 + o, cy - 4, 9 + o, cy + 3, "#1b2138")
    # sprout inside
    rect(g, 6 + o, cy - 1, 7 + o, cy + 3, STEM)
    rect(g, 4 + o, cy - 3, 6 + o, cy - 1, "#5fbf6f")   # left leaf
    rect(g, 7 + o, cy - 4, 9 + o, cy - 2, "#5fbf6f")   # right leaf
    px(g, 5 + o, cy, EYE); px(g, 8 + o, cy, EYE)        # eyes
    # glass highlights
    px(g, 4 + o, cy - 4, GLASS_LT); px(g, 3 + o, cy - 2, GLASS_LT)
    px(g, 10 + o, cy + 1, GLASS_DK)
    return g

render(orbling(0), "orbling-0.svg", scale=2, outline="#141830")
render(orbling(1), "orbling-1.svg", scale=2, outline="#141830")

# ======================================================================================
# SPORE (NEW) — glass-pod plant. forest counterpart: PoisonFlower
# ======================================================================================
POD = "#6fd0b0"
POD_DK = "#3f9a7a"
POD_LT = "#a8f0da"

# closed pod (a sealed teal bulb glinting under glass)
g = new_grid(12, 12)
rect(g, 4, 8, 7, 11, BASE_DK)                 # base
rect(g, 3, 3, 8, 9, POD)
rect(g, 4, 2, 7, 3, POD)
rect(g, 3, 3, 4, 9, POD_LT)
rect(g, 7, 3, 8, 9, POD_DK)
px(g, 5, 4, GLASS_LT); px(g, 4, 6, "#eaffff")  # glass glints
render(g, "podbloom-closed.svg", scale=2, outline="#141830")

# open pod (cracked, venting glowing spores)
g = new_grid(16, 16)
rect(g, 6, 12, 9, 15, BASE_DK)                # base
rect(g, 2, 5, 13, 11, POD)                    # split shell
rect(g, 3, 3, 12, 5, POD)
rect(g, 2, 10, 13, 11, POD_DK)
rect(g, 2, 5, 3, 11, POD_LT)
rect(g, 5, 6, 10, 10, "#173a30")              # dark maw
px(g, 6, 7, GLOWC); px(g, 9, 7, GLOWC)         # eyes
for (x, y) in [(7, 8), (8, 9), (4, 3), (11, 3), (13, 6)]:
    px(g, x, y, POD_LT)                        # escaping spores
render(g, "podbloom-open.svg", scale=2, outline="#141830")

# glowing spore projectile
g = new_grid(4, 4)
rect(g, 0, 0, 3, 3, "#4fbfa0")
px(g, 1, 1, "#d0fff0")
render(g, "pod-spore.svg", scale=2, outline="#123028")

# ======================================================================================
# BOSS (NEW) — "Rosa Cósmica": a glowing rose under a cracked glass dome. special = spikeBurst
# ======================================================================================
PET = "#ff5c7a"
PET_DK = "#c92a48"
PET_LT = "#ff9db0"
CORE = "#ffe066"
LEAF = "#3f8f5a"
LEAF_DK = "#2a6b40"
DOME = "#bfe6ff"
DOME_LT = "#eaffff"
DOME_DK = "#7fb8e0"

def cosmic_rose():
    g = new_grid(34, 40)
    # star base / soil mound on a metal saucer
    rect(g, 6, 34, 27, 39, BASE)
    rect(g, 6, 34, 27, 34, "#5c688c")
    rect(g, 4, 37, 29, 39, BASE_DK)
    # leaves fanning from the base
    rect(g, 3, 30, 10, 33, LEAF); rect(g, 3, 30, 10, 30, "#5fbf6f")
    rect(g, 23, 30, 30, 33, LEAF); rect(g, 23, 32, 30, 33, LEAF_DK)
    # thick stem
    rect(g, 15, 24, 18, 34, LEAF); rect(g, 15, 24, 15, 34, "#5fbf6f"); rect(g, 18, 24, 18, 34, LEAF_DK)
    # ---- the rose bloom (concentric petal rings, bright spiral heart) ----
    rect(g, 7, 8, 26, 25, PET)                 # outer petal mass
    rect(g, 9, 6, 24, 8, PET)
    rect(g, 7, 8, 9, 25, PET_LT)               # lit left
    rect(g, 24, 8, 26, 25, PET_DK)             # shaded right
    rect(g, 7, 23, 26, 25, PET_DK)             # under-shadow
    rect(g, 11, 11, 22, 22, PET_DK)            # inner petals
    rect(g, 13, 12, 20, 20, PET)
    rect(g, 14, 14, 19, 19, PET_LT)
    rect(g, 15, 15, 18, 18, CORE)              # glowing heart
    px(g, 16, 16, "#fff3b0")
    # petal seams for a folded look
    for (x, y) in [(12, 9), (21, 9), (10, 16), (23, 16), (13, 23), (20, 23)]:
        px(g, x, y, PET_DK)
    # subtle menacing eyes tucked in the petals
    px(g, 13, 13, "#3a1020"); px(g, 20, 13, "#3a1020")
    # ---- clear rounded glass dome (a bell/helmet) fully enclosing the bloom ----
    # Drawn as a 2px translucent shell so the rose shows through the open interior. The rounded
    # top + curved shoulders + straight side walls + a bright diagonal shine make it read
    # unmistakably as a glass dome rather than a flat cap.
    rect(g, 12, 1, 21, 2, DOME)                # crown
    rect(g, 9, 2, 12, 3, DOME); rect(g, 21, 2, 24, 3, DOME)   # shoulders
    rect(g, 7, 3, 9, 5, DOME); rect(g, 24, 3, 26, 5, DOME)    # upper curves
    rect(g, 5, 5, 7, 8, DOME); rect(g, 26, 5, 28, 8, DOME)    # curve into the walls
    rect(g, 4, 8, 5, 27, DOME); rect(g, 28, 8, 29, 27, DOME)  # side walls
    rect(g, 4, 27, 29, 28, DOME_DK)            # base rim where the dome meets the saucer
    # bright glass shine: a diagonal streak down the upper-left + a few top glints
    rect(g, 6, 8, 6, 18, DOME_LT)
    px(g, 7, 6, DOME_LT); px(g, 8, 4, DOME_LT); px(g, 13, 1, DOME_LT); px(g, 10, 3, DOME_LT)
    return g

def all_white(src):
    g = [row[:] for row in src]
    for row in g:
        for x in range(len(row)):
            if row[x] is not None:
                row[x] = "#ffffff"
    return g

boss = cosmic_rose()
render(boss, "boss-rose.svg", scale=3, outline="#141830")
render(all_white(boss), "boss-rose-flash.svg", scale=3, outline="#141830")

# ---- boss seed (small rose pod; unused by spikeBurst but part of the variant) ----
g = new_grid(5, 5)
rect(g, 0, 0, 4, 4, PET_DK)
rect(g, 1, 1, 3, 3, PET_LT)
px(g, 2, 2, CORE)
render(g, "rose-seed.svg", scale=2, outline="#3a1020")

# ---- boss heavy orb: a spiked cosmic orb (violet shell, pink core) ----
g = new_grid(16, 16)
rect(g, 4, 1, 11, 14, "#6a1b6f")
rect(g, 1, 4, 14, 11, "#6a1b6f")
rect(g, 3, 3, 12, 12, "#6a1b6f")
rect(g, 5, 3, 10, 12, "#b5179e")
rect(g, 3, 5, 12, 10, "#b5179e")
rect(g, 6, 5, 9, 10, "#ffd0f0")
rect(g, 5, 6, 10, 9, "#ffd0f0")
for (x, y) in [(0, 7), (0, 8), (15, 7), (15, 8), (7, 0), (8, 0), (7, 15), (8, 15)]:
    px(g, x, y, "#ff9db0")
render(g, "rose-orb.svg", scale=2, outline="#2a0a2e")

# ---- boss spike-burst shard: a bright star-shard (reads clearly against the dark deck) ----
g = new_grid(9, 5)
rect(g, 0, 2, 6, 2, "#5fe0ff")                # cyan shaft
rect(g, 1, 2, 4, 2, "#eaffff")               # bright core
rect(g, 6, 1, 8, 3, "#ffffff")               # white-hot tip
px(g, 6, 0, "#5fe0ff"); px(g, 6, 4, "#5fe0ff")  # star barbs
render(g, "rose-shard.svg", scale=2, outline="#123048")

print("space done")
