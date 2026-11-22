"""Ajoute un nachid de fond sous la voix off d'une vidéo, avec baisse automatique quand la voix parle.
Usage : python3 tools/mix_nasheed.py video.mp4 audio/nasheed-60.mp3 sortie.mp4 [--crf 24]
Réglage validé par Karim le 22/11/2026 (test ép. 3) : nachid ≈ 18 dB sous la voix, remonte dans les silences."""
import argparse, json, re, subprocess

def lufs(path):
    out = subprocess.run(["ffmpeg", "-nostats", "-i", path, "-af", "ebur128", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", out)[-1])

def duration(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]))

ap = argparse.ArgumentParser()
ap.add_argument("video"); ap.add_argument("nasheed"); ap.add_argument("out")
ap.add_argument("--crf", default="24"); ap.add_argument("--offset-db", type=float, default=0.0, help="+3 = nachid plus fort")
a = ap.parse_args()
d = duration(a.video)
gain = -8.0 + (-14.4 - lufs(a.nasheed)) + a.offset_db   # -8 dB pour un nachid à -14,4 LUFS (référence nasheed-60)
fc = (f"[0:a]aformat=sample_rates=44100:channel_layouts=stereo,asplit=2[v][key];"
      f"[1:a]aresample=44100,aformat=channel_layouts=stereo,atrim=0:{d},asetpts=N/SR/TB,volume={gain:.1f}dB,"
      f"afade=t=in:d=1.5,afade=t=out:st={d - 2.5:.2f}:d=2.5[m];"
      f"[m][key]sidechaincompress=threshold=0.06:ratio=2:attack=30:release=500[md];"
      f"[v][md]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-15:TP=-1.5:LRA=9,aresample=44100[a]")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", a.video, "-i", a.nasheed, "-filter_complex", fc,
                "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "slow", "-crf", a.crf, "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", a.out], check=True)
print(f"{a.out} : nachid à {gain:.1f} dB, {d:.1f} s, {lufs(a.out):.1f} LUFS")
