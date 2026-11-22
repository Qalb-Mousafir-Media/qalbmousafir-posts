"""Validate an episode script: schema, text lengths, tts phonemes, Arabic widths, voice duration."""
import json, sys, re
from PIL import ImageFont
from kokoro_onnx import Kokoro
import soundfile as sf, numpy as np

AMIRI = "/root/fonts/Amiri-1.000/Amiri-Bold.ttf"
import os; AMIRI = os.path.expanduser("~/fonts/Amiri-1.000/Amiri-Bold.ttf")
def arw(t, size):
    f = ImageFont.truetype(AMIRI, size, layout_engine=ImageFont.Layout.RAQM)
    l, _, r, _ = f.getbbox(t, direction="rtl"); return r - l + int(size * 0.7)

k = Kokoro(*[__import__('os').path.join(__import__('os').environ.get('QM_MODELS', __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.abspath(__file__))), 'models')), f) for f in ('kokoro.onnx','voices.bin')])
path = sys.argv[1]; save = len(sys.argv) > 2
ep = json.load(open(path))
steps = [s for s in ep["scenes"] if s["type"] == "step"]
assert all(s["total"] == len(steps) for s in steps), "total mismatch"
assert [s["index"] for s in steps] == list(range(1, len(steps) + 1))
tot = 0.0; rows = []
for i, s in enumerate(ep["scenes"]):
    tag = f"{i+1:02d}_{s['type']}" + (f"{s['index']}" if s["type"] == "step" else "")
    for key in ("narration", "tts"): assert s.get(key), f"{tag} missing {key}"
    assert "ﷺ" not in s["tts"], f"{tag}: ﷺ in tts"
    if s["type"] == "recap": assert 3 <= len(s["items"]) <= 8
    if "text" in s and len(s["text"]) > 110: print(f"!! {tag} text {len(s['text'])} chars")
    ph = k.tokenizer.phonemize(s["tts"], "fr-fr")
    if "(en)" in ph: print(f"!! {tag} ENGLISH: {ph}")
    # arabic widths at the sizes used in make.py
    sizes = {"hook": 160, "quote": 108, "step": 220, "outro": 170}
    if s.get("arabic") and s["type"] in sizes:
        w = arw(s["arabic"], sizes[s["type"]])
        if w > 1000: print(f"   {tag} arabic width {w}px at {sizes[s['type']]}px (needs smaller size/wrap)")
    samples, sr = k.create(s["tts"], voice="ff_siwis", speed=0.97, lang="fr-fr")
    d = len(samples) / sr; tot += d; rows.append((tag, round(d, 2)))
    if save:
        os.makedirs(sys.argv[2], exist_ok=True); sf.write(f"{sys.argv[2]}/{tag}.wav", samples, sr)
for r in rows: print(f"   {r[0]:14} {r[1]:6.2f} s")
print(f"TOTAL {path.split('/')[-1]}: {tot:.2f} s")
