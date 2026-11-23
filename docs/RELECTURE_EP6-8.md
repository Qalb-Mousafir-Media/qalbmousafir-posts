# Relecture religieuse : épisodes 6, 7 et 8 (Qalb Mousafir, « Les bases »)

Relecteur indépendant. Date : 22/11/2026.
Copies d'origine conservées : `episodes/ep6_priere_partie2.orig.json`, `episodes/ep7_chahada.orig.json`, `episodes/ep8_ihsan.orig.json`.
Voix : Azure (Vivienne). Le champ lu est `narration`, et `tts` = `narration` dans toutes les scènes (vérifié par script).


## Synthèse

| Ép. | Verdict | Corrections | Mots de narration avant → après | Max `text` | Points pour Karim |
|---|---|---|---|---|---|
| 6 Prière, partie 2 | **Validé avec corrections** | 7 | 194 → **199** | 103 car. | 4 |
| 7 La Shahada | **Validé avec corrections** | 5 | 187 → **200** | 98 car. | 3 |
| 8 Al-Ihsan | **Validé avec corrections** | 2 | 190 → **190** | 102 car. | 3 |

Mots comptés comme le scénariste (mots et apostrophes, sans la ponctuation : on retrouve ses 194 / 187 / 190 sur les originaux). L'ép. 7 est pile à la limite haute (200).

Contrôles passés sur les 3 fichiers :
- `python3 -m json.tool` OK ; fichiers réécrits en `json.dump(indent=1, ensure_ascii=False)`, comme pour les ép. 2 à 5 ;
- `tts` = `narration` partout, aucun ﷺ dans `narration` / `tts` ;
- tous les `text` font 110 caractères ou moins ;
- `tools/check.py` : aucune erreur de schéma. Durées Kokoro (pour info seulement, la voix réelle est Azure) : ép. 6 **65,7 s**, ép. 7 **67,5 s**, ép. 8 **59,8 s**. Les avertissements « ENGLISH » et de largeur d'arabe sont ceux déjà connus (voir NOTES_EP6-8.md) ;
- ﷺ à l'écran après chaque « Prophète » / « Muhammad » des champs affichés, « paix et salut sur lui » à l'oral après chaque mention (vérifié par script ; seule exception voulue : « Muhammadan » à l'intérieur de la formule arabe de la Shahada, voir ép. 7, doute 4) ;
- aucune ponctuation collée à ﷺ dans les champs affichés (problème de `text_block` signalé par le scénariste) ;
- graphies à l'écran et dans la narration : « Shahada », « Muhammad ﷺ », « Fajr, Dhuhr, Asr, Maghrib, Isha ». Il ne reste aucun « Chahada » dans les champs affichés ni dans la narration ;
- aucun contenu polémique.

### Accès aux sites de référence
En accès direct (curl), sunnah.com, dorar.net, hadeethenc.com et islamweb.net renvoient **403** (proxy). Je les ai donc lus avec WebFetch : sunnah.com, dorar.net et hadeethenc.com ont répondu ; dorar.net/hadith/sharh/8632 a échoué côté site. WebFetch ne restitue que de courts extraits : j'ai donc vérifié chaque citation segment par segment, en demandant les mots exacts avec leurs voyelles.

Note sur la vocalisation (même convention que la relecture des ép. 2 à 5) : les sites écrivent « لاَ / إِلاَّ / صَلاَةِ / الأُولَيَيْنِ / الإِحْسَانَ / شَىْءٍ » ; les scripts utilisent la vocalisation moderne complète « لَا / إِلَّا / صَلَاةِ / الْأُولَيَيْنِ / الْإِحْسَانَ / شَيْءٍ ». Le nom « اللهَ » écrit sans shadda ni fatha sur le lam est une convention d'impression (hadeethenc écrit ainsi Muslim 1955). Ce sont les mêmes lettres et les mêmes voyelles prononcées : aucun écart réel.


---

## Épisode 6 : Comment faire la prière, partie 2 (`ep6_priere_partie2.json`) : VALIDÉ AVEC CORRECTIONS

Consigne du directeur appliquée : la vidéo reste sur la structure commune (sourate dans les 2 premières rak'at, position assise après la 2e rak'a dans les prières de 3 et 4, rak'at restantes, position assise finale, salam, nombre de rak'at). Pour les éléments dont le statut ou le moment diverge, j'ai retiré tout impératif et toute tournure d'obligation : la vidéo **décrit** ce qui se fait, à l'indicatif (« tu t'assois », « tu dis »), sans statut ni moment précis. Le résumé renvoie à l'imam pour les détails.

### Citation vérifiée
| Citation | Résultat | Source vérifiée |
|---|---|---|
| « كَانَ النَّبِيُّ ﷺ يَقْرَأُ فِي الرَّكْعَتَيْنِ الْأُولَيَيْنِ مِنْ صَلَاةِ الظُّهْرِ بِفَاتِحَةِ الْكِتَابِ وَسُورَتَيْنِ » (Abu Qatada) | **Identique mot pour mot et voyelle par voyelle** aux conventions près. Texte du site : « عَنْ أَبِيهِ، قَالَ كَانَ النَّبِيُّ صلى الله عليه وسلم يَقْرَأُ » puis « فِي الرَّكْعَتَيْنِ الأُولَيَيْنِ مِنْ صَلاَةِ الظُّهْرِ بِفَاتِحَةِ الْكِتَابِ وَسُورَتَيْنِ » (le mot suivant est « يُطَوِّلُ »). ﷺ remplace « صلى الله عليه وسلم », convention de la chaîne. La citation commence au matn : retirer l'isnad est correct. **N° 759 confirmé** (in-book 10/153). Traduction fidèle. | https://sunnah.com/bukhari:759 · même hadith, « صحيح – متفق عليه » : https://hadeethenc.com/ar/browse/hadith/10916 |
| Appui de l'étape 3 (al-Fatiha seule dans les deux dernières rak'at du Dhuhr) | Confirmé : **al-Bukhari 776** (in-book 10/171), même narrateur. Il n'est pas affiché. L'explication de hadeethenc 10916 donne la même chose. Le texte arabe n'est pas disponible sur la page de sunnah.com (seulement en anglais). | https://sunnah.com/bukhari:776 · https://hadeethenc.com/ar/browse/hadith/10916 |

Mots arabes isolés (صِفَةُ الصَّلَاةِ, السُّورَةُ, التَّشَهُّدُ الْأَوَّلُ, الْقِيَامُ, التَّشَهُّدُ الْأَخِيرُ, عَدَدُ الرَّكَعَاتِ, التَّشَهُّدُ, التَّسْلِيمُ, الرَّكَعَاتُ, الشَّهَادَةُ) : vocalisation correcte.

### Corrections appliquées
| # | Scène / champ | Avant | Après | Pourquoi |
|---|---|---|---|---|
| 1 | Étape 1 (sourate), `text` | « Quand tu pries seul, dans les 2 premières rak'at : après al-Fatiha, récite une sourate ou des versets. » | « Quand tu pries seul, dans chacune des 2 premières rak'at : après al-Fatiha, une sourate ou des versets. » (103 car.) | Doute 2. (a) « وَسُورَتَيْنِ » veut dire une sourate dans chaque rak'a. « dans les 2 premières… une sourate » pouvait se comprendre comme une seule sourate pour les deux. (b) Le statut diverge (wajib chez les hanafites, Sunna ailleurs) : j'ai retiré l'impératif. |
| 1b | Étape 1, `narration` | « …dans les deux premières rak'at, après al-Fatiha, récite une sourate… » | « …dans chacune des deux premières rak'at, après al-Fatiha, tu récites une sourate… » | Même raison. « Quand tu pries seul » et l'exemple al-Ikhlas sont conservés. |
| 2 | Étape 2 (1er tashahhud), `text` | « …après les 2 sujud de la 2e rak'a, ne te relève pas. Reste assis : tashahhud. » | « …après les 2 sujud de la 2e rak'a, tu t'assois pour le tashahhud. » | Doute 3 et consigne du directeur. Le statut diverge : wajib chez les hanafites et les hanbalites, Sunna chez les malikites et les chafiites. « ne te relève pas : reste assis » se comprenait comme une obligation. La position assise est pratiquée dans les quatre écoles : la décrire suffit. |
| 2b | Étape 2, `narration` | « Deux : une prière de trois ou quatre rak'at ? Après la deuxième rak'a, ne te relève pas : reste assis, et récite le tashahhud. » | « Deux : dans une prière de trois ou quatre rak'at, après la deuxième rak'a, tu t'assois pour le tashahhud. » | Même raison. |
| 3 | Étape 3 (se relever), `text` | « Relève-toi avec « Allahu akbar ». On y récite al-Fatiha ; le reste varie selon les écoles. » | « Tu te relèves et tu dis « Allahu akbar ». Quand tu pries seul, tu récites al-Fatiha dans ces rak'at. » (101 car.) | Doutes 1 et 4. **Takbir** : chez les malikites, il se dit une fois debout ; les autres écoles le disent en se relevant. « avec » laissait entendre « en même temps » ; « tu te relèves et tu dis » ne fixe pas le moment. **Al-Fatiha dans les 3e et 4e rak'at** : pilier chez les malikites, chafiites et hanbalites, Sunna chez les hanafites. La phrase la décrit, sans statut, comme le fait Bukhari 776. J'ai ajouté « quand tu pries seul », comme à l'ép. 5 : derrière l'imam, la récitation diverge. « le reste varie selon les écoles » était vague (le reste de quoi ?) : retiré, car le résumé renvoie déjà à l'imam. |
| 3b | Étape 3, `narration` | « Trois : relève-toi avec « Allahu akbar », pour la ou les rak'at qui restent. On y récite al-Fatiha ; pour le reste, demande à ton imam. » | « Trois : tu te relèves pour la ou les rak'at qui restent, et tu dis « Allahu akbar ». Quand tu pries seul, tu y récites al-Fatiha. » | Même raison. |
| 4 | Étape 4 (tashahhud final), `narration` | « …assieds-toi pour le tashahhud final et la prière sur le Prophète, paix et salut sur lui. Puis termine par le salam. » | « …tu t'assois pour le tashahhud final et la prière sur le Prophète, paix et salut sur lui. Puis tu termines par le salam. » | Doute 5. **Prière sur le Prophète ﷺ : conservée**, sans statut et sans impératif. Elle est pratiquée dans les quatre écoles à cet endroit (pilier chez les chafiites et les hanbalites, Sunna chez les hanafites et les malikites). La retirer aurait privé un débutant chafiite ou hanbalite d'un pilier. Le `text` (« Après la dernière rak'a, assis : le tashahhud final et la prière sur le Prophète ﷺ puis le salam. ») n'avait pas d'impératif : je n'y ai pas touché. |
| 5 | Étape 5 (nombre), `narration` | « …Le Dhuhr, l'Asr et l'Isha, quatre. » | « …Le Dhuhr, l'Asr et l'Isha, quatre, hors voyage. » | Doute 7 : même précision qu'à l'écran et qu'à l'ép. 3. Placée après les prières de 4 rak'at, les seules qu'on raccourcit, elle est plus juste qu'après la liste entière. |
| 6 | Résumé, `narration` | « …le tashahhud au milieu et à la fin… » | « …le tashahhud après la deuxième rak'a et à la fin… » | Doute 8. « au milieu » est faux pour le Fajr ; « après la deuxième rak'a » est juste pour toutes les prières (au Fajr, c'est la fin). |
| 7 | Outro, `next_title` / `narration` | « La Chahada, mot à mot » / « la Chahada » | « La Shahada, mot à mot » / « la Shahada » | Cohérence avec l'ép. 1 publié. |

### Conclusions sur les doutes de NOTES_EP6-8.md (ép. 6)
1. **Al-Fatiha dans les 3e et 4e rak'at** : formulée sans statut, à l'indicatif, dans le cadre de la prière faite seul (correction 3).
2. **Sourate après al-Fatiha** : sans statut, sans impératif, « dans chacune » ajouté (correction 1). Al-Ikhlas convient comme exemple : elle atteint le minimum hanafite. OK.
3. **Premier tashahhud** : non, l'impératif « ne te relève pas : reste assis » n'était pas acceptable. Corrigé en description (correction 2).
4. **Takbir en se relevant** : moment non fixé (correction 3). Voir le point humain H.
5. **Prière sur le Prophète ﷺ** : conservée, sans statut (correction 4).
6. **Takbirs de transition, « Sami'a Allahu liman hamidah »** : toujours absents des ép. 5 et 6. Voir le point humain H.
7. **« (hors voyage) »** : OK, ajouté aussi à l'oral (correction 5).
8. **« au milieu »** : corrigé (correction 6).

### Points qui restent à la décision humaine (ép. 6)
- **H.** Le seul takbir de transition mentionné dans les ép. 5 et 6 est celui du relèvement après le 1er tashahhud. Un débutant peut croire qu'il n'y en a pas d'autre. Je recommande une ligne de légende : « À chaque changement de position, on dit « Allahu akbar », sauf en se redressant de l'inclinaison : « Sami'a Allahu liman hamidah ». Le moment exact et le statut varient selon les écoles. » On peut aussi y consacrer un épisode futur.
- **I.** Le texte du tashahhud et celui de la prière sur le Prophète ﷺ ne sont pas enseignés. Les versions diffèrent selon les écoles (Ibn Mas'oud, Ibn 'Abbas, 'Umar) et toutes sont valables. Le résumé renvoie à l'imam. Un épisode dédié pourrait les présenter « selon les écoles ».
- **J.** La traduction de la citation (« al-Fatiha et deux sourates ») est littérale. L'étape 1 précise désormais « dans chacune ». Si Karim le veut, on peut ajouter « (une dans chacune) » à la traduction, entre parenthèses pour montrer que c'est une explication. Je ne l'ai pas fait, pour ne rien ajouter au texte prophétique.
- **K.** Mise en page : l'item 4 du résumé a pour titre « Tashahhud final », mais son arabe est « التَّسْلِيمُ » (le salam, repris dans le sous-titre). Pour mieux coller au titre, on peut mettre « التَّشَهُّدُ الْأَخِيرُ », à condition de vérifier la largeur dans `recap_row`. Je n'y ai pas touché : ce n'est pas une erreur religieuse.


---

## Épisode 7 : La Shahada, mot à mot (`ep7_chahada.json`) : VALIDÉ AVEC CORRECTIONS

### Citation vérifiée
| Citation | Résultat | Source vérifiée |
|---|---|---|
| « مَنْ مَاتَ وَهُوَ يَعْلَمُ أَنَّهُ لَا إِلَهَ إِلَّا اللَّهُ دَخَلَ الْجَنَّةَ » ('Uthman ibn 'Affan) | **Identique mot pour mot et voyelle par voyelle** (site : « …لاَ إِلَهَ إِلاَّ اللَّهُ… »). **Muslim n° 26** confirmé (26a, in-book 1/43). Sur dorar.net : Muslim 26, « صحيح », 'Uthman ibn 'Affan. Traduction « Celui qui meurt en sachant qu'il n'y a de divinité qu'Allah entrera au Paradis » fidèle et littérale. | https://sunnah.com/muslim:26a · https://dorar.net/hadith/sharh/26743 |

Formule de la Shahada (résumé ; MOTS de `make_textes.py`) : « أَشْهَدُ أَنْ لَا إِلٰهَ إِلَّا الله، وَأَشْهَدُ أَنَّ مُحَمَّدًا رَسُولُ الله ». Grammaire correcte (« مُحَمَّدًا » à l'accusatif après « أَنَّ », « رَسُولُ » au nominatif) et forme de pause à la fin. Mots isolés (الشَّهَادَةُ, أَشْهَدُ, لَا إِلٰهَ, إِلَّا اللهُ, مُحَمَّدًا, رَسُولُ اللهِ, مُحَمَّدٌ رَسُولُ اللهِ ﷺ, الْإِحْسَانُ) : vocalisation correcte. « مُحَمَّدًا » isolé à l'étape 4 garde le cas de la formule : correct.

### Corrections appliquées
| # | Scène / champ | Avant | Après | Pourquoi |
|---|---|---|---|---|
| 1 | `title` du fichier + accroche `title` | « La Chahada, mot à mot » | « La Shahada, mot à mot » | Doute 7 : cohérence avec l'ép. 1 publié (« Shahada »). Le slug et le nom de fichier `ep7_chahada` ne changent pas (technique, voir le point humain N). |
| 2 | Accroche, `narration` | « Une seule phrase fait entrer dans l'islam. » | « Une seule phrase, dite avec conviction, fait entrer dans l'islam. » | Doute 1 et consigne du directeur. La phrase ne fait entrer dans l'islam que dite avec conviction, pas seulement prononcée. Trois mots suffisent ; l'étape 1 développe (« savoir, en être convaincu dans ton cœur, et le déclarer » à l'écran). |
| 3 | Citation, `narration` | « …Rapporté par Muslim. En sachant : alors apprenons son sens. » | « …Rapporté par Muslim. Il y entrera au final, même si ses péchés peuvent l'en retarder. « En sachant » : apprenons son sens. » | Doute 2 et consigne du directeur. Croyance d'Ahl as-Sunna : le monothéiste qui meurt sur le tawhid entre au Paradis au final ; il peut d'abord être puni pour ses péchés, ou Allah lui pardonne. « peuvent » garde les deux possibilités. La traduction du hadith reste littérale : la nuance est dite après « Rapporté par Muslim », comme une explication et non comme une partie du texte. Les guillemets autour de « En sachant » montrent qu'on reprend le mot du hadith. |
| 4 | Étape 2, `narration` | « On commence par dire non : … » | « D'abord, on dit non : … » | Pas une correction religieuse : un mot de moins (limite de 200 mots), et la narration reprend exactement le texte à l'écran. |
| 5 | Outro, `next_title` / `narration` | « Al-Ihsan, le plus haut degré de la foi » | « Al-Ihsan, le plus haut degré de la religion » | Doute 9 et consigne du directeur. Dans le hadith de Jibril, islam, iman et ihsan sont trois degrés de la religion (« يُعَلِّمُكُمْ دِينَكُمْ »). Dire « de la foi » (iman) confond le 2e et le 3e degré. |

Note : j'ai d'abord ajouté « dans ton cœur » à la narration de l'étape 1, puis je l'ai retiré pour rester à 200 mots. L'accroche dit maintenant « dite avec conviction », et l'écran de l'étape 1 garde « convaincu dans ton cœur ».

### Conclusions sur les doutes (ép. 7)
1. **Accroche** : nuancée (correction 2).
2. **« entrera au Paradis »** : nuancé à l'oral, sans toucher à la traduction (correction 3).
3. **« digne d'adoration »** dans les explications et traduction du hadith littérale : OK.
4. **« Muhammadan » sans « paix et salut sur lui » dans la formule** : OK, conforme au point A des ép. 2 à 5. Il est dit juste après, en français, à l'étape 4 et au résumé.
5. **« Tu crois ce qu'il a transmis, et tu suis son exemple »** : simplification juste et consensuelle (croire ce qu'il a transmis, suivre sa Sunna). OK.
6. **« إِلٰهَ » (alif suscrit) / « إِلَهَ » dans la citation** : les deux graphies sont correctes. À écouter : il faut vérifier qu'Azure lit bien « ilāha », avec un a long (point humain M).
7. **Shahada** : harmonisé (correction 1 ci-dessus, correction 7 de l'ép. 6, correction 2 de l'ép. 8, clé MOTS).
8. **Résumé limité à 4 items, ﷺ dans l'arabe de l'item 4** : acceptable, ﷺ est bien présent à l'écran. La limite de police de `recap_row` est une question de montage.
9. **« le plus haut degré de la religion »** : appliqué (correction 5, et ép. 8).

### Points qui restent à la décision humaine (ép. 7)
- **L.** La narration fait **200 mots**, la limite haute. Si la voix Azure dépasse la durée voulue, on peut retirer en priorité « D'abord, on dit non : » (étape 2), sans perte religieuse.
- **M.** À l'écoute en mode « ar », vérifier « لَا إِلٰهَ » et la formule complète : « ilāha » avec un a long, et « Allāh » en forme de pause.
- **N.** Le nom de fichier et le slug `ep7_chahada` gardent « chahada » : seul le titre affiché est corrigé. Les renommer changerait les chemins (`tools/out/`, `textes/`). C'est à décider par le monteur.


---

## Épisode 8 : Al-Ihsan (`ep8_ihsan.json`) : VALIDÉ AVEC CORRECTIONS

### Citations vérifiées
| Citation | Résultat | Source vérifiée |
|---|---|---|
| « أَنْ تَعْبُدَ اللهَ كَأَنَّكَ تَرَاهُ، فَإِنْ لَمْ تَكُنْ تَرَاهُ فَإِنَّهُ يَرَاكَ » (hadith de Jibril, 'Umar) | **Identique** (site : « فَأَخْبِرْنِي عَنِ الإِحْسَانِ قَالَ أَنْ تَعْبُدَ اللَّهَ كَأَنَّكَ تَرَاهُ فَإِنْ لَمْ تَكُنْ تَرَاهُ فَإِنَّهُ يَرَاكَ ») ; « اللهَ » = « اللَّهَ » (convention), la virgule est ajoutée pour la lisibilité. **Muslim n° 8** confirmé (8a, in-book 1/1). La fin « فَإِنَّهُ جِبْرِيلُ » confirme l'intro « Jibril, venu sous l'apparence d'un homme ». « Parle-moi de l'ihsan » rend fidèlement « فَأَخْبِرْنِي عَنِ الإِحْسَانِ ». Traduction fidèle. | https://sunnah.com/muslim:8a · déjà vérifié : https://www.islamweb.net/ar/library/content/1/80/ |
| « Allah a prescrit l'excellence en toute chose » = « إِنَّ اللَّهَ كَتَبَ الإِحْسَانَ عَلَى كُلِّ شَىْءٍ » (Shaddad ibn Aws) | Confirmé, **Muslim n° 1955** (1955a, in-book 34/84) ; hadeethenc : « إِنَّ اللهَ كَتَبَ الْإِحْسَانَ عَلَى كُلِّ شَيْءٍ », Muslim 1955, sahih. Seule la phrase générale est citée, comme dans les 40 hadiths d'an-Nawawi (n° 17) : c'est acceptable, et la suite sur l'abattage n'en change pas le sens. Traduction fidèle. L'arabe n'est pas affiché. | https://sunnah.com/muslim:1955a · https://hadeethenc.com/ar/browse/hadith/4319 |
| Coran **17:23**, « وَبِالْوَالِدَيْنِ إِحْسَانًا » | Numéro et texte confirmés : « وقضى ربك ألا تعبدوا إلا إياه وبالوالدين إحسانا » (sourate al-Isra', verset 23). Le verset n'est **ni affiché en arabe, ni récité** : la voix dit seulement « Le Coran demande l'ihsan envers les parents ». Le mot isolé « الإِحْسَان » prononcé en arabe n'est pas une récitation. Conforme à la règle Coran 7:204. | https://quran.com/17/23 |

Mots arabes (الْإِحْسَانُ, الْإِسْلَامُ, الْإِيمَانُ, فِي الصَّلَاةِ, فِي الْعَمَلِ, مَعَ النَّاسِ, الصَّلَاةُ, الْعَمَلُ, الْأَخْلَاقُ) : vocalisation correcte.

### Corrections appliquées
| # | Scène / champ | Avant | Après | Pourquoi |
|---|---|---|---|---|
| 1 | `title` du fichier + accroche `subtitle` | « …le plus haut degré de la foi » | « …le plus haut degré de la religion » | Même raison que la correction 5 de l'ép. 7. C'est aussi cohérent avec « Les trois niveaux de la religion » (étape 1). |
| 2 | Étape 1, `text` | « la Chahada » | « la Shahada » | Cohérence avec l'ép. 1 publié. |

### Conclusions sur les doutes (ép. 8)
1. **Islam = les actes, iman = la foi du cœur** : c'est la répartition du hadith de Jibril, où les deux termes sont nommés ensemble. C'est aussi la formulation la plus sûre : dire que l'iman inclut les actes reprendrait une divergence (position de la majorité d'Ahl as-Sunna, que les hanafites et maturidites ne partagent pas). OK, sans correction.
2. **Fusion des deux degrés de l'ihsan** : fidèle au hadith (« comme si tu Le voyais… Lui te voit »). OK.
3. **Muslim 1955, première phrase seulement** : OK (voir le tableau).
4. **Coran 17:23** : mentionné, non récité. OK.
5. **« Jibril a demandé… » à l'oral** : acceptable. La précision « venu sous l'apparence d'un homme » reste à l'écran, et le hadith confirme que c'était Jibril.
6. **Exemples** (prière sans se presser, travail bien fait, douceur avec les parents, parole tenue, sourire) : consensuels et sans polémique. OK.
7. **Libellés « NIVEAU » / « AU QUOTIDIEN »** : question de montage, aucun enjeu religieux.
8. **Outro sans sujet** : OK.

### Points qui restent à la décision humaine (ép. 8)
- **O.** Étape 1 : « la zakat… le hajj » en minuscules, alors que l'ép. 1 affiche « la Zakat… le Hajj ». C'est un alignement typographique : je ne l'ai pas fait, à confirmer.
- **P.** À l'oral, « l'islam » est dit en français, puis « l'iman » et « l'ihsan » en arabe. Ce n'est pas une erreur. Pour plus d'homogénéité, on peut ajouter la clé `("l'islam", "الإِسْلَام")`, mais elle changerait aussi l'accroche de l'ép. 7 (« fait entrer dans l'islam »), où le français est préférable.
- **Q.** L'étape 5 cite le hadith à l'oral (« Le Prophète, paix et salut sur lui, a dit… ») sans dire la source ; la source (Muslim, n° 1955) est à l'écran. Si Karim veut que la voix suive la même règle que les autres citations, il faut ajouter « Rapporté par Muslim. » (3 mots ; total 193).


---

## Fichiers Azure (`tools/azure/make_textes.py`, `tools/azure/textes/`)

- **Modification ciblée de MOTS** (une seule ligne, fichier relu juste avant, car un autre agent y a ajouté des lignes pour comp1) : `("Chahada", "شَهَادَة")` → `("Shahada", "شَهَادَة")`. Aucune narration de la série n'utilise encore « Chahada ». L'ép. 1 dit « la Shahada » à l'oral : la clé lui servira s'il passe un jour par `make_textes.py`.
- Régénération : `python3 tools/azure/make_textes.py episodes/ep6_priere_partie2.json episodes/ep7_chahada.json episodes/ep8_ihsan.json` donne 9, 9 et 10 scènes.
- Relecture des `.txt` : toutes les balises `[ar:…|…]` sont fermées (ép. 6 : 30, ép. 7 : 11, ép. 8 : 10) et ne contiennent que de l'arabe. Aucun article n'est doublé (« la [ar:شَهَادَة|Shahada] », « du [ar:ظُهْر|Dhuhr] », « [ar:العَصْر|l'Asr] », « [ar:الإِحْسَان|l'ihsan] »). Aucune phrase n'est coupée par erreur entre les deux langues : la formule complète de la Shahada est balisée d'un seul bloc, « Muhammadan » de l'étape 4 aussi, et « Allah » seul reste en français, comme dans les épisodes précédents.
- **À écouter en mode « fr »** : vérifier que Vivienne lit « Shahada » avec le son « ch » (graphie « sh »). En mode « ar », le mot est dit en arabe.
- **Rappel (signalé par le scénariste, toujours valable)** : la clé « illa Allah » se déclencherait au milieu de la formule de l'ép. 2, étape 8. Avant de passer l'ép. 2 dans `make_textes.py`, il faut ajouter un champ `azure` à cette scène, ou une clé pour la formule complète de l'ép. 2.
