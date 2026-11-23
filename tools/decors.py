#!/usr/bin/env python3
"""Qalb Mousafir — décors procéduraux animés pour les scènes « story » (série « Les Compagnons »).

Tout est dessiné en code (numpy + PIL + OpenCV), aucune image téléchargée.
RÈGLE ABSOLUE : aucun être humain ni animal, même suggéré (ni silhouette, ni ombre, ni main).
Uniquement des paysages et des objets.

API utilisée par render.py :
    DECORS                      -> noms disponibles
    get(name)                   -> objet décor (construit une fois par processus, mis en cache)
    get(name).frame(t, p, ctx)  -> np.float32 (H, W, 3), valeurs 0..255
        t   : secondes depuis le début de la « série » de scènes consécutives qui partagent ce décor
        p   : progression 0..1 sur cette série (Ken Burns, traces qui apparaissent…) ; peut dépasser 1
        ctx : dict optionnel ; pour « parchemin » : {"texts": [(img_rgba_uint8, reveal 0..1, rtl, alpha)]}

Mouvement : chaque plan a une profondeur k (0 = lointain, 1 = proche) ; la caméra fait un léger
travelling latéral (parallaxe ∝ k) et un zoom lent de type Ken Burns (∝ k). Le ciel reste fixe
(à l'infini), seules les étoiles scintillent.
"""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

try:
    import cv2
    cv2.setNumThreads(1)
except Exception:          # pragma: no cover
    cv2 = None

W, H = 1080, 1920
M = 160                    # marge horizontale de chaque plan (parallaxe)
CX = W // 2 - 20           # même axe que render.py (décalé à gauche des boutons TikTok)

NIGHT_TOP, NIGHT_BOT = (7, 12, 32), (28, 30, 62)
GOLD, CREAM = (226, 189, 112), (246, 238, 222)

DECORS = ("desert_nuit", "desert_aube", "medine_nuit", "kaaba_loin",
          "lanterne", "traces_sable", "parchemin", "palmeraie")

# ------------------------------------------------------------------ outils
def _f(c):
    return np.asarray(c, np.float32)

def smooth(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3 - 2 * x)

def ease_io(x):
    x = min(max(x, 0.0), 1.0)
    return 0.5 - 0.5 * math.cos(math.pi * x)

def vgrad(stops, h=H, w=W):
    """Dégradé vertical : stops = [(position 0..1, (r, g, b)), ...] -> float32 (h, w, 3)."""
    ys = np.linspace(0, 1, h)
    pos = [s[0] for s in stops]
    cols = np.array([s[1] for s in stops], np.float32)
    col = np.stack([np.interp(ys, pos, cols[:, k]) for k in range(3)], -1).astype(np.float32)
    return np.repeat(col[:, None, :], w, axis=1)

def radial(cx, cy, rx, ry, w=W, h=H, x0=0, y0=0, power=2.0):
    yy, xx = np.mgrid[y0:y0 + h, x0:x0 + w].astype(np.float32)
    d = np.sqrt(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2)
    return np.exp(-d ** power)

def fade_edges(a, frac=0.18):
    """Multiplie un sprite de lumière par une fenêtre qui tombe à 0 sur les bords (pas de bord visible)."""
    h, w = a.shape[:2]
    wx = smooth(np.minimum(np.arange(w), w - 1 - np.arange(w)) / (frac * w))
    wy = smooth(np.minimum(np.arange(h), h - 1 - np.arange(h)) / (frac * h))
    win = (wy[:, None] * wx[None, :]).astype(np.float32)
    return a * (win[..., None] if a.ndim == 3 else win)

def noise1d(n, seed, scale, octaves=4, persist=0.5):
    """Bruit 1D lisse (interpolation smoothstep), amplitude ≈ ±1."""
    rng = np.random.default_rng(seed)
    out = np.zeros(n, np.float32)
    amp, tot = 1.0, 0.0
    xs = np.arange(n, dtype=np.float32)
    for o in range(octaves):
        step = scale / (2 ** o)
        k = int(n / step) + 3
        pts = rng.uniform(-1, 1, k).astype(np.float32)
        u = xs / step
        i = np.floor(u).astype(int)
        fr = u - i
        fr = fr * fr * (3 - 2 * fr)
        out += amp * (pts[i] * (1 - fr) + pts[i + 1] * fr)
        tot += amp
        amp *= persist
    return out / tot

def noise2d(h, w, seed, cell, octaves=3):
    """Bruit 2D lisse (valeurs aléatoires agrandies en bicubique), ≈ ±1."""
    rng = np.random.default_rng(seed)
    out = np.zeros((h, w), np.float32)
    amp, tot = 1.0, 0.0
    for o in range(octaves):
        c = max(2, cell / (2 ** o))
        gh, gw = int(h / c) + 3, int(w / c) + 3
        g = rng.uniform(-1, 1, (gh, gw)).astype(np.float32)
        big = cv2.resize(g, (int(gw * c), int(gh * c)), interpolation=cv2.INTER_CUBIC)
        out += amp * big[:h, :w]
        tot += amp
        amp *= 0.5
    return out / tot

class Layer:
    """Plan prémultiplié uint8 (h, w, 4), placé à l'écran en (x0, y0), profondeur k (0..1)."""
    def __init__(self, img, y0, k, x0=-M):
        self.img, self.y0, self.k, self.x0 = img, y0, k, x0

def premult(rgb, a):
    a = np.clip(a, 0, 1).astype(np.float32)
    out = np.empty(rgb.shape[:2] + (4,), np.uint8)
    out[..., :3] = np.clip(rgb * a[..., None] + 0.5, 0, 255)
    out[..., 3] = np.clip(a * 255 + 0.5, 0, 255)
    return out

def pil_premult(img):
    """PIL RGBA (alpha droit) -> uint8 prémultiplié."""
    arr = np.asarray(img.convert("RGBA")).astype(np.float32)
    return premult(arr[..., :3], arr[..., 3] / 255)

def blend_pm(frame, src, x, y, gain=1.0):
    """Compose un uint8 prémultiplié (h, w, 4) sur frame float32 en (x, y), avec découpe."""
    h, w = src.shape[:2]
    x0, y0, x1, y1 = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
    if x1 <= x0 or y1 <= y0:
        return
    s = np.ascontiguousarray(src[y0 - y:y1 - y, x0 - x:x1 - x])
    reg = frame[y0:y1, x0:x1]                 # vue : OpenCV écrit directement dans l'image (≈ 4× plus rapide que numpy)
    a = s[..., 3].astype(np.float32)
    inv = cv2.merge([a, a, a])
    inv *= np.float32(-gain / 255.0)
    inv += np.float32(1.0)
    cv2.multiply(reg, inv, dst=reg)
    rgb = cv2.cvtColor(s, cv2.COLOR_RGBA2RGB).astype(np.float32)
    if gain != 1.0:
        rgb *= np.float32(gain)
    cv2.add(reg, rgb, dst=reg)

def add_light(frame, src, x, y, gain=1.0):
    """Ajout de lumière (src float32 (h, w, 3)) en (x, y)."""
    h, w = src.shape[:2]
    x0, y0, x1, y1 = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
    if x1 <= x0 or y1 <= y0:
        return
    reg = frame[y0:y1, x0:x1]
    s = src[y0 - y:y1 - y, x0 - x:x1 - x]
    if s.shape[0] * s.shape[1] < 4096:      # petits sprites (étoiles) : numpy suffit
        reg += s * np.float32(gain)
    else:
        cv2.scaleAdd(np.ascontiguousarray(s), float(gain), reg, dst=reg)

class Cam:
    """Caméra : zoom Ken Burns (focale fx, fy) + travelling latéral lent, tous deux ∝ profondeur."""
    def __init__(self, fx=CX, fy=960, zoom=0.06, pan=36.0, period=80.0):
        self.fx, self.fy, self.zoom, self.pan, self.w = fx, fy, zoom, pan, 2 * math.pi / period

    def at(self, k, t, p):
        s = 1.0 + self.zoom * (0.2 + 0.8 * k) * ease_io(min(p, 1.15) / 1.15)
        dx = -self.pan * k * math.sin(self.w * t)
        return s, dx

    def pt(self, k, t, p, x, y):
        s, dx = self.at(k, t, p)
        return s * (x - self.fx) + self.fx + dx, s * (y - self.fy) + self.fy, s

def comp_layer(frame, L, cam, t, p, gain=1.0):
    s, dx = cam.at(L.k, t, p)
    h, w = L.img.shape[:2]
    top = s * (L.y0 - cam.fy) + cam.fy
    bot = s * (L.y0 + h - cam.fy) + cam.fy
    oy0, oy1 = max(0, int(math.floor(top))), min(H, int(math.ceil(bot)))
    if oy1 <= oy0:
        return
    tx = s * (L.x0 - cam.fx) + cam.fx + dx
    ty = s * (L.y0 - cam.fy) + cam.fy - oy0
    mat = np.float32([[s, 0, tx], [0, s, ty]])
    out = cv2.warpAffine(L.img, mat, (W, oy1 - oy0), flags=cv2.INTER_LINEAR,
                         borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    blend_pm(frame, out, 0, oy0, gain)

def comp_sprite(frame, spr, ax, ay, x, y, scale=1.0, angle=0.0, gain=1.0, light=False):
    """Sprite (prémultiplié uint8 RGBA, ou float32 RGB si light) : le point (ax, ay) du sprite va en (x, y)
    écran, avec échelle et rotation (degrés, sens horaire positif)."""
    h, w = spr.shape[:2]
    a = math.radians(angle)
    c, s_ = math.cos(a) * scale, math.sin(a) * scale
    # coins transformés -> boîte englobante
    pts = [(-ax, -ay), (w - ax, -ay), (-ax, h - ay), (w - ax, h - ay)]
    xs = [x + c * px - s_ * py for px, py in pts]
    ys = [y + s_ * px + c * py for px, py in pts]
    bx0, by0 = int(math.floor(min(xs))) - 1, int(math.floor(min(ys))) - 1
    bx1, by1 = int(math.ceil(max(xs))) + 1, int(math.ceil(max(ys))) + 1
    bx0c, by0c, bx1c, by1c = max(0, bx0), max(0, by0), min(W, bx1), min(H, by1)
    if bx1c <= bx0c or by1c <= by0c:
        return
    mat = np.float32([[c, -s_, x - c * ax + s_ * ay - bx0c],
                      [s_, c, y - s_ * ax - c * ay - by0c]])
    out = cv2.warpAffine(spr, mat, (bx1c - bx0c, by1c - by0c), flags=cv2.INTER_LINEAR,
                         borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    if light:
        add_light(frame, out, bx0c, by0c, gain)
    else:
        blend_pm(frame, out, bx0c, by0c, gain)

def ss_draw(w, h, k, fn):
    """Dessin anticrénelé : fn(draw, k) dessine sur un masque L k× plus grand ; renvoie un masque float (h, w)."""
    big = Image.new("L", (w * k, h * k), 0)
    fn(ImageDraw.Draw(big), k)
    return np.asarray(big.resize((w, h), Image.LANCZOS)).astype(np.float32) / 255.0

# ------------------------------------------------------------------ ciel
class Stars:
    def __init__(self, n, seed, ymax, ymin=0, xmin=0, xmax=W, bright=1.0, glints=5):
        rng = np.random.default_rng(seed)
        self.items = []
        for i in range(n):
            x, y = rng.uniform(xmin, xmax), ymin + (ymax - ymin) * rng.uniform(0, 1) ** 1.25
            r = rng.uniform(0.6, 1.9)
            b = rng.uniform(0.35, 1.0) * bright * (1 - 0.6 * (y - ymin) / max(1, ymax - ymin))
            ph, sp = rng.uniform(0, 6.28), rng.uniform(0.7, 2.0)
            glint = i < glints
            R = 12 if glint else 4
            yy, xx = np.mgrid[-R:R + 1, -R:R + 1].astype(np.float32)
            fx, fy = x - int(x), y - int(y)
            d2 = (xx - fx + 0.5) ** 2 + (yy - fy + 0.5) ** 2
            spr = np.exp(-d2 / (2 * (0.55 * r) ** 2))
            if glint:
                spr = spr * 1.4 + 0.35 * (np.exp(-np.abs(xx - fx + 0.5) / 0.7) * np.exp(-np.abs(yy - fy + 0.5) / 4.5)
                                          + np.exp(-np.abs(yy - fy + 0.5) / 0.7) * np.exp(-np.abs(xx - fx + 0.5) / 4.5))
            col = _f((255, 246, 228)) if rng.uniform() < 0.8 else _f((210, 220, 255))
            self.items.append((int(x) - R, int(y) - R, (spr[..., None] * col).astype(np.float32), b, ph, sp))

    def draw(self, frame, t, gain=1.0):
        for x, y, spr, b, ph, sp in self.items:
            a = b * gain * (0.55 + 0.45 * math.sin(t * sp + ph))
            if a > 0.02:
                add_light(frame, spr, x, y, a)

def crescent(r, glow=2.6, col=CREAM, phase=0.42):
    """Croissant de lune avec halo : float32 RGB (lumière additive)."""
    R = int(r * glow * 1.5) + 4
    k = 4
    def fn(d, k):
        c = R * k
        d.ellipse((c - r * k, c - r * k, c + r * k, c + r * k), fill=255)
        o = r * phase * 2 * k
        d.ellipse((c - r * k + o, c - r * k - o * 0.35, c + r * k + o, c + r * k - o * 0.35), fill=0)
    m = ss_draw(2 * R, 2 * R, k, fn)
    disc = ss_draw(2 * R, 2 * R, k, lambda d, k: d.ellipse((R * k - r * k, R * k - r * k, R * k + r * k, R * k + r * k), fill=255))
    g = cv2.GaussianBlur(m, (0, 0), r * 0.45) * 0.55 + cv2.GaussianBlur(m, (0, 0), r * 1.2) * 0.45
    rgb = m[..., None] * _f(col) + g[..., None] * _f((235, 210, 160)) * 0.55 + disc[..., None] * _f((40, 46, 80)) * 0.18
    return fade_edges(rgb.astype(np.float32), 0.3), R

def night_sky(horizon=1000, warm=0.6, seed=1):
    sky = vgrad([(0, NIGHT_TOP), (0.30, (10, 16, 42)), (horizon / H, NIGHT_BOT), (1, (34, 32, 62))])
    g = radial(CX, horizon + 60, 760, 300)
    sky += g[..., None] * _f((70, 45, 22)) * warm
    return sky

# ------------------------------------------------------------------ formes
def crest_dunes(n, base, dunes, seed, noise_amp=6.0):
    """Ligne de crête (y écran par colonne) : union de dunes asymétriques (crête vive) + bruit."""
    x = np.arange(n, dtype=np.float32)
    h = np.zeros(n, np.float32)
    for c, hg, wl, wr in dunes:
        u = np.where(x < c, (c - x) / wl, (x - c) / wr)
        uc = np.clip(u, 0, 1)
        prof = 0.55 * (1 - uc) ** 2 * (1 + 2 * uc) + 0.45 * (1 - uc) ** 1.3   # crête vive, flancs en S
        h = np.maximum(h, hg * prof)
    return base - h + noise1d(n, seed, 420, 3) * noise_amp

def shaded_layer(crest, y_bottom, base, lit, shadow, light=1.0, fall=140.0, skew=0.7, rim=None, rim_a=0.0,
                 rim_w=2.4, vdark=0.0, ripples=0.0, seed=0, k=0.5, tex=0.0, lsmooth=0.0, fade_floor=0.35, haze=None,
                 bend=None):
    """Plan à crête (dunes, montagnes) : faces éclairées / à l'ombre selon la pente, frontière en biais,
    liseré de lumière sur la crête. light=+1 : lumière venant de la droite ; -1 : de la gauche."""
    n = crest.shape[0]
    y0 = int(math.floor(crest.min())) - 3
    h = int(y_bottom) - y0
    ys = np.arange(y0, y0 + h, dtype=np.float32)[:, None]
    d = ys - crest[None, :]
    alpha = np.clip(d + 0.5, 0, 1)
    dd = np.clip(d, 0, None)
    slope = np.gradient(crest)
    if lsmooth:
        slope = cv2.GaussianBlur(slope.reshape(1, -1).astype(np.float32), (0, 0), lsmooth).ravel()
    L = np.tanh(-slope * light * 3.0)            # >0 : face tournée vers la lumière
    # frontière d'ombre : droite en biais, ou courbe qui s'évase (bend > 0) vers le premier plan
    off = skew * dd if bend is None else skew * dd * (1 + dd / bend)
    xi = np.clip((np.arange(n)[None, :] + light * off).astype(np.int32), 0, n - 1)
    Ld = L[xi]
    fade = fade_floor + (1 - fade_floor) * np.exp(-dd / fall)
    tl = np.clip(Ld, 0, 1) * fade
    ts = np.clip(-Ld, 0, 1) * fade
    base, lit, shadow = _f(base), _f(lit), _f(shadow)
    rgb = base + (lit - base) * tl[..., None] + (shadow - base) * ts[..., None]
    if vdark:
        rgb *= (1 - vdark * np.clip(dd / 600.0, 0, 1))[..., None]
    if tex:
        nz = noise2d(h, n, seed + 7, 60, 3)
        rgb *= (1 + tex * nz)[..., None]
    if ripples:
        wob = noise1d(n, seed + 3, 200, 3)[None, :] * 26
        rp = np.sin((dd * 0.9 + wob + 0.05 * np.arange(n)[None, :]) * 0.22)
        rp *= smooth((dd - 25) / 80) * np.exp(-dd / 700)
        rgb *= (1 + ripples * rp)[..., None]
    if haze is not None:            # brume au pied des montagnes : (y début, y fin, couleur, intensité)
        hy0, hy1, hcol, ham = haze
        hz = smooth((ys - hy0) / (hy1 - hy0)) * ham
        rgb = rgb + (_f(hcol) - rgb) * hz[..., None]
    if rim is not None:
        rimm = np.exp(-dd / rim_w) * np.clip(0.25 + L[None, :], 0, 1)
        rgb = rgb + (_f(rim) - rgb) * (rimm * rim_a)[..., None]
    return Layer(premult(rgb, alpha), y0, k)

def ridge_mountains(n, base, amp, seed, scale=260, sharp=1.0):
    """Ligne de crête rocheuse (pics) : bruit « ridged »."""
    r = noise1d(n, seed, scale, 5, 0.55)
    r = 1 - np.abs(r) ** sharp
    r2 = noise1d(n, seed + 11, scale * 0.35, 3, 0.5) * 0.18
    return base - amp * (r + r2)

# ---------- palmier (silhouette) ----------
def palm_sprites(height, seed, color, lean=0.08, fronds=13, ss=3, frond_len=None):
    """Renvoie (tronc, couronne_arriere, couronne_avant) en uint8 prémultipliés + ancrages.
    Le tronc a son pied au point (bx, by) ; les couronnes tournent autour du sommet (cx, cy)."""
    rng = np.random.default_rng(seed)
    fl = frond_len or height * 0.42
    pad = int(fl * 1.25)
    w = int(pad * 2 + abs(lean) * height + 20)
    hh = int(height + pad * 1.3)
    bx = w / 2 - lean * height / 2
    by = hh - 4
    tx, ty = bx + lean * height, by - height
    bend = rng.uniform(-0.06, 0.06) * height

    def trunk(d, k):
        pts_l, pts_r = [], []
        N = 30
        for i in range(N + 1):
            s = i / N
            x = bx + (tx - bx) * s + bend * math.sin(math.pi * s)
            y = by + (ty - by) * s
            wd = (height * 0.045) * (1 - 0.45 * s) + 1.2
            notch = 0.12 * wd * (1 if (i % 2) else -1)
            pts_l.append(((x - wd - notch) * k, y * k))
            pts_r.append(((x + wd + notch) * k, y * k))
        d.polygon(pts_l + pts_r[::-1], fill=255)

    cx, cy = tx + bend * 0, ty

    def crown(sel):
        def fn(d, k):
            for i in range(fronds):
                if i % 2 != sel:
                    continue
                ang = -math.pi / 2 + (i / (fronds - 1) - 0.5) * math.radians(280) + rng.uniform(-0.12, 0.12)
                L = fl * rng.uniform(0.78, 1.08)
                droop = 0.55 * (abs(math.cos(ang)) ** 0.8) + 0.15
                pts = []
                for j in range(26):
                    s = j / 25
                    x = cx + L * s * math.cos(ang)
                    y = cy + L * s * math.sin(ang) + droop * L * s * s
                    pts.append((x, y))
                # nervure
                for j in range(25):
                    w0 = max(1.0, 4.2 * (1 - j / 25)) * height / 600
                    d.line((pts[j][0] * k, pts[j][1] * k, pts[j + 1][0] * k, pts[j + 1][1] * k), fill=255,
                           width=max(1, int(w0 * k * 1.6)))
                # folioles
                for j in range(3, 25):
                    s = j / 25
                    px, py = pts[j]
                    qx, qy = pts[j + 1]
                    tdx, tdy = qx - px, qy - py
                    nrm = math.hypot(tdx, tdy) + 1e-6
                    tdx, tdy = tdx / nrm, tdy / nrm
                    ll = L * 0.24 * (math.sin(math.pi * min(1, s * 1.15)) ** 0.6) * (1 - 0.5 * s)
                    for sg in (-1, 1):
                        a2 = math.radians(52) * sg
                        vx = tdx * math.cos(a2) - tdy * math.sin(a2)
                        vy = tdx * math.sin(a2) + tdy * math.cos(a2)
                        vy += 0.55  # les folioles retombent
                        nv = math.hypot(vx, vy)
                        ex, ey = px + vx / nv * ll, py + vy / nv * ll
                        d.line((px * k, py * k, ex * k, ey * k), fill=255,
                               width=max(1, int(2.2 * height / 600 * k + 1)))
            r = height * 0.035
            d.ellipse(((cx - r) * k, (cy - r) * k, (cx + r) * k, (cy + r * 1.3) * k), fill=255)
        return fn

    col = np.ones((hh, w, 3), np.float32) * _f(color)
    t_m = ss_draw(w, hh, ss, trunk)
    c0 = ss_draw(w, hh, ss, crown(0))
    c1 = ss_draw(w, hh, ss, crown(1))
    return {"trunk": premult(col, t_m), "back": premult(col, c0), "front": premult(col, c1),
            "base": (bx, by), "top": (cx, cy)}

def bake(dst_rgb, dst_a, spr_pm, x, y):
    """Colle un sprite prémultiplié dans un plan en construction (rgb prémult float, alpha float)."""
    h, w = spr_pm.shape[:2]
    x, y = int(round(x)), int(round(y))
    H_, W_ = dst_a.shape
    x0, y0, x1, y1 = max(0, x), max(0, y), min(W_, x + w), min(H_, y + h)
    if x1 <= x0 or y1 <= y0:
        return
    s = spr_pm[y0 - y:y1 - y, x0 - x:x1 - x].astype(np.float32)
    a = s[..., 3] / 255.0
    dst_rgb[y0:y1, x0:x1] = dst_rgb[y0:y1, x0:x1] * (1 - a[..., None]) + s[..., :3]
    dst_a[y0:y1, x0:x1] = dst_a[y0:y1, x0:x1] * (1 - a) + a

def layer_from_pm(rgb_pm, a, y0, k):
    out = np.empty(a.shape + (4,), np.uint8)
    out[..., :3] = np.clip(rgb_pm + 0.5, 0, 255)
    out[..., 3] = np.clip(a * 255 + 0.5, 0, 255)
    return Layer(out, y0, k)

def palm_sway(t, amp, seed):
    return amp * (0.75 * math.sin(t * 0.9 + seed * 1.7) + 0.25 * math.sin(t * 2.1 + seed * 0.6))

def crop_pm(spr):
    """Recadre un sprite prémultiplié sur sa partie visible ; renvoie (sprite, dx, dy) du coin gardé."""
    ys, xs = np.nonzero(spr[..., 3] > 0)
    y0, y1, x0, x1 = max(0, ys.min() - 2), ys.max() + 3, max(0, xs.min() - 2), xs.max() + 3
    return np.ascontiguousarray(spr[y0:y1, x0:x1]), x0, y0

class Palm:
    """Palmier animé : tronc fixe + deux couronnes qui oscillent avec des phases différentes."""
    def __init__(self, x, base_y, height, seed, color, k, amp=1.8, lean=0.08):
        s = palm_sprites(height, seed, color, lean=lean)
        bx, by = s["base"]
        cx, cy = s["top"]
        self.parts = []
        for key in ("trunk", "back", "front"):
            spr, ox, oy = crop_pm(s[key])
            if key == "trunk":
                self.parts.append((spr, bx - ox, by - oy))
            else:
                self.parts.append((spr, cx - ox, cy - oy))
        self.top_off = (cx - bx, cy - by)
        self.x, self.y, self.k, self.amp, self.seed = x, base_y, k, amp, seed

    def draw(self, frame, cam, t, p, gain=1.0):
        X, Y, sc = cam.pt(self.k, t, p, self.x, self.y)
        (tr, tax, tay), (bk, bax, bay), (fr_, fax, fay) = self.parts
        comp_sprite(frame, tr, tax, tay, X, Y, sc, gain=gain)
        TX, TY = X + self.top_off[0] * sc, Y + self.top_off[1] * sc   # sommet du tronc à l'écran
        a = palm_sway(t, self.amp, self.seed)
        comp_sprite(frame, bk, bax, bay, TX, TY, sc, a * 0.8, gain=gain)
        comp_sprite(frame, fr_, fax, fay, TX, TY, sc, a * 1.15 + 0.4 * math.sin(t * 1.3 + self.seed), gain=gain)

# ------------------------------------------------------------------ décors
class Decor:
    name = ""
    cam = Cam()

    def frame(self, t, p, ctx=None):
        raise NotImplementedError

class _Desert(Decor):
    """Dunes en 3 plans (communes à desert_nuit et desert_aube) + sable qui glisse sur la crête proche."""
    def __init__(self, dawn=False):
        self.name = "desert_aube" if dawn else "desert_nuit"
        n = W + 2 * M
        self.cam = Cam(fy=1000, zoom=0.06, pan=40)
        far = crest_dunes(n, 975, [(180, 55, 330, 200), (600, 75, 420, 240), (1000, 48, 330, 210), (1300, 66, 360, 220)], 11, 4)
        mid = crest_dunes(n, 1075, [(60, 80, 380, 220), (500, 120, 520, 280), (1040, 100, 480, 260), (1400, 60, 320, 200)], 12, 5)
        near = crest_dunes(n, 1250, [(320, 170, 680, 320), (980, 130, 560, 300), (1460, 100, 420, 240)], 13, 6)
        fb, mb = int(mid.max()) + 90, int(near.max()) + 90
        self.near_crest = near
        if not dawn:
            self.sky = night_sky(horizon=1000, warm=0.75)
            self.stars = Stars(170, 21, 960, 60, glints=6)
            self.moon, self.moon_r = crescent(58)
            self.moon_xy = (760, 520)
            lt = 1.0  # lune à droite
            self.layers = [
                shaded_layer(far, fb, (38, 40, 80), (62, 62, 104), (28, 30, 64), lt, 200, 0.45, (150, 150, 190), 0.35, k=0.15, bend=260, fade_floor=0.25, lsmooth=2),
                shaded_layer(mid, mb, (28, 28, 62), (54, 52, 96), (19, 20, 46), lt, 220, 0.45, (190, 170, 160), 0.45, k=0.45, ripples=0.03, seed=2, bend=260, fade_floor=0.25, lsmooth=2),
                shaded_layer(near, H, (18, 18, 42), (44, 40, 76), (11, 12, 30), lt, 260, 0.4, GOLD, 0.65, k=1.0, ripples=0.05, seed=3, vdark=0.35, bend=260, fade_floor=0.25, lsmooth=2),
            ]
            self.dust_col = _f((235, 215, 180))
        else:
            self.sky = vgrad([(0, (28, 30, 62)), (0.22, (52, 44, 86)), (0.38, (122, 78, 104)),
                              (0.47, (204, 118, 104)), (0.52, (238, 160, 102)), (0.56, (250, 204, 146)), (1, (250, 210, 160))])
            self.sun_xy = (360, 975)
            g = radial(self.sun_xy[0], self.sun_xy[1], 420, 260, power=1.3)
            self.sky += g[..., None] * _f((70, 52, 18))
            self.stars = Stars(60, 22, 520, 40, bright=0.45, glints=2)
            sun = ss_draw(240, 240, 4, lambda d, k: d.ellipse((50 * k, 50 * k, 190 * k, 190 * k), fill=255))
            self.sun = (sun[..., None] * _f((255, 226, 170)) * 0.92 + cv2.GaussianBlur(sun, (0, 0), 18)[..., None] * _f((255, 190, 120)) * 0.45).astype(np.float32)
            lt = -1.0  # soleil à gauche
            self.layers = [
                shaded_layer(far, fb, (190, 124, 116), (226, 164, 128), (160, 102, 112), lt, 200, 0.45, (255, 220, 170), 0.5, k=0.15, bend=260, fade_floor=0.25, lsmooth=2),
                shaded_layer(mid, mb, (182, 112, 78), (230, 160, 102), (124, 76, 84), lt, 220, 0.45, (255, 214, 150), 0.6, k=0.45, ripples=0.04, seed=2, bend=260, fade_floor=0.25, lsmooth=2),
                shaded_layer(near, H, (134, 78, 58), (214, 140, 86), (78, 46, 58), lt, 260, 0.4, (255, 222, 160), 0.7, k=1.0, ripples=0.06, seed=3, vdark=0.45, bend=260, fade_floor=0.25, lsmooth=2),
            ]
            self.dust_col = _f((255, 228, 180))
        self.dawn = dawn
        # voile de sable : texture périodique qui glisse le long de la crête proche
        rng = np.random.default_rng(5)
        self.haze_tex = np.clip(noise2d(90, 2 * n, 9, 40, 3) * 0.9 + 0.35, 0, 1).astype(np.float32)
        ys = np.arange(90, dtype=np.float32)[:, None]
        self.haze_prof = np.exp(-((ys - 62) / 22) ** 2).astype(np.float32)
        self.parts = [(rng.uniform(0, n), rng.uniform(0.05, 0.16), rng.uniform(0, 1), rng.uniform(0.6, 1.6), rng.uniform(60, 160))
                      for _ in range(70)]

    def frame(self, t, p, ctx=None):
        fr = self.sky.copy()
        if self.dawn:
            add_light(fr, self.sun, self.sun_xy[0] - 120, self.sun_xy[1] - 120)
            self.stars.draw(fr, t, 0.8)
        else:
            self.stars.draw(fr, t)
            add_light(fr, self.moon, self.moon_xy[0] - self.moon_r, self.moon_xy[1] - self.moon_r)
        for L in self.layers:
            comp_layer(fr, L, self.cam, t, p)
        self._sand(fr, t, p)
        return fr

    def _sand(self, fr, t, p):
        """Sable soulevé par le vent : voile qui glisse + grains le long de la crête proche."""
        n = self.near_crest.shape[0]
        s, dx = self.cam.at(1.0, t, p)
        off = int(t * 38) % n
        tex = self.haze_tex[:, off:off + n] * self.haze_prof
        # placement colonne par colonne le long de la crête (échantillonné aux colonnes écran)
        xs = np.arange(W, dtype=np.float32)
        src_x = ((xs - dx - self.cam.fx) / s + self.cam.fx + M).astype(np.int32).clip(0, n - 1)
        crest_scr = s * (self.near_crest[src_x] - self.cam.fy) + self.cam.fy
        ytop = int(crest_scr.min()) - 70
        hgt = int(crest_scr.max() - ytop) + 25
        if ytop < 0 or ytop + hgt > H:
            return
        rows = np.arange(hgt, dtype=np.float32)[:, None] + ytop
        rel = (rows - crest_scr[None, :] + 62).astype(np.int32)   # ligne dans le profil
        ok = (rel >= 0) & (rel < 90)
        relc = rel.clip(0, 89)
        a = np.where(ok, tex[relc, src_x[None, :]], 0) * (0.10 if not self.dawn else 0.13)
        a *= (rows < crest_scr[None, :] + 4)  # seulement au-dessus / sur la crête
        fr[ytop:ytop + hgt] += a[..., None] * (self.dust_col - fr[ytop:ytop + hgt]) * 0.9
        for x0, sp, ph, sz, travel in self.parts:
            age = (t * sp + ph) % 1.0
            xx = (x0 + age * travel * 2.2) % n
            yy = self.near_crest[int(xx)] - 4 - 26 * math.sin(math.pi * age) * (sz / 1.6)
            X = s * (xx - M - self.cam.fx) + self.cam.fx + dx
            Y = s * (yy - self.cam.fy) + self.cam.fy
            al = math.sin(math.pi * age) * 0.5
            xi, yi = int(X), int(Y)
            if 1 <= xi < W - 2 and 1 <= yi < H - 2:
                fr[yi:yi + 2, xi:xi + 2] += (self.dust_col - fr[yi:yi + 2, xi:xi + 2]) * al

class MedineNuit(Decor):
    """Médine au VIIe siècle, la nuit : maisons de terre basses à toits plats, palmiers, mont au loin."""
    name = "medine_nuit"

    def __init__(self):
        n = W + 2 * M
        self.cam = Cam(fy=1000, zoom=0.055, pan=34)
        self.sky = night_sky(horizon=980, warm=0.55)
        self.stars = Stars(170, 31, 900, 60, glints=6)
        self.moon, self.moon_r = crescent(46)
        self.moon_xy = (300, 500)
        mount = ridge_mountains(n, 950, 120, 41, 380, 1.4)
        mount = np.minimum(mount + 40 * np.cos(np.linspace(0, 3, n)), 980)
        self.layers = [shaded_layer(mount, H, (34, 36, 72), (52, 52, 92), (26, 28, 60), -1.0, 120, 0.6,
                                    (120, 120, 170), 0.25, k=0.1, tex=0.05, seed=4)]
        rng = np.random.default_rng(77)
        # plan moyen : bosquet de palmiers + maisons lointaines
        y0m, hm = 700, 450
        rgb = np.zeros((hm, n, 3), np.float32)
        a = np.zeros((hm, n), np.float32)
        midcol = (24, 24, 52)
        for i in range(16):
            ph = rng.uniform(170, 290)
            sp = palm_sprites(ph, 100 + i, midcol, lean=rng.uniform(-0.12, 0.12), fronds=11)
            px = rng.uniform(0, n)
            bake(rgb, a, sp["trunk"], px - sp["base"][0], 1060 - y0m - sp["base"][1] + rng.uniform(-6, 6))
            for key in ("back", "front"):
                bake(rgb, a, sp[key], px - sp["base"][0], 1060 - y0m - sp["base"][1])
        hm_house = self._houses(n, 1075 - y0m, rng, scale=0.55, col=(30, 28, 54), lit=(44, 40, 70), win_p=0.0)
        bake(rgb, a, hm_house, 0, 0)
        a[1060 - y0m:, :] = 1
        rgb[1060 - y0m:, :] = _f(midcol)
        self.layers.append(layer_from_pm(rgb, a, y0m, 0.4))
        # plan proche : maisons de terre avec quelques fenêtres éclairées
        y0n, hn = 740, H - 740
        rgb = np.zeros((hn, n, 3), np.float32)
        a = np.zeros((hn, n), np.float32)
        self.windows = []
        hpm = self._houses(n, 1135 - y0n, rng, scale=1.0, col=(48, 40, 58), lit=(74, 62, 80), win_p=0.35, collect=self.windows,
                           y_off=y0n)
        bake(rgb, a, hpm, 0, 0)
        g0 = 1130 - y0n
        rgb[g0:] = (vgrad([(0, (26, 22, 38)), (1, (12, 12, 24))], hn - g0, n) * 1.0)
        a[g0:] = 1
        self.layers.append(layer_from_pm(rgb, a, y0n, 0.85))
        self.palms = [Palm(-40, 1150, 560, 5, (16, 15, 32), 1.0, amp=1.4, lean=0.12),
                      Palm(990, 1150, 470, 6, (16, 15, 32), 1.0, amp=1.6, lean=-0.1)]
        # halo des fenêtres
        g = radial(40, 40, 26, 26, 80, 80, power=1.6)
        self.win_glow = fade_edges((g[..., None] * _f((255, 176, 90))).astype(np.float32))

    def _houses(self, n, ground, rng, scale, col, lit, win_p, collect=None, y_off=0):
        """Rangée de maisons cubiques en terre (toits plats, petit parapet, poutres apparentes)."""
        hh = int(ground + 5)
        k = 3
        img = Image.new("RGBA", (n * k, hh * k), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        x = rng.uniform(-60, 0)
        colw = tuple(int(c) for c in col) + (255,)
        cols = tuple(int(c) for c in lit) + (255,)
        dark = tuple(int(c * 0.55) for c in col) + (255,)
        winlit = (238, 176, 96, 255)
        while x < n:
            w = rng.uniform(130, 250) * scale
            h = rng.uniform(95, 190) * scale * (1.35 if rng.uniform() < 0.25 else 1)
            top = ground - h
            d.rectangle((x * k, top * k, (x + w) * k, ground * k), fill=colw)
            # face latérale éclairée par la lune (à gauche)
            sw = w * 0.14
            d.rectangle((x * k, top * k, (x + sw) * k, ground * k), fill=cols)
            # parapet bas sur une partie du toit
            if rng.uniform() < 0.6:
                px0 = x + rng.uniform(0, w * 0.3)
                d.rectangle((px0 * k, (top - 8 * scale) * k, (px0 + w * rng.uniform(0.4, 0.7)) * k, top * k), fill=colw)
            # liseré de lune sur l'arête du toit
            d.rectangle((x * k, top * k, (x + w) * k, (top + 2.2 * scale) * k), fill=(96, 86, 110, 255))
            # poutres de palmier apparentes sous le toit
            if rng.uniform() < 0.7:
                bx = x + 10 * scale
                while bx < x + w - 8 * scale:
                    d.rectangle((bx * k, (top + 9 * scale) * k, (bx + 4 * scale) * k, (top + 13 * scale) * k), fill=dark)
                    bx += 19 * scale
            # porte
            if rng.uniform() < 0.6 and h > 80 * scale:
                dx_ = x + rng.uniform(0.3, 0.7) * w
                dw, dh = 26 * scale, 52 * scale
                d.rectangle(((dx_ - dw / 2) * k, (ground - dh) * k, (dx_ + dw / 2) * k, ground * k), fill=dark)
            # fenêtres (jamais par paires symétriques au-dessus d'une porte)
            if win_p > 0:
                nw = int(rng.integers(0, 3))
                used = []
                for _ in range(nw):
                    wx = x + rng.uniform(0.18, 0.82) * w
                    if any(abs(wx - u) < 40 * scale for u in used):
                        continue
                    used.append(wx)
                    wy = top + rng.uniform(0.28, 0.5) * h
                    ww, wh = 13 * scale, 18 * scale
                    lit_on = rng.uniform() < win_p
                    d.rectangle(((wx - ww / 2) * k, (wy - wh / 2) * k, (wx + ww / 2) * k, (wy + wh / 2) * k),
                                fill=winlit if lit_on else dark)
                    if lit_on and collect is not None:
                        collect.append((wx - M, wy + y_off, rng.uniform(0, 6.28), rng.uniform(0.7, 1.0)))
            x += w + rng.uniform(-30, 20) * scale
        img = img.resize((n, hh), Image.LANCZOS)
        return pil_premult(img)

    def frame(self, t, p, ctx=None):
        fr = self.sky.copy()
        self.stars.draw(fr, t)
        add_light(fr, self.moon, self.moon_xy[0] - self.moon_r, self.moon_xy[1] - self.moon_r)
        for L in self.layers:
            comp_layer(fr, L, self.cam, t, p)
        for x, y, ph, b in self.windows:
            X, Y, sc = self.cam.pt(0.85, t, p, x, y)
            fl = 0.75 + 0.12 * math.sin(t * 2.3 + ph) + 0.06 * math.sin(t * 5.1 + 2 * ph)
            add_light(fr, self.win_glow, int(X) - 40, int(Y) - 40, 0.45 * b * fl)
        for pm in self.palms:
            pm.draw(fr, self.cam, t, p)
        return fr

class KaabaLoin(Decor):
    """La Kaaba vue de loin, la nuit, au fond d'une vallée entourée de montagnes rocheuses. Rien d'autre de construit."""
    name = "kaaba_loin"

    def __init__(self):
        n = W + 2 * M
        self.cam = Cam(fx=CX, fy=1010, zoom=0.07, pan=26)
        self.sky = night_sky(horizon=900, warm=0.45)
        self.stars = Stars(230, 51, 860, 40, glints=7)
        self.moon, self.moon_r = crescent(44)
        self.moon_xy = (790, 430)
        far = ridge_mountains(n, 860, 140, 61, 300, 1.2)
        xs = np.arange(n, dtype=np.float32) - (CX + M)
        env = np.clip(np.abs(xs) / 560, 0, 1.25) ** 1.25
        mid = 1000 - 360 * env + ridge_mountains(n, 0, 70, 62, 160, 1.0)
        mid = np.minimum(mid, 1030)
        nearL = 1190 - 640 * np.clip((-(xs) - 250) / 380, 0, 1.4) ** 1.1 + ridge_mountains(n, 0, 40, 63, 160, 1.0)
        nearR = 1190 - 580 * np.clip(((xs) - 270) / 400, 0, 1.4) ** 1.1 + ridge_mountains(n, 0, 40, 64, 160, 1.0)
        near = np.minimum(nearL, nearR)
        near = np.minimum(near, 1170 + noise1d(n, 65, 160, 3) * 10)
        self.layers = [
            shaded_layer(far, int(mid.max()) + 90, (34, 38, 78), (52, 54, 96), (26, 30, 66), 1.0, 90, 0.9, (130, 130, 175), 0.3,
                         k=0.1, tex=0.06, seed=5, lsmooth=3),
            shaded_layer(mid, 1090, (24, 26, 56), (44, 44, 84), (16, 18, 42), 1.0, 80, 0.9, (170, 160, 170), 0.4, k=0.4,
                         tex=0.08, seed=6, lsmooth=4, haze=(900, 1012, (54, 50, 74), 0.75)),
        ]
        # fond de vallée (sol de sable et de cailloux, légèrement ondulé) + Kaaba, au même plan
        y0, hv = 940, 1260 - 940
        fcrest = 1004 + noise1d(n, 66, 220, 3) * 5 - 26 * np.clip((np.abs(xs) - 300) / 300, 0, 1) ** 1.5
        fl = shaded_layer(fcrest, y0 + hv, (50, 44, 60), (58, 50, 66), (40, 36, 54), 1.0, 60, 0.5, (120, 110, 130), 0.35,
                          k=0.6, tex=0.06, seed=16, fade_floor=0.0)
        img = fl.img.astype(np.float32)
        rgb = np.zeros((hv, n, 3), np.float32)
        a = np.zeros((hv, n), np.float32)
        oy = fl.y0 - y0
        rgb[oy:] = img[:hv - oy, :, :3]
        a[oy:] = img[:hv - oy, :, 3] / 255
        ys = np.arange(hv, dtype=np.float32)[:, None, None] + y0
        rgb *= np.interp(ys, [1000, 1080, 1260], [1.0, 0.8, 0.55])
        kab = self._kaaba()
        self.kx, self.ky = CX, 1024      # pied de la Kaaba
        kh, kw = kab.shape[:2]
        bake(rgb, a, kab, self.kx + M - kw / 2, self.ky - y0 - kh + 8)
        self.layers.append(layer_from_pm(rgb, a, y0, 0.6))
        self.layers.append(shaded_layer(near, H, (16, 16, 36), (36, 34, 66), (10, 11, 26), 1.0, 45, 0.5, (190, 170, 150), 0.45,
                                        k=1.0, tex=0.12, seed=7, vdark=0.35, lsmooth=14, fade_floor=0.0))
        g = radial(110, 60, 150, 46, 220, 120, power=1.4)
        self.glow = fade_edges((g[..., None] * _f((200, 160, 90))).astype(np.float32))
        gb = radial(60, 10, 34, 5, 120, 20, power=1.5)
        self.band_glint = fade_edges((gb[..., None] * _f((255, 220, 150))).astype(np.float32))

    def _kaaba(self):
        """Cube noir, deux faces visibles, bande dorée (hizam) au tiers supérieur, porte dorée."""
        fw, sw, h = 68, 30, 82
        k = 4
        Wd, Hd = fw + sw + 4, h + 10
        img = Image.new("RGBA", (Wd * k, Hd * k), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        top = 4
        # ombre portée au sol
        d.ellipse((-6 * k, (top + h - 4) * k, (Wd + 10) * k, (top + h + 6) * k), fill=(10, 10, 20, 150))
        d.rectangle((2 * k, top * k, (2 + fw) * k, (top + h) * k), fill=(12, 12, 16, 255))
        d.polygon([((2 + fw) * k, top * k), ((2 + fw + sw) * k, (top + 3) * k), ((2 + fw + sw) * k, (top + h - 1) * k),
                   ((2 + fw) * k, (top + h) * k)], fill=(26, 26, 34, 255))
        # arête supérieure à peine éclairée par la lune
        d.line((2 * k, top * k, (2 + fw) * k, top * k), fill=(70, 70, 90, 255), width=k)
        d.line(((2 + fw) * k, top * k, (2 + fw + sw) * k, (top + 3) * k), fill=(80, 80, 100, 255), width=k)
        # bande dorée
        by, bh = top + h * 0.2, 7.5
        d.rectangle((2 * k, by * k, (2 + fw) * k, (by + bh) * k), fill=GOLD + (255,))
        d.polygon([((2 + fw) * k, by * k), ((2 + fw + sw) * k, (by + 1.4) * k), ((2 + fw + sw) * k, (by + bh + 1.2) * k),
                   ((2 + fw) * k, (by + bh) * k)], fill=(176, 144, 84, 255))
        # porte dorée (surélevée), sur la face avant
        dx0 = 2 + fw * 0.66
        d.rectangle((dx0 * k, (top + h * 0.5) * k, (dx0 + 9) * k, (top + h * 0.82) * k), fill=(120, 96, 56, 255))
        img = img.resize((Wd, Hd), Image.LANCZOS)
        return pil_premult(img)

    def frame(self, t, p, ctx=None):
        fr = self.sky.copy()
        self.stars.draw(fr, t)
        add_light(fr, self.moon, self.moon_xy[0] - self.moon_r, self.moon_xy[1] - self.moon_r)
        for i, L in enumerate(self.layers):
            comp_layer(fr, L, self.cam, t, p)
            if i == 2:   # après le fond de vallée : douce lueur + reflet sur la bande dorée
                X, Y, sc = self.cam.pt(0.6, t, p, self.kx, self.ky)
                add_light(fr, self.glow, int(X) - 110, int(Y) - 70, 0.12)
                add_light(fr, self.band_glint, int(X) - 62 + int(16 * math.sin(t * 0.5)), int(Y - 66 * sc) - 10,
                          0.18 + 0.08 * math.sin(t * 1.1))
        return fr

def flicker(t, seed=0.0):
    return (0.45 * math.sin(t * 11.3 + seed) + 0.3 * math.sin(t * 7.1 + 1.3 + seed) + 0.25 * math.sin(t * 17.9 + 2.1 + seed))

class Lanterne(Decor):
    """Gros plan d'une lanterne à huile ancienne posée sur un rebord, flamme vivante, halo."""
    name = "lanterne"

    def __init__(self):
        self.cam = Cam(fx=CX, fy=800, zoom=0.07, pan=14)
        self.base_y = 1080
        wall = vgrad([(0, (8, 12, 30)), (0.4, (16, 18, 42)), (0.56, (26, 24, 46)), (1, (14, 14, 30))])
        tex = noise2d(H, W, 3, 120, 4)
        wall *= (1 + 0.05 * tex)[..., None]
        self.sky = wall
        # rebord (bois sombre) au premier plan
        n = W + 2 * M
        y0 = self.base_y - 6
        hh = H - y0
        top = vgrad([(0, (78, 56, 44)), (0.04, (58, 40, 34)), (0.25, (36, 26, 26)), (1, (16, 13, 18))], hh, n)
        grain = noise2d(hh, n, 8, 40, 3)
        grain = np.sin(np.arange(n)[None, :] * 0.012 + grain * 6 + np.arange(hh)[:, None] * 0.0) * 0.5 + grain * 0.5
        top *= (1 + 0.06 * grain)[..., None]
        a = np.ones((hh, n), np.float32)
        a[:2] = 0.0
        top[2:5] = top[2:5] * 0.4 + _f((150, 110, 70)) * 0.6
        self.layers = [Layer(premult(top, a), y0, 0.8)]
        self.lamp, self.lamp_anchor, self.glass = self._lantern()
        self.halo = fade_edges((radial(500, 500, 360, 360, 1000, 1000, power=1.3)[..., None] * _f((255, 170, 90))).astype(np.float32), 0.3)
        self.halo2 = fade_edges((radial(180, 180, 95, 95, 360, 360, power=1.6)[..., None] * _f((255, 214, 150))).astype(np.float32), 0.3)
        self.pool = fade_edges((radial(360, 70, 330, 50, 720, 140, power=1.6)[..., None] * _f((255, 170, 90))).astype(np.float32), 0.3)
        rng = np.random.default_rng(9)
        self.motes = [(rng.uniform(-260, 260), rng.uniform(0, 1), rng.uniform(0.03, 0.08), rng.uniform(0, 6.28), rng.uniform(0.6, 1.6))
                      for _ in range(26)]
        self.LS = 1.3                                  # échelle de la lanterne (gros plan)
        self.flame_y = self.base_y - 110 * self.LS     # pied de la flamme = haut de la mèche

    def _lantern(self):
        """Lanterne en laiton : pied, cage à 3 montants et vitres, toit conique à pointe, anneau."""
        k = 3
        w, h = 340, 640
        img = Image.new("RGBA", (w * k, h * k), (0, 0, 0, 0))
        glass = Image.new("L", (w * k, h * k), 0)
        d, dg = ImageDraw.Draw(img), ImageDraw.Draw(glass)
        cx = w / 2
        br = (150, 104, 48, 255); brl = (214, 166, 92, 255); brd = (92, 62, 32, 255)
        S = lambda *v: tuple(x * k for x in v)
        base = h - 6
        # pied
        d.polygon([S(cx - 120, base), S(cx + 120, base), S(cx + 100, base - 26), S(cx - 100, base - 26)], fill=brd)
        d.rectangle(S(cx - 100, base - 40, cx + 100, base - 26), fill=br)
        d.rectangle(S(cx - 100, base - 40, cx + 100, base - 37), fill=brl)
        # vitres (cage)
        gt, gb = base - 330, base - 40
        dg.rectangle(S(cx - 92, gt, cx + 92, gb), fill=255)
        d.rectangle(S(cx - 92, gt, cx + 92, gb), fill=(255, 196, 120, 70))
        # réservoir et mèche
        d.ellipse(S(cx - 46, gb - 52, cx + 46, gb - 4), fill=(110, 76, 38, 255))
        d.ellipse(S(cx - 46, gb - 52, cx + 46, gb - 34), fill=(170, 124, 62, 255))
        d.rectangle(S(cx - 5, gb - 72, cx + 5, gb - 46), fill=(70, 50, 30, 255))
        # montants (3 visibles) + arcs brisés en haut de chaque vitre
        for xm in (cx - 92, cx, cx + 92):
            d.rectangle(S(xm - 7, gt, xm + 7, gb), fill=br)
            d.rectangle(S(xm - 7, gt, xm - 3, gb), fill=brl)
        for x0, x1 in ((cx - 85, cx - 7), (cx + 7, cx + 85)):
            m = (x0 + x1) / 2
            pts = [S(x0, gt + 60)]
            for i in range(11):
                u = i / 10
                pts.append(S(x0 + (m - x0) * u, gt + 60 - 46 * math.sin(u * math.pi / 2) ** 0.8))
            for i in range(11):
                u = i / 10
                pts.append(S(m + (x1 - m) * u, gt + 14 + 46 * (1 - math.cos(u * math.pi / 2)) ** 1.25))
            pts += [S(x1, gt), S(x0, gt)]
            d.polygon(pts, fill=br)
            dg.polygon(pts, fill=0)
        d.rectangle(S(cx - 104, gb - 4, cx + 104, gb + 4), fill=br)
        d.rectangle(S(cx - 104, gt - 16, cx + 104, gt), fill=br)
        d.rectangle(S(cx - 104, gt - 16, cx + 104, gt - 12), fill=brl)
        # toit conique ajouré (petites ouvertures)
        rt = gt - 16
        d.polygon([S(cx - 104, rt), S(cx + 104, rt), S(cx + 14, rt - 120), S(cx - 14, rt - 120)], fill=br)
        d.polygon([S(cx - 104, rt), S(cx - 70, rt), S(cx - 8, rt - 120), S(cx - 14, rt - 120)], fill=brl)
        for i in range(-2, 3):
            ox = cx + i * 30
            d.ellipse(S(ox - 5, rt - 40, ox + 5, rt - 30), fill=(255, 190, 110, 200))
        d.rectangle(S(cx - 18, rt - 132, cx + 18, rt - 120), fill=brd)
        d.polygon([S(cx - 10, rt - 132), S(cx + 10, rt - 132), S(cx, rt - 176)], fill=br)
        # anneau de suspension
        d.ellipse(S(cx - 26, rt - 236, cx + 26, rt - 172), outline=br, width=8 * k)
        d.arc(S(cx - 26, rt - 236, cx + 26, rt - 172), 150, 260, fill=brl, width=3 * k)
        img = img.resize((w, h), Image.LANCZOS)
        glass = np.asarray(glass.resize((w, h), Image.LANCZOS)).astype(np.float32) / 255
        return pil_premult(img), (cx, base), glass

    def _flame(self, t):
        """Flamme en goutte, hauteur et pointe qui vacillent ; renvoie lumière float32 (h, w, 3)."""
        fw, fh = 70, 150
        f1, f2 = flicker(t), flicker(t * 0.83, 2.0)
        hgt = 92 * (1 + 0.07 * f1)
        wid = 19 * (1 - 0.04 * f1)
        sway = 5.5 * f2
        k = 3
        def shape(scale_h, scale_w):
            pts = []
            for i in range(60):
                th = 2 * math.pi * i / 60
                yv = math.cos(th)                       # 1 bas … -1 haut
                xv = math.sin(th) * (math.sin(th / 2) ** 1.6)
                up = (1 - yv) / 2                        # 0 bas … 1 pointe
                X = fw / 2 + xv * wid * scale_w + sway * up ** 2
                Y = fh - 18 - up * hgt * scale_h
                pts.append((X * k, Y * k))
            return pts
        outer = ss_draw(fw, fh, k, lambda d, k_: d.polygon(shape(1.0, 1.0), fill=255))
        inner = ss_draw(fw, fh, k, lambda d, k_: d.polygon(shape(0.55, 0.5), fill=255))
        outer = cv2.GaussianBlur(outer, (0, 0), 1.2)
        rgb = outer[..., None] * _f((255, 150, 60)) * 0.95 + inner[..., None] * _f((255, 236, 196))
        rgb += cv2.GaussianBlur(outer, (0, 0), 8)[..., None] * _f((255, 150, 70)) * 0.5
        return rgb.astype(np.float32), (fw / 2, fh - 18)

    def frame(self, t, p, ctx=None):
        fr = self.sky.copy()
        f1 = flicker(t * 0.7, 1.0)
        inten = 1.0 + 0.06 * f1
        fx, fy, sc = self.cam.pt(1.0, t, p, CX, self.flame_y)
        # halo sur le mur
        comp = self.halo
        add_light(fr, comp, int(fx) - 500, int(fy) - 500 - 70, 0.42 * inten)
        for L in self.layers:
            comp_layer(fr, L, self.cam, t, p)
        bx, by, _ = self.cam.pt(0.8, t, p, CX, self.base_y)
        add_light(fr, self.pool, int(bx) - 360, int(by) - 50, 0.45 * inten)
        ax, ay = self.lamp_anchor
        X, Y, sc = self.cam.pt(1.0, t, p, CX, self.base_y)
        comp_sprite(fr, self.lamp, ax, ay, X, Y, sc * self.LS)
        # vitres éclairées par la flamme
        gl = (self.glass[..., None] * _f((255, 180, 100)) * 0.16 * inten).astype(np.float32)
        comp_sprite(fr, gl, ax, ay, X, Y, sc * self.LS, light=True)
        fl, (fax, fay) = self._flame(t)
        comp_sprite(fr, fl, fax, fay, fx, fy, sc * self.LS, light=True)
        add_light(fr, self.halo2, int(fx) - 180, int(fy) - 180 - int(55 * self.LS), 0.5 * inten)
        # poussières dans la lumière
        for x0, ph, sp, ph2, sz in self.motes:
            u = (ph + t * sp) % 1.0
            mx = fx + x0 * sc + 18 * math.sin(t * 0.4 + ph2)
            my = fy + 160 - u * 640
            dist = math.hypot(mx - fx, my - fy) / 300
            al = 0.35 * math.sin(math.pi * u) * max(0.0, 1 - dist)
            xi, yi = int(mx), int(my)
            if al > 0.02 and 1 <= xi < W - 2 and 1 <= yi < H - 2:
                fr[yi:yi + 2, xi:xi + 2] += _f((255, 214, 160)) * al
        return fr

class TracesSable(Decor):
    """Traces de pas dans le sable qui apparaissent une à une vers l'horizon (aucune personne)."""
    name = "traces_sable"

    def __init__(self):
        n = W + 2 * M
        self.horizon = 800
        self.cam = Cam(fx=CX + 40, fy=830, zoom=0.07, pan=22)
        self.sky = vgrad([(0, (9, 13, 36)), (0.22, (22, 24, 58)), (0.34, (66, 52, 92)), (0.40, (150, 96, 102)),
                          (0.43, (214, 146, 104)), (1, (214, 146, 104))])
        self.stars = Stars(110, 71, 600, 40, bright=0.8, glints=4)
        self.moon, self.moon_r = crescent(30, phase=0.36)
        self.moon_xy = (770, 560)
        far = crest_dunes(n, 808, [(240, 40, 300, 180), (700, 55, 360, 200), (1150, 36, 280, 170)], 81, 3)
        self.layers = [shaded_layer(far, H, (118, 76, 84), (160, 104, 100), (96, 62, 78), -1.0, 120, 0.8,
                                    (240, 180, 140), 0.4, k=0.15)]
        # sol : plan presque plat, plus chaud et plus clair au premier plan
        y0 = 820
        hh = H - y0
        crest = 840 + noise1d(n, 82, 500, 3) * 6 - 20 * np.exp(-((np.arange(n) - 1100) / 300) ** 2)
        gl = shaded_layer(crest, H, (150, 100, 84), (178, 122, 94), (132, 88, 80), -1.0, 600, 0.3, (240, 186, 140), 0.5,
                          k=0.75, ripples=0.05, seed=8)
        # dégradé de profondeur sur le sol
        img = gl.img.astype(np.float32)
        ys = np.arange(gl.y0, gl.y0 + img.shape[0], dtype=np.float32)
        warm = np.interp(ys, [840, 1000, 1300, 1920], [0.92, 1.05, 1.12, 0.7])[:, None, None]
        img[..., :3] = np.clip(img[..., :3] * warm, 0, 255)
        gl.img = img.astype(np.uint8)
        self.ground = gl
        self.layers.append(gl)
        self.prints = self._prints()

    def _prints(self):
        """Empreintes en perspective (pied nu stylisé : semelle + talon, en creux), le long d'un chemin courbe."""
        K = 300.0
        hz = self.horizon + 18
        out = []
        z = 1.0
        side = 1
        i = 0
        while True:
            y = hz + K / z
            if y < hz + 22:
                break
            X = 0.55 * math.sin(z * 0.33 + 0.4) - 0.25
            x = CX + 40 + (X + side * 0.05) * 640 / z
            L = 110 / z
            out.append((x, y, L, side, i))
            z *= 1.13 if z < 3 else 1.1
            side = -side
            i += 1
        sprites = []
        for x, y, L, side, i in out:
            spr = self._print_sprite(L, side)
            sprites.append((x, y, spr, i))
        self.n_prints = len(sprites)
        return sprites

    def _print_sprite(self, L, side):
        """Empreinte de pied nu stylisée (contour allongé, voûte plantaire), en creux : bord supérieur dans
        l'ombre, bord inférieur éclairé. side = ±1 (pied gauche/droit, légère rotation vers l'extérieur)."""
        k = 4
        fore = 0.72                       # raccourci de perspective (sol vu en biais)
        ww = int(L * 0.62) + 10
        hh = int(L * fore * 1.05) + 10
        def fn(d, k):
            cx, cy = ww / 2, hh / 2
            pts = []
            # contour paramétrique d'une plante de pied (avant en haut, vers l'horizon)
            for i in range(48):
                th = 2 * math.pi * i / 48
                v = -math.cos(th)            # -1 talon (bas) … +1 orteils (haut)
                width = 0.17 + 0.07 * (v + 1) / 2 - 0.05 * math.exp(-((v + 0.05) / 0.35) ** 2)
                if math.sin(th) * side < 0:  # voûte plantaire du côté intérieur
                    width -= 0.04 * math.exp(-((v + 0.05) / 0.3) ** 2)
                x = cx + math.sin(th) * width * L
                y = cy - v * 0.48 * L * fore
                pts.append((x * k, y * k))
            d.polygon(pts, fill=255)
        m = ss_draw(ww, hh, k, fn)
        m = cv2.GaussianBlur(m, (0, 0), max(0.5, L / 70))
        sh = max(1, int(L / 28))
        top_wall = np.clip(m - np.roll(m, -sh, axis=0), 0, 1)     # bord haut (ombre)
        bot_wall = np.clip(m - np.roll(m, sh, axis=0), 0, 1)      # bord bas (lumière)
        a = np.clip(m * 0.28 + top_wall * 0.55, 0, 1)
        dark = _f((88, 54, 56))
        rgb_pm = dark[None, None, :] * a[..., None] + _f((250, 206, 156))[None, None, :] * (bot_wall * 0.45)[..., None]
        a = np.clip(a + bot_wall * 0.45, 0, 1)
        out = np.empty((hh, ww, 4), np.uint8)
        out[..., :3] = np.clip(rgb_pm, 0, 255)
        out[..., 3] = np.clip(a * 255, 0, 255)
        if side:
            M_ = cv2.getRotationMatrix2D((ww / 2, hh / 2), -7 * side, 1.0)
            out = cv2.warpAffine(out, M_, (ww, hh), flags=cv2.INTER_LINEAR)
        return out

    def frame(self, t, p, ctx=None):
        fr = self.sky.copy()
        self.stars.draw(fr, t, 0.9)
        add_light(fr, self.moon, self.moon_xy[0] - self.moon_r, self.moon_xy[1] - self.moon_r, 0.9)
        for L in self.layers:
            comp_layer(fr, L, self.cam, t, p)
        n = self.n_prints
        for x, y, spr, i in self.prints:
            p_in = 0.04 + 0.66 * i / max(1, n - 1)
            a = smooth((p - p_in) / 0.035)
            if a <= 0.01:
                continue
            X, Y, sc = self.cam.pt(0.75, t, p, x, y)
            h, w = spr.shape[:2]
            comp_sprite(fr, spr, w / 2, h / 2, X, Y, sc, gain=a)
        return fr

class Parchemin(Decor):
    """Un parchemin qui se déroule (rouleaux de bois aux embouts dorés) ; le texte s'y écrit."""
    name = "parchemin"
    BOX = (140, 470, 900, 1110)   # x0, y0, x1, y1 de la feuille une fois déroulée

    def __init__(self):
        self.cam = Cam(fx=CX, fy=790, zoom=0.035, pan=10)
        sky = night_sky(horizon=1300, warm=0.9)
        self.sky = sky
        self.stars = Stars(120, 91, 1300, 40, bright=0.7, glints=4)
        x0, y0, x1, y1 = self.BOX
        w, h = x1 - x0, y1 - y0
        self.sw, self.sh = w, h
        base = np.ones((h, w, 3), np.float32) * _f((238, 222, 190))
        nz = noise2d(h, w, 12, 90, 4)
        nz2 = noise2d(h, w, 13, 14, 2)
        base *= (1 + 0.05 * nz + 0.025 * nz2)[..., None]
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        edge = np.minimum(np.minimum(xx, w - 1 - xx) / 60, 1) * np.minimum(np.minimum(yy, h - 1 - yy) / 40, 1)
        vign = 0.78 + 0.22 * smooth(edge)
        base *= vign[..., None]
        base = base * (1 - (1 - vign[..., None]) * 0.0) + (_f((150, 100, 60)) - base) * ((1 - vign) * 0.45)[..., None]
        # bords légèrement irréguliers à gauche et à droite
        jag = noise1d(h, 14, 30, 3) * 3
        a = np.ones((h, w), np.float32)
        a *= np.clip(xx - 4 - jag[:, None], 0, 1) * np.clip(w - 5 - xx - jag[::-1, None], 0, 1)
        # filet doré décoratif
        img = Image.new("L", (w * 3, h * 3), 0)
        d = ImageDraw.Draw(img)
        d.rectangle((30 * 3, 34 * 3, (w - 30) * 3, (h - 34) * 3), outline=255, width=6)
        d.rectangle((40 * 3, 44 * 3, (w - 40) * 3, (h - 44) * 3), outline=255, width=2)
        fil = np.asarray(img.resize((w, h), Image.LANCZOS)).astype(np.float32) / 255
        base = base * (1 - fil[..., None] * 0.7) + _f((178, 130, 60)) * (fil[..., None] * 0.7)
        self.sheet = premult(base, a)
        self.roller = self._roller(w + 70)
        sh = np.zeros((h + 80, w + 80), np.float32)
        sh[40:-40, 40:-40] = 1
        sh = cv2.GaussianBlur(sh, (0, 0), 18)
        self.shadow = sh
        rng = np.random.default_rng(10)
        self.motes = [(rng.uniform(0, W), rng.uniform(300, 1400), rng.uniform(0, 6.28), rng.uniform(4, 10)) for _ in range(30)]

    def _roller(self, length):
        k = 3
        h = 40
        img = Image.new("RGBA", ((length + 40) * k, h * k), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        for i in range(h - 12):
            u = i / (h - 13)
            c = 0.55 + 0.6 * math.sin(math.pi * (0.2 + 0.8 * u)) - 0.25 * u
            col = (int(110 * c), int(70 * c), int(40 * c), 255)
            d.rectangle((20 * k, (6 + i) * k, (length + 20) * k, (7 + i) * k), fill=col)
        for ex in (6, length + 22):
            d.ellipse(((ex - 8) * k, 0, (ex + 12) * k, h * k), fill=(196, 156, 84, 255))
            d.ellipse(((ex - 4) * k, 6 * k, (ex + 4) * k, 18 * k), fill=(246, 214, 150, 255))
        img = img.resize((length + 40, h), Image.LANCZOS)
        return pil_premult(img)

    def unroll(self, t):
        return ease_io((t - 0.15) / 1.6)

    def frame(self, t, p, ctx=None):
        fr = self.sky.copy()
        self.stars.draw(fr, t, 0.7)
        x0, y0, x1, y1 = self.BOX
        u = self.unroll(t)
        shown = max(2, int(self.sh * u))
        s, dx = self.cam.at(1.0, t, p)
        def P(x, y):
            return s * (x - self.cam.fx) + self.cam.fx + dx, s * (y - self.cam.fy) + self.cam.fy
        # ombre douce sous la feuille
        shd = self.shadow[:shown + 80]
        sx, sy = P(x0 - 40 + 12, y0 - 40 + 22)
        sh = np.zeros(shd.shape + (4,), np.uint8)
        sh[..., 3] = np.clip(shd * 150, 0, 255)
        comp_sprite(fr, sh, 0, 0, sx, sy, s)
        # feuille : on prend le haut (déroulé du haut vers le bas)
        sheet = self.sheet[:shown].copy()
        if ctx and ctx.get("texts"):
            self._write(sheet, ctx["texts"])
        X, Y = P(x0, y0)
        comp_sprite(fr, sheet, 0, 0, X, Y, s)
        # rouleaux : haut fixe, bas qui descend
        rl = self.roller
        rx, ry = P(x0 - 55, y0 - 24)
        comp_sprite(fr, rl, 0, 0, rx, ry, s)
        rx, ry = P(x0 - 55, y0 + shown - 16)
        comp_sprite(fr, rl, 0, 0, rx, ry, s)
        for mx, my, ph, sp in self.motes:
            xx = mx + 30 * math.sin(t / sp + ph)
            yy = my - (t * 8 + ph * 40) % 200
            al = 0.18 * (0.5 + 0.5 * math.sin(t * 0.8 + ph))
            xi, yi = int(xx), int(yy)
            if 1 <= xi < W - 2 and 1 <= yi < H - 2:
                fr[yi:yi + 2, xi:xi + 2] += _f((255, 220, 170)) * al
        return fr

    def _write(self, sheet, texts):
        """texts : [(img uint8 RGBA alpha droit, x, y dans la feuille, reveal 0..1, rtl, alpha, hauteur de ligne,
        décalage de la 1re coupure)] ; l'écriture progresse ligne par ligne (droite→gauche si rtl)."""
        for img, x, y, rev, rtl, alpha, lh, off in texts:
            if rev <= 0 or alpha <= 0.01:
                continue
            h, w = img.shape[:2]
            nl = max(1, int(h / lh))
            mask = np.zeros((h, w), np.float32)
            # écriture ligne par ligne, avec un bord doux de 24 px
            tot = rev * nl
            xs = np.arange(w, dtype=np.float32)
            for li in range(nl):
                fr_ = min(max(tot - li, 0.0), 1.0)
                if fr_ <= 0:
                    break
                ya = 0 if li == 0 else int(li * lh + off)
                yb = h if li == nl - 1 else int((li + 1) * lh + off)
                edge = fr_ * (w + 24)
                if rtl:
                    m = np.clip((xs - (w - edge)) / 24 + 1, 0, 1)
                else:
                    m = np.clip((edge - xs) / 24, 0, 1)
                mask[ya:yb] = m[None, :]
            a = img[..., 3].astype(np.float32) / 255 * mask * alpha
            sx0, sy0 = int(x), int(y)
            sx1, sy1 = min(sheet.shape[1], sx0 + w), min(sheet.shape[0], sy0 + h)
            if sx1 <= sx0 or sy1 <= sy0:
                continue
            a = a[:sy1 - sy0, :sx1 - sx0]
            reg = sheet[sy0:sy1, sx0:sx1].astype(np.float32)
            col = img[:sy1 - sy0, :sx1 - sx0, :3].astype(np.float32)
            reg[..., :3] = reg[..., :3] * (1 - a[..., None]) + col * a[..., None] * (reg[..., 3:4] / 255)
            sheet[sy0:sy1, sx0:sx1] = np.clip(reg, 0, 255).astype(np.uint8)

class Palmeraie(Decor):
    """Palmiers au vent au coucher du soleil, sur 3 plans."""
    name = "palmeraie"

    def __init__(self):
        n = W + 2 * M
        self.cam = Cam(fx=CX, fy=1000, zoom=0.06, pan=40)
        self.sky = vgrad([(0, (24, 26, 58)), (0.2, (48, 40, 84)), (0.36, (118, 68, 104)), (0.46, (206, 106, 88)),
                          (0.515, (244, 160, 92)), (0.545, (252, 204, 140)), (1, (252, 204, 140))])
        self.sun_xy = (CX + 40, 1035)
        g = radial(self.sun_xy[0], self.sun_xy[1], 520, 300, power=1.2)
        self.sky += g[..., None] * _f((60, 40, 12))
        sun = ss_draw(300, 300, 4, lambda d, k: d.ellipse((60 * k, 60 * k, 240 * k, 240 * k), fill=255))
        self.sun = (sun[..., None] * _f((255, 228, 170)) * 0.9 + cv2.GaussianBlur(sun, (0, 0), 22)[..., None] * _f((255, 180, 110)) * 0.5).astype(np.float32)
        self.stars = Stars(40, 101, 420, 40, bright=0.4, glints=2)
        rng = np.random.default_rng(111)
        # plan lointain : ligne de palmiers + sol, couleur brumeuse
        y0f, hf = 760, H - 760
        rgb = np.zeros((hf, n, 3), np.float32)
        a = np.zeros((hf, n), np.float32)
        farcol = (128, 66, 82)
        for i in range(26):
            ph = rng.uniform(110, 200)
            sp = palm_sprites(ph, 200 + i, farcol, lean=rng.uniform(-0.14, 0.14), fronds=11)
            px = rng.uniform(-40, n + 40)
            gy = 1050 - y0f + rng.uniform(-4, 4)
            for key in ("trunk", "back", "front"):
                bake(rgb, a, sp[key], px - sp["base"][0], gy - sp["base"][1])
        g0 = 1046 - y0f
        rgb[g0:] = vgrad([(0, farcol), (1, (60, 30, 50))], hf - g0, n)
        a[g0:] = 1
        self.layers = [layer_from_pm(rgb, a, y0f, 0.2)]
        # sol du plan moyen
        crest = 1110 + noise1d(n, 112, 400, 3) * 10
        self.layers.append(shaded_layer(crest, H, (64, 32, 52), (96, 50, 62), (50, 26, 46), -1.0, 200, 0.5,
                                        (250, 180, 120), 0.5, k=0.5))
        crest2 = 1230 + noise1d(n, 113, 400, 3) * 14
        self.near_ground = shaded_layer(crest2, H, (30, 18, 36), (44, 26, 44), (22, 14, 30), -1.0, 200, 0.5,
                                        (230, 150, 110), 0.4, k=1.0)
        midcol = (70, 36, 60)
        self.palms_mid = [Palm(x, 1118, h_, 300 + i, midcol, 0.5, amp=2.2, lean=l)
                          for i, (x, h_, l) in enumerate([(120, 420, 0.1), (330, 360, -0.06), (690, 470, 0.08), (880, 380, -0.1)])]
        nearcol = (28, 16, 34)
        self.palms_near = [Palm(-30, 1250, 820, 401, nearcol, 1.0, amp=2.6, lean=0.16),
                           Palm(1060, 1250, 720, 402, nearcol, 1.0, amp=2.9, lean=-0.18)]
        self.motes = [(rng.uniform(0, W), rng.uniform(700, 1150), rng.uniform(0, 6.28), rng.uniform(10, 25)) for _ in range(40)]

    def frame(self, t, p, ctx=None):
        fr = self.sky.copy()
        self.stars.draw(fr, t, 0.6)
        add_light(fr, self.sun, self.sun_xy[0] - 150, self.sun_xy[1] - 150)
        comp_layer(fr, self.layers[0], self.cam, t, p)
        comp_layer(fr, self.layers[1], self.cam, t, p)
        for pm in self.palms_mid:
            pm.draw(fr, self.cam, t, p)
        comp_layer(fr, self.near_ground, self.cam, t, p)
        for pm in self.palms_near:
            pm.draw(fr, self.cam, t, p)
        for mx, my, ph, sp in self.motes:   # grains de poussière dorés dans la lumière rasante
            xx = (mx + t * sp) % W
            yy = my + 14 * math.sin(t * 0.6 + ph)
            al = 0.22 * (0.5 + 0.5 * math.sin(t * 1.3 + ph))
            xi, yi = int(xx), int(yy)
            if 1 <= xi < W - 2 and 1 <= yi < H - 2:
                fr[yi:yi + 2, xi:xi + 2] += (_f((255, 226, 170)) - fr[yi:yi + 2, xi:xi + 2]) * al
        return fr

# ------------------------------------------------------------------ registre
_BUILD = {"desert_nuit": lambda: _Desert(False), "desert_aube": lambda: _Desert(True),
          "medine_nuit": MedineNuit, "kaaba_loin": KaabaLoin, "lanterne": Lanterne,
          "traces_sable": TracesSable, "parchemin": Parchemin, "palmeraie": Palmeraie}
_CACHE = {}

def get(name):
    if name not in _CACHE:
        _CACHE[name] = _BUILD[name]()
    return _CACHE[name]

PARCH_BOX = Parchemin.BOX
PARCH_UNROLL_END = 0.15 + 1.6

if __name__ == "__main__":     # aperçu rapide : python3 decors.py [nom] [t] [p]
    import sys, time
    names = sys.argv[1:2] or list(DECORS)
    t = float(sys.argv[2]) if len(sys.argv) > 2 else 4.0
    p = float(sys.argv[3]) if len(sys.argv) > 3 else 0.8
    for nm in names:
        t0 = time.time(); d = get(nm); t1 = time.time()
        f = d.frame(t, p); t2 = time.time()
        Image.fromarray(np.clip(f, 0, 255).astype(np.uint8)).save(f"/tmp/decor_{nm}.jpg", quality=90)
        print(f"{nm}: construction {t1 - t0:.2f} s, image {1000 * (t2 - t1):.0f} ms")
