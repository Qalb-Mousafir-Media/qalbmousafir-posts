# Format d'un script d'épisode (JSON) — partagé entre scénariste et monteur

Fichier : episodes/epN_slug.json

```json
{
  "episode": 2,
  "slug": "ep2_woudou",
  "title": "Comment faire les ablutions",
  "scenes": [
    {"type": "hook", "pill": "ÉPISODE 2 · LES BASES", "arabic": "الوضوء",
     "title": "Comment faire les ablutions", "subtitle": "Étape par étape",
     "narration": "texte lu à l'écran-voix (orthographe normale)",
     "tts": "même texte mais respellé pour la synthèse vocale"},
    {"type": "quote", "intro": "Le Prophète ﷺ a dit :", "arabic": "texte arabe vocalisé",
     "translation": "« traduction »", "source": "Rapporté par Muslim (n° 223)",
     "narration": "...", "tts": "..."},
    {"type": "step", "index": 1, "total": 8, "label": "ÉTAPE",
     "arabic": "النية", "title": "An-Niyya", "subtitle": "L'intention",
     "text": "Une à deux phrases courtes (max ~110 caractères).",
     "narration": "...", "tts": "..."},
    {"type": "recap", "title": "En résumé",
     "items": [{"title": "An-Niyya", "subtitle": "L'intention", "arabic": "النية"}],
     "narration": "...", "tts": "..."},
    {"type": "outro", "next_label": "Prochain épisode", "next_title": "Les 5 prières du jour",
     "next_arabic": "الصلوات الخمس", "cta": "Abonne-toi pour ne pas le rater",
     "narration": "...", "tts": "..."}
  ]
}
```

Scène « story » (série « Les Compagnons ») :

```json
{"type": "story", "decor": "medine_nuit", "caption": "Une phrase de 90 caractères maximum.",
 "arabic": "texte arabe vocalisé ou \"\"", "narration": "...", "tts": "..."}
```
- "decor" (obligatoire) : `desert_nuit`, `desert_aube`, `medine_nuit`, `kaaba_loin`, `lanterne`, `traces_sable`,
  `parchemin`, `palmeraie` (détails dans tools/README.md, section « Scènes story et décors »).
- "caption" : ≤ 90 caractères (au-delà : avertissement et police réduite). "arabic" : vide ("") = non affiché.
- Aucun être humain ni animal à l'écran : les décors ne montrent que des paysages et des objets ; le récit passe par la voix et la légende.
- hook, quote et outro acceptent aussi un "decor" optionnel (même liste) qui remplace le fond ciel + rosace.
- Deux scènes consécutives avec le même décor s'enchaînent sans coupure ; sinon fondu enchaîné.

Règles :
- "label" d'un step : « ÉTAPE », « PILIER », « PRIÈRE »… ; "total" = nombre de steps.
- recap : 3 à 8 items.
- story : "decor" obligatoire, "caption" ≤ 90 caractères.
- "arabic" peut être vide ("") si aucun mot arabe n'a de sens.
- Durée cible totale : 50 à 75 s de voix (≈ 150 mots par minute en français).
- "tts" : réécrire les mots arabes pour que la voix française les prononce bien. Graphies testées qui marchent :
  Chahada, Salate, Zakate, Saoum, Hadj, Fadjr, Dhohr, Asr, Magrib, Ichâ, Mouhammad, al-Boukhari, Mouslim,
  nissab, Allah, Ramadan. Éviter « u » pour le son « ou » (écrire « ou »), éviter « aj/ajj » (écrire « adj »),
  ajouter un « e » final aux mots finissant par t/m prononcés (Salate, Zakate). Les nombres en lettres.
  Ne jamais mettre ﷺ dans "tts" : écrire « paix et salut sur lui ».
