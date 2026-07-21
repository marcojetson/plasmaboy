from pixelart import new_grid, rect, px, render

# ============================================================
#  FOREST — mossy green forest floor, earth underneath
# ============================================================

# top tile: mostly green moss/grass with dark earth peeking through
g = new_grid(16, 16)
rect(g, 0, 0, 15, 15, "#3a7a2e")  # base green
rect(g, 0, 0, 15, 0, "#4a9a3e")  # lighter top edge

# mossy variation — darker green patches
for (x, y) in [(1, 2), (2, 2), (5, 4), (6, 4), (9, 1), (10, 1),
               (13, 3), (14, 3), (3, 8), (4, 8), (11, 7), (12, 7),
               (7, 11), (8, 11), (1, 14), (2, 14), (14, 12), (15, 12)]:
    px(g, x, y, "#2d5e22")

# brighter moss highlights
for (x, y) in [(0, 1), (4, 3), (8, 0), (12, 2), (6, 9), (10, 10),
               (2, 12), (15, 6), (7, 5), (13, 9)]:
    px(g, x, y, "#5cb84a")

# tiny earth pebbles showing through
for (x, y) in [(3, 6), (11, 5), (8, 13), (14, 8), (1, 10)]:
    px(g, x, y, "#6b4a2a")

# small dark root/stone specks
for (x, y) in [(5, 7), (12, 11), (9, 14), (0, 5)]:
    px(g, x, y, "#1f4a18")

render(g, "tile-ground.svg", scale=2, outline=None)

# sub tile: darker earth-green, no bright top edge
g = new_grid(16, 16)
rect(g, 0, 0, 15, 15, "#2f6424")
rect(g, 0, 0, 15, 0, "#245018")  # dark seam

for (x, y) in [(2, 3), (3, 3), (9, 5), (10, 6), (6, 9), (7, 9),
               (4, 12), (12, 13), (13, 2), (1, 8)]:
    px(g, x, y, "#234a1a")
for (x, y) in [(5, 6), (12, 9), (7, 2), (2, 13), (14, 11)]:
    px(g, x, y, "#4a8a3a")
for (x, y) in [(3, 10), (11, 4), (8, 14)]:
    px(g, x, y, "#1a3a12")

render(g, "tile-dirt.svg", scale=2, outline=None)

# platform: mossy log
g = new_grid(16, 16)
rect(g, 0, 0, 15, 15, "#5a3a1e")
rect(g, 0, 0, 15, 1, "#4a2e14")

for y in (3, 4, 8, 9, 13, 14):
    rect(g, 0, y, 15, y, "#4e3218")
px(g, 5, 3, "#3a2410")
px(g, 10, 8, "#3a2410")
px(g, 3, 13, "#3a2410")

moss = [0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0]
for x, m in enumerate(moss):
    if m:
        px(g, x, 0, "#52b788")
        px(g, x, 1, "#40916c")

render(g, "tile-platform.svg", scale=2, outline=None)

# ============================================================
#  DESERT — warm sand tones (mostly fine as-is, slight refresh)
# ============================================================

g = new_grid(16, 16)
rect(g, 0, 0, 15, 15, "#e6c07a")

# sand grain variation
for (x, y) in [(1, 1), (5, 3), (9, 0), (13, 2), (3, 7), (11, 5),
               (7, 10), (15, 8), (0, 12), (6, 14), (10, 13), (14, 11)]:
    px(g, x, y, "#f2d79a")
for (x, y) in [(2, 4), (8, 2), (12, 6), (4, 11), (10, 9), (6, 15),
               (14, 1), (0, 8)]:
    px(g, x, y, "#d4ad60")

# tiny darker specks (pebbles)
for (x, y) in [(3, 5), (11, 3), (7, 12), (13, 9), (1, 14)]:
    px(g, x, y, "#b89040")

render(g, "tile-sand.svg", scale=2, outline=None)

g = new_grid(16, 16)
rect(g, 0, 0, 15, 15, "#d4ad60")
rect(g, 0, 0, 15, 0, "#c49a50")

for (x, y) in [(2, 3), (9, 5), (6, 9), (12, 11), (4, 7), (14, 2)]:
    px(g, x, y, "#e6c07a")
for (x, y) in [(5, 6), (11, 8), (3, 12), (8, 14), (13, 4)]:
    px(g, x, y, "#b89040")

render(g, "tile-sand-sub.svg", scale=2, outline=None)

g = new_grid(16, 16)
rect(g, 0, 0, 15, 15, "#c8a05a")
rect(g, 0, 0, 15, 0, "#b08840")

for y in (4, 5, 10, 11):
    rect(g, 0, y, 15, y, "#b89048")
for (x, y) in [(3, 2), (10, 7), (6, 13), (14, 3)]:
    px(g, x, y, "#a07830")

render(g, "tile-sandstone.svg", scale=2, outline=None)

# ============================================================
#  WATER — blue ocean floor
# ============================================================

g = new_grid(16, 16)
rect(g, 0, 0, 15, 15, "#2060a0")  # solid blue base

# lighter water ripples
for (x, y) in [(1, 1), (5, 3), (9, 0), (13, 2), (3, 7), (11, 5),
               (7, 10), (15, 8), (0, 12), (6, 14), (10, 13)]:
    px(g, x, y, "#3080c0")
for (x, y) in [(2, 4), (8, 2), (12, 6), (4, 11), (10, 9), (6, 15)]:
    px(g, x, y, "#1850a0")

# darker deep-water specks
for (x, y) in [(3, 5), (11, 3), (7, 12), (13, 9), (1, 14)]:
    px(g, x, y, "#1040a0")

render(g, "tile-seabed.svg", scale=2, outline=None)

g = new_grid(16, 16)
rect(g, 0, 0, 15, 15, "#1850a0")
rect(g, 0, 0, 15, 0, "#1040a0")

for (x, y) in [(2, 3), (9, 5), (6, 9), (12, 11), (4, 7)]:
    px(g, x, y, "#2060a0")
for (x, y) in [(5, 6), (11, 8), (3, 12), (8, 14)]:
    px(g, x, y, "#1040a0")

render(g, "tile-seabed-sub.svg", scale=2, outline=None)

g = new_grid(16, 16)
rect(g, 0, 0, 15, 15, "#1a4a8a")
rect(g, 0, 0, 15, 0, "#1440a0")

for y in (4, 5, 10, 11):
    rect(g, 0, y, 15, y, "#1848a0")
for (x, y) in [(3, 2), (10, 7), (6, 13), (14, 3)]:
    px(g, x, y, "#103a80")

render(g, "tile-coral-rock.svg", scale=2, outline=None)

# ============================================================
#  CAVE — dark stone
# ============================================================

g = new_grid(16, 16)
rect(g, 0, 0, 15, 15, "#3a3a4a")

for (x, y) in [(1, 1), (5, 3), (9, 0), (13, 2), (3, 7), (11, 5),
               (7, 10), (15, 8), (0, 12), (6, 14)]:
    px(g, x, y, "#4a4a5a")
for (x, y) in [(2, 4), (8, 2), (12, 6), (4, 11), (10, 9)]:
    px(g, x, y, "#2a2a3a")

# crystal sparkles
for (x, y) in [(5, 1), (11, 7), (3, 13)]:
    px(g, x, y, "#6a6a8a")

render(g, "tile-cave.svg", scale=2, outline=None)

g = new_grid(16, 16)
rect(g, 0, 0, 15, 15, "#2a2a3a")
rect(g, 0, 0, 15, 0, "#222232")

for (x, y) in [(2, 3), (9, 5), (6, 9), (12, 11), (4, 7)]:
    px(g, x, y, "#3a3a4a")
for (x, y) in [(5, 6), (11, 8), (3, 12)]:
    px(g, x, y, "#1a1a2a")

render(g, "tile-cave-sub.svg", scale=2, outline=None)

g = new_grid(16, 16)
rect(g, 0, 0, 15, 15, "#4a4a5a")
rect(g, 0, 0, 15, 0, "#3a3a4a")

for y in (4, 5, 10, 11):
    rect(g, 0, y, 15, y, "#3e3e4e")
for (x, y) in [(3, 2), (10, 7), (6, 13)]:
    px(g, x, y, "#2a2a3a")

render(g, "tile-cave-rock.svg", scale=2, outline=None)

# ============================================================
#  SWAMP — dark muddy green
# ============================================================

g = new_grid(16, 16)
rect(g, 0, 0, 15, 15, "#4a5a2a")  # dark olive base

for (x, y) in [(1, 1), (5, 3), (9, 0), (13, 2), (3, 7), (11, 5),
               (7, 10), (15, 8), (0, 12), (6, 14)]:
    px(g, x, y, "#3a4a20")
for (x, y) in [(2, 4), (8, 2), (12, 6), (4, 11), (10, 9)]:
    px(g, x, y, "#5a6a3a")

# muddy spots
for (x, y) in [(3, 5), (11, 3), (7, 12), (13, 9), (1, 14)]:
    px(g, x, y, "#3a3a1a")

render(g, "tile-mud.svg", scale=2, outline=None)

g = new_grid(16, 16)
rect(g, 0, 0, 15, 15, "#3a4a20")
rect(g, 0, 0, 15, 0, "#2e3e18")

for (x, y) in [(2, 3), (9, 5), (6, 9), (12, 11), (4, 7)]:
    px(g, x, y, "#4a5a2a")
for (x, y) in [(5, 6), (11, 8), (3, 12)]:
    px(g, x, y, "#2a3a14")

render(g, "tile-mud-sub.svg", scale=2, outline=None)

g = new_grid(16, 16)
rect(g, 0, 0, 15, 15, "#5a4a2a")
rect(g, 0, 0, 15, 0, "#4a3a1e")

for y in (4, 5, 10, 11):
    rect(g, 0, y, 15, y, "#4e3e22")
for (x, y) in [(3, 2), (10, 7), (6, 13)]:
    px(g, x, y, "#3a2a14")

render(g, "tile-bog.svg", scale=2, outline=None)

# ============================================================
#  MUSEUM — greenhouse / light tile floor
# ============================================================

g = new_grid(16, 16)
rect(g, 0, 0, 15, 15, "#c8d8c0")  # pale sage green

for (x, y) in [(1, 1), (5, 3), (9, 0), (13, 2), (3, 7), (11, 5),
               (7, 10), (15, 8), (0, 12), (6, 14)]:
    px(g, x, y, "#d8e8d0")
for (x, y) in [(2, 4), (8, 2), (12, 6), (4, 11), (10, 9)]:
    px(g, x, y, "#b8c8b0")

# tile grout lines
for x in range(16):
    px(g, x, 7, "#a8b8a0")
    px(g, x, 15, "#a8b8a0")
for y in [0, 1, 2, 3, 4, 5, 6]:
    px(g, 7, y, "#a8b8a0")
    px(g, 15, y, "#a8b8a0")

render(g, "tile-greenhouse.svg", scale=2, outline=None)

g = new_grid(16, 16)
rect(g, 0, 0, 15, 15, "#b8c8b0")
rect(g, 0, 0, 15, 0, "#a8b8a0")

for (x, y) in [(2, 3), (9, 5), (6, 9), (12, 11), (4, 7)]:
    px(g, x, y, "#c8d8c0")
for (x, y) in [(5, 6), (11, 8), (3, 12)]:
    px(g, x, y, "#a8b8a0")

render(g, "tile-greenhouse-sub.svg", scale=2, outline=None)

g = new_grid(16, 16)
rect(g, 0, 0, 15, 15, "#8a7a5a")  # wooden planter
rect(g, 0, 0, 15, 0, "#7a6a4a")

for y in (4, 5, 10, 11):
    rect(g, 0, y, 15, y, "#7a6a4e")
for (x, y) in [(3, 2), (10, 7), (6, 13)]:
    px(g, x, y, "#6a5a3a")

render(g, "tile-planter.svg", scale=2, outline=None)
