# Spécial 1 : « La boucle » (ce qu'ils voient, ils le deviennent)

Script : `episodes/special1_la_boucle.json` · Texte Azure : `tools/azure/textes/special1_la_boucle.txt`
Narration : 123 mots, soit environ 50 à 58 s avec les pauses (10 scènes).

## Exception à la charte
Karim a validé le 26/11/2026 une exception **pour cette vidéo seulement** : des personnages dessinés (un papa, son fils à différents âges, puis le grand-père). Le reste de la charte s'applique : couleurs, polices, sources, nachid sans instruments, et aucune publication sans son accord.

## Sources (à relire)
| Scène | Contenu | Source | Jugement |
|---|---|---|---|
| 4 (légende) | Le Prophète ﷺ priait en portant sa petite-fille Umama bint Zaynab | al-Bukhari 516 ; Muslim 543 | Sahih, muttafaq 'alayh. **Vérifié en ligne** (sunnah.com/bukhari:516 ; Bulugh al-Maram 2/91 : Bukhari 516, Muslim 543) |
| 9 (citation) | « كُلُّكُمْ رَاعٍ، وَكُلُّكُمْ مَسْئُولٌ عَنْ رَعِيَّتِهِ » | al-Bukhari 893 (aussi 2554) ; Muslim 1829, d'après Ibn 'Umar | Sahih, muttafaq 'alayh. **Vérifié en ligne** (alsunna.net/hadith/1478 ; hadeethenc 5819) |

Points pour le relecteur :
1. La citation ne reprend que le début du hadith. La suite détaille l'imam, l'homme, la femme et le serviteur. Le sens n'est pas modifié.
2. Scène 4 : la légende sert à montrer qu'un enfant sur le père pendant la prière ne pose pas de problème en soi. Elle ne donne aucun avis sur la validité de la prière.
3. Il n'y a pas de Coran récité, donc pas de conflit avec la règle 7:204.
4. Les numéros ont été vérifiés en ligne le 26/11/2026. Le texte arabe de la citation suit Muslim et alsunna.net (« مَسْئُولٌ ») ; certaines éditions écrivent « مَسْؤُولٌ » : les deux graphies sont correctes.
5. Traduction de « رَعِيَّتِهِ » : « son troupeau » (sens littéral, la métaphore du berger) ; la narration dit « chacun est responsable de son troupeau ».

## Images à générer (Canva IA), format 1080×1920
Style commun, à coller au début de chaque prompt :
> Warm flat 2D cartoon illustration, soft pastel colors, cozy living room at night with warm lamp light, deep navy and gold accents (#070C20, #E2BD70), modest Muslim family. Father: short dark beard, white thobe, white kufi. Prayer mat: dark green with a gold border. Vertical 9:16. Keep the characters in the upper two thirds; leave the bottom third simple for text. No text in the image.

| N° | Fichier | Scène |
|---|---|---|
| 1 | 01_jour1.png | Father standing in prayer on the mat, newborn sleeping in a small wicker basket beside the mat |
| 2 | 02_2mois.png | Father in sujood, baby lying on a blanket just in front of the mat, looking at him |
| 3 | 03_6mois.png | Father standing in prayer, baby crawling around his feet on the mat, playful |
| 4 | 04_10mois.png | Father in sujood, toddler climbing on his back, father calm and patient |
| 5 | 05_2ans.png | Father in ruku', 2-year-old boy beside him copying the pose clumsily, bottom up, smiling |
| 6 | 06_5ans.png | 5-year-old boy unrolling his own small green prayer mat next to his father's |
| 7 | 07_12ans.png | 12-year-old boy at the door holding a rolled prayer mat, calling his father who sits on the sofa |
| 8 | 08_25ans.png | The son, now a young bearded man in a white thobe, in sujood with his own baby on his back; the grandfather (grey beard) sitting behind on a chair, smiling |

Point technique : il faut garder **les mêmes visages et les mêmes vêtements** d'une image à l'autre. C'est le principal risque avec un générateur d'images. Faire la scène 1 d'abord, puis réutiliser la même description pour les autres. Si le rendu est trop irrégulier, en refaire quelques-unes.

## Moteur de rendu
`tools/render.py` ne connaît pas encore le type `illustration`. Il faut l'ajouter. L'image prend tout l'écran, avec un léger zoom lent (Ken Burns). L'étiquette (« JOUR 1 », « 10 MOIS »…) s'affiche en or, en haut, et reste toujours au même endroit (y ≈ 300). La légende utilise le bandeau des scènes `story`.

## Légende TikTok (à valider)
```
Il priait, tu jouais sur son dos… et un jour c'est toi qui l'appelles 🤍
Qui t'a appris à prier ? Dis-le en commentaire 👇
Envoie-la à ton père, ou à un papa qui en a besoin 🤲
#islam #priere #papa #famillemusulmane #salat #qalbmousafir
```
