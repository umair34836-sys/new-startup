# Hindi / Hinglish voiceover (TTS) models: research, Oct 2026

Status (Oct 2026): local voiceover now = VoiceStudio (see voicestudio.md) and ai_voice.py (ACE-Step). ElevenLabs is
owner-gated (see CLAUDE.md). Audit 2026-10-24: every item below re-checked on that date at the source in brackets
(HF = huggingface.co/api/models/<id> card metadata).

Candidates (open source):
- hexgrad/Kokoro-82M: licence apache-2.0, not gated [HF]. Hindi voice files in its repo: voices/hf_alpha.pt,
  hf_beta.pt, hm_omega.pt, hm_psi.pt [HF tree listing]. "Tiny, fast on CPU": not measured here (unverified).
- harrrshall/hinglish-tts: NOT a fine-tune; it is IndicF5 (330M params) plus "a two-line duration patch and automatic
  script normalisation" (README says "No fine-tuning was applied"). Its own 30-sentence eval (self-reported): overall
  4.70 vs Kokoro v1.0 Hindi 3.90 vs Indic Parler-TTS 3.40 [raw.githubusercontent.com/harrrshall/hinglish-tts/main/README.md].
- ai4bharat/indic-parler-tts: licence apache-2.0 on the HF card (an AIKosh "MIT" claim was not re-checked); gated=auto
  (click-to-accept with a logged-in HF account + token, auto-approved) [HF]. Card language codes (18): en, as, bn, gu, hi,
  kn, ks, or, ml, mr, ne, pa, sa, sd, ta, te, ur, om [HF]. (The old "21 languages, ~1.8k h" figures could not be
  re-read: the card README is behind the gate; unverified.) Voice/style set by a text description (unverified here).
- ai4bharat/IndicF5: licence mit, gated=auto, 11 language codes: as, bn, gu, mr, hi, kn, ml, or, pa, ta, te (no Urdu)
  [HF]. In arXiv 2604.21481 ("Preferences of a Voice-First Nation", 7 TTS systems, 120K+ pairwise votes) IndicF5 ranks
  last (Table 3, 805.75) [arxiv.org/pdf/2604.21481].
- harrrshall/xtts-v2-hinglish-synthetic: XTTS-v2 fine-tune, licence coqui-public-model-license (CPML, coqui.ai/cpml)
  [its HF README]. CPML "allows only non-commercial use of a machine learning model and its outputs"
  [huggingface.co/coqui/XTTS-v2/raw/main/LICENSE.txt].
- facebook/mms-tts-hin: Hindi only, licence cc-by-nc-4.0 = NON-COMMERCIAL [HF]. "Robotic": not measured (unverified).
