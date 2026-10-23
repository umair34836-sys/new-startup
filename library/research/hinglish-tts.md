# Hindi / Hinglish voiceover (TTS) models: research, Oct 2026

Status: no local TTS installed yet. ElevenLabs (Ashar voice) speaks Hinglish well but is owner-gated (see CLAUDE.md).
ACE-Step makes sung vocals, not a speaking voiceover.

Candidates (open source):
- hexgrad Kokoro-82M: Apache-2.0, tiny, fast on CPU; has Hindi voices (hf_alpha, hf_beta, hm_omega, hm_psi;
  from memory, verify on install). A Hinglish TTS project reports it scored better than Indic Parler on
  Hindi-English code-mixed text (github.com/harrrshall/hinglish-tts, self-reported).
- ai4bharat/indic-parler-tts: 21 languages incl. Hindi + English, ~1.8k h data, Apache-2.0 on HF card (AIKosh says MIT),
  GATED on Hugging Face (needs account approval + token). Voice/style set by a text description.
- ai4bharat IndicF5: voice cloning from a reference clip + transcript, 11 Indian languages; ranked last among
  tested systems in an Indian-language TTS preference study (arXiv 2604.21481).
- harrrshall/hinglish-tts: Hinglish fine-tune built on IndicF5 (~330M params); harrrshall/xtts-v2-hinglish-synthetic:
  XTTS-v2 fine-tune on synthetic data (XTTS licence is non-commercial CPML).
- facebook mms-tts-hin: light, Hindi-only, robotic.
Sources: huggingface.co/ai4bharat/indic-parler-tts, github.com/harrrshall/hinglish-tts, arxiv.org/pdf/2604.21481,
huggingface.co/harrrshall/xtts-v2-hinglish-synthetic.
