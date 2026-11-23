# Qalb Mousafir - generation de la voix off avec Azure Speech (francais + mots arabes)
# Lancer : powershell -ExecutionPolicy Bypass -File .\generer-voix.ps1
# La cle est lue dans la variable Windows AZURE_SPEECH_KEY (jamais ecrite dans un fichier).
# Textes : textes\*.txt (une ligne par scene : numero|texte). [ar:ARABE|francais] = mot arabe.
# Sortie : audio\<voix>-<mode>\<episode>\<numero>.mp3   (mode ar = mots arabes en arabe, mode fr = tout en francais)

$ErrorActionPreference = "Stop"
$dossier = Split-Path -Parent $MyInvocation.MyCommand.Path
$voixListe = @("fr-FR-VivienneMultilingualNeural")
$modes     = @("ar")
$vitesse   = "-4%"

$cle = $env:AZURE_SPEECH_KEY
if (-not $cle) { $cle = [Environment]::GetEnvironmentVariable("AZURE_SPEECH_KEY", "User") }
$region = $env:AZURE_SPEECH_REGION
if (-not $region) { $region = [Environment]::GetEnvironmentVariable("AZURE_SPEECH_REGION", "User") }
if (-not $region) { $region = "canadacentral" }
if (-not $cle) {
  Write-Host "Cle Azure introuvable. Refaire : setx AZURE_SPEECH_KEY ""TA-CLE""" -ForegroundColor Red
  Read-Host "Appuie sur Entree pour fermer"; exit 1
}

$url = "https://$region.tts.speech.microsoft.com/cognitiveservices/v1"
$entetes = @{
  "Ocp-Apim-Subscription-Key" = $cle
  "X-Microsoft-OutputFormat"  = "audio-24khz-96kbitrate-mono-mp3"
  "User-Agent"                = "qalbmousafir-voix"
}
$motif = '\[ar:([^|\]]+)\|([^\]]+)\]'

function Construire-Ssml([string]$texte, [string]$voix, [string]$mode) {
  $t = [Security.SecurityElement]::Escape($texte)
  if ($mode -eq "fr") {
    $t = [regex]::Replace($t, $motif, '$2')
    $corps = "<lang xml:lang=""fr-FR""><prosody rate=""$vitesse"">$t</prosody></lang>"
  } else {
    $corps = ""
    $pos = 0
    foreach ($m in [regex]::Matches($t, $motif)) {
      $avant = $t.Substring($pos, $m.Index - $pos)
      if ($avant.Trim()) { $corps += "<lang xml:lang=""fr-FR""><prosody rate=""$vitesse"">$avant</prosody></lang>" }
      $corps += "<lang xml:lang=""ar-SA""><prosody rate=""$vitesse"">" + $m.Groups[1].Value + "</prosody></lang>"
      $pos = $m.Index + $m.Length
    }
    $reste = $t.Substring($pos)
    if ($reste.Trim()) { $corps += "<lang xml:lang=""fr-FR""><prosody rate=""$vitesse"">$reste</prosody></lang>" }
  }
  return "<speak version=""1.0"" xmlns=""http://www.w3.org/2001/10/synthesis"" xmlns:mstts=""http://www.w3.org/2001/mstts"" xml:lang=""fr-FR""><voice name=""$voix"">$corps</voice></speak>"
}

$textes = Get-ChildItem -Path (Join-Path $dossier "textes") -Filter "*.txt" | Sort-Object Name
if (-not $textes) { Write-Host "Aucun fichier texte dans le dossier textes." -ForegroundColor Red; Read-Host "Entree"; exit 1 }

$total = 0; $erreurs = 0
foreach ($voix in $voixListe) {
  $court = ($voix -replace '^fr-FR-', '' -replace 'MultilingualNeural$', '').ToLower()
  foreach ($mode in $modes) {
    foreach ($fichier in $textes) {
      $nom = [IO.Path]::GetFileNameWithoutExtension($fichier.Name)
      $sortie = Join-Path $dossier ("audio\$court-$mode\" + $nom)
      New-Item -ItemType Directory -Force -Path $sortie | Out-Null
      Write-Host "== $court ($mode) - $nom" -ForegroundColor Cyan
      foreach ($ligne in (Get-Content -Path $fichier.FullName -Encoding UTF8)) {
        $ligne = $ligne.Trim()
        if (-not $ligne -or $ligne.StartsWith("#")) { continue }
        $parts = $ligne.Split("|", 2)
        if ($parts.Count -lt 2) { continue }
        $id = $parts[0].Trim(); $texte = $parts[1].Trim()
        $mp3 = Join-Path $sortie ($id + ".mp3")
        $trace = Join-Path $sortie ($id + ".ssml")
        $ssml = Construire-Ssml $texte $voix $mode
        if ((Test-Path $mp3) -and (Test-Path $trace) -and ((Get-Content -Raw -Encoding UTF8 $trace) -eq $ssml)) { Write-Host "  $id deja fait"; continue }
        $corps = [Text.Encoding]::UTF8.GetBytes($ssml)
        try {
          Invoke-WebRequest -Uri $url -Method Post -Headers $entetes -ContentType "application/ssml+xml; charset=utf-8" -Body $corps -OutFile $mp3 -UseBasicParsing | Out-Null
          [IO.File]::WriteAllText($trace, $ssml, (New-Object Text.UTF8Encoding($false)))
          Write-Host "  $id ok" -ForegroundColor Green
          $total += $texte.Length
        } catch {
          $erreurs++
          Write-Host "  $id ERREUR : $($_.Exception.Message)" -ForegroundColor Red
        }
      }
    }
  }
}
Write-Host ""
Write-Host "Termine. Environ $total caracteres utilises (gratuit jusqu'a 500 000 par mois). Erreurs : $erreurs" -ForegroundColor Yellow
Read-Host "Appuie sur Entree pour fermer"
