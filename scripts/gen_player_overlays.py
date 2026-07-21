from pixelart import new_grid, rect, px, render

# Shoulder cannon mount — a big, prominent cannon that clamps over the shoulder with a
# thick forward-pointing barrel and a glowing muzzle. Drawn pointing right; flips with facing.
ORANGE = "#ff6d00"
ORANGE_DK = "#c94f00"
ORANGE_LT = "#ffa040"
STEEL = "#9aa4b0"
STEEL_DK = "#5a6472"
GLOW = "#3ee6e6"

g = new_grid(20, 15)
# shoulder clamp / housing (the bulky body sitting on the shoulder)
rect(g, 0, 3, 10, 13, ORANGE)
rect(g, 0, 3, 10, 4, ORANGE_LT)
rect(g, 0, 11, 10, 13, ORANGE_DK)
rect(g, 1, 1, 8, 3, ORANGE_DK)
# rivets / detail on the housing
px(g, 2, 6, ORANGE_DK)
px(g, 8, 6, ORANGE_DK)
px(g, 5, 9, ORANGE_LT)
# thick steel barrel jutting forward
rect(g, 9, 5, 18, 11, STEEL)
rect(g, 9, 5, 18, 6, "#c0c8d0")
rect(g, 9, 10, 18, 11, STEEL_DK)
# barrel bands
rect(g, 12, 5, 12, 11, STEEL_DK)
rect(g, 15, 5, 15, 11, STEEL_DK)
# glowing muzzle
rect(g, 18, 6, 19, 10, GLOW)
px(g, 19, 7, "#c8feff")
render(g, "player-shoulder-cannon.svg", scale=2)

# Katana sheathed diagonally across the back.
g = new_grid(6, 16)
for i in range(12):
    px(g, i // 2, 14 - i, "#e0e0e0")
    px(g, i // 2 + 1, 14 - i, "#e0e0e0")
px(g, 0, 15, "#3a2410")
px(g, 1, 15, "#3a2410")
px(g, 5, 2, "#d6453c")
px(g, 5, 1, "#d6453c")
render(g, "player-katana.svg", scale=2)
