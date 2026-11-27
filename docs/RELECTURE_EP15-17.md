# Relecture religieuse : épisodes 15, 16 et 17 (Qalb Mousafir, « Les bases »)

Relecteur indépendant. Date : 27/11/2026.
Copies d'origine conservées : `episodes/ep15_aid.orig.json`, `episodes/ep16_anges.orig.json`, `episodes/ep17_invocations.orig.json`.
Voix : Azure. Le champ lu est `narration`, et `tts` = `narration` dans toutes les scènes (vérifié par script).


## Synthèse

| Ép. | Verdict | Corrections | Mots de narration avant → après | Max `text` | Points pour Karim |
|---|---|---|---|---|---|
| 15 Les deux fêtes | **Validé avec corrections** | 3 (texte arabe du hadith, « bélier », « exalté soit-Il » manquant) + 2 clés Azure | 187 → **198** | 107 car. | 5 |
| 16 Les anges | **Validé avec corrections** | 3 (« deux anges » pour 82:10-11, « paix sur lui / sur eux » manquants) | 156 → **165** | 101 car. | 4 |
| 17 Les invocations | **Validé avec corrections mineures** | 1 (références à l'écran) | 143 → **143** | 108 car. | 3 |

Mots comptés séparés par des espaces, sans la ponctuation seule (« l'argent » = 1 mot). Si l'on coupe aussi aux apostrophes : 210, 171 et 146 (voir K15-5).

Contrôles passés sur les 3 fichiers :
- `python3 -m json.tool` OK ; fichiers réécrits en `json.dump(indent=1, ensure_ascii=False)` ;
- `tts` = `narration` partout, aucun ﷺ dans `narration` / `tts` ;
- tous les `text` font 110 caractères ou moins (max 108) ;
- ﷺ à l'écran après chaque « Prophète » (Muhammad) des champs affichés (intros des citations des ép. 15 et 16), sans ponctuation collée (vérifié par script) ; « paix et salut sur lui » à l'oral après chaque mention (citations des ép. 15 et 16). L'ép. 17 ne nomme pas le Prophète ﷺ ;
- « Allah, exalté soit-Il » : une fois par épisode (ép. 15 : ajouté à l'étape 3, correction 15-3 ; ép. 16 : étape 5 ; ép. 17 : intro de la citation coranique) ;
- « paix sur lui » : Ibrahim (ép. 15 étape 3, écran et oral), Jibril (ép. 16 étape 3 et résumé, correction 16-3) ; « paix sur eux » : anges (ép. 16 étapes 1 et 4) et prophètes (ép. 16 étape 3) ; « qu'Allah l'agrée » : Anas (ép. 15, intro à l'écran ; il n'est pas nommé à l'oral) ;
- **Coran jamais lu par la voix** : 2:152 (ép. 17) affiché en arabe, seule la traduction est lue ; « لَا يَعْصُونَ » (66:6) et « كِرَامًا كَاتِبِينَ » (82:11) sont des mots-titres affichés, jamais lus en arabe ; aucune balise `[ar:…]` sur ces passages dans les `.txt` Azure ;
- aucun visuel de personne, d'ange ou de prophète (hook / quote / step / recap / outro, sans `decor`) ;
- `tools/check.py` non lancé (module `kokoro_onnx` absent, comme pour les ép. 9 à 14). Schéma vérifié à la main (`total` = 5, recap à 5 items).

### Accès aux sites de référence
- **quran.com : lu** pour 2:152, 37:102, 37:107, 66:6 et 82:10-12.
- **sunnah.com : lu** pour an-Nasa'i 1556, Muslim 2996, Muslim 2022, al-Bukhari 957, 1509, 5376 et 6312 ; **beta.sunnah.com : lu** pour Abu Dawud 1134 (la page sunnah.com:abudawud:1134 s'affiche sans le texte arabe). **Bloqués ou non lus** : sunnah.com muslim:2734 (erreur du site), sunnah.com bukhari:1503 (erreur du site), beta.sunnah.com muslim:2734, bukhari:1503 et bukhari:5545 (autorisation non accordée à temps). Muslim 2734 a été lu sur **hadeethenc.com** ; al-Bukhari 1503 sur **en.tohed.com**. al-Bukhari 5545 (sacrifice après la prière) : non lu.
- Limite de l'outil : les pages ne sont rendues que par extraits de 125 caractères au plus. Les textes arabes ci-dessous sont les extraits lus, pas les hadiths entiers.


---

## Épisode 15 : Les deux fêtes (`ep15_aid.json`) : VALIDÉ AVEC CORRECTIONS

### Citations vérifiées
| Citation | Résultat | Source |
|---|---|---|
| **Abu Dawud 1134** (Anas ibn Malik) | Texte lu : « إِنَّ اللَّهَ قَدْ أَبْدَلَكُمْ بِهِمَا خَيْرًا مِنْهُمَا يَوْمَ الأَضْحَى وَيَوْمَ الْفِطْرِ ». Même texte sur en.tohed.com (« …خَيْرًا مِنْهُمَا : يَوْمَ الْأَضْحَى ، وَيَوْمَ الْفِطْرِ »). Début : « قَدِمَ رَسُولُ اللَّهِ ﷺ الْمَدِينَةَ وَلَهُمْ يَوْمَانِ يَلْعَبُونَ فِيهِمَا ». Jugement : **sahih (al-Albani)** ; Zubair Ali Zai : chaîne sahih. L'arabe écrit de mémoire (« قَدْ أَبْدَلَكُمُ اللهُ بِهِمَا… ») était **faux** : il manquait « إِنَّ », et l'ordre « أَبْدَلَكُمُ اللهُ » est celui d'an-Nasa'i, mélangé avec l'ordre Adha/Fitr d'Abu Dawud. **Remplacé** (15-1). | https://beta.sunnah.com/abudawud:1134 · https://en.tohed.com/hadith/abu-dawud/1134 · https://sunnah.com/abudawud:1134 (anglais seulement) |
| **an-Nasa'i 1556** (Anas) | Lu : « وَقَدْ أَبْدَلَكُمُ اللَّهُ بِهِمَا خَيْرًا مِنْهُمَا يَوْمَ الْفِطْرِ وَيَوْمَ الأَضْحَى » (ordre Fitr puis Adha). Sahih (Darussalam). Même sens : cité en seconde référence. Le texte affiché reste celui d'Abu Dawud. | https://sunnah.com/nasai:1556 |
| Coran **37:102-107** (sacrifice) | 37:107 : « وَفَدَيۡنَٰهُ بِذِبۡحٍ عَظِيمٖ » = « Nous l'avons racheté par un sacrifice immense ». Le fils n'est pas nommé (« يَا بُنَيَّ ») ; **le verset ne dit pas « bélier »** : le bélier vient de l'exégèse (avis répandu), pas du texte. Corrigé (15-2). | https://quran.com/37/102-107 · https://quran.com/37/107 |
| Zakat al-fitr : **al-Bukhari 1503 / 1509** (Ibn 'Umar) | 1503 : due « عَلَى الْعَبْدِ وَالْحُرِّ وَالذَّكَرِ وَالْأُنْثَى وَالصَّغِيرِ وَالْكَبِيرِ مِنَ الْمُسْلِمِينَ », à donner « قَبْلَ خُرُوجِ النَّاسِ إِلَى الصَّلَاةِ » ; 1509 : « أَمَرَ بِزَكَاةِ الْفِطْرِ قَبْلَ خُرُوجِ النَّاسِ إِلَى الصَّلاَةِ ». Le script (« avant la prière », « pour soi et pour sa famille à charge ») est conforme. Non cité à l'écran. | https://sunnah.com/bukhari:1509 · https://en.tohed.com/hadith/bukhari/1503 |
| Sermon après la prière : **al-Bukhari 957** (Ibn 'Umar) | Lu : « ثُمَّ يَخْطُبُ بَعْدَ الصَّلاَةِ », pour les deux Aïd. Le script (« une prière en groupe, suivie d'un sermon ») est conforme. | https://sunnah.com/bukhari:957 |

Mots arabes : الْعِيدَانِ (duel), عِيدُ الْفِطْرِ, زَكَاةُ الْفِطْرِ, عِيدُ الْأَضْحَى, الْأُضْحِيَّةُ (alif damma, ya chadda), صَلَاةُ الْعِيدِ : corrects.

### Fiqh (formulé sans trancher)
- **Aïd al-Fitr le 1er Shawwal**, **Aïd al-Adha le 10 Dhou al-Hijja** (jour du sacrifice, pendant le hajj) : consensus. OK.
- **Zakat al-fitr** : obligatoire pour chaque musulman, que l'on donne pour soi et pour ceux dont on a la charge (al-Bukhari 1503) ; la donner avant la prière de l'Aïd est l'ordre du hadith (1509). Le début exact du temps (coucher du soleil la veille ou aube de l'Aïd) et l'avance permise (un ou deux jours, ou plus selon les écoles) divergent : non cités, bien. La condition de moyens (surplus du jour, ou nisab chez les hanafites) n'est pas citée : voir K15-2.
- **But** : « pour que les pauvres puissent aussi fêter » : rejoint « طُعْمَةً لِلْمَسَاكِينِ » (Abu Dawud 1609, hasan ; non relu en ligne cette fois). Non présenté comme citation : OK.
- **Sacrifice** : sunna confirmée pour la majorité, obligatoire chez les hanafites pour le résident qui en a les moyens. « Ceux qui le peuvent sacrifient une bête » ne tranche pas : OK. Le partage (famille, voisins, pauvres) est la pratique recommandée, pas une obligation de proportions : la formule descriptive convient.
- **Prière de l'Aïd** : le matin, en groupe, sermon après la prière (al-Bukhari 957). Statut divergent (obligatoire chez les hanafites, sunna confirmée chez les malikites et chafiites, obligation collective chez les hanbalites) : non cité, bien.
- **« Aïd moubarak »** : formule d'usage, présentée comme coutume (« on se souhaite »), pas comme sunna : OK (voir K15-3).

### Corrections appliquées
| # | Scène / champ | Avant | Après | Pourquoi |
|---|---|---|---|---|
| 15-1 | Citation, `arabic` | « قَدْ أَبْدَلَكُمُ اللهُ بِهِمَا خَيْرًا مِنْهُمَا: يَوْمَ الْأَضْحَى وَيَوْمَ الْفِطْرِ » | « إِنَّ اللَّهَ قَدْ أَبْدَلَكُمْ بِهِمَا خَيْرًا مِنْهُمَا: يَوْمَ الْأَضْحَى وَيَوْمَ الْفِطْرِ » | Texte exact d'Abu Dawud 1134 (beta.sunnah.com et tohed.com). Hamza de « الْأَضْحَى » en graphie courante (convention de la série). |
| 15-1b | Citation, `source` | « Rapporté par Abu Dawud (n° 1134) » | « Rapporté par Abu Dawud (n° 1134) et an-Nasa'i (n° 1556) ; authentifié par al-Albani » | Seconde référence et jugement (hors Bukhari/Muslim : même convention que comp1). |
| 15-1c | Citation, `translation` | « Allah vous les a remplacées par deux jours meilleurs : … » | « Allah vous a donné à leur place deux jours meilleurs : le jour de l'Adha et le jour du Fitr. » | « remplacées » était mal accordé (les *jours*) ; même formule qu'à l'oral. |
| 15-1d | Citation, `narration` | « Le Prophète, paix et salut sur lui, a dit : « … » Rapporté par Abu Dawud. » | « À Médine, les gens avaient deux jours de jeux d'avant l'islam. Le Prophète, paix et salut sur lui, a dit : « … » Rapporté par Abu Dawud et an-Nasa'i. » | Sans le contexte du hadith, « à leur place » ne veut rien dire pour l'auditeur (+14 mots). |
| 15-2 | Étape 3, `narration` | « …paix sur lui, et Allah a remplacé son fils par un bélier. » | « …paix sur lui. Allah, exalté soit-Il, a racheté son fils par un sacrifice immense. » | Fidèle à 37:107 (« بِذِبۡحٍ عَظِيمٍ ») ; le verset ne nomme ni le fils ni l'animal. |
| 15-3 | Même phrase | — | « Allah, exalté soit-Il » | La formule manquait dans l'épisode. |
| 15-4 | Étape 3 et résumé, `narration` | « le dix du mois de Dhou al-Hijja » ; « l'Aïd al-Fitr après Ramadan, … » | « le dix de Dhou al-Hijja » ; « l'Aïd al-Fitr, … » | Compensation pour rester sous 200 mots (203 → 198). Aucun changement de sens. |

### Points laissés à Karim (ép. 15)
- **K15-1.** Le bélier : c'est l'avis répandu des exégètes (non relu en ligne ici), pas le texte du verset. Si Karim tient au mot, écrire « Allah a racheté son fils par un sacrifice immense, un bélier selon les exégètes » (+5 mots, 198 → 203 : il faudrait couper ailleurs). Non modifié.
- **K15-2.** Zakat al-fitr : ajouter « si on en a les moyens » serait plus précis (la condition varie selon les écoles, la formule ne tranche pas). Écran : « Ceux qui le peuvent la donnent pour eux et leur famille à charge, pour que les pauvres fêtent aussi. » (≈ 97 car.). Non modifié (budget de mots).
- **K15-3.** Formule des Compagnons pour l'Aïd : « تَقَبَّلَ اللَّهُ مِنَّا وَمِنْكُمْ » (rapportée avec une chaîne jugée bonne par Ibn Hajar ; non relu en ligne ici). On peut la citer à la place ou à côté de « Aïd moubarak ». Non modifié.
- **K15-4.** Étape 4 : le sacrifice se fait **après la prière de l'Aïd** (al-Bukhari 5545 et suivants ; page non lue cette fois). Point utile et largement admis ; le début exact du temps diffère (prière faite ou temps de la prière écoulé selon les écoles), donc « après la prière » décrit la pratique sans trancher. Non ajouté (budget de mots).
- **K15-5.** 198 mots (≤ 200) ; 210 si l'on coupe aux apostrophes. Pour de la marge : retirer « juste » à l'étape 1 (−1) ou « Puis on se souhaite : Aïd moubarak ! » à l'étape 5 (−6).


---

## Épisode 16 : Les anges (`ep16_anges.json`) : VALIDÉ AVEC CORRECTIONS

### Citations vérifiées
| Citation | Résultat | Source |
|---|---|---|
| **Muslim 2996** « خُلِقَتِ الْمَلَائِكَةُ مِنْ نُورٍ » | **Conforme** : début du hadith d'Aïcha, qu'Allah l'agrée : « خُلِقَتِ الْمَلاَئِكَةُ مِنْ نُورٍ وَخُلِقَ الْجَانُّ مِنْ مَارِجٍ مِنْ نَارٍ وَخُلِقَ آدَمُ مِمَّا وُصِفَ لَكُمْ ». « الْمَلَائِكَةُ » / « الْمَلاَئِكَةُ » : même mot, graphie courante. La coupe après « نُورٍ » est propre (fin de proposition). Traduction fidèle. Référence exacte (Muslim 2996, livre 55, n° 78). | https://sunnah.com/muslim:2996 |
| Coran **66:6** « لَا يَعْصُونَ » | Lu : « …عَلَيۡهَا مَلَٰٓئِكَةٌ غِلَاظٞ شِدَادٞ لَّا يَعۡصُونَ ٱللَّهَ مَآ أَمَرَهُمۡ وَيَفۡعَلُونَ مَا يُؤۡمَرُونَ ». Le texte de l'étape 2 en est la traduction fidèle. Contexte : le verset parle des anges **gardiens du Feu** ; les savants en tirent une qualité de tous les anges, appuyée par d'autres versets (voir K16-1). Non modifié. | https://quran.com/66/6 |
| Coran **82:10-12** « كِرَامًا كَاتِبِينَ » | Lu : 82:10 « وَإِنَّ عَلَيۡكُمۡ لَحَٰفِظِينَ », 82:11 « كِرَامٗا كَٰتِبِينَ », 82:12 « يَعۡلَمُونَ مَا تَفۡعَلُونَ ». Le mot-titre « كِرَامًا كَاتِبِينَ » est exact (graphie courante). **Le passage ne dit pas « deux anges »** (le nombre deux vient de 50:17, « الْمُتَلَقِّيَانِ », non cité) : corrigé (16-1). 82:12 (« ils savent ce que vous faites ») justifie « même quand on est seul » : référence étendue à 10-12. | https://quran.com/82/10-12 |

Mots arabes : الْمَلَائِكَةُ, الْإِيمَانُ بِالْمَلَائِكَةِ, لَا يَعْصُونَ, جِبْرِيلُ, أَدْوَارٌ (pluriel de دَوْر, tanwin damma), كِرَامًا كَاتِبِينَ (accusatif, comme dans le verset) : corrects.

### Croyance (formulé sans trancher)
- **Un des six piliers de la foi** : hadith de Jibril (Muslim 8, déjà vérifié à l'ép. 4). OK, et renvoi à l'ép. 4 juste (`ep4_6_piliers_foi`).
- **Créés de lumière, invisibles, obéissants** : consensus. OK.
- **Jibril, l'ange de la révélation** : 2:97, 26:193-194 (non relus en ligne cette fois). OK.
- **L'ange de la mort** : « مَلَكُ الْمَوْتِ » (32:11, non relu en ligne cette fois). Le script ne lui donne **pas** de nom propre : bien (« 'Azra'il » ne vient d'aucun texte authentique).
- **L'ange de la trompe** : le Coran parle du souffle dans la trompe (« وَنُفِخَ فِي الصُّورِ », 39:68, non relu en ligne cette fois) sans nommer l'ange. Le nom « Israfil » est répandu chez les savants mais ne vient pas d'un texte explicite et sûr. Le script dit « un ange soufflera dans la trompe » sans le nommer : **conforme à la consigne**, non modifié.
- **Les nobles scribes** : 82:10-12 ; « bons et mauvais » rejoint 50:18 (« مَا يَلْفِظُ مِنْ قَوْلٍ إِلَّا لَدَيْهِ رَقِيبٌ عَتِيدٌ », non relu en ligne). OK.
- **Accroche** « Ils sont autour de toi en ce moment » : justifiée par 82:10 (« عَلَيْكُمْ لَحَافِظِينَ ») et l'étape 5. OK.

### Corrections appliquées
| # | Scène / champ | Avant | Après | Pourquoi |
|---|---|---|---|---|
| 16-1 | Étape 5, `text` | « Deux anges notent nos actes, bons et mauvais (Coran 82:10-11). Même quand on est seul. » | « Des anges nobles notent nos actes, bons et mauvais (Coran 82:10-12). Même quand on est seul. » (92 car.) | 82:10-11 ne parle pas de « deux » anges ; 82:12 fonde « même quand on est seul ». « nobles » traduit « كِرَامًا » affiché. La narration disait déjà « des anges ». |
| 16-2 | Étape 1, `narration` | « croire aux anges est l'un des six piliers… » | « croire aux anges, paix sur eux, est l'un des six piliers… » | « paix sur eux » à la première mention des anges (+3 mots). |
| 16-3 | Étape 3, `text` + `narration` | « …a apporté la révélation aux prophètes. » | « …a apporté la révélation aux prophètes, paix sur eux. » (74 car.) | « paix sur eux » pour les prophètes (+3 mots). |
| 16-3b | Résumé, `narration` | « …Jibril, d'autres rôles… » | « …Jibril, paix sur lui, d'autres rôles… » | « paix sur lui » à chaque mention de Jibril (+3 mots). |

### Points laissés à Karim (ép. 16)
- **K16-1.** Étape 2 : 66:6 parle des anges gardiens du Feu. Pour une référence sur **tous** les anges, ajouter 16:50 (« وَيَفْعَلُونَ مَا يُؤْمَرُونَ », après « وَالْمَلَائِكَةُ » au verset 49) ou 21:27 : `text` « …ce qui leur est ordonné (Coran 66:6 ; 16:50). » (≈ 88 car.). Versets non relus en ligne cette fois : à vérifier sur quran.com avant. Non modifié.
- **K16-2.** Citation : nommer la narratrice à l'écran : « Aïcha, qu'Allah l'agrée, rapporte que le Prophète ﷺ a dit : » (comme Anas à l'ép. 15). Non modifié.
- **K16-3.** « Paix sur eux » n'est pas répété à chaque « ils » / « des anges » (étapes 2 et 5, accroche) : cela alourdirait la voix. Il est dit à la 1re mention (étape 1) et après les rôles (étape 4). Si Karim veut la formule à chaque mention, il faut l'ajouter étape 5 (+3 mots, 165 → 168).
- **K16-4.** Le contrôle `Prophète`/ﷺ ne s'applique pas : le Prophète ﷺ n'est mentionné qu'à la citation (OK). 165 mots : marge de 35 mots.


---

## Épisode 17 : Les invocations du quotidien (`ep17_invocations.json`) : VALIDÉ AVEC CORRECTIONS MINEURES

### Citations vérifiées
| Citation | Résultat | Source |
|---|---|---|
| Coran **2:152** « فَاذْكُرُونِي أَذْكُرْكُمْ » | **Identique voyelle par voyelle** au début du verset (« فَٱذۡكُرُونِيٓ أَذۡكُرۡكُمۡ وَٱشۡكُرُواْ لِي وَلَا تَكۡفُرُونِ »), graphie courante. Coupe propre (fin de proposition). Traduction fidèle. | https://quran.com/2/152 |
| **al-Bukhari 5376 / Muslim 2022** (Bismillah avant de manger) | Lu (les deux) : « يَا غُلاَمُ سَمِّ اللَّهَ، وَكُلْ بِيَمِينِكَ وَكُلْ مِمَّا يَلِيكَ », hadith de 'Umar ibn Abi Salama, qu'Allah l'agrée. « سَمِّ اللَّهَ » = « mentionne le nom d'Allah », c'est-à-dire dire « Bismillah » : « on dit Bismillah » est juste. Muslim : n° 2022a. Statut (sunna pour la majorité, obligatoire selon certains) : non cité, bien. | https://sunnah.com/bukhari:5376 · https://sunnah.com/muslim:2022 |
| **Muslim 2734** (louer Allah après le repas) | Lu sur hadeethenc.com : « إِنَّ اللهَ لَيَرْضَى عَنِ الْعَبْدِ أَنْ يَأْكُلَ الْأَكْلَةَ فَيَحْمَدَهُ عَلَيْهَا… » (Anas, Muslim 2734, sahih). Fonde « après le repas, on dit al-hamdu lillah ». sunnah.com en erreur. | https://hadeethenc.com/en/browse/hadith/5798 · https://sunnah.com/muslim:2734 (page en erreur) |
| **al-Bukhari 6312** (coucher et réveil) | Lu (Hudhayfa, qu'Allah l'agrée) : coucher « بِاسْمِكَ أَمُوتُ وَأَحْيَا » (**sans « اللَّهُمَّ »**, comme demandé) ; réveil « الْحَمْدُ لِلَّهِ الَّذِي أَحْيَانَا بَعْدَ مَا أَمَاتَنَا وَإِلَيْهِ النُّشُورُ ». Les mots arabes affichés aux étapes 3 et 4 sont **identiques** (l'étape 3 n'affiche que le début, voir K17-1). Traductions fidèles : « C'est en Ton nom que je meurs et que je vis » ; « Louange à Allah qui nous a redonné la vie après nous avoir fait mourir, et vers Lui est la résurrection » (النُّشُور = la résurrection). « Ces deux invocations sont rapportées par al-Bukhari » : exact (même hadith). | https://sunnah.com/bukhari:6312 |

Mots arabes : الْأَذْكَارُ, بِسْمِ اللهِ, الْحَمْدُ لِلَّهِ, الِاسْتِيقَاظُ (alif wasla, kasra de liaison sur le lam), النَّوْمُ, خُطْوَةً خُطْوَةً : corrects. Prochain épisode « الْحَلَالُ وَالْحَرَامُ » : correct.

### Fond
- « Le sommeil est comme une petite mort » : l'invocation elle-même dit « après nous avoir fait mourir » ; cf. 39:42 (non relu en ligne). Présenté comme comparaison : OK.
- « Commence par une seule cette semaine » : conseil pédagogique, pas une règle religieuse : OK.

### Corrections appliquées
| # | Scène / champ | Avant | Après | Pourquoi |
|---|---|---|---|---|
| 17-1 | Étape 1, `text` | « Avant de manger, on dit « Bismillah » : au nom d'Allah. » | « …au nom d'Allah (al-Bukhari 5376, Muslim 2022). » (86 car.) | Référence exacte à l'écran, comme pour 6312. |
| 17-1b | Étape 2, `text` | « Après le repas, on dit « Al-hamdu lillah » : louange à Allah. » | « …louange à Allah (Muslim 2734). » (75 car.) | Même raison. |

### Points laissés à Karim (ép. 17)
- **K17-1.** Étape 3 : l'arabe affiché n'est que le début de l'invocation (« الْحَمْدُ لِلَّهِ الَّذِي أَحْيَانَا »), alors que le `text` traduit l'invocation entière. Pour qu'on l'apprenne en entier : `arabic` « الْحَمْدُ لِلَّهِ الَّذِي أَحْيَانَا بَعْدَ مَا أَمَاتَنَا وَإِلَيْهِ النُّشُورُ » (texte vérifié ci-dessus), si le rendu accepte une ligne longue. Non modifié (risque de débordement du mot-titre).
- **K17-2.** Al-hamdu lillah après le repas : il existe des formules plus longues authentiques (ex. al-Bukhari 5458, « الْحَمْدُ لِلَّهِ كَثِيرًا طَيِّبًا مُبَارَكًا فِيهِ… » ; non relu en ligne). Le simple « al-hamdu lillah » suffit pour débutants. À garder pour un épisode « suite ».
- **K17-3.** 143 mots : épisode court (≈ 57 s à 150 mots/min, dans la cible 50-75 s). Marge de 57 mots si Karim veut ajouter K17-1 à l'oral ou dire « le Prophète, paix et salut sur lui, disait » avant les invocations 3 et 4.


---

## Point commun aux 3 épisodes
- **G.** Non lus en ligne (bloqués ou non accordés) : sunnah.com muslim:2734 et bukhari:1503 (lus sur hadeethenc.com et en.tohed.com), bukhari:5545. Références citées seulement dans ce rapport, non relues : Abu Dawud 1609, al-Bukhari 5458, Coran 2:97, 16:50, 21:27, 26:193, 32:11, 39:42, 39:68, 50:17-18, formule « تَقَبَّلَ اللَّهُ مِنَّا وَمِنْكُمْ ». Aucune n'est dans les scripts.


## Fichiers Azure (`tools/azure/make_textes.py`, `tools/azure/textes/`)
- `make_textes.py` : **deux clés ajoutées** dans le bloc « ép. 15 à 17 », `("Abu Dawud", "أَبُو دَاوُد")` et `("an-Nasa'i", "النَّسَائِي")` (narration de la citation de l'ép. 15). Aucun autre épisode ne cite ces noms à l'oral, donc rien ne change ailleurs au prochain lancement. « zakat » et « hajj » **non balisés**, comme demandé.
- Régénération : `python3 tools/azure/make_textes.py episodes/ep15_aid.json episodes/ep16_anges.json episodes/ep17_invocations.json` donne 9, 9 et 9 scènes.
- Relecture des `.txt` : balises fermées, aucun article doublé (« de [ar:ذُو الحِجَّة|Dhou al-Hijja] », « par [ar:أَبُو دَاوُد|Abu Dawud] et [ar:النَّسَائِي|an-Nasa'i] », « on dit : [ar:بِسْمِ الله|Bismillah] »). Aucune balise dans la ligne de citation coranique (ép. 17, ligne 02) ni dans les traductions de hadith. Non balisés (mots courants en français) : « Aïd », « Adha », « Fitr », « zakat al-fitr », « Shawwal », « Médine », « hajj ».
- `tools/check.py` non lancé (module `kokoro_onnx` absent).
