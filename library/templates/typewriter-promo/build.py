# FireCraft SMP typewriter video: every line is text read on www.firecraft.fun or in the admin announcement (2026-10-25).
# Per-character reveal on the GSAP timeline with seeded human jitter (skill #408), one caret per line, typing sounds
# pre-mixed with numpy (one wav instead of hundreds of <audio> clips), small bell when a card finishes.
import json, random, subprocess, html, os
import numpy as np, soundfile as sf

D = os.path.dirname(os.path.abspath(__file__))
P = f"{D}/proj"
rng = random.Random(25)

# [[x]] = accent colour, {{x}} = red. kind: k = kicker (appears instantly), h = headline (typed), s = sub (typed)
CARDS = [
    dict(id="c-title", lines=[("k", "PRIVATE LIFESTEAL SMP — APPLY FREE"), ("h", "FIRE[[CRAFT]] SMP")], logo=True, hold=2.0),
    dict(id="c-hearts", lines=[("k", "LIFESTEAL MECHANICS"), ("h", "You Start with {{10 Hearts}}"),
                               ("s", "Kill a player and steal their heart. Die and lose one.")], hold=2.0),
    dict(id="c-elim", lines=[("k", "EVERY FIGHT HAS STAKES"), ("h", "{{0 Hearts}} = Eliminated"),
                             ("s", "Craft Heart Crystals before it's too late.")], hold=2.0),
    dict(id="c-powers", lines=[("k", "11 CUSTOM POWERS"), ("h", "Spin the [[Power Wheel]]"), ("s", "on first login.")],
         powers=["Fire", "Ice", "Wind", "Dark", "Lightning", "Trader", "Rift", "Warden", "Wither", "Dragon", "Gravity"], hold=2.1),
    dict(id="c-mobs", lines=[("k", "63 TAMEABLE MOBS"), ("h", "Level them up to [[100]]"),
                             ("s", "and bring up to 3 into battle.")], hold=2.0),
    dict(id="c-gear", lines=[("k", "GEAR"), ("h", "[[5]] Armor Sets"), ("h", "[[3]] Legendary Weapons")], hold=2.0),
    dict(id="c-free", lines=[("k", "JOINING"), ("h", "100% FREE"), ("s", "No payment ever.")], hold=1.8),
    dict(id="c-s2", lines=[("k", "SEASON 2"), ("h", "Sun 25 Oct · [[2:00 PM]] PKT"), ("s", "Pehla 1 ghanta PvP off")], hold=2.1),
    dict(id="c-end", lines=[("k", "⚡ APPLY FOR WHITELIST"), ("h", "[[www.firecraft.fun]]"),
                            ("s", "Staff reviews within 24–48 hours.")], logo=True, hold=3.6),
]
CPS = {"h": 0.075, "s": 0.042}  # seconds per character (headline slower, sub faster)


def parse(s):
    """-> list of (char, cls)"""
    out, i, cls = [], 0, ""
    while i < len(s):
        if s.startswith("[[", i): cls = "acc"; i += 2; continue
        if s.startswith("{{", i): cls = "red"; i += 2; continue
        if s.startswith("]]", i) or s.startswith("}}", i): cls = ""; i += 2; continue
        out.append((s[i], cls)); i += 1
    return out


t = 0.6  # first card: logo + kicker visible at frame 0, typing starts at 0.6
sets, keys, bells, markup, js = [], [], [], [], []
card_spans = []
for ci, c in enumerate(CARDS):
    c_start = 0 if ci == 0 else t - 0.6
    rows, carets = [], []
    lt = c_start + (0.6 if ci == 0 else 0.35)
    for li, (kind, text) in enumerate(c["lines"]):
        lid = f"{c['id']}-l{li}"
        if kind == "k":
            rows.append(f'<div class="k" id="{lid}">{html.escape(text)}</div>')
            js.append(f'tl.from("#{lid}", {{ opacity: 0, x: -20, duration: 0.3, ease: "power2.out" }}, {lt - 0.3 if ci else 0:.3f});' if ci else "")
            continue
        chars = parse(text)
        spans = []
        for k, (ch, cls) in enumerate(chars):
            cid = f"{lid}-{k}"
            spans.append(f'<span id="{cid}" class="ch {cls}">{"&nbsp;" if ch == " " else html.escape(ch)}</span>')
            gap = CPS[kind] * rng.uniform(0.6, 1.45)
            if ch == " ": gap *= 1.35
            if ch in ".,:·—": gap += 0.12
            lt += gap
            sets.append((cid, lt))
            if ch != " ": keys.append((lt, kind))
        cid = f"{lid}-caret"
        rows.append(f'<div class="{kind}" id="{lid}">{"".join(spans)}<i class="caret" id="{cid}"></i></div>')
        carets.append((cid, sets[-len(chars)][1] - 0.05, lt))
        lt += 0.28
    # caret: shown while its line types, blinks after the last line until the card ends
    end_type = lt
    card_end = end_type + c["hold"]
    for j, (cid, a, b) in enumerate(carets):
        js.append(f'tl.set("#{cid}", {{ opacity: 1 }}, {a:.3f});')
        if j < len(carets) - 1:
            js.append(f'tl.set("#{cid}", {{ opacity: 0 }}, {b + 0.2:.3f});')
        else:
            n = max(1, int((card_end - b - 0.3) / 0.5))
            js.append(f'tl.to("#{cid}", {{ opacity: 0, duration: 0.25, ease: "steps(1)", repeat: {n * 2 - 1}, yoyo: true }}, {b + 0.25:.3f});')
    extra = ""
    if c.get("powers"):
        icons = []
        pt = end_type - 0.1
        for pi, name in enumerate(c["powers"]):
            pid = f"pw-{name.lower()}"
            icons.append(f'<div class="pw" id="{pid}"><img src="assets/powers/{name.lower()}.jpg" alt="{name} power" />'
                         f'<span id="{pid}-n">{name}</span></div>')
            js.append(f'tl.from("#{pid}", {{ scale: 0.4, opacity: 0, y: 30, duration: 0.32, ease: "back.out(2.2)" }}, {pt:.3f});')
            keys.append((pt + 0.02, "s"))
            pt += 0.16
        extra = f'<div class="powers">{"".join(icons)}</div>'
        card_end = max(card_end, pt + 1.4)
    if c.get("logo"):
        extra = '<img class="biglogo" id="%s-logo" src="assets/logo-512.png" alt="FireCraft SMP logo" />' % c["id"] + extra
        if ci:
            js.append(f'tl.from("#{c["id"]}-logo", {{ scale: 0.7, opacity: 0, duration: 0.5, ease: "back.out(1.7)" }}, {c_start:.3f});')
    bells.append(end_type + 0.05)
    last = ci == len(CARDS) - 1
    if not last:
        js.append(f'tl.to("#{c["id"]} .inner", {{ y: -40, opacity: 0, duration: 0.3, ease: "power2.in" }}, {card_end - 0.3:.3f});')
    markup.append(f'<div id="{c["id"]}" class="clip card" data-start="{c_start:.3f}" data-duration="{card_end - c_start:.3f}" '
                  f'data-track-index="{1 + ci % 2}"><div class="inner">{extra}{"".join(rows)}</div></div>')
    card_spans.append((c["id"], round(c_start, 3), round(card_end, 3)))
    t = card_end + 0.6  # next card's typing starts 0.6 s after this card ends (c_start = t - 0.6 = card_end)

TOTAL = round(card_spans[-1][2], 3)
for cid, at in sets:
    js.append(f'tl.set("#{cid}", {{ display: "inline" }}, {at:.3f});')

# ---- typing sound track (numpy) ----
SR = 44100
def load(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32)
key = load(f"{P}/assets/sfx/keypress.mp3"); bell = load(f"{P}/assets/sfx/bell-small.mp3")
buf = np.zeros(int((TOTAL + 2) * SR), np.float32)
for at, kind in keys:
    r = rng.uniform(0.92, 1.1)  # small pitch variation by resampling
    k2 = np.interp(np.arange(0, len(key), r), np.arange(len(key)), key).astype(np.float32)
    g = rng.uniform(0.45, 0.75) * (1.0 if kind == "h" else 0.7)
    i = int(at * SR); buf[i:i + len(k2)] += g * k2[: len(buf) - i]
for at in bells:
    i = int(at * SR); buf[i:i + len(bell)] += 0.45 * bell[: len(buf) - i]
buf = buf / max(1e-6, np.abs(buf).max()) * 0.89
sf.write(f"{P}/assets/sfx/typing-track.wav", buf, SR)

tpl = open(f"{D}/index.tpl.html").read()
html_out = (tpl.replace("{{TOTAL}}", f"{TOTAL:.3f}").replace("{{CARDS}}", "\n      ".join(markup))
            .replace("{{JS}}", "\n      ".join(x for x in js if x)).replace("{{MUSIC_DUR}}", f"{TOTAL:.3f}")
            .replace("{{FADE}}", f"{TOTAL - 2.5:.3f}"))
open(f"{P}/index.html", "w").write(html_out)
json.dump(dict(total=TOTAL, cards=card_spans, keys=len(keys), bells=bells), open(f"{D}/timing.json", "w"), indent=1)
print(TOTAL, card_spans, len(keys))
