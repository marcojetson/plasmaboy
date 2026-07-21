"""Underwater-theme sprite set for level 3 (see src/config/themes.ts 'water').

Same conventions as the other gen_*.py scripts. Enemy skins keep the shared archetype
silhouettes (walker / straight-shooter / aimer / burrow-charger / spore) so they drop into the
existing behavior classes unchanged — here reskinned as algae/sea creatures. Also generates the
seabed tiles, kelp/coral scenery, drifting bubbles, and the treasure-chest level goal.
"""
from pixelart import new_grid, rect, px, render

# ======================================================================================
# Palette
# ======================================================================================
WSAND = "#bdb894"       # cool wet seabed sand (grayer than desert)
WSAND_DK = "#9a9670"
WSAND_LT = "#d8d3b0"
GRAIN_D = "#87835f"
GRAIN_L = "#e6e2c0"

CROCK = "#c9806a"       # coral rock
CROCK_DK = "#a85f4a"
CROCK_LT = "#e0a088"

ALGAE = "#3fae7a"       # main algae green-teal
ALGAE_DK = "#2a7f5a"
ALGAE_LT = "#6fd6a0"
FROND = "#2f9e6a"
EYE = "#1a2a2e"

# ======================================================================================
# Tiles (scale 2, no outline)
# ======================================================================================
# seabed floor: filled edge-to-edge so things rest flush (matches the fixed desert sand fix)
g = new_grid(16, 16)
rect(g, 0, 0, 15, 15, WSAND)
rect(g, 0, 5, 15, 5, WSAND_DK)     # soft seam low in the body
for x in (1, 4, 5, 9, 12, 13):
    px(g, x, 0, WSAND_LT)          # sparse pale grains along the crest (not a hard band)
for (x, y) in [(3, 7), (9, 9), (12, 7), (6, 12), (2, 13), (14, 11)]:
    px(g, x, y, GRAIN_D)
for (x, y) in [(5, 10), (10, 13), (7, 6), (14, 8)]:
    px(g, x, y, GRAIN_L)
render(g, "tile-seabed.svg", scale=2, outline=None)

# sub-sand
g = new_grid(16, 16)
rect(g, 0, 0, 15, 15, WSAND)
rect(g, 0, 0, 15, 0, WSAND_DK)
for (x, y) in [(2, 3), (9, 5), (6, 9), (12, 12), (3, 13), (14, 7), (1, 9)]:
    px(g, x, y, GRAIN_D)
for (x, y) in [(5, 6), (11, 3), (8, 11), (13, 14)]:
    px(g, x, y, GRAIN_L)
render(g, "tile-seabed-sub.svg", scale=2, outline=None)

# coral-rock ledge
g = new_grid(16, 16)
rect(g, 0, 0, 15, 15, CROCK)
rect(g, 0, 0, 15, 1, CROCK_LT)     # sunlit top lip
for y in (4, 5, 9, 10, 14):
    rect(g, 0, y, 15, y, CROCK_DK) # coral strata
px(g, 4, 7, CROCK_DK)
px(g, 11, 12, CROCK_DK)
px(g, 8, 2, "#ffd0c0")             # coral polyp speck
render(g, "tile-coral-rock.svg", scale=2, outline=None)

# ======================================================================================
# Background scenery (scale 3, dark outline), origin bottom
# ======================================================================================
def kelp():
    g = new_grid(20, 34)
    SEA = "#2f9e6a"; SEA_DK = "#1f6f4a"; SEA_LT = "#5fd090"
    # two swaying fronds
    rect(g, 8, 2, 11, 33, SEA)
    rect(g, 8, 2, 9, 33, SEA_LT)
    rect(g, 4, 10, 7, 30, SEA)
    rect(g, 13, 6, 16, 28, SEA)
    rect(g, 13, 6, 14, 28, SEA_DK)
    # leafy nubs
    for y in (8, 14, 20, 26):
        px(g, 3, y, SEA_LT)
        px(g, 17, y - 2, SEA_LT)
    return g

render(kelp(), "kelp-bg.svg", scale=3, outline="#0d3826")

def coral_mound():
    g = new_grid(24, 34)
    CM = "#c9806a"; CM_DK = "#a85f4a"; CM_LT = "#e0a088"
    rect(g, 2, 16, 21, 33, CM)
    rect(g, 4, 12, 19, 17, CM)
    rect(g, 2, 16, 4, 33, CM_LT)
    rect(g, 18, 16, 21, 33, CM_DK)
    # coral branches on top
    for bx in (6, 11, 16):
        rect(g, bx, 8, bx + 1, 14, CM)
        px(g, bx, 8, CM_LT)
    for (x, y) in [(7, 22), (14, 25), (18, 20)]:
        px(g, x, y, "#ffd0c0")
    return g

render(coral_mound(), "coral-mound.svg", scale=3, outline="#5a3428")

# ======================================================================================
# Overhead ambiance: drifting bubble cluster (scale 3, no outline)
# ======================================================================================
g = new_grid(20, 12)
B = "#cdeeff"; BR = "#eafaff"
for (x, y, r) in [(5, 6, 3), (11, 4, 2), (14, 8, 2), (8, 9, 1), (16, 5, 1)]:
    rect(g, x - r, y - r, x + r, y + r, B)
    px(g, x - 1, y - 1, BR)  # highlight
render(g, "bubble-cluster.svg", scale=3, outline=None)

# ======================================================================================
# Ground decor (scale 2, outline)
# ======================================================================================
# branching coral
g = new_grid(12, 12)
C = "#ff8a6a"; C_DK = "#d4603f"; C_LT = "#ffb59a"
rect(g, 4, 6, 7, 11, C)
rect(g, 2, 4, 3, 9, C); rect(g, 8, 3, 9, 9, C)
rect(g, 5, 2, 6, 6, C)
rect(g, 4, 10, 7, 11, C_DK)
px(g, 2, 4, C_LT); px(g, 8, 3, C_LT); px(g, 5, 2, C_LT)
render(g, "coral.svg", scale=2)

# sea shell
g = new_grid(11, 9)
SH = "#ffd9a8"; SH_DK = "#d8a86a"; SH_LT = "#fff0d8"
rect(g, 2, 3, 8, 8, SH)
rect(g, 3, 1, 7, 3, SH)
rect(g, 2, 7, 8, 8, SH_DK)
for x in (3, 5, 7):
    rect(g, x, 2, x, 8, SH_DK)   # ridges
px(g, 5, 2, SH_LT)
render(g, "sea-shell.svg", scale=2)

# seaweed tuft
g = new_grid(10, 10)
S = "#2f9e6a"; S_LT = "#5fd090"
for x in (2, 4, 6, 8):
    rect(g, x, 3, x, 9, S)
    px(g, x, 3, S_LT)
px(g, 3, 5, S_LT); px(g, 7, 4, S_LT)
render(g, "seaweed-tuft.svg", scale=2, outline=None)

# sea rock
g = new_grid(12, 8)
R = "#7f8a90"; R_DK = "#5c666c"; R_LT = "#a4adb2"
rect(g, 1, 3, 10, 7, R)
rect(g, 2, 2, 8, 3, R_LT)
rect(g, 1, 6, 10, 7, R_DK)
px(g, 4, 4, R_LT); px(g, 8, 5, R_DK)
render(g, "sea-rock.svg", scale=2)

# ======================================================================================
# WALKER — drifting algae clump (2 frames), forest counterpart: WalkingMushroom
# ======================================================================================
PAD = 2
AW, AH = 14 + PAD * 2, 14

def algae_clump(sway):
    g = new_grid(AW, AH)
    o = PAD
    top = 3 - sway
    # blobby body
    rect(g, 2 + o, top + 2, 13 + o, 13, ALGAE)
    rect(g, 1 + o, 6, 14 + o, 11, ALGAE)
    rect(g, 1 + o, 6, 2 + o, 11, ALGAE_LT)
    rect(g, 13 + o, 6, 14 + o, 11, ALGAE_DK)
    rect(g, 2 + o, 12, 13 + o, 13, ALGAE_DK)
    # wavy fronds on top (sway between frames)
    for fx, base in ((4, top), (8, top - 1), (11, top)):
        rect(g, fx + o + sway, base, fx + o + sway, top + 2, FROND)
        px(g, fx + o + sway, base, ALGAE_LT)
    # blobs of light
    for (x, y) in [(5, 8), (10, 9), (7, 6)]:
        px(g, x + o, y, ALGAE_LT)
    # eyes
    px(g, 6 + o, 8, EYE)
    px(g, 9 + o, 8, EYE)
    return g

render(algae_clump(0), "algae-crawl-0.svg", scale=2)
render(algae_clump(1), "algae-crawl-1.svg", scale=2)

# ======================================================================================
# STRAIGHT SHOOTER — spiny urchin, forest counterpart: ThornBush
# ======================================================================================
URCH = "#4a7a72"
URCH_DK = "#33564f"
URCH_LT = "#6fa89e"
SPINE = "#d6f0e6"

def urchin(firing):
    g = new_grid(15, 15)
    # round body
    rect(g, 4, 4, 10, 11, URCH)
    rect(g, 3, 6, 11, 9, URCH)
    rect(g, 5, 3, 9, 4, URCH)
    rect(g, 4, 10, 10, 11, URCH_DK)
    rect(g, 4, 4, 5, 11, URCH_LT)
    # spines radiating out
    for (x, y) in [(7, 0), (7, 14), (0, 7), (14, 7), (2, 2), (12, 2), (2, 12), (12, 12)]:
        px(g, x, y, SPINE)
    for (x, y) in [(7, 1), (7, 13), (1, 7), (13, 7)]:
        px(g, x, y, SPINE)
    # eyes
    px(g, 6, 6, "#ffe066")
    px(g, 9, 6, "#ffe066")
    # mouth
    if firing:
        rect(g, 6, 8, 8, 9, "#ff6f8f")
    else:
        rect(g, 6, 8, 8, 8, "#20302e")
    return g

render(urchin(False), "urchin-idle.svg", scale=2)
render(urchin(True), "urchin-fire.svg", scale=2)

# algae spine projectile
g = new_grid(6, 3)
rect(g, 0, 1, 4, 1, URCH_DK)
px(g, 5, 0, SPINE); px(g, 5, 2, SPINE); px(g, 0, 1, SPINE)
render(g, "algae-spine.svg", scale=2)

# ======================================================================================
# AIMER — sea anemone (rotates to track), forest counterpart: AngrySunflower
# ======================================================================================
AN = "#5fc0a8"
AN_DK = "#3f9e86"
AN_TIP = "#ffd0e0"

def anemone(firing):
    g = new_grid(14, 14)
    # radial tentacle crown
    rect(g, 6, 0, 7, 13, AN)
    rect(g, 0, 6, 13, 7, AN)
    rect(g, 2, 2, 4, 4, AN)
    rect(g, 9, 2, 11, 4, AN)
    rect(g, 2, 9, 4, 11, AN)
    rect(g, 9, 9, 11, 11, AN)
    for (x, y) in [(6, 0), (7, 0), (0, 6), (0, 7), (13, 6), (13, 7), (6, 13), (7, 13),
                   (2, 2), (11, 2), (2, 11), (11, 11)]:
        px(g, x, y, AN_TIP)
    # mouth disc
    core = "#ff7f9f" if firing else "#3a6f66"
    rect(g, 4, 4, 9, 9, core)
    rect(g, 4, 8, 9, 9, AN_DK if not firing else "#ff5f88")
    px(g, 5, 6, "#1a2a2e")
    px(g, 8, 6, "#1a2a2e")
    return g

render(anemone(False), "anemone-idle.svg", scale=2)
render(anemone(True), "anemone-fire.svg", scale=2)

# anemone seed projectile (a stinging pod)
g = new_grid(4, 4)
rect(g, 0, 0, 3, 3, "#7fe0c8")
px(g, 1, 1, "#eafff8")
px(g, 2, 2, "#3f9e86")
render(g, "algae-seed.svg", scale=2)

# ======================================================================================
# BURROW-CHARGER — moray eel, forest counterpart: VineWorm
# ======================================================================================
SDIRT = "#9a9670"
SDIRT_DK = "#77745a"
EEL = "#5aa0b0"
EEL_DK = "#3a7684"
EEL_BELLY = "#bfe0e8"
EMOUTH = "#7a2f3f"

# mound (burrowed hole in the sand)
g = new_grid(15, 6)
rect(g, 2, 3, 12, 5, SDIRT)
rect(g, 4, 2, 10, 3, SDIRT)
rect(g, 2, 5, 12, 5, SDIRT_DK)
rect(g, 6, 3, 8, 5, "#3a4a4a")  # dark hole
render(g, "eel-mound.svg", scale=2)

# emerging (rising, mouth open)
g = new_grid(12, 15)
rect(g, 3, 4, 8, 14, EEL)
rect(g, 4, 4, 7, 14, EEL_BELLY)
rect(g, 3, 12, 8, 14, EEL_DK)
for sy in (7, 10, 13):
    rect(g, 3, sy, 8, sy, EEL_DK)
px(g, 4, 6, "#1a2a2e")
px(g, 7, 6, "#1a2a2e")
rect(g, 4, 8, 7, 9, EMOUTH)
render(g, "eel-emerge.svg", scale=2)

# charging (lunging forward)
g = new_grid(13, 13)
rect(g, 1, 5, 11, 11, EEL)
rect(g, 1, 5, 11, 7, EEL_BELLY)
rect(g, 1, 10, 11, 11, EEL_DK)
for sx in (4, 7):
    rect(g, sx, 5, sx, 11, EEL_DK)
px(g, 9, 5, "#1a2a2e")
px(g, 9, 8, "#1a2a2e")
rect(g, 10, 6, 12, 8, EMOUTH)
render(g, "eel-charge.svg", scale=2)

# ======================================================================================
# SPORE — algae spore bloom, forest counterpart: PoisonFlower
# ======================================================================================
BLOOM = "#4aae8a"
BLOOM_DK = "#2f7f62"
BLOOM_LT = "#7fd6b0"
DUST = "#d6fff0"

# closed bloom
g = new_grid(12, 12)
rect(g, 4, 7, 7, 11, "#2f7f5a")   # stalk
rect(g, 2, 2, 9, 8, BLOOM)
rect(g, 3, 1, 8, 2, BLOOM)
rect(g, 2, 2, 3, 8, BLOOM_LT)
rect(g, 8, 2, 9, 8, BLOOM_DK)
for (x, y) in [(5, 0), (1, 4), (10, 4)]:
    px(g, x, y, BLOOM_LT)
render(g, "bloom-closed.svg", scale=2)

# open bloom (spewing spore bubbles)
g = new_grid(16, 16)
rect(g, 6, 11, 9, 15, "#2f7f5a")   # stalk
rect(g, 2, 4, 13, 10, BLOOM)
rect(g, 3, 2, 12, 4, BLOOM)
rect(g, 2, 9, 13, 10, BLOOM_DK)
rect(g, 2, 4, 3, 10, BLOOM_LT)
rect(g, 5, 5, 10, 9, "#245c46")    # dark maw
px(g, 6, 6, "#ffe066"); px(g, 9, 6, "#ffe066")
for (x, y) in [(7, 7), (8, 8), (4, 3), (11, 3)]:
    px(g, x, y, DUST)
render(g, "bloom-open.svg", scale=2)

# spore bubble projectile
g = new_grid(4, 4)
rect(g, 0, 0, 3, 3, "#7fd6b0")
px(g, 1, 1, DUST)
render(g, "spore-bubble.svg", scale=2)

# ======================================================================================
# SPINNER — spinning urchin ball (water skin of the level-2 spinner). Radial so it reads
# while continuously rotating.
# ======================================================================================
URb = "#3f8f8a"
URb_DK = "#2a6f6a"
URb_LT = "#6fc0b8"
USPK = "#d6f0ea"
g = new_grid(16, 16)
rect(g, 5, 5, 10, 10, URb)
rect(g, 4, 6, 11, 9, URb)
rect(g, 6, 4, 9, 11, URb)
rect(g, 5, 5, 7, 7, URb_LT)
rect(g, 8, 8, 10, 10, URb_DK)
for (x, y) in [(7, 0), (8, 0), (7, 15), (8, 15), (0, 7), (0, 8), (15, 7), (15, 8),
               (2, 2), (13, 2), (2, 13), (13, 13)]:
    px(g, x, y, USPK)
for (x, y) in [(7, 2), (8, 13), (2, 7), (13, 8), (3, 3), (12, 12)]:
    px(g, x, y, URb_DK)
render(g, "spin-urchin.svg", scale=2, outline="#173f3a")

# ======================================================================================
# FLYER — darting fish (2-frame tail flap), NEW in level 3. Drawn facing LEFT (the Flyer
# flips it when heading right).
# ======================================================================================
FISH = "#4aae9a"
FISH_DK = "#2f8f7a"
FISH_LT = "#7fd6c0"
FIN = "#ffd23f"
FEYE = "#12242a"

def fish(tail_up):
    g = new_grid(18, 12)
    # body (front/mouth on the LEFT)
    rect(g, 4, 3, 14, 8, FISH)
    rect(g, 5, 2, 13, 3, FISH)
    rect(g, 5, 8, 13, 9, FISH)
    rect(g, 4, 3, 7, 8, FISH_LT)   # bright front
    rect(g, 11, 3, 14, 8, FISH_DK) # shaded back
    # tail on the RIGHT (flaps between frames)
    if tail_up:
        rect(g, 14, 2, 17, 5, FISH)
        rect(g, 15, 5, 17, 6, FISH_DK)
    else:
        rect(g, 14, 6, 17, 9, FISH)
        rect(g, 15, 5, 17, 6, FISH_DK)
    # top fin
    rect(g, 8, 1, 11, 2, FIN)
    # eye near the front, mouth at the tip
    px(g, 6, 5, FEYE)
    px(g, 3, 6, FISH_DK)
    return g

render(fish(True), "fish-0.svg", scale=2)
render(fish(False), "fish-1.svg", scale=2)

# ======================================================================================
# Small rising bubble (seabed ambiance)
# ======================================================================================
g = new_grid(8, 8)
B = "#cdeeff"
BR = "#ffffff"
rect(g, 2, 1, 5, 6, B)
rect(g, 1, 2, 6, 5, B)
px(g, 2, 2, BR)
px(g, 3, 2, BR)
render(g, "bubble.svg", scale=2, outline=None)

# ======================================================================================
# GOAL — sunken treasure chest (level-end marker; placeholder until a boss is designed)
# ======================================================================================
WOOD = "#8a5a2b"
WOOD_DK = "#5c3a1a"
WOOD_LT = "#b07c44"
GOLDM = "#c9a24a"
GOLD = "#ffd54f"
GOLD_LT = "#fff0a8"
g = new_grid(22, 18)
# chest base
rect(g, 2, 8, 19, 17, WOOD)
rect(g, 2, 8, 3, 17, WOOD_LT)
rect(g, 18, 8, 19, 17, WOOD_DK)
rect(g, 2, 16, 19, 17, WOOD_DK)
# metal bands + lock
rect(g, 5, 8, 6, 17, GOLDM)
rect(g, 15, 8, 16, 17, GOLDM)
rect(g, 9, 11, 12, 14, GOLDM)
px(g, 10, 12, WOOD_DK)
# open lid (arched, hinged back)
rect(g, 2, 3, 19, 7, WOOD)
rect(g, 3, 1, 18, 3, WOOD)
rect(g, 2, 3, 19, 4, WOOD_LT)
rect(g, 2, 6, 19, 7, GOLDM)
# spilling gold coins on top
for (x, y) in [(6, 5), (9, 4), (12, 5), (15, 4), (8, 6), (13, 6), (10, 6)]:
    px(g, x, y, GOLD)
px(g, 9, 4, GOLD_LT); px(g, 12, 5, GOLD_LT)
render(g, "goal-chest.svg", scale=3, outline="#2a1808")

# ======================================================================================
# BOSS — yellow tube sponge (Aplysina fistularis). A cluster of vertical yellow tubes with
# dark oscula (openings); the tallest central tube wears a face.
# ======================================================================================
SPO = "#ffcf3a"
SPO_DK = "#e0932a"
SPO_LT = "#ffe88a"
HOLE = "#8a5a1a"
HOLE_DK = "#4a2f08"
SEYE = "#1a1a2e"
SEYEW = "#ffffff"
SMAW = "#a01f3a"
SMAW_DK = "#6e1226"
STOOTH = "#fff2e0"

def _tube(g, x0, x1, top):
    bottom = 41
    rect(g, x0, top + 2, x1, bottom, SPO)
    rect(g, x0, top + 2, x0 + 1, bottom, SPO_LT)
    rect(g, x1 - 1, top + 2, x1, bottom, SPO_DK)
    rect(g, x0 + 1, top, x1 - 1, top + 1, SPO)          # rounded rim
    rect(g, x0 + 2, top + 1, x1 - 2, top + 3, HOLE)      # osculum
    rect(g, x0 + 2, top + 1, x1 - 2, top + 1, HOLE_DK)
    for k in range(top + 6, bottom - 1, 5):              # porous speckles
        px(g, x0 + 2, k, SPO_DK)
        px(g, x1 - 2, k + 2, HOLE_DK)

def build_sponge():
    g = new_grid(36, 44)
    # base clump
    rect(g, 3, 32, 32, 43, SPO)
    rect(g, 3, 32, 5, 43, SPO_LT)
    rect(g, 30, 32, 32, 43, SPO_DK)
    rect(g, 3, 42, 32, 43, SPO_DK)
    # tubes (back to front)
    _tube(g, 4, 11, 15)     # left
    _tube(g, 27, 34, 12)    # right
    _tube(g, 20, 27, 6)     # right-centre
    _tube(g, 12, 20, 3)     # central face tube (tallest)
    # face on the central tube
    rect(g, 13, 8, 19, 20, SPO)
    rect(g, 13, 8, 14, 20, SPO_LT)
    rect(g, 18, 8, 19, 20, SPO_DK)
    rect(g, 14, 10, 15, 12, SEYEW)
    px(g, 14, 11, SEYE)
    rect(g, 17, 10, 18, 12, SEYEW)
    px(g, 18, 11, SEYE)
    rect(g, 14, 9, 15, 9, SPO_DK)       # angry brows
    rect(g, 17, 9, 18, 9, SPO_DK)
    rect(g, 14, 15, 18, 19, SMAW)       # maw
    rect(g, 14, 18, 18, 19, SMAW_DK)
    for tx in (14, 16, 18):
        px(g, tx, 15, STOOTH)
    return g

def _whiten(src):
    g = [row[:] for row in src]
    for row in g:
        for x in range(len(row)):
            if row[x] is not None:
                row[x] = "#ffffff"
    return g

_sponge = build_sponge()
render(_sponge, "boss-sponge.svg", scale=3, outline="#5a3a08")
render(_whiten(_sponge), "boss-sponge-flash.svg", scale=3, outline="#5a3a08")

# seed volley (spore glob)
g = new_grid(5, 5)
rect(g, 0, 0, 4, 4, SPO_DK)
rect(g, 1, 1, 3, 3, SPO)
px(g, 2, 2, SPO_LT)
render(g, "sponge-spore.svg", scale=2)

# heavy orb (big bubble with a spore core)
_CORE = "#eaffff"
_MID = "#7fd0e0"
_OUT = "#2f8faa"
_SPK = "#ffe066"
g = new_grid(16, 16)
rect(g, 4, 1, 11, 14, _OUT)
rect(g, 1, 4, 14, 11, _OUT)
rect(g, 3, 3, 12, 12, _OUT)
rect(g, 5, 3, 10, 12, _MID)
rect(g, 3, 5, 12, 10, _MID)
rect(g, 6, 5, 9, 10, _CORE)
rect(g, 5, 6, 10, 9, _CORE)
for (x, y) in [(0, 7), (0, 8), (15, 7), (15, 8), (7, 0), (8, 0), (7, 15), (8, 15)]:
    px(g, x, y, _SPK)
render(g, "sponge-orb.svg", scale=2, outline="#123a44")

# spikeBurst jet (bright droplet flung radially)
g = new_grid(7, 7)
rect(g, 2, 0, 4, 6, SPO)
rect(g, 1, 2, 5, 4, SPO)
rect(g, 2, 1, 4, 3, SPO_LT)
px(g, 3, 5, SPO_DK)
render(g, "sponge-jet.svg", scale=2, outline="#5a3a08")
