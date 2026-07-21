from pixelart import new_grid, rect, px, render

DIRT = "#5c4326"
DIRT_DK = "#3a2a18"
BODY = "#6b8f3f"
BODY_DK = "#4a6b2a"
BELLY = "#9fc26b"
EYE = "#1a1a2e"
MOUTH = "#7a1f1f"

# mound (burrowed)
g = new_grid(15, 6)
rect(g, 2, 3, 12, 5, DIRT)
rect(g, 4, 2, 10, 3, DIRT)
rect(g, 2, 5, 12, 5, DIRT_DK)
render(g, "vine-worm-mound.svg", scale=2)

# emerging (rising up, mouth open wide)
g = new_grid(12, 15)
rect(g, 3, 4, 8, 14, BODY)
rect(g, 4, 4, 7, 14, BELLY)
rect(g, 3, 12, 8, 14, BODY_DK)
px(g, 4, 6, EYE)
px(g, 7, 6, EYE)
rect(g, 4, 8, 7, 9, MOUTH)
render(g, "vine-worm-emerge.svg", scale=2)

# charging (leaning forward, low + long)
g = new_grid(13, 13)
rect(g, 1, 5, 11, 11, BODY)
rect(g, 1, 5, 11, 7, BELLY)
rect(g, 1, 10, 11, 11, BODY_DK)
px(g, 9, 5, EYE)
px(g, 9, 8, EYE)
rect(g, 10, 6, 12, 8, MOUTH)
render(g, "vine-worm-charge.svg", scale=2)
