#!/usr/bin/env python3
"""Urdu / Pashto / Hindi caption block for HyperFrames (Nastaliq-safe, RTL, per-word reveal).

  python3 urdu_captions.py spec.json compositions/ucap.html      # write the scene
  python3 urdu_captions.py --check spec.json --fonts assets/fonts  # only check the text

spec.json:
  {"id": "ucap", "width": 1080, "height": 1920, "duration": 6,
   "lines": [{"in": 0.2, "out": 2.8, "text": "... *accent ...", "script": "nastaliq", "sub": "optional LTR line"}]}

script: nastaliq (Urdu, default) | naskh (Pashto, Urdu fallback) | sans (bold Arabic-script titles) | deva (Hindi) | latin.
A word starting with * is the gold accent word. Words are split on spaces only, never inside a word,
so Arabic-script joining is kept (splitting letters into spans breaks the joins: tested, see
library/research/urdu-captions.md). A word with no Arabic-script letter (Latin, ASCII digits, phone
numbers) gets dir="ltr" inside its own span, so it reads left-to-right inside the RTL line.

Copy into the project's assets/fonts/: NotoNastaliqUrdu-Variable.ttf, NotoNaskhArabic-Variable.ttf,
NotoSansArabic-Variable.ttf, NotoSansDevanagari-Variable.ttf, PlusJakartaSans-Variable.ttf
(all in library/fonts), and GSAP to assets/vendor/gsap-3.14.2.min.js.
--check reports characters missing from the font a line uses, Arabic presentation-form code points,
and Arabic yeh/kaf (U+064A / U+0643) in Urdu lines (Urdu uses U+06CC / U+06A9; sources in the research note).
It never changes the text.
"""
import html
import json
import os
import re
import sys
import unicodedata

FONTS = {
    "nastaliq": ("NotoNastaliqUrdu-Variable.ttf", "UrNastaliq", "rtl", 700, 2.0, "0.25em"),
    "naskh": ("NotoNaskhArabic-Variable.ttf", "UrNaskh", "rtl", 700, 1.7, "0.12em"),
    "sans": ("NotoSansArabic-Variable.ttf", "UrSans", "rtl", 800, 1.7, "0.1em"),
    "deva": ("NotoSansDevanagari-Variable.ttf", "HiDeva", "ltr", 700, 1.5, "0"),
    "latin": ("PlusJakartaSans-Variable.ttf", "Jakarta", "ltr", 800, 1.3, "0"),
}
ARABIC = re.compile(r"[؀-ۿݐ-ݿࢠ-ࣿ]")
PRESENTATION = re.compile(r"[ﭐ-﷿ﹰ-﻿]")


def word_spans(text, lid):
    # Consecutive LTR words share one span: separate LTR spans in an RTL line get laid out
    # right-to-left ("UDHR 1948" showed as "1948 UDHR" when tested).
    groups = []
    for w in text.split():
        gold = w.startswith("*") and len(w) > 1
        w = w[1:] if gold else w
        ltr = not ARABIC.search(w)
        if ltr and groups and groups[-1][0] and groups[-1][1] == gold:
            groups[-1][2].append(w)
        else:
            groups.append([ltr, gold, [w]])
    out = []
    for ltr, gold, ws in groups:
        cls = "w %s-w" % lid + (" gold" if gold else "")
        out.append('<span class="%s"%s>%s</span>' % (cls, ' dir="ltr"' if ltr else "", html.escape(" ".join(ws))))
    return " ".join(out)


def build(spec):
    cid = spec.get("id", "ucap")
    W, H = spec.get("width", 1080), spec.get("height", 1920)
    fs = spec.get("font_size", 74 if W < H else 64)
    bottom = spec.get("bottom", 300 if W < H else 110)
    used = sorted({l.get("script", "nastaliq") for l in spec["lines"]} | {"latin"})
    faces = "\n".join(
        '    @font-face { font-family: "%s"; src: url("assets/fonts/%s"); font-weight: 100 900; }' % (FONTS[k][1], FONTS[k][0])
        for k in used)
    styles = "\n".join(
        '    .s-%s { font-family: "%s", sans-serif; direction: %s; font-weight: %d; line-height: %s; word-spacing: %s; }'
        % (k, FONTS[k][1], FONTS[k][2], FONTS[k][3], FONTS[k][4], FONTS[k][5]) for k in used)
    lines, js, pre = [], [], []
    for i, l in enumerate(spec["lines"], 1):
        lid = "%s-l%d" % (cid, i)
        sc = l.get("script", "nastaliq")
        lang = {"nastaliq": "ur", "naskh": l.get("lang", "ps"), "sans": "ur", "deva": "hi", "latin": "en"}[sc]
        sub = ('\n      <div class="sub" dir="ltr">%s</div>' % html.escape(l["sub"])) if l.get("sub") else ""
        lines.append('    <div id="%s" class="line s-%s" lang="%s" dir="%s">%s%s</div>'
                     % (lid, sc, lang, FONTS[sc][2], word_spans(l["text"], lid), sub))
        tin, tout = float(l["in"]), float(l["out"])
        if tin <= 0:
            pre.append('    gsap.set("#%s", { visibility: "visible" });' % lid)
        else:
            js.append('    tl.set("#%s", { visibility: "visible" }, %.3f);' % (lid, tin))
        js.append('    tl.fromTo(".%s-w", { opacity: 0, y: 26, filter: "blur(10px)" }, { opacity: 1, y: 0, filter: "blur(0px)", '
                  'duration: 0.34, ease: "power3.out", stagger: 0.12 }, %.3f);' % (lid, tin))
        if l.get("sub"):
            js.append('    tl.fromTo("#%s .sub", { opacity: 0 }, { opacity: 1, duration: 0.3 }, %.3f);' % (lid, tin + 0.2))
        js.append('    tl.to("#%s", { opacity: 0, filter: "blur(6px)", duration: 0.2, ease: "power2.in" }, %.3f);' % (lid, tout - 0.2))
        js.append('    tl.set("#%s", { visibility: "hidden" }, %.3f);' % (lid, tout))
    return f"""<template>
  <style>
{faces}
    #root {{ position: absolute; inset: 0; pointer-events: none; }}
    #{cid}-veil {{ position: absolute; left: 0; right: 0; bottom: 0; height: {int(H * 0.42)}px;
      background: linear-gradient(to top, rgba(6, 8, 12, 0.88), rgba(6, 8, 12, 0.55) 45%, rgba(6, 8, 12, 0)); }}
    .line {{ position: absolute; left: {int(W * 0.08)}px; right: {int(W * 0.08)}px; bottom: {bottom}px; text-align: center;
      font-size: {fs}px; color: var(--text, #ffffff); unicode-bidi: isolate; visibility: hidden;
      text-shadow: 0 4px 24px rgba(0, 0, 0, 0.85), 0 1px 3px rgba(0, 0, 0, 0.7); }}
{styles}
    .line .w {{ display: inline-block; }}
    .line .gold {{ color: var(--accent, #ffc94a); }}
    .line .sub {{ font-family: "Jakarta", sans-serif; font-weight: 600; font-size: {int(fs * 0.5)}px; line-height: 1.3;
      direction: ltr; word-spacing: 0; color: rgba(255, 255, 255, 0.86); margin-top: 6px; }}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="{W}" data-height="{H}" data-layout-allow-overflow>
    <div id="{cid}-veil"></div>
{chr(10).join(lines)}
  </div>
  <script>
    gsap.set(".line .w", {{ opacity: 0 }});
{chr(10).join(pre)}
    const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""


def check(spec, font_dir):
    from fontTools.ttLib import TTFont
    cmaps, problems = {}, 0
    for i, l in enumerate(spec["lines"], 1):
        sc = l.get("script", "nastaliq")
        f = os.path.join(font_dir, FONTS[sc][0])
        if f not in cmaps:
            cmaps[f] = TTFont(f).getBestCmap()
        text = l["text"].replace("*", "")
        miss = sorted({c for c in text if not c.isspace() and ord(c) not in cmaps[f]})
        for c in miss:
            problems += 1
            print("line %d: U+%04X %s not in %s" % (i, ord(c), unicodedata.name(c, "?"), FONTS[sc][0]))
        for c in sorted(set(PRESENTATION.findall(text))):
            problems += 1
            print("line %d: presentation form U+%04X %s (ask the supplier; effect on shaping untested)" % (i, ord(c), unicodedata.name(c, "?")))
        if sc in ("nastaliq", "sans") and l.get("lang", "ur") == "ur":
            for c in ("ي", "ك"):
                if c in text:
                    problems += 1
                    print("line %d: %s U+%04X found; Urdu normally uses %s (check the source text, do not guess)"
                          % (i, unicodedata.name(c), ord(c), "U+06CC" if c == "ي" else "U+06A9"))
        for w in text.split():
            if not ARABIC.search(w) and sc in ("nastaliq", "naskh", "sans"):
                print("line %d: '%s' has no Arabic-script letter -> rendered LTR" % (i, w))
    print("problems: %d" % problems)
    return problems


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "--check":
        fd = a[a.index("--fonts") + 1] if "--fonts" in a else os.path.join(os.path.dirname(__file__), "..", "fonts")
        sys.exit(1 if check(json.load(open(a[1], encoding="utf-8")), fd) else 0)
    if len(a) != 2:
        sys.exit(__doc__)
    open(a[1], "w", encoding="utf-8").write(build(json.load(open(a[0], encoding="utf-8"))))
    print("wrote", a[1])
