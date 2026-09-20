from PIL import Image, ImageDraw, ImageFont
import math
import os

W, H = 1200, 360
FRAMES = 28
OUT = "assets/header.gif"

BG1 = (7, 17, 31)
BG2 = (10, 27, 43)
BG3 = (13, 40, 56)

GRID = (23, 53, 74)
TEAL = (66, 232, 180)
TEAL_SOFT = (77, 130, 151)
WHITE = (248, 250, 252)
SOFT = (155, 179, 195)
PANEL = (11, 32, 48)
PANEL_BORDER = (28, 70, 91)

def get_font(size, bold=False):
    candidates = []
    if bold:
        candidates += [
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/segoeuib.ttf",
        ]
    candidates += [
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "arial.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                pass
    return ImageFont.load_default()

font_small = get_font(11)
font_mono = get_font(14)
font_mono_small = get_font(10)
font_title = get_font(43, bold=True)
font_sub = get_font(17)
font_section = get_font(15)

def lerp(a, b, t):
    return int(a + (b - a) * t)

def gradient_bg():
    img = Image.new("RGB", (W, H), BG1)
    px = img.load()
    for y in range(H):
        t = y / H
        r = lerp(BG1[0], BG3[0], t)
        g = lerp(BG1[1], BG3[1], t)
        b = lerp(BG1[2], BG3[2], t)
        for x in range(W):
            px[x, y] = (r, g, b)
    return img

def draw_grid(d):
    for y in [90, 180, 270]:
        d.line((0, y, W, y), fill=GRID, width=1)
    for x in [300, 600, 900]:
        d.line((x, 0, x, H), fill=GRID, width=1)

def draw_header_text(d, online_on=True):
    d.text((38, 28), "DEVELOPER NAVIGATION SYSTEM // MC-26", fill=TEAL_SOFT, font=font_small)

    online_color = TEAL if online_on else (40, 110, 90)
    d.ellipse((1085, 29, 1095, 39), fill=online_color)
    d.text((1105, 28), "ONLINE", fill=TEAL, font=font_small)

    d.text((365, 98), "DEVELOPER FLIGHT DECK", fill=TEAL, font=font_section)
    d.text((365, 145), "MAYARA CELESTINO", fill=WHITE, font=font_title)
    d.text((368, 192), "Software Development · Full Stack · APIs · DevOps", fill=SOFT, font=font_sub)

    d.rounded_rectangle((365, 235, 1035, 302), radius=8, fill=PANEL, outline=PANEL_BORDER, width=1)
    d.text((388, 250), "CURRENT MISSION", fill=(102, 141, 160), font=font_mono_small)
    d.text((388, 275), "Junior Developer @ CAVOK Tecnologia", fill=WHITE, font=font_mono)

    d.ellipse((1003, 264, 1013, 274), fill=TEAL if online_on else (40, 110, 90))
    d.text((1020, 264), "ACTIVE", fill=TEAL, font=font_mono_small)

    d.text((1037, 330), "BUILD // LEARN // SHIP", fill=(65, 103, 121), font=font_mono_small)

def draw_radar_base(d):
    cx, cy = 185, 190
    radii = [105, 76, 47, 18]
    for r in radii:
        d.ellipse((cx-r, cy-r, cx+r, cy+r), outline=(36, 81, 104), width=1)

    d.line((80, cy, 290, cy), fill=(36, 81, 104), width=1)
    d.line((cx, 85, cx, 295), fill=(36, 81, 104), width=1)
    d.line((111, 116, 259, 264), fill=(36, 81, 104), width=1)
    d.line((259, 116, 111, 264), fill=(36, 81, 104), width=1)

    d.text((137, 318), "RADAR ACTIVE", fill=TEAL_SOFT, font=font_mono_small)

def draw_radar_sweep(d, angle_deg):
    cx, cy = 185, 190
    radius = 105
    angle = math.radians(angle_deg)
    angle2 = math.radians(angle_deg - 28)

    x1 = cx + radius * math.cos(angle)
    y1 = cy + radius * math.sin(angle)
    x2 = cx + radius * math.cos(angle2)
    y2 = cy + radius * math.sin(angle2)

    # setor suave
    d.polygon([(cx, cy), (x1, y1), (x2, y2)], fill=(20, 120, 90))
    # linha principal
    d.line((cx, cy, x1, y1), fill=TEAL, width=2)

def draw_targets(d, frame):
    blink1 = 255 if frame % 8 < 5 else 90
    blink2 = 255 if frame % 10 < 4 else 120

    c1 = (66, 232, 180, blink1)
    c2 = (66, 232, 180, blink2)

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    od.ellipse((228, 145, 236, 153), fill=c1)
    od.ellipse((142, 230, 148, 236), fill=c2)

    return overlay

frames = []

for i in range(FRAMES):
    img = gradient_bg().convert("RGBA")
    d = ImageDraw.Draw(img)

    draw_grid(d)
    draw_radar_base(d)

    angle = -90 + (360 / FRAMES) * i
    draw_radar_sweep(d, angle)

    img.alpha_composite(draw_targets(d, i))

    online_on = i % 6 < 4
    draw_header_text(d, online_on=online_on)

    frames.append(img.convert("P", palette=Image.ADAPTIVE))

os.makedirs("assets", exist_ok=True)
frames[0].save(
    OUT,
    save_all=True,
    append_images=frames[1:],
    duration=110,
    loop=0,
    optimize=False,
)

print(f"GIF gerado com sucesso em: {OUT}")