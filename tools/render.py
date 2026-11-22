#!/usr/bin/env python3
"""Qalb Mousafir — moteur de rendu piloté par JSON (format : docs/SCHEMA.md).

Usage :
    python3 render.py chemin/epN.json            # rendu complet -> out/<slug>/<slug>.mp4
    python3 render.py chemin/epN.json --preview  # 1 JPEG par scène + planche contact
    python3 render.py chemin/epN.json --only 3 5 # ne rend que les scènes 3 et 5 (pas de montage final)

Look identique à le moteur de l'épisode 1 : mêmes couleurs, fond, rosace, étoiles,
animations, mise en page centrée automatique, décalage CX vers la gauche.
"""
import argparse, gc, hashlib, json, math, multiprocessing as mp, os, random, subprocess, sys, time
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1080, 1920, 30

FONTS = os.environ.get("QM_FONTS", os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts"))
AMIRI = os.path.join(FONTS, "Amiri-Bold.ttf")
AMIRI_R = os.path.join(FONTS, "Amiri-Regular.ttf")
INTER = os.path.join(FONTS, "Inter-%s.otf")
SERIF = os.path.join(FONTS, "CrimsonText-%s.ttf")

_MODELS = os.environ.get("QM_MODELS", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models"))
TTS_MODEL = os.path.join(_MODELS, "kokoro.onnx")
TTS_VOICES = os.path.join(_MODELS, "voices.bin")
TTS_VOICE, TTS_SPEED, TTS_LANG = "ff_siwis", 0.97, "fr-fr"
TTS_CACHE = os.path.join(HERE, "cache", "tts")
VOICE_DELAY = 0.3      # la voix démarre 0,3 s après le début de la scène
VOICE_TAIL = 1.0       # durée scène >= durée voix + 1,0 s
AUDIO_FILTER = "highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=5:release=80,loudnorm=I=-15:TP=-1.5:LRA=9"

GOLD = (226, 189, 112)
GOLD_SOFT = (200, 170, 110)
CREAM = (246, 238, 222)
MUTED = (178, 190, 214)

# Durée de scène = max(minimum, voix + VOICE_TAIL). Minimum bas par défaut (3,5 s) ; surcharge possible
# dans le JSON : "timing": {"min_scene": 3.5, "tail": 1.0, "min_by_type": {"step": 6.3, ...}}
# ou "duration" sur une scène. make.py utilisait {"hook": 4.2, "quote": 6.0, "step": 6.3, "recap": 6.0, "outro": 5.0}.
MIN_SCENE = 3.5
VISIBLE_BEFORE_END = 1.5   # tout doit être affiché (fondu fini) au moins 1,5 s avant la fin de la scène
FADE_IN = 0.6

_fc = {}
def F(path, size):
    k = (path, size)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(path, size, layout_engine=ImageFont.Layout.RAQM)
    return _fc[k]

def is_ar(s):
    return any('؀' <= c <= 'ۿ' or 'ﭐ' <= c <= '﷿' or 'ﹰ' <= c <= '﻿' for c in s)

# ---------- text rendering ----------
# Ponctuation française qui ne doit jamais commencer une ligne ; « ( n° ne doivent jamais finir une ligne ;
# un nombre reste avec le mot suivant (« 3 rak'at », « 5 prières ») ; ﷺ reste collé au nom qui le précède.
_PUNCT = set(":;!?%»….,)]€$")
def _glue_prev(w): return w == "ﷺ" or (w != "" and all(c in _PUNCT for c in w))
def _glue_next(w): return w in ("«", "(", "[") or w.endswith("n°") or (w.isdigit() and len(w) <= 4)

def _units(words):
    """Groupe les mots insécables ; une unité = liste de mots."""
    units = []
    glue_next = False
    for w in words:
        prev_ok = units and (w == "ﷺ" or (not is_ar(w) and not is_ar(units[-1][-1])))
        if prev_ok and (glue_next or _glue_prev(w)):
            units[-1].append(w)
        else:
            units.append([w])
        glue_next = _glue_next(w)
    return units

def text_block(text, font_path, size, color, max_w=860, line_gap=1.28, ar_size=None, align="center", shadow=True,
               no_orphan=False):
    """Word-wrapped block; words containing Arabic are drawn in Amiri (identique à make.py,
    + ponctuation insécable ; no_orphan=True évite un mot seul sur la dernière ligne)."""
    fl = F(font_path, size)
    fa = F(AMIRI, ar_size or int(size * 1.15))
    paras = text.split("\n")
    if len(paras) > 1:          # retour à la ligne forcé : un bloc par paragraphe, empilés
        imgs = [text_block(p_.strip(), font_path, size, color, max_w, line_gap, ar_size, align, False, no_orphan) for p_ in paras]
        lh = int(size * line_gap)
        bw = max(i.width for i in imgs)
        img = Image.new("RGBA", (bw, sum(i.height for i in imgs) - (len(imgs) - 1) * (int(size * 0.5))), (0, 0, 0, 0))
        y = 0
        for i in imgs:
            img.alpha_composite(i, ((bw - i.width) // 2, y)); y += i.height - int(size * 0.5)
        return add_shadow(img) if shadow else img
    words = [w for w in text.split(" ") if w != ""]
    def wfont(w): return fa if is_ar(w) else fl
    def wlen(w):
        f = wfont(w)
        return f.getlength(w, direction="rtl" if is_ar(w) else None)
    space = fl.getlength(" ")
    def ulen(u): return sum(wlen(w) for w in u) + space * (len(u) - 1)
    lines, cur, cw = [], [], 0
    for u in _units(words):
        lw = ulen(u)
        if cur and cw + space + lw > max_w:
            lines.append((cur, cw)); cur, cw = list(u), lw
        else:
            cw = cw + (space if cur else 0) + lw; cur.extend(u)
    if cur: lines.append((cur, cw))
    if no_orphan and len(lines) >= 2:
        us = [_units(l[0]) for l in lines]
        if len(us[-1]) == 1 and len(us[-2]) >= 3:
            mv = us[-2][-1]
            last = mv + us[-1][0]
            lw = ulen(last)
            if lw <= max_w:
                prev = [w for u in us[-2][:-1] for w in u]
                pw = sum(wlen(w) for w in prev) + space * (len(prev) - 1)
                lines[-2], lines[-1] = (prev, pw), (last, lw)
    lh = int(size * line_gap)
    bw = int(max(l[1] for l in lines)) + 40
    bh = lh * len(lines) + int(size * 0.5)
    img = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    asc = fl.getmetrics()[0]
    for i, (ws, lwid) in enumerate(lines):
        x = (bw - lwid) / 2 if align == "center" else 20
        y = i * lh + 10
        for w in ws:
            f = wfont(w)
            dy = 0
            if f is fa:
                dy = asc - fa.getmetrics()[0] + int(size * 0.12)
            d.text((x, y + dy), w, font=f, fill=color + (255,), direction="rtl" if is_ar(w) else None)
            x += wlen(w) + space
    return add_shadow(img) if shadow else img

def arabic(text, size, color=GOLD, font=AMIRI, glow=True):
    f = F(font, size)
    l, t, r, b = f.getbbox(text, direction="rtl")
    pad = int(size * 0.35)
    img = Image.new("RGBA", (r - l + 2 * pad, b - t + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(img).text((pad - l, pad - t), text, font=f, fill=color + (255,), direction="rtl")
    if glow:
        g = img.getchannel("A").filter(ImageFilter.GaussianBlur(size * 0.12))
        g = g.point(lambda v: int(v * 0.55))
        glow_img = Image.new("RGBA", img.size, GOLD + (0,)); glow_img.putalpha(g)
        img = Image.alpha_composite(glow_img, img)
    return img

def arabic_lines(lines, size, color=GOLD, font=AMIRI, glow=True, pitch=1.6):
    """Plusieurs lignes arabes (ordre logique : 1re ligne en haut), centrées, lignes de base régulières."""
    f = F(font, size)
    boxes = [f.getbbox(ln, direction="rtl", anchor="ms") for ln in lines]
    lh = int(size * pitch)
    pad = int(size * 0.35)
    bw = max(r - l for l, t, r, b in boxes) + 2 * pad
    top = min(t + k * lh for k, (l, t, r, b) in enumerate(boxes))
    bot = max(b + k * lh for k, (l, t, r, b) in enumerate(boxes))
    img = Image.new("RGBA", (bw, bot - top + 2 * pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for k, (ln, (l, t, r, b)) in enumerate(zip(lines, boxes)):
        x = bw / 2 - (l + r) / 2
        d.text((x, pad - top + k * lh), ln, font=f, fill=color + (255,), direction="rtl", anchor="ms")
    if glow:
        g = img.getchannel("A").filter(ImageFilter.GaussianBlur(size * 0.12))
        g = g.point(lambda v: int(v * 0.55))
        glow_img = Image.new("RGBA", img.size, GOLD + (0,)); glow_img.putalpha(g)
        img = Image.alpha_composite(glow_img, img)
    return img

def _split_balanced(words, k, wd):
    """Découpe des mots en k lignes en minimisant la ligne la plus large (programmation dynamique)."""
    n = len(words)
    memo = {}
    def best(i, k):
        if (i, k) in memo: return memo[(i, k)]
        if k == 1:
            r = (wd(" ".join(words[i:])), [" ".join(words[i:])])
        else:
            r = (float("inf"), None)
            for j in range(i + 1, n - k + 2):
                w1 = wd(" ".join(words[i:j]))
                if w1 >= r[0]: break
                sub = best(j, k - 1)
                m = max(w1, sub[0])
                if m < r[0]: r = (m, [" ".join(words[i:j])] + sub[1])
        memo[(i, k)] = r
        return r
    return best(0, k)

def arabic_fit(text, size, max_w=860, min_scale=0.8, max_lines=1, wrap_min_scale=0.62, **kw):
    """Arabe qui tient dans max_w :
    1) une ligne à la taille demandée (identique à make.py) ;
    2) une ligne réduite jusqu'à min_scale ;
    3) si max_lines > 1 : 2..max_lines lignes équilibrées, taille réduite si besoin
       (on prend le moins de lignes possible tant que la taille reste >= 0,8×) ;
    4) sinon une ligne réduite autant que nécessaire."""
    font = kw.get("font", AMIRI)
    def wd_at(s):
        f = F(font, s)
        def wd(t):
            l, _, r, _ = f.getbbox(t, direction="rtl"); return r - l
        return wd
    w0 = wd_at(size)(text)
    if w0 <= max_w:
        return arabic(text, size, **kw)
    s1 = int(size * max_w / w0)
    if s1 >= size * min_scale or max_lines <= 1:
        while s1 > 10 and wd_at(s1)(text) > max_w: s1 -= 1
        return arabic(text, s1, **kw)
    words = text.split()
    wd = wd_at(size)
    opts = []
    for k in range(2, min(max_lines, len(words)) + 1):
        m, lines = _split_balanced(words, k, wd)
        sk = min(size, int(size * max_w / m))
        opts.append((k, sk, lines))
        if sk >= size * 0.8: break
    k, sk, lines = max(opts, key=lambda o: (o[1] >= size * 0.8, -o[0] if o[1] >= size * 0.8 else o[1]))
    sk = max(sk, int(size * wrap_min_scale))
    kw2 = {k_: v for k_, v in kw.items() if k_ in ("color", "font", "glow")}
    return arabic_lines(lines, sk, **kw2)

def add_shadow(img, r=6, op=0.6):
    a = img.getchannel("A").filter(ImageFilter.GaussianBlur(r)).point(lambda v: int(v * op))
    s = Image.new("RGBA", img.size, (5, 8, 20, 0)); s.putalpha(a)
    return Image.alpha_composite(s, img)

def line_ornament(w=420):
    img = Image.new("RGBA", (w, 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    c = w // 2
    d.line((20, 20, c - 26, 20), fill=GOLD_SOFT + (200,), width=2)
    d.line((c + 26, 20, w - 20, 20), fill=GOLD_SOFT + (200,), width=2)
    star(d, c, 20, 13, 6, GOLD + (255,))
    return img

def star(d, cx, cy, R, r, fill, n=8, rot=0):
    pts = []
    for i in range(2 * n):
        ang = rot + math.pi * i / n - math.pi / 2
        rad = R if i % 2 == 0 else r
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(pts, fill=fill)

def progress(k, total=5):
    """total points (3..10), k = courant (1..total). Pas de 70 px comme make.py (700 px max à 10)."""
    step = 70 if total <= 10 else int(700 / total)
    img = Image.new("RGBA", (total * step, 50), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for i in range(total):
        cx = step // 2 + i * step
        if i + 1 == k:
            star(d, cx, 25, 20, 9, GOLD + (255,))
        elif i + 1 < k:
            d.ellipse((cx - 8, 17, cx + 8, 33), fill=GOLD_SOFT + (230,))
        else:
            d.ellipse((cx - 8, 17, cx + 8, 33), outline=MUTED + (160,), width=2)
    return img

def pill(text, size=34):
    f = F(INTER % "SemiBold", size)
    tw = f.getlength(text)
    img = Image.new("RGBA", (int(tw) + 70, size + 34), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((1, 1, img.width - 2, img.height - 2), radius=img.height // 2,
                        outline=GOLD + (220,), width=2, fill=(20, 28, 55, 150))
    d.text((35, 15), text, font=f, fill=GOLD + (255,))
    return img

# ---------- background (identique à make.py) ----------
rng = random.Random(7)
top, bot = np.array([7, 12, 32], float), np.array([28, 30, 62], float)
yy = np.linspace(0, 1, H)[:, None, None]
grad = (top * (1 - yy) + bot * yy) * np.ones((1, W, 1))
gy, gx = np.mgrid[0:H, 0:W]
glow = np.exp(-(((gx - W / 2) / 700) ** 2 + ((gy - H * 1.05) / 520) ** 2))
grad += glow[..., None] * np.array([70, 45, 20])
BG = Image.fromarray(np.clip(grad, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
del yy, grad, gy, gx, glow

STARS = [(rng.uniform(0, W), rng.uniform(0, H * 0.85), rng.uniform(0.8, 2.4), rng.uniform(0, 6.28), rng.uniform(0.6, 1.8)) for _ in range(140)]

def rosette(size=1500):
    s = size
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    c = s / 2
    col = GOLD + (34,)
    for R in (690, 560, 430, 300):
        for k in range(2):
            rot = k * math.pi / 4
            pts = [(c + R * math.cos(rot + i * math.pi / 2), c + R * math.sin(rot + i * math.pi / 2)) for i in range(4)]
            d.polygon(pts, outline=col, width=2)
        d.ellipse((c - R * 0.71, c - R * 0.71, c + R * 0.71, c + R * 0.71), outline=GOLD + (18,), width=2)
    for i in range(16):
        a = i * math.pi / 8
        d.line((c, c, c + 690 * math.cos(a), c + 690 * math.sin(a)), fill=GOLD + (12,), width=1)
    return img
ROS = rosette()

try:
    import cv2
    cv2.setNumThreads(1)          # 1 thread par processus : le parallélisme se fait par scène
    _ROS_NP = np.ascontiguousarray(np.asarray(ROS))
except Exception:                 # pas d'OpenCV : chemin PIL (identique à make.py)
    cv2 = None
EXACT_BG = os.environ.get("QM_EXACT_BG") == "1"

def _rosette_layer(t):
    """Rosette tournée, seulement la zone visible. OpenCV (≈3× plus rapide) : écart max 11/255 sur
    les traits très fins, mêmes positions ; QM_EXACT_BG=1 => PIL.rotate, pixel-identique à make.py."""
    s = ROS.width
    px, py = W // 2 - s // 2, int(H * 0.42) - s // 2
    if EXACT_BG or cv2 is None:
        return ROS.rotate(t * 2.2, resample=Image.BICUBIC), (px, py)
    ox, oy = max(0, -px), max(0, -py)
    cw, ch = min(s - ox, W - px - ox), min(s - oy, H - py - oy)
    ang = -math.radians(t * 2.2)
    a, b = math.cos(ang), math.sin(ang)
    d, e = -b, a
    c = -a * s / 2 - b * s / 2 + s / 2
    f = -d * s / 2 - e * s / 2 + s / 2
    # même matrice inverse que PIL.rotate, convention centre de pixel de PIL
    M = np.array([[a, b, a * (ox + 0.5) + b * (oy + 0.5) + c - 0.5],
                  [d, e, d * (ox + 0.5) + e * (oy + 0.5) + f - 0.5]])
    out = cv2.warpAffine(_ROS_NP, M, (cw, ch), flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP,
                         borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    return Image.fromarray(out, "RGBA"), (px + ox, py + oy)

def background(t):
    img = BG.copy()
    r, pos = _rosette_layer(t)
    img.alpha_composite(r, pos)
    d = ImageDraw.Draw(img)
    for x, y, rad, ph, sp in STARS:
        a = 0.45 + 0.55 * math.sin(t * sp + ph)
        v = int(255 * max(0, a) * 0.8)
        d.ellipse((x - rad, y - rad, x + rad, y + rad), fill=(255, 245, 225, v))
    return img

# ---------- animation helpers (identiques à make.py) ----------
def ease(x):
    x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3

def put(frame, el, cx, y, lt, t_in, dur, fade_in=0.6, out_at=None, fade_out=0.35, rise=40):
    if lt < t_in: return
    a = ease((lt - t_in) / fade_in)
    if out_at is not None and lt > out_at:
        a *= max(0.0, 1 - (lt - out_at) / fade_out)
    if a <= 0.01: return
    dy = int((1 - a) * rise) if lt - t_in < fade_in else 0
    e = el
    if a < 0.999:
        e = el.copy(); e.putalpha(el.getchannel("A").point(lambda v: int(v * a)))
    frame.alpha_composite(e, (int(cx - el.width / 2), int(y + dy)))

CX = W // 2 - 20  # décalage à gauche des boutons TikTok

# ---------- scènes (look de make.py, pilotées par JSON) ----------
def _s(sc, k, default=""):
    v = sc.get(k, default)
    return "" if v is None else str(v)

def scene_hook(sc):
    els = []
    if _s(sc, "pill"): els.append((pill(_s(sc, "pill")), 0, 0.1))
    if _s(sc, "arabic"): els.append((arabic_fit(_s(sc, "arabic"), 160, min_scale=0.6), 10, 0.4))
    if _s(sc, "title"): els.append((text_block(_s(sc, "title"), SERIF % "SemiBold", 100, CREAM, max_w=900, no_orphan=True), -10, 0.9))
    els.append((line_ornament(), 40, 1.3))
    if _s(sc, "subtitle"): els.append((text_block(_s(sc, "subtitle"), INTER % "Medium", 54, MUTED, no_orphan=True), 30, 1.6))
    return els

def _sentence_break(text, font_path, size, max_w):
    """Si le texte ne tient pas sur une ligne, coupe de préférence après une fin de phrase
    (. ? ! suivi éventuellement de ») quand chaque morceau tient sur une ligne."""
    if "\n" in text or F(font_path, size).getlength(text) <= max_w:
        return text
    import re
    for m in reversed(list(re.finditer(r"[.?!…]( »)? ", text))):
        a, b = text[:m.end()].strip(), text[m.end():].strip()
        if a and b and all(F(font_path, size).getlength(x) <= max_w for x in (a, b)):
            return a + "\n" + b
    return text

QUOTE_MAX_H = 1360   # hauteur max du bloc citation (≈ y 220 → 1580, centré sur 900)

def scene_quote(sc):
    """Citation : arabe sur 1 à 4 lignes (≤ 860 px), traduction multi-lignes ; si le tout est trop haut,
    on réduit progressivement l'arabe et la traduction."""
    for ar_size, tr_size, intro_size in ((108, 68, 48), (100, 64, 46), (92, 60, 44), (84, 56, 42), (76, 52, 40)):
        els = []
        if _s(sc, "intro"):
            els.append((text_block(_sentence_break(_s(sc, "intro"), INTER % "Medium", intro_size, 940), INTER % "Medium",
                                   intro_size, MUTED, max_w=940, ar_size=int(intro_size * 74 / 48), no_orphan=True), 0, 0.2))
        if _s(sc, "arabic"): els.append((arabic_fit(_s(sc, "arabic"), ar_size, max_w=860, max_lines=4), 10, 0.6))
        if _s(sc, "translation"):
            els.append((text_block(_s(sc, "translation"), SERIF % "Italic", tr_size, CREAM, max_w=960, no_orphan=True), 0, 1.4))
        els.append((line_ornament(), 40, 2.0))
        if _s(sc, "source"):
            els.append((text_block(_s(sc, "source"), INTER % "Regular", 40, GOLD_SOFT, max_w=960, no_orphan=True), 20, 2.2))
        if sum(el.height + g for el, g, _ in els) <= QUOTE_MAX_H:
            break
    return els

def scene_step(sc):
    idx, total = int(sc.get("index", 1)), int(sc.get("total", 5))
    label = _s(sc, "label", "ÉTAPE") or "ÉTAPE"
    els = [(progress(idx, total), 0, 0.0),
           (text_block(f"{label} {idx} / {total}", INTER % "SemiBold", 38, GOLD_SOFT, shadow=False), 20, 0.15)]
    if _s(sc, "arabic"): els.append((arabic_fit(_s(sc, "arabic"), 220, max_w=820, min_scale=0.5), -10, 0.35))
    if _s(sc, "title"): els.append((text_block(_s(sc, "title"), SERIF % "SemiBold", 104, CREAM, no_orphan=True), -30, 0.8))
    if _s(sc, "subtitle"): els.append((text_block(_s(sc, "subtitle"), INTER % "Medium", 50, GOLD, no_orphan=True), -10, 1.05))
    els.append((line_ornament(360), 30, 1.3))
    if _s(sc, "text"): els.append((text_block(_s(sc, "text"), INTER % "Regular", 50, CREAM, max_w=820, line_gap=1.38, no_orphan=True), 30, 1.6))
    return els

REC_TOP, REC_BOTTOM = 300, 1500   # zone utile du récapitulatif

def _fit_font(path, size, text, max_w, min_size):
    while size > min_size and F(path, size).getlength(text) > max_w:
        size -= 1
    return F(path, size)

def recap_row(i, it, h=150):
    """Ligne du résumé ; h=150 => identique à make.py. Plus petit pour 6–8 items."""
    s = h / 150
    fs = min(1.0, 0.45 + 0.55 * s)          # les polices rétrécissent moins vite que la ligne
    row = Image.new("RGBA", (840, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(row)
    m = 10 if h >= 150 else 5
    d.rounded_rectangle((0, m, 839, h - m), radius=int(26 * s), fill=(255, 255, 255, 16), outline=GOLD + (70,), width=2)
    cy = h // 2
    star(d, 70, cy, 30 * fs, 14 * fs, GOLD + (255,))
    d.text((70, cy), str(i + 1), font=F(INTER % "Bold", int(26 * fs)), fill=(20, 24, 50, 255), anchor="mm")
    a = arabic(it["arabic"], int(66 * fs), glow=False) if it.get("arabic") else None
    max_tw = 815 - 130 - (a.width - int(66 * fs * 0.35) + 20 if a else 0)
    ft = _fit_font(SERIF % "SemiBold", int(52 * fs), it.get("title", ""), max_tw, int(36 * fs))
    fsub = _fit_font(INTER % "Regular", int(30 * fs), it.get("subtitle", ""), max_tw, int(22 * fs))
    if it.get("subtitle"):
        d.text((130, cy - int(35 * fs)), it.get("title", ""), font=ft, fill=CREAM + (255,))
        d.text((130, cy + int(23 * fs)), it["subtitle"], font=fsub, fill=MUTED + (255,))
    else:
        d.text((130, cy), it.get("title", ""), font=ft, fill=CREAM + (255,), anchor="lm")
    if a:
        row.alpha_composite(a, (815 - a.width, cy - a.height // 2))
    return row

def scene_recap(sc):
    items = sc.get("items", [])
    n = len(items)
    head = [(text_block(_s(sc, "title", "En résumé") or "En résumé", SERIF % "SemiBold", 90, CREAM), 0, 0.1),
            (line_ornament(), 10, 0.3)]
    head_h = sum(el.height + g for el, g, _ in head)
    gap, first_gap = (14, 30) if n <= 5 else (8, 20)
    avail = (REC_BOTTOM - REC_TOP) - head_h - first_gap - gap * (n - 1)
    h = int(min(150, avail / max(n, 1)))
    els = list(head)
    stagger = 0.32 if n <= 6 else 0.26
    for i, it in enumerate(items):
        els.append((recap_row(i, it, h), first_gap if i == 0 else gap, 0.5 + i * stagger))
    return els

def scene_outro(sc):
    els = []
    if _s(sc, "next_label"): els.append((text_block(_s(sc, "next_label"), INTER % "Medium", 48, MUTED), 0, 0.1))
    if _s(sc, "next_title"): els.append((text_block(_s(sc, "next_title"), SERIF % "SemiBold", 92, CREAM, max_w=900), 0, 0.4))
    if _s(sc, "next_arabic"): els.append((arabic_fit(_s(sc, "next_arabic"), 170, min_scale=0.6), -10, 0.8))
    els.append((line_ornament(), 30, 1.2))
    if _s(sc, "cta"): els.append((text_block(_s(sc, "cta"), INTER % "SemiBold", 50, GOLD), 30, 1.5))
    els.append((arabic("قلب مسافر", 96, color=CREAM, glow=False), 10, 1.9))
    els.append((text_block("Qalb Mousafir", INTER % "Medium", 40, MUTED, shadow=False), -20, 2.1))
    return els

BUILDERS = {"hook": scene_hook, "quote": scene_quote, "step": scene_step, "recap": scene_recap, "outro": scene_outro}

def build_els(sc, dur):
    """Éléments positionnés + délais d'apparition comprimés si la scène est courte."""
    els = layout(BUILDERS[sc["type"]](sc))
    last_in = max(t for _, _, t in els)
    budget = dur - VISIBLE_BEFORE_END - FADE_IN
    if last_in > budget > 0:
        k = budget / last_in
        els = [(el, y, round(t * k, 3)) for el, y, t in els]
    return els

CENTER_Y = 900
def layout(items):
    total = sum(el.height + gap for el, gap, _ in items)
    y = CENTER_Y - total / 2
    out = []
    for el, gap, t in items:
        y += gap
        out.append((el, int(y), t))
        y += el.height
    return out

def draw(els, dur, lt, gt, last=False):
    fr = background(gt)
    out_at = None if last else dur - 0.4
    for el, y, t_in in els:
        put(fr, el, CX, y, lt, t_in, dur, out_at=out_at)
    if last and lt > dur - 0.8:  # fondu au noir à la toute fin
        k = (lt - (dur - 0.8)) / 0.8
        fr = Image.blend(fr, Image.new("RGBA", fr.size, (0, 0, 0, 255)), min(1, k))
    if gt < 0.5:
        fr = Image.blend(Image.new("RGBA", fr.size, (0, 0, 0, 255)), fr, gt / 0.5)
    return fr.convert("RGB")

# ---------- validation ----------
def validate(ep):
    errs, warns = [], []
    for k in ("slug", "scenes"):
        if k not in ep: errs.append(f"champ manquant : {k}")
    for i, sc in enumerate(ep.get("scenes", []), 1):
        t = sc.get("type")
        if t not in BUILDERS: errs.append(f"scène {i} : type inconnu {t!r}")
        if not (sc.get("tts") or sc.get("narration")): warns.append(f"scène {i} : pas de tts/narration (scène muette)")
        if "ﷺ" in sc.get("tts", ""): errs.append(f"scène {i} : ﷺ dans tts (écrire « paix et salut sur lui »)")
        if t == "step":
            tot = int(sc.get("total", 0))
            if not 3 <= tot <= 10: errs.append(f"scène {i} : total={tot} hors 3..10")
            if not 1 <= int(sc.get("index", 0)) <= max(tot, 1): errs.append(f"scène {i} : index hors 1..total")
            if len(sc.get("text", "")) > 140: warns.append(f"scène {i} : text long ({len(sc['text'])} car.)")
        if t == "recap" and not 3 <= len(sc.get("items", [])) <= 8:
            errs.append(f"scène {i} : recap avec {len(sc.get('items', []))} items (3..8)")
    return errs, warns

def check_bounds(name, els):
    top = min(y for _, y, _ in els); bottom = max(y + el.height for el, y, _ in els)
    if top < 150 or bottom > 1650:
        print(f"  ! {name} : contenu de y={top} à y={bottom} (risque de sortir du cadre / sous l'interface TikTok)")

# ---------- voix ----------
LEXIQUE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lexique_arabe.json")

def load_lexique():
    try:
        d = json.load(open(LEXIQUE_PATH, encoding="utf-8"))
    except FileNotFoundError:
        return {}
    return {k: v for k, v in d.items() if not k.startswith("_")}

def to_phonemes(kok, txt, lex):
    """Texte français -> phonèmes, en remplaçant les mots du lexique arabe par leurs phonèmes."""
    if not lex:
        return None
    import re
    pat = re.compile(r"(?<![\w'’])(" + "|".join(re.escape(k) for k in sorted(lex, key=len, reverse=True)) + r")(?![\w'’])")
    if not pat.search(txt):
        return None
    out = []
    for i, part in enumerate(pat.split(txt)):
        if i % 2:
            out.append(lex[part])
        elif part.strip(" "):
            lead = " " if part[:1] == " " else ""
            trail = " " if part[-1:] == " " else ""
            core = part.strip(" ")
            ph = kok.tokenizer.phonemize(core, TTS_LANG) if re.search(r"\w", core) else core
            if trail and ph:
                # petit mot juste avant un mot arabe (le, la, de, à, et, en…) : pas d'accent, liaison « en » -> « ɑ̃n »
                toks = ph.split(" ")
                last = toks[-1].replace("ˈ", "").replace("ˌ", "")
                if len(last) <= 3 and re.match(r"^[^\W\d_]+$", last.replace("\u0303", "")):
                    nxt = pat.split(txt)[i + 1] if i + 1 < len(pat.split(txt)) else ""
                    if last == "ɑ̃" and lex.get(nxt, "x")[:1] in "aeiouɑɛɔəyøœʊɪ":
                        last = "ɑ̃n"
                    toks[-1] = last
                ph = " ".join(toks)
            out.append(lead + ph + trail)
        else:
            out.append(part)
    return re.sub(r" {2,}", " ", "".join(out)).strip()

def tts_all(scenes):
    """Retourne [(chemin_wav ou None, durée_s)] ; cache par hash(texte, voix, vitesse, langue)."""
    os.makedirs(TTS_CACHE, exist_ok=True)
    import soundfile as sf
    kok, res = None, []
    lex = load_lexique()
    lex_sig = hashlib.sha1(json.dumps(lex, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:8] if lex else ""
    for i, sc in enumerate(scenes, 1):
        txt = (sc.get("tts") or sc.get("narration") or "").strip()
        if not txt:
            res.append((None, 0.0)); continue
        key = hashlib.sha1(f"{TTS_VOICE}|{TTS_SPEED}|{TTS_LANG}|{lex_sig}|{txt}".encode()).hexdigest()[:16]
        path = os.path.join(TTS_CACHE, key + ".wav")
        if not os.path.exists(path):
            if kok is None:
                from kokoro_onnx import Kokoro
                kok = Kokoro(TTS_MODEL, TTS_VOICES)
            t0 = time.time()
            ph = to_phonemes(kok, txt, lex)
            if ph:
                a, sr = kok.create(ph, voice=TTS_VOICE, speed=TTS_SPEED, lang=TTS_LANG, is_phonemes=True)
            else:
                a, sr = kok.create(txt, voice=TTS_VOICE, speed=TTS_SPEED, lang=TTS_LANG)
            sf.write(path + ".tmp.wav", a, sr, subtype="PCM_16")
            os.replace(path + ".tmp.wav", path)
            print(f"  voix scène {i} : {len(a) / sr:.2f} s (générée en {time.time() - t0:.1f} s)")
        info = sf.info(path)
        res.append((path, round(info.frames / info.samplerate, 2)))
    del kok; gc.collect()
    return res

def build_audio(voices, starts_f, total_frames, path):
    import soundfile as sf
    sr = 24000
    for p, _ in voices:
        if p: sr = sf.info(p).samplerate; break
    buf = np.zeros(int(round(total_frames / FPS * sr)) + 1, np.float32)
    for (p, _), sf_ in zip(voices, starts_f):
        if not p: continue
        a, _sr = sf.read(p, dtype="float32")
        o = int(round((sf_ / FPS + VOICE_DELAY) * sr))
        n = min(len(a), len(buf) - o)
        buf[o:o + n] += a[:n]
    buf = buf[:int(round(total_frames / FPS * sr))]
    sf.write(path, np.clip(buf, -1, 1), sr, subtype="PCM_16")

def mux(video, wav, out):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-i", wav, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-af", AUDIO_FILTER, "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
                    "-shortest", "-movflags", "+faststart", out + ".tmp.mp4"], check=True)
    os.replace(out + ".tmp.mp4", out)

# ---------- plan ----------
def plan(ep, voices):
    """Calcule durées, nombre d'images et image de départ globale de chaque scène."""
    tm = ep.get("timing", {})
    tail = float(tm.get("tail", VOICE_TAIL))
    out, f0 = [], 0
    for i, (sc, (vp, vd)) in enumerate(zip(ep["scenes"], voices)):
        planned = float(sc.get("duration", tm.get("min_by_type", {}).get(sc["type"], tm.get("min_scene", MIN_SCENE))))
        dur = round(max(planned, vd + tail), 2) if vp else planned
        nf = int(round(dur * FPS))
        name = f"{i + 1:02d}_{sc['type']}"
        out.append({"i": i, "name": name, "dur": dur, "nf": nf, "f0": f0, "voice": vd})
        f0 += nf
    return out, f0

# ---------- rendu ----------
_EP = None  # épisode, partagé avec les processus (fork)

def render_scene(job):
    sc = _EP["scenes"][job["i"]]
    t0 = time.time()
    dur, nf, f0, last = job["dur"], job["nf"], job["f0"], job["last"]
    els = build_els(sc, dur)
    tmp, final = job["path"][:-4] + ".tmp.mp4", job["path"]
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast",
                          "-crf", "18", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for f in range(nf):
        lt = f / FPS
        p.stdin.write(draw(els, dur, lt, (f0 + f) / FPS, last).tobytes())
    p.stdin.close()
    ok = p.wait() == 0
    if ok:
        os.replace(tmp, final)
        with open(final[:-4] + ".key", "w") as fh: fh.write(job["key"])
    return job["name"], ok, time.time() - t0, nf

def scene_key(sc, job):
    d = {k: v for k, v in sc.items() if k not in ("narration", "tts")}
    d.update(dur=job["dur"], nf=job["nf"], f0=job["f0"], last=job["last"])
    src = open(os.path.abspath(__file__), "rb").read()
    return hashlib.sha1(json.dumps(d, sort_keys=True, ensure_ascii=False).encode() + src).hexdigest()

def preview(ep, jobs, outdir):
    pdir = os.path.join(outdir, "preview"); os.makedirs(pdir, exist_ok=True)
    thumbs = []
    for j in jobs:
        sc = ep["scenes"][j["i"]]
        els = build_els(sc, j["dur"])
        check_bounds(j["name"], els)
        lt = j["dur"] - (0.9 if j["last"] else 0.6)  # moment le plus chargé (tout est affiché, pas de fondu)
        img = draw(els, j["dur"], lt, j["f0"] / FPS + lt, j["last"])
        p = os.path.join(pdir, f"prev_{j['name']}.jpg"); img.save(p, quality=88)
        thumbs.append((j, img))
    tw, th, cols = 360, 640, 5
    rows = math.ceil(len(thumbs) / cols)
    sheet = Image.new("RGB", (tw * cols, (th + 44) * rows), (12, 12, 18))
    d = ImageDraw.Draw(sheet)
    for k, (j, img) in enumerate(thumbs):
        x, y = (k % cols) * tw, (k // cols) * (th + 44)
        sheet.paste(img.resize((tw, th), Image.LANCZOS), (x, y))
        d.text((x + 10, y + th + 8), f"{j['name']}  {j['dur']:.2f}s  (voix {j['voice']:.2f}s)",
               font=F(INTER % "Medium", 22), fill=(230, 230, 230))
    p = os.path.join(pdir, "contact.jpg"); sheet.save(p, quality=85)
    print("planche contact :", p)
    return p

def main():
    global _EP
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("json")
    ap.add_argument("--preview", action="store_true", help="1 JPEG par scène + planche contact, pas de vidéo")
    ap.add_argument("--only", type=int, nargs="+", help="numéros de scènes (1..N) à rendre ; pas de montage final")
    ap.add_argument("--jobs", type=int, default=0, help="processus en parallèle (défaut : nb de cœurs)")
    ap.add_argument("--force", action="store_true", help="re-rendre même les scènes inchangées")
    a = ap.parse_args()

    T0 = time.time()
    ep = json.load(open(a.json, encoding="utf-8"))
    errs, warns = validate(ep)
    for w in warns: print("  attention :", w)
    if errs:
        for e in errs: print("  ERREUR :", e)
        sys.exit(1)
    slug = ep["slug"]
    outdir = os.path.join(HERE, "out", slug)
    sdir = os.path.join(outdir, "scenes"); os.makedirs(sdir, exist_ok=True)

    print(f"[1/4] voix ({len(ep['scenes'])} scènes)")
    t = time.time(); voices = tts_all(ep["scenes"]); t_tts = time.time() - t
    jobs, total_frames = plan(ep, voices)
    for j in jobs:
        j["last"] = j["i"] == len(jobs) - 1
        j["path"] = os.path.join(sdir, j["name"] + ".mp4")
        j["key"] = scene_key(ep["scenes"][j["i"]], j)
    print(f"  durée totale {total_frames / FPS:.2f} s ; voix totale {sum(v for _, v in voices):.2f} s")
    with open(os.path.join(outdir, "timings.json"), "w") as fh:
        json.dump([{k: j[k] for k in ("name", "dur", "nf", "f0", "voice")} for j in jobs], fh, indent=1)

    if a.preview:
        print("[2/2] preview")
        preview(ep, jobs, outdir)
        print(f"terminé en {time.time() - T0:.1f} s")
        return

    todo = [j for j in jobs if (not a.only or j["i"] + 1 in a.only)]
    if not a.force:
        def fresh(j):
            k = j["path"][:-4] + ".key"
            return os.path.exists(j["path"]) and os.path.exists(k) and open(k).read() == j["key"]
        skipped = [j["name"] for j in todo if fresh(j)]
        if skipped: print("  inchangées (non re-rendues) :", ", ".join(skipped))
        todo = [j for j in todo if j["name"] not in skipped]
    todo.sort(key=lambda j: -j["nf"])  # plus longues d'abord = meilleur équilibrage
    n = max(1, min(len(todo) or 1, a.jobs or os.cpu_count() or 1))
    print(f"[2/4] rendu de {len(todo)} scène(s) sur {n} processus")
    _EP = ep
    t = time.time(); stats = []
    if todo:
        with mp.get_context("fork").Pool(n) as pool:
            for name, ok, dt, nf in pool.imap_unordered(render_scene, todo):
                stats.append((name, ok, dt, nf))
                print(f"  {'ok ' if ok else 'ÉCHEC'} {name} : {nf} images en {dt:.1f} s ({nf / dt:.1f} i/s)")
    t_render = time.time() - t
    if any(not st[1] for st in stats):
        print("ÉCHEC du rendu d'au moins une scène"); sys.exit(2)
    with open(os.path.join(outdir, "render_stats.json"), "w") as fh:
        json.dump({"tts_s": round(t_tts, 1), "render_wall_s": round(t_render, 1), "processes": n,
                   "scenes": [{"name": s[0], "frames": s[3], "seconds": round(s[2], 1)} for s in stats]}, fh, indent=1)
    if a.only:
        for j in jobs:   # extrait de contrôle : scène + sa voix (mêmes réglages audio que le montage final)
            if j["i"] + 1 in a.only and voices[j["i"]][0] and os.path.exists(j["path"]):
                wav = j["path"][:-4] + "_voix.wav"
                build_audio([voices[j["i"]]], [0], j["nf"], wav)
                mux(j["path"], wav, j["path"][:-4] + "_voix.mp4")
                print("  extrait avec voix :", j["path"][:-4] + "_voix.mp4")
        print(f"terminé (scènes seules) en {time.time() - T0:.1f} s"); return

    print("[3/4] concaténation")
    lst = os.path.join(outdir, "list.txt")
    with open(lst, "w") as fh:
        for j in jobs: fh.write(f"file '{j['path']}'\n")
    v = os.path.join(outdir, "v.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", v], check=True)

    print("[4/4] voix + mux")
    wav = os.path.join(outdir, "voice.wav")
    build_audio(voices, [j["f0"] for j in jobs], total_frames, wav)
    final = os.path.join(outdir, f"{slug}.mp4")
    mux(v, wav, final)
    print(f"OK : {final}  ({total_frames / FPS:.2f} s) — total {time.time() - T0:.1f} s")

if __name__ == "__main__":
    main()
