# Relecture religieuse : épisodes 2, 3, 4 et 5 (Qalb Mousafir, « Les bases »)

Relecteur indépendant. Date : 21/11/2026.
Copies d'origine conservées : `ep2_woudou.orig.json`, `ep3_5_prieres.orig.json`, `ep4_6_piliers_foi.orig.json`, `ep5_priere_partie1.orig.json`.


## Synthèse

| Ép. | Verdict | Corrections | Voix avant → après (check.py) | Points pour Karim |
|---|---|---|---|---|
| 2 Woudou' | **Validé avec corrections** | 7 | 61,5 s → **63,8 s** | 2 |
| 3 5 prières | **Validé avec corrections** | 3 | 54,4 s → **56,1 s** | 1 |
| 4 6 piliers de la foi | **Validé avec corrections** | 2 | 62,8 s → **65,9 s** | 1 |
| 5 Prière, partie 1 | **Validé avec corrections** | 3 | 66,0 s → **71,2 s** | 3 |

Contrôles passés sur les 4 fichiers :
- `python3 -m json.tool` OK ;
- tous les `text` font 110 caractères ou moins (max : 106 / 80 / 99 / 101) ;
- `check.py` ne signale aucun « (en) » ;
- voix entre 50 et 75 s ;
- ﷺ présent à l'écran et « paix et salut sur lui » à l'oral à chaque mention du Prophète ﷺ ;
- aucun contenu polémique.

Les fichiers ont été réécrits avec `json.dump(indent=1)`. Le contenu et le schéma n'ont pas changé, seule la mise en page des fichiers change.

Vérification demandée par le directeur (« Parádis », ép. 2 étape 8) : aucun des 8 fichiers (versions actuelles et `.orig`) ne contient « Parádis ». Le mot est écrit « Paradis » en ASCII simple (octets vérifiés), donc rien à corriger. Aucun champ affiché ne contient une graphie phonétique des `tts` : j'ai cherché Bissmilâh, Soûnna, Mouhammad, Fadjr, Marib, Ichâ, Djibril, rak'ates, Roukou, Soudjoude, Tachahhoude, Allahou, Takbirate, dau, Assalamou, Mouslim, Boukhari, etc.

Sites de référence : **sunnah.com et dorar.net sont bloqués** par le proxy de cette session (HTTP 403). Les textes ont donc été vérifiés sur **hadeethenc.com** et **islamweb.net** (Sahih al-Bukhari, Sahih Muslim et Sharh an-Nawawi en ligne). Un seul numéro (Bukhari 631) a été confirmé sur un site secondaire, voir plus bas.
Note sur la vocalisation : les sites écrivent parfois « لاَ / الصَّلاَةُ » (fatha après le lam-alif) ou omettent le soukoun de l'article (« العَمَلِ »). Les scripts utilisent la vocalisation complète moderne (« لَا », « الْ »). C'est le même texte, aucun écart réel.

---

## Épisode 2 : Comment faire les ablutions (`ep2_woudou.json`) : VALIDÉ AVEC CORRECTIONS

### Citations vérifiées
| Citation | Résultat | Source vérifiée |
|---|---|---|
| مَنْ تَوَضَّأَ فَأَحْسَنَ الْوُضُوءَ خَرَجَتْ خَطَايَاهُ مِنْ جَسَدِهِ حَتَّى تَخْرُجَ مِنْ تَحْتِ أَظْفَارِهِ (Muslim 245, 'Uthman) | **Identique mot pour mot et voyelle par voyelle.** Numéro 245 confirmé. Traduction fidèle. | https://hadeethenc.com/ar/browse/hadith/6263 |
| Invocation finale, 1re chaîne (Muslim 234, 'Uqba ibn 'Amir) : « …يَتَوَضَّأُ فَيُبْلِغُ - أَوْ فَيُسْبِغُ - الْوَضُوءَ ثُمَّ يَقُولُ: أَشْهَدُ أَنْ لَا إِلَهَ إِلَّا اللهُ وَأَنَّ مُحَمَّدًا عَبْدُ اللهِ وَرَسُولُهُ إِلَّا فُتِحَتْ لَهُ أَبْوَابُ الْجَنَّةِ الثَّمَانِيَةُ يَدْخُلُ مِنْ أَيِّهَا شَاءَ » | Confirmé, n° 234. | https://hadeethenc.com/ar/browse/hadith/8388 |
| Formule dite à l'oral (2e chaîne de Muslim 234) : « مَنْ تَوَضَّأَ فَقَالَ أَشْهَدُ أَنْ لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ وَأَشْهَدُ أَنَّ مُحَمَّدًا عَبْدُهُ وَرَسُولُهُ » (« فَذَكَرَ مِثْلَهُ ») | **Confirmé** dans Sahih Muslim, sous le même n° 234. La translittération orale correspond. | https://www.islamweb.net/ar/library/content/1/416/ (Sahih Muslim, باب الذكر المستحب عقب الوضوء) |
| Déroulé : Bukhari 159 ('Uthman) | Confirmé. Bouche et nez **sans nombre** ; tête « ثُمَّ مَسَحَ بِرَأْسِهِ » **sans nombre** ; pas d'oreilles ; pas de bismillah ; pas d'ordre droite puis gauche. islamweb numérote ce hadith **158** (ancienne numérotation) : c'est le 159 de Fath al-Bari et sunnah.com. | https://www.islamweb.net/ar/library/content/0/160/ (Sahih al-Bukhari, باب الوضوء ثلاثا ثلاثا) |
| Déroulé : Muslim 226 ('Uthman) | Confirmé, n° 226. Droite puis gauche pour les bras (« إِلَى الْمِرْفَقِ ») et les pieds (« إِلَى الْكَعْبَيْنِ »). Bouche et nez sans nombre, tête sans nombre, pas d'oreilles, pas de bismillah. | https://www.islamweb.net/ar/library/content/1/402/ (Sahih Muslim, باب صفة الوضوء وكماله) |
| Version Bukhari 164 ('Uthman, autre chaîne) | Même constat : « تَمَضْمَضَ وَاسْتَنْشَقَ وَاسْتَنْثَرَ » sans nombre. | https://hadeethenc.com/ar/browse/hadith/3313 |
| Bouche et nez « 3 » : hadith de 'Abdallah ibn Zayd | **Confirmé : al-Bukhari 186 (muttafaq 'alayh, = Muslim 235)** : « فَمَضْمَضَ وَاسْتَنْشَقَ وَاسْتَنْثَرَ، ثَلاَثَ غَرَفَاتٍ » (trois poignées). Le même hadith dit pour la tête « فَأَقْبَلَ بِهِمَا وَأَدْبَرَ مَرَّةً وَاحِدَةً ». | https://hadeethenc.com/ar/browse/hadith/3444 |

Mots arabes isolés (الْوُضُوءُ, النِّيَّةُ, الْكَفَّانِ, الْفَمُ وَالْأَنْفُ, الْوَجْهُ, الْيَدَانِ, مَسْحُ الرَّأْسِ, الرَّأْسُ, الرِّجْلَانِ, الذِّكْرُ, الصَّلَوَاتُ الْخَمْسُ) : vocalisation correcte.

**Référence affichée ou dite pour les étapes :** aucune scène n'affiche ni ne dit « Bukhari 159 / Muslim 226 ». La seule source à l'écran pendant les étapes est « Muslim, n° 234 », à l'étape 8, et elle concerne bien l'invocation. Le hadith de la scène 2 (Muslim 245) porte sur le mérite des ablutions, pas sur leur déroulé. Rien ne laisse donc croire que la bismillah, les oreilles ou le « 3 fois » pour bouche et nez viennent du hadith de 'Uthman. Pas de correction nécessaire sur ce point.

### Corrections appliquées
| # | Scène / champ | Avant | Après | Pourquoi |
|---|---|---|---|---|
| 1 | Hook, `narration` + `tts` | « …effaçait tes péchés ? » | « …effaçait tes **petits** péchés ? » | Doute n° 9. La plupart des savants comprennent ces hadiths d'expiation comme visant les péchés mineurs ; les grands péchés demandent le repentir. C'est l'explication donnée par hadeethenc pour ce hadith : « كفارة للذنوب الصغائر، أما الكبائر فلا بد من التوبة ». La traduction du hadith reste littérale (« ses péchés »), sans rien ajouter au texte prophétique. |
| 2 | Étape 5 (bras), `subtitle` | « Jusqu'aux coudes · 3 fois » | « Coudes compris · 3 fois » | Doute n° 5. Les quatre écoles incluent les coudes. En français, « jusqu'au coude » peut se comprendre en excluant le coude. |
| 3 | Étape 5, `text` / `narration` / `tts` | « Lave le bras droit jusqu'au coude, trois fois… » / « le bras droit, jusqu'au coude, trois fois » | « Lave le bras droit, coude compris, trois fois… » / « le bras droit, coude compris, trois fois » | Même raison. |
| 4 | Étape 6 (tête), `subtitle` / `text` / `narration` / `tts` | « Essuyer · 1 fois » ; « …sur ta tête, une fois. Puis essuie tes oreilles. » | « Essuyer, sans laver » ; « …sur ta tête. Puis essuie tes oreilles. » | Doute n° 3. Le nombre ne figure ni dans Bukhari 159 ni dans Muslim 226. Les chafiites recommandent trois passages. Placé à côté des « 3 fois » des autres étapes, « 1 fois » laissait croire que c'est la seule Sunna. La surface à essuyer (toute la tête ou une partie) diverge aussi : le texte reste neutre. |
| 5 | Résumé, item 6 « Tête et oreilles », `subtitle` | « 1 fois » | « Essuyer » | Même raison. |
| 6 | Étape 7 (pieds), `subtitle` / `text` / `narration` / `tts` | « Jusqu'aux chevilles · 3 fois » ; « …le pied droit jusqu'aux chevilles… » | « Chevilles comprises · 3 fois » ; « …le pied droit, chevilles comprises… » | Doute n° 5 : les chevilles sont incluses dans les quatre écoles. |
| 7 | Étape 8, `text` | « Récite l'attestation de foi : les 8 portes du Paradis s'ouvrent pour toi (Muslim, n° 234). » | « Après un woudou' bien fait, dis l'attestation de foi : les 8 portes du Paradis s'ouvrent (Muslim, n° 234). » | Doute n° 10. Le hadith pose la condition « فَيُبْلِغُ أَوْ فَيُسْبِغُ الْوُضُوءَ » (ablutions faites complètement). Le texte garde 106 caractères. |
| 7b | Étape 8, `narration` / `tts` | « Huit : à la fin, dis : … » | « Huit : après un woudou' bien fait, dis : … » (`tts` : « woudou ») | Même condition, à l'oral. La formule elle-même ne change pas (2e chaîne de Muslim 234, vérifiée). |
| 8 | Résumé, `narration` / `tts` | « laver une fois suffit, trois fois, c'est la Sunna » | « laver chaque partie une fois, en entier, suffit ; trois fois, c'est la Sunna » | Doute n° 7. **Conclusion : consensus.** Le minimum obligatoire est un lavage qui couvre entièrement chaque partie, et trois lavages sont la Sunna. An-Nawawi rapporte l'accord des savants là-dessus dans son commentaire de Muslim. J'ai ajouté « en entier » : un lavage partiel ne suffit pas, c'est ce qui compte pour un débutant. Le mot « laver » exclut l'essuyage de la tête, ce qui évite de contredire la correction n° 4. |

### Conclusions sur les doutes de NOTES.md (ép. 2)
1. **Bismillah** : à garder telle quelle (« Puis dis : Bismillah », sans statut). Elle est au minimum recommandée dans les quatre écoles et obligatoire chez les hanbalites. Aucune référence n'est affichée. OK.
2. **Bouche et nez « 3 fois »** : confirmé par le hadith de 'Abdallah ibn Zayd, **al-Bukhari 186 / Muslim 235**, et non par Bukhari 159 / Muslim 226. Aucune référence trompeuse n'est affichée. Pas de statut donné, alors que ce point diverge (obligatoire chez les hanbalites, Sunna ailleurs). OK.
3. **Tête** : nombre retiré (corrections 4 et 5).
4. **Oreilles** : absentes des hadiths de 'Uthman (vérifié). Elles viennent d'autres hadiths authentifiés des recueils de Sunan (notamment Ibn 'Abbas chez an-Nasa'i et at-Tirmidhi). Je n'ai pas pu vérifier ces hadiths sur les 4 sites de référence, dorar.net et sunnah.com étant bloqués. Comme aucune référence n'est affichée et qu'aucun statut n'est donné, je n'ai rien corrigé.
5. **Coudes et chevilles** : « compris / comprises » ajouté (corrections 2, 3 et 6).
6. **Intention dans le cœur** : formulation neutre (son statut diverge : Sunna chez les hanafites). OK.
7. **Une fois / trois fois** : consensus, formulation précisée (correction 8).
8. **Ordre** : bien retiré du résumé. Les étapes sont numérotées dans l'ordre du hadith, sans dire que cet ordre est obligatoire. OK.
9. **Péchés / petits péchés** : nuancé dans l'accroche (correction 1).
10. **Huit portes** : condition rétablie (corrections 7 et 7b).
11. **« الذِّكْرُ »** pour l'étape 8 : correct et acceptable.
12. **« Muhammadan » dans la formule, sans « paix et salut sur lui »** : je n'ai pas modifié. C'est une formule de dhikr citée telle que le hadith la donne, et l'interrompre altérerait le texte prophétique. Voir le point humain A.

### Points qui restent à la décision humaine (ép. 2)
- **A.** Formule de l'étape 8 : je recommande de la laisser intacte, sans « paix et salut sur lui » au milieu. Si Karim veut appliquer la règle à la lettre, il faut l'ajouter *après* la formule complète (« …wa rassoulouh. Paix et salut sur lui. »), jamais à l'intérieur. Cela ajoute environ 1,5 s.
- **B.** « petits péchés » dans l'accroche : c'est l'avis très majoritaire. Si Karim préfère coller au texte du hadith, l'alternative est « Et si l'eau des ablutions faisait sortir tes fautes ? ».

---

## Épisode 3 : Les 5 prières du jour (`ep3_5_prieres.json`) : VALIDÉ AVEC CORRECTIONS

### Citation vérifiée
| Citation | Résultat | Source vérifiée |
|---|---|---|
| Question « أَيُّ الْعَمَلِ أَحَبُّ إِلَى اللَّهِ » et réponse « الصَّلَاةُ عَلَى وَقْتِهَا » (Ibn Mas'oud) | **Confirmé, al-Bukhari 527** (muttafaq 'alayh ; Muslim 85 aussi). Mêmes lettres et mêmes voyelles, aux conventions d'écriture près (voir plus haut). Traduction « La prière accomplie à son heure » fidèle. Citer seulement al-Bukhari est correct. | https://hadeethenc.com/ar/browse/hadith/3365 |

Mots arabes (الْفَجْرُ, الظُّهْرُ, الْعَصْرُ, الْمَغْرِبُ, الْعِشَاءُ, الصَّلَوَاتُ الْخَمْسُ, أَرْكَانُ الْإِيمَانِ) : vocalisation correcte.

### Corrections appliquées
| # | Scène / champ | Avant | Après | Pourquoi |
|---|---|---|---|---|
| 1 | Prière 2, `title` + `narration` ; résumé item 2 `title` | « Dhohr » / « le Dhohr » | « Dhuhr » / « le Dhuhr » | Alignement sur l'épisode 1 (« Fajr, Dhuhr, Asr, Maghrib, Isha »). Le `tts` « Dhohr » n'a pas changé. |
| 2 | Prière 5, `title` + `narration` ; résumé item 5 `title` | « Icha » / « l'Icha » | « Isha » / « l'Isha » | Même raison. Le `tts` « Ichâ » n'a pas changé. |
| 3 | Résumé, `narration` / `tts` | « Dix-sept rak'at obligatoires par jour. » | « Dix-sept rak'at obligatoires par jour, quand tu n'es pas en voyage. » (`tts` : « rak'ates ») | Doute n° 4. Le chiffre 17 ne vaut que pour le résident. Le statut du raccourcissement en voyage diverge (obligatoire chez les hanafites, permis ou Sunna ailleurs) : la formule le signale sans trancher, ce qui compte pour une chaîne sur le voyage. |

### Conclusions sur les doutes (ép. 3)
1. **Asr** (« plus tard dans l'après-midi, quand les ombres s'allongent ») : ne tranche pas entre ombre ×1 et ombre ×2. OK.
2. **Isha** (« quand la lueur du crépuscule a disparu ») : couvre le crépuscule rouge (majorité) et le blanc (Abu Hanifa). Ne pas parler de la fin du temps est le bon choix. OK.
3. **Fajr** (« de l'aube jusqu'au lever du soleil ») : consensus. OK.
4. **17 rak'at** : corrigé (correction 3).
5. **Witr** non mentionné : bon choix, car son statut diverge.
6. **Translittérations** : alignées sur l'épisode 1 (corrections 1 et 2). Les `tts` n'ont pas changé.

### Point à la décision humaine (ép. 3)
- **C.** Les calendriers de prière proposent deux réglages pour l'Asr (« standard » ou « hanafite »). Karim peut ajouter dans la légende : « choisis le réglage de ton école ou de ta mosquée ». Je ne l'ai pas mis dans la voix.

---

## Épisode 4 : Les 6 piliers de la foi (`ep4_6_piliers_foi.json`) : VALIDÉ AVEC CORRECTIONS

### Citation vérifiée
| Citation | Résultat | Source vérifiée |
|---|---|---|
| « أَنْ تُؤْمِنَ بِاللَّهِ وَمَلَائِكَتِهِ وَكُتُبِهِ وَرُسُلِهِ وَالْيَوْمِ الْآخِرِ وَتُؤْمِنَ بِالْقَدَرِ خَيْرِهِ وَشَرِّهِ » (hadith de Jibril, 'Umar) | **Identique, Muslim n° 8.** Le hadith commence par « طَلَعَ عَلَيْنَا رَجُلٌ شَدِيدُ بَيَاضِ الثِّيَابِ » et se termine par « فَإِنَّهُ جِبْرِيلُ أَتَاكُمْ يُعَلِّمُكُمْ دِينَكُمْ » (vérifié). Traduction fidèle. | https://www.islamweb.net/ar/library/content/1/80/ (Sahih Muslim, باب بيان الإيمان والإسلام والإحسان) |

Anges créés de lumière (Muslim 2996), Coran 15:9 et 33:40 : ces références ne sont pas citées à l'écran et sont correctes sur le fond. Mots arabes (اللَّهُ, الْمَلَائِكَةُ, الْكُتُبُ, الرُّسُلُ, الْيَوْمُ الْآخِرُ, الْقَدَرُ, صِفَةُ الصَّلَاةِ) : vocalisation correcte.

### Corrections appliquées
| # | Scène / champ | Avant | Après | Pourquoi |
|---|---|---|---|---|
| 1 | Citation, `intro` / `narration` / `tts` | « Jibril a demandé : … » / « L'ange Jibril a demandé au Prophète… » | « Jibril, venu sous l'apparence d'un homme, a demandé : … » / « L'ange Jibril, venu sous l'apparence d'un homme, a demandé au Prophète… » | Doute n° 4. Dans le hadith, un homme est venu, et le Prophète ﷺ dit à la fin que c'était Jibril. La nouvelle formule suit le texte (« رَجُلٌ » puis « فَإِنَّهُ جِبْرِيلُ »). Cela ajoute environ 1,5 s. |
| 2 | Pilier 3 (livres), `text` / `narration` / `tts` | « La Torah, les Psaumes, l'Évangile… et le Coran, le dernier, préservé par Allah. » | `text` : « Tels qu'Allah les a révélés : la Torah, les Psaumes, l'Évangile… et le Coran, le dernier, préservé. » (99 caractères) · voix : « Trois : Ses livres, tels qu'Allah les a révélés. La Torah… » | Doute n° 1. On croit aux livres sous leur forme révélée. La tournure est positive et ne critique personne, ce qui évite la polémique, alors que « dans leur forme d'origine » appelle une comparaison. |

### Conclusions sur les doutes (ép. 4)
1. **Livres** : corrigé (correction 2). Les feuillets d'Ibrahim restent sous-entendus par « … ». OK.
2. **Destin** (« Rien n'arrive sans qu'Allah le sache et le veuille, le bien comme le mal ») : exact et accepté par toutes les écoles de croyance sunnites. C'est une simplification acceptable (deux des quatre degrés). Pas de correction.
3. **Messagers** : « paix sur eux » à l'oral, ﷺ seulement pour Muhammad ﷺ, et Adam couvert par « … ». OK.
4. **Jibril** : corrigé (correction 1).
5. **Citation de 16,3 s** : acceptable. Le total reste à 65,9 s.

### Point à la décision humaine (ép. 4)
- **D.** Le `next_title` de l'outro est « Comment faire la prière (partie 1) », alors que l'ép. 5 a pour titre « Comment faire la prière — partie 1 ». C'est un alignement purement typographique : je ne l'ai pas fait, à confirmer.

---

## Épisode 5 : Comment faire la prière, partie 1 (`ep5_priere_partie1.json`) : VALIDÉ AVEC CORRECTIONS

Consigne de Karim appliquée : uniquement les points communs aux quatre écoles, et la vidéo précise qu'elle décrit la prière faite seul. Le `tts` « le dau droit » est conservé, comme demandé.

### Citations vérifiées
| Citation | Résultat | Source vérifiée |
|---|---|---|
| « صَلُّوا كَمَا رَأَيْتُمُونِي أُصَلِّي » (Malik ibn al-Huwayrith) | Texte confirmé : « وَصَلُّوا كَمَا رَأَيتُمُونِي أُصَلِّي » (le site omet le soukoun du ي ; le script vocalise entièrement, c'est correct). Retirer le « وَ » de liaison est acceptable. Traduction fidèle. Le **n° 631** d'al-Bukhari est confirmé sur un site secondaire, sunnah.com étant bloqué. | Texte : https://hadeethenc.com/ar/browse/hadith/3059 · numéro : https://en.tohed.com/hadith/bukhari/631/ |
| Structure : hadith de celui qui priait mal | **Confirmé, al-Bukhari 757** (muttafaq 'alayh) : « فَكَبِّرْ… ثُمَّ اقْرَأْ… ثُمَّ ارْكَعْ حَتَّى تَطْمَئِنَّ رَاكِعًا، ثُمَّ ارْفَعْ حَتَّى تَعْدِلَ قَائِمًا، ثُمَّ اسْجُدْ حَتَّى تَطْمَئِنَّ سَاجِدًا، ثُمَّ ارْفَعْ حَتَّى تَطْمَئِنَّ جَالِسًا ». Ce hadith appuie « reste un instant immobile » et « calmement ». Il n'est pas affiché. | https://hadeethenc.com/ar/browse/hadith/3185 |

Mots arabes (صِفَةُ الصَّلَاةِ, الطَّهَارَةُ, النِّيَّةُ, تَكْبِيرَةُ الْإِحْرَامِ, التَّكْبِيرُ, الْقِيَامُ, الرُّكُوعُ, الِاعْتِدَالُ, السُّجُودُ, التَّسْلِيمُ) : vocalisation correcte.

### Corrections appliquées
| # | Scène / champ | Avant | Après | Pourquoi |
|---|---|---|---|---|
| 1 | Hook, `subtitle` / `narration` / `tts` | « Partie 1 : les étapes d'une rak'a » ; « Voici les étapes d'une rak'a. » | « Partie 1 : une rak'a, quand tu pries seul » ; « Voici les étapes d'une rak'a, quand tu pries seul. » | Doute n° 1 et consigne de Karim : on cadre toute la vidéo comme la description de la prière faite seul, sans entrer dans la divergence sur al-Fatiha derrière l'imam. |
| 2 | Étape 4 (Qiyam), `text` / `narration` / `tts` | « Debout, récite la sourate al-Fatiha. » | `text` : « Debout. Quand tu pries seul, récite la sourate al-Fatiha. » · voix : « Quatre : debout, et quand tu pries seul, récite la sourate al-Fatiha. » | Même consigne, rappelée à l'endroit exact de la divergence. La condition ne porte que sur la récitation : « debout » reste valable pour tout le monde. On ne dit pas ce qui change derrière un imam. |
| 3 | Outro, `narration` / `tts` | « Prochain épisode : comment faire la prière, partie deux. » | « Prochain épisode, partie deux : la sourate après al-Fatiha, et les prières de trois et quatre rak'at. » (`tts` : « rak'ates ») | Sans cette annonce, un débutant pourrait croire que la prière s'arrête à ces gestes. Or les quatre écoles font une sourate après al-Fatiha dans les deux premières rak'at (wajib chez les hanafites, Sunna ailleurs) et le tashahhud du milieu dans les prières de 3 et 4 rak'at. Le statut n'est pas donné. Voir le point humain E. |

### Conclusions sur les doutes de NOTES_ep5.md
1. **Al-Fatiha derrière un imam** : traité selon la consigne (corrections 1 et 2).
2. **« Dos droit » / « front au sol »** : OK. Le dos droit fait partie de la forme parfaite du rukû' dans toutes les écoles, et le front est commun à toutes. Le nez et les 7 membres sont omis à juste titre.
3. **« Reste un instant immobile » / « calmement »** : appuyés par Bukhari 757, sans statut (pilier pour la majorité, wajib chez les hanafites). OK.
4. **Préciser quelle prière on fait** : c'est commun aux quatre écoles pour les prières obligatoires. OK.
5. **Taslim** : « As-salamu 'alaykum » est présent dans toutes les écoles et aucun statut n'est donné. OK.
6. **Takbir de transition** : son absence est acceptable pour la partie 1. À traiter en partie 2.
7. **Étape 1 (conditions)** : ce qui est dit est juste (pureté, qibla). La 'awra couverte et l'entrée du temps manquent. Voir le point humain F.
8. **Titre et étape 8** : c'est signalé à l'écran (« À la fin de la prière »). OK.
- « Reprends à l'étape quatre » pour la rak'a suivante : c'est exact (pas de nouvelle intention ni de takbirat al-ihram). L'annonce de l'outro (correction 3) couvre le cas du tashahhud du milieu.

### Points qui restent à la décision humaine (ép. 5)
- **E.** L'outro annonce désormais le contenu de la partie 2 (sourate après al-Fatiha, prières de 3 et 4 rak'at). Le scénariste doit s'y tenir. Sinon, revenir à l'outro d'origine et ajouter cette mention ailleurs.
- **F.** Étape 1 : ajouter « vêtu(e) correctement » ou « couvert(e) » (la 'awra, condition admise par toutes les écoles), ou le traiter en partie 2. Je n'y ai pas touché pour garder le texte à 101 caractères.
- **G.** Montage : 71,2 s de voix. Avec la durée minimale de 6,3 s par étape dans `build()`, la vidéo dépassera nettement 75 s. Il faut réduire cette durée minimale, comme le notait déjà le scénariste.

---

## Remarques communes pour le monteur (hors religion, rappel de check.py)
- Arabe trop large : citation de l'ép. 2 (2920 px à 108 px), citation de l'ép. 4 (2675 px), « الْفَمُ وَالْأَنْفُ » de l'ép. 2 (1042 px à 220 px), « تَكْبِيرَةُ الْإِحْرَامِ » de l'ép. 5 (1180 px à 220 px). Il faut un retour à la ligne ou une taille plus petite.
- `progress()` doit gérer 5, 6 et 8 points.

## Durées après correction (check.py, ff_siwis, speed 0.97)
- Ép. 2 : **63,77 s** (hook 4,99 · étape 5 4,10 · étape 6 3,54 · étape 7 3,48 · étape 8 10,94 · résumé 10,09)
- Ép. 3 : **56,06 s** (résumé 11,93)
- Ép. 4 : **65,88 s** (citation 16,32 · pilier 3 7,13)
- Ép. 5 : **71,19 s** (hook 5,48 · étape 4 3,75 · outro 7,70)
