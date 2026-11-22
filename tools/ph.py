import sys
from kokoro_onnx import Kokoro
k = Kokoro(*[__import__('os').path.join(__import__('os').environ.get('QM_MODELS', __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.abspath(__file__))), 'models')), f) for f in ('kokoro.onnx','voices.bin')])
for w in sys.argv[1:]:
    print(f"{w!r:40} -> {k.tokenizer.phonemize(w, 'fr-fr')}")
