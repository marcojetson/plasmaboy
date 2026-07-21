"""Two extra playable characters, drawn on the SAME 16x22 grid as plasmaboy (see gen_player.py)
with the identical arm-cannon position (right arm rows 10-12, gun at x12-15) and leg/belt rows,
so the shared weapon overlays and physics body stay aligned — only the look changes.

  * plasma-ranger — purple Power-Ranger suit: helmet + black visor, white accents + boots.
  * plant-girl    — light-brown long hair, green leafy dress (inspired by the author's daughter).

Emits <id>-idle-0/1 and <id>-walk-0/1 for each (idle frames identical/static, like plasmaboy).
"""
from pixelart import new_grid, rect, px, render

W, H = 16, 22

# ---- shared bits -------------------------------------------------------------------------
GUN = "#b8c0cc"
GUN_DK = "#5a6472"
GUN_TIP = "#3ee6e6"


def gun_arm(g, sleeve, sleeve_dk):
    # right arm forward holding the plasma cannon (same coords as plasmaboy)
    rect(g, 11, 10, 13, 12, sleeve)
    rect(g, 12, 10, 15, 12, GUN)
    rect(g, 14, 10, 15, 12, GUN_DK)
    px(g, 15, 11, GUN_TIP)
    px(g, 11, 12, sleeve_dk)


def legs(g, frame, legc, bootc):
    """frame: 'idle' | 'a' | 'b' — plasmaboy's leg geometry, recolored per character."""
    if frame == 'idle':
        rect(g, 5, 17, 6, 19, legc); rect(g, 9, 17, 10, 19, legc)
        rect(g, 5, 20, 7, 21, bootc); rect(g, 8, 20, 10, 21, bootc)
    elif frame == 'a':
        rect(g, 4, 16, 6, 18, legc); rect(g, 3, 19, 6, 20, bootc)
        rect(g, 9, 17, 10, 21, legc); rect(g, 9, 20, 11, 21, bootc)
    else:  # 'b'
        rect(g, 9, 16, 11, 18, legc); rect(g, 9, 19, 12, 20, bootc)
        rect(g, 5, 17, 6, 21, legc); rect(g, 4, 20, 6, 21, bootc)


def emit(prefix, head_torso, legc, bootc):
    for name, frame in [('idle-0', 'idle'), ('idle-1', 'idle'), ('walk-0', 'a'), ('walk-1', 'b')]:
        g = new_grid(W, H)
        head_torso(g)
        legs(g, frame, legc, bootc)
        render(g, f"{prefix}-{name}.svg", scale=2)


# =========================================================================================
# PLASMA RANGER
# =========================================================================================
R_SUIT = "#8a5cf6"
R_SUIT_DK = "#6a3ce0"
R_WHITE = "#f0f0f5"
R_WHITE_DK = "#c8c8d4"
R_VISOR = "#14141f"
R_VISOR_LT = "#3ee6e6"
R_GOLD = "#ffd23f"


def ranger_head_torso(g):
    # helmet dome
    rect(g, 3, 0, 12, 2, R_SUIT)
    px(g, 2, 1, R_SUIT_DK); px(g, 13, 1, R_SUIT_DK)
    px(g, 2, 2, R_SUIT_DK); px(g, 13, 2, R_SUIT_DK)
    # white crest down the centre of the helmet
    px(g, 7, 0, R_WHITE); px(g, 8, 0, R_WHITE_DK)
    # helmet face-plate
    rect(g, 2, 3, 13, 7, R_SUIT)
    rect(g, 2, 3, 2, 7, R_SUIT_DK); rect(g, 13, 3, 13, 7, R_SUIT_DK)
    # black visor band with cyan glints
    rect(g, 3, 4, 12, 6, R_VISOR)
    px(g, 4, 4, R_VISOR_LT); px(g, 10, 5, R_VISOR_LT)
    # white mouth grille
    rect(g, 5, 7, 10, 7, R_WHITE_DK)
    px(g, 6, 7, R_VISOR); px(g, 8, 7, R_VISOR); px(g, 9, 7, R_VISOR)
    # white collar
    rect(g, 4, 8, 11, 8, R_WHITE)
    # torso suit
    rect(g, 4, 9, 11, 15, R_SUIT)
    rect(g, 4, 9, 5, 15, R_SUIT_DK); rect(g, 10, 9, 11, 15, R_SUIT_DK)
    # white chest diamond emblem
    px(g, 7, 10, R_WHITE); px(g, 8, 10, R_WHITE)
    rect(g, 6, 11, 9, 11, R_WHITE)
    px(g, 7, 12, R_WHITE); px(g, 8, 12, R_WHITE)
    # back arm (white glove)
    rect(g, 1, 10, 3, 13, R_SUIT_DK)
    rect(g, 1, 13, 2, 14, R_WHITE)
    # gun arm
    gun_arm(g, R_SUIT, R_SUIT_DK)
    # white belt with gold buckle
    rect(g, 4, 15, 11, 16, R_WHITE)
    px(g, 7, 15, R_GOLD); px(g, 8, 15, R_GOLD)


emit('ranger', ranger_head_torso, R_SUIT, R_WHITE)  # white boots


# =========================================================================================
# PLANT GIRL — taller feel via long flowing hair + a longer dress
# =========================================================================================
G_HAIR = "#c9a06a"
G_HAIR_DK = "#a97e4a"
G_HAIR_LT = "#e0bd88"
G_SKIN = "#ffcc99"
G_SKIN_DK = "#e0a373"
G_EYE = "#3a2a1a"
G_CHEEK = "#ffb0a0"
G_DRESS = "#5fae4a"
G_DRESS_DK = "#3f8f3a"
G_DRESS_LT = "#7ed957"
G_FLOWER = "#ff9ecf"
G_FLOWER_C = "#fff3b0"
G_SHOE = "#6b4a2a"


def plantgirl_head_torso(g):
    # hair crown
    rect(g, 3, 0, 11, 1, G_HAIR)
    rect(g, 2, 2, 12, 2, G_HAIR)
    px(g, 5, 0, G_HAIR_LT); px(g, 9, 0, G_HAIR_LT)
    # long hair falling down both sides past the shoulders
    rect(g, 1, 3, 2, 14, G_HAIR); px(g, 1, 3, G_HAIR_DK)
    for yy in range(6, 15, 2):
        px(g, 1, yy, G_HAIR_DK)
    rect(g, 12, 3, 13, 14, G_HAIR); px(g, 13, 3, G_HAIR_DK)
    for yy in range(6, 15, 2):
        px(g, 13, yy, G_HAIR_DK)
    # face
    rect(g, 3, 3, 11, 7, G_SKIN)
    px(g, 3, 3, G_HAIR); px(g, 11, 3, G_HAIR)   # hair over forehead corners
    px(g, 3, 7, G_SKIN_DK); px(g, 11, 7, G_SKIN_DK)
    px(g, 6, 5, G_EYE); px(g, 9, 5, G_EYE)       # brown eyes
    px(g, 4, 6, G_CHEEK); px(g, 10, 6, G_CHEEK)  # rosy cheeks
    px(g, 7, 7, G_SKIN_DK); px(g, 8, 7, G_SKIN_DK)  # small smile
    # little flower tucked in the hair
    px(g, 3, 1, G_FLOWER); px(g, 4, 0, G_FLOWER); px(g, 4, 2, G_FLOWER)
    px(g, 4, 1, G_FLOWER_C)
    # green leafy collar
    rect(g, 4, 8, 11, 8, G_DRESS_LT)
    # dress bodice
    rect(g, 4, 9, 11, 14, G_DRESS)
    rect(g, 4, 9, 5, 14, G_DRESS_DK); rect(g, 10, 9, 11, 14, G_DRESS_DK)
    # leaf motif on the chest
    px(g, 7, 11, G_DRESS_LT); px(g, 8, 12, G_DRESS_LT); px(g, 7, 12, G_DRESS_LT)
    # back arm (skin hand peeking past the hair)
    rect(g, 2, 10, 3, 13, G_DRESS_DK)
    px(g, 2, 13, G_SKIN)
    # gun arm (green sleeve)
    gun_arm(g, G_DRESS, G_DRESS_DK)
    # flared skirt
    rect(g, 3, 15, 12, 16, G_DRESS)
    rect(g, 3, 16, 12, 16, G_DRESS_DK)
    px(g, 3, 15, G_DRESS_LT); px(g, 12, 15, G_DRESS_DK)


emit('plantgirl', plantgirl_head_torso, G_SKIN, G_SHOE)  # bare legs + brown shoes

print("characters done")
