#!/usr/bin/env bash
# Installe les dépendances et télécharge le modèle de voix (≈ 330 Mo) dans models/
set -e
cd "$(dirname "$0")/.."
pip install --break-system-packages -q kokoro-onnx soundfile pillow numpy opencv-python-headless
mkdir -p models
[ -f models/kokoro.onnx ] || curl -L -o models/kokoro.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
[ -f models/voices.bin ] || curl -L -o models/voices.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
echo "Prêt. Exemple : python3 tools/render.py episodes/ep2_woudou.json --preview"
