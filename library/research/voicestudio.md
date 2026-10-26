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

## VoxCPM2 Hindi tutorial VO (FireCraft whitelist tutorial, measured here 2026-10-24)
- Setup in a fresh container: setup-all.sh's `uv sync` for VoiceStudio failed once ("Failed to inspect Python interpreter
  ... .venv/bin/python3"), a rerun worked; a second `uv sync` REMOVES voxcpm (not in the lock), so reinstall
  `voxcpm>=2.0.3` after every sync. Model install via the API: 4.7 GB in ~/.cache/huggingface in about 2 min.
  `POST /models/licenses/accept {"repo_id"}` alone returns 422 (needs fingerprint + accepted), but generation with
  VoxCPM2 worked anyway in this container.
- Design one line (`--instruct "male, young adult, friendly, clear, energetic youtube tutorial narrator"`): seed 7
  said every word but added a run-on tail ("आप दिकनियाएका?", 4.5-5.3 s); seed 21 garbled more. Trimmed seed 7 at 4.3 s
  (silence at 4.04-4.62 s) and used it as `--ref` for cloning: 11 lines, one consistent voice, no run-on tails
  (last word end = clip end), each line 2.5-6.3 s, first request 2m30s incl. load, the 11 cloned lines ~15 min.
- Whisper small similarity on cloned lines: 32-90%; low scores were mostly spelling (अकाँँट, स्तेटस), but line
  "फिर लिखें कि आप फ़ायरक्राफ़्ट क्यों..." was garbled at seed 7 (33%) and fine at seed 33 (71%).
  "स्टाफ़ चौबीस से अड़तालीस घंटे..." stayed unclear in 3 seeds ("चाछ चाबिष", "अच्टाएद"); number words चौबीस/अड़तालीस
  and घंटे ("गड़े") were heard wrong in every take, so the numbers were also shown on screen.

## VoxCPM2 WELCOME30 reel VO (MoradoSolution, measured here 2026-10-24)
- Fresh container: `POST /models/install {"repo_id":"openbmb/VoxCPM2"}` finished in under 5 min (4,960,731,703 B on disk);
  voxcpm already importable in VoiceStudio's .venv. Reference line (design, seed 7) took 3m58s incl. model load.
- 8 cloned lines (`--parts`) took ~19 min. Whisper small heard every word of all 8 (scores 0-43% are spelling only:
  it writes "30% OFF", "AMD Epic, NVMe" in Latin). One pass missed the first words of a line with spelled letters
  ("ए एम डी एपिक, एन वी एम ई") but a second transcription heard them: re-run before regenerating.
- `--parts` writes 000.wav..007.wav (zero-based). To give a scene more screen time without regenerating, rebuild the
  VO from the parts with a longer silence after that line (numpy concat) and rewrite lines.json; then loudnorm.

## VoxCPM2 long Hindi VO (MoradoSolution RDP + BUSY explainer, measured here 2026-10-26)
- First /generate right after `voicestudio.sh start` returned HTTP 400 after 12 s (vs_tts.py curl exit 22); the same request
  a minute later succeeded (200) but took 604 s, because the first call loads the model. Send one short warm-up request and
  wait for its 200 before a long batch.
- 24 cloned lines (seed 7, ref from the brief recipe) took 08:16-09:35 (~3.3 min per line, 0.6-7.0 s lines).
- Whisper small could not hear "हेलो एवरीवन!" in any of 5 takes (seeds 7/21/33, Latin "Hello everyone!", spelling हेल्लो),
  even joined to the next line; listen.py voice activity does show speech there (0.67-1.6 s). Unverified, kept.
- "इंडियन आर डी पी" came back as "अद्टिन अद्टीपी" / "अईंदिन अड़िपी" in every take (Devanagari, hyphenated, Latin "Indian RDP")
  and "प्री-इंस्टॉल्ड और प्री-कॉन्फ़िगर्ड" garbled in all 3 seeds; rewording to "पहले से इंस्टॉल और कॉन्फ़िगर होगा" was heard.
- "थैंक यू फ़ॉर चूज़िंग अवर सर्विस" garbled at seeds 7 and 33, clear at seed 21. Regenerate weak lines with 2 more seeds.
