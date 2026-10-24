# Urdu / Pashto / Hindi captions in HyperFrames

Everything here is either sourced (URL + date read) or "tested here 2026-10-24" with HyperFrames 0.8.188
(`npx --yes hyperframes@0.8.188 check --json`, `snapshot --at ...`, `render --quality draft`), Chromium in the cloud
container, 1080x1920 test project in the session scratchpad. Screenshots were looked at, not committed.
Anything not checked is marked **unverified**.

## Fonts (library/fonts, all SIL OFL 1.1, licence file beside each)

Downloaded 2026-10-24 from `https://raw.githubusercontent.com/google/fonts/main/ofl/<family>/` (licence "OFL" in each
family's METADATA.pb, OFL.txt copied). Coverage checked with fontTools `getBestCmap()` for: Urdu `ٹڈڑںھہۂےۓیکگپچژ`,
Pashto `ټډړږښګڼۍېځڅ`, Urdu digits `۰-۹`, Devanagari sample, Latin A-Z/0-9.

| File | Use | Urdu | Pashto | Weights | hhea line ("normal") |
| --- | --- | --- | --- | --- | --- |
| `NotoNastaliqUrdu-Variable.ttf` (v3.009) | Urdu captions, Nastaliq | yes | yes in cmap (see Pashto note) | wght 400-700 | 2.50 em |
| `Gulzar-Regular.ttf` (v1.000) | Alternative Nastaliq | yes | **no** (ټ ډ ړ ږ ښ ګ ڼ ۍ ې ځ څ missing) | 400 | 2.70 em |
| `NotoNaskhArabic-Variable.ttf` (v2.021) | Pashto captions, Naskh Urdu | yes | yes | 400-700 | 1.70 em |
| `NotoSansArabic-Variable.ttf` (v2.012) | Bold display titles | yes | yes | 100-900, wdth 62.5-100 | 2.11 em |
| `Vazirmatn-Variable.ttf` (v33.003) | Bold display titles | yes | yes | 100-900 | 1.56 em |
| `NotoSansDevanagari-Variable.ttf` (v2.007) | Hindi | - | - | 100-900, wdth | 1.30 em |
| `Mukta-Regular.ttf`, `Mukta-Bold.ttf` (v2.538) | Hindi | - | - | 400 / 700 | 1.66 em |

Also checked and NOT added: Lalezar (no Pashto letters), Lateef (has Pashto; not needed beside Noto Naskh).
Mehr Nastaliq / Jameel Noori Nastaleeq: not added, no OFL licence verified.
All Arabic-script fonts above also contain Latin and ASCII digits (cmap check).

## Test text (never invented)

Sample lines are copied from the UDHR translations in NLTK's `udhr2` corpus
(`https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/udhr2.zip`, read 2026-10-24):
`urd.txt` Article 1 and title, `pbu.txt` (Pashto) Article 1, `hin.txt` Article 1. The corpus Urdu writes
hamza-on-yeh as U+06CC + U+0654 (`ہویٔے`); kept as is.

## What rendered correctly (tested here 2026-10-24, looked at the frames)

- Noto Nastaliq Urdu 400 and 700, Gulzar, Noto Naskh 700, Noto Sans Arabic 900, Vazirmatn 900: letters join, RTL order
  correct, wrapping breaks between words.
- **Per-word `<span style="display:inline-block">` keeps the joins** (each word is shaped on its own; words do not join
  across spaces anyway). Animating opacity / y / `filter: blur()` per word: mid-animation frame of the draft render
  showed a blurred word still fully joined.
- **Splitting a word into one span per letter breaks the joins** (letters showed in isolated forms). Never do it.
- Pashto in Noto Naskh at 90 px (zoomed crop): ring under ټ and ړ, tail on ۍ all visible. Code points checked:
  U+067C, U+0693, U+06CD.
- Pashto in Noto Nastaliq: ring under ړ visible; ټ and ۍ shapes were not clear enough to confirm at 90 px ->
  **unverified**, so the block uses Naskh for Pashto.
- U+06CC + U+0654 (`ہویٔے`) and U+0626 (`ہوئے`, same word with the code point substituted) rendered identically in Noto
  Nastaliq. r12a notes U+0626 is the de facto standard in Urdu and that U+06CC+U+0654 is an alternative strategy
  (https://r12a.github.io/scripts/arab/ur-characters.html, read 2026-10-24).
- Hindi in Noto Sans Devanagari 700 and Mukta Bold: conjuncts and matras correct (क्ष-type conjuncts, ों, ं).

## Line height (measured)

Noto Nastaliq 700, 60 px, Article 1 sentence wrapped to 2 lines, box outline, white ink pixels counted outside the box:

| line-height | ink above box | ink below box |
| --- | --- | --- |
| 1.6 | 6 px | 11 px |
| 1.8 | 0 px | 5 px |
| 2.0 | 0 px | 0 px |
| 2.2 | 0 px | 0 px |

At 1.2 with `overflow: hidden` the second line was cut off. So: Nastaliq `line-height: 2.0` (2.2 for safety with
taller words); never `overflow: hidden` on a Nastaliq box. Naskh 1.7 and Devanagari 1.5 looked clean in the
snapshots (not pixel-measured). Font extremes (head yMax/yMin): Noto Nastaliq +1.808 / -1.382 em, so single tall
glyphs can still poke out: the block root carries `data-layout-allow-overflow`.

## Word spacing (seen in snapshots)

- Noto Nastaliq: the space after non-joining letters (د, ر) looks almost absent: `د بشر` looked like one word.
  `word-spacing: 0.25em` made it clearly two words. Block default: 0.25em.
- Gulzar tucked `اور` against the next word even with `word-spacing: 0.2em`. Prefer Noto Nastaliq for captions.

## Mixed Urdu + Latin + numbers (tested)

- Raw `... ۱۹۴۸ — UDHR 1948 — 0300-1234567` in an RTL div: the bidi algorithm split and reordered the run, the phone
  number broke across lines. Wrapping each Latin/number run in `<bdi dir="ltr" style="white-space:nowrap">` fixed it.
- In the per-word block, two separate LTR spans (`UDHR`, `1948`) showed as `1948 UDHR`: atomic inline-blocks in an RTL
  line are laid out right-to-left. Fix in `urdu_captions.py`: consecutive non-Arabic words go into ONE
  `<span dir="ltr">`. Re-rendered: `UDHR 1948` correct, at the start (right side) of the line.
- Latin inside a Nastaliq line uses the Nastaliq font's own Latin glyphs (serif look).
- Urdu digits `۱۰؍دسمبر ۱۹۴۸` rendered in order. Sanah sign U+0601 must be typed BEFORE the digits
  (r12a, same page: example `؁۲۰۰۴ء`); typed after them (as in the corpus) it showed as a stray sweep. The r12a example
  rendered with the sweep under the digits in Noto Naskh and Noto Nastaliq.

## Encoding pitfalls (sourced)

- Urdu small yeh is U+06CC ی, large yeh U+06D2 ے; U+064A ي may be found in data but is incorrect for Urdu
  (SIL, "Notes on some Unicode Arabic characters", https://static-scripts.sil.org/cms/sites/nrsi/download/arabicletterusagenotes/ArabicLetterUsageNotes.pdf, read 2026-10-24).
- Urdu kaf is U+06A9 ک; کھ = U+06A9 + U+06BE (r12a page above).
- Presentation-form code points (U+FB50-FDFF, U+FE70-FEFF) bypass shaping: `urdu_captions.py --check` flags them
  (rule from the Unicode block ranges; flagged, not auto-fixed).

## Block and tool

- `library/tools/urdu_captions.py spec.json out.html` writes the caption scene; `--check spec.json` checks every
  character against the line's font cmap and flags U+064A/U+0643 in Urdu lines. It never edits the text.
- `library/blocks/urdu-captions.html` (+ `urdu-captions.json`, the spec it was built from): 1080x1920, 13 s demo,
  bottom veil, Nastaliq 700 74 px lh 2.0, per-word blur/rise reveal (0.12 s stagger), gold accent (`*word`), Pashto line
  in Naskh, Hindi line in Devanagari, optional LTR sub line. `check --json`: ok (only warning: first frame empty,
  because the demo has no title at 0 s). Draft render 13.000 s.

## Roman Urdu <-> Urdu script

No converter was tested. Leads found 2026-10-24 (`agent-reach web search`), all tiny/unmaintained, **unverified**:
github.com/zohaibadnan137/Urduify (2 stars), github.com/code-mj12/Roman-to-Urdu-Transliteration (2 stars),
github.com/Tehseen-Ajmal/Transliterater (0 stars), github.com/Anas1108/Transliteration-RomantoUrdu-And-ViceVersa (uses
`urduhack`). Roman Urdu spelling is not standard, so a converter can pick the wrong letter (e.g. س ص ث are all pronounced /s/ in Urdu: r12a ur-characters page, read 2026-10-24).
Rule: get Urdu-script captions from the client (or the owner) and show them the rendered frame to confirm; never
write Urdu-script words ourselves from Roman Urdu without that confirmation.
