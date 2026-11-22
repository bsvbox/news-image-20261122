"""Generator for entry.png (the image shipped with this entry).

This is the program that drew entry.png: a newspaper front page with
Pillow only, no network, no random numbers, no clock reads. It is kept
here so the image's provenance is visible; the graded entrypoint
main.py only copies entry.png to /output/entry.png, so the graded run
needs no fonts and no Pillow.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (247, 243, 234)
NAVY = (20, 33, 61)
NAVY_LIGHT = (36, 54, 96)
GOLD = (201, 162, 39)
RED = (185, 28, 28)
INK = (24, 24, 24)
GREY = (90, 90, 88)
CARD = (255, 255, 255)
SKY = (13, 27, 62)
SEA = (24, 52, 96)
ORANGE = (249, 115, 22)
CREAM = (238, 232, 214)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
_FONTS_OK = os.path.exists(os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf"))


def font(name, size):
    if _FONTS_OK:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    return ImageFont.load_default(size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for word in words:
            trial = (cur + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def card(draw, box, outline=(205, 198, 182)):
    draw.rounded_rectangle(box, radius=10, fill=CARD, outline=outline, width=2)


def kicker(draw, x, y, text, color=RED):
    fnt = font(SANS_B, 24)
    draw.text((x, y), text, font=fnt, fill=color)
    return y + 32


def headline(draw, x, y, text, size, max_w, fill=INK, leading=None):
    fnt = font(SERIF_B, size)
    lead = leading or int(size * 1.12)
    lines = wrap(draw, text, fnt, max_w)
    return draw_lines(draw, lines, x, y, fnt, fill, lead)


def body(draw, x, y, text, size, max_w, fill=GREY):
    fnt = font(SANS, size)
    lines = wrap(draw, text, fnt, max_w)
    return draw_lines(draw, lines, x, y, fnt, fill, int(size * 1.3))


def draw_masthead(draw):
    draw.rectangle([0, 0, W, 148], fill=NAVY)
    draw.rectangle([0, 148, W, 154], fill=GOLD)
    title = "THE WORLD IN ONE PAGE"
    tf = font(SERIF_B, 58)
    tw = draw.textlength(title, font=tf)
    draw.text(((W - tw) / 2, 22), title, font=tf, fill=(255, 255, 255))
    date = "SUNDAY, 22 NOVEMBER 2026"
    df = font(SANS_B, 30)
    dw = draw.textlength(date, font=df)
    draw.text(((W - dw) / 2, 96), date, font=df, fill=GOLD)


def starburst(draw, cx, cy, r_out, r_in, points, fill):
    import math

    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def draw_lead_visual(draw, x0, y0, x1, y1):
    """Night scene over the Gulf: tanker silhouette, blast, labels."""
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    # stars
    for sx, sy in [(28, 18), (90, 44), (150, 12), (210, 36), (260, 16),
                   (320, 48), (60, 70), (180, 64), (300, 78), (120, 30)]:
        draw.ellipse([x0 + sx - 2, y0 + sy - 2, x0 + sx + 2, y0 + sy + 2],
                     fill=(220, 220, 200))
    # sea
    draw.rectangle([x0, y0 + 130, x1, y1], fill=SEA)
    draw.line([x0, y0 + 130, x1, y0 + 130], fill=(120, 150, 200), width=2)
    # tanker silhouette
    draw.rectangle([x0 + 30, y0 + 162, x0 + 300, y0 + 184], fill=(10, 12, 18))
    draw.rectangle([x0 + 230, y0 + 142, x0 + 272, y0 + 162], fill=(10, 12, 18))
    draw.rectangle([x0 + 246, y0 + 128, x0 + 256, y0 + 142], fill=(10, 12, 18))
    # blast above the tanker
    starburst(draw, x0 + 250, y0 + 84, 52, 24, 10, ORANGE)
    starburst(draw, x0 + 250, y0 + 84, 30, 14, 10, (253, 224, 71))
    # dashed route line
    for dx in range(0, 340, 18):
        draw.line([x0 + 12 + dx, y0 + 205, x0 + 22 + dx, y0 + 205],
                  fill=(255, 255, 255), width=2)
    lab = font(SANS_B, 20)
    draw.text((x0 + 16, y0 + 104), "BAHRAIN", font=lab, fill=(255, 255, 255))
    draw.text((x0 + 16, y0 + 212), "STRAIT OF HORMUZ", font=lab,
              fill=(200, 210, 230))


def draw_lead(draw):
    card(draw, [16, 168, 1008, 440])
    kicker(draw, 40, 188, "GULF WAR WIDENS")
    headline(draw, 40, 224, "Iran strikes US bases\nin Bahrain", 46, 560)
    body(draw, 40, 336,
         "IRGC claims Patriot radars hit at al-Riffa and Awali. "
         "Two tankers struck by projectiles off Oman.",
         22, 560)
    draw_lead_visual(draw, 624, 188, 984, 420)


def draw_ballot_box(draw, x, y, s=1.0):
    """Small ballot box; s scales it. y is the box top."""
    bw, bh = int(130 * s), int(78 * s)
    draw.rectangle([x, y, x + bw, y + bh], fill=NAVY)
    draw.rectangle([x - 5, y - 8, x + bw + 5, y + 2], fill=NAVY_LIGHT)
    draw.line([x + int(30 * s), y - 3, x + int(100 * s), y - 3],
              fill=GOLD, width=4)


def draw_globe(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=4)
    draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
                 outline=NAVY, width=3)
    draw.line([cx - r, cy, cx + r, cy], fill=NAVY, width=3)
    draw.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
             0, 360, fill=NAVY, width=3)


def panel(draw, box, kick, head, body_text, visual):
    card(draw, box)
    x0, y0, x1, y1 = box
    kicker(draw, x0 + 22, y0 + 14, kick)
    headline(draw, x0 + 22, y0 + 48, head, 29, x1 - x0 - 44)
    body(draw, x0 + 22, y0 + 120, body_text, 20, x1 - x0 - 44)
    visual(draw, x0, y0, x1, y1)


def visual_hk(draw, x0, y0, x1, y1):
    draw.text((x0 + 22, y1 - 56), "723 seats", font=font(SERIF_B, 38),
              fill=NAVY)
    draw_ballot_box(draw, x1 - 140, y1 - 52, 0.55)


def visual_cop(draw, x0, y0, x1, y1):
    draw_globe(draw, x1 - 62, y1 - 32, 22)
    badge = [x0 + 22, y1 - 52, x0 + 186, y1 - 18]
    draw.rounded_rectangle(badge, radius=8, fill=RED)
    bf = font(SANS_B, 18)
    draw.text((badge[0] + 13, badge[1] + 8), "NO DEAL YET", font=bf,
              fill=(255, 255, 255))


def visual_sa(draw, x0, y0, x1, y1):
    base = y1 - 22
    draw.rectangle([x0 + 26, base - 28, x0 + 58, base], fill=NAVY_LIGHT)
    draw.rectangle([x0 + 72, base - 21, x0 + 104, base], fill=NAVY)
    sf = font(SANS_B, 13)
    draw.text((x0 + 26, base + 3), "2021", font=sf, fill=GREY)
    draw.text((x0 + 72, base + 3), "2026", font=sf, fill=GREY)
    draw.text((x0 + 128, base - 26), "ANC share falls",
              font=font(SANS_B, 19), fill=INK)


def visual_sport(draw, x0, y0, x1, y1):
    sx, sy = x1 - 132, y1 - 50
    for i in range(3):
        draw.rectangle([sx + i * 13, sy, sx + i * 13 + 7, sy + 34],
                       fill=GOLD)
    draw.rectangle([sx + 2, sy - 4, sx + 13, sy - 1], fill=GOLD)
    draw.rectangle([sx + 15, sy - 4, sx + 26, sy - 1], fill=GOLD)
    draw.ellipse([sx + 54, sy + 8, sx + 74, sy + 28], fill=RED)
    draw.arc([sx + 54, sy + 8, sx + 74, sy + 28], 200, 340,
             fill=(255, 255, 255), width=2)
    draw.polygon([(x0 + 28, y1 - 52), (x0 + 50, y1 - 56),
                  (x0 + 66, y1 - 18), (x0 + 44, y1 - 14)],
                 fill=(217, 179, 128), outline=(150, 110, 60))


def draw_ticker(draw):
    draw.rectangle([0, 936, W, H], fill=NAVY)
    draw.rectangle([0, 936, W, 940], fill=GOLD)
    text = ("ALSO THIS WEEKEND:  France seeks UN action on Myanmar   •   "
            "FBI probes hack of its crime database")
    tf = font(SANS_B, 19)
    while draw.textlength(text, font=tf) > W - 48 and tf.size > 14:
        tf = font(SANS_B, tf.size - 1)
    draw.text((24, 968), text, font=tf, fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    draw_lead(draw)
    panel(draw, [16, 456, 496, 680], "HONG KONG VOTES",
          "Hong Kong votes for its Election Committee",
          "856 candidates contest 723 seats.\nPolls open 9am to 6pm.",
          visual_hk)
    panel(draw, [528, 456, 1008, 680], "CLIMATE",
          "COP31 talks deadlocked in overtime",
          "No deal yet in Antalya.\nFossil-fuel fight blocks a deal.",
          visual_cop)
    panel(draw, [16, 696, 496, 920], "SOUTH AFRICA",
          "ANC loses ground in local polls",
          "Historic setback.\nCoalition talks decide hung councils.",
          visual_sa)
    panel(draw, [528, 696, 1008, 920], "SPORT",
          "India face New Zealand in Wellington",
          "India v New Zealand in Wellington.\nCummins keeps Australia captaincy.",
          visual_sport)
    draw_ticker(draw)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, format="PNG")


if __name__ == "__main__":
    main()
