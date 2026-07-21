from pixelart import new_grid, rect, px, render

STEM = "#2d6a4f"
BUD = "#6a1b6f"
BUD_DK = "#4a1250"
PETAL = "#b5179e"
PETAL_DK = "#7a0f6b"
SPORE = "#e0aaff"
EYE = "#ffe066"

# closed bud
g = new_grid(12, 12)
rect(g, 3, 6, 8, 11, STEM)
rect(g, 2, 2, 9, 7, BUD)
rect(g, 3, 1, 8, 2, BUD)
rect(g, 2, 6, 9, 7, BUD_DK)
render(g, "poison-flower-closed.svg", scale=2)

# open, spore-spewing
g = new_grid(16, 16)
rect(g, 5, 10, 10, 15, STEM)
# petals splayed open
rect(g, 1, 3, 14, 9, PETAL)
rect(g, 3, 1, 12, 3, PETAL)
rect(g, 1, 8, 14, 9, PETAL_DK)
px(g, 0, 5, PETAL_DK)
px(g, 15, 5, PETAL_DK)
# inner mouth + eyes
rect(g, 5, 4, 10, 8, BUD_DK)
px(g, 6, 5, EYE)
px(g, 9, 5, EYE)
px(g, 7, 7, SPORE)
px(g, 8, 7, SPORE)
render(g, "poison-flower-open.svg", scale=2)
