# Relecture religieuse : épisodes 9, 10 et 11 (Qalb Mousafir, « Les bases »)

Relecteur indépendant. Date : 27/11/2026.
Copies d'origine conservées : `episodes/ep9_coran.orig.json`, `episodes/ep10_prophete.orig.json`, `episodes/ep11_ramadan.orig.json`.
Voix : Azure. Le champ lu est `narration`, et `tts` = `narration` dans toutes les scènes (vérifié par script).


## Synthèse

| Ép. | Verdict | Corrections | Mots de narration avant → après | Max `text` | Points pour Karim |
|---|---|---|---|---|---|
| 9 Le Coran | **Validé avec corrections** | 3 | 176 → **181** | 87 car. | 3 |
| 10 Le Prophète ﷺ | **Validé avec corrections** | 3 | 171 → **171** | 101 car. | 3 |
| 11 Le jeûne du Ramadan | **Validé avec corrections** | 2 (fiqh + hadith) | 195 → **208** | 110 car. | 5 |

Mots comptés comme pour les ép. 6 à 8 (mots et apostrophes, sans la ponctuation). L'ép. 11 dépasse la limite haute de 200 de 8 mots (voir le point K11-1).

Contrôles passés sur les 3 fichiers :
- `python3 -m json.tool` OK ; fichiers réécrits en `json.dump(indent=1, ensure_ascii=False)` ;
- `tts` = `narration` partout, aucun ﷺ dans `narration` / `tts` ;
- tous les `text` font 110 caractères ou moins ;
- ﷺ à l'écran après chaque « Prophète » / « Muhammad » des champs affichés (titres, `next_title`, `text`, items), sans ponctuation collée (vérifié par script) ; « paix et salut sur lui » à l'oral après chaque mention du Prophète ;
- « Allah, exalté soit-Il » : une fois par épisode (intro de la citation coranique) ;
- « paix sur lui » après Jibril (ép. 9) ; aucun Compagnon nommé dans les 3 épisodes ;
- **Coran jamais lu par la voix de synthèse** : les 3 citations coraniques (15:9, 21:107, 2:183) sont affichées en arabe ; la voix ne lit que la traduction française. Dans les `.txt` Azure, aucune balise `[ar:…]` dans les lignes de citation. Les fragments coraniques affichés seuls (« اقْرَأْ », « بِلِسَانٍ عَرَبِيٍّ ») ne sont pas prononcés en arabe ;
- aucun visuel de personne (scènes hook / quote / step / recap / outro sans `decor` humain) ;
- `tools/check.py` **n'a pas pu tourner** : le module `kokoro_onnx` n'est pas installé dans cet environnement. Schéma vérifié à la main (types, `total` = 5, recap à 5 items). Pas de durées Kokoro.

### Accès aux sites de référence
**Les 6 WebFetch demandés ont été bloqués** (demande d'autorisation restée sans réponse) : quran.com/15/9, /96/1, /21/107, /2/183, /2/184 et sunnah.com/bukhari:1903. Je n'ai pas réessayé. J'ai utilisé à la place la recherche web (WebSearch), qui ne renvoie que les titres et adresses des pages. Les titres des pages de quran.ksu.edu.sa (tafsir de l'Université du roi Saoud) contiennent le verset vocalisé : cela suffit pour 15:9, 21:107 et 96:1. Pour 2:183, 2:184, al-Bukhari 1903 et la sira, la recherche confirme la référence (numéro, narrateur) mais pas le texte voyelle par voyelle : **le contrôle mot à mot sur sunnah.com / quran.com reste à faire** (point G).


---

## Épisode 9 : Le Coran, la parole d'Allah (`ep9_coran.json`) : VALIDÉ AVEC CORRECTIONS

### Citations vérifiées
| Citation | Résultat | Source |
|---|---|---|
| Coran **15:9** « إِنَّا نَحْنُ نَزَّلْنَا الذِّكْرَ وَإِنَّا لَهُ لَحَافِظُونَ » | **Identique voyelle par voyelle** au titre de la page (« إِنَّا نَحْنُ نَزَّلْنَا الذِّكْرَ وَإِنَّا لَهُ لَحَافِظُونَ (9) »). Sourate al-Hijr, verset 9 confirmé. Traduction « C'est Nous qui avons fait descendre le Rappel, et c'est Nous qui en sommes les gardiens » : fidèle (« الذِّكْر » = le Rappel, « لَحَافِظُونَ » = gardiens, l'emphase « إِنَّا نَحْنُ » rendue par « C'est Nous qui »). | https://quran.ksu.edu.sa/tafseer/ibn-katheer-saadi-qortobi/sura15-aya9.html · quran.com/15/9 bloqué |
| Coran **96:1** « اقْرَأْ » (affiché seul ; « (96:1) » dans le `text`) | Le verset est « اقْرَأْ بِاسْمِ رَبِّكَ الَّذِي خَلَقَ » (titre de la page). Le mot affiché est correct et vocalisé (hamza quiescente). Premier mot révélé, dans la grotte de Hira : récit de 'Aïcha, al-Bukhari n° 3 (non relu en ligne cette fois). | https://quran.ksu.edu.sa/tafseer/qortobi/sura96-aya1.html · quran.com/96/1 bloqué |
| « بِلِسَانٍ عَرَبِيٍّ » (étape 5, affiché seul) | Fragment de 26:195 (« بِلِسَانٍ عَرَبِيٍّ مُّبِينٍ »), correctement vocalisé, non prononcé. Voir le point C9-2. | (non vérifié en ligne) |

Mots et nombres : الْقُرْآنُ الْكَرِيمُ, كَلَامُ اللهِ, اقْرَأْ : corrects. « ٢٣ سَنَةً » et « ١١٤ سُورَةً » : le complément d'un nombre de 11 à 99 (et de 100 + 14) est au singulier accusatif : **correct**.

### Corrections appliquées
| # | Scène / champ | Avant | Après | Pourquoi |
|---|---|---|---|---|
| 1 | Étape 3 (23 ans), `text` | « La révélation a duré environ 23 ans, verset après verset, selon les événements. » | « La révélation a duré environ 23 ans, par passages, souvent en lien avec les événements. » (87 car.) | « verset après verset » est inexact : des passages entiers, et des sourates entières (al-Fatiha, al-Kawthar…), sont descendus d'un coup. Et toute la révélation n'est pas liée à un événement (asbab an-nuzul) : « souvent ». |
| 1b | Étape 3, `narration` | « …verset après verset, selon les événements. » | « …par passages, souvent en lien avec les événements. » | Même raison. |
| 2 | Résumé, `narration` | « …révélée par Jibril, pendant vingt-trois ans… » | « …révélée par Jibril, paix sur lui, pendant vingt-trois ans… » | Règle de la chaîne pour Jibril. +3 mots. Voir le point C9-3 (les ép. 4 et 8 ne le font pas). |
| 3 | Outro, `next_title` | « Qui est le Prophète Muhammad » | « Qui est le Prophète Muhammad ﷺ » | ﷺ à l'écran après le nom du Prophète. |

### Points laissés à Karim (ép. 9)
- **C9-1.** Accroche : « Le livre le plus appris par cœur au monde. » C'est une affirmation courante et très probable, mais ce n'est pas un fait religieux vérifiable. Pour être prudent : « Sans doute le livre le plus appris par cœur au monde. » Non modifié.
- **C9-2.** Étape 5 : « بِلِسَانٍ عَرَبِيٍّ » est un fragment de verset sans référence à l'écran. On peut ajouter « (26:195) » dans le `text` (il reste 34 caractères) ou mettre « بِالْعَرَبِيَّةِ » (mot ordinaire). Non modifié.
- **C9-3.** « paix sur lui » après Jibril : appliqué ici (étape 1 et résumé), mais les ép. 4 et 8 déjà validés ne le disent pas. Choisir une règle pour toute la série (une fois par épisode, ou à chaque mention).


---

## Épisode 10 : Qui est le Prophète Muhammad ﷺ ? (`ep10_prophete.json`) : VALIDÉ AVEC CORRECTIONS

### Citations et faits vérifiés
| Élément | Résultat | Source |
|---|---|---|
| Coran **21:107** « وَمَا أَرْسَلْنَاكَ إِلَّا رَحْمَةً لِّلْعَالَمِينَ » | Texte des pages : « وَمَا أَرْسَلْنَاكَ إِلَّا رَحْمَةً لِّلْعَالَمِينَ (107) ». Le script avait « لِلْعَالَمِينَ » (sans shadda sur le lam) : **corrigé** pour suivre le Mushaf (correction 2). Même prononciation, mais le Coran s'écrit comme dans le Mushaf. Traduction « Et Nous ne t'avons envoyé qu'en miséricorde pour les mondes » : fidèle et littérale. | https://quran.ksu.edu.sa/tafseer/ibn-katheer-tabary-saadi/sura21-aya107.html · https://surahquran.com/aya-107-sora-21.html · quran.com/21/107 bloqué |
| Naissance à La Mecque **vers 570** | Exact : l'année de l'Éléphant, 570 ou 571 selon les calculs ; « vers » couvre les deux. | Sira (Ibn Hisham) ; non relu en ligne |
| Orphelin, élevé par **'Abd al-Muttalib puis Abou Talib** | Exact : père mort avant sa naissance, mère morte quand il avait environ 6 ans, grand-père mort quand il avait environ 8 ans, puis son oncle Abou Talib. | Sira ; non relu en ligne |
| **Al-Amin** avant la révélation | Exact et connu : surnom donné par Quraysh (récit de la pierre noire lors de la reconstruction de la Kaaba). | Sira ; non relu en ligne |
| Révélation **à 40 ans, à Hira** ; **13 ans** à La Mecque ; **Hijra 622** ; **décès 632 à 63 ans**, à Médine | Exact. Ibn 'Abbas : « envoyé à quarante ans, il resta à La Mecque treize ans à recevoir la révélation, puis reçut l'ordre d'émigrer, émigra dix ans, et mourut à soixante-trois ans » (al-Bukhari, chapitre « مَبْعَث النَّبِيّ ﷺ » ; n° **3902** et 3851, référence à confirmer, point G). Hira : al-Bukhari 3. 622 et 632 : dates admises (12 Rabi' al-Awwal 11 H pour le décès). | https://sunnah.com/bukhari:3902 · https://sunnah.com/bukhari:3851 (adresses trouvées, pages non lues) |

Mots arabes : مُحَمَّدٌ رَسُولُ اللهِ ﷺ, مَكَّةُ (nom propre diptote, nominatif sans tanwin : correct), الْأَمِينُ, الْهِجْرَةُ, الْمَدِينَةُ : corrects. « حِرَاءُ » : corrigé (correction 3).

### Corrections appliquées
| # | Scène / champ | Avant | Après | Pourquoi |
|---|---|---|---|---|
| 1 | Accroche, `title` | « Qui est le Prophète ? » | « Qui est le Prophète ﷺ ? » | ﷺ à l'écran après « Prophète ». Le « ? » est séparé par une espace : il n'est pas collé au signe (problème de `text_block`). |
| 2 | Citation, `arabic` | « …رَحْمَةً لِلْعَالَمِينَ » | « …رَحْمَةً لِّلْعَالَمِينَ » | Graphie du Mushaf (shadda sur le lam). |
| 3 | Étape 3, `arabic` + item 3 du résumé | « حِرَاءُ » | « غَارُ حِرَاءٍ » | « حِرَاء » se décline avec tanwin (al-Bukhari 3 : « فِي غَارِ حِرَاءٍ ») ; « حِرَاءُ » sans tanwin le traitait comme diptote. « غَارُ حِرَاءٍ » (la grotte de Hira) est correct et colle à « dans la grotte de Hira ». À vérifier en aperçu : deux mots au lieu d'un (largeur dans `recap_row`). |

### Points laissés à Karim (ép. 10)
- **C10-1.** Translittération : « Abou Talib » (avec « ou ») à l'écran, alors que la série écrit « Abu Qatada », « Abu Jahl ». La clé MOTS de `make_textes.py` est « Abou Talib », donc changer l'écran demande aussi de changer la clé. Non modifié.
- **C10-2.** Étape 4 : « le début du calendrier musulman ». Précision possible : le calendrier hégirien commence à l'**année** de la Hijra (fixée sous 'Umar, qu'Allah l'agrée), pas au jour du départ. On peut écrire « l'an 1 du calendrier musulman » (87 car.). Non modifié : la phrase actuelle n'est pas fausse.
- **C10-3.** Le titre du fichier (« Qui est le Prophète Muhammad ﷺ ? ») apparaît dans l'en-tête du `.txt` Azure : ce n'est qu'un commentaire (`#`), il n'est pas lu.


---

## Épisode 11 : Le jeûne du Ramadan (`ep11_ramadan.json`) : VALIDÉ AVEC CORRECTIONS

### Citations vérifiées
| Citation | Résultat | Source |
|---|---|---|
| Coran **2:183** « يَا أَيُّهَا الَّذِينَ آمَنُوا كُتِبَ عَلَيْكُمُ الصِّيَامُ كَمَا كُتِبَ عَلَى الَّذِينَ مِنْ قَبْلِكُمْ لَعَلَّكُمْ تَتَّقُونَ » | Texte et vocalisation conformes au texte connu du verset (al-Baqara 183) ; « مِنْ قَبْلِكُمْ » avec soukoun est la graphie usuelle (le Mushaf écrit « مِن » sans soukoun, ikhfa') : convention, pas d'écart. **Non relu mot à mot en ligne** (pages trouvées, texte non affiché). Traduction fidèle (proche de Hamidullah). | https://quran.ksu.edu.sa/tafseer/ibn-qortobi-katheer-saadi/sura2-aya183.html (adresse) · quran.com/2/183 bloqué |
| Coran **2:184** (fidya) « وَعَلَى الَّذِينَ يُطِيقُونَهُ فِدْيَةٌ طَعَامُ مِسْكِينٍ » | Base de la fidya ; **non affiché**, non cité. Son application au vieillard et au malade sans espoir de guérison vient de l'explication d'Ibn 'Abbas (al-Bukhari 4505). Le statut diverge : obligatoire chez les hanafites, chafiites et hanbalites, recommandée chez les malikites (correction 1). | https://quran.ksu.edu.sa/tafseer/tabary/sura2-aya184.html (adresse) · quran.com/2/184 bloqué |
| **al-Bukhari 1903** (Abu Hurayra) « مَنْ لَمْ يَدَعْ قَوْلَ الزُّورِ وَالْعَمَلَ بِهِ فَلَيْسَ لِلَّهِ حَاجَةٌ فِي أَنْ يَدَعَ طَعَامَهُ وَشَرَابَهُ » | **Numéro et narrateur confirmés** (titre sunnah.com : « Narrated Abu Huraira ») ; texte confirmé sans voyelles par les titres de surahquran.com. Le script **omettait « وَالْعَمَلَ بِهِ » (et le fait d'agir selon lui)** : corrigé (correction 2). L'arabe n'est pas affiché. | https://sunnah.com/bukhari:1903 (adresse, page bloquée) · https://surahquran.com/Hadith-14792.html · https://dorar.net/hadith/sharh/15883 |

Mots arabes : صِيَامُ رَمَضَانَ, الرُّكْنُ الرَّابِعُ, مِنَ الْفَجْرِ إِلَى الْمَغْرِبِ, السَّحُورُ وَالْإِفْطَارُ (« السَّحُور » avec fatha = le repas : correct), الرُّخْصَةُ, أَكْثَرُ مِنَ الطَّعَامِ, الصِّيَامُ, الزَّكَاةُ : corrects.

### Fiqh (formulé sans trancher)
- **4e pilier** : cohérent avec l'ép. 1 publié (ordre de Muslim 16 et du hadith de Jibril, Muslim 8). OK.
- **Intention** : « avec l'intention de jeûner pour Allah » : condition dans les quatre écoles. Le **moment** (la nuit pour les chafiites, malikites et hanbalites ; jusqu'à midi chez les hanafites) et la question d'une intention pour tout le mois (malikites) divergent : le script ne les fixe pas. OK.
- **Ce qui est interdit, de l'aube au coucher du soleil** : manger, boire, relations intimes : consensus. OK.
- **Conditions** (musulman, pubère, sain d'esprit, capable, résident) : non citées. Ce n'est pas une erreur ; voir le point K11-4.
- **Dispenses** : corrigées (correction 1). Malade et voyageur : **permission** de rompre puis rattraper (2:184-185). Femme en règles : elle **ne jeûne pas** (son jeûne ne serait pas valable), et rattrape : consensus. L'original mettait les trois cas sur le même plan (« on rattrape »), comme si la femme avait seulement le choix.
- **Fidya** : l'original disait « nourrit un pauvre pour chaque jour » comme une obligation pour tous. Corrigé : « obligatoire ou conseillé, selon les écoles ». La quantité (un mudd, un demi-sa'…) diverge : non citée.
- **Sahour / iftar** : descriptions justes ; le statut (Sunna) n'est pas dit. OK.

### Corrections appliquées
| # | Scène / champ | Avant | Après | Pourquoi |
|---|---|---|---|---|
| 1 | Étape 4 (dispenses), `text` | « Malade, voyageur, femme en période de règles : on rattrape plus tard. Si c'est impossible à vie : la fidya. » | « Malade ou voyageur : on peut rompre ; en période de règles, on ne jeûne pas. Les jours se rattrapent ensuite. » (109 car.) | Distinguer la permission (malade, voyageur) de l'interdiction (règles). La fidya, dont le statut diverge, passe à l'oral seulement, avec « selon les écoles » (pas la place à l'écran). |
| 1b | Étape 4, `narration` | « Quatre : le malade, le voyageur et la femme pendant ses règles rattrapent les jours plus tard. Celui qui ne pourra jamais jeûner nourrit un pauvre pour chaque jour. » | « Quatre : le malade et le voyageur peuvent rompre, la femme ne jeûne pas pendant ses règles, et tous rattrapent ensuite. Qui ne pourra jamais jeûner nourrit un pauvre par jour : obligatoire ou conseillé, selon les écoles. » | Même raison ; statut de la fidya non tranché. |
| 2 | Étape 5 (hadith), `text` | « « Qui ne délaisse pas le mensonge… Allah n'a pas besoin qu'il délaisse sa nourriture » (al-Bukhari 1903). » | « « Qui ne délaisse pas le mensonge en paroles et en actes, Allah n'a pas besoin qu'il délaisse sa nourriture… » » (110 car.) | « قَوْلَ الزُّورِ وَالْعَمَلَ بِهِ » : la parole fausse **et le fait d'agir selon elle**. Les points de suspension coupaient justement cette partie. Pour tenir en 110 caractères, la source passe au sous-titre. |
| 2b | Étape 5, `subtitle` | « La langue et les actes » | « Rapporté par al-Bukhari (n° 1903) » | La référence exacte reste à l'écran. L'item 5 du résumé garde « La langue et les actes ». |
| 2c | Étape 5, `narration` | « …a dit : celui qui ne délaisse pas le mensonge, Allah n'a pas besoin qu'il délaisse sa nourriture et sa boisson. » | « …a dit : « Celui qui ne délaisse pas le mensonge, en paroles et en actes, Allah n'a pas besoin qu'il délaisse sa nourriture et sa boisson. » » | Même raison ; guillemets pour marquer la citation. |

### Points laissés à Karim (ép. 11)
- **K11-1.** Narration à **208 mots** (limite haute : 200). Pistes, sans perte religieuse : étape 3 « L'iftar, c'est le repas de rupture » → « L'iftar, celui de la rupture » (−1) ; résumé « de l'aube au coucher du soleil » → « de l'aube au coucher » (−2) ; étape 5 « le jeûne, ce n'est pas que le ventre » à retirer (−8).
- **K11-2.** L'étape 5 cite le hadith à l'oral sans dire la source (elle est à l'écran, au sous-titre) — même cas que le point Q de l'ép. 8. Ajouter « Rapporté par al-Bukhari. » coûte 4 mots.
- **K11-3.** Femme enceinte ou qui allaite, et lochies (nifas) : non cités. Les règles du nifas sont les mêmes que celles des règles (consensus) ; pour la femme enceinte ou qui allaite, le rattrapage et la fidya divergent entre écoles. Je recommande de les laisser hors de la vidéo, ou une ligne de légende : « Femme enceinte ou qui allaite : les règles varient selon les écoles, demande à ton imam. »
- **K11-4.** Conditions du jeûne (musulman, pubère, sain d'esprit, capable) : non citées. Si Karim veut un épisode plus complet, elles sont consensuelles et tiennent en une ligne.
- **K11-5.** Résumé, `narration` : « l'iftar » (minuscule) n'est pas balisé par `make_textes.py` (la clé MOTS est « L'iftar », avec majuscule). En mode « ar », la voix le dira en français à cet endroit seulement. Ajouter la clé `("l'iftar", "الإِفْطَار")` dans `make_textes.py` (je n'y ai pas touché : hors des fichiers autorisés).


---

## Point commun aux 3 épisodes
- **G.** Vérification en ligne incomplète (WebFetch bloqué). Avant publication, relire mot à mot sur : https://quran.com/2/183, https://sunnah.com/bukhari:1903, https://sunnah.com/bukhari:3902 (âge de 40 ans, 13 ans, 63 ans). 15:9, 21:107 et 96:1 sont confirmés voyelle par voyelle par quran.ksu.edu.sa.


## Fichiers Azure (`tools/azure/make_textes.py`, `tools/azure/textes/`)
- `make_textes.py` non modifié (les clés des ép. 9 à 11 y étaient déjà).
- Régénération : `python3 tools/azure/make_textes.py episodes/ep9_coran.json episodes/ep10_prophete.json episodes/ep11_ramadan.json` donne 9, 9 et 9 scènes.
- Relecture des `.txt` : balises fermées, aucun article doublé (« la [ar:هِجْرَة|Hijra] », « le [ar:سَحُور|sahour] », « du [ar:مُصْحَف|Mushaf] »). Aucune balise dans les lignes de citation coranique. Seul défaut : « l'iftar » non balisé au résumé de l'ép. 11 (K11-5).
- `tools/check.py` non lancé (module `kokoro_onnx` absent).
