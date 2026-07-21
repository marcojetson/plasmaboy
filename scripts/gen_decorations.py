from pixelart import new_grid, rect, px, render

# ---- cloud ----
g = new_grid(20, 10)
rect(g, 3, 4, 16, 8, "#ffffff")
rect(g, 5, 2, 13, 4, "#ffffff")
rect(g, 1, 5, 4, 7, "#ffffff")
rect(g, 15, 5, 18, 7, "#ffffff")
rect(g, 6, 5, 13, 6, "#eaf6ff")
render(g, "cloud.svg", scale=3, outline=None)

# ---- background tree (big, two variants for variety) ----
def bg_tree(trunk_w, canopy_color, canopy_color_dk):
    g = new_grid(24, 34)
    rect(g, 10, 20, 13, 33, "#5c3a21")
    rect(g, 10, 20, 11, 33, "#432712")
    # canopy - layered rounded blobs
    rect(g, 2, 6, 21, 22, canopy_color)
    rect(g, 5, 2, 18, 7, canopy_color)
    rect(g, 0, 12, 23, 20, canopy_color)
    rect(g, 2, 18, 21, 23, canopy_color_dk)
    px(g, 4, 10, canopy_color_dk)
    px(g, 18, 9, canopy_color_dk)
    px(g, 8, 15, canopy_color_dk)
    return g

render(bg_tree(4, "#2d6a4f", "#1b4332"), "bg-tree-0.svg", scale=3, outline="#0d2818")
render(bg_tree(4, "#3a7a5a", "#255440"), "bg-tree-1.svg", scale=3, outline="#0d2818")

# ---- foreground decorative bush (not an enemy!) ----
g = new_grid(12, 8)
rect(g, 1, 2, 10, 7, "#40916c")
rect(g, 3, 0, 8, 2, "#40916c")
rect(g, 1, 5, 10, 7, "#2d6a4f")
px(g, 3, 3, "#95d5b2")
px(g, 8, 4, "#95d5b2")
render(g, "bush.svg", scale=2)

# ---- grass tuft ----
g = new_grid(10, 6)
for x in (1, 3, 5, 7, 8):
    px(g, x, 5, "#40916c")
    px(g, x, 4, "#52b788")
px(g, 2, 3, "#74c69d")
px(g, 6, 3, "#74c69d")
render(g, "grass-tuft.svg", scale=2, outline=None)

# ---- decorative daisy flower (different from the pink hidden-flower collectible) ----
g = new_grid(8, 9)
rect(g, 1, 5, 6, 8, "#2d6a4f")
rect(g, 3, 0, 4, 1, "#ffffff")
rect(g, 0, 3, 1, 4, "#ffffff")
rect(g, 6, 3, 7, 4, "#ffffff")
rect(g, 3, 6, 4, 7, "#ffffff")
px(g, 3, 3, "#ffd700")
px(g, 4, 3, "#ffd700")
render(g, "daisy.svg", scale=2)

# ---- checkpoint flag (tinted gray until reached, then gold) ----
g = new_grid(12, 22)
rect(g, 1, 0, 2, 21, "#6b5a3a")   # wooden pole
rect(g, 1, 0, 1, 21, "#4a3d26")   # pole shade
rect(g, 3, 1, 10, 7, "#ffd54f")   # banner
rect(g, 3, 1, 10, 2, "#fff0a8")   # banner highlight
rect(g, 3, 6, 10, 7, "#e0a800")   # banner shade
# swallowtail notch on the flying edge
px(g, 10, 3, "#ffd54f")
px(g, 9, 4, "#e0a800")
px(g, 10, 5, "#ffd54f")
# little star on the banner
px(g, 6, 4, "#ffffff")
px(g, 5, 4, "#ffffff")
px(g, 7, 4, "#ffffff")
render(g, "checkpoint-flag.svg", scale=2)

# ---- heart icon (HUD) ----
g = new_grid(9, 8)
rect(g, 1, 1, 3, 2, "#ff5c7a")
rect(g, 5, 1, 7, 2, "#ff5c7a")
rect(g, 0, 2, 8, 4, "#ff5c7a")
rect(g, 1, 5, 7, 5, "#ff5c7a")
rect(g, 2, 6, 6, 6, "#ff5c7a")
rect(g, 3, 7, 5, 7, "#ff5c7a")
px(g, 2, 2, "#ffb3c1")
px(g, 2, 3, "#ffb3c1")
render(g, "heart-icon.svg", scale=2)
