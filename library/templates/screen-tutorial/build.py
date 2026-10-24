# Assemble the FireCraft whitelist tutorial: speed-fit recording segments to VO lines, place VO + clicks, write index.html.
import json, subprocess, os
D = os.path.dirname(os.path.abspath(__file__))
REC = f"{D}/run3/recording.mp4"
EV = json.load(open(f"{D}/run3/events.json"))
TUT = f"{D}/tut"
VO = [f"{D}/vo/ref.wav"] + [f"{D}/vo/c7/{i:03d}.wav" for i in range(11)]
over = json.load(open(f"{D}/vo/override.json")) if os.path.exists(f"{D}/vo/override.json") else {}
VO = [over.get(str(i), p) for i, p in enumerate(VO)]

def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                capture_output=True, text=True).stdout)

vl = [dur(p) for p in VO]
# (rec start, rec end) per VO line 2..12; a single number = freeze on that frame
SEG = [(0.3, 8.0), (8.0, 11.6), (11.6, 24.7), (28.0, 33.9), 34.0, (34.0, 40.6), (40.6, 47.5), (47.5, 53.0),
       (53.0, 59.2), (59.2, 61.0), (61.0, 66.2)]
LEAD, GAP = 0.25, 0.45
TITLE = max(vl[0] + 1.0, 4.5)

chains, outs, t = [], [], TITLE
vo_at = [0.5]
plan = []
for k, s in enumerate(SEG):
    need = LEAD + vl[k + 1] + GAP
    if isinstance(s, (int, float)):
        d = need
        chains.append(f"[0:v]trim=start={s}:duration=0.04,setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration={d},trim=duration={d}[s{k}]")
        plan.append(dict(rec=(s, s), out=t, speed=None, d=d))
    else:
        a, b = s; L = b - a
        speed = min(max(L / need, 0.85), 3.0)
        d = max(L / speed, need)
        chains.append(f"[0:v]trim={a}:{b},setpts=(PTS-STARTPTS)/{speed:.4f},tpad=stop_mode=clone:stop_duration={d},trim=duration={d}[s{k}]")
        plan.append(dict(rec=(a, b), out=t, speed=speed, d=d))
    vo_at.append(t + LEAD)
    outs.append(f"[s{k}]"); t += d
SCREEN_END = t
END = 4.0
TOTAL = round(SCREEN_END + END, 3)

graph = ";".join(chains) + ";" + "".join(outs) + f"concat=n={len(outs)}:v=1:a=0,fps=30,format=yuv420p[v]"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", REC, "-filter_complex", graph, "-map", "[v]", "-an", "-c:v", "libx264",
                "-crf", "16", "-preset", "medium", f"{TUT}/assets/screen.mp4"], check=True)

# VO: each line placed at its time (numpy, not adelay), one wav, loudnorm -16
import numpy as np, soundfile as sf
SR = 44100
buf = np.zeros(int((TOTAL + 1) * SR))
for p, at in zip(VO, vo_at):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
    x = np.frombuffer(raw, np.float32)
    i = int(at * SR); buf[i:i + len(x)] += x[: len(buf) - i]
sf.write(f"{D}/vo_raw.wav", buf, SR)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{D}/vo_raw.wav", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", str(SR),
                f"{TUT}/assets/vo.wav"], check=True)

# clicks: map recording times through the plan
clicks = []
for e in EV["events"]:
    if e["type"] not in ("click", "fakeclick"):
        continue
    for p in plan:
        a, b = p["rec"]
        if p["speed"] and a <= e["t"] < b:
            clicks.append(round(p["out"] + (e["t"] - a) / p["speed"], 3))
            break

def out_t(rec_t):
    for p in plan:
        a, b = p["rec"]
        if p["speed"] and a <= rec_t < b:
            return p["out"] + (rec_t - a) / p["speed"]

steps = [(TITLE, plan[3]["out"], "STEP 1", "Account banayein"),
         (plan[3]["out"], plan[10]["out"], "STEP 2", "Form bharein"),
         (plan[10]["out"], SCREEN_END, "STEP 3", "Status dekhein")]
hl = [  # highlight boxes (video px) when the voice names the thing
    dict(id="hl-ign", start=plan[4]["out"] + 0.3, end=plan[4]["out"] + plan[4]["d"] - 0.1, x=372, y=446, w=592, h=136),
    dict(id="hl-rules", start=out_t(50.2), end=plan[7]["out"] + plan[7]["d"] - 0.1, x=372, y=624, w=252, h=40),
]
json.dump(dict(title=TITLE, total=TOTAL, screen_end=SCREEN_END, vo_at=vo_at, vl=vl, plan=plan, clicks=clicks, steps=steps,
               hl=hl), open(f"{D}/timing.json", "w"), indent=1)

R = lambda v: f"{v:.3f}"
click_tags = "\n".join(
    f'      <audio id="click{i}" class="clip" src="assets/sfx/mouse-click.mp3" data-start="{R(c - 0.012)}" data-duration="0.096" '
    f'data-track-index="{4 + i % 2}" data-volume="0.55"></audio>' for i, c in enumerate(clicks))
step_tags = "\n".join(
    f'      <div id="step{i + 1}" class="clip step" data-start="{R(a)}" data-duration="{R(b - a)}" data-track-index="6">'
    f'<span class="num">{n}</span><span class="lbl">{l}</span></div>' for i, (a, b, n, l) in enumerate(steps))
hl_tags = "\n".join(
    f'      <div id="{h["id"]}" class="clip hl" data-start="{R(h["start"])}" data-duration="{R(h["end"] - h["start"])}" data-track-index="7" '
    f'style="left:{h["x"]}px;top:{h["y"]}px;width:{h["w"]}px;height:{h["h"]}px"><div class="ring"></div></div>' for h in hl)
info_at = vo_at[11]
hl_tags += (f'\n      <div id="info" class="clip info" data-start="{R(info_at)}" data-duration="{R(SCREEN_END - info_at)}" data-track-index="8">'
            '<span class="big">24–48</span><span class="sm">ghante mein review</span></div>')
hl_js_extra = f'      tl.from("#info .big, #info .sm", {{ y: 30, opacity: 0, duration: 0.45, stagger: 0.1, ease: "back.out(1.8)" }}, {R(info_at + 0.1)});'
step_js = "\n".join(
    f'      tl.from("#step{i + 1} .num, #step{i + 1} .lbl", {{ x: -40, opacity: 0, duration: 0.45, stagger: 0.08, ease: "power3.out" }}, {R(a + 0.1)});'
    for i, (a, b, n, l) in enumerate(steps))
hl_js = "\n".join(
    f'      tl.fromTo("#{h["id"]} .ring", {{ scale: 1.25, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2)" }}, {R(h["start"])});'
    for h in hl)

html = open(f"{D}/index.tpl.html").read()
for k, v in dict(TOTAL=R(TOTAL), TITLE=R(TITLE), SCREEN_START=R(TITLE), SCREEN_DUR=R(SCREEN_END - TITLE),
                 END_START=R(SCREEN_END), END_DUR=R(END), CLICKS=click_tags, STEPS=step_tags, HLS=hl_tags,
                 STEP_JS=step_js, HL_JS=hl_js + "\n" + hl_js_extra, MUSIC_DUR=R(TOTAL), FADE_START=R(SCREEN_END - 0.6)).items():
    html = html.replace("{{" + k + "}}", v)
open(f"{TUT}/index.html", "w").write(html)
print(json.dumps(dict(title=TITLE, total=TOTAL, clicks=len(clicks),
                      plan=[(p["rec"], round(p["out"], 2), p["speed"] and round(p["speed"], 2), round(p["d"], 2)) for p in plan]), indent=0))
