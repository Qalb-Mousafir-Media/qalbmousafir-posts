# Relecture religieuse : épisodes 12, 13 et 14 (Qalb Mousafir, « Les bases »)

Relecteur indépendant. Date : 27/11/2026.
Copies d'origine conservées : `episodes/ep12_zakat.orig.json`, `episodes/ep13_hajj.orig.json`, `episodes/ep14_vendredi.orig.json`.
Voix : Azure. Le champ lu est `narration`, et `tts` = `narration` dans toutes les scènes (vérifié par script).


## Synthèse

| Ép. | Verdict | Corrections | Mots de narration avant → après | Max `text` | Points pour Karim |
|---|---|---|---|---|---|
| 12 La zakat | **Validé avec corrections** | 1 (fiqh : 2,5 % aussi pour les marchandises) | 190 → **198** | 107 car. | 4 |
| 13 Le hajj | **Validé avec corrections** | 2 (accroche, dates) + 1 clé Azure | 190 → **194** | 107 car. | 4 |
| 14 La prière du vendredi | **Validé avec corrections** | 2 (« Allah, exalté soit-Il » manquant, ﷺ collé au point) | 184 → **192** | 107 car. | 4 |

Mots comptés séparés par des espaces, sans la ponctuation seule (« l'argent » = 1 mot). Si l'on coupe aussi aux apostrophes (« l' » + « argent »), on obtient 208, 204 et 202 : voir le point K12-4.

Contrôles passés sur les 3 fichiers :
- `python3 -m json.tool` OK ; fichiers réécrits en `json.dump(indent=1, ensure_ascii=False)` ;
- `tts` = `narration` partout, aucun ﷺ dans `narration` / `tts` ;
- tous les `text` font 110 caractères ou moins (max 107) ;
- ﷺ à l'écran après chaque « Prophète » des champs affichés (ép. 14 : intro de la citation, étape 4), sans ponctuation collée (vérifié par script) ; « paix et salut sur lui » à l'oral après chaque mention du Prophète (ép. 13 étape 5, ép. 14 citation et étape 4) ;
- « Allah, exalté soit-Il » : une fois par épisode (ép. 12 et 13 : intro de la citation coranique ; ép. 14 : ajouté à l'étape 1, correction 14-1) ;
- « paix sur lui » à chaque mention d'un prophète autre que Muhammad ﷺ (nouvelle règle) : Ibrahim, ép. 13 étape 5, à l'écran et à l'oral. Jibril et les autres prophètes ne sont pas cités. Aucun Compagnon nommé (le narrateur de Muslim 854, Abu Hurayra, n'est pas cité) ;
- **Coran jamais lu par la voix** : 2:43 et 3:97 sont affichés en arabe, la voix ne lit que la traduction française ; aucune balise `[ar:…]` dans ces lignes des `.txt` Azure. 62:9 (ép. 14) est seulement évoqué (« comme Allah… l'ordonne dans le Coran »), ni affiché ni lu ;
- aucun visuel de personne (hook / quote / step / recap / outro, sans `decor`) ;
- `tools/check.py` non lancé (module `kokoro_onnx` absent, comme pour les ép. 9 à 11). Schéma vérifié à la main (types, `total` = 5, recap à 5 items).

### Accès aux sites de référence
- **quran.com : lu** pour 2:43, 3:97, 9:60 et 62:9 (WebFetch OK, texte affiché en graphie uthmanie mot par mot).
- **sunnah.com : bloqué** (erreur du site sur `muslim:854`, `muslim:854a`, `muslim/7/21`). Muslim 854 a été vérifié sur **hadeethenc.com** (Encyclopédie des hadiths traduits), qui donne le texte vocalisé, « رواه مسلم », « صحيح مسلم (2/ 585) (854) » et le jugement « صحيح ». La recherche web confirme que sunnah.com classe ce texte sous muslim:854 (titre « كتاب الجمعة »).
- « Le hajj, c'est 'Arafa » : lu sur en.tohed.com (Tirmidhi 889). al-Kahf le vendredi : lu sur islamqa.info (n° 10700). « رُبْعُ الْعُشْرِ » : lu sur sounah.com (charh d'al-Bukhari 1454). Nombre de pèlerins : titres de presse (GASTAT) via la recherche, pages non lues.


---

## Épisode 12 : La zakat (`ep12_zakat.json`) : VALIDÉ AVEC CORRECTIONS

### Citations vérifiées
| Citation | Résultat | Source |
|---|---|---|
| Coran **2:43** « وَأَقِيمُوا الصَّلَاةَ وَآتُوا الزَّكَاةَ » | **Conforme** : c'est le début du verset (quran.com : « وَأَقِيمُواْ ٱلصَّلَوٰةَ وَءَاتُواْ ٱلزَّكَوٰةَ وَٱرۡكَعُواْ مَعَ ٱلرَّٰكِعِينَ »). Le script l'écrit en graphie courante (الصَّلَاةَ, الزَّكَاةَ, وَآتُوا sans alif final de pluriel marqué) : même texte, même vocalisation, convention de la série. La suite (« et inclinez-vous avec ceux qui s'inclinent ») n'est ni affichée ni traduite : la coupe est propre (fin de proposition). Traduction fidèle. | https://quran.com/2/43 |
| Coran **9:60** (catégories, cité « (9:60) » à l'étape 4) | **Conforme** : le verset cite **huit** catégories : pauvres (الْفُقَرَاء), nécessiteux (الْمَسَاكِين), ceux qui la collectent, ceux dont on gagne les cœurs, l'affranchissement, les endettés (الْغَارِمِين), dans le sentier d'Allah, le voyageur. Le script cite pauvres, nécessiteux, endettés « et d'autres » : exact. Voir K12-1. | https://quran.com/9/60 |
| « رُبْعُ الْعُشْرِ » (2,5 %) | **Correct** : rub' (ر ضamma, ب soukoun) et 'ushr (ع damma, ش soukoun). C'est l'expression même du hadith d'Anas sur la lettre d'Abu Bakr, qu'Allah l'agrée : « وَفِي الرِّقَةِ رُبْعُ الْعُشْرِ » (al-Bukhari 1454). La page lue écrit « العُشْرِ » sans soukoun sur le lam : convention, pas d'écart. | https://sounah.com/hadith/1398/ · https://sunnah.com/urn/6521510 (adresse) |

Mots arabes : الزَّكَاةُ, الرُّكْنُ الثَّالِثُ, النِّصَابُ, لِمَنْ؟, طُهْرَةٌ (ṭuhra, damma : « purification », cf. 9:103 « تُطَهِّرُهُمْ »), الْحَجُّ : corrects.

### Fiqh (formulé sans trancher)
- **3e pilier** : cohérent avec l'ép. 1 (Shahada, Salat, Zakat, Sawm, Hajj). OK.
- **Sens du mot** : purification et croissance : sens linguistiques admis. OK.
- **Nisab + année lunaire (hawl)** pour l'argent, l'or et les marchandises : conditions communes aux quatre écoles. Le script ne cite pas le hawl pour les récoltes (où il ne s'applique pas) : bien. La manière de compter le nisab pendant l'année (hanafites : au début et à la fin ; les autres : tout au long de l'année) n'est pas fixée par « atteignent… pendant une année lunaire » : OK. La valeur du nisab en grammes (85 g d'or, 595 g d'argent, chiffres usuels mais calculs divergents) n'est pas donnée : prudent.
- **Taux de 2,5 %** : vaut pour l'or, l'argent (et la monnaie) **et les marchandises de commerce**, dans les quatre écoles. L'original le limitait à « l'argent et l'or » alors que l'étape 2 cite les marchandises : **corrigé** (correction 12-1).
- **Bétail, récoltes** : « ont leurs propres règles » : exact et sans détail divergent.
- **Bénéficiaires** : 9:60, consensus sur la liste. OK.
- **« elle ne diminue pas ta richesse »** : rejoint le hadith « مَا نَقَصَتْ صَدَقَةٌ مِنْ مَالٍ » (Muslim 2588, non relu en ligne cette fois) ; non présenté comme citation : OK.
- **« demande à un imam ou à une organisation de confiance »** : bon renvoi, pas de fatwa.

### Corrections appliquées
| # | Scène / champ | Avant | Après | Pourquoi |
|---|---|---|---|---|
| 12-1 | Étape 3, `text` | « Pour l'argent et l'or, le taux est de 2,5 %. D'autres biens (bétail, récoltes) ont leurs propres règles. » | « Pour l'argent, l'or et les marchandises, le taux est de 2,5 %. Bétail et récoltes ont leurs propres règles. » (107 car.) | Le taux de 2,5 % vaut aussi pour les marchandises (quatre écoles). Sinon, l'étape 2 (« argent, or, marchandises ») et l'étape 3 se contredisent. |
| 12-1b | Étape 3, `subtitle` + item 3 du résumé | « Pour l'argent et l'or » | « Argent, or, marchandises » | Même raison. |
| 12-1c | Étape 3, `narration` | « Trois : pour l'argent et l'or, le taux est de deux virgule cinq pour cent. D'autres biens… » | « Trois : pour l'argent, l'or et les marchandises, le taux est de deux virgule cinq pour cent, le quart du dixième. D'autres biens… » | Même raison ; « le quart du dixième » traduit « رُبْعُ الْعُشْرِ » affiché à l'écran (+4 mots). |
| 12-1d | Résumé, `narration` | « …pour cent pour l'argent et l'or, … » | « …pour cent pour l'argent, l'or et les marchandises, … » | Même raison. |

### Points laissés à Karim (ép. 12)
- **K12-1.** Étape 4 : on peut dire « **huit** catégories » (consensus, 9:60) : `subtitle` « Huit catégories » et narration « elle va à huit catégories citées dans le Coran ». Plus précis que « des catégories précises ». Non modifié.
- **K12-2.** « l'argent » est ambigu en français (monnaie ou métal). Le sens « les deux » est juste ici. Si Karim veut lever l'ambiguïté : « l'or, l'argent (métal) et l'épargne ». Non modifié.
- **K12-3.** Accroche : « une partie de ton argent est le droit des pauvres » : vrai pour qui atteint le nisab (cf. 70:24-25 « حَقٌّ مَعْلُومٌ »). Le spectateur sans épargne peut se sentir concerné à tort, mais l'étape 2 le précise. Non modifié.
- **K12-4.** 198 mots (≤ 200) ; 208 si l'on coupe aux apostrophes. Pour avoir de la marge : retirer « le quart du dixième » (−4) ou, au résumé, « pour l'argent, l'or et les marchandises » (−7).


---

## Épisode 13 : Le hajj (`ep13_hajj.json`) : VALIDÉ AVEC CORRECTIONS

### Citations et faits vérifiés
| Élément | Résultat | Source |
|---|---|---|
| Coran **3:97** « وَلِلَّهِ عَلَى النَّاسِ حِجُّ الْبَيْتِ مَنِ اسْتَطَاعَ إِلَيْهِ سَبِيلًا » | **Identique voyelle par voyelle** au passage du verset sur quran.com (« وَلِلَّهِ عَلَى ٱلنَّاسِ حِجُّ ٱلۡبَيۡتِ مَنِ ٱسۡتَطَاعَ إِلَيۡهِ سَبِيلٗا »), graphie courante. « حِجُّ » avec kasra : lecture de Hafs, correcte. Fragment du milieu du verset, coupé à la fin de la proposition (ۚ). Traduction fidèle (proche de Hamidullah). | https://quran.com/3/97 |
| « Le hajj, c'est 'Arafa » (« الْحَجُّ عَرَفَةُ ») | **Authentique** : hadith de 'Abd ar-Rahman ibn Ya'mar, at-Tirmidhi 889, Abu Dawud 1949, an-Nasa'i 3016 (3019 selon les éditions), Ibn Majah 3015 ; jugé sahih par al-Albani. Il justifie « la journée d'Arafat est le cœur du hajj ». Non cité dans le script (voir K13-1). | https://en.tohed.com/hadith/tirmidhi/889 |
| Nombre de pèlerins | GASTAT : **1 673 230** en 2025, **environ 1,70 million** en 2026. « Des millions » était exagéré : corrigé (13-1). | Titres : saudigazette.com.sa/article/652489 ; guardian.ng (« 1.70m pilgrims performed 2026 Hajj ») |

Mots arabes : الْحَجُّ, الرُّكْنُ الْخَامِسُ, ذُو الْحِجَّةِ (ḥijja avec kasra, forme usuelle), الْإِحْرَامُ, الطَّوَافُ وَالسَّعْيُ, صَلَاةُ الْجُمُعَةِ : corrects. « عَرَفَةُ » : nom propre féminin, diptote, nominatif sans tanwin : **correct** (le jour = 'Arafa ; le lieu = 'Arafat).

### Fiqh (formulé sans trancher)
- **5e pilier, une fois dans la vie, pour qui en a les moyens** : consensus (3:97 ; « une fois », Muslim 1337, non relu en ligne). « adulte » et « moyens physiques et financiers » : OK. Points divergents non cités (obligation immédiate ou non, mahram pour la femme) : bien.
- **Dhou al-Hijja** : les rites ont lieu du **8 au 12 ou 13** ; les « premiers jours » de l'original englobait les jours 1 à 7, où il n'y a pas de rite. **Corrigé** (13-2).
- **Ihram** : « entrer en état sacré » : juste. Les deux tissus non cousus pour les hommes : consensus. Les femmes gardent leurs vêtements pudiques habituels : le script dit « Les hommes portent… », donc rien de faux. Statut (pilier chez trois écoles, condition chez les hanafites) : non cité, bien.
- **Tawaf** sept tours ; **sa'y** entre Safa et Marwa (sept trajets) : exact. Statut du sa'y (pilier ou obligatoire selon les écoles) : non cité, bien.
- **Arafat** : la station à 'Arafa est le pilier sans lequel il n'y a pas de hajj : consensus. OK.
- **Traces d'Ibrahim, paix sur lui, et du Prophète ﷺ** : juste (rites liés à Ibrahim, Hajar et Isma'il ; « خُذُوا عَنِّي مَنَاسِكَكُمْ », Muslim 1297, non relu en ligne).

### Corrections appliquées
| # | Scène / champ | Avant | Après | Pourquoi |
|---|---|---|---|---|
| 13-1 | Accroche, `narration` | « Des millions de personnes, habillées pareil, au même endroit, au même moment. C'est le hajj. » | « Plus d'un million et demi de pèlerins, en tenue simple, au même endroit, au même moment. C'est le hajj. » | Chiffre exact (1,67 M en 2025, 1,70 M en 2026). « habillées pareil » est faux pour les femmes, qui n'ont pas de tenue d'ihram fixe. |
| 13-2 | Étape 2, `text` | « Il a lieu chaque année, pendant les premiers jours du mois de Dhou al-Hijja, à La Mecque. » | « Il a lieu chaque année, au mois de Dhou al-Hijja, surtout du 8 au 13, à La Mecque et dans les lieux autour. » (107 car.) | Les rites vont du 8 au 12/13 ; Mina, Muzdalifa et Arafat sont hors de La Mecque (aligné sur la narration). |
| 13-3 | `tools/azure/make_textes.py`, MOTS | — | ajout `("d'Arafat", "عَرَفَة")` | « d'Arafat » (étape 5 et résumé) n'était pas balisé : la règle de la regex refuse un mot précédé d'une apostrophe. |

### Points laissés à Karim (ép. 13)
- **K13-1.** Étape 5 : on peut citer le hadith « Le hajj, c'est 'Arafa » (at-Tirmidhi 889, Abu Dawud 1949, sahih) : `text` « « Le hajj, c'est 'Arafa » (at-Tirmidhi 889). Le hajj suit les traces d'Ibrahim, paix sur lui. » (≈ 95 car.). À l'oral, cela ajoute une mention du Prophète, paix et salut sur lui, et ≈ 10 mots (194 → ≈ 204 : retirer « Riches ou pauvres, tout le monde est égal » pour compenser). Non modifié.
- **K13-2.** Sous-titre de l'étape 4 « Autour de la Kaaba » : vrai pour le tawaf, pas pour le sa'y (Safa et Marwa sont dans la Mosquée sacrée, mais pas autour de la Kaaba). Proposition : « À la Mosquée sacrée ». Non modifié.
- **K13-3.** Ihram : l'ihram, c'est d'abord **l'intention** d'entrer dans les rites, pas le vêtement. Ajout possible à la narration : « le pèlerin fait l'intention et entre dans l'ihram » (+4 mots). Non modifié.
- **K13-4.** « hajj » n'est pas balisé dans `make_textes.py` (comme « zakat » dans les ép. 11 et 12) : en mode « ar », Azure le dit en français. Si Karim veut le mot en arabe, ajouter `("hajj", "حَجّ")` et `("zakat", "زَكَاة")` ; cela changera aussi l'ép. 11 au prochain lancement. Non ajouté.


---

## Épisode 14 : La prière du vendredi (`ep14_vendredi.json`) : VALIDÉ AVEC CORRECTIONS

### Citations vérifiées
| Citation | Résultat | Source |
|---|---|---|
| **Muslim 854** « خَيْرُ يَوْمٍ طَلَعَتْ عَلَيْهِ الشَّمْسُ يَوْمُ الْجُمُعَةِ » | **Identique voyelle par voyelle** au début du hadith sur hadeethenc.com (« خَيْرُ يَوْمٍ طَلَعَتْ عَلَيْهِ الشَّمْسُ يَوْمُ الْجُمُعَةِ، فِيهِ خُلِقَ آدَمُ… »). Abu Hurayra, « صحيح مسلم (2/ 585) (854) », sahih. La suite (création d'Adam, paix sur lui, entrée et sortie du Paradis, l'Heure) n'est pas citée : coupe propre. Traduction fidèle. sunnah.com n'a pas pu être lu (voir G). | https://hadeethenc.com/ar/browse/hadith/3711 · https://sunnah.com/muslim:854 (adresse, page en erreur) |
| Coran **62:9** (ordre de se rendre à la prière du vendredi) | Lu : « يَٰٓأَيُّهَا ٱلَّذِينَ ءَامَنُوٓاْ إِذَا نُودِيَ لِلصَّلَوٰةِ مِن يَوۡمِ ٱلۡجُمُعَةِ… ». Sert de base à l'ajout 14-1 ; ni affiché en arabe ni lu. | https://quran.com/62/9 |
| al-Kahf le vendredi | Hadith d'Abu Sa'id al-Khudri, qu'Allah l'agrée (lumière d'un vendredi à l'autre) : al-Hakim (2/399), al-Bayhaqi (3/249) ; hasan selon Ibn Hajar, sahih selon al-Albani (Sahih al-Jami' 6470). Le script ne le cite pas et dit « selon de nombreux savants » : formulation juste : la recommandation est répandue (notamment chez les chafiites et les hanbalites), mais elle n'est pas formulée de la même façon dans toutes les écoles (position malikite non vérifiée en ligne ici). | https://islamqa.info/en/answers/10700 |

Mots arabes : يَوْمُ الْجُمُعَةِ, الْجُمُعَةُ, الْخُطْبَةُ, مَنْ؟, السُّنَنُ (pluriel de sunna), سُورَةُ الْكَهْفِ, الْعِيدَانِ (duel nominatif) : corrects.

### Fiqh (formulé sans trancher)
- **La jumu'a remplace Dhuhr** : consensus (qui l'a priée ne prie pas Dhuhr). OK.
- **« à l'heure de Dhuhr »** : c'est l'heure de la majorité et la pratique partout ; chez les hanbalites, elle est permise un peu avant le zénith, mais il est préférable de la faire après. La formule décrit la pratique sans trancher : OK.
- **Khutba puis deux rak'at en groupe** : consensus (khutba avant la prière, condition de validité ; deux rak'at ; en groupe). Le nombre de khutbas (deux, ou une suffit chez les hanafites) n'est pas fixé (« le sermon ») : OK.
- **Qui est tenu** : homme, pubère, sain d'esprit, résident, sans excuse ; voyageur et malade dispensés : consensus. **Femme** : non obligatoire, et si elle y assiste, sa prière est valable et remplace Dhuhr : consensus rapporté par Ibn al-Mundhir. OK.
- **Sunan** : ghusl (sunna dans les quatre écoles ; hadith « غُسْلُ يَوْمِ الْجُمُعَةِ وَاجِبٌ عَلَى كُلِّ مُحْتَلِمٍ », al-Bukhari 879, compris comme insistance par la majorité), beaux habits, venir tôt (al-Bukhari 881), multiplier les prières sur le Prophète ﷺ (Abu Dawud 1047, sahih) : « recommandé » est juste. Références non relues en ligne cette fois.

### Corrections appliquées
| # | Scène / champ | Avant | Après | Pourquoi |
|---|---|---|---|---|
| 14-1 | Étape 1, `narration` | « …se réunissent à la mosquée pour la jumu'a. Elle remplace la prière du Dhuhr. » | « …se réunissent à la mosquée pour la jumu'a, comme Allah, exalté soit-Il, l'ordonne dans le Coran. Elle remplace la prière du Dhuhr. » | Règle « Allah, exalté soit-Il » une fois par épisode : Allah n'était pas nommé dans l'épisode. Fondé sur 62:9 (+8 mots). |
| 14-1b | Étape 1, `text` | « …se réunissent à la mosquée. Elle remplace Dhuhr. » | « …se réunissent à la mosquée (62:9). Elle remplace Dhuhr. » (102 car.) | Référence du verset à l'écran. |
| 14-2 | Étape 4, `text` | « Se laver, bien s'habiller, venir tôt, et multiplier les prières sur le Prophète ﷺ. » | « Se laver, bien s'habiller, venir tôt, et multiplier les prières sur le Prophète ﷺ ce jour-là. » (93 car.) | Le point était collé à ﷺ (même problème de `text_block` que l'ép. 10). |

### Points laissés à Karim (ép. 14)
- **K14-1.** Une règle importante et consensuelle manque : **écouter la khutba en silence** (« إِذَا قُلْتَ لِصَاحِبِكَ يَوْمَ الْجُمُعَةِ أَنْصِتْ وَالْإِمَامُ يَخْطُبُ فَقَدْ لَغَوْتَ », al-Bukhari 934, Muslim 851). Une phrase à l'étape 2 : « Pendant la khutba, on écoute en silence. » (+7 mots, 192 → 199). Non ajouté.
- **K14-2.** Étape 5 : la source du hadith d'al-Kahf (al-Hakim, al-Bayhaqi, authentifié par al-Albani) n'est pas dite. Ce n'est pas un recueil Bukhari/Muslim : garder « selon de nombreux savants » est prudent ; si Karim veut citer le hadith, mettre la source exacte à l'écran.
- **K14-3.** Titre à l'écran « Le vendredi » et titre du fichier « La prière du vendredi » : sans conséquence religieuse, à harmoniser si Karim veut.
- **K14-4.** 192 mots (≤ 200) ; 202 si l'on coupe aux apostrophes. Retirer « Voici pourquoi. » à l'accroche (−2) ou « ce jour-là » à l'étape 5 (−2) si besoin.


---

## Point commun aux 3 épisodes
- **G.** sunnah.com n'a pas répondu (erreur du site). Avant publication, relire Muslim 854 sur https://sunnah.com/muslim:854 (le texte est déjà confirmé sur hadeethenc.com). Les autres références citées seulement dans ce rapport (Muslim 1337, 1297, 2588 ; al-Bukhari 879, 881, 934 ; Abu Dawud 1047) n'ont pas été relues en ligne : elles ne sont pas dans les scripts.


## Fichiers Azure (`tools/azure/make_textes.py`, `tools/azure/textes/`)
- `make_textes.py` : **une clé ajoutée**, `("d'Arafat", "عَرَفَة")`, juste avant `("Arafat", …)`. Rien d'autre changé.
- Régénération : `python3 tools/azure/make_textes.py episodes/ep12_zakat.json episodes/ep13_hajj.json episodes/ep14_vendredi.json` donne 9, 9 et 9 scènes.
- Relecture des `.txt` : balises fermées, aucun article doublé (« le [ar:نِصَاب|nisab] », « dans [ar:الإِحْرَام|l'ihram] », « la journée [ar:عَرَفَة|d'Arafat] », « la [ar:جُمُعَة|jumu'a] »). Aucune balise dans les lignes de citation coranique (2:43, 3:97). Non balisés : « zakat », « hajj » (voir K13-4), « Mecque », « imam », « sourate » (mots courants en français).
- `tools/check.py` non lancé (module `kokoro_onnx` absent).
