# Moteur vidéo Qalb Mousafir

Rend une vidéo TikTok 1080×1920, 30 i/s, avec voix off française, à partir d'un script JSON (format : `docs/SCHEMA.md`).

## Installation

```
tools/setup.sh        # dépendances Python + modèle de voix Kokoro dans models/
```
Il faut aussi `ffmpeg` et Pillow compilé avec raqm (texte arabe).

## Utilisation

```
python3 tools/render.py episodes/ep2_woudou.json --preview   # une image par scène + planche contact (≈ 1 s)
python3 tools/render.py episodes/ep2_woudou.json             # rendu complet -> tools/out/<slug>/<slug>.mp4
python3 tools/render.py episodes/ep2_woudou.json --only 3 5  # refaire les scènes 3 et 5
```
Options : `--jobs N` (processus en parallèle, `--jobs 1` si la machine est chargée), `--force` (ignore le cache).

- Types de scènes : `hook`, `quote`, `step`, `recap`, `outro`.
- Durée d'une scène = durée de la voix + 1,0 s (minimum 3,5 s) ; la voix démarre à 0,3 s.
- Audio : passe-haut 70 Hz, compression douce, normalisation à −15 LUFS, AAC 192k.
- Temps de rendu : environ 2 à 3 min pour 60 s de vidéo sur 2 cœurs.

## Contrôles avant publication

```
python3 tools/check.py episodes/<script>.json   # JSON, longueur des textes, largeur de l'arabe, prononciation, durée de voix
python3 tools/ph.py "Woudou"                    # prononciation d'un mot ; « (en) » = lu à l'anglaise, changer la graphie
```

## Compression pour l'hébergement

```
ffmpeg -i tools/out/<slug>/<slug>.mp4 -c:v libx264 -preset slow -crf 24 -pix_fmt yuv420p -c:a copy -movflags +faststart videos/<slug>.mp4
```

## Prononciation des mots arabes

`tools/lexique_arabe.json` remplace, au moment de la synthèse, certains mots du champ `tts` par leurs phonèmes (API phonétique de Kokoro). Les petits mots juste avant (le, la, de, à, et, en) perdent leur accent, et « en » fait la liaison (« en Allah »).

Pour tester un nouveau mot : ajouter des variantes dans un fichier comme `tools/prononciation/cases.json` (graphie `tts`, mot arabe visé, phonèmes à essayer), puis
```
QM_ASR=models/sherpa-onnx-whisper-small python3 tools/prononciation/eval.py tools/prononciation/cases.json
```
Le script fait lire chaque variante par la voix, la fait transcrire par Whisper small en arabe (modèle sherpa-onnx, publié sur GitHub dans k2-fsa/sherpa-onnx, release « asr-models ») et classe les variantes par ressemblance au mot visé. C'est un indicateur, pas une garantie : la décision finale se fait à l'écoute.

## Nachid de fond

```
python3 tools/mix_nasheed.py tools/out/<slug>/<slug>.mp4 audio/nasheed-60.mp3 videos/<slug>.mp4 [--offset-db 3]
```
Voir `audio/README.md`.

## Voix Azure (Vivienne, retenue le 22/11/2026)

1. `python3 tools/azure/make_textes.py episodes/<script>.json` crée `tools/azure/textes/<slug>.txt` (mots arabes marqués `[ar:ARABE|français]`, liste dans `make_textes.py`).
2. Sur le PC de Karim : copier le .txt dans `Documents\QalbMousafir-voix\textes\`, puis
   `powershell -ExecutionPolicy Bypass -File .\generer-voix.ps1` (clé `AZURE_SPEECH_KEY`, région `canadacentral`).
3. Récupérer `audio\vivienne-ar\<slug>\NN.mp3`, les copier dans `audio/voix/vivienne-ar/<slug>/`, puis
   `python3 tools/render.py episodes/<script>.json --voix-dir audio/voix/vivienne-ar/<slug>`
4. Ajouter le nachid avec `tools/mix_nasheed.py`.
