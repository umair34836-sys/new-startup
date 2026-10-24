# VoiceStudio (debpalash/VoiceStudio): checked Oct 24 2026

Audit 2026-10-24: licences/sizes re-read on huggingface.co API and the repo README (raw.githubusercontent.com); the
install steps and test timings below are past measurements in an earlier session the same day (not re-run).

- What: "open-source, fully-local ElevenLabs alternative": voice cloning, voice design, video dubbing, dictation,
  transcription, audiobooks; 16+ TTS and 11 ASR engines behind one FastAPI backend + Electron app. Formerly
  OmniVoice-Studio. Repo licence AGPL-3.0 (README badge + Exa repo metadata, 2026-10-24; the README says a paid app licence exists but does
  not cover model weights). Version tested: 0.5.7-beta.2 (commit 80a01e5).
  Stars: 79,257 (Exa snapshot via agent-reach web search, 2026-10-24; a dev.to post had said "82k").
- Install here (no GPU, no display): clone, `uv sync --locked --no-group cuda --group cpu` (CPU torch 2.8.0, venv 2.3 GB,
  Python 3.11), then `library/tools/voicestudio.sh start` = `uv run --no-sync uvicorn main:app --app-dir backend --port 3900`.
  Skip `scripts/setup.py` (Windows VC++/CUDA/ROCm only). /health -> {"status":"ok","device":"cpu"}.
- API: OpenAI-style `POST /v1/audio/speech` {model, input, voice, language, instruct (voice design text), seed,
  response_format}; native `POST /generate` (multipart: text, language, ref_audio + ref_text for cloning, instruct,
  profile_id, num_step, guidance_scale, speed, effect_preset); `/v1/audio/transcriptions`; profiles `/profiles`;
  model catalogue `GET /models`, `POST /models/install {"repo_id"}`, status `/models/install/status`; MCP at /mcp.
- Model downloads need 2 GB headroom beyond the model; OmniVoice (repo files total 3.27 GB, HF API tree 2026-10-24) took 30 s.
- LICENCES (VoiceStudio's own registry, GET /models/licenses/details/<repo>): generation is blocked (403
  model_licence_required) until the licence is accepted (POST /models/licenses/accept).
  * k2-fsa/OmniVoice (default engine, 600+ languages incl. Urdu/Hindi/Pashto, cloning + design):
    "CC-BY-NC; Higgs Audio 2; Meta Llama 3" = NON-COMMERCIAL. Not for client/paid videos. (Confirmed 2026-10-24 on the HF
    card: "The pre-trained model is licensed under the CC-BY-NC"; card lists 646 language codes incl. ur, hi, ps, pbt.)
    Its tokenizer eustlb/higgs-audio-v2-tokenizer: licence NOASSERTION.
  * openbmb/VoxCPM2 (4.96 GB, 30 language codes incl. hi, no ur/ps; apache-2.0: HF API 2026-10-24; cloning + design
    and "slow on CPU" not re-checked).
  * FunAudioLLM CosyVoice3 0.5B (9.8 GB): apache-2.0 (HF Fun-CosyVoice3-0.5B-2512, 2026-10-24), no Hindi/Urdu (registry).
    GPT-SoVITS: MIT (HF lj1995/GPT-SoVITS, 2026-10-24) (zh/en/ja/ko/yue per registry).
  * MOSS-TTS-Nano 100M (20 langs, CPU realtime): apache-2.0 per the registry (HF repo id not found in the audit:
    unverified). KittenTTS (English): apache-2.0 (HF KittenML/kitten-tts-nano-0.1, 2026-10-24).
  Registry note: "Licence identifier is upstream model-card metadata, not verified".
- Disk: the main tools venv carried the CUDA torch build (nvidia-* + triton = ~5 GB) on this CPU-only box. Swapped to
  torch 2.10.0+cpu (download.pytorch.org/whl/cpu): free disk 3.2 -> 9.1 GB, ACE-Step/whisper/audio-separator still import
  (torchao prints harmless "Failed to load _C_mxfp8/_C_cutlass_90a" CUDA-kernel warnings). setup-ai-song.sh now does this.
- Test Oct 24 2026 (OmniVoice, CPU, seed 7, instruct "male, young adult"/"male, middle-aged, low pitch"): Urdu 5.4 s in
  29 s (incl. model load), Urdu 9.5 s in 36 s, Hindi 6.8 s in 32 s, Pashto 4.4 s in 22 s. Whisper small match vs the
  script: Urdu 100% and 97%, Hindi 92%, Pashto 81% (Whisper's own Pashto is weak). Owner accepted the OmniVoice and
  VoxCPM2 licences (Oct 24 2026). voxcpm 2.0.3 installed into VoiceStudio's venv (keeps torch 2.8.0+cpu); the VoxCPM2
  checkpoint (4.96 GB) was NOT downloaded: only 4.7 GB disk free in this session.

## VoxCPM2 Hindi test (MoradoSolution promo, measured here 2026-10-24)
- Install: freed disk (OmniVoice HF cache 3.1 GB, npm cache, ACE-Step LM 1.7B 3.5 GB), then
  `curl -X POST :3900/models/install -d '{"repo_id":"openbmb/VoxCPM2"}'` -> 4.7 GB in ~/.cache/huggingface in a few
  minutes (model.safetensors 4,580,080,592 B + audiovae.pth 376,951,122 B: HF tree API 2026-10-24). Licence: apache-2.0.
- Speed on this 4-core CPU: first request 2m22s for a 2.1 s line (model load + 28 s warm-up); later lines 2.1-8.4 s of audio
  took ~1-3 min each (file mtimes); 8 lines ~13 min.
- Voice design per line (`--instruct`, one request per line) gave a DIFFERENT voice per line: median f0 164-240 Hz across
  the 8 lines (pyworld harvest). For one consistent narrator, clone one good line instead (`--ref` + `--ref-text`).
- Mixed script (English words in Latin inside Hindi) came out with garbled English per Whisper small ("India" ->
  "अरी अद्टीा", "included" -> "ख्लूदेड"); one line ran on for 8.4 s with nonsense after the real words
  (Whisper heard extra syllables after "फ्र्रंकफुट में"). Whisper-check every line; regenerate bad ones.
