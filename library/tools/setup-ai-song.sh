#!/bin/bash
# Install ACE-Step 1.5 (lyrics -> song with vocals) and OpenAI Whisper (transcription) into
# /home/user/tools/venv (Python 3.12, CPU). Code comes from GitHub/pypi, which this environment allows.
# Model WEIGHTS still download on first use from huggingface.co (ACE-Step) and
# openaipublic.azureedge.net (Whisper): those hosts must be allowed in the environment's network settings.
set -euo pipefail
T=/home/user/tools
mkdir -p "$T" && cd "$T"
[ -d ACE-Step-1.5 ] || GIT_LFS_SKIP_SMUDGE=1 git clone -q --depth 1 https://github.com/ace-step/ACE-Step-1.5

# CPU-only box: install torch from the CPU wheel index. The pypi build pulls ~4.9 GB of nvidia-* CUDA libs + triton
# that are useless here and filled the disk (Oct 2026); the +cpu build is the same version without them.
cat > reqs-cpu.txt <<'EOF'
torch==2.10.0
torchvision==0.25.0
torchaudio==2.10.0
safetensors==0.7.0
transformers>=4.51.0,<4.58.0
diffusers
gradio==6.2.0
matplotlib>=3.7.5
scipy>=1.10.1
soundfile>=0.13.1
loguru>=0.7.3
einops>=0.8.1
accelerate>=1.12.0
fastapi>=0.110.0
uvicorn[standard]>=0.27.0
python-multipart>=0.0.18
numba>=0.63.1
vector-quantize-pytorch>=1.27.15
torchcodec>=0.9.1
torchao>=0.16.0,<0.17.0
toml
modelscope
pytorch-wavelets>=1.3.0
openai-whisper
yt-dlp
diskcache
peft>=0.18.0
typer-slim>=0.21.1
pywavelets>=1.9.0
setuptools<72
EOF
[ -d venv ] || uv venv -q -p /usr/bin/python3.12 venv
source venv/bin/activate
uv pip install -q -r reqs-cpu.txt --index-url https://download.pytorch.org/whl/cpu \
  --extra-index-url https://pypi.org/simple --index-strategy unsafe-best-match
uv pip install -q --no-deps -e ACE-Step-1.5 -e ACE-Step-1.5/acestep/third_parts/nano-vllm
python -c "import torch, whisper, acestep; print('ready: torch', torch.__version__, '| whisper | acestep')"
