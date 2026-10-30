# Final audio mix (owner 2026-10-28: "music ki awaaz kam karo jab kuch bola ja raha ho, SFX aur music pro editor ki tarah
# manage karo, hype aur hook"). One wav for HyperFrames: VO + music bed with gain automation + level-matched SFX.
# - Music: -5 dB in pauses / intros (energy), -20 dB under speech (voice always on top); ducks in 60 ms, comes back over
#   350 ms, and does not pump up in gaps shorter than ~0.4 s (speech mask dilated 0.2 s). Skills #316/#317 (ducking).
# - SFX: each file scaled so its loudest 10 ms reaches a per-type target (impacts loudest, UI clicks quietest);
#   -3 dB when it lands on speech (except the reveal hits). Guide: "Har dialogue ke baad SFX mat lagana" (plan in build.py).
# - Master: loudnorm -15 LUFS, true peak -1.5 dB.
import json, subprocess
import numpy as np
SR = 48000


def load(p, ch=2):
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", str(ch), "-ar", str(SR), "-f", "f32le", "-"],
                                     capture_output=True).stdout, np.float32)
    return x.reshape(-1, ch).copy()


vo = load("assets/vo.wav")
bed = load("assets/bed_raw.wav")
N = max(len(vo), len(bed))
TOTAL = json.load(open("timing.json"))["total"]
N = int(TOTAL * SR)
mix = np.zeros((N, 2), np.float32)
mix[:min(N, len(vo))] += vo[:N]

# speech mask from the VO envelope (10 ms frames)
F = SR // 100
m = vo[:, 0]
env = np.array([np.sqrt((m[i:i + F] ** 2).mean()) for i in range(0, len(m) - F, F)])
db = 20 * np.log10(env + 1e-9)
speech = db > np.percentile(db[db > -70], 95) - 30
k = 20                                                      # dilate 0.2 s each side: no pumping in short gaps
sp = np.convolve(speech.astype(float), np.ones(2 * k + 1), "same") > 0
target = np.where(sp, -20.0, -5.0)
g = np.empty_like(target); cur = -5.0
for i, t in enumerate(target):                              # attack 60 ms down, release 350 ms up
    a = 1 - np.exp(-1 / (6 if t < cur else 35))
    cur += (t - cur) * a; g[i] = cur
gain = 10 ** (np.interp(np.arange(N) / SR, np.arange(len(g)) / 100, g, right=-5.0) / 20)
mix[:min(N, len(bed))] += bed[:N] * gain[:min(N, len(bed)), None]

TGT = {"impact-boom": -10, "sub-drop": -11, "impact-punch": -11, "record-scratch": -10, "tape-stop": -11, "glitch-medium": -13,
       "glitch-short": -15, "whoosh-fast-0.3s": -14, "swish-4": -15, "pop-high": -17, "bubble-pop": -17, "mouse-click": -18,
       "switch": -16, "error-buzz": -13, "ui-error-1": -13, "alarm": -16, "negative": -15, "magic-shimmer": -12, "sparkle": -15,
       "wink": -14, "game-coin": -16, "success-chime": -15, "typing-keyboard-fast": -24, "thruster": -14, "riser-2s": -14,
       "riser-4s": -13, "boing": -13, "badumtss": -11, "fall": -15, "blip-up": -17, "trombone": -12, "plop": -17, "cricket": -14, "game-levelup": -16, "punch-medium": -11, "punch-heavy": -11, "swish-1": -15, "whoosh-up-0.6s": -15}
REVEAL = {"impact-boom", "record-scratch", "sub-drop"}
plan = json.load(open("sfx_plan.json"))
cache = {}
for e in plan:
    name, st, d, hit = e["name"], e["start"], e["dur"], e["hit"]
    if name not in TGT or st >= TOTAL:
        continue
    if name not in cache:
        cache[name] = load(f"assets/sfx/{name}.mp3")
    x = cache[name][:int(d * SR)]
    xm = x.mean(1)
    pk = 20 * np.log10(max(np.sqrt((xm[i:i + F] ** 2).mean()) for i in range(0, max(1, len(xm) - F), F)) + 1e-9)
    gdb = TGT[name] - pk
    fi = int(hit * 100)
    if name not in REVEAL and 0 <= fi < len(sp) and sp[fi]:
        gdb -= 3
    x = x * 10 ** (gdb / 20)
    i0 = int(st * SR); i1 = min(N, i0 + len(x))
    mix[i0:i1] += x[:i1 - i0]
    e["gain_db"] = round(float(gdb), 1)
json.dump(plan, open("sfx_plan.json", "w"), indent=0)
raw = mix.astype(np.float32).tobytes()
r = subprocess.run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-af",
                    "loudnorm=I=-15:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], input=raw, capture_output=True)
L = json.loads(r.stderr.decode()[r.stderr.decode().rindex("{"):])
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-af",
                f"loudnorm=I=-15:TP=-1.5:LRA=11:measured_I={L['input_i']}:measured_TP={L['input_tp']}:measured_LRA={L['input_lra']}:"
                f"measured_thresh={L['input_thresh']}:offset={L['target_offset']}:linear=true,alimiter=limit=0.84:attack=2:release=50:level=false,aresample=48000",
                "-c:a", "pcm_s16le", "assets/mix.wav"], input=raw, check=True)
print("mix", round(N / SR, 2), "sfx", len(plan))
