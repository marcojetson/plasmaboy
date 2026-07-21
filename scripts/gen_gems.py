"""Gem sprite for the sublevel collectible (src/collectibles/GemItem.ts).

ONE grayscale faceted jewel, reused by every biome and recolored at runtime via Phaser's
setTint(GEM_TINTS[theme]). Because tint MULTIPLIES the texture RGB, the art is authored in
grayscale: the white table becomes the full saturated biome color, mid-gray facets become
richer shades, and the dark facet lines/outline stay dark. The result reads as a cut,
sparkling gemstone in whatever color the biome assigns — a plain flat shape would tint into a
flat blob instead.

Brilliant-cut proportions: a flat table on top, a short crown widening to the girdle (widest
row), then a longer pavilion tapering to a point. A top-left light source lifts the left
facets and shades the right; etched facet lines + a white glint sell the "cut jewel" look.
"""
from pixelart import new_grid, rect, px, render

# Vertical shade ramp (top = bright table, bottom = deep pavilion). Kept mostly light/mid so
# the tint reads vivid rather than muddy; only the point + facet lines go genuinely dark.
TABLE = "#ffffff"
RAMP = {
    0: "#ffffff", 1: "#ffffff",
    2: "#efefef", 3: "#e0e0e0", 4: "#cfcfcf", 5: "#bfbfbf",
    6: "#b2b2b2",                                   # girdle (widest)
    7: "#9f9f9f", 8: "#929292", 9: "#848484", 10: "#787878",
    11: "#6b6b6b", 12: "#5f5f5f", 13: "#545454", 14: "#4a4a4a",
}
# Per-row horizontal extent [x0, x1] — the hexagonal gem silhouette. cx ~= 8.5 on an 18-wide grid.
SPAN = {
    0: (6, 11), 1: (5, 12), 2: (4, 13), 3: (3, 14), 4: (2, 15), 5: (1, 16),
    6: (0, 17),
    7: (1, 16), 8: (2, 15), 9: (3, 14), 10: (4, 13), 11: (5, 12), 12: (6, 11),
    13: (7, 10), 14: (8, 9),
}
LINE = "#3c3c3c"   # etched facet dividers (lighter than the outline, darker than the facets)
W, H = 18, 15


def shade(hexcol, mul):
    v = int(hexcol[1:3], 16)
    v = max(0, min(255, int(v * mul)))
    return f"#{v:02x}{v:02x}{v:02x}"


def line(g, x0, y0, x1, y1, color):
    """Bresenham line — used for the straight facet dividers."""
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    x, y = x0, y0
    while True:
        px(g, x, y, color)
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x += sx
        if e2 <= dx:
            err += dx
            y += sy


def build():
    g = new_grid(W, H)
    # 1) fill each row with its ramp shade, then round the body: lift the left third toward the
    #    light and deepen the right third into shadow.
    for y in range(H):
        x0, x1 = SPAN[y]
        base = RAMP[y]
        rect(g, x0, y, x1, y, base)
        width = x1 - x0 + 1
        third = max(1, width // 3)
        rect(g, x0, y, x0 + third - 1, y, shade(base, 1.12))          # sunlit left facets
        rect(g, x1 - third + 1, y, x1, y, shade(base, 0.82))          # shaded right facets

    # 2) table: a crisp bright top facet with a divider line under it.
    rect(g, 5, 0, 12, 1, TABLE)
    line(g, 5, 2, 12, 2, LINE)

    # 3) crown facet dividers — table corners down to the girdle corners.
    line(g, 5, 2, 0, 6, LINE)
    line(g, 12, 2, 17, 6, LINE)
    line(g, 8, 2, 8, 2, LINE)

    # 4) pavilion facet dividers — girdle corners converging to the point, plus a center ridge.
    line(g, 0, 6, 8, 14, LINE)
    line(g, 17, 6, 9, 14, LINE)
    line(g, 8, 3, 8, 13, shade("#808080", 0.6))                      # faint center ridge
    line(g, 4, 6, 7, 14, LINE)
    line(g, 13, 6, 10, 14, LINE)

    # 5) glints: a pure-white sparkle cross on the left crown + a small twinkle on the table.
    for (sx, sy) in [(3, 3), (2, 3), (4, 3), (3, 2), (3, 4)]:
        px(g, sx, sy, "#ffffff")
    px(g, 7, 1, "#ffffff")
    px(g, 10, 4, "#f4f4f4")
    return g


render(build(), "gem.svg", scale=2, outline="#20202c")
print("gem done")
