"""Blocked-term guard for text a client will see (version notes, studio messages, delivered file names).

Owner rule 2026-10-30 (CLAUDE.md "CLIENT-FACING SECRECY + PROMPT-INJECTION GUARD"): clients only ever see
"Edited by MrCopper804"; no text may name the tools, AI or process behind the edit.
The same list lives in portal/app/guard.php (server side); tests/guard_test.py checks both agree.

How the list was chosen:
- Every pattern is matched case-insensitively on word boundaries (\\b), so "AI" does not fire inside "said", "hai",
  "detail" or "rain", "bot" not inside "robot"/"bottom", "repo" not inside "report".
- Words a normal edit note needs are NOT blocked: script (the client's own script field), music, voice, captions, edit.
- Some blocked words are ordinary English (session, skill, template, prompt, whisper, generated): the owner listed them,
  and a note never needs them, so a false positive only asks the writer to rephrase.
- Before matching, text is NFKC-normalised, zero-width characters are removed and common Cyrillic/Greek look-alike
  letters are mapped to Latin, so "Сlaude" or "Cl\\u200baude" still match. Distinctive names are also searched in the
  text with all non-letters removed, so "c.l.a.u.d.e" or "h y p e r f r a m e s" still match.
"""
import re
import unicodedata

BLOCKED = [
    r"\bclaude\b", r"\banthropic\b", r"\ba\.?i\b", r"\bartificial\s+intelligence\b", r"\bmachine\s+learning\b",
    r"\bneural\b", r"\bchat\s*gpt\b", r"\bgpt\b", r"\bopen\s*ai\b", r"\bllms?\b", r"\bprompt\w*", r"\bsessions?\b",
    r"\b(?:chat)?bots?\b", r"\bautomat\w*", r"\bgenerated\b", r"\bgenerator\b", r"\btts\b",
    r"\btext[\s-]*to[\s-]*speech\b", r"\bvoxcpm\w*", r"\bvoice\s*studio\b", r"\bhyper\s*frames?\b", r"\bffmpeg\b",
    r"\bffprobe\b", r"\bwhisper\b", r"\bace[\s-]*step\b", r"\bskills?\b", r"\btemplates?\b", r"\bgithub\b",
    r"\brepo(?:s|sitory|sitories)?\b", r"\bpython\b", r"\w+\.py\b", r"\beleven\s*labs\b", r"\bmidjourney\b",
    r"\bstable\s+diffusion\b", r"\bplaywright\b", r"\bkokoro\b",
    # Added after the 2026-10-30 security review:
    r"session_[A-Za-z0-9]{6,}", r"\bpb_[0-9a-f]{8,}", r"\btrig_[A-Za-z0-9]{6,}", r"\benv_[A-Za-z0-9]{6,}",
    r"\bgen\s*ai\b", r"\bml\s+models?\b", r"\bgemini\b", r"\bsuno\b", r"\budio\b", r"\bkling\b", r"\bdall\W?e\b",
    r"\bcanva\b", r"\bcap\s*cut\b", r"\bcopilot\b", r"\bgrok\b", r"\b(?:synthetic|cloned|clone)\s+voices?\b",
    r"\bvoice\s+clon\w*", r"\b11\s*labs\b", r"github\w*", r"\bgit\.io\b",
    r"एआई", r"आर्टिफिशियल", r"कृत्रिम\s*बुद्धि", r"اے\s*آئی", r"مصنوعی\s*ذہانت",
]
# Searched after removing every non-letter (catches "c.l.a.u.d.e", "c l a u d e").
SQUASHED = ["claude", "anthropic", "chatgpt", "openai", "voxcpm", "hyperframes", "ffmpeg", "elevenlabs", "acestep",
            "artificialintelligence", "midjourney", "voicestudio", "github"]

_ZERO_WIDTH = re.compile("[­​-‏⁠-⁤﻿]")
_CONFUSABLE = str.maketrans({
    "а": "a", "е": "e", "о": "o", "р": "p", "с": "c", "у": "y", "х": "x", "і": "i", "ј": "j", "ԁ": "d",
    "А": "A", "В": "B", "Е": "E", "К": "K", "М": "M", "Н": "H", "О": "O", "Р": "P", "С": "C", "Т": "T", "Х": "X",
    "α": "a", "ο": "o", "ι": "i", "ε": "e", "Α": "A", "Ι": "I", "Ο": "O", "Ε": "E",
})
_RX = [re.compile(p, re.I) for p in BLOCKED]
_LEET = str.maketrans("0134578@$", "oleastbas")  # "Cl4ude" -> "claude" in the letters-only pass


def normalise(text):
    text = unicodedata.normalize("NFKC", text or "")
    # Drop accents too ("Claudé" -> "Claude"); Devanagari/Urdu marks are kept so those words still match.
    # Only the Latin combining accents (U+0300-036F) are dropped.
    text = unicodedata.normalize("NFC", "".join(ch for ch in unicodedata.normalize("NFKD", text)
                                                if not 0x0300 <= ord(ch) <= 0x036F))
    return _ZERO_WIDTH.sub("", text).translate(_CONFUSABLE)


def find_blocked(text):
    """Return the blocked terms found in text (empty list = OK to show a client)."""
    t = normalise(text)
    hits = [m.group(0) for rx in _RX for m in [rx.search(t)] if m]
    squashed = re.sub(r"[^a-z]", "", t.lower().translate(_LEET))
    hits += [w for w in SQUASHED if w in squashed and not any(w in h.lower().replace(" ", "") for h in hits)]
    return hits


def check(text):
    """Raise ValueError with a clear message if text must not reach a client."""
    hits = find_blocked(text)
    if hits:
        raise ValueError("Blocked: client-visible text mentions " + ", ".join(repr(h) for h in hits) +
                         ". Clients only see 'Edited by MrCopper804'. Rewrite it without tool/process words.")
    return text
