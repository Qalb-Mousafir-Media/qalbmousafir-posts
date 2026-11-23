# Relecture religieuse — « Les Compagnons », épisode 1 : 'Umar al-Faruq

Relecteur indépendant (hadith et sira), 22/11/2026.
Fichier relu : `episodes/comp1_umar_al_faruq.json`. Copie d'origine : `episodes/comp1_umar_al_faruq.orig.json`.
Texte Azure régénéré : `tools/azure/textes/comp1_umar_al_faruq.txt`. `make_textes.py` n'a **pas** été modifié, car aucun mot arabe de la narration n'a changé.

## Verdict

**Publiable après les 7 corrections ci-dessous** (déjà appliquées). Tous les faits racontés sont authentiques. Les références et les textes arabes affichés sont exacts. Aucune citation inventée, aucune attribution faible au Prophète ﷺ. Les corrections portent sur la précision des formules (« un homme », « Allah a choisi », « pour leur islam », le sous-titre) et sur le ton (« sa propre sœur », « récits célèbres »). Aucune erreur de fond n'a été trouvée.

Contrôles techniques après correction :
- JSON valide (`python3 -m json.tool`).
- `tts` = `narration` dans les 10 scènes.
- Narration : 210 mots (comptés sans la ponctuation isolée, même méthode que les notes, qui donnaient 207 avant correction). C'est la limite haute de la fourchette 170–210.
- Légendes : 90 caractères au plus (scène 3 : 85 ; scène 5 : 74 ; scène 8 : 90). Aucun champ `text` dans cet épisode.
- Texte Azure : balises correctes, pas d'article doublé (« le [ar:شَيْطَان|Shaytan] »). « qu'Allah » et « d'Allah » ne sont pas balisés, comme dans les épisodes précédents.

## Vérification des sources

| Point | Texte arabe vérifié | Référence | Jugement (savant, source) | Fidélité du script | URL |
|---|---|---|---|---|---|
| Invocation | « اللَّهُمَّ أَعِزَّ الإِسْلَامَ بِأَحَبِّ هَذَيْنِ الرَّجُلَيْنِ إِلَيْكَ بِأَبِي جَهْلٍ أَوْ بِعُمَرَ بْنِ الخَطَّابِ » + « قَالَ: وَكَانَ أَحَبَّهُمَا إِلَيْهِ عُمَرُ ». Le texte affiché à l'écran est identique (seul ajout : un deux-points avant « بِأَبِي »). | at-Tirmidhi 3681 (d'après Ibn 'Umar) ; Ahmad 5696, qui dit explicitement « فَكَانَ أَحَبُّهُمَا إِلَى اللهِ عُمَرَ بْنَ الْخَطَّابِ » | At-Tirmidhi : « هَذَا حَدِيثٌ حَسَنٌ صَحِيحٌ غَرِيبٌ مِنْ حَدِيثِ ابْنِ عُمَرَ ». Al-Albani : sahih (Sahih at-Tirmidhi 3681). Darussalam : hasan. Ibn Hajar : renforcé par ses témoins. Al-Hakim : sahih al-isnad, avec l'accord d'adh-Dhahabi (sur la variante d'Ibn 'Abbas, selon hadithprophet). Remarque : la chaîne d'at-Tirmidhi passe par Kharija ibn 'Abdallah (« صدوق له أوهام », Taqrib) : elle est hasan seule et sahih avec ses témoins. | Traduction fidèle. | https://beta.sunnah.com/tirmidhi:3681 ; https://surahquran.com/Hadith-41295.html ; https://surahquran.com/Hadith-47356.html ; https://islamtics.com/hadith/musnad-ahmad/5696/ ; https://hadithprophet.com/hadith-10027.html ; https://islamqa.info/ar/answers/327548 |
| Sa'id ibn Zayd attaché | « لَوْ رَأَيْتُنِي مُوثِقِي عُمَرُ عَلَى الإِسْلَامِ أَنَا وَأُخْتُهُ وَمَا أَسْلَمَ » | al-Bukhari 3867 (Manaqib al-Ansar, bab islam 'Umar) ; al-Bukhari 3862 : « وَإِنَّ عُمَرَ لَمُوثِقِي عَلَى الإِسْلَامِ قَبْلَ أَنْ يُسْلِمَ عُمَرُ » (sans la sœur) | Sahih (al-Bukhari). Ibn Hajar : « رَبَطَهُ بِسَبَبِ إِسْلَامِه إِهَانَةً لَهُ وَإِلْزَامًا بِالرُّجُوعِ عَنِ الإِسْلَام ». Il rejette la lecture d'al-Kirmani (« يُثَبِّتُنِي ») qu'il juge « بَعِيدٌ جِدًّا » à cause de « قبل أن يسلم عمر ». Il identifie la sœur : Fatima bint al-Khattab, épouse de Sa'id. | « attaché… à cause de leur islam » : fidèle. « beau-frère » : exact. | https://sunnah.com/bukhari:3867 ; https://hadithprophet.com/hadith-34531.html ; https://hadithprophet.com/hadith-34526.html |
| La foule, 'Abdallah enfant, al-'As | « لَمَّا أَسْلَمَ عُمَرُ اجْتَمَعَ النَّاسُ عِنْدَ دَارِهِ وَقَالُوا صَبَا عُمَرُ، وَأَنَا غُلَامٌ فَوْقَ ظَهْرِ بَيْتِي… فَقَالَ: قَدْ صَبَا عُمَرُ فَمَا ذَاكَ؟ فَأَنَا لَهُ جَارٌ… فَرَأَيْتُ النَّاسَ تَصَدَّعُوا عَنْهُ… قَالُوا: الْعَاصِ بْنُ وَائِلٍ » | al-Bukhari 3865 ; al-Bukhari 3864 (même scène vue de la maison : 'Umar « فِي الدَّارِ خَائِفًا » ; al-'As lui dit « لَا سَبِيلَ إِلَيْكَ » ; une grande foule venue pour lui rebrousse chemin) | Sahih (al-Bukhari). Ibn Hajar : Ibn 'Umar avait environ 5 ans ; al-'As ibn Wa'il as-Sahmi, de Quraych, est mort non musulman avant l'Hégire. | Fidèle. « Un notable » est justifié : il porte un manteau de brocart (« قَبَاءٌ مِنْ دِيبَاجٍ ») et il a assez de rang pour disperser la foule. Il n'est pas glorifié. Le script ne présente pas 'Umar comme « sans peur », ce qui respecte 3864. | https://hadithprophet.com/hadith-34529.html ; https://sunnah.com/bukhari:3865 ; https://sunnah.com/bukhari:3864 |
| Parole d'Ibn Mas'ud | « مَا زِلْنَا أَعِزَّةً مُنْذُ أَسْلَمَ عُمَرُ » | al-Bukhari 3684 (Fada'il as-Sahaba, Manaqib 'Umar) et 3863 (Manaqib al-Ansar, bab islam 'Umar), même texte | Sahih (al-Bukhari ; hadeethenc : sahih). Hadeethenc explique « أعزة » par « قويين ظاهرين ». | « Nous n'avons cessé d'être forts depuis que 'Umar est devenu musulman » : fidèle. | https://sunnah.com/bukhari:3684 ; https://hadithprophet.com/hadith-34527.html ; https://hadeethenc.com/ar/browse/hadith/66311 |
| Surnom al-Faruq | « الفَارُوق » | Surnom établi. Les rapports divergent sur qui l'a employé en premier : selon al-Zuhri (chez Ibn Sa'd et at-Tabari), ce sont les gens du Livre, « et nous n'avons pas entendu que le Prophète ﷺ l'ait dit ». Le récit « أنت الفاروق » attribué au Prophète ﷺ passe par al-Kalbi (matruk). | Attribution au Prophète ﷺ : très faible. Le script ne l'attribue **pas** au Prophète ﷺ (« On le surnommera al-Faruq ») : c'est conforme. | « celui qui sépare le vrai du faux » : sens reconnu du mot (فَرَقَ). | https://en.wikipedia.org/wiki/Al-Farooq_(title) (cite at-Tabari et Ibn Sa'd) ; https://en.tohed.com/threads/the-validity-of-the-title-“al-fārūq”-for-ʿumar-رضي-الله-عنه.2256/ |
| Outro (épisode suivant) | « مَا لَقِيَكَ الشَّيْطَانُ سَالِكًا فَجًّا قَطُّ إِلَّا سَلَكَ فَجًّا غَيْرَ فَجِّكَ » | al-Bukhari 3294 et 3683 ; Muslim 2396 | Sahih, muttafaq 'alayh | « فَجًّا غَيْرَ فَجِّكَ » : exact. | https://sunnah.com/bukhari:3683 ; https://sunnah.com/muslim:2396 |
| Récits de conversion | — | Version d'Anas (al-Qasim ibn 'Uthman) : adh-Dhahabi la qualifie de « منكرة جدا ». Akram Diya' al-'Umari : « فلم يثبت شيء من هذه القصص من طريق صحيحة ». | Faibles, coupés ou sans isnad. Islamqa note que toutes les versions s'accordent sur un point : il s'est converti après avoir entendu le Coran. | « Les récits détaillés n'ont pas de chaîne sûre » est exact. Le script ne dit pas que ces récits sont faux. | https://islamqa.info/ar/answers/327548 |
| Contexte mecquois | — | Avant l'islam de 'Umar, beaucoup de musulmans cachaient leur islam (islamqa 468983, qui cite al-Bukhari 3863 et 3864) | Établi | « peu nombreux, souvent cachés » : exact et mesuré. | https://islamqa.info/ar/answers/468983 |

## Corrections appliquées (avant → après, pourquoi)

1. **Scène 1, narration (doutes 1 et 2)**
   - Avant : « …a prié Allah de renforcer l'islam par un homme. Allah a choisi 'Umar, qu'Allah l'agrée. »
   - Après : « …a prié Allah de renforcer l'islam par l'un de deux hommes. Ce fut 'Umar, qu'Allah l'agrée. »
   - Pourquoi : l'invocation porte sur deux hommes nommés. « Par un homme » modifie son contenu, même si la scène 4 le rétablit ensuite. « Allah a choisi » est une lecture de commentateur, alors que le texte dit « le plus aimé des deux auprès de Lui était 'Umar ». « Ce fut 'Umar » est un fait certain : l'islam a été renforcé par lui (Ibn Mas'ud, al-Bukhari 3684). L'accroche garde son effet : « l'un de deux hommes… ce fut 'Umar ».
2. **Scène 1, sous-titre, et `title`**
   - Avant : « L'homme qui a rendu les musulmans forts »
   - Après : « L'homme par qui Allah a renforcé l'islam »
   - Pourquoi : la force (العزة) vient d'Allah. La nouvelle formule reprend les mots mêmes de l'invocation (« أَعِزَّ الإِسْلَامَ ») sans attribuer la force à un homme seul. Elle évite aussi d'attribuer à un homme seul toute la force des musulmans.
3. **Scène 3, narration**
   - Avant : « …et sa propre sœur, pour leur islam. »
   - Après : « …et sa sœur, à cause de leur islam. »
   - Pourquoi : « عَلَى الإِسْلَامِ » veut dire « à cause de l'islam ». « pour leur islam » est ambigu à l'oral : on peut l'entendre comme « pour les affermir dans l'islam », c'est-à-dire la lecture d'al-Kirmani, que rejette Ibn Hajar. « propre » n'ajoutait que du drame. Le nom de la sœur (Fatima, selon Ibn Hajar) n'est toujours pas dit, puisque le hadith ne le donne pas (doute 4).
4. **Scène 3, légende**
   - Avant : « Avant son islam, 'Umar attache son beau-frère et sa propre sœur (al-Bukhari 3867) »
   - Après : « Avant son islam, 'Umar attache son beau-frère et sa sœur, musulmans (al-Bukhari 3867) »
   - Pourquoi : même raison que la correction 3. La légende indique la cause en restant sous 90 caractères (85).
5. **Scène 5, narration et légende (doute 2)**
   - Avant : « Le plus aimé des deux, c'était 'Umar »
   - Après : « Le plus aimé des deux auprès d'Allah, c'était 'Umar » (légende : « « Le plus aimé des deux auprès d'Allah était 'Umar » : il devient musulman »)
   - Pourquoi : « إِلَيْهِ » renvoie à Allah. La version d'Ahmad 5696 le dit en toutes lettres (« إِلَى اللهِ »). Sans cette précision, on pouvait comprendre « le plus aimé du Prophète ».
6. **Scène 5, narration (point 3 : ton)**
   - Avant : « Les récits célèbres n'ont pas de chaîne sûre. »
   - Après : « Les récits détaillés n'ont pas de chaîne sûre. »
   - Pourquoi : c'est plus exact. Le fond, qu'il s'est converti après avoir entendu le Coran, fait l'accord de toutes les versions (islamqa 327548) ; seuls les détails sont faibles. C'est aussi moins provocant : la phrase ne s'en prend pas à « ce que tout le monde connaît » et ne dit pas « faux ».
7. **Scène 7, narration (budget de mots)**
   - Avant : « Et la foule se disperse. »
   - Après : « La foule se disperse. »
   - Pourquoi : le sens ne change pas, et cela ramène la narration à 210 mots.

Sources du JSON (`sources`) :
- Retiré : « isnad sahih selon Ahmad Shakir ». Ce jugement n'a pas pu être vérifié en ligne.
- Ajouté : « hasan selon Darussalam », « renforcé par ses témoins selon Ibn Hajar », la formule d'Ahmad 5696 et le nom de la sœur selon Ibn Hajar.
- Surnom al-Faruq : la mention de Fada'il as-Sahaba n° 74 est remplacée par la divergence sur qui a employé le surnom en premier. Le n° 74 n'était vérifié que sur un forum.

## Les 7 doutes de l'historien : décisions

1. **« un homme »** : corrigé en « l'un de deux hommes » (correction 1).
2. **« Allah a choisi »** : remplacé par « Ce fut 'Umar » et par « le plus aimé des deux auprès d'Allah » (corrections 1 et 5). Ce sont les formules les plus proches du texte. Islamqa 327548 dit qu'Allah a exaucé l'invocation en facilitant l'islam de 'Umar, mais il n'est plus nécessaire de l'affirmer à l'oral.
3. **« attaché »** : maintenu. C'est la lecture d'Ibn Hajar, vérifiée ; la cause est maintenant explicite.
4. **La sœur** : toujours non nommée. Ibn Hajar la nomme Fatima bint al-Khattab, ce qui a été vérifié, donc la nommer serait permis. Ce n'est pas nécessaire, et cela coûterait des mots.
5. **Scène 7 et la peur de 'Umar** : le choix de l'auteur est approuvé. 3864 dit bien « خَائِفًا », et le script ne le contredit pas.
6. **« qu'Allah l'agrée »** : dit une fois, à la première mention orale (scène 1). C'est conforme. رضي الله عنه apparaît à l'écran dans le hook. Ne pas l'ajouter à la scène 3 (avant son islam) est approuvé.
7. **Coran** : aucune récitation dans l'épisode. Conforme à 7:204.

## Formules et ton
- Le Prophète ﷺ : « paix et salut sur lui » aux deux mentions orales (scènes 1 et 4), et ﷺ à l'écran (scène 4, sources). Conforme.
- 'Umar : « qu'Allah l'agrée » à la première mention orale, رضي الله عنه à l'écran. Conforme.
- Aucune moquerie, aucune polémique, rien contre aucun groupe. Abu Jahl et al-'As ibn Wa'il sont nommés sans insulte, seulement parce que les textes les nomment.
- Pas de détail inventé : la foule n'est pas dessinée, 'Umar ne parle pas, il n'y a ni épée ni sourate Taha.

## Numéros « de mémoire, à confirmer » dans COMPAGNONS_UMAR_RECHERCHE.md
Tous vérifiés. Ils étaient tous **exacts**, et le fichier a été mis à jour :
- Muslim 2396 (le Shaytan change de chemin, Sa'd) : https://sunnah.com/muslim:2396
- Muslim 2394 (Jabir) et 2395 (Abu Hurayra), le palais : https://sunnah.com/muslim:2394 ; https://en.tohed.com/hadith/muslim/6200
- al-Bukhari 3700 (mort de 'Umar, choura, d'après 'Amr ibn Maymun) : https://en.tohed.com/hadith/bukhari/3700/
- al-Bukhari 1392 (permission demandée à 'A'isha pour l'enterrement) : https://sunnah.com/bukhari:1392
- al-Bukhari 3667-3668 ('A'isha) et 4454 (Ibn 'Abbas ; 'Umar tombe en entendant 3:144) : https://sunnah.com/bukhari:3667 ; https://en.tohed.com/hadith/bukhari/4454
- al-Bukhari 3689 et 3469 (Abu Hurayra), Muslim 2398 ('A'isha), al-muhaddath : https://sunnah.com/bukhari:3689 ; https://sunnah.com/bukhari:3469 ; https://sunnah.com/muslim:2398
- Également corrigé dans ce fichier : le jugement « isnad sahih selon Ahmad Shakir » est signalé comme non vérifié.

## Points laissés à la décision humaine (Karim)
1. **Sous-titre et titre** (correction 2) : on peut revenir à « L'homme qui a rendu les musulmans forts » si l'on préfère. C'est une paraphrase défendable d'Ibn Mas'ud, mais elle est moins juste théologiquement. Je recommande la nouvelle formule.
2. **Leçon de la scène 9** (« Toi aussi, ta sincérité peut rendre les autres plus forts ») : elle est correcte, mais elle ne découle pas directement des textes. Alternative plus liée au récit (même nombre de mots environ) : « Ne désespère de personne : le plus dur contre l'islam en est devenu la force. » Non appliquée.
3. **Nommer la sœur** (Fatima bint al-Khattab, selon Ibn Hajar) : c'est permis. Non fait, faute de place (210 mots).
4. **Budget de mots** : la narration est à 210 mots, la limite haute. Toute nouvelle phrase demandera d'en couper une autre.
5. **Non vérifié par moi** : le jugement d'Ahmad Shakir sur Musnad 5696, et le n° 74 de Fada'il as-Sahaba (vu seulement sur un forum). Ni l'un ni l'autre n'est utilisé à l'écran ni à l'oral.
6. **Pages inaccessibles pendant la relecture** : dorar.net (toutes les pages en erreur), islamweb.net (audio.islamweb, erreur), accès direct à sunnah.com par curl (bloqué par le proxy), beta.sunnah.com/bukhari:3700 et beta.sunnah.com/muslim:2395 (permission non accordée à temps). Les mêmes contenus ont été vérifiés sur sunnah.com (WebFetch), hadithprophet.com (Fath al-Bari), surahquran.com, islamtics.com et en.tohed.com.
7. Hors pilote, toujours à confirmer : le jugement précis d'al-Albani sur le récit de la femme et de la dot, et la chaîne du rapport sur la prière publique à la Kaaba (islamqa 468983 cite Fath al-Bari 7/48 sans juger la chaîne).
