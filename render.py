#!/usr/bin/env python3
"""Render the V3 news-image entry: a numbered world atlas of 13 Nov 2026.

Draws a 1024x1024 image: title header, lead-story banner, a world map with
26 numbered pins, and a 3-column story index keyed to the map numbers.
Run: python3 render.py  ->  writes entry.png next to this script.
All facts were verified against reporting from 13 November 2026.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# ---------- palette ----------
NAVY = (22, 40, 60)
NAVY2 = (30, 52, 78)
PAPER = (247, 243, 234)
INK = (28, 28, 26)
GREY = (96, 96, 92)
RULE = (205, 198, 182)
OCEAN = (207, 224, 236)
LAND = (236, 229, 211)
LAND_EDGE = (154, 143, 111)
RED = (178, 34, 34)
RED_DK = (140, 24, 24)
GOLD = (197, 146, 44)
LABEL_GREY = (106, 122, 138)

FDIR = "/usr/share/fonts/truetype/liberation/"


def font(name, size):
    return ImageFont.truetype(os.path.join(FDIR, name), size)


F_TITLE = font("LiberationSans-Bold.ttf", 46)
F_SUB = font("LiberationSans-Regular.ttf", 19)
F_LEAD_TAG = font("LiberationSans-Bold.ttf", 15)
F_LEAD = font("LiberationSans-Bold.ttf", 23)
F_LEAD2 = font("LiberationSans-Regular.ttf", 15)
F_MAPLBL = font("LiberationSans-Bold.ttf", 15)
F_PIN = font("LiberationSans-Bold.ttf", 14)
F_SEC = font("LiberationSans-Bold.ttf", 17)
F_HEAD = font("LiberationSans-Bold.ttf", 15)
F_DET = font("LiberationSans-Regular.ttf", 12)
F_FOOT = font("LiberationSans-Regular.ttf", 12)
F_LEGEND = font("LiberationSans-Regular.ttf", 13)
F_LEGEND_B = font("LiberationSans-Bold.ttf", 13)

# ---------- map geometry ----------
# Equirectangular: lon -180..180 -> x 12..1012 ; lat 80..-60 -> y 136..488
MAP_X0, MAP_X1 = 12, 1012
MAP_Y0, MAP_Y1 = 136, 488
LAT_TOP, LAT_BOT = 80.0, -60.0


def xy(lon, lat):
    x = MAP_X0 + (lon + 180.0) * (MAP_X1 - MAP_X0) / 360.0
    y = MAP_Y0 + (LAT_TOP - lat) * (MAP_Y1 - MAP_Y0) / (LAT_TOP - LAT_BOT)
    return (x, y)


def poly(points):
    return [xy(lon, lat) for lon, lat in points]


# Simplified continent outlines (lon, lat), hand-drawn for recognisability.
NORTH_AMERICA = [(-168, 66), (-158, 71), (-145, 70), (-135, 69), (-128, 70),
                 (-120, 72), (-110, 68), (-100, 69), (-90, 69), (-85, 66),
                 (-82, 62), (-78, 58), (-72, 58), (-65, 60), (-60, 52),
                 (-55, 47), (-60, 44), (-65, 44), (-70, 42), (-74, 39),
                 (-76, 35), (-80, 32), (-81, 26), (-84, 30), (-86, 30),
                 (-90, 29), (-94, 29), (-97, 26), (-97, 22), (-94, 18),
                 (-91, 16), (-87, 15), (-83, 15), (-80, 9), (-77, 8),
                 (-80, 8), (-83, 10), (-88, 13), (-92, 15), (-96, 16),
                 (-100, 18), (-105, 20), (-109, 23), (-112, 27), (-117, 32),
                 (-121, 35), (-124, 40), (-124, 47), (-128, 51), (-132, 56),
                 (-137, 59), (-145, 60), (-153, 58), (-160, 58), (-165, 60)]
GREENLAND = [(-58, 64), (-52, 60), (-43, 60), (-38, 64), (-30, 68),
             (-24, 70), (-28, 74), (-38, 77), (-52, 77), (-62, 75),
             (-70, 72), (-66, 68), (-60, 65)]
SOUTH_AMERICA = [(-77, 8), (-72, 12), (-64, 10), (-59, 8), (-53, 5),
                 (-50, 0), (-44, -3), (-35, -8), (-37, -13), (-39, -18),
                 (-41, -23), (-48, -26), (-53, -33), (-58, -38), (-62, -41),
                 (-65, -45), (-68, -50), (-69, -54), (-73, -53), (-73, -46),
                 (-73, -39), (-72, -31), (-70, -23), (-73, -16), (-77, -12),
                 (-80, -6), (-81, -1), (-80, 2)]
EURASIA = [(-10, 37), (-9, 43), (-2, 48), (2, 51), (5, 53), (8, 55),
           (8, 58), (12, 56), (17, 55), (20, 56), (23, 59), (28, 60),
           (30, 63), (33, 66), (40, 68), (50, 69), (60, 69), (70, 72),
           (80, 73), (90, 75), (100, 77), (110, 76), (120, 73), (130, 72),
           (140, 71), (150, 70), (160, 69), (170, 67), (178, 65), (178, 62),
           (170, 60), (163, 59), (158, 53), (153, 47), (145, 45), (142, 50),
           (140, 40), (136, 35), (131, 33), (127, 34), (122, 31), (120, 25),
           (114, 22), (109, 20), (106, 10), (104, 2), (101, 7), (99, 11),
           (97, 16), (94, 18), (91, 22), (88, 22), (85, 19), (81, 14),
           (78, 8), (75, 12), (73, 18), (70, 21), (66, 25), (61, 25),
           (57, 26), (53, 28), (49, 30), (45, 30), (41, 31), (37, 36),
           (33, 36), (30, 36), (27, 37), (23, 36), (20, 40), (16, 42),
           (13, 45), (9, 44), (6, 43), (3, 43), (-1, 38), (-6, 36)]
UK = [(-5, 50), (-3, 53), (-5, 56), (-4, 58), (-2, 58), (0, 53), (1, 51),
      (-2, 50)]
JAPAN = [(130, 31), (132, 33), (135, 34), (138, 35), (140, 37), (141, 40),
         (142, 43), (144, 44), (143, 41), (141, 38), (139, 36), (136, 34),
         (133, 33)]
AFRICA = [(-17, 15), (-16, 20), (-13, 27), (-9, 31), (-5, 35), (0, 36),
          (10, 37), (15, 32), (20, 32), (28, 31), (32, 31), (34, 28),
          (36, 24), (38, 21), (41, 15), (43, 12), (48, 11), (51, 10),
          (48, 4), (43, -2), (40, -7), (39, -13), (37, -19), (35, -23),
          (33, -27), (29, -32), (25, -34), (20, -35), (17, -32), (15, -27),
          (13, -21), (12, -15), (10, -6), (9, -1), (6, 4), (0, 5), (-6, 5),
          (-11, 7), (-15, 11)]
MADAGASCAR = [(44, -16), (47, -15), (50, -17), (49, -21), (47, -25),
              (45, -25), (43, -21), (43, -18)]
AUSTRALIA = [(113, -22), (118, -20), (122, -17), (126, -14), (132, -12),
             (136, -12), (140, -17), (142, -11), (146, -14), (148, -19),
             (150, -23), (153, -26), (153, -30), (150, -37), (147, -39),
             (143, -39), (139, -37), (136, -35), (133, -33), (129, -32),
             (125, -33), (120, -34), (115, -34), (113, -30)]
NEW_ZEALAND = [(167, -46), (170, -43), (173, -40), (176, -38), (178, -37),
               (175, -40), (172, -43), (169, -46)]
SUMATRA = [(95, 5), (98, 3), (101, 0), (104, -3), (106, -6), (103, -5),
           (100, -1), (97, 2)]
BORNEO = [(109, 1), (113, 4), (117, 6), (119, 2), (117, -2), (113, -3),
          (110, -1)]
JAVA = [(105, -6), (110, -6), (114, -7), (114, -8), (109, -8), (105, -7)]
NEW_GUINEA = [(131, -1), (136, -2), (141, -3), (146, -6), (150, -9),
              (147, -10), (143, -8), (138, -7), (133, -4)]
SULAWESI = [(119, 0), (121, 1), (122, -2), (120, -4), (119, -2)]
PHILIPPINES = [(120, 18), (122, 18), (122, 14), (121, 10), (120, 12),
               (119, 15)]
ICELAND = [(-22, 64), (-18, 63), (-14, 64), (-15, 66), (-20, 66), (-23, 65)]
CUBA = [(-85, 22), (-80, 23), (-74, 20), (-74, 19), (-80, 21), (-85, 21)]
SRI_LANKA = [(80, 9), (82, 7), (81, 6), (80, 7)]
TAIWAN = [(120, 22), (121, 25), (122, 25), (121, 22)]

LAND_POLYS = [NORTH_AMERICA, GREENLAND, SOUTH_AMERICA, EURASIA, UK, JAPAN,
              AFRICA, MADAGASCAR, AUSTRALIA, NEW_ZEALAND, SUMATRA, BORNEO,
              JAVA, NEW_GUINEA, SULAWESI, PHILIPPINES, ICELAND, CUBA,
              SRI_LANKA, TAIWAN]

# Region labels: (text, lon, lat)
REGION_LABELS = [
    ("NORTH AMERICA", -100, 58),
    ("SOUTH AMERICA", -60, -27),
    ("EUROPE", 18, 64),
    ("AFRICA", 13, 1),
    ("ASIA", 88, 56),
    ("OCEANIA", 152, -24),
]

# Stories: (number, headline, detail, lon, lat, dx, dy)
# dx/dy shift the displayed pin away from the true point (leader line drawn).
STORIES = [
    (1, "FAA GROUNDS ALL US FLIGHTS",
     "Telecom outage halts departures for hours; 10,000+ delayed, 5,000 cancelled",
     -106, 43, 0, 0),
    (2, "US PRODUCER PRICES JUMP",
     "October PPI +0.3% on the month, +6.5% on the year, most since 2022",
     -77, 39, 0, -30),
    (3, "NVIDIA CHIEF QUITS",
     "Jensen Huang resigns; shares slide, finance chief Kress takes over",
     -122, 37, 0, 0),
    (4, "SENATE LEADERSHIP FIGHT",
     "Van Hollen challenges Schumer after midterm wins; vote due Dec 1",
     -77, 39, 32, -12),
    (5, "BROOKLYN COLLAPSE TOLL 8",
     "Search ends; two children among dead, checks ordered at 100 sites",
     -74, 41, 30, 18),
    (6, "DEMOCRAT WINS KANSAS",
     "Governor's race called after a two-day count",
     -95.7, 39, 0, 0),
    (7, "$1.2BN CRYPTO SEIZURE",
     "US court backs seizure of Binance hack funds blamed on North Korea",
     -77, 39, -30, -8),
    (8, "MEASLES RULING AWAITED",
     "Experts weigh whether the virus spread for a year in the US and Mexico",
     -102, 30, 0, 0),
    (9, "POPE LEO IN PERU",
     "Meets abuse survivors in Lima as record crowds line the streets",
     -77, -12, 0, 0),
    (10, "EUROPE JOINS UKRAINE TALKS",
     "Russia, Ukraine agree Europeans at next round; huge prisoner swap eyed",
     30, 50, 0, -14),
    (11, "STORM CHARLES HITS PORTUGAL",
     "Schools shut as severe weather batters the mainland",
     -9, 39, 0, 0),
    (12, "ENGLAND BEAT CROATIA",
     "Kane penalty at Wembley sends Three Lions to Nations League last eight",
     0, 51, -26, -16),
    (13, "US OFFICER NAMED IN SPY PROBE",
     "Lt Col Tyner held in UK over alleged Russia espionage; charges due",
     -2, 52, -32, 12),
    (14, "FRANCE PUSHES RUSSIA SANCTIONS",
     "Paris reportedly seeks new EU curbs on Russian banks",
     2, 49, 26, -14),
    (15, "SUDAN ARMY TAKES STRONGHOLD",
     "Forces seize al-Mazroub in North Kordofan from the RSF",
     29.5, 13, 0, 0),
    (16, "SUDAN-ETHIOPIA EXPULSIONS",
     "Tit-for-tat consulate closures as drone-attack row deepens",
     37, 9, 0, 0),
    (17, "CHINA DRILLS RING TAIWAN",
     "100+ vessels in unannounced Pacific exercise Taipei calls intimidation",
     121, 23.5, 0, 0),
    (18, "IAEA LOSES SIGHT OF IRAN SITE",
     "Watchdog cannot locate Isfahan plant; 441 kg of 60% uranium unverified",
     51.7, 32.7, 0, 0),
    (19, "FOUR TANKERS HIT IN HORMUZ",
     "Iran says LNG carrier struck a mine; Gulf shipping on alert",
     56.5, 26.5, 12, 14),
    (20, "TURKEY-QATAR DEFENCE PACT",
     "Erdogan, Emir Tamim sign mutual defence deal in Istanbul",
     29, 41, 0, 0),
    (21, "GAZA HOSPITAL STRIKE KILLS 6",
     "Strike on Khan Younis complex kills a surgeon and five others",
     34.3, 31.3, 0, 0),
    (22, "YEN SLIDES PAST 160",
     "Japan warns it may act again after currency hits two-month low",
     139.7, 35.7, 0, 0),
    (23, "IEA SEES OIL SURPLUS",
     "Agency forecasts Q4 supply beating demand by 1.7m barrels a day",
     2.35, 48.85, 32, 14),
    (24, "MICROSOFT 365 GOES DOWN",
     "Outlook, Teams fail in 74 countries; 120,000+ problem reports",
     -122, 47.6, 0, 0),
    (25, "CHIP CURBS ROW",
     "Bessent frustrated at delays over Singapore firm Megaspeed",
     104, 1.3, 0, 0),
    (26, "AUSTRALIA ROUT ENGLAND",
     "Seven-wicket win in Perth ODI; England bowled out for 131",
     115.9, -32, 0, 0),
]

LEAD_HEAD = "AMERICA'S SKIES STAND STILL"
LEAD_DET = ("The FAA halts every US departure for hours after a telecom outage "
            "hits air traffic control. 10,000+ flights delayed, 5,000 cancelled.")


def wrap_text(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines fitting max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_map(d):
    # ocean
    d.rectangle([MAP_X0, MAP_Y0, MAP_X1, MAP_Y1], fill=OCEAN)
    # graticule
    for lon in range(-150, 181, 30):
        x = xy(lon, 0)[0]
        d.line([(x, MAP_Y0), (x, MAP_Y1)], fill=(188, 208, 224), width=1)
    for lat in range(-60, 81, 30):
        y = xy(0, lat)[1]
        d.line([(MAP_X0, y), (MAP_X1, y)], fill=(188, 208, 224), width=1)
    # land
    for pts in LAND_POLYS:
        d.polygon(poly(pts), fill=LAND, outline=LAND_EDGE, width=1)
    # region labels
    for text, lon, lat in REGION_LABELS:
        cx, cy = xy(lon, lat)
        w = d.textlength(text, font=F_MAPLBL)
        d.text((cx - w / 2, cy - 8), text, font=F_MAPLBL, fill=LABEL_GREY)
    # pins (leader lines first, then circles, then numbers)
    for num, _h, _dt, lon, lat, dx, dy in STORIES:
        tx, ty = xy(lon, lat)
        px, py = tx + dx, ty + dy
        if dx or dy:
            d.line([(tx, ty), (px, py)], fill=(120, 120, 118), width=1)
            d.ellipse([tx - 3, ty - 3, tx + 3, ty + 3], fill=(90, 90, 88))
    for num, _h, _dt, lon, lat, dx, dy in STORIES:
        tx, ty = xy(lon, lat)
        px, py = tx + dx, ty + dy
        r = 12
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                  outline=(255, 255, 255), width=2)
        s = str(num)
        w = d.textlength(s, font=F_PIN)
        d.text((px - w / 2, py - 8), s, font=F_PIN, fill=(255, 255, 255))
    # frame
    d.rectangle([MAP_X0, MAP_Y0, MAP_X1, MAP_Y1], outline=NAVY, width=2)


def draw_header(d):
    d.rectangle([0, 0, W, 76], fill=NAVY)
    d.rectangle([0, 76, W, 80], fill=GOLD)
    title = "THE WORLD IN ONE DAY"
    d.text((24, 14), title, font=F_TITLE, fill=(255, 255, 255))
    date = "FRIDAY 13 NOVEMBER 2026"
    w = d.textlength(date, font=F_SUB)
    d.text((W - 24 - w, 14), date, font=F_SUB, fill=(220, 226, 232))
    sub = "26 stories  ·  6 continents"
    w2 = d.textlength(sub, font=font("LiberationSans-Regular.ttf", 15))
    d.text((W - 24 - w2, 42), sub,
           font=font("LiberationSans-Regular.ttf", 15), fill=(168, 182, 196))


def draw_lead(d):
    y0, y1 = 84, 132
    d.rectangle([12, y0, 1012, y1], fill=(255, 255, 255), outline=RULE, width=1)
    d.rectangle([12, y0, 20, y1], fill=RED)
    tag = "LEAD  "
    d.text((30, y0 + 7), tag, font=F_LEAD_TAG, fill=RED_DK)
    tw = d.textlength(tag, font=F_LEAD_TAG)
    d.text((30 + tw, y0 + 4), LEAD_HEAD, font=F_LEAD, fill=INK)
    d.text((30, y0 + 28), LEAD_DET, font=F_LEAD2, fill=GREY)


def draw_stories(d):
    sec_y = 500
    d.text((16, sec_y), "THE STORIES  —  NUMBERS MATCH THE MAP", font=F_SEC, fill=NAVY)
    d.line([(16, sec_y + 24), (1008, sec_y + 24)], fill=NAVY, width=2)
    # grid: 3 columns x 9 rows; 26 stories + 1 legend cell
    cols, rows = 3, 9
    gx0, gx1 = 16, 1008
    gy0, gy1 = 532, 988
    gutter = 14
    col_w = (gx1 - gx0 - gutter * (cols - 1)) / cols
    row_h = (gy1 - gy0) / rows
    cells = list(STORIES) + [None]  # legend cell last
    for i, cell in enumerate(cells):
        r, c = divmod(i, cols)
        x0 = gx0 + c * (col_w + gutter)
        y0 = gy0 + r * row_h
        if cell is None:
            draw_legend(d, x0, y0, col_w, row_h)
            continue
        num, head, det, _lon, _lat, _dx, _dy = cell
        # number chip
        d.rounded_rectangle([x0, y0 + 2, x0 + 24, y0 + 26], radius=4, fill=RED)
        s = str(num)
        w = d.textlength(s, font=F_PIN)
        d.text((x0 + 12 - w / 2, y0 + 6), s, font=F_PIN, fill=(255, 255, 255))
        tx = x0 + 31
        tw = col_w - 31
        # headline, up to 2 lines
        hl = wrap_text(d, head, F_HEAD, tw)[:2]
        yy = y0 + 1
        for line in hl:
            d.text((tx, yy), line, font=F_HEAD, fill=INK)
            yy += 17
        # detail, up to 2 lines
        dl = wrap_text(d, det, F_DET, tw)[:2]
        for line in dl:
            d.text((tx, yy), line, font=F_DET, fill=GREY)
            yy += 14
        # divider under each row except the last
        if r < rows - 1:
            d.line([(x0, y0 + row_h - 5), (x0 + col_w, y0 + row_h - 5)],
                   fill=RULE, width=1)


def draw_legend(d, x0, y0, w, h):
    d.rounded_rectangle([x0, y0 + 1, x0 + w, y0 + h - 6], radius=6,
                        fill=(232, 226, 210), outline=RULE, width=1)
    d.text((x0 + 10, y0 + 4), "WHERE THE NEWS FELL", font=F_LEGEND_B, fill=NAVY)
    lines = [
        "8 N America · 5 Europe · 4 Mideast · 3 Asia-Pac",
        "2 Africa · 1 S America · 1 Oceania · 2 global",
    ]
    yy = y0 + 21
    for line in lines:
        d.text((x0 + 10, yy), line, font=F_LEGEND, fill=GREY)
        yy += 14


def draw_footer(d):
    d.line([(16, 996), (1008, 996)], fill=RULE, width=1)
    foot = ("All events happened, or were first reported, on 13 November 2026.  "
            "Sources: Reuters, AP, BLS, FAA, IAEA, IEA, Al Jazeera, Microsoft, Downdetector.")
    w = d.textlength(foot, font=F_FOOT)
    d.text(((W - w) / 2, 1002), foot, font=F_FOOT, fill=GREY)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_header(d)
    draw_lead(d)
    draw_map(d)
    draw_stories(d)
    draw_footer(d)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
