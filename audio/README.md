# Nachids de fond

| Fichier | Durée | Usage | Remarque |
|---|---|---|---|
| `nasheed-60.mp3` | 1 min 46 | Sous la voix off (épisodes) | Le plus régulier, à privilégier |
| `nasheed-27.mp3` | 1 min 35 | Sous la voix off (épisodes) | Presque aucune percussion |
| `nasheed-37.mp3` | 1 min 32 | Plutôt vidéos sans voix | Beaucoup d'énergie dans la zone de la voix : mixer plus bas |
| `bineleyas-arabic-nasheed.mp3` | 4 min 21 | Vidéos de voyage sans voix, si validé à l'écoute | Rythme marqué, graves, volume qui monte : pas sous la voix off |

Source probable : Pixabay. Garder le certificat de licence de chaque son (utile en cas de réclamation Content ID sur YouTube).

## Mixage sous la voix off

Nachid à −8 dB, compression déclenchée par la voix (seuil 0,06, ratio 2, attaque 30 ms, relâche 500 ms), fondu d'entrée 1,5 s et de sortie 2,5 s, puis normalisation à −15 LUFS.
Résultat mesuré sur l'épisode 3 : nachid environ 18 dB sous la voix pendant qu'elle parle, il remonte pendant les silences.

```
ffmpeg -i video.mp4 -i audio/nasheed-60.mp3 -filter_complex "[0:a]aformat=sample_rates=44100:channel_layouts=stereo,asplit=2[v][key];[1:a]aresample=44100,aformat=channel_layouts=stereo,atrim=0:DUREE,asetpts=N/SR/TB,volume=-8dB,afade=t=in:d=1.5,afade=t=out:st=DUREE-2.5:d=2.5[m];[m][key]sidechaincompress=threshold=0.06:ratio=2:attack=30:release=500[md];[v][md]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-15:TP=-1.5:LRA=9,aresample=44100[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -movflags +faststart sortie.mp4
```
