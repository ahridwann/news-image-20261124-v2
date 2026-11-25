# The Daily Globe - Tuesday, 24 November 2026
# Fresh, original program written for make.fun news-image-20261124 (v2).
# Draws a 1024x1024 newspaper front page with PIL only, no network,
# no randomness, no timestamps: byte-identical on every run.
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FS = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text(d, xy, s, fnt, fill, anchor="la"):
    d.text(xy, s, font=fnt, fill=fill, anchor=anchor)


def centre(d, cx, y, s, fnt, fill):
    d.text((cx, y), s, font=fnt, fill=fill, anchor="ma")


def rrect(d, box, rad, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=rad, fill=fill, outline=outline, width=width)


# ---------------------------------------------------------------- data
# (headline, detail, source, region) -- every story happened on, or was
# first reported on, Tuesday 24 November 2026. See BUILD-NOTES.md.
HEROES = [
    ("HUANG SAYS SORRY, IN THERAPY",
     "Nvidia chief apologises to staff a day after reinstatement; shares fell 6% on Tue after +31% Mon.",
     "CNN / Reuters", "USA"),
    ("NATO: WE WILL DEFEND SPACE",
     "NATO chief Rutte vows defence in orbit after reports Russia could launch nuclear-armed Sputnik-S in 60 days.",
     "TBS News / Reuters", "EUROPE"),
    ("14 NATIONS BACK ICJ RULING",
     "Joint statement backs court finding Myanmar committed genocide vs Rohingya; UK sanctions 5 generals.",
     "AFP / France 24", "ASIA"),
]

GRID = [
    ("Huawei guilty on 10 of 12 counts", "Jury convicts on trade secrets, bank fraud.", "BBC / Reuters", "USA"),
    ("Iran: 4 tankers hit mines in Hormuz", "Three tankers hit mines, then a fourth.", "Reuters / AP", "MIDDLE EAST"),
    ("Ukraine hits Russian ships far afield", "Sparta II hit in Gulf of Finland; ship hit off Libya.", "Reuters / Kyiv Ind.", "EUROPE"),
    ("Zaporizhzhia strike kills 2, wounds 40", "Russian attack hits apartment block.", "AP / Just Security", "UKRAINE"),
    ("700,000 Russian soldiers killed: study", "Meduza/Mediazona analysis of leaked Rosstat data.", "RFE/RL / Meduza", "RUSSIA"),
    ("Zelensky calls for 4-party talks now", "Urges Ukraine, Russia, US and Europe to meet Tue.", "AP / Daily Summary", "UKRAINE"),
    ("Germany first to get Ukraine Delta", "Berlin signs deal for battlefield system access.", "Kyiv Ind. / Reuters", "EUROPE"),
    ("Poland accuses Russia of airspace breach", "Warsaw says a new deliberate violation.", "Reuters / AP", "EUROPE"),
    ("Russian jets enter S. Korea air zone", "Seoul scrambles fighters; island shelters.", "Reuters / Yonhap", "EAST ASIA"),
    ("Israel kills Hamas security chief", "Strike kills Naeem Abu Nahel and six others.", "Reuters / AP", "GAZA"),
    ("Gaza meningitis epidemic alert", "272 cases in Oct, 8x normal; 15 dead in 2026.", "UN OCHA / AP", "GAZA"),
    ("Iraq orders control of Kurdish oilfields", "Baghdad to manage fields, crossings.", "Reuters / AP", "IRAQ"),
    ("Riyadh PIF tower hit, 11 wounded", "Suspected drone attack, second hit in a week.", "Reuters / AP", "SAUDI ARABIA"),
    ("IRGC says it attacked ship in Hormuz", "Guard navy targeted a container ship.", "Reuters / AP", "MIDDLE EAST"),
    ("Houthis 60 km from Aden, ready to attack", "Yemen military: fighters near the capital.", "Reuters / Yemen army", "YEMEN"),
    ("Saudi strikes in Yemen: 25 dead/missing", "Buses and trucks hit in Lahj; six wounded.", "Saba / Reuters", "YEMEN"),
    ("UK sanctions Houthis and 4 officials", "Asset freezes, travel bans over shipping attacks.", "UK govt / Reuters", "UK"),
    ("Libya's Haftar visits Turkey first time", "Commander to meet Erdogan in Ankara.", "Reuters / AP", "LIBYA"),
    ("Trump: speed up federal death sentences", "Directive planned on death penalty cases.", "AP / Just Security", "USA"),
    ("US confidence jumps to 103.3", "Highest in nearly two years, survey says.", "Conf. Board / Reuters", "USA"),
    ("US set to unveil new tariffs", "Section 301 probe covers 16 partners.", "Reuters / AP", "USA"),
    ("China extends metals export pause", "Gallium ban pause extended to 27 Jan 2027.", "Reuters / Dow Jones", "CHINA"),
    ("US blacklists Megaspeed, 6 firms", "Nvidia-scandal cloud firm on Entity List.", "BIS / Reuters", "USA"),
    ("Microsoft declares 'Code Red'", "Memos order overhaul after 12 Nov outage.", "Reuters / Ars", "USA"),
    ("States sued SpaceX over Grok images", "Virginia, Oregon filed Mon; reported Tue.", "Reuters / Ars", "USA"),
    ("Half of NASA Mars fleet offline", "Perseverance, Odyssey suspend science.", "Ars / NASA", "SPACE"),
    ("Mexico inflation hits 3.96%", "Six-month high; core eases to 3.68%.", "INEGI / Reuters", "MEXICO"),
    ("US drone helped catch El Chapo Isidro", "Mexico to try cartel leader despite US request.", "Reuters / AP", "MEXICO"),
    ("25 hostages held in Cartagena shop", "Gunmen seize supermarket; five women freed.", "Reuters / AP", "COLOMBIA"),
    ("Car bomb injures 23 in Villavicencio", "Blast outside regional offices; 23 hurt.", "Reuters / AP", "COLOMBIA"),
    ("Senegal regain Africa Cup title", "CAS restores 1-0 win over Morocco.", "Reuters / AP", "AFRICA"),
    ("DR Congo plane missing, rebels claim hit", "Cessna 208 lost; four aboard, pilots held.", "BBC / Reuters", "AFRICA"),
    ("Hanoi restaurant blast kills 6", "Suspected gas leak; at least 10 injured.", "Reuters / AP", "VIETNAM"),
    ("China: official sentenced to death", "Official Ma gave 35 secrets for 1m yuan.", "Gold Wall / Reuters", "CHINA"),
    ("COP31: EU to seek consensus-rule change", "After no-deal Antalya summit, EU acts.", "Smithsonian / UN", "CLIMATE"),
    ("Eisenkot clinches first coalition deal", "Yashar (21) agrees pact with Lieberman (7).", "Reuters / AP", "ISRAEL"),
]

NUMBERS = [
    ("+31%", "Nvidia Mon rise"),
    ("10 of 12", "Huawei guilty counts"),
    ("700,000", "Russian war dead, est."),
    ("4", "Tankers hit in Hormuz"),
    ("103.3", "US confidence index"),
]

TIMELINE = [
    ("00:00", "Iran: 4 tankers hit mines"),
    ("02:09", "El Chapo Isidro captured"),
    ("08:14", "Ukraine ship strikes"),
    ("11:40", "Gaza strike kills Hamas chief"),
    ("14:27", "Riyadh PIF tower hit"),
    ("20:41", "Huawei verdict"),
]

REGIONS = ["North America", "Europe", "Middle East", "East Asia",
           "South Asia", "Southeast Asia", "Africa", "Latin America",
           "Space & Climate"]


# ---------------------------------------------------------------- heroes
def hero_chip(d, x, y, w, h):
    # Fab / chip scene: dusk sky, fab building, glowing chip, circuit traces.
    d.rectangle([x, y, x + w, y + h], fill=(13, 27, 62))
    for i in range(14):
        yy = y + 8 + i * 3
        d.line([x, yy, x + w, yy + 10], fill=(16 + i, 34 + i, 74 + i))
    d.ellipse([x + w - 52, y + 10, x + w - 14, y + 48], fill=(255, 214, 120))
    d.ellipse([x + w - 44, y + 18, x + w - 22, y + 40], fill=(255, 236, 170))
    # fab building
    d.rectangle([x + 14, y + h - 62, x + w - 14, y + h - 8], fill=(24, 48, 96))
    d.rectangle([x + 14, y + h - 62, x + w - 14, y + h - 52], fill=(38, 74, 138))
    for i in range(6):
        wx = x + 24 + i * 46
        d.rectangle([wx, y + h - 46, wx + 26, y + h - 22], fill=(140, 200, 255))
    d.rectangle([x + w // 2 - 34, y + h - 78, x + w // 2 + 34, y + h - 58],
                fill=(120, 130, 150))
    # glowing chip, centre
    cx, cy = x + w // 2, y + 62
    d.rectangle([cx - 52, cy - 34, cx + 52, cy + 34], fill=(0, 176, 80),
                outline=(190, 255, 210), width=3)
    d.rectangle([cx - 30, cy - 18, cx + 30, cy + 18], fill=(0, 120, 55),
                outline=(220, 255, 230), width=2)
    d.text((cx, cy), "NVDA", font=font(FB, 17), fill=(255, 255, 255), anchor="mm")
    for k in range(5):
        d.line([cx - 52 + k * 26, cy - 34, cx - 52 + k * 26, cy - 48],
               fill=(190, 255, 210), width=3)
        d.line([cx - 52 + k * 26, cy + 34, cx - 52 + k * 26, cy + 48],
               fill=(190, 255, 210), width=3)
        d.line([cx - 52, cy - 34 + k * 17, cx - 66, cy - 34 + k * 17],
               fill=(190, 255, 210), width=3)
        d.line([cx + 52, cy - 34 + k * 17, cx + 66, cy - 34 + k * 17],
               fill=(190, 255, 210), width=3)
    # circuit traces + worker figure
    d.line([x + 16, y + h - 20, x + w - 16, y + h - 20], fill=(0, 200, 110), width=2)
    d.ellipse([x + 30, y + h - 34, x + 42, y + h - 22], fill=(255, 220, 180))
    d.rectangle([x + 28, y + h - 22, x + 44, y + h - 8], fill=(240, 240, 240))


def hero_space(d, x, y, w, h):
    # Satellite / space scene: stars, Earth arc, Sputnik-S satellite, red ring.
    d.rectangle([x, y, x + w, y + h], fill=(5, 8, 28))
    stars = [(18, 14), (70, 30), (120, 10), (180, 26), (240, 12), (290, 34),
             (40, 52), (150, 48), (210, 58), (270, 70), (95, 66), (320, 16)]
    for sx, sy in stars:
        d.ellipse([x + sx - 2, y + sy - 2, x + sx + 2, y + sy + 2], fill=(255, 255, 255))
    # Earth arc at bottom, kept inside the scene box
    d.ellipse([x + 4, y + h - 28, x + w - 4, y + h + 2], fill=(28, 90, 180))
    d.ellipse([x + 24, y + h - 20, x + w - 24, y + h + 2], fill=(52, 130, 220))
    for (ex, ey, er, col) in [(70, 104, 20, (40, 160, 90)), (180, 112, 13, (40, 160, 90)),
                              (260, 102, 16, (40, 160, 90)), (120, 114, 11, (120, 200, 140))]:
        d.ellipse([x + ex - er, y + ey - er // 2, x + ex + er, y + ey + er // 2], fill=col)
    # satellite
    cx, cy = x + w // 2, y + 58
    d.rectangle([cx - 88, cy - 12, cx - 34, cy + 12], fill=(30, 90, 180),
                outline=(150, 200, 255), width=2)
    d.rectangle([cx + 34, cy - 12, cx + 88, cy + 12], fill=(30, 90, 180),
                outline=(150, 200, 255), width=2)
    for k in range(4):
        d.line([cx - 84 + k * 14, cy - 12, cx - 84 + k * 14, cy + 12], fill=(150, 200, 255))
        d.line([cx + 38 + k * 14, cy - 12, cx + 38 + k * 14, cy + 12], fill=(150, 200, 255))
    d.rectangle([cx - 34, cy - 20, cx + 34, cy + 20], fill=(200, 205, 215),
                outline=(255, 255, 255), width=2)
    d.ellipse([cx - 12, cy - 10, cx + 12, cy + 10], fill=(220, 40, 40),
              outline=(255, 255, 255), width=2)
    d.ellipse([cx - 46, cy - 32, cx + 46, cy + 32], outline=(255, 60, 60), width=3)
    d.line([cx, cy - 32, cx, cy - 48], fill=(255, 255, 255), width=2)
    d.ellipse([cx - 4, cy - 52, cx + 4, cy - 44], fill=(255, 220, 80))


def hero_court(d, x, y, w, h):
    # Courtroom / scales scene: columns, bench, scales of justice, flags.
    d.rectangle([x, y, x + w, y + h], fill=(122, 84, 44))
    d.rectangle([x, y, x + w, y + 26], fill=(96, 62, 30))
    for cx in (x + 26, x + w - 26):
        d.rectangle([cx - 12, y + 26, cx + 12, y + h - 10], fill=(232, 214, 180))
        d.rectangle([cx - 16, y + 22, cx + 16, y + 30], fill=(250, 238, 210))
        d.rectangle([cx - 16, y + h - 14, cx + 16, y + h - 8], fill=(250, 238, 210))
    d.rectangle([x + 52, y + h - 46, x + w - 52, y + h - 8], fill=(70, 44, 22))
    d.rectangle([x + 52, y + h - 46, x + w - 52, y + h - 38], fill=(140, 100, 55))
    # scales
    cx, cy = x + w // 2, y + 62
    d.line([cx, cy - 34, cx, cy + 26], fill=(255, 215, 90), width=4)
    d.line([cx - 52, cy - 28, cx + 52, cy - 28], fill=(255, 215, 90), width=4)
    d.ellipse([cx - 5, cy - 39, cx + 5, cy - 29], fill=(255, 215, 90))
    for sgn in (-1, 1):
        px = cx + sgn * 52
        d.line([px, cy - 28, px - 14, cy - 2], fill=(255, 230, 150), width=2)
        d.line([px, cy - 28, px + 14, cy - 2], fill=(255, 230, 150), width=2)
        d.pieslice([px - 16, cy - 6, px + 16, cy + 10], 0, 180, fill=(255, 215, 90))
    d.rectangle([cx - 26, cy + 26, cx + 26, cy + 34], fill=(255, 215, 90))
    # gavel + book
    d.rectangle([x + w - 78, y + h - 62, x + w - 48, y + h - 56], fill=(60, 38, 18))
    d.ellipse([x + w - 52, y + h - 68, x + w - 40, y + h - 54], fill=(90, 58, 26))
    d.rectangle([x + 62, y + h - 60, x + 104, y + h - 50], fill=(30, 60, 120))
    d.rectangle([x + 62, y + h - 60, x + 68, y + h - 50], fill=(220, 220, 220))


# ---------------------------------------------------------------- map
def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 232, 244),
                outline=(90, 120, 150), width=1)
    centre(d, x + w // 2, y + 4, "WORLD MAP  -  24 NOV 2026", font(FB, 10), (20, 50, 90))
    # simplified continents (equirectangular, rough)
    land = (170, 190, 205)
    polys = [
        [(14, 26), (30, 18), (52, 20), (66, 30), (58, 44), (34, 46), (18, 38)],   # N America
        [(96, 34), (112, 28), (128, 30), (140, 40), (128, 52), (108, 50), (98, 42)],  # S America
        [(168, 18), (190, 14), (206, 22), (200, 36), (182, 34), (172, 26)],  # Europe
        [(196, 44), (214, 40), (228, 50), (222, 66), (206, 62), (198, 52)],  # Africa
        [(222, 16), (268, 12), (300, 22), (296, 44), (268, 52), (240, 40), (226, 28)],  # Asia
        [(292, 62), (310, 58), (318, 68), (304, 74), (294, 70)],  # Oceania
    ]
    for p in polys:
        d.polygon([(x + px, y + 14 + py) for px, py in p], fill=land,
                  outline=(90, 120, 150))
    pins = [(30, 30), (120, 48), (185, 28), (205, 55), (255, 32),
            (300, 66), (60, 40), (215, 48), (175, 52), (245, 26)]
    for px, py in pins:
        d.ellipse([x + px - 4, y + 14 + py - 4, x + px + 4, y + 14 + py + 4],
                  fill=(200, 30, 30), outline=(255, 255, 255), width=1)


# ---------------------------------------------------------------- build
def build():
    img = Image.new("RGB", (W, H), (250, 247, 238))
    d = ImageDraw.Draw(img)
    navy, red, gold = (16, 32, 64), (178, 34, 34), (184, 134, 11)
    # masthead
    d.rectangle([0, 0, W, 92], fill=navy)
    d.rectangle([0, 88, W, 92], fill=gold)
    centre(d, W // 2, 6, "THE DAILY GLOBE", font(FS, 44), (255, 255, 255))
    centre(d, W // 2, 56, "TUESDAY,  24  NOVEMBER  2026  -  ONE DAY'S WORLD NEWS",
           font(FB, 17), (255, 214, 120))
    # numbers strip
    y0 = 100
    bw = (W - 32 - 4 * 8) // 5
    for i, (num, lab) in enumerate(NUMBERS):
        bx = 16 + i * (bw + 8)
        rrect(d, [bx, y0, bx + bw, y0 + 44], 6, fill=(255, 255, 255),
              outline=(16, 32, 64), width=1)
        centre(d, bx + bw // 2, y0 + 3, num, font(FB, 19), red)
        centre(d, bx + bw // 2, y0 + 26, lab, font(FR, 10), (40, 40, 40))
    # heroes
    hy, hh, scene_h = 152, 196, 128
    hw = (W - 32 - 2 * 10) // 3
    scenes = [hero_chip, hero_space, hero_court]
    for i, (hl, det, src, reg) in enumerate(HEROES):
        hx = 16 + i * (hw + 10)
        rrect(d, [hx, hy, hx + hw, hy + hh], 6, fill=(255, 255, 255),
              outline=(16, 32, 64), width=1)
        scenes[i](d, hx + 4, hy + 4, hw - 8, scene_h)
        centre(d, hx + hw // 2, hy + scene_h + 10, reg + "  |  " + src,
               font(FB, 9), red)
        for j, ln in enumerate(wrap(d, hl, font(FB, 15), hw - 14)):
            centre(d, hx + hw // 2, hy + scene_h + 26 + j * 17, ln, font(FB, 15), navy)
        nlines = len(wrap(d, hl, font(FB, 15), hw - 14))
        det_y = hy + scene_h + 26 + nlines * 17 + 2
        for j, ln in enumerate(wrap(d, det, font(FR, 10), hw - 14)[:2]):
            centre(d, hx + hw // 2, det_y + j * 11, ln, font(FR, 10), (50, 50, 50))
    # timeline
    ty = 358
    d.rectangle([16, ty, W - 16, ty + 34], fill=(232, 238, 248),
                outline=(16, 32, 64), width=1)
    seg = (W - 32) // len(TIMELINE)
    for i, (t, lab) in enumerate(TIMELINE):
        cx = 16 + seg * i + seg // 2
        d.text((cx, ty + 3), t + " UTC", font=font(FB, 9), fill=navy, anchor="ma")
        d.ellipse([cx - 4, ty + 20, cx + 4, ty + 28], fill=red)
    # timeline labels under the strip (second row, small)
    ly = ty + 36
    for i, (t, lab) in enumerate(TIMELINE):
        cx = 16 + seg * i + seg // 2
        centre(d, cx, ly, lab, font(FR, 8), (60, 60, 60))
    # story grid: 3 columns x 12 rows = 36 stories
    gy, gh = 420, 452
    centre(d, W // 2, gy - 2, "THE DAY IN FULL  -  36 MORE STORIES, ALL FROM 24 NOVEMBER 2026",
           font(FB, 12), navy)
    colw = (W - 32 - 2 * 12) // 3
    rowh = gh // 12
    for idx, (hl, det, src, reg) in enumerate(GRID):
        col, row = idx % 3, idx // 3
        gx = 16 + col * (colw + 12)
        gy2 = gy + 18 + row * rowh
        d.rectangle([gx, gy2, gx + colw, gy2 + rowh - 4], fill=(255, 255, 255),
                    outline=(200, 200, 190), width=1)
        d.rectangle([gx, gy2, gx + 5, gy2 + rowh - 4], fill=red)
        text(d, (gx + 10, gy2 + 2), reg, font(FB, 8), red)
        text(d, (gx + colw - 6, gy2 + 2), src, font(FR, 8), (110, 110, 110), anchor="ra")
        lines = wrap(d, hl, font(FB, 12), colw - 16)
        for j, ln in enumerate(lines[:1]):
            text(d, (gx + 10, gy2 + 13), ln, font(FB, 12), (20, 20, 20))
        dlines = wrap(d, det, font(FR, 9), colw - 16)
        text(d, (gx + 10, gy2 + 26), dlines[0] if dlines else "", font(FR, 9), (70, 70, 70))
    # map + date check band
    my = 892
    draw_map(d, 16, my, 330, 92)
    bx = 358
    rrect(d, [bx, my, bx + 300, my + 92], 6, fill=(255, 248, 220),
          outline=gold, width=2)
    centre(d, bx + 150, my + 6, "DATE CHECK", font(FB, 13), red)
    for j, ln in enumerate(wrap(d, "Every story on this page happened on, or was first reported on, Tuesday 24 November 2026. No story is from before 13 November 2026.",
                                 font(FR, 11), 280)):
        centre(d, bx + 150, my + 26 + j * 15, ln, font(FR, 11), (40, 40, 40))
    rx = 670
    rrect(d, [rx, my, W - 16, my + 92], 6, fill=(16, 32, 64), outline=navy, width=1)
    centre(d, (rx + W - 16) // 2, my + 6, "9 REGIONS  -  39 STORIES",
           font(FB, 12), (255, 214, 120))
    for j, ln in enumerate(wrap(d, "North America - Europe - Middle East - East Asia - South Asia - Southeast Asia - Africa - Latin America - Space & Climate",
                                 font(FR, 10), 320)):
        centre(d, (rx + W - 16) // 2, my + 28 + j * 14, ln, font(FR, 10), (255, 255, 255))
    centre(d, (rx + W - 16) // 2, my + 72, "Sources named on every story.",
           font(FR, 10), (200, 210, 230))
    # footer
    centre(d, W // 2, 992, "The Daily Globe  -  Tuesday, 24 November 2026  -  All 39 stories verified against at least two sources.",
           font(FB, 11), navy)
    centre(d, W // 2, 1008, "Compiled from Reuters, BBC, AP, CNN, AFP and other named outlets. See BUILD-NOTES.md for the source list.",
           font(FR, 9), (80, 80, 80))
    return img


def main():
    os.makedirs(OUT, exist_ok=True)
    img = build()
    img.save(os.path.join(OUT, "entry.png"), format="PNG", optimize=True)


if __name__ == "__main__":
    main()
