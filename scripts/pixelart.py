"""Tiny pixel-art -> SVG renderer used to hand-author Plasma Boy's sprite set.

Each sprite is built on a small integer grid using rect-fill helpers (rather than
hand-typed ASCII art, which is error prone), then rendered as a grid of <rect>
elements sized `scale` SVG units per pixel. A cheap outline pass (dilate the
silhouette by 1px, drawn first in a dark color) gives every sprite a clean
cartoon border for free.
"""
import os

# Sprites live under src/ (not public/) so Vite inlines them into the bundle — this is what
# lets the production build be a single self-contained HTML file with no external asset fetches.
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "src", "sprites")
os.makedirs(OUT_DIR, exist_ok=True)


def new_grid(w, h):
    return [[None for _ in range(w)] for _ in range(h)]


def rect(grid, x0, y0, x1, y1, color):
    """Inclusive rect fill."""
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if 0 <= y < len(grid) and 0 <= x < len(grid[0]):
                grid[y][x] = color


def px(grid, x, y, color):
    if 0 <= y < len(grid) and 0 <= x < len(grid[0]):
        grid[y][x] = color


def render(grid, path, scale=3, outline="#14141f"):
    h = len(grid)
    w = len(grid[0])
    cells = []

    if outline:
        dilated = set()
        for y in range(h):
            for x in range(w):
                if grid[y][x] is not None:
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < w and 0 <= ny < h and grid[ny][nx] is None:
                            dilated.add((nx, ny))
        for (x, y) in dilated:
            cells.append((x, y, outline))

    for y in range(h):
        for x in range(w):
            if grid[y][x] is not None:
                cells.append((x, y, grid[y][x]))

    rects = "".join(
        f'<rect x="{x*scale}" y="{y*scale}" width="{scale}" height="{scale}" fill="{color}"/>'
        for x, y, color in cells
    )
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {w*scale} {h*scale}" width="{w*scale}" height="{h*scale}">{rects}</svg>'
    )
    with open(os.path.join(OUT_DIR, path), "w") as f:
        f.write(svg)
    print(f"wrote {path} ({w*scale}x{h*scale})")
