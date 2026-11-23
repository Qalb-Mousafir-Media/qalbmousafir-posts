# Qalb Mousafir - comparaison de voix Azure sur 4 phrases (test-voix.txt)
# Lancer : powershell -ExecutionPolicy Bypass -File .\tester-voix.ps1
# Sortie : audio\test-voix\<config>\t1.mp3 ... t4.mp3

$ErrorActionPreference = "Stop"
$dossier = Split-Path -Parent $MyInvocation.MyCommand.Path
$vitesse = "-4%"
# fr = voix des phrases en francais ; ar = voix des mots arabes ("" = la meme voix, balise de langue ; "auto" = arabe ecrit tel quel, sans balise)
$configs = @(
  @{ nom = "A_vivienne_seule";        fr = "fr-FR-VivienneMultilingualNeural"; ar = "" },
  @{ nom = "B_vivienne_et_zariyah";   fr = "fr-FR-VivienneMultilingualNeural"; ar = "ar-SA-ZariyahNeural" },
  @{ nom = "C_remy_et_hamed";         fr = "fr-FR-RemyMultilingualNeural";     ar = "ar-SA-HamedNeural" },
  @{ nom = "D_henri_et_hamed";        fr = "fr-FR-HenriNeural";                ar = "ar-SA-HamedNeural" },
  @{ nom = "E_denise_et_zariyah";     fr = "fr-FR-DeniseNeural";               ar = "ar-SA-ZariyahNeural" },
  @{ nom = "F_vivienne_HD";           fr = "fr-FR-Vivienne:DragonHDLatestNeural"; ar = "auto" },
  @{ nom = "G_remy_HD";               fr = "fr-FR-Remy:DragonHDLatestNeural";     ar = "auto" }
)

$cle = $env:AZURE_SPEECH_KEY
if (-not $cle) { $cle = [Environment]::GetEnvironmentVariable("AZURE_SPEECH_KEY", "User") }
$region = $env:AZURE_SPEECH_REGION
if (-not $region) { $region = [Environment]::GetEnvironmentVariable("AZURE_SPEECH_REGION", "User") }
if (-not $region) { $region = "canadacentral" }
if (-not $cle) { Write-Host "Cle Azure introuvable." -ForegroundColor Red; Read-Host "Entree"; exit 1 }

$url = "https://$region.tts.speech.microsoft.com/cognitiveservices/v1"
$entetes = @{ "Ocp-Apim-Subscription-Key" = $cle; "X-Microsoft-OutputFormat" = "audio-24khz-96kbitrate-mono-mp3"; "User-Agent" = "qalbmousafir-voix" }
$motif = '\[ar:([^|\]]+)\|([^\]]+)\]'

function Ssml([string]$texte, $c) {
  $t = [Security.SecurityElement]::Escape($texte)
  $fr = $c.fr; $ar = $c.ar
  if ($ar -eq "auto") {
    $t = [regex]::Replace($t, $motif, '$1')
    return "<speak version=""1.0"" xmlns=""http://www.w3.org/2001/10/synthesis"" xml:lang=""fr-FR""><voice name=""$fr"">$t</voice></speak>"
  }
  $corps = ""; $pos = 0
  foreach ($m in [regex]::Matches($t, $motif)) {
    $avant = $t.Substring($pos, $m.Index - $pos)
    $mot = $m.Groups[1].Value
    if ($ar -eq "") {
      if ($avant.Trim()) { $corps += "<voice name=""$fr""><lang xml:lang=""fr-FR""><prosody rate=""$vitesse"">$avant</prosody></lang></voice>" }
      $corps += "<voice name=""$fr""><lang xml:lang=""ar-SA""><prosody rate=""$vitesse"">$mot</prosody></lang></voice>"
    } else {
      if ($avant.Trim()) { $corps += "<voice name=""$fr""><prosody rate=""$vitesse"">$avant</prosody></voice>" }
      $corps += "<voice name=""$ar""><prosody rate=""$vitesse"">$mot</prosody></voice>"
    }
    $pos = $m.Index + $m.Length
  }
  $reste = $t.Substring($pos)
  if ($reste.Trim()) { $corps += "<voice name=""$fr""><prosody rate=""$vitesse"">$reste</prosody></voice>" }
  return "<speak version=""1.0"" xmlns=""http://www.w3.org/2001/10/synthesis"" xml:lang=""fr-FR"">$corps</speak>"
}

$lignes = Get-Content -Path (Join-Path $dossier "test-voix.txt") -Encoding UTF8 | Where-Object { $_ -and -not $_.StartsWith("#") }
$erreurs = 0
foreach ($c in $configs) {
  $sortie = Join-Path $dossier ("audio\test-voix\" + $c.nom)
  New-Item -ItemType Directory -Force -Path $sortie | Out-Null
  Write-Host "== $($c.nom)" -ForegroundColor Cyan
  foreach ($ligne in $lignes) {
    $parts = $ligne.Split("|", 2); $id = $parts[0].Trim()
    $mp3 = Join-Path $sortie ($id + ".mp3")
    try {
      Invoke-WebRequest -Uri $url -Method Post -Headers $entetes -ContentType "application/ssml+xml; charset=utf-8" -Body ([Text.Encoding]::UTF8.GetBytes((Ssml $parts[1].Trim() $c))) -OutFile $mp3 -UseBasicParsing | Out-Null
      Write-Host "  $id ok" -ForegroundColor Green
    } catch { $erreurs++; Write-Host "  $id ERREUR : $($_.Exception.Message)" -ForegroundColor Red }
  }
}
Write-Host ""; Write-Host "Termine. Erreurs : $erreurs (une voix HD peut ne pas exister dans ta region : ce n'est pas grave)" -ForegroundColor Yellow
Read-Host "Appuie sur Entree pour fermer"
