"""draw.py — news-23 b126 front-page-dense: THE WORLD TODAY, Mon 23 Nov 2026."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1024, 1024
BD = "/usr/share/fonts/truetype/dejavu"
def fb(sz): return ImageFont.truetype(f"{BD}/DejaVuSans-Bold.ttf", sz)
def fr(sz): return ImageFont.truetype(f"{BD}/DejaVuSans.ttf", sz)
def sb(sz): return ImageFont.truetype(f"{BD}/DejaVuSerif-Bold.ttf", sz)

BLACK = (12, 12, 12); WHITE = (255, 255, 255); GOLD = (212, 175, 55)
RED = (166, 25, 46); NAVY = (16, 32, 74); GREEN = (32, 102, 52)
CREAM = (250, 246, 236); GREY = (90, 90, 90); LGREY = (232, 230, 224)
MAPG = (178, 205, 170)

img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)

def text(x, y, s, f, fill, anchor="la"):
    d.text((x, y), s, font=f, fill=fill, anchor=anchor)

def wrap(s, f, maxw):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w_
    if cur: lines.append(cur)
    return lines

def chip(x, y, label, fill):
    f = fb(9)
    w_ = d.textlength(label, font=f) + 10
    d.rounded_rectangle([x, y, x + w_, y + 14], radius=2, fill=fill)
    d.text((x + 5, y + 2), label, font=f, fill=WHITE)
    return w_

# ---- masthead ----
d.rectangle([0, 0, W, 56], fill=BLACK)
text(14, 6, "THE WORLD TODAY", sb(42), WHITE)
dt = "MONDAY 23 NOVEMBER 2026"
text(1010, 18, dt, fb(19), GOLD, anchor="ra")

# ---- kicker ----
d.rectangle([0, 56, W, 78], fill=RED)
text(512, 61, "AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  US lead over China at record low  \u00b7  Anthropic IPO $107.3B",
     fb(15), WHITE, anchor="ma")

# ---- number strip (2 rows x 5) ----
strip = [("-3.3%", "KOSPI"), ("5.3", "US-CHINA POWER GAP"), ("11,762", "EBOLA CASES, DRC"),
         ("10T won", "SEOUL STABILISATION FUND"), ("2%", "BILLIONAIRE TAX IN PARIS"),
         ("$450M", "SKUBAL DEAL"), ("165", "RUSSIAN MISSILES/WEEK"), ("12,000", "CLEARED IN MANCHESTER"),
         ("264 kg", "EXPLOSIVES SEIZED"), ("$107.3B", "ANTHROPIC IPO")]
xs = [14, 216, 418, 620, 822]
for i, (v, lab) in enumerate(strip):
    r, c = divmod(i, 5)
    yv = 82 + r * 32
    text(xs[c], yv, v, fb(24), BLACK)
    text(xs[c], yv + 24, lab, fr(10), GREY)

# ---- region bar ----
d.rectangle([0, 152, W, 174], fill=BLACK)
segs = [("ASIA-PACIFIC 7", 224, (16, 32, 74)), ("AMERICAS 8", 256, RED),
        ("MIDDLE EAST 6", 193, (32, 102, 52)), ("EUROPE 5", 161, (96, 32, 112)),
        ("AFRICA 3", 96, (0, 120, 110)), ("WORLD 2", 64, GREY)]
x = 14
for lab, w_, col in segs:
    d.rectangle([x, 152, x + w_, 174], fill=col)
    text(x + w_ / 2, 158, lab, fb(12), WHITE, anchor="ma")
    x += w_

# ---- UTC strip ----
text(14, 178, "THE DAY IN UTC    ~00:00 Kospi dives    ~05:30 Guterres opens    ~09:00 Power Index    ~12:00 Paris 2% tax    ~15:00 Kyiv missiles",
     fr(11), GREY)
text(1010, 178, "~ APPROX", fr(11), GREY, anchor="ra")

# ---- heroes ----
cols = [(14, 318), (340, 330), (678, 332)]
# hero 1 scene: Kospi skyline + falling chart
x0, w0 = cols[0]
d.rectangle([x0, 192, x0 + w0, 308], fill=NAVY)
import random
random.seed(23)
bx = x0 + 8
while bx < x0 + w0 - 20:
    bw_ = random.randint(18, 30); bh = random.randint(30, 66)
    d.rectangle([bx, 308 - bh, bx + bw_, 308], fill=(24, 48, 96))
    for wy in range(308 - bh + 6, 304, 12):
        for wx in range(bx + 4, bx + bw_ - 4, 8):
            if random.random() < 0.7:
                d.rectangle([wx, wy, wx + 3, wy + 4], fill=GOLD)
    bx += bw_ + 4
pts = [(x0 + 150, 202), (x0 + 180, 218), (x0 + 205, 214), (x0 + 235, 236), (x0 + 262, 244), (x0 + 292, 264), (x0 + 312, 274)]
d.line(pts, fill=(255, 140, 40), width=3)
for p in pts:
    d.ellipse([p[0] - 4, p[1] - 4, p[0] + 4, p[1] + 4], fill=WHITE, outline=(255, 140, 40))
text(x0 + 10, 198, "\u22123.3%", fb(34), WHITE)
d.rectangle([x0, 288, x0 + w0, 308], fill=(8, 18, 46))
text(x0 + 10, 293, "KOSPI 4,708.54  \u00b7  -161 PTS", fb(11), WHITE)
# hero 2 scene: Guterres globe
x1, w1 = cols[1]
d.rectangle([x1, 192, x1 + w1, 308], fill=GREEN)
gt = ["150", "DELEGATES", "BACK A RISK", "FRAMEWORK"]
text(x1 + 12, 196, gt[0], fb(46), GOLD)
for i, ln in enumerate(gt[1:]):
    text(x1 + 12, 244 + i * 20, ln, fb(19), GOLD)
cx, cy, r_ = x1 + w1 - 62, 246, 52
d.ellipse([cx - r_, cy - r_, cx + r_, cy + r_], fill=(210, 232, 200))
for k in range(-2, 3):
    d.arc([cx - r_, cy - r_ + k * 20, cx + r_, cy + r_ + k * 20], 0, 360, fill=(120, 170, 120))
d.line([cx - r_, cy, cx + r_, cy], fill=(120, 170, 120))
d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(120, 170, 120))
# hero 3 scene: Power Index bars
x2, w2 = cols[2]
d.rectangle([x2, 192, x2 + w2, 308], fill=(240, 234, 220))
h3a, h3b = "NARROWEST SINCE 2018", "GAP 5.3"
fa, fbb = fb(14), fb(17)
while d.textlength(h3a, font=fa) + d.textlength(h3b, font=fbb) + 20 > w2 - 16 and fa.size > 10:
    fa = fb(fa.size - 1); fbb = fb(fbb.size - 1)
text(x2 + 8, 198, h3a, fa, BLACK)
text(x2 + w2 - 8, 197, h3b, fbb, RED, anchor="ra")
bars = [("78.9", "US", NAVY, 0.92), ("73.6", "CHINA", RED, 0.86), ("40.5", "INDIA", (176, 140, 30), 0.48)]
by = 222
for val, lab, col, frac in bars:
    text(x2 + 8, by, val, fb(15), BLACK)
    bw_ = int((w2 - 70) * frac)
    d.rectangle([x2 + 62, by + 2, x2 + 62 + bw_, by + 20], fill=col)
    text(x2 + 68, by + 4, lab, fb(11), WHITE)
    by += 28

heroes = [
    ("AI ROUT HITS ASIA",
     "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
     "KOREA EXCHANGE", "REPORTED", NAVY),
    ("GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit; 150 back a risk framework.",
     "UNITED NATIONS", "REPORTED", NAVY),
    ("US LEAD OVER CHINA AT RECORD LOW",
     "Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest since 2018. India third at 40.5.",
     "LOWY INSTITUTE", "REPORTED", NAVY),
]
for (x_, w_), (hl, body, src, ch, chcol) in zip(cols, heroes):
    lines = wrap(hl, fb(17), w_)
    y = 312
    for ln in lines[:2]:
        text(x_, y, ln, fb(17), BLACK)
        y += 19
    bl = wrap(body, fr(11), w_)
    y = 352
    for ln in bl[:2]:
        text(x_, y, ln, fr(11), BLACK)
        y += 13
    text(x_, 382, src, fr(9), GREY)
    chip(x_ + w_ - 62, 380, ch, chcol)

# ---- cards ----
d.rectangle([0, 392, W, 412], fill=BLACK)
text(14, 396, "MORE OF THE DAY  \u2014  10 STORIES", fb(13), WHITE)
cards = [
    ("AMERICAS", "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.", "WSJ", "REPORTED", NAVY),
    ("AMERICAS", "FBI PROBES NCIC HACK", "NCIC database hacked.", "AP", "REPORTED", NAVY),
    ("WHITE HOUSE", "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.", "Reuters", "REPORTED", NAVY),
    ("MARKETS", "US FUTURES JUMP 3%", "Holiday rally lifts 3%.", "Bloomberg", "REPORTED", NAVY),
    ("SPORT", "SKUBAL'S $450M METS DEAL", "Nine-year, largest ever.", "AP", "REPORTED", NAVY),
    ("SPORT", "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice.", "ESPN", "REPORTED", NAVY),
    ("LEGAL", "STATES SUE SPACEX", "Ten states sue over AI.", "AP", "REPORTED", NAVY),
    ("TECH", "ANTHROPIC IPO: $107.3B", "Raised $83; closes $97.17.", "WSJ", "REPORTED", NAVY),
    ("EUROPE", "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: 3 Kh-101s crossed.", "AP", "CLAIM", RED),
    ("SPACE", "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.", "Reuters", "CLAIM", RED),
]
cw, gap = 196, 4
for i, (cat, hl, body, src, ch, chcol) in enumerate(cards):
    r, c = divmod(i, 5)
    cx0 = 14 + c * (cw + gap)
    cy0 = 418 + r * 82
    text(cx0, cy0, cat, fb(9), RED)
    text(cx0 + cw - 8, cy0, str(i + 1), fb(11), RED, anchor="ra")
    hl_lines = wrap(hl, fb(12), cw)
    y = cy0 + 14
    for ln in hl_lines[:2]:
        text(cx0, y, ln, fb(12), BLACK)
        y += 14
    text(cx0, cy0 + 44, body, fr(10), BLACK)
    text(cx0, cy0 + 60, src, fr(9), GREY)
    chip(cx0 + cw - 62, cy0 + 58, ch, chcol)

# ---- map section ----
d.rectangle([0, 586, W, 606], fill=BLACK)
text(14, 590, "WHERE IT HAPPENED", fb(13), WHITE)
# blobs
d.polygon([(34, 650), (110, 640), (118, 720), (96, 800), (70, 856), (40, 830), (28, 740)], fill=MAPG)
d.polygon([(140, 656), (258, 648), (264, 716), (240, 768), (176, 770), (142, 720)], fill=MAPG)
d.polygon([(178, 772), (258, 770), (252, 830), (214, 852), (184, 820)], fill=MAPG)
d.polygon([(272, 646), (326, 640), (330, 720), (312, 776), (276, 760), (268, 700)], fill=MAPG)
pins = [(300, 700), (58, 800), (288, 664), (44, 672), (66, 652), (222, 676),
        (176, 706), (158, 676), (232, 700), (154, 714), (252, 724), (238, 748), (210, 812)]
for i, (px, py) in enumerate(pins, 1):
    d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED, outline=WHITE, width=2)
    f = fb(9)
    s = str(i)
    text(px, py - 5, s, f, WHITE, anchor="ma")
text(14, 830, "Pins 1\u201313: 1 Seoul \u00b7 2 Bridgetown \u00b7 3 Beijing", fr(9), GREY)
text(14, 842, "4 Washington \u00b7 5 New York \u00b7 6 Kyiv \u00b7 7 Paris", fr(9), GREY)
text(14, 854, "8 London \u00b7 9 Warsaw \u00b7 10 Manchester \u00b7 11 Beirut", fr(9), GREY)
text(14, 866, "12 Gaza \u00b7 13 Khartoum", fr(9), GREY)

# ---- ALSO ----
text(340, 612, "ALSO ON MONDAY", fb(13), BLACK)
also = [
    "Paris: 100+ back 2% billionaire tax", "Manchester: 12,000 cleared",
    "Zelenskyy: 165 missiles in a week", "COP31: the day after Antalya pact rejected",
    "Israel unity talks resume", "Gaza: two killed in Israeli strike",
    "West Bank settler attacks", "Iran war: no deal in sight",
    "Lebanon seizes 264 kg explosives", "Bahrain: strike hits plant, 2 hurt",
    "Benghazi: UN demands probe [CLAIM]", "Sudan: defences down drones [CLAIM]",
    "DRC: fighting traps Ebola teams", "Bangladesh: Hasina jailed if she returns",
    "Seoul minister quits in exam row", "SK Telecom -7.3% as hype cools",
    "China eases margin rules", "Seoul readies 10T-won fund",
]
for i, item in enumerate(also):
    col, row = divmod(i, 9)
    ax = 340 + col * 340
    ay = 634 + row * 24
    n = 14 + i
    red = "[CLAIM]" in item
    text(ax, ay, f"{n}. {item}", fr(11), RED if red else BLACK)

# ---- DATE CHECK ----
d.rectangle([14, 882, 1010, 954], outline=RED, width=2)
text(24, 888, "DATE CHECK  \u2014  READ 23 NOV 2026, 23:59 UTC  \u00b7  STORIES DATED 23 NOV ONLY", fb(12), RED)
text(24, 908, "LEFT OUT \u2014 NOT 23 NOV:  Dems reach 258 (22 Nov)  \u00b7  Sparta II fire (22 Nov)  \u00b7  El Chapo Isidro captured (22 Nov)", fr(11), BLACK)
text(24, 924, "EU\u2013Indonesia pact (21 Nov)  \u00b7  Nigeria boat (21 Nov)  \u00b7  ICJ Myanmar ruling (19 Nov)", fr(11), BLACK)
text(24, 940, "NOT YET \u2014 Dymer search continues (14 missing)  \u00b7  4 House races uncalled  \u00b7  COP32 venue not set  \u00b7  WHO evacuating trapped Ebola staff", fr(11), BLACK)

# ---- footer ----
text(14, 962, "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).", fr(10), GREY)
text(14, 976, "CHIPS: REPORTED = confirmed by wires \u00b7 CLAIM = one side's claim, independently unconfirmed \u00b7 ONGOING = still developing.", fr(10), GREY)
text(14, 990, "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.", fr(10), GREY)
text(512, 1006, "THE WORLD TODAY  \u00b7  Monday 23 November 2026  \u00b7  31 stories  \u00b7  6 regions", fb(12), GOLD, anchor="ma")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out)
print("saved", out, os.path.getsize(out))
