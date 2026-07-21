"""Desert-theme sprite set for level 2 (see src/config/themes.ts 'desert').

Mirrors the forest art conventions in the other gen_*.py scripts: small integer grids, the
shared rect/px/render helpers, a 1px cartoon outline on characters, no outline on tiles. Enemy
skins keep the same silhouettes/roles as their forest counterparts (walker, straight-shooter,
aimer, burrow-charger, spore) so the reskin drops into the existing behavior classes unchanged.
"""
from pixelart import new_grid, rect, px, render

# ======================================================================================
# Tiles (scale 2, no outline — they tessellate)
# ======================================================================================
SAND = "#e6c07a"
SAND_DK = "#cfa25c"
SAND_LT = "#f2d79a"
GRAIN_D = "#b98a44"
GRAIN_L = "#f7e6b8"

# ---- sand ground: warm dune surface, filled edge-to-edge so the top of the tile IS the
# surface (feet rest flush, no transparent gap that would make things look like they float).
# The top is a soft speckled crest — NOT a hard bright band — so the sand reads naturally and
# sits at the same visual height as the forest floor. ----
g = new_grid(16, 16)
rect(g, 0, 0, 15, 15, SAND)        # full fill, surface flush at the very top row
rect(g, 0, 5, 15, 5, SAND_DK)      # one soft seam low in the body for layered depth
# scattered sun-bleached grains along the crest (sparse dots, not a solid stripe)
for x in (1, 4, 5, 9, 12, 13):
    px(g, x, 0, SAND_LT)
for (x, y) in [(3, 7), (9, 9), (12, 7), (6, 12), (2, 13), (14, 11)]:
    px(g, x, y, GRAIN_D)
for (x, y) in [(5, 10), (10, 13), (7, 6), (14, 8)]:
    px(g, x, y, GRAIN_L)
render(g, "tile-sand.svg", scale=2, outline=None)

# ---- sub-sand: plain packed sand for rows below the surface ----
g = new_grid(16, 16)
rect(g, 0, 0, 15, 15, SAND)
rect(g, 0, 0, 15, 0, SAND_DK)  # layered seam
for (x, y) in [(2, 3), (9, 5), (6, 9), (12, 12), (3, 13), (14, 7), (1, 9)]:
    px(g, x, y, GRAIN_D)
for (x, y) in [(5, 6), (11, 3), (8, 11), (13, 14)]:
    px(g, x, y, GRAIN_L)
render(g, "tile-sand-sub.svg", scale=2, outline=None)

# ---- sandstone ledge: horizontal rock strata ----
ROCK = "#cf9a55"
ROCK_DK = "#a8743a"
ROCK_LT = "#e6b877"
g = new_grid(16, 16)
rect(g, 0, 0, 15, 15, ROCK)
rect(g, 0, 0, 15, 1, ROCK_LT)  # sunlit top lip
for y in (4, 5, 9, 10, 14):
    rect(g, 0, y, 15, y, ROCK_DK)  # strata seams
px(g, 4, 7, ROCK_DK)
px(g, 11, 12, ROCK_DK)
px(g, 8, 2, ROCK_LT)
render(g, "tile-sandstone.svg", scale=2, outline=None)

# ======================================================================================
# Background scenery (scale 3, dark outline) — saguaro + rock mesa, drawn origin bottom
# ======================================================================================
CBODY = "#3f8f3a"
CBODY_DK = "#2f6a2a"
CBODY_LT = "#5fae4a"
CRIB = "#2a5f26"

def saguaro():
    g = new_grid(24, 34)
    # trunk
    rect(g, 9, 4, 15, 33, CBODY)
    rect(g, 9, 4, 10, 33, CBODY_LT)
    rect(g, 14, 4, 15, 33, CBODY_DK)
    rect(g, 11, 2, 13, 5, CBODY)  # rounded crown
    # left arm
    rect(g, 3, 16, 9, 20, CBODY)
    rect(g, 3, 10, 5, 18, CBODY)
    rect(g, 3, 10, 3, 18, CBODY_LT)
    # right arm
    rect(g, 15, 13, 21, 17, CBODY)
    rect(g, 19, 7, 21, 15, CBODY)
    rect(g, 20, 7, 21, 15, CBODY_DK)
    # ribs
    for rx in (11, 13):
        rect(g, rx, 5, rx, 32, CRIB)
    return g

render(saguaro(), "cactus-bg.svg", scale=3, outline="#123010")

def mesa():
    ROCKB = "#c07a3a"
    ROCKB_DK = "#9a5a28"
    ROCKB_LT = "#d99a5a"
    g = new_grid(24, 34)
    rect(g, 2, 14, 21, 33, ROCKB)
    rect(g, 2, 14, 21, 15, ROCKB_LT)     # flat sunlit top
    rect(g, 2, 14, 4, 33, ROCKB_LT)
    rect(g, 18, 14, 21, 33, ROCKB_DK)
    # a lower shoulder step for a butte silhouette
    rect(g, 14, 22, 23, 33, ROCKB)
    rect(g, 14, 22, 23, 23, ROCKB_LT)
    rect(g, 21, 22, 23, 33, ROCKB_DK)
    for y in (19, 26, 30):
        rect(g, 3, y, 20, y, ROCKB_DK)   # strata
    return g

render(mesa(), "mesa-bg.svg", scale=3, outline="#5a3418")

# ======================================================================================
# Ground decor (scale 2, outline) — small cactus, rock, dry shrub
# ======================================================================================
# small barrel cactus
g = new_grid(12, 12)
rect(g, 3, 3, 8, 11, CBODY)
rect(g, 3, 3, 4, 11, CBODY_LT)
rect(g, 7, 3, 8, 11, CBODY_DK)
rect(g, 5, 2, 6, 3, CBODY)          # nub top
for rx in (5, 7):
    rect(g, rx, 4, rx, 10, CRIB)
px(g, 4, 5, "#e8f0c0")               # spines
px(g, 8, 7, "#e8f0c0")
px(g, 5, 1, "#ff5c7a")               # tiny flower
render(g, "cactus-small.svg", scale=2)

# desert rock
g = new_grid(12, 8)
rect(g, 1, 3, 10, 7, "#b0895a")
rect(g, 2, 2, 8, 3, "#c79b66")
rect(g, 1, 6, 10, 7, "#8f6a40")
px(g, 3, 4, "#d9b483")
px(g, 7, 5, "#8f6a40")
render(g, "rock.svg", scale=2)

# dry shrub / tumble-brush
g = new_grid(12, 8)
BR = "#b58a4a"
BR_DK = "#8a6633"
for (x0, y0, x1, y1) in [(2, 4, 9, 7), (3, 2, 8, 4)]:
    rect(g, x0, y0, x1, y1, BR)
rect(g, 2, 6, 9, 7, BR_DK)
for (x, y) in [(3, 3), (6, 1), (9, 3), (5, 5), (8, 5)]:
    px(g, x, y, BR_DK)
render(g, "dry-shrub.svg", scale=2)

# ======================================================================================
# WALKER — barrel-cactus roller (2 frames), forest counterpart: WalkingMushroom
# ======================================================================================
PAD = 2
BW, BH = 14 + PAD * 2, 14
BEYE = "#1a1a2e"
BBROW = "#1f4a1a"

def barrel(bounce):
    g = new_grid(BW, BH)
    o = PAD
    top = 3 - bounce         # squash/stretch the crown for a rolling bounce
    rect(g, 2 + o, top + 2, 13 + o, 13, CBODY)
    rect(g, 1 + o, 6, 14 + o, 11, CBODY)      # bulged middle
    rect(g, 1 + o, 6, 2 + o, 11, CBODY_LT)
    rect(g, 13 + o, 6, 14 + o, 11, CBODY_DK)
    rect(g, 2 + o, 12, 13 + o, 13, CBODY_DK)
    for rx in (5, 8, 11):
        rect(g, rx + o, top + 3, rx + o, 12, CRIB)
    # spines
    for (x, y) in [(4, 6), (7, 8), (10, 6), (6, 10), (9, 11)]:
        px(g, x + o, y, "#e8f0c0")
    # flower crown
    rect(g, 6 + o, top, 8 + o, top + 1, "#ff5c7a")
    px(g, 7 + o, top, "#ffd23f")
    # angry eyes
    px(g, 5 + o, 7, BBROW)
    px(g, 6 + o, 7, BBROW)
    px(g, 9 + o, 7, BBROW)
    px(g, 10 + o, 7, BBROW)
    px(g, 6 + o, 8, BEYE)
    px(g, 9 + o, 8, BEYE)
    return g

render(barrel(0), "barrel-0.svg", scale=2)
render(barrel(1), "barrel-1.svg", scale=2)

# ======================================================================================
# STRAIGHT SHOOTER — needle cactus, forest counterpart: ThornBush
# ======================================================================================
NEEDLE = "#e8f0c0"

def needle_cactus(firing):
    g = new_grid(15, 15)
    rect(g, 5, 1, 9, 13, CBODY)            # central pad
    rect(g, 3, 4, 11, 11, CBODY)
    rect(g, 5, 1, 6, 13, CBODY_LT)
    rect(g, 9, 1, 9, 13, CBODY_DK)
    rect(g, 3, 11, 11, 12, CBODY_DK)
    for rx in (7,):
        rect(g, rx, 2, rx, 12, CRIB)
    # needles bristling outward
    for y in (4, 7, 10):
        px(g, 1, y, NEEDLE)
        px(g, 13, y, NEEDLE)
    px(g, 7, 0, NEEDLE)
    # angry eyes
    px(g, 5, 5, "#ffe066")
    px(g, 9, 5, "#ffe066")
    # mouth
    if firing:
        rect(g, 6, 7, 8, 9, "#ff6f3c")
    else:
        rect(g, 6, 8, 8, 8, "#5c1a2e")
    return g

render(needle_cactus(False), "needle-cactus-idle.svg", scale=2)
render(needle_cactus(True), "needle-cactus-fire.svg", scale=2)

# needle projectile
g = new_grid(6, 3)
rect(g, 0, 1, 5, 1, "#7a5a2a")
px(g, 5, 0, NEEDLE)
px(g, 5, 2, NEEDLE)
px(g, 0, 1, "#d9c58a")
render(g, "cactus-needle.svg", scale=2)

# ======================================================================================
# AIMER — agave bloom (rotates to track), forest counterpart: AngrySunflower
# ======================================================================================
AG = "#5fae4a"
AG_DK = "#3f8f3a"
AG_TIP = "#cfe08a"

def agave(firing):
    g = new_grid(14, 14)
    # radial rosette of pointed leaves
    rect(g, 6, 0, 7, 13, AG)     # vertical pair
    rect(g, 0, 6, 13, 7, AG)     # horizontal pair
    rect(g, 2, 2, 4, 4, AG)      # diagonals
    rect(g, 9, 2, 11, 4, AG)
    rect(g, 2, 9, 4, 11, AG)
    rect(g, 9, 9, 11, 11, AG)
    # leaf tips (pale spines)
    for (x, y) in [(6, 0), (7, 0), (0, 6), (0, 7), (13, 6), (13, 7), (6, 13), (7, 13),
                   (2, 2), (11, 2), (2, 11), (11, 11)]:
        px(g, x, y, AG_TIP)
    # menacing core
    core = "#ff914d" if firing else "#6b4423"
    rect(g, 4, 4, 9, 9, core)
    rect(g, 4, 8, 9, 9, AG_DK if not firing else "#ff6f3c")
    px(g, 5, 6, "#1a1a2e")
    px(g, 8, 6, "#1a1a2e")
    return g

render(agave(False), "agave-idle.svg", scale=2)
render(agave(True), "agave-fire.svg", scale=2)

# agave seed projectile
g = new_grid(4, 4)
rect(g, 0, 0, 3, 3, "#cfe08a")
px(g, 1, 1, "#f2f7d0")
px(g, 2, 2, "#8faa4a")
render(g, "agave-seed.svg", scale=2)

# ======================================================================================
# BURROW-CHARGER — sandworm, forest counterpart: VineWorm
# ======================================================================================
SDIRT = "#cfa25c"
SDIRT_DK = "#a8743a"
WBODY = "#d98a5a"
WBODY_DK = "#a85f34"
WBELLY = "#f0c088"
WMOUTH = "#7a1f1f"

# mound (burrowed)
g = new_grid(15, 6)
rect(g, 2, 3, 12, 5, SDIRT)
rect(g, 4, 2, 10, 3, SDIRT)
rect(g, 2, 5, 12, 5, SDIRT_DK)
px(g, 5, 3, SDIRT_DK)
px(g, 9, 4, SDIRT_DK)
render(g, "sandworm-mound.svg", scale=2)

# emerging (rising, mouth open)
g = new_grid(12, 15)
rect(g, 3, 4, 8, 14, WBODY)
rect(g, 4, 4, 7, 14, WBELLY)
rect(g, 3, 12, 8, 14, WBODY_DK)
for sy in (7, 10, 13):
    rect(g, 3, sy, 8, sy, WBODY_DK)   # body segments
px(g, 4, 6, "#1a1a2e")
px(g, 7, 6, "#1a1a2e")
rect(g, 4, 8, 7, 9, WMOUTH)
render(g, "sandworm-emerge.svg", scale=2)

# charging (lunging forward)
g = new_grid(13, 13)
rect(g, 1, 5, 11, 11, WBODY)
rect(g, 1, 5, 11, 7, WBELLY)
rect(g, 1, 10, 11, 11, WBODY_DK)
for sx in (4, 7):
    rect(g, sx, 5, sx, 11, WBODY_DK)  # segments
px(g, 9, 5, "#1a1a2e")
px(g, 9, 8, "#1a1a2e")
rect(g, 10, 6, 12, 8, WMOUTH)
render(g, "sandworm-charge.svg", scale=2)

# ======================================================================================
# SPORE — spore puffball, forest counterpart: PoisonFlower
# ======================================================================================
PUFF = "#a9963f"
PUFF_DK = "#7c6d2a"
PUFF_LT = "#cbb75a"
DUST = "#efe3a8"

# closed puffball (spiky ball bud)
g = new_grid(12, 12)
rect(g, 4, 7, 7, 11, "#6b4423")       # short stem
rect(g, 2, 2, 9, 8, PUFF)
rect(g, 3, 1, 8, 2, PUFF)
rect(g, 2, 2, 3, 8, PUFF_LT)
rect(g, 8, 2, 9, 8, PUFF_DK)
for (x, y) in [(5, 0), (1, 4), (10, 4), (2, 7), (9, 7)]:
    px(g, x, y, "#e8f0c0")             # spines
render(g, "puffball-closed.svg", scale=2)

# open puffball (burst, spewing dust)
g = new_grid(16, 16)
rect(g, 6, 11, 9, 15, "#6b4423")       # stem
rect(g, 2, 4, 13, 10, PUFF)            # split-open dome
rect(g, 3, 2, 12, 4, PUFF)
rect(g, 2, 9, 13, 10, PUFF_DK)
rect(g, 2, 4, 3, 10, PUFF_LT)
rect(g, 5, 5, 10, 9, PUFF_DK)          # dark maw
px(g, 6, 6, "#ffe066")                 # eyes
px(g, 9, 6, "#ffe066")
for (x, y) in [(7, 7), (8, 8), (4, 3), (11, 3)]:
    px(g, x, y, DUST)                  # escaping spores
render(g, "puffball-open.svg", scale=2)

# puff spore projectile
g = new_grid(4, 4)
rect(g, 0, 0, 3, 3, "#b8a24a")
px(g, 1, 1, DUST)
render(g, "puff-spore.svg", scale=2)

# ======================================================================================
# BOSS — giant carnivorous saguaro, forest counterpart: MiniBoss (Venus flytrap)
# ======================================================================================
BSP = "#e8f0c0"
BMOUTH = "#a01f3a"
BMOUTH_DK = "#6e1226"
BTOOTH = "#fff2e0"
BEYEC = "#ffe066"
BEYE_DK = "#3a2a00"
BFLOWER = "#ff5c7a"

def boss_cactus():
    g = new_grid(34, 40)
    # --- main trunk ---
    rect(g, 11, 4, 23, 39, CBODY)
    rect(g, 11, 4, 13, 39, CBODY_LT)
    rect(g, 21, 4, 23, 39, CBODY_DK)
    rect(g, 13, 2, 21, 5, CBODY)      # rounded crown
    # --- arms raised like a menacing pose ---
    # left arm
    rect(g, 3, 18, 12, 23, CBODY)
    rect(g, 3, 9, 6, 20, CBODY)
    rect(g, 3, 9, 4, 20, CBODY_LT)
    # right arm
    rect(g, 22, 16, 31, 21, CBODY)
    rect(g, 28, 7, 31, 18, CBODY)
    rect(g, 29, 7, 31, 18, CBODY_DK)
    # --- ribs down the trunk ---
    for rx in (15, 17, 19):
        rect(g, rx, 6, rx, 38, CRIB)
    # --- big fanged maw carved into the trunk ---
    rect(g, 13, 21, 21, 32, BMOUTH)
    rect(g, 13, 29, 21, 32, BMOUTH_DK)
    for (x, y) in [(15, 24), (17, 26), (19, 24)]:
        px(g, x, y, "#d46a80")
    # interlocking teeth top + bottom rims
    for tx in range(13, 21, 2):
        rect(g, tx, 21, tx, 22, BTOOTH)
        rect(g, tx + 1, 31, tx + 1, 32, BTOOTH)
    # --- menacing eyes on the upper trunk ---
    rect(g, 13, 11, 16, 14, BEYEC)
    rect(g, 18, 11, 21, 14, BEYEC)
    px(g, 14, 12, BEYE_DK)
    px(g, 19, 12, BEYE_DK)
    rect(g, 13, 10, 16, 10, CBODY_DK)  # angry brows
    rect(g, 18, 10, 21, 10, CBODY_DK)
    # --- spines across the body ---
    for (x, y) in [(12, 8), (22, 9), (14, 17), (20, 18), (12, 35), (22, 35),
                   (5, 12), (30, 11), (7, 20), (24, 18)]:
        px(g, x, y, BSP)
    # --- flower crowns on the arm tips + head ---
    for (x, y) in [(4, 8), (29, 6), (16, 1), (18, 1)]:
        px(g, x, y, BFLOWER)
    px(g, 17, 1, "#ffd23f")
    return g

def all_white(src):
    g = [row[:] for row in src]
    for row in g:
        for x in range(len(row)):
            if row[x] is not None:
                row[x] = "#ffffff"
    return g

boss = boss_cactus()
render(boss, "boss-cactus.svg", scale=3, outline="#123010")
render(all_white(boss), "boss-cactus-flash.svg", scale=3, outline="#123010")

# ---- boss seed volley projectile (spiky green pod) ----
g = new_grid(5, 5)
rect(g, 0, 0, 4, 4, CBODY_DK)
rect(g, 1, 1, 3, 3, CBODY_LT)
px(g, 2, 2, BSP)
render(g, "cactus-seed.svg", scale=2)

# ---- spinning tumble-burr (desert SPINNER enemy, new in level 2). Roughly radial so it
# reads while continuously rotating. ----
BURR = "#b58a4a"
BURR_DK = "#8a6633"
BURR_LT = "#d9b877"
BSPK = "#efe6c0"
g = new_grid(16, 16)
rect(g, 5, 5, 10, 10, BURR)
rect(g, 4, 6, 11, 9, BURR)
rect(g, 6, 4, 9, 11, BURR)
rect(g, 5, 5, 7, 7, BURR_LT)
rect(g, 8, 8, 10, 10, BURR_DK)
for (x, y) in [(7, 0), (8, 0), (7, 15), (8, 15), (0, 7), (0, 8), (15, 7), (15, 8),
               (2, 2), (13, 2), (2, 13), (13, 13)]:
    px(g, x, y, BSPK)  # radial spikes
for (x, y) in [(7, 2), (8, 13), (2, 7), (13, 8), (3, 3), (12, 12)]:
    px(g, x, y, BURR_DK)
render(g, "spin-burr.svg", scale=2, outline="#5a3a1a")

# ---- boss spike-burst needle: bright & high-contrast so the radial volley reads clearly
# against the sand (the small brown enemy needle would camouflage) ----
g = new_grid(9, 4)
rect(g, 0, 1, 6, 2, "#ffd23f")     # golden shaft
rect(g, 1, 1, 4, 1, "#fff3b0")     # bright top highlight
rect(g, 6, 1, 8, 2, "#ffffff")     # white-hot tip
px(g, 6, 0, "#ffe066")             # barbs
px(g, 6, 3, "#ffe066")
render(g, "boss-spike.svg", scale=2, outline="#5a3a00")

# ---- boss heavy orb: a spiked ball of desert energy (gold core, green shell) ----
CORE = "#fff6d0"
MID = "#c7d24a"
OUTER = "#5f7a2a"
SPIKE = "#ffe066"
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
render(g, "cactus-orb.svg", scale=2, outline="#2a3410")
