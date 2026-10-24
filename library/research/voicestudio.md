# VoiceStudio (debpalash/VoiceStudio): checked Oct 24 2026

- What: "open-source, fully-local ElevenLabs alternative": voice cloning, voice design, video dubbing, dictation,
  transcription, audiobooks; 16+ TTS and 11 ASR engines behind one FastAPI backend + Electron app. Formerly
  OmniVoice-Studio. Repo licence AGPL-3.0 (commercial licence on request). Version tested: 0.5.7-beta.2 (commit 80a01e5).
  A dev.to post calls it "82k stars" (not verified here; GitHub web pages blocked for the API in this session).
- Install here (no GPU, no display): clone, `uv sync --locked --no-group cuda --group cpu` (CPU torch 2.8.0, venv 2.3 GB,
  Python 3.11), then `library/tools/voicestudio.sh start` = `uv run --no-sync uvicorn main:app --app-dir backend --port 3900`.
  Skip `scripts/setup.py` (Windows VC++/CUDA/ROCm only). /health -> {"status":"ok","device":"cpu"}.
- API: OpenAI-style `POST /v1/audio/speech` {model, input, voice, language, instruct (voice design text), seed,
  response_format}; native `POST /generate` (multipart: text, language, ref_audio + ref_text for cloning, instruct,
  profile_id, num_step, guidance_scale, speed, effect_preset); `/v1/audio/transcriptions`; profiles `/profiles`;
  model catalogue `GET /models`, `POST /models/install {"repo_id"}`, status `/models/install/status`; MCP at /mcp.
- Model downloads need 2 GB headroom beyond the model; OmniVoice (3.27 GB incl. audio tokenizer) took 30 s.
- LICENCES (VoiceStudio's own registry, GET /models/licenses/details/<repo>): generation is blocked (403
  model_licence_required) until the licence is accepted (POST /models/licenses/accept).
  * k2-fsa/OmniVoice (default engine, 600+ languages incl. Urdu/Hindi/Pashto, cloning + design):
    "CC-BY-NC; Higgs Audio 2; Meta Llama 3" = NON-COMMERCIAL. Not for client/paid videos.
    Its tokenizer eustlb/higgs-audio-v2-tokenizer: licence NOASSERTION.
  * openbmb/VoxCPM2 (5 GB, 30 languages incl. Hindi, cloning + design, slow on CPU): apache-2.0.
  * FunAudioLLM CosyVoice3 0.5B (9.8 GB): apache-2.0, no Hindi/Urdu. GPT-SoVITS: MIT (zh/en/ja/ko/yue).
  * MOSS-TTS-Nano 100M (20 langs, CPU realtime), KittenTTS (English): apache-2.0.
  Registry note: "Licence identifier is upstream model-card metadata, not verified".
- Disk: the main tools venv carried the CUDA torch build (nvidia-* + triton = ~5 GB) on this CPU-only box. Swapped to
  torch 2.10.0+cpu (download.pytorch.org/whl/cpu): free disk 3.2 -> 9.1 GB, ACE-Step/whisper/audio-separator still import
  (torchao prints harmless "Failed to load _C_mxfp8/_C_cutlass_90a" CUDA-kernel warnings). setup-ai-song.sh now does this.
- Test Oct 24 2026 (OmniVoice, CPU, seed 7, instruct "male, young adult"/"male, middle-aged, low pitch"): Urdu 5.4 s in
  29 s (incl. model load), Urdu 9.5 s in 36 s, Hindi 6.8 s in 32 s, Pashto 4.4 s in 22 s. Whisper small match vs the
  script: Urdu 100% and 97%, Hindi 92%, Pashto 81% (Whisper's own Pashto is weak). Owner accepted the OmniVoice and
  VoxCPM2 licences (Oct 24 2026). voxcpm 2.0.3 installed into VoiceStudio's venv (keeps torch 2.8.0+cpu); the VoxCPM2
  checkpoint (4.96 GB) was NOT downloaded: only 4.7 GB disk free in this session.
