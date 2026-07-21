from pixelart import new_grid, rect, px, render

W, H = 16, 22

# Palette
HAIR = "#ffd54f"
HAIR_DK = "#e0a800"
SKIN = "#ffcc99"
SKIN_DK = "#e0a373"
EYE = "#1a1a2e"
SCARF = "#ff6f3c"
PURPLE = "#8a5cf6"
PURPLE_DK = "#6a3ce0"
BELT = "#3a2a5c"
BOOT = "#2b1f47"
GUN = "#b8c0cc"
GUN_DK = "#5a6472"
GUN_TIP = "#3ee6e6"


def draw_head_and_torso(g):
    # hair
    rect(g, 3, 0, 11, 1, HAIR)
    px(g, 2, 1, HAIR_DK)
    px(g, 12, 1, HAIR_DK)
    rect(g, 2, 2, 12, 2, HAIR)
    px(g, 1, 2, HAIR_DK)
    px(g, 13, 2, HAIR_DK)
    # spiky tips
    px(g, 4, 0, HAIR_DK)
    px(g, 7, 0, HAIR_DK)
    px(g, 10, 0, HAIR_DK)

    # face
    rect(g, 3, 3, 12, 7, SKIN)
    rect(g, 3, 3, 4, 4, HAIR)  # hair over forehead sides
    rect(g, 11, 3, 12, 4, HAIR)
    px(g, 3, 7, SKIN_DK)
    px(g, 12, 7, SKIN_DK)
    # eyes
    px(g, 7, 5, EYE)
    px(g, 10, 5, EYE)
    # small mouth
    px(g, 9, 7, SKIN_DK)

    # scarf / collar
    rect(g, 4, 8, 11, 8, SCARF)
    px(g, 3, 9, SCARF)

    # torso
    rect(g, 4, 9, 11, 15, PURPLE)
    rect(g, 4, 9, 5, 15, PURPLE_DK)
    rect(g, 10, 9, 11, 15, PURPLE_DK)

    # back arm (left, resting)
    rect(g, 1, 10, 3, 13, PURPLE_DK)
    rect(g, 1, 13, 2, 14, SKIN)

    # gun arm (right, forward)
    rect(g, 11, 10, 13, 12, PURPLE)
    rect(g, 12, 10, 15, 12, GUN)
    rect(g, 14, 10, 15, 12, GUN_DK)
    px(g, 15, 11, GUN_TIP)

    # belt
    rect(g, 4, 15, 11, 16, BELT)


def legs_idle(g):
    rect(g, 5, 17, 6, 19, PURPLE)
    rect(g, 9, 17, 10, 19, PURPLE)
    rect(g, 5, 20, 7, 21, BOOT)
    rect(g, 8, 20, 10, 21, BOOT)


def legs_walk_a(g):
    # left leg forward/up, right leg back/extended
    rect(g, 4, 16, 6, 18, PURPLE)
    rect(g, 3, 19, 6, 20, BOOT)
    rect(g, 9, 17, 10, 21, PURPLE)
    rect(g, 9, 20, 11, 21, BOOT)


def legs_walk_b(g):
    rect(g, 9, 16, 11, 18, PURPLE)
    rect(g, 9, 19, 12, 20, BOOT)
    rect(g, 5, 17, 6, 21, PURPLE)
    rect(g, 4, 20, 6, 21, BOOT)


def legs_run_a(g):
    rect(g, 3, 17, 6, 18, PURPLE)
    rect(g, 2, 19, 5, 20, BOOT)
    rect(g, 9, 17, 11, 21, PURPLE)
    rect(g, 10, 20, 12, 21, BOOT)


def legs_run_b(g):
    rect(g, 9, 17, 12, 18, PURPLE)
    rect(g, 10, 19, 13, 20, BOOT)
    rect(g, 4, 17, 6, 21, PURPLE)
    rect(g, 3, 20, 5, 21, BOOT)


def legs_jump(g):
    rect(g, 4, 17, 6, 19, PURPLE)
    rect(g, 4, 19, 6, 20, BOOT)
    rect(g, 9, 17, 11, 19, PURPLE)
    rect(g, 9, 19, 11, 20, BOOT)


def legs_fall(g):
    rect(g, 3, 17, 5, 20, PURPLE)
    rect(g, 2, 20, 5, 21, BOOT)
    rect(g, 10, 17, 12, 20, PURPLE)
    rect(g, 10, 20, 13, 21, BOOT)


FRAMES = {
    "player-idle-0.svg": legs_idle,
    "player-idle-1.svg": legs_idle,
    "player-walk-0.svg": legs_walk_a,
    "player-walk-1.svg": legs_walk_b,
    "player-run-0.svg": legs_run_a,
    "player-run-1.svg": legs_run_b,
    "player-jump-0.svg": legs_jump,
    "player-fall-0.svg": legs_fall,
}

for filename, leg_fn in FRAMES.items():
    g = new_grid(W, H)
    draw_head_and_torso(g)
    leg_fn(g)
    render(g, filename, scale=2)
