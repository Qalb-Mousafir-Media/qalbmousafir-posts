# Relecture religieuse : épisodes 18 et 19 (Qalb Mousafir, « Les bases »)

Relecteur indépendant. Date : 27/11/2026.
Copies d'origine conservées : `episodes/ep18_halal_haram.orig.json`, `episodes/ep19_comportement.orig.json`.
Voix : Azure. Le champ lu est `narration`, et `tts` = `narration` dans toutes les scènes (vérifié par script).


## Synthèse

| Ép. | Verdict | Corrections | Mots de narration avant → après | Max `text` | Points pour Karim |
|---|---|---|---|---|---|
| 18 Le halal et le haram | **Validé avec corrections** | 5 (« exalté soit-Il » manquant, règle de base formulée sans trancher, adoration, références des interdits, le douteux) + 1 clé Azure | 199 → **200** | 103 car. | 4 |
| 19 Le bon comportement | **Validé avec corrections** | 4 (« Jour de la Résurrection », numéros du hadith de la balance, « paix et salut sur lui » manquant au résumé, résumé redondant) + 1 clé Azure | 190 → **200** | 105 car. | 4 |

Mots comptés **séparés par des espaces, ponctuation isolée comprise** (« : » compte pour 1) : 200 et 200, soit la limite exacte. Sans la ponctuation isolée (méthode du rapport 15-17) : 187 et 188. Pour de la marge, voir K18-4 et K19-4.

Contrôles passés sur les 2 fichiers :
- `python3 -m json.tool` OK ; fichiers réécrits en `json.dump(indent=1, ensure_ascii=False)` ;
- `tts` = `narration` partout, aucun ﷺ dans `narration` / `tts` ;
- tous les `text` font 110 caractères ou moins (max 103 et 105) ;
- ﷺ à l'écran : intros des citations (ép. 18 et 19), titre et `text` de l'étape 2 de l'ép. 19 ; jamais de ponctuation collée (vérifié par script) ; **aucun ﷺ dans un `subtitle` ni dans un item de résumé** (vérifié par script ; l'item 2 du résumé de l'ép. 19 dit « Notre modèle », sans ﷺ) ;
- « paix et salut sur lui » à l'oral après chaque « Prophète » : ép. 18 citation (1/1) ; ép. 19 citation, étapes 1 et 2, résumé (ajouté, 19-3), outro (5/5) ;
- « Allah, exalté soit-Il » : une fois par épisode (ép. 18 étape 4, ajouté, 18-1 ; ép. 19 étape 2) ;
- « qu'Allah l'agrée » : Abou Bakr as-Siddiq (ép. 19 outro). Aucun autre Compagnon nommé (voir K18-1, K19-1) ;
- **Coran jamais lu par la voix** : 68:4 est affiché (mot-titre « خُلُقٍ عَظِيمٍ » et traduction à l'écran), la voix le paraphrase en français ; 5:3, 5:4 et 5:90 ne sont que des références à l'écran. Aucune balise `[ar:…]` sur un passage coranique dans les `.txt` ;
- aucun visuel de personne (hook / quote / step / recap / outro, sans `decor`) ;
- `tools/check.py` non lancé (module `kokoro_onnx` absent, comme pour les ép. 9 à 17). Schéma vérifié à la main (`total` = 5, recap à 5 items).

### Accès aux sites de référence
- **quran.com : lu** pour 5:3, 5:4, 5:90 et 68:4.
- **sunnah.com : lu** pour al-Bukhari 52, Muslim 1599a, Muslim 2003a, Abu Dawud 4799, al-Bukhari 6035 (traduction et références ; la page s'affiche sans l'arabe) ; **beta.sunnah.com : lu** pour al-Bukhari 6035 (arabe) et at-Tirmidhi 2002 (sunnah.com tirmidhi:2002 en erreur).
- Limite de l'outil : extraits de 125 caractères au plus. Pour al-Bukhari 52, seul le début arabe a été lu ; la suite (« celui qui se garde des choses douteuses préserve sa religion et son honneur ») n'a été lue qu'en résumé anglais.


---

## Épisode 18 : Le halal et le haram (`ep18_halal_haram.json`) : VALIDÉ AVEC CORRECTIONS

### Citations vérifiées
| Citation | Résultat | Source |
|---|---|---|
| **Muslim 1599** (an-Nu'man ibn Bashir) | Lu : « إِنَّ الْحَلاَلَ بَيِّنٌ وَإِنَّ الْحَرَامَ بَيِّنٌ وَبَيْنَهُمَا مُشْتَبِهَاتٌ ». **Identique** au texte affiché (« الْحَلَالَ » / « الْحَلاَلَ » : même mot, graphie courante ; la virgule est une ponctuation ajoutée). Coupe propre (la suite « لاَ يَعْلَمُهُنَّ كَثِيرٌ مِنَ النَّاسِ » est omise). Muslim 1599a, livre 22, n° 133. | https://sunnah.com/muslim:1599a |
| **al-Bukhari 52** (même Compagnon) | Lu : « الْحَلاَلُ بَيِّنٌ وَالْحَرَامُ بَيِّنٌ، وَبَيْنَهُمَا مُشَبَّهَاتٌ » : **sans « إِنَّ »** et avec « مُشَبَّهَاتٌ ». Même hadith, mot à mot un peu différent. Le texte affiché est celui de **Muslim** : précisé dans `source` (18-2). Livre 2, n° 45. | https://sunnah.com/bukhari:52 |
| Traduction | « Le licite est clair, l'illicite est clair, et entre les deux il y a des choses douteuses. » : **fidèle**. | — |
| Coran **5:3** | Lu : « حُرِّمَتْ عَلَيْكُمُ الْمَيْتَةُ وَالدَّمُ وَلَحْمُ الْخِنزِيرِ وَمَا أُهِلَّ لِغَيْرِ اللَّهِ بِهِ… » puis l'étouffée, l'assommée, la bête morte d'une chute ou d'un coup de corne, celle entamée par un fauve « إِلَّا مَا ذَكَّيْتُمْ », et ce qui est immolé sur les pierres dressées. **Porc, sang, bête morte et mal abattue : conformes.** L'exception de la nécessité (« فَمَنِ اضْطُرَّ فِي مَخْمَصَةٍ ») est à la fin du verset (voir K18-2). | https://quran.com/5/3 |
| Coran **5:90** | Lu : « إِنَّمَا الْخَمْرُ وَالْمَيْسِرُ وَالْأَنْصَابُ وَالْأَزْلَامُ رِجْسٌ مِنْ عَمَلِ الشَّيْطَانِ فَاجْتَنِبُوهُ ». Fonde l'interdit de l'alcool (الْخَمْر). **« tout ce qui enivre » n'est pas dans le verset** : c'est le hadith de Muslim 2003, d'où la référence ajoutée (18-4). | https://quran.com/5/90 |
| **Muslim 2003** (Ibn 'Umar) | Lu : « كُلُّ مُسْكِرٍ خَمْرٌ وَكُلُّ مُسْكِرٍ حَرَامٌ ». Fonde « tout ce qui enivre ». Muslim 2003a, livre 36, n° 92. | https://sunnah.com/muslim:2003a |
| Coran **5:4** | Lu : « يَسْأَلُونَكَ مَاذَا أُحِلَّ لَهُمْ قُلْ أُحِلَّ لَكُمُ الطَّيِّبَاتُ ». Fonde « les bonnes choses sont permises » (étape 2, référence ajoutée, 18-3). | https://quran.com/5/4 |

Mots arabes : الْحَلَالُ وَالْحَرَامُ, حَلَالٌ وَحَرَامٌ, الْأَصْلُ الْإِبَاحَةُ (début de la maxime « الأصل في الأشياء الإباحة »), الْعِبَادَاتُ, الْمُحَرَّمَاتُ, الشُّبُهَاتُ (pluriel de شُبْهَة, le hadith dit « مُشْتَبِهَاتٌ » : même racine, terme courant) : corrects.

### Fiqh (formulé sans trancher)
- **Halal = permis, haram = interdit** : consensus. OK.
- **Base de la permission dans les choses courantes** : avis de la grande majorité des savants des quatre écoles, appuyé par 5:4 et 2:29 ; quelques savants ont formulé la règle autrement (abstention avant preuve). L'original le présentait comme une règle sans réserve : **« pour la majorité des savants »** ajouté à l'écran et à l'oral (18-3).
- **L'adoration suit ce qui est enseigné** : principe admis par toutes les écoles (on n'adore pas Allah par un acte sans fondement dans le Coran et la Sunna). L'original disait « on ne fait que ce qui a été enseigné », formule qui peut être lue comme une prise de position dans le débat sur l'innovation (définitions qui diffèrent entre écoles) ; remplacé par « on suit ce qui a été enseigné dans le Coran et la Sunna » (18-5), qui reste le point commun.
- **Interdits alimentaires** : porc, sang (répandu, 6:145, non relu en ligne), bête morte, bête non abattue selon les règles, alcool et tout enivrant : consensus. « selon les règles » ne détaille pas les conditions de l'abattage (formule, viande des gens du Livre…), qui varient selon les écoles : bien.
- **Le douteux** : le hadith dit que celui qui s'en garde préserve sa religion. S'en écarter est une prudence recommandée ; « on s'abstient » sonnait comme une obligation générale. Remplacé par **« mieux vaut s'écarter »**, plus fidèle (18-6). « demander à une personne de savoir » : OK (16:43, non relu).

### Corrections appliquées
| # | Scène / champ | Avant | Après | Pourquoi |
|---|---|---|---|---|
| 18-1 | Étape 4, `narration` | « Quatre : parmi les interdits clairs dans l'alimentation : le porc, l'alcool et tout ce qui enivre, le sang, et la bête morte ou qui n'a pas été abattue selon les règles. » | « Quatre : dans l'alimentation, Allah, exalté soit-Il, interdit clairement le porc, le sang, et la bête morte ou non abattue selon les règles. Et tout ce qui enivre est interdit. » | « Allah, exalté soit-Il » manquait dans l'épisode. Les interdits de 5:3 sont attribués à Allah ; l'enivrant (hadith) est dit à part. |
| 18-2 | Citation, `source` | « Rapporté par al-Bukhari (n° 52) et Muslim (n° 1599) » | « Rapporté par al-Bukhari (n° 52) et Muslim (n° 1599) ; texte de Muslim » | Le texte affiché (« إِنَّ… مُشْتَبِهَاتٌ ») est celui de Muslim ; al-Bukhari dit « الْحَلاَلُ بَيِّنٌ… مُشَبَّهَاتٌ ». |
| 18-3 | Étape 2, `text` + `narration` | « Pour la nourriture, les objets et les échanges, les bonnes choses sont permises ; les interdits sont précis. » | `text` : « Nourriture, objets, échanges : pour la majorité des savants, la base est la permission (Coran 5:4). » (99 car.) ; oral : « …la majorité des savants enseigne que la base est la permission. Les interdits sont précis. » | Règle formulée sans trancher, avec son appui coranique. |
| 18-4 | Étape 4, `text` | « Le porc, l'alcool et tout ce qui enivre, le sang, la bête morte ou mal abattue (Coran 5:3, 5:90). » | « Le porc, le sang, la bête morte ou mal abattue (Coran 5:3), et tout ce qui enivre (5:90 ; Muslim 2003). » (103 car.) | Chaque interdit sous sa vraie source : « tout ce qui enivre » vient du hadith, pas de 5:90. |
| 18-5 | Étape 3, `text` + `narration` | « …c'est l'inverse : on ne fait que ce qui a été enseigné. » | « …c'est l'inverse : on suit ce qui a été enseigné dans le Coran et la Sunna. » (92 car.) | Point commun des écoles, sans entrer dans le débat sur l'innovation. |
| 18-6 | Étape 5, `text` + `narration` | « Quand c'est douteux, on s'abstient et on demande… » | « Dans le doute, mieux vaut s'écarter et demander… » (103 car.) | Fidèle au hadith (préserver sa religion), sans en faire une obligation. |

### Points laissés à Karim (ép. 18)
- **K18-1.** Citation : nommer le narrateur à l'écran : « An-Nu'man ibn Bashir, qu'Allah l'agrée, rapporte que le Prophète ﷺ a dit : » (comme Anas à l'ép. 15). Non modifié.
- **K18-2.** L'exception de la nécessité (fin de 5:3 : celui qui est contraint par la faim, sans chercher le péché) est un point de consensus utile aux débutants. Non ajouté (budget de mots).
- **K18-3.** Le hook « Halal, ce n'est pas que la viande » : la viande n'est pas vraiment traitée (seulement « non abattue selon les règles »). Si Karim prévoit un épisode « viande halal », c'est là qu'il faudra dire « selon les écoles » pour les conditions de l'abattage et la viande des gens du Livre (5:5).
- **K18-4.** 200 mots (ponctuation comprise), limite exacte. Marge possible : retirer « clairement » (étape 4) ou « mais » (étape 3).


---

## Épisode 19 : Le bon comportement (`ep19_comportement.json`) : VALIDÉ AVEC CORRECTIONS

### Citations vérifiées
| Citation | Résultat | Source |
|---|---|---|
| **al-Bukhari 6035** ('Abdallah ibn 'Amr, par Masruq) | Lu (beta.sunnah.com) : « إِنَّ خِيَارَكُمْ أَحَاسِنُكُمْ أَخْلاَقًا ». **Identique** au texte affiché (« أَخْلَاقًا » / « أَخْلاَقًا » : graphie). Traduction fidèle. Livre 78, n° 65. (À ne pas confondre avec al-Bukhari 3559, « إِنَّ مِنْ خِيَارِكُمْ… », non relu.) | https://beta.sunnah.com/bukhari:6035 · https://sunnah.com/bukhari:6035 (sans arabe) |
| **Abu Dawud 4799** (Abu ad-Darda') | Lu : « مَا مِنْ شَيْءٍ أَثْقَلُ فِي الْمِيزَانِ مِنْ حُسْنِ الْخُلُقِ ». **Sahih (al-Albani).** Livre 43, n° 27. Cette version ne dit ni « du croyant » ni « le Jour de la Résurrection ». | https://sunnah.com/abudawud:4799 |
| **at-Tirmidhi 2002** (Abu ad-Darda') | Lu : « مَا شَيْءٌ أَثْقَلُ فِي مِيزَانِ الْمُؤْمِنِ يَوْمَ الْقِيَامَةِ مِنْ خُلُقٍ حَسَنٍ ». At-Tirmidhi : « **حَسَنٌ صَحِيحٌ** » ; Darussalam : sahih. Livre 27, n° 108. C'est cette version qui fonde « la balance du croyant » et le jour : **« le Jour de la Résurrection »** (يَوْمَ الْقِيَامَةِ) remplace « le Jour dernier » (19-1). sunnah.com en erreur. | https://beta.sunnah.com/tirmidhi:2002 |
| Coran **68:4** | Lu : « وَإِنَّكَ لَعَلَىٰ خُلُقٍ عَظِيمٍ ». Mot-titre « خُلُقٍ عَظِيمٍ » : exact (cas du verset, convention de la série). Traduction « Et tu es d'une moralité immense » : fidèle. La voix ne lit pas le verset (paraphrase). | https://quran.com/68/4 |

Mots arabes : حُسْنُ الْخُلُقِ, فِي الْمِيزَانِ (mot à mot d'Abu Dawud), الصِّدْقُ, الْإِحْسَانُ (ici au sens du bien fait aux autres, cf. « وَبِالْوَالِدَيْنِ إِحْسَانًا », non relu), بِلَا كَلَامٍ, أَبُو بَكْرٍ الصِّدِّيقُ (nominatif, الصِّدِّيقُ qualifie أَبُو) : corrects.

### Fond
- Vérité, promesses, ne pas médire, parents, voisin, sourire, pardon : points de consensus, présentés sans références : OK.
- « La plus belle façon de montrer l'islam, sans un mot » : conseil, pas une règle : OK.
- **Conclusion de la série** : « La série des bases se termine ici. Merci d'avoir appris avec nous ! » : correct, cohérent avec l'outro de l'ép. 18 (« le dernier épisode des bases »).
- **Annonce d'Abou Bakr as-Siddiq** : formule « qu'Allah l'agrée » présente ; arabe correct. Voir K19-2 pour la cohérence avec le pilote 'Umar.

### Corrections appliquées
| # | Scène / champ | Avant | Après | Pourquoi |
|---|---|---|---|---|
| 19-1 | Hook et étape 1, `narration` | « le Jour dernier » | « le Jour de la Résurrection » | Mot du hadith (« يَوْمَ الْقِيَامَةِ », at-Tirmidhi 2002). |
| 19-2 | Étape 1, `text` | « Rien ne pèse plus lourd dans la balance du croyant que le bon comportement (Abu Dawud, at-Tirmidhi). » | « Rien n'est plus lourd dans la balance du croyant que le bon comportement (Abu Dawud 4799, Tirmidhi 2002). » (105 car.) | Numéros exacts à l'écran (« at- » retiré et « pèse » → « est » pour rester sous 110). |
| 19-2b | Étape 1, `narration` | « …que le bon comportement. » | « …que le bon comportement. Rapporté par Abu Dawud et at-Tirmidhi. » | Source dite à l'oral, comme pour les autres hadiths. |
| 19-3 | Résumé, `narration` | « …le modèle du Prophète, la parole vraie… » | « …le modèle du Prophète, paix et salut sur lui, la parole vraie… » | Formule manquante. |
| 19-4 | Résumé, item 2 | « Le modèle » / « Notre modèle » | « Notre modèle » / « Une moralité immense » | Titre et sous-titre redisaient la même chose ; pas de ﷺ possible dans un item. |
| 19-5 | Étapes 3, 4, 5 et outro, `narration` | « concrètement, c'est… » ; « c'est aussi respecter… » ; « c'est aussi la plus belle… » ; « Avec cet épisode, la série des bases se termine. » | « c'est… » ; « c'est respecter… » ; « c'est la plus belle… » ; « La série des bases se termine ici. » | Compensation pour rester à 200 mots. Aucun changement de sens. |

### Points laissés à Karim (ép. 19)
- **K19-1.** Citation : nommer le narrateur : « 'Abdallah ibn 'Amr, qu'Allah les agrée, rapporte que le Prophète ﷺ a dit : » (« les » : lui et son père, usage courant). Non modifié.
- **K19-2.** L'outro annonce la série des Compagnons « en commençant par Abou Bakr as-Siddiq ». Or un pilote **'Umar al-Faruq** existe déjà (`episodes/comp1_umar_al_faruq.json`, relu le 22/11). Si ce pilote est (ou sera) publié avant, dire plutôt « avec Abou Bakr as-Siddiq » ou renuméroter. Aucun dossier de recherche Abou Bakr n'existe encore dans `docs/` : chaque récit devra être vérifié comme pour 'Umar. Non modifié (choix éditorial).
- **K19-3.** « les Compagnons du Prophète » : pas de « qu'Allah les agrée » après « Compagnons » (il est dit pour Abou Bakr juste après). Si Karim veut la formule aussi pour le groupe : +4 mots, il faut couper ailleurs.
- **K19-4.** 200 mots (ponctuation comprise), limite exacte. Marge possible : retirer « sans un mot » (étape 5, −3) ou « Tu devines ? » (hook, −3).


---

## Point commun aux 2 épisodes
- **G.** Non lus en ligne : la suite d'al-Bukhari 52 (lue en résumé anglais seulement), at-Tirmidhi 2002 sur sunnah.com (lu sur beta.sunnah.com). Références citées seulement dans ce rapport, non relues : Coran 2:29, 5:5, 6:145, 16:43, 17:23 (« إِحْسَانًا »), al-Bukhari 3559. Aucune n'est dans les scripts.


## Fichiers Azure (`tools/azure/make_textes.py`, `tools/azure/textes/`)
- `make_textes.py` : **deux clés ajoutées** dans un bloc « ép. 18 et 19 » : `("Abou Bakr as-Siddiq", "أَبُو بَكْرٍ الصِّدِّيق")` (outro ép. 19) et `("Sunna", "سُنَّة")` (sans article, car la narration dit « la Sunna »). Effet ailleurs : l'ép. 2 dit aussi « c'est la Sunna » (résumé) ; s'il passe un jour par `make_textes.py`, il donnera « la [ar:سُنَّة|Sunna] », sans article doublé. « zakat » et « hajj » **non balisés**, comme demandé. « halal » et « haram » non balisés (mots courants en français).
- Régénération : `python3 tools/azure/make_textes.py episodes/ep18_halal_haram.json episodes/ep19_comportement.json` donne 9 et 9 scènes.
- Relecture des `.txt` : balises fermées, aucun article doublé (« la [ar:سُنَّة|Sunna] », « par [ar:أَبُو دَاوُد|Abu Dawud] et [ar:التِّرْمِذِي|at-Tirmidhi] », « par [ar:أَبُو بَكْرٍ الصِّدِّيق|Abou Bakr as-Siddiq] »). Aucune balise sur une traduction de hadith ou de verset.
- `tools/check.py` non lancé (module `kokoro_onnx` absent).
