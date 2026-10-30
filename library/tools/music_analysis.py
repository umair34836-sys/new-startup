# Shared analysis helpers for music_catalogue.py and music_fit.py (perc-venv python: numpy + ffmpeg).
# derive(): intro/drop/ending numbers from the 100 ms RMS envelope and listen.py's downbeat grid.
# The rules are written out in library/music/catalogue.md "Tag rules".
import subprocess
import numpy as np


def decode(path, sr=11025):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vn", "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32), sr


def env_db(x, sr, win=0.1):
    n = int(sr * win)
    k = len(x) // n
    r = np.sqrt(np.mean(x[: k * n].reshape(k, n) ** 2, axis=1))
    return 20 * np.log10(np.maximum(r, 1e-7))


def derive(path, rep):
    """ending / intro / drop numbers from the RMS envelope + listen.py downbeats."""
    x, sr = decode(path)
    e = env_db(x, sr)  # 10 per second
    dur = len(x) / sr
    rh = rep.get("rhythm", {})
    bpm = rh.get("bpm") or 0
    bar = rh.get("bar_s_4_4") or (240 / bpm if bpm else None)
    dbs = np.array(rh.get("downbeats_s_estimated") or [])
    out = {}
    lin = 10 ** (e / 20)

    def seg_db(t0, t1):
        i0, i1 = max(0, int(t0 * 10)), min(len(e), int(t1 * 10))
        return 20 * np.log10(max(np.sqrt(np.mean(lin[i0:i1] ** 2)), 1e-7)) if i1 > i0 else -140.0

    if bar and len(dbs) >= 4:
        bars = [seg_db(t, t + bar) for t in dbs]
        body = float(np.median(bars))
        p80 = float(np.percentile(bars, 80))
        out["body_bar_rms_db"] = round(float(body), 1)
        ff = next((float(t) for t, b in zip(dbs, bars) if b >= p80 - 4), None)
        out["first_full_s"] = round(ff, 2) if ff is not None else None
        best, bt = 0.0, None
        for i in range(2, len(dbs) - 2):
            rise = np.mean([seg_db(dbs[i], dbs[i] + 2 * bar)]) - np.mean([seg_db(dbs[i] - 2 * bar, dbs[i])])
            if rise > best:
                best, bt = rise, float(dbs[i])
        out["main_drop_s"] = round(bt, 2) if bt is not None and best >= 3 else None
        out["main_drop_rise_db"] = round(float(best), 1) if bt is not None and best >= 3 else None
    else:
        body = float(np.median(e[e > -80])) if (e > -80).any() else -80
        out["body_bar_rms_db"] = round(float(body), 1)
        out["first_full_s"], out["main_drop_s"], out["main_drop_rise_db"] = None, None, None
    # ending
    tail_end = float(np.mean(e[-3:])) if len(e) >= 3 else -140
    loud = np.where(e >= body - 6)[0]
    t_last = loud[-1] / 10 if len(loud) else 0.0
    last10 = e[-100:] if len(e) >= 100 else e
    # steady decline: count 1 s steps (in the last 10 s) that are lower than the step before
    steps = [float(np.mean(last10[i:i + 10])) for i in range(0, len(last10) - 9, 10)]
    falling = sum(1 for p, q in zip(steps, steps[1:]) if q < p - 0.5)
    if tail_end <= -45 and dur - t_last <= 6 and falling < 6:
        kind = "natural"
    elif falling >= 6 and steps and steps[0] - steps[-1] >= 10:
        kind = "fade-out"
    elif float(np.mean(e[-3:])) >= body - 8:
        kind = "abrupt"
    else:
        kind = "natural" if tail_end <= -45 else "soft-tail"
    out["ending"] = kind
    out["ending_tail_db"] = round(tail_end, 1)
    out["last_body_level_s"] = round(t_last, 2)
    if len(dbs):
        cand = dbs[dbs <= t_last + 0.05]
        out["ending_from_s"] = round(float(cand[-1]), 2) if len(cand) else None
    else:
        out["ending_from_s"] = None
    return out
