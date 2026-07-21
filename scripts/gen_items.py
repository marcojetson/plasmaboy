from pixelart import new_grid, rect, px, render

# ---- ground tile ----
g = new_grid(16, 16)
rect(g, 0, 0, 15, 2, "#5fae3e")
rect(g, 0, 0, 15, 0, "#7ed957")
rect(g, 0, 3, 15, 15, "#8a5a2b")
rect(g, 0, 3, 15, 4, "#6b4423")
px(g, 3, 5, "#734a24")
px(g, 11, 8, "#734a24")
px(g, 6, 11, "#734a24")
render(g, "tile-ground.svg", scale=2, outline=None)

# ---- pit tile ----
g = new_grid(16, 16)
rect(g, 0, 0, 15, 15, "#0a0508")
rect(g, 1, 1, 14, 14, "#1a0f14")
render(g, "tile-pit.svg", scale=2, outline=None)

# ---- health pickup: a heart (matches the heart in the HUD) ----
# 2px margin all around so the 1px cartoon outline isn't clipped on the sides/bottom.
HEART = "#ff4d6d"
HEART_DK = "#c92a48"
HEART_LT = "#ff9db0"
ox, oy = 2, 2
g = new_grid(17, 16)
rect(g, ox + 1, oy + 1, ox + 4, oy + 3, HEART)     # left lobe
rect(g, ox + 8, oy + 1, ox + 11, oy + 3, HEART)    # right lobe
rect(g, ox + 0, oy + 3, ox + 12, oy + 6, HEART)    # wide body
rect(g, ox + 1, oy + 7, ox + 11, oy + 7, HEART)
rect(g, ox + 2, oy + 8, ox + 10, oy + 8, HEART)
rect(g, ox + 3, oy + 9, ox + 9, oy + 9, HEART)
rect(g, ox + 4, oy + 10, ox + 8, oy + 10, HEART)
rect(g, ox + 5, oy + 11, ox + 7, oy + 11, HEART)
rect(g, ox + 0, oy + 6, ox + 12, oy + 6, HEART_DK)  # lower shading
rect(g, ox + 2, oy + 8, ox + 10, oy + 9, HEART_DK)
rect(g, ox + 2, oy + 1, ox + 3, oy + 2, HEART_LT)   # shine on left lobe
px(g, ox + 1, oy + 3, HEART_LT)
render(g, "energy-orb.svg", scale=2)

# ---- shoulder-cannon capsule: a mini version of the actual weapon ----
ORANGE = "#ff6d00"
ORANGE_DK = "#c94f00"
ORANGE_LT = "#ffa040"
STEEL = "#9aa4b0"
STEEL_DK = "#5a6472"
GLOW = "#3ee6e6"
g = new_grid(16, 11)
rect(g, 0, 2, 7, 9, ORANGE)          # housing
rect(g, 0, 2, 7, 3, ORANGE_LT)
rect(g, 0, 8, 7, 9, ORANGE_DK)
rect(g, 7, 3, 13, 8, STEEL)          # barrel
rect(g, 7, 3, 13, 3, "#c0c8d0")
rect(g, 7, 8, 13, 8, STEEL_DK)
rect(g, 10, 3, 10, 8, STEEL_DK)      # barrel band
rect(g, 13, 4, 14, 7, GLOW)          # glowing muzzle
render(g, "capsule-shoulder.svg", scale=2)

# ---- katana capsule: a mini version of the actual sword ----
BLADE = "#e0e0e0"
BLADE_LT = "#ffffff"
GUARD = "#ffd23f"
HANDLE = "#7a1f1f"
g = new_grid(16, 16)
for i in range(10):                  # diagonal blade, bottom-left -> top-right
    x = 4 + i
    y = 11 - i
    rect(g, x, y, x + 1, y, BLADE)
    px(g, x, y, BLADE_LT)
px(g, 3, 12, GUARD)                  # tsuba (guard)
px(g, 4, 12, GUARD)
px(g, 3, 13, GUARD)
rect(g, 1, 13, 3, 15, HANDLE)        # wrapped handle
px(g, 1, 14, "#a83030")
render(g, "capsule-katana.svg", scale=2)

# ---- score item (gold gem) ----
g = new_grid(7, 7)
rect(g, 2, 0, 4, 0, "#fff3b0")
rect(g, 1, 1, 5, 3, "#ffd700")
rect(g, 2, 4, 4, 5, "#e0a800")
px(g, 3, 2, "#fff3b0")
render(g, "score-item.svg", scale=2)

# ---- hidden flower ----
g = new_grid(8, 8)
rect(g, 3, 0, 4, 1, "#ff9ecf")
rect(g, 0, 3, 1, 4, "#ff9ecf")
rect(g, 6, 3, 7, 4, "#ff9ecf")
rect(g, 3, 6, 4, 7, "#ff9ecf")
rect(g, 3, 3, 4, 4, "#fff3b0")
render(g, "hidden-flower.svg", scale=2)

# ---- plasma bolt ----
g = new_grid(6, 4)
rect(g, 0, 1, 5, 2, "#00e5ff")
rect(g, 1, 1, 3, 1, "#c8feff")
render(g, "plasma-bolt.svg", scale=2)

# ---- shoulder cannon shell (big, obviously heavier than a plasma bolt) ----
g = new_grid(16, 12)
rect(g, 1, 2, 13, 9, "#ff6d00")
rect(g, 3, 3, 9, 5, "#ffd54f")      # hot core
rect(g, 2, 3, 12, 4, "#ffa040")     # highlight
rect(g, 1, 8, 13, 9, "#c94f00")     # shadow underside
# pointed nose + trailing flame
rect(g, 13, 4, 15, 7, "#ffd54f")
rect(g, 0, 4, 1, 7, "#ffed99")
px(g, 6, 6, "#fff3b0")
render(g, "shoulder-shell.svg", scale=2)

# ---- explosion burst ----
g = new_grid(16, 16)
rect(g, 5, 5, 10, 10, "#ffffff")
rect(g, 3, 3, 12, 12, "#ffd54f")
rect(g, 1, 6, 14, 9, "#ffab40")
rect(g, 6, 1, 9, 14, "#ffab40")
render(g, "shoulder-explosion.svg", scale=4, outline=None)

# ---- muzzle flash ----
g = new_grid(5, 5)
rect(g, 1, 1, 3, 3, "#ffffff")
px(g, 2, 0, "#ffe066")
px(g, 2, 4, "#ffe066")
px(g, 0, 2, "#ffe066")
px(g, 4, 2, "#ffe066")
render(g, "muzzle-flash.svg", scale=2, outline=None)

# ---- enemy spike ----
g = new_grid(5, 3)
rect(g, 0, 1, 4, 1, "#2d6a4f")
px(g, 4, 0, "#40916c")
px(g, 4, 2, "#40916c")
render(g, "enemy-spike.svg", scale=2)

# ---- enemy seed ----
g = new_grid(4, 4)
rect(g, 0, 0, 3, 3, "#ffd23f")
px(g, 1, 1, "#fff3b0")
render(g, "enemy-seed.svg", scale=2)

# ---- enemy spore ----
g = new_grid(4, 4)
rect(g, 0, 0, 3, 3, "#b5179e")
px(g, 1, 1, "#e0aaff")
render(g, "enemy-spore.svg", scale=2)

# ---- boss seed ----
g = new_grid(5, 5)
rect(g, 0, 0, 4, 4, "#40916c")
rect(g, 1, 1, 3, 3, "#95d5b2")
render(g, "boss-seed.svg", scale=2)

# ---- katana slash streak: a long tapered energy crescent, white-hot core with a cyan
# edge and trailing motion lines, so the "10x" swing reads as a dramatic beam ----
W = 80
g = new_grid(W, 14)
for x in range(W):
    # thickness bulges in the middle third and tapers to points at both ends
    t = (x / (W - 1))
    bulge = 1.0 - abs(t - 0.55) * 2.0
    bulge = max(0.0, bulge)
    half = int(round(bulge * 6))
    if half <= 0:
        continue
    cy = 7
    # cyan outer edge
    rect(g, x, cy - half, x, cy + half, "#3ee6ff")
    # white-hot core
    if half >= 2:
        rect(g, x, cy - half + 1, x, cy + half - 1, "#ffffff")
# trailing motion streaks behind the leading edge
for (sx, sy) in [(6, 4), (12, 3), (10, 11), (16, 10)]:
    rect(g, sx, sy, sx + 8, sy, "#a8f0ff")
render(g, "katana-slash.svg", scale=4, outline=None)

# ---- katana swing flash: a bright burst at the blade origin when the slash launches ----
g = new_grid(14, 14)
rect(g, 5, 0, 8, 13, "#ffffff")
rect(g, 0, 5, 13, 8, "#ffffff")
rect(g, 3, 3, 10, 10, "#eaffff")
rect(g, 5, 5, 8, 8, "#3ee6ff")
render(g, "katana-flash.svg", scale=3, outline=None)

# ---- extra life: a golden winged heart (distinct from the red health heart) ----
GOLD = "#ffd54f"
GOLD_DK = "#e0a000"
GOLD_LT = "#fff3b0"
WING = "#ffffff"
WING_DK = "#cfe0f5"
ox = 6
g = new_grid(20, 14)
# wings behind the heart
rect(g, 1, 3, 4, 4, WING)
rect(g, 0, 4, 3, 6, WING)
rect(g, 0, 5, 4, 5, WING_DK)
rect(g, 15, 3, 18, 4, WING)
rect(g, 16, 4, 19, 6, WING)
rect(g, 15, 5, 19, 5, WING_DK)
# golden heart
rect(g, ox + 1, 2, ox + 3, 3, GOLD)     # left lobe
rect(g, ox + 5, 2, ox + 7, 3, GOLD)     # right lobe
rect(g, ox + 0, 3, ox + 8, 6, GOLD)     # wide body
rect(g, ox + 1, 7, ox + 7, 7, GOLD)
rect(g, ox + 2, 8, ox + 6, 8, GOLD)
rect(g, ox + 3, 9, ox + 5, 9, GOLD)
rect(g, ox + 4, 10, ox + 4, 10, GOLD)
rect(g, ox + 0, 6, ox + 8, 6, GOLD_DK)  # lower shading
rect(g, ox + 2, 8, ox + 6, 9, GOLD_DK)
px(g, ox + 2, 3, GOLD_LT)               # shine
px(g, ox + 1, 3, GOLD_LT)
render(g, "extra-life.svg", scale=2)
