# GTA VO edit: best take of every line (retakes removed), dead air out. Spans are original-VO seconds; every boundary is
# moved to the quietest 10 ms within +-0.15 s; joins get 15 ms fades and a 0.25 s gap (#63 shorten, don't delete);
# pauses > 0.6 s inside a span drop to 0.35 s (#289 dialogue compression).
import json, subprocess, numpy as np
SR = 48000
SPANS = [(0.0, 29.3), (30.1, 32.6), (33.3, 35.9), (37.2, 40.6), (42.7, 52.6), (52.6, 60.5), (64.9, 68.1), (68.6, 80.1),
         (80.7, 105.0), (106.6, 128.2), (129.2, 131.2), (131.2, 139.8), (145.14, 158.7), (161.5, 204.2), (206.1, 212.5),
         (213.2, 226.6), (231.28, 237.1), (246.5, 249.6), (252.0, 255.6), (262.5, 266.6), (268.9, 273.6), (275.5, 279.8),
         (283.3, 287.6), (295.78, 302.04), (303.72, 306.44), (315.98, 320.6), (321.9, 323.6), (324.4, 335.74),
         (344.44, 346.6), (346.6, 349.62), (351.84, 354.32), (355.0, 367.6), (371.4, 380.1), (381.3, 390.5), (395.4, 404.6),
         (404.6, 412.5), (413.9, 453.2)]
a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", "in/vo.mp3", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                                 capture_output=True, check=True).stdout, np.float32).reshape(-1, 2)
mono = a.mean(1)
def rms(t):
    i = int(t * SR); return float(np.sqrt((mono[i:i + 480] ** 2).mean())) if i < len(mono) else 0.0
def quiet(t):
    c = np.arange(max(0, t - 0.15), t + 0.15, 0.005); return float(min(c, key=rms))
out, segmap, tcur, tmap = [], [], 0.0, []
fade = int(0.015 * SR)
for k, (s, e) in enumerate(SPANS):
    s2, e2 = quiet(s), quiet(e)
    piece = a[int(s2 * SR):int(e2 * SR)].copy()
    # compress inner pauses
    fr = 0.01; n = int(fr * SR); en = 20 * np.log10(np.sqrt((piece[:len(piece) // n * n].mean(1).reshape(-1, n) ** 2).mean(1)) + 1e-9)
    thr = np.percentile(en, 10) + 12
    keep = np.ones(len(en), bool); run = 0
    for i, q in enumerate(en < thr):
        run = run + 1 if q else 0
        if run > 35: keep[i] = False            # keep the first 0.35 s of any pause
    mask = np.repeat(keep, n); mask = np.concatenate([mask, np.ones(len(piece) - len(mask), bool)])
    piece = piece[mask]
    kept = np.nonzero(mask)[0][::480]                     # every 10 ms: original time -> new time
    tmap += [[round(s2 + i / SR, 3), round(tcur + j * 480 / SR, 3)] for j, i in enumerate(kept)]
    piece[:fade] *= np.linspace(0, 1, fade)[:, None]; piece[-fade:] *= np.linspace(1, 0, fade)[:, None]
    segmap.append([round(s2, 3), round(e2, 3), round(tcur, 3), round(tcur + len(piece) / SR, 3), int((~keep).sum())])
    out.append(piece); tcur += len(piece) / SR
    if k + 1 < len(SPANS):
        out.append(np.zeros((int(0.25 * SR), 2), np.float32)); tcur += 0.25
vo = np.concatenate(out)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-",
                "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", str(SR), "vo_cut.wav"], input=vo.tobytes(), check=True)
json.dump(segmap, open("vo_cut_map.json", "w")); json.dump(tmap, open("vo_tmap.json", "w"))
print("cut VO %.1f s from 453.5 s, %d spans" % (len(vo) / SR, len(SPANS)))
