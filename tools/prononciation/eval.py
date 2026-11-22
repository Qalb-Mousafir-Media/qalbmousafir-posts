"""Compare des variantes de prononciation de mots arabes avec la voix Kokoro ff_siwis,
en les faisant transcrire par Whisper small (langue arabe) et en mesurant la ressemblance au mot visé."""
import json, re, sys, unicodedata, difflib
import numpy as np, sherpa_onnx, librosa
from kokoro_onnx import Kokoro

K = Kokoro(*[__import__("os").path.join(__import__("os").environ.get("QM_MODELS", "models"), f) for f in ("kokoro.onnx", "voices.bin")])
M = __import__("os").environ.get("QM_ASR", "models/sherpa-onnx-whisper-small") + "/small-"
REC = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=M + "encoder.int8.onnx", decoder=M + "decoder.int8.onnx",
                                                 tokens=M + "tokens.txt", language="ar", task="transcribe", num_threads=2)

def norm(s):
    s = "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))
    s = re.sub("[إأآٱ]", "ا", s).replace("ة", "ه").replace("ى", "ي").replace("ـ", "")
    s = re.sub(r"[^ء-ي ]", "", s)
    s = " ".join(w[2:] if w.startswith("ال") and len(w) > 3 else w for w in s.split())
    return s.replace(" ", "")

def synth(ph, text=False, speed=0.97):
    a, sr = K.create(ph, voice="ff_siwis", speed=speed, lang="fr-fr", is_phonemes=not text)
    a = librosa.resample(a.astype(np.float32), orig_sr=sr, target_sr=16000)
    return np.concatenate([np.zeros(4000, np.float32), a, np.zeros(8000, np.float32)])

def asr(a):
    st = REC.create_stream(); st.accept_waveform(16000, a); REC.decode_stream(st)
    return st.result.text.strip()

def score(hyp, target):
    return difflib.SequenceMatcher(None, norm(hyp), norm(target)).ratio()

if __name__ == "__main__":
    cases = json.load(open(sys.argv[1]))
    out = {}
    for c in cases:
        res = []
        cur = K.tokenizer.phonemize(c["tts"], "fr-fr")
        for label, ph in [("actuel", cur)] + list(c["variants"].items()):
            hyps = [asr(synth(ph, speed=sp)) for sp in (0.9, 0.97, 1.05)]
            res.append((round(sum(score(h, c["ar"]) for h in hyps) / 3, 2), label, ph, " | ".join(hyps)))
        res.sort(key=lambda r: -r[0])
        out[c["tts"]] = res
        print(f"\n{c['tts']}  →  {c['ar']}")
        for r in res: print(f"   {r[0]:.2f}  {r[1]:8s} /{r[2]}/  ⇒ {r[3]}")
    json.dump(out, open(sys.argv[1].replace(".json", "_res.json"), "w"), ensure_ascii=False, indent=1)
