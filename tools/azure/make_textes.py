"""Fabrique les fichiers texte pour generer-voix.ps1 (Azure) à partir des scripts JSON.
Les mots arabes deviennent [ar:ARABE|français] : en mode « ar » la voix les dit en arabe, en mode « fr » en français.
Usage : python3 tools/azure/make_textes.py episodes/ep3_5_prieres.json [...]  -> tools/azure/textes/<slug>.txt"""
import json, os, re, sys

# (texte de la narration, arabe vocalisé). Les plus longs d'abord. Si un article français précède, l'arabe est sans « al- ».
MOTS = [
    # Les Compagnons (comp1) : noms longs avant leurs préfixes ('Umar, 'Abdallah)
    ("'Umar ibn al-Khattab", "عُمَرُ بْنُ الخَطَّاب"),
    ("'Abdallah ibn Mas'ud", "عَبْدُ اللهِ بْنُ مَسْعُود"),
    ("al-'As ibn Wa'il", "العَاصُ بْنُ وَائِل"),
    ("Sa'id ibn Zayd", "سَعِيدُ بْنُ زَيْد"),
    ("at-Tirmidhi", "التِّرْمِذِي"),
    ("Abu Jahl", "أَبُو جَهْل"),
    ("al-Faruq", "الفَارُوق"),
    ("'Abdallah", "عَبْدُ الله"),
    ("Shaytan", "شَيْطَان"),
    ("'Umar", "عُمَر"),
    # Les bases, ép. 9 à 11
    ("'Abd al-Muttalib", "عَبْدُ المُطَّلِب"),
    ("Abou Talib", "أَبُو طَالِب"),
    ("al-Amin", "الأَمِين"),
    ("Hijra", "هِجْرَة"),
    ("Hira", "حِرَاء"),
    ("Mushaf", "مُصْحَف"),
    ("an-Nas", "النَّاس"),
    ("sahour", "سَحُور"),
    ("L'iftar", "الإِفْطَار"),
    ("l'iftar", "الإِفْطَار"),
    ("ash-hadu an la ilaha illa Allah, wa ash-hadu anna Muhammadan rasulu Allah", "أَشْهَدُ أَنْ لَا إِلٰهَ إِلَّا الله، وَأَشْهَدُ أَنَّ مُحَمَّدًا رَسُولُ الله"),
    ("wa ash-hadu anna Muhammadan", "وَأَشْهَدُ أَنَّ مُحَمَّدًا"),
    ("ash-hadu", "أَشْهَدُ"),
    ("la ilaha", "لَا إِلٰهَ"),
    ("illa Allah", "إِلَّا الله"),
    ("rasul Allah", "رَسُولُ الله"),
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
    ("al-Ikhlas", "الإِخْلَاص"),
    ("Shahada", "شَهَادَة"),
    ("al-Ihsan", "الإِحْسَان"),
    ("l'ihsan", "الإِحْسَان"),
    ("l'iman", "الإِيمَان"),
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
