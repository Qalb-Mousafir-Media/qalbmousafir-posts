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

- Types de scènes : `hook`, `quote`, `step`, `recap`, `outro`, `story` (voir plus bas).
- Durée d'une scène = durée de la voix + 1,0 s (minimum 3,5 s) ; la voix démarre à 0,3 s.
- Audio : passe-haut 70 Hz, compression douce, normalisation à −15 LUFS, AAC 192k.
- Temps de rendu : environ 2 à 3 min pour 60 s de vidéo sur 2 cœurs.

## Scènes story et décors

Pour la série « Les Compagnons » : une scène `story` affiche un décor procédural animé (`tools/decors.py`,
tout dessiné en code, aucune image téléchargée) et une légende. **Aucun être humain ni animal** n'apparaît,
même suggéré (ni silhouette, ni ombre, ni main) : seulement des paysages et des objets.

```json
{"type": "story", "decor": "desert_nuit", "caption": "phrase ≤ 90 caractères", "arabic": "texte arabe ou \"\"",
 "narration": "...", "tts": "..."}
```

| décor | contenu | mouvement |
|---|---|---|
| `desert_nuit` | dunes sur 3 plans, croissant de lune, étoiles | parallaxe, scintillement, sable soulevé sur la crête |
| `desert_aube` | mêmes dunes, ciel d'aube ocre/rose, soleil bas | idem |
| `medine_nuit` | maisons de terre basses à toits plats (VIIe siècle : ni minaret, ni dôme, ni lampadaire), palmiers, mont au loin | fenêtres qui vacillent, palmes au vent, parallaxe |
| `kaaba_loin` | la Kaaba (cube noir, bande dorée) au fond d'une vallée de montagnes rocheuses, la nuit, rien d'autre de construit | reflet sur la bande dorée, zoom lent |
| `lanterne` | gros plan d'une lanterne à huile posée sur un rebord | flamme qui vacille, halo, poussières dans la lumière |
| `traces_sable` | traces de pas vers l'horizon (traces seulement) | les empreintes apparaissent une à une |
| `parchemin` | parchemin à rouleaux de bois | se déroule, puis l'arabe (droite→gauche) et la légende (ligne par ligne) s'y écrivent |
| `palmeraie` | palmiers sur 3 plans au coucher du soleil | palmes au vent, poussières dorées |

- Caméra : léger travelling latéral (parallaxe sur 2–3 plans) + zoom lent type Ken Burns ; le ciel reste fixe.
- Texte : arabe (Amiri doré) puis légende (Crimson crème, ombre), en fondu, dans un bandeau dégradé sombre
  (texte entre y = 1140 et 1480). Si `arabic` est vide, il n'est pas affiché. Taille réduite automatiquement si le bloc est trop haut.
  Pour `parchemin`, le texte s'écrit sur la feuille (encre brune, arabe en or foncé) au lieu du bandeau.
- Zone sûre TikTok respectée : rien d'important au-dessus de y = 250, sous y ≈ 1500, ni à droite de x ≈ 940.
- Scènes consécutives avec le même décor : le décor continue sans coupure (même caméra, traces déjà posées, parchemin déjà déroulé).
  Décor différent (ou passage au fond ciel + rosace) : fondu enchaîné de 0,9 s au début de la scène suivante.
- `hook`, `quote` et `outro` acceptent un champ `"decor"` optionnel : le décor remplace le fond ciel + rosace, assombri de 50 %
  pour la lisibilité. Sans ce champ, rien ne change (rendu identique au pixel près).
- Essai : `python3 tools/render.py tools/test_story.json --preview` (les 8 décors, textes de test neutres) ;
  aperçu d'un décor seul : `python3 tools/decors.py lanterne 4 0.8` -> `/tmp/decor_lanterne.jpg`.
- Temps de rendu : ≈ 2,5 s de calcul par seconde de vidéo (≈ 1,3–1,5 s réelles sur 2 cœurs libres) ;
  `palmeraie` est le plus lourd (≈ 4 s de calcul par seconde), `parchemin` et `lanterne` les plus légers.
- Nécessite OpenCV (`opencv-python-headless`, installé par `setup.sh`).

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
