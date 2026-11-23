# Notes du scénariste : épisodes 6, 7 et 8 (« Les bases »)

Date : 22/11/2026. Fichiers : `ep6_priere_partie2.json`, `ep7_chahada.json`, `ep8_ihsan.json`.
Voix : Azure, Vivienne. `tts` = `narration` partout (exigé par le schéma).

## Contrôles passés

- `python3 -m json.tool` : OK sur les 3 fichiers.
- `tools/check.py` (QM_MODELS=/home/claude/tts) : schéma OK, recap entre 3 et 8 items, aucun `text` au-dessus de 110 caractères, pas de ﷺ dans `tts`. Les avertissements « ENGLISH » de Kokoro sont ignorés (« assieds-toi », « Maghrib », « ash-hadu »), comme demandé. Les avertissements de largeur d'arabe sont absorbés par le rendu : `arabic_fit` réduit l'arabe des étapes, et le rendu coupe les citations en plusieurs lignes.
- `tools/render.py --preview` sur les 3 épisodes : toutes les scènes sont lisibles. Planches dans `tools/out/<slug>/preview/contact.jpg`.
- Note pour le monteur : dans `text_block`, une ponctuation collée à ﷺ (« ﷺ, » ou « ﷺ… ») s'affiche à gauche du signe, parce que le mot est traité comme de l'arabe. Les textes des ép. 6 et 7 évitent ce cas (vérifié sur les aperçus).
- `tools/azure/make_textes.py` : les 3 fichiers `tools/azure/textes/ep6_priere_partie2.txt`, `ep7_chahada.txt` et `ep8_ihsan.txt` sont produits et relus. Chaque mot arabe est balisé, aucune balise n'est cassée, aucun article n'est doublé (« la [ar:شَهَادَة|Chahada] », « [ar:الإِحْسَان|l'ihsan] », « du [ar:ظُهْر|Dhuhr] »).

## Mots et durées

| Ép. | Mots de narration | Estimation à 150 mots/min | Kokoro (check.py, pour info) | Max `text` |
|---|---|---|---|---|
| 6 Prière, partie 2 | 194 | ≈ 78 s | 66,2 s | 102 car. |
| 7 La Chahada | 187 | ≈ 75 s | 62,6 s | 98 car. |
| 8 Al-Ihsan | 190 | ≈ 76 s | 59,8 s | 102 car. |

L'épisode 6 dépasse un peu la fourchette de 150 à 190 mots, parce que j'ai ajouté la prière sur le Prophète au tashahhud final (doute 6.5). L'estimation reste sous 80 s.

## Citations : références et vérification

| Ép. | Citation (affichée) | Référence | Vérifié sur |
|---|---|---|---|
| 6 | كَانَ النَّبِيُّ ﷺ يَقْرَأُ فِي الرَّكْعَتَيْنِ الْأُولَيَيْنِ مِنْ صَلَاةِ الظُّهْرِ بِفَاتِحَةِ الْكِتَابِ وَسُورَتَيْنِ (Abu Qatada) | al-Bukhari n° 759 (muttafaq 'alayh selon hadeethenc) | https://sunnah.com/bukhari:759 (texte : « كَانَ النَّبِيُّ صلى الله عليه وسلم يَقْرَأُ فِي الرَّكْعَتَيْنِ الأُولَيَيْنِ مِنْ صَلاَةِ الظُّهْرِ » puis « بِفَاتِحَةِ الْكِتَابِ وَسُورَتَيْنِ » ; n° 759, in-book 10/153) · https://hadeethenc.com/ar/browse/hadith/10916 (même hadith ; « dans les deux dernières, al-Fatiha seule ») |
| 7 | مَنْ مَاتَ وَهُوَ يَعْلَمُ أَنَّهُ لَا إِلَهَ إِلَّا اللَّهُ دَخَلَ الْجَنَّةَ ('Uthman ibn 'Affan) | Muslim n° 26 | https://sunnah.com/muslim/1 (Muslim 26a, in-book 1/43, texte voyelle par voyelle) · https://dorar.net/hadith/sharh/26743 (Muslim 26, sahih) |
| 8 | أَنْ تَعْبُدَ اللهَ كَأَنَّكَ تَرَاهُ، فَإِنْ لَمْ تَكُنْ تَرَاهُ فَإِنَّهُ يَرَاكَ (hadith de Jibril, 'Umar) | Muslim n° 8 | https://sunnah.com/muslim/1 (Muslim 8a : « فَأَخْبِرْنِي عَنِ الإِحْسَانِ. قَالَ أَنْ تَعْبُدَ اللَّهَ كَأَنَّكَ تَرَاهُ فَإِنْ لَمْ تَكُنْ تَرَاهُ فَإِنَّهُ يَرَاكَ ») · déjà vérifié par le relecteur : https://www.islamweb.net/ar/library/content/1/80/ |
| 8 (étape 5) | « Allah a prescrit l'excellence en toute chose » = إِنَّ اللهَ كَتَبَ الْإِحْسَانَ عَلَى كُلِّ شَيْءٍ (Shaddad ibn Aws) | Muslim n° 1955 | https://hadeethenc.com/ar/browse/hadith/4319 (« صحيح مسلم - 1955 ») |
| 8 (étape 6) | Le Coran demande l'ihsan envers les parents : « وَبِالْوَالِدَيْنِ إِحْسَانًا » (non affiché en arabe, non récité) | Coran 17:23 | https://equran.me/ntafseer-23-17.html |

Sites : hadeethenc.com, dorar.net et sunnah.com ne passent pas en accès direct (proxy 403). Je les ai lus avec WebFetch à partir des liens donnés par la recherche web.
Vocalisation : à l'écran, la citation de l'ép. 6 remplace « صلى الله عليه وسلم » par le signe ﷺ (même sens, déjà la convention de la chaîne). Comme dans les épisodes précédents, j'écris « لَا / الْ » en vocalisation moderne complète.

## Mots ajoutés à MOTS (tools/azure/make_textes.py)

Ajout ciblé : des lignes insérées, sans réécrire le fichier. Les clés de la Chahada sont en tête de liste, pour que la formule complète passe avant « ash-hadu ».

| Narration | Arabe | Remarque |
|---|---|---|
| ash-hadu an la ilaha illa Allah, wa ash-hadu anna Muhammadan rasulu Allah | أَشْهَدُ أَنْ لَا إِلٰهَ إِلَّا الله، وَأَشْهَدُ أَنَّ مُحَمَّدًا رَسُولُ الله | formule complète (résumé ép. 7), forme de pause à la fin |
| wa ash-hadu anna Muhammadan | وَأَشْهَدُ أَنَّ مُحَمَّدًا | ép. 7, étape 4 |
| ash-hadu | أَشْهَدُ | |
| la ilaha | لَا إِلٰهَ | |
| illa Allah | إِلَّا الله | |
| rasul Allah | رَسُولُ الله | |
| al-Ikhlas | الإِخْلَاص | avec « al- » dans le texte |
| Chahada | شَهَادَة | toujours précédé de « la » |
| al-Ihsan | الإِحْسَان | |
| l'ihsan | الإِحْسَان | « l' » collé, comme « l'Asr » |
| l'iman | الإِيمَان | idem |

**Attention, ép. 2** : la nouvelle clé « illa Allah » se déclencherait au milieu de la formule de l'ép. 2, étape 8 (« Achhadou an lâ ilâha illa Allah, wahdahou… »), le jour où l'on produira son texte Azure. La phrase serait alors dite à moitié en arabe. Avant de passer l'ép. 2 dans make_textes.py, il faut ajouter un champ `azure` à cette scène, ou une clé MOTS pour la formule complète de l'ép. 2. Les ép. 3, 4 et 5 ne changent pas (vérifié).
« l'islam » reste dit en français : c'est un mot français, et une clé changerait aussi l'accroche de l'ép. 7. Dans l'ép. 8, on entend donc « l'islam » en français, puis « l'iman » et « l'ihsan » en arabe. Ajouter `("l'islam", "الإِسْلَام")` si Karim préfère.

## Doutes pour le relecteur religieux

### Épisode 6 : Comment faire la prière, partie 2
1. **3e et 4e rak'at** : « On y récite al-Fatiha ; pour le reste, demande à ton imam » (à l'écran : « le reste varie selon les écoles »). Les hanafites ne rendent pas al-Fatiha obligatoire dans ces rak'at (elle y est recommandée, avec d'autres choix possibles). Les trois autres écoles en font un pilier. La phrase décrit ce qu'on fait, sans donner de statut. Elle est appuyée par la suite du hadith d'Abu Qatada (hadeethenc 10916). À valider.
2. **La sourate après al-Fatiha** : son statut diverge (wajib chez les hanafites, Sunna ailleurs) et la vidéo n'en donne pas. Seul exemple donné : al-Ikhlas, qui atteint le minimum hanafite de 3 versets courts. Le cadre « quand tu pries seul » est rappelé à l'étape 1, parce que la récitation derrière l'imam diverge.
3. **Premier tashahhud** : son statut diverge (wajib chez les hanafites et les hanbalites, Sunna chez les malikites et les chafiites). La vidéo ne donne pas de statut, mais l'impératif « ne te relève pas : reste assis » peut s'entendre comme une obligation. Est-ce acceptable ?
4. **« Relève-toi avec Allahu akbar »** : le moment du takbir diverge. Chez les malikites, il se dit une fois debout après le premier tashahhud. « avec » reste vague exprès. À valider.
5. **Prière sur le Prophète ﷺ au tashahhud final** : je l'ai ajoutée sans statut (« le tashahhud final et la prière sur le Prophète »). Elle est pratiquée dans les quatre écoles : obligatoire chez les chafiites et les hanbalites, Sunna chez les hanafites et les malikites. L'omettre aurait laissé un débutant chafiite ou hanbalite sans un pilier. Si le relecteur préfère s'en tenir au plan initial, retirer environ 9 mots.
6. **Takbirs de transition et « Sami'a Allahu liman hamidah »** : pas traités, faute de place (point 6 de la relecture de l'ép. 5). À ajouter dans la légende ou dans un épisode futur.
7. **« (hors voyage) »** à l'écran, étape 5 : c'est la même précision que la correction 3 de l'ép. 3.
8. Le résumé dit « le tashahhud au milieu et à la fin ». Le Fajr n'a pas de tashahhud au milieu, mais l'étape 5 et l'item du résumé (« prières de 3 et 4 ») le précisent.

### Épisode 7 : La Chahada, mot à mot
1. **Accroche** : « Une seule phrase fait entrer dans l'islam ». C'est une simplification : il faut la dire avec conviction et sincérité. L'étape 1 rattrape ce point (« savoir, en être convaincu, et le déclarer »). À valider, ou remplacer par « La phrase qui fait entrer dans l'islam ».
2. **Muslim 26, « entrera au Paradis »** : selon Ahl as-Sunna, il y entre au final, même s'il est d'abord puni pour ses péchés. La vidéo ne le précise pas. On peut l'ajouter en légende.
3. **« digne d'adoration »** : ajouté dans les explications, comme demandé. La traduction du hadith reste littérale (« il n'y a de divinité qu'Allah »).
4. **« paix et salut sur lui »** : il n'est jamais inséré à l'intérieur de la formule arabe (« Muhammadan »), comme le recommande le point A de la relecture. Il est dit juste après, dans la traduction française (« et que Muhammad, paix et salut sur lui, est Son messager »), et à l'étape 4.
5. **Étape 5** : « Tu crois ce qu'il a transmis, et tu suis son exemple ». C'est un résumé du sens de la 2e partie (croire, obéir, s'abstenir de ce qu'il a interdit, adorer Allah selon sa Sunna). Simplification à valider.
6. **Arabe** : « إِلٰهَ » (alif suscrit), comme dans la consigne du directeur, pour les étapes et la formule. La citation garde « إِلَهَ », comme dans la source. Les deux sont corrects. À écouter : vérifier qu'Azure lit bien « ilāha » avec l'alif suscrit.
7. **Graphie** : « Chahada » ici (consigne), mais l'ép. 1 affiche « Shahada ». À harmoniser ?
8. **Résumé limité à 4 items** : le rendu des lignes du résumé (`recap_row`, police Crimson Text) ne sait pas dessiner ﷺ. Je n'ai donc pas mis d'item « Muhammad ﷺ » en français. Le ﷺ figure dans l'arabe de l'item 4 (« مُحَمَّدٌ رَسُولُ اللهِ ﷺ », police Amiri). Note pour le monteur : il faudrait que `recap_row` sache basculer sur une police arabe.
9. **Outro, « le plus haut degré de la foi »** : c'est la formule demandée. Au sens strict, l'ihsan est le plus haut des trois degrés de la religion (dîn), l'iman étant le 2e. L'ép. 8 parle des « trois niveaux de la religion ». On peut remplacer par « le plus haut degré de la religion ».

### Épisode 8 : Al-Ihsan
1. **Islam = « les actes », iman = « la foi du cœur »** : c'est la répartition des réponses dans le hadith de Jibril. Quand on le mentionne seul, l'iman inclut aussi les actes chez Ahl as-Sunna. Simplification à valider.
2. **Niveau 3** : « adorer Allah comme si tu Le voyais, en sachant qu'Il te voit ». Je fusionne les deux degrés expliqués par les commentateurs (contemplation, puis conscience d'être vu).
3. **Muslim 1955** : le hadith continue sur l'abattage (« فَإِذَا قَتَلْتُمْ فَأَحْسِنُوا الْقِتْلَةَ… »). Seule la première phrase, générale, est citée, comme dans les 40 hadiths d'an-Nawawi (n° 17). Je traduis الْإِحْسَانَ par « l'excellence » et عَلَى كُلِّ شَيْءٍ par « en toute chose ».
4. **Coran 17:23** : seulement mentionné (« Le Coran demande l'ihsan envers les parents »), sans récitation par la voix de synthèse, conformément à la règle sur le Coran.
5. **Citation** : la voix dit « Jibril a demandé au Prophète… », pour gagner du temps. La précision « venu sous l'apparence d'un homme » (correction 1 de l'ép. 4) reste à l'écran, dans l'intro.
6. **Exemples** (prière sans se presser, travail bien fait même seul, douceur avec les parents, tenir parole, sourire) : ils ne sont ni polémiques ni spécifiques à une école.
7. **Montage** : les étapes ont deux libellés, « NIVEAU 1-3 / 6 » puis « AU QUOTIDIEN 4-6 / 6 ». Le compteur est commun (`total` = 6). À valider visuellement.
8. **Outro** : « bientôt, une nouvelle série », sans sujet. `next_arabic` est vide (accepté par le rendu).
