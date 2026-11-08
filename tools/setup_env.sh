#!/bin/bash
# TrueWhys toolchain for a fresh cloud container: Blender (bpy), Kokoro + Gemini voice tools, Whisper, Kaggle CLI, ffmpeg.
# Idempotent; run from the repo root or by the environment setup script. Test prefix: C3D_PREFIX=/tmp/x KOKORO_PREFIX=/tmp/k
set -e
P=${C3D_PREFIX:-/opt/c3d}; K=${KOKORO_PREFIX:-/opt/kokoro}
if ! command -v ffmpeg >/dev/null || ! command -v espeak-ng >/dev/null; then
  apt-get update -qq && apt-get install -y -qq ffmpeg espeak-ng libcairo2 libxkbcommon0 libsm6 libxi6 libxxf86vm1 libxfixes3 libxrender1 libgl1 >/dev/null
fi
command -v uv >/dev/null || python3 -m pip install -q uv || pip install -q uv
if [ ! -x "$P/bin/python" ]; then
  uv venv -q -p 3.11 "$P"
  uv pip install -q -p "$P/bin/python" cairosvg==2.9.1 kokoro-onnx==0.6.1 faster-whisper==1.2.1 kaggle==2.2.5 \
    numpy pillow pyloudnorm scipy soundfile yt-dlp cython requests zstandard
  # bpy pins numpy<2 but kokoro needs numpy>=2; bpy works with numpy 2 (only a harmless import warning), so skip its pin
  uv pip install -q -p "$P/bin/python" --no-deps bpy==5.0.1
fi
mkdir -p "$K"
for f in kokoro-v1.0.onnx voices-v1.0.bin; do
  [ -s "$K/$f" ] || curl -sSL -o "$K/$f" "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/$f"
done
"$P/bin/python" -c "import bpy, kokoro_onnx, faster_whisper, cairosvg, pyloudnorm, soundfile, PIL; print('toolchain ok', bpy.app.version_string)"
