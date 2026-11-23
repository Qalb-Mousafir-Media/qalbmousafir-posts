"""Fabrique les fichiers texte pour generer-voix.ps1 (Azure) à partir des scripts JSON.
Les mots arabes deviennent [ar:ARABE|français] : en mode « ar » la voix les dit en arabe, en mode « fr » en français.
Usage : python3 tools/azure/make_textes.py episodes/ep3_5_prieres.json [...]  -> tools/azure/textes/<slug>.txt"""
import json, os, re, sys

# (texte de la narration, arabe vocalisé). Les plus longs d'abord. Si un article français précède, l'arabe est sans « al- ».
MOTS = [
    ("As-salamu 'alaykum", "السَّلَامُ عَلَيْكُمْ"),
    ("Takbirat al-Ihram", "تَكْبِيرَةُ الإِحْرَام"),
    ("Allahu akbar", "اللهُ أَكْبَر"),
    ("al-Bukhari", "البُخَارِي"),
    ("al-Fatiha", "الفَاتِحَة"),
    ("al-qadar", "القَدَر"),
    ("l'Asr", "العَصْر"),
    ("l'Isha", "العِشَاء"),
    ("Fajr", "فَجْر"),
    ("Dhuhr", "ظُهْر"),
    ("Maghrib", "مَغْرِب"),
    ("rak'at", "رَكَعَات"),
    ("rak'a", "رَكْعَة"),
    ("Muhammad", "مُحَمَّد"),
    ("Jibril", "جِبْرِيل"),
    ("Muslim", "مُسْلِم"),
    ("Nouh", "نُوح"),
    ("Ibrahim", "إِبْرَاهِيم"),
    ("Moussa", "مُوسَى"),
    ("'Issa", "عِيسَى"),
    ("woudou'", "وُضُوء"),
    ("qibla", "قِبْلَة"),
    ("Kaaba", "كَعْبَة"),
    ("ruku'", "رُكُوع"),
    ("sujud", "سُجُود"),
    ("tashahhud", "تَشَهُّد"),
    ("salam", "سَلَام"),
]
PAT = re.compile(r"(?<![\w'])(" + "|".join(re.escape(m) for m, _ in MOTS) + r")(?![\w])")
AR = dict(MOTS)

def marquer(texte):
    return PAT.sub(lambda m: f"[ar:{AR[m.group(1)]}|{m.group(1)}]", texte)

here = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(here, "textes"), exist_ok=True)
for path in sys.argv[1:]:
    d = json.load(open(path, encoding="utf-8"))
    lignes = [f"# Voix off - {d['slug']} - {d.get('title', '')}",
              "# numero|texte ; [ar:ARABE|francais] = mot dit en arabe (mode ar) ou en francais (mode fr)"]
    for i, s in enumerate(d["scenes"], 1):
        t = (s.get("azure") or s.get("narration") or "").replace("\n", " ").strip()
        if t:
            lignes.append(f"{i:02d}|{marquer(t)}")
    out = os.path.join(here, "textes", d["slug"] + ".txt")
    open(out, "w", encoding="utf-8").write("\n".join(lignes) + "\n")
    print(out, len(lignes) - 2, "scènes")
