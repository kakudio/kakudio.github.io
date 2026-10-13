"""Generate pixel-art SVG decoration for the Shell Game map rooms.

Each zone gets three pieces: a thin strip along the top of a room, a strip
along the bottom, and a scene for the bottom-right corner. Usage:
    python3 -I tools/zone-art.py assets/themes/spelunky/img/zones
"""
import math
import os
import random
import sys


class Canvas:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.px = {}

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h and c:
            self.px[(x, y)] = c

    def get(self, x, y):
        return self.px.get((x, y))

    def svg(self):
        out = []
        for y in range(self.h):
            x = 0
            while x < self.w:
                c = self.px.get((x, y))
                if not c:
                    x += 1
                    continue
                run = 1
                while self.px.get((x + run, y)) == c:
                    run += 1
                out.append(f'<rect x="{x}" y="{y}" width="{run}" height="1" fill="{c}"/>')
                x += run
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
                f'width="{self.w}" height="{self.h}" shape-rendering="crispEdges">'
                + "".join(out) + "</svg>\n")


def wrap(c, x):
    return x % c.w


# ---------------------------------------------------------------- jungle

def jungle_top(r):
    c = Canvas(64, 10)
    leaf = ["#1f3a17", "#2c4f1d", "#3b6a26"]
    for x in range(64):
        c.set(x, 0, leaf[0])
        if r.random() < 0.7:
            c.set(x, 1, leaf[r.randrange(2)])
    x = 0
    while x < 64:
        x += r.randint(5, 11)
        length = r.randint(3, 9)
        for y in range(1, length):
            c.set(wrap(c, x), y, "#28471b")
            if r.random() < 0.35:
                side = r.choice((-1, 1))
                c.set(wrap(c, x + side), y, leaf[2])
        c.set(wrap(c, x), length, leaf[2])
        c.set(wrap(c, x - 1), length - 1, leaf[1])
        c.set(wrap(c, x + 1), length - 1, leaf[1])
    return c


def jungle_bottom(r):
    c = Canvas(64, 10)
    greens = ["#24411a", "#2f5520", "#3f6f2a", "#55893a"]
    for x in range(64):
        c.set(x, 9, "#1a1208")
        c.set(x, 8, "#21170b" if r.random() < 0.6 else "#24411a")
        c.set(x, 7, greens[r.randrange(2)])
    x = 0
    while x < 64:
        x += r.randint(2, 5)
        height = r.randint(2, 6)
        lean = r.choice((-1, 0, 1))
        for i in range(height):
            c.set(wrap(c, x + (lean if i > height // 2 else 0)), 6 - i, greens[min(3, 1 + i // 2)])
    return c


def jungle_corner(r):
    c = Canvas(32, 32)
    dark, mid, light, vein = "#24411a", "#2f5a20", "#3f7329", "#1a3012"
    # Fronds rising from the bottom-right corner, each a curved leaf.
    for ang, length, col in ((200, 26, mid), (225, 30, light), (250, 24, mid), (175, 20, dark), (270, 18, dark)):
        a = math.radians(ang)
        for t in range(length * 3):
            s = t / (length * 3)
            bend = 0.35 * s * s
            x = 31 + math.cos(a + bend) * s * length
            y = 31 + math.sin(a + bend) * s * length
            width = math.sin(math.pi * s) * 3.2
            nx, ny = -math.sin(a + bend), math.cos(a + bend)
            for w in range(-int(width), int(width) + 1):
                c.set(round(x + nx * w), round(y + ny * w), col)
            c.set(round(x), round(y), vein)
    return c


# ---------------------------------------------------------------- volcana

def volcana_top(r):
    c = Canvas(64, 8)
    rock = ["#2a1009", "#341409", "#3f190b"]
    for x in range(64):
        depth = 2 + (1 if r.random() < 0.5 else 0) + (2 if r.random() < 0.12 else 0)
        for y in range(depth):
            c.set(x, y, rock[r.randrange(3)])
    for _ in range(5):
        x, y = r.randrange(64), 0
        for _ in range(r.randint(3, 6)):
            c.set(x, y, "#c2451c")
            x = wrap(c, x + r.choice((-1, 0, 1)))
            y = min(c.h - 1, y + r.choice((0, 1)))
            if c.get(x, y) is None:
                break
    for _ in range(4):
        x = r.randrange(64)
        c.set(x, 4, "#ff8a3c")
        c.set(x, 5, "#c2451c")
    return c


def volcana_bottom(r):
    c = Canvas(64, 12)
    for x in range(64):
        surface = 6 + round(math.sin(x / 64 * math.tau * 3) * 1.2)
        for y in range(surface, 12):
            c.set(x, y, "#ff9b3d" if y == surface else ("#e2621f" if y < surface + 3 else "#a8331a"))
        if r.random() < 0.18:
            c.set(x, surface - 1, "#ffcf6a")
    for _ in range(6):
        x = r.randrange(64)
        c.set(x, 9, "#ffcf6a")
        c.set(wrap(c, x + 1), 9, "#ff9b3d")
    for _ in range(5):
        x, y = r.randrange(64), r.randint(0, 3)
        c.set(x, y, "#ff8a3c")
    return c


def volcana_corner(r):
    c = Canvas(32, 32)
    # A rock with glowing cracks, and a small flame on top.
    cx, cy, rx, ry = 22, 27, 11, 8
    for y in range(32):
        for x in range(32):
            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1:
                c.set(x, y, "#3a170b" if (x + y) % 5 else "#2c1008")
    x, y = 14, 26
    for _ in range(22):
        if c.get(x, y):
            c.set(x, y, "#e2621f")
        x += r.choice((1, 1, 0))
        y += r.choice((-1, 0, 1))
    # Rock highlight along the top edge.
    for x in range(32):
        for y in range(32):
            if c.get(x, y) and not c.get(x, y - 1):
                c.set(x, y, "#5a2a12")
    # A teardrop flame: outer, middle and core layers, leaning a little.
    top, base, cxf, maxw = 4, 22, 22, 6.5
    for layer, scale, col in ((0, 1.0, "#c2451c"), (1, 0.66, "#ff8a3c"), (2, 0.34, "#ffcf6a")):
        for y in range(top + layer * 3, base + 1):
            t = (y - top) / (base - top)
            w = maxw * scale * (t ** 0.7)
            if t > 0.72:
                w *= max(0.0, 1 - ((t - 0.72) / 0.32) ** 2)
            centre = cxf + math.sin(t * 3.2) * 1.2 * (1 - t)
            for x in range(round(centre - w), round(centre + w) + 1):
                c.set(x, y, col)
    for x, y in ((18, 6), (26, 3), (20, 2)):
        c.set(x, y, "#ff8a3c")
    return c


# ---------------------------------------------------------------- ice caves

def ice_top(r):
    c = Canvas(64, 10)
    for x in range(64):
        c.set(x, 0, "#9fd4ec")
        c.set(x, 1, "#6ea9c6" if r.random() < 0.8 else "#9fd4ec")
    x = 0
    while x < 64:
        x += r.randint(3, 7)
        length = r.randint(2, 9)
        for y in range(2, 2 + length):
            width = max(0, round((1 - (y - 2) / length) * 1.4))
            for dx in range(-width, width + 1):
                c.set(wrap(c, x + dx), y, "#bfe6f7" if dx == -width else "#7fb7d3")
    return c


def ice_bottom(r):
    c = Canvas(64, 10)
    for x in range(64):
        top = 4 + round(math.sin(x / 64 * math.tau * 2) * 1.5 + math.sin(x / 64 * math.tau * 5) * 0.6)
        for y in range(top, 10):
            c.set(x, y, "#e6f6ff" if y == top else ("#b8dcef" if y < top + 2 else "#7fa9c2"))
    for _ in range(8):
        c.set(r.randrange(64), r.randint(0, 2), "#e6f6ff")
    return c


def ice_corner(r):
    c = Canvas(32, 32)
    # A cluster of crystals growing from the corner.
    for base_x, height, half in ((27, 24, 3), (21, 17, 2), (31, 14, 2), (16, 10, 2), (24, 9, 1)):
        top = 31 - height
        for y in range(top, 32):
            if y < top + half:
                w = y - top
            else:
                w = half
            for x in range(base_x - w, base_x + w + 1):
                if x < base_x:
                    col = "#d6f1ff"
                elif x == base_x:
                    col = "#a8d8ef"
                else:
                    col = "#6fa6c4"
                c.set(x, y, col)
    for _ in range(6):
        c.set(r.randrange(4, 30), r.randrange(2, 16), "#e6f6ff")
    return c



# ---------------------------------------------------------------- shared shapes

def ellipse(c, cx, cy, rx, ry, col):
    for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
        for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1:
                c.set(x, y, col)


def drips(c, r, band, drip, tip, spacing=(4, 9), length=(2, 7), top=0):
    """A band along the top edge with drips hanging from it."""
    for x in range(c.w):
        for y in range(top, top + 2):
            c.set(x, y, band[(x + y) % len(band)] if r.random() < 0.85 else band[0])
    x = 0
    while x < c.w:
        x += r.randint(*spacing)
        n = r.randint(*length)
        for y in range(top + 2, top + 2 + n):
            c.set(wrap(c, x), y, drip)
        c.set(wrap(c, x), top + 2 + n, tip)


def ground(c, r, colors, waves=((3, 1.2),), base=None, speck=None, specks=0):
    """Wavy ground along the bottom edge, in bands of colour."""
    base = c.h // 2 if base is None else base
    for x in range(c.w):
        top = base + round(sum(math.sin(x / c.w * math.tau * k) * a for k, a in waves))
        for y in range(top, c.h):
            c.set(x, y, colors[min(len(colors) - 1, y - top)])
    for _ in range(specks):
        x = r.randrange(c.w)
        for y in range(c.h):
            if c.get(x, y):
                c.set(x, y + r.randint(1, 3), speck)
                break


# ---------------------------------------------------------------- dwelling

def dwelling_top(r):
    c = Canvas(64, 10)
    dirt = ["#3a2412", "#452b16", "#322010"]
    for x in range(64):
        for y in range(2 + (1 if r.random() < 0.4 else 0)):
            c.set(x, y, dirt[r.randrange(3)])
    x = 0
    while x < 64:
        x += r.randint(6, 13)
        y, cx = 2, x
        for _ in range(r.randint(3, 8)):
            c.set(wrap(c, cx), y, "#6b4a2a")
            y += 1
            cx += r.choice((-1, 0, 0, 1))
    return c


def dwelling_bottom(r):
    c = Canvas(64, 10)
    ground(c, r, ["#6b4424", "#553519", "#452b16", "#3a2412"], waves=((2, 0.8), (5, 0.4)), base=5)
    for _ in range(4):
        x = r.randrange(64)
        for dx in range(3):
            c.set(wrap(c, x + dx), 4, "#8a8072")
            c.set(wrap(c, x + dx), 3, "#a8a090" if dx == 1 else None)
    for _ in range(3):
        x = r.randrange(64)
        c.set(x, 7, "#e8dcc0")
        c.set(wrap(c, x + 1), 7, "#e8dcc0")
        c.set(wrap(c, x + 2), 7, "#cbbf9f")
    return c


def dwelling_corner(r):
    c = Canvas(32, 32)
    # A clay pot on a little mound.
    ellipse(c, 22, 31, 12, 4, "#3a2412")
    for y in range(13, 30):
        t = (y - 13) / 16
        w = 4 + math.sin(math.pi * min(1, t * 1.15)) * 5
        for x in range(round(22 - w), round(22 + w) + 1):
            shade = "#a8582c" if x < 22 - w * 0.4 else ("#8a4422" if x < 22 + w * 0.5 else "#6b331a")
            c.set(x, y, shade)
    for x in range(18, 27):
        c.set(x, 12, "#6b331a")
        c.set(x, 11, "#a8582c")
    for x in range(16, 29):
        if c.get(x, 19):
            c.set(x, 19, "#c9a24a")
    return c


# ---------------------------------------------------------------- olmec

def olmec_top(r):
    c = Canvas(64, 8)
    for x in range(64):
        for y in range(4):
            edge = x % 16 == 0 or y == 3
            c.set(x, y, "#2a2a20" if edge else ("#5a5a46" if (x // 16 + y) % 2 else "#4c4c3c"))
    x = 0
    while x < 64:
        x += r.randint(3, 8)
        for y in range(4, 4 + r.randint(1, 4)):
            c.set(wrap(c, x), y, "#4f7a32")
    return c


def olmec_bottom(r):
    c = Canvas(64, 10)
    for x in range(64):
        for y in range(4, 10):
            edge = (x + (8 if y > 6 else 0)) % 16 == 0 or y in (4, 7)
            c.set(x, y, "#2a2a20" if edge else ("#5f5f4a" if y < 7 else "#4c4c3c"))
    for _ in range(10):
        c.set(r.randrange(64), 4, "#5d8a3a")
    return c


def olmec_corner(r):
    c = Canvas(32, 32)
    # A carved stone head: brow, eyes, broad nose, lips.
    stone, dark, light = "#6a6a52", "#3a3a2c", "#8a8a6c"
    for y in range(6, 32):
        for x in range(10, 32):
            dx, dy = (x - 21) / 11, (y - 18) / 13
            if dx * dx + dy * dy <= 1 or y > 24:
                c.set(x, y, stone)
    for x in range(12, 31):
        c.set(x, 9, light)
        c.set(x, 13, dark)
    for ex in (15, 25):
        for x in range(ex - 2, ex + 3):
            c.set(x, 15, dark)
        c.set(ex, 15, "#2a2a20")
    for y in range(16, 22):
        for x in range(19, 24 + (1 if y > 19 else 0)):
            c.set(x, y, light if x == 19 else stone)
    for x in range(17, 26):
        c.set(x, 24, dark)
        c.set(x, 25, "#7a5a46")
    return c


# ---------------------------------------------------------------- tide pool

def tide_top(r):
    c = Canvas(64, 10)
    # Curved roof tiles along the top, like the pagodas.
    for x in range(64):
        c.set(x, 0, "#1f4a4a")
        c.set(x, 1, "#2f6a66")
        c.set(x, 2, "#2f6a66" if x % 8 not in (0, 7) else "#1f4a4a")
        if x % 8 in (0, 7):
            c.set(x, 3, "#3f8a82")
    for x in range(3, 64, 16):
        for y in range(4, 4 + r.randint(2, 5)):
            c.set(x, y, "#6fd6d0")
    return c


def tide_bottom(r):
    c = Canvas(64, 12)
    ground(c, r, ["#9fe6e0", "#4fb0b0", "#2f8a8e", "#1f6a74", "#174f5a"], waves=((4, 1.0), (9, 0.4)), base=5)
    for x in range(64):
        if (x // 3) % 7 == 0:
            c.set(x, 9, "#6fd6d0")
    return c


def tide_corner(r):
    c = Canvas(32, 32)
    # Coral stalks with branches reaching up, and a shell on the sea floor.
    for base_x, height, col, tip in ((17, 15, "#e86a6a", "#ffb0a0"), (23, 22, "#ff8a6a", "#ffc0a0"), (29, 12, "#d0507a", "#ff9fb4")):
        for y in range(31 - height, 31):
            c.set(base_x, y, col)
            c.set(base_x + 1, y, col)
        for i, y in enumerate(range(31 - height + 3, 29, 3)):
            side = -1 if i % 2 else 1
            for k in range(1, 4):
                x = base_x + (1 if side > 0 else 0) + side * k
                c.set(x, y - k, col)
            c.set(base_x + (1 if side > 0 else 0) + side * 3, y - 4, tip)
        c.set(base_x, 30 - height, tip)
        c.set(base_x + 1, 30 - height, tip)
    ellipse(c, 10, 29, 4, 3, "#f2d0a8")
    for x in range(7, 14, 2):
        c.set(x, 28, "#c9a07a")
        c.set(x, 29, "#c9a07a")
    for x in range(32):
        c.set(x, 31, "#2f8a8e")
    return c


# ---------------------------------------------------------------- temple

def temple_top(r):
    c = Canvas(64, 8)
    # A carved sandstone frieze.
    for x in range(64):
        for y in range(5):
            c.set(x, y, "#a8823e" if y in (0, 4) else "#8a6a30")
        if x % 8 == 3:
            for y in (1, 2, 3):
                c.set(x, y, "#5a4420")
        if x % 8 in (5, 6):
            c.set(x, 2, "#5a4420")
    return c


def temple_bottom(r):
    c = Canvas(64, 10)
    ground(c, r, ["#f0cf7a", "#d9b25a", "#c09a46", "#a8823e"], waves=((2, 1.5), (5, 0.5)), base=4)
    for _ in range(8):
        c.set(r.randrange(64), 8, "#8a6a30")
    return c


def temple_corner(r):
    c = Canvas(32, 32)
    # A pyramid in the distance and an obelisk in front of it.
    for y in range(14, 32):
        w = y - 14
        for x in range(26 - w, 26 + w + 1):
            c.set(x, y, "#c09a46" if x < 26 else "#8a6a30")
    for y in range(6, 32):
        w = 1 if y < 9 else 2
        for x in range(13 - w, 13 + w + 1):
            c.set(x, y, "#d9b25a" if x < 13 else "#a8823e")
    c.set(13, 5, "#f0cf7a")
    for y in (12, 16, 20):
        c.set(13, y, "#5a4420")
    return c


# ---------------------------------------------------------------- neo babylon

def neo_top(r):
    c = Canvas(64, 8)
    for x in range(64):
        c.set(x, 0, "#2a2440")
        c.set(x, 1, "#3a3260")
        c.set(x, 2, "#b9a8ff" if x % 16 < 12 else "#3a3260")
        c.set(x, 3, "#2a2440")
    for x in range(6, 64, 16):
        for y in range(4, 7):
            c.set(x, y, "#5a4a9a")
        c.set(x, 7, "#7fe8ff")
    return c


def neo_bottom(r):
    c = Canvas(64, 10)
    for x in range(64):
        c.set(x, 5, "#7fe8ff" if x % 8 < 5 else "#3a3260")
        for y in range(6, 10):
            c.set(x, y, "#3a3260" if (x % 16 == 0 or y == 7) else "#2a2440")
    return c


def neo_corner(r):
    c = Canvas(32, 32)
    # A stepped ziggurat with glowing seams.
    for i, (w, h) in enumerate(((14, 6), (11, 6), (8, 6), (5, 6))):
        y0 = 31 - (i + 1) * h + 1
        for y in range(y0, y0 + h):
            for x in range(24 - w, 24 + w + 1):
                c.set(x, y, "#4a3e7a" if x < 24 else "#352c5a")
        for x in range(24 - w, 24 + w + 1):
            c.set(x, y0, "#b9a8ff")
    for y in range(2, 8):
        c.set(24, y, "#7fe8ff")
    return c


# ---------------------------------------------------------------- tiamat

def tiamat_top(r):
    c = Canvas(64, 8)
    drips(c, r, ["#1f2f5a", "#253a6a"], "#3f5f9a", "#8fb8ff", spacing=(5, 11), length=(1, 4))
    for _ in range(5):
        c.set(r.randrange(64), r.randint(5, 7), "#cfe0ff")
    return c


def tiamat_bottom(r):
    c = Canvas(64, 12)
    ground(c, r, ["#8fb8ff", "#3f6ab0", "#2a4f8a", "#1f3a6a", "#172c52"], waves=((3, 1.4), (7, 0.5)), base=5)
    return c


def tiamat_corner(r):
    c = Canvas(32, 32)
    # A sea serpent: two humps breaking the water and a neck rising to its head.
    body, belly, fin = "#2f6a9a", "#1f4a74", "#8fd0ff"
    for cx in (7, 16):
        for x in range(cx - 4, cx + 5):
            top = 27 - round(math.sqrt(max(0, 16 - (x - cx) ** 2)) * 1.1)
            for y in range(top, 29):
                c.set(x, y, body if y < top + 2 else belly)
            if x % 2 == 0:
                c.set(x, top - 1, fin)
    for i in range(40):
        t = i / 39
        x = 23 + math.sin(t * 2.2) * 3
        y = 29 - t * 20
        for d in range(-2, 2):
            c.set(round(x + d), round(y), body if d > -2 else belly)
        if i % 5 == 0:
            c.set(round(x) + 2, round(y), fin)
    ellipse(c, 25, 8, 4.5, 2.6, body)
    ellipse(c, 20.5, 9, 2.5, 1.6, body)
    c.set(26, 7, "#ffcf6a")
    for x in range(18, 21):
        c.set(x, 10, belly)
    for x in range(32):
        c.set(x, 29, "#3f6ab0")
        c.set(x, 30, "#2a4f8a")
        c.set(x, 31, "#1f3a6a")
    return c


# ---------------------------------------------------------------- sunken city

def sunken_top(r):
    c = Canvas(64, 10)
    drips(c, r, ["#6a2238", "#7a2a44", "#5a1c30"], "#a83a5a", "#ff9fb4", spacing=(3, 7), length=(1, 6))
    return c


def sunken_bottom(r):
    c = Canvas(64, 12)
    ground(c, r, ["#ff9fb4", "#c9506e", "#a83a5a", "#7a2a44", "#5a1c30"], waves=((5, 1.2), (11, 0.6)), base=6)
    for _ in range(5):
        x, y = r.randrange(64), r.randint(1, 4)
        c.set(x, y, "#ff9fb4")
    return c


def sunken_corner(r):
    c = Canvas(32, 32)
    # A watchful eye on a fleshy stalk.
    for y in range(18, 32):
        sway = round(math.sin(y / 4) * 1.5)
        for x in range(23 + sway, 27 + sway):
            c.set(x, y, "#a83a5a" if x < 25 + sway else "#7a2a44")
    ellipse(c, 24, 13, 7, 7, "#f6e6e0")
    ellipse(c, 25, 13, 3.5, 3.5, "#c9506e")
    ellipse(c, 25, 13, 1.6, 1.6, "#1a0a10")
    c.set(23, 11, "#ffffff")
    for a in range(0, 360, 30):
        x = 24 + math.cos(math.radians(a)) * 7
        y = 13 + math.sin(math.radians(a)) * 7
        c.set(round(x), round(y), "#c9506e")
    return c


# ---------------------------------------------------------------- eggplant world

def eggplant_top(r):
    c = Canvas(64, 10)
    for x in range(64):
        c.set(x, 0, "#3a1f4a")
        c.set(x, 1, "#4a2a5f" if r.random() < 0.8 else "#3a1f4a")
    x = 0
    while x < 64:
        x += r.randint(7, 14)
        n = r.randint(2, 5)
        for y in range(2, 2 + n):
            c.set(wrap(c, x), y, "#4f8a3a")
        for dy in range(3):
            for dx in (-1, 0, 1):
                if not (dy == 2 and dx):
                    c.set(wrap(c, x + dx), 2 + n + dy, "#9a4ac9" if dx < 1 else "#6a2a8a")
    return c


def eggplant_bottom(r):
    c = Canvas(64, 10)
    ground(c, r, ["#b06ae0", "#7a3a9a", "#5f2a7a", "#4a1f5f"], waves=((3, 1.0), (8, 0.5)), base=5)
    return c


def eggplant_corner(r):
    c = Canvas(32, 32)
    # One proud eggplant.
    for y in range(9, 31):
        t = (y - 9) / 21
        w = 2.5 + t * 6 if t < 0.75 else 2.5 + 0.75 * 6 - (t - 0.75) * 24
        cx = 22 + t * 2
        for x in range(round(cx - w), round(cx + w) + 1):
            c.set(x, y, "#b06ae0" if x < cx - w * 0.3 else ("#7a3a9a" if x < cx + w * 0.5 else "#5f2a7a"))
    for x in range(18, 26):
        c.set(x, 9, "#4f8a3a")
        c.set(x, 10, "#3f6f2a" if x % 2 else "#4f8a3a")
    for y in range(5, 9):
        c.set(21, y, "#4f8a3a")
    c.set(19, 15, "#d6a4ff")
    c.set(19, 16, "#d6a4ff")
    return c

PIECES = {
    "jungle": (jungle_top, jungle_bottom, jungle_corner),
    "volcana": (volcana_top, volcana_bottom, volcana_corner),
    "ice-caves": (ice_top, ice_bottom, ice_corner),
    "dwelling": (dwelling_top, dwelling_bottom, dwelling_corner),
    "olmec": (olmec_top, olmec_bottom, olmec_corner),
    "tide-pool": (tide_top, tide_bottom, tide_corner),
    "temple": (temple_top, temple_bottom, temple_corner),
    "neo-babylon": (neo_top, neo_bottom, neo_corner),
    "tiamat": (tiamat_top, tiamat_bottom, tiamat_corner),
    "sunken-city": (sunken_top, sunken_bottom, sunken_corner),
    "eggplant-world": (eggplant_top, eggplant_bottom, eggplant_corner),
}


def main(out):
    os.makedirs(out, exist_ok=True)
    for zone, fns in PIECES.items():
        for part, fn in zip(("top", "bottom", "corner"), fns):
            r = random.Random(f"{zone}-{part}")
            with open(os.path.join(out, f"{zone}-{part}.svg"), "w") as f:
                f.write(fn(r).svg())


if __name__ == "__main__":
    main(sys.argv[1])
