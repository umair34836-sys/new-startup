#!/home/user/tools/perc-venv/bin/python
# Usage: /home/user/tools/perc-venv/bin/python library/tools/music_fit.py TRACK OUT.wav --length 30
#            [--drop-at 7.4] [--src-drop 52.1] [--end resolve|fade|cut] [--fade 2.5] [--lufs -14] [--check]
# Cuts or stitches a music track to an EXACT length the way an editor does it, instead of trimming + fading mid-phrase:
#   * every internal join is downbeat -> downbeat (beat grid from listen.py / catalogue.json), snapped to the nearest
#     onset (+-50 ms) and joined with a 40 ms equal-power crossfade that ends just before the incoming transient
#     (skills #280-#283, #360: the downbeat's hit masks the splice);
#   * jumps are whole phrases (4 bars) when they fit, else whole bars (#361);
#   * --drop-at T: the track's main drop (catalogue main_drop_s, or --src-drop) lands at output time T, e.g. on the
#     logo reveal; if the track's drop comes too early, the 4-bar build before it is repeated (#362 look-alike joins);
#   * --end resolve: keep the composer's real ending (ending_from_s .. end of file) and hide the edit in the middle
#     (#363 backtime the ending). Tracks without a natural ending (loops, fade-outs) fall back to "hit": stop on a
#     downbeat and let it ring out over 1.5-2.5 s. --end fade: fade over the last --fade s (#365/#366). --end cut: hard cut.
#   * --check runs listen.py on the result and reports how far each join is from the nearest detected beat.
# Output: WAV 48 kHz stereo (+ OUT.json plan). Tested on real tracks: see library/research/music-for-video-tests.md.
import argparse, json, os, subprocess, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CATALOGUE = os.path.join(ROOT, "library", "music", "catalogue.json")
PY = "/home/user/tools/perc-venv/bin/python"
SR = 48000
XF = 0.040      # join crossfade (s)
PRE = 0.005     # crossfade ends this long before the incoming transient

ap = argparse.ArgumentParser()
ap.add_argument("track")
ap.add_argument("out")
ap.add_argument("--length", type=float, required=True)
ap.add_argument("--drop-at", type=float, help="output time where the track's drop must land")
ap.add_argument("--src-drop", type=float, help="source time of the drop (default: catalogue main_drop_s)")
ap.add_argument("--start", type=float, default=0.0, help="source start when no --drop-at (default 0 = the track's own start)")
ap.add_argument("--end", choices=["resolve", "fade", "cut"], default="resolve")
ap.add_argument("--fade", type=float, default=2.5, help="fade length for --end fade (s)")
ap.add_argument("--lufs", type=float, help="normalise the result to this integrated loudness (gain + -1 dBTP limiter)")
ap.add_argument("--check", action="store_true", help="re-measure the result with listen.py")
a = ap.parse_args()
L = a.length


def decode(path, ch=2, sr=SR):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vn", "-ac", str(ch), "-ar", str(sr), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, ch).astype(np.float64)


def analysis(path):
    """catalogue entry if the track is catalogued, else listen.py + music_analysis.derive."""
    ap_ = os.path.abspath(path)
    if os.path.exists(CATALOGUE):
        for e in json.load(open(CATALOGUE)):
            if e.get("file") and os.path.abspath(os.path.join(ROOT, e["file"])) == ap_:
                return e, "catalogue.json"
    tmp = os.path.join("/tmp", "music_fit_" + os.path.basename(path) + ".json")
    if not os.path.exists(tmp):
        subprocess.run([PY, os.path.join(HERE, "listen.py"), path, "--no-words", "--out", tmp], check=True,
                       capture_output=True)
    rep = json.load(open(tmp))
    sys.path.insert(0, HERE)
    from music_analysis import derive
    d = derive(path, rep)
    rh = rep["rhythm"]
    e = {"duration_s": rep["duration_s"], "bpm": rh["bpm"], "bar_s": rh["bar_s_4_4"],
         "downbeats_s": rh["downbeats_s_estimated"], **d}
    return e, "listen.py"


info, src_kind = analysis(a.track)
x = decode(a.track)
dur = len(x) / SR
bar = float(info["bar_s"])
dbs = np.array([d for d in info["downbeats_s"] if d < dur - 0.05], float)
if len(dbs) < 4:
    sys.exit("too few downbeats for a bar-accurate fit (free-time music?): trim by hand with a fade")

# snap downbeats to the nearest onset peak (+-50 ms) so the crossfade ends right before the transient
import librosa  # noqa: E402
y22 = librosa.resample(x.mean(1), orig_sr=SR, target_sr=22050)
oenv = librosa.onset.onset_strength(y=y22, sr=22050, hop_length=256)
ot = librosa.frames_to_time(np.arange(len(oenv)), sr=22050, hop_length=256)


def snap(t):
    m = (ot >= t - 0.05) & (ot <= t + 0.05)
    if not m.any():
        return float(t)
    i = np.where(m)[0][np.argmax(oenv[m])]
    return float(ot[i]) - PRE


phrase = 4 * bar


def plan():
    """list of (src_a, src_b) segments whose lengths sum to L; joins are downbeats (except the first start)."""
    segs, notes = [], []
    natural = info.get("ending") in ("natural", "soft-tail") and info.get("ending_from_s")
    end_mode = a.end
    if end_mode == "resolve" and not natural:
        end_mode = "hit"
        notes.append(f"track ending is '{info.get('ending')}' (no natural ending): resolve -> hit (stop on a downbeat + ring-out)")
    # ---- head: material before the anchor (drop) ----
    if a.drop_at is not None:
        D = a.src_drop if a.src_drop is not None else info.get("main_drop_s")
        if D is None:
            sys.exit("track has no measured drop (main_drop_s is null): pass --src-drop <source s>")
        D = float(dbs[np.argmin(abs(dbs - D))])
        T = a.drop_at
        if D >= T:
            segs.append([D - T, D])
            notes.append(f"head: source {D - T:.2f}-{D:.2f} s (drop at source {D:.2f} s lands at {T:.2f} s)")
        else:
            J = phrase
            while D + J < T:
                J += phrase
            if D - J < dbs[0] - 0.01:  # not enough build before the drop for a 4-bar repeat: use bars
                J = bar
                while D + J < T:
                    J += bar
            b0 = D - J if D - J >= dbs[0] - 0.01 else float(dbs[0])
            s = D + (D - b0) - T
            segs += [[s, D], [b0, D]]
            notes.append(f"head: source {s:.2f}-{D:.2f} s, then the {D - b0:.2f} s build before the drop repeats "
                         f"({b0:.2f}-{D:.2f} s) so the drop lands at {T:.2f} s")
        anchor = D
        rest = L - T
    else:
        anchor, rest = a.start, L
    # ---- tail ----
    if end_mode == "resolve":
        E0 = float(info["ending_from_s"])
        E = float(dbs[np.argmin(abs(dbs - E0))])
        # lead into the ending with a full phrase when there is room (the ending then starts on a phrase line)
        tail_len = dur - E
        body = rest - tail_len
        if body < 0:
            # not even the ending fits: start the ending later and fade the overflow
            notes.append("ending longer than the space after the anchor: its tail is shortened with a fade")
            segs.append([anchor, anchor + rest])
            return segs, notes, "fade-tail"
        fill(segs, anchor, body, E, notes)
        segs.append([E, dur])
        notes.append(f"ending: the track's own ending {E:.2f}-{dur:.2f} s ({tail_len:.2f} s)")
        return segs, notes, "resolve"
    if end_mode == "hit":
        ring = 2.0
        fill(segs, anchor, rest - ring, None, notes)
        b = segs[-1][1]
        segs.append([b, b + ring])
        notes.append(f"ending: stops on the downbeat at output {L - ring:.2f} s and rings out {ring:.1f} s")
        return segs, notes, "hit"
    fill(segs, anchor, rest, None, notes, exact=True)
    return segs, notes, end_mode


def fill(segs, start, need, stop_before, notes, exact=False):
    """append segments from `start` lasting ~`need` s, ending on a downbeat (unless exact) and, if `stop_before`
    is set, ending on a downbeat at or before it (the join into the ending). Loops back by whole phrases."""
    lim = (stop_before if stop_before is not None else dur - 0.5)
    cur, left = start, need
    first = True
    while True:
        avail = lim - cur
        if left <= avail + 1e-6:
            if exact:
                segs.append([cur, cur + left])
                return
            # end on a downbeat X with X - cur ~ left, and X a downbeat that can join into stop_before
            cand = dbs[(dbs > cur + 0.5 * bar) & (dbs <= lim + 0.01)]
            if stop_before is not None:
                target = cur + left
                # join X -> stop_before: X must be a downbeat; pick X nearest to target
                X = float(cand[np.argmin(abs(cand - target))]) if len(cand) else cur
                segs.append([cur, X])
                err = (X - cur) - left
                ERR.append(err)
                return
            X = float(cand[np.argmin(abs(cand - (cur + left)))]) if len(cand) else cur + left
            segs.append([cur, X])
            ERR.append((X - cur) - left)
            return
        # not enough track left: play to the last downbeat before the limit, jump back by whole phrases
        endb = dbs[dbs <= lim + 0.01]
        X = float(endb[-1])
        if X - cur < bar:
            sys.exit("track too short to loop cleanly")
        segs.append([cur, X])
        left -= X - cur
        back = X - phrase * max(1, int((X - start) // phrase))
        back = float(dbs[np.argmin(abs(dbs - back))])
        notes.append(f"loop: {X:.2f} s jumps back to {back:.2f} s ({(X - back) / bar:.0f} bars)")
        cur = back
        first = False


ERR = []  # bar-grid leftovers (s): + = the plan is that much too long, - = too short


def absorb(segs, notes):
    """the bar grid leaves up to half a bar too much/too little. Without --drop-at the head start is the free edge
    (start a little later into the track, with the 0.35 s fade-in); with --drop-at (or when the head is already at 0)
    it is taken from the end: trim the last segment (its tail gets the end fade) or pad silence after the ending."""
    err = sum(ERR)
    if abs(err) < 0.005:
        return 0.0
    if err > 0:
        sa, sb = float(segs[-1][0]), float(segs[-1][1])
        tail = x[int((sb - err) * SR):int(sb * SR)]
        quiet = tail.size == 0 or 20 * np.log10(max(1e-9, float(np.sqrt(np.mean(tail ** 2))))) < -45
        if quiet or a.drop_at is not None or segs[0][0] + err >= segs[0][1] - 1:
            segs[-1][1] = sb - err
            notes.append(f"bar grid left {err:+.2f} s: the last {err:.2f} s of the track's tail are trimmed"
                         + (" (they are below -45 dBFS)" if quiet else ""))
        else:
            segs[0][0] += err
            notes.append(f"bar grid left {err:+.2f} s: the start moves {err:.2f} s into the track")
        return 0.0
    notes.append(f"bar grid left {err:+.2f} s: {-err:.2f} s of silence after the ending")
    return -err


segs, notes, end_kind = plan()
pad_s = absorb(segs, notes)
merged = [segs[0]]  # a segment that starts where the previous one stopped is not an edit: merge it
for sg in segs[1:]:
    if abs(float(sg[0]) - float(merged[-1][1])) < 0.02:
        merged[-1] = [merged[-1][0], sg[1]]
    else:
        merged.append(sg)
segs = merged

# ---- render ----
n = int(round(L * SR))
out = np.zeros((n, 2))
pos = 0
xf = int(XF * SR)
for k, (sa, sb) in enumerate(segs):
    if sa == "pad":
        continue
    sa_s, sb_s = float(sa), float(sb)
    if k > 0:  # join: incoming segment starts on a snapped downbeat; crossfade ends at it
        sa_s = snap(sa_s)
    if k < len(segs) - 1 and segs[k + 1][0] != "pad":
        sb_s = snap(sb_s)
    i0, i1 = int(round(sa_s * SR)), int(round(sb_s * SR))
    seg = x[i0:i1].copy()
    if k == 0 and sa_s > 0.05:
        f = min(len(seg), int(0.35 * SR))  # 0.3-0.5 s BGM fade-in when not starting at the track's start (#366)
        seg[:f] *= np.sin(np.linspace(0, np.pi / 2, f))[:, None] ** 2
    if k > 0 and pos >= xf:
        pre = x[max(0, i0 - xf):i0]
        w = np.linspace(0, np.pi / 2, len(pre))[:, None]
        out[pos - len(pre):pos] = out[pos - len(pre):pos] * np.cos(w) + pre * np.sin(w)
    m = min(len(seg), n - pos)
    out[pos:pos + m] = seg[:m]
    pos += m
    if pos >= n:
        break
joins_out, t = [], 0.0
for k, (sa, sb) in enumerate(segs[:-1]):
    if sa == "pad":
        continue
    t += float(sb) - float(sa)
    joins_out.append(round(t, 3))
if end_kind == "hit":
    r = int(2.0 * SR)
    out[n - r:] *= (np.linspace(1, 0, r) ** 2)[:, None]
elif end_kind in ("fade", "fade-tail"):
    # start the fade on a downbeat (the source downbeat that plays near L - fade), so it begins with a bar
    fl = min(a.fade, L / 3)
    sa, sb = float(segs[-1][0]), float(segs[-1][1])
    t_last0 = L - pad_s - (sb - sa)  # output time where the last segment starts
    cand = [t_last0 + (d - sa) for d in dbs if sa < d < sb]
    near = [c for c in cand if abs((L - c) - fl) <= bar / 2 and L - c >= 1.0]
    if near:
        fl = L - min(near, key=lambda c: abs((L - c) - fl))
        notes.append(f"fade starts on the downbeat at output {L - fl:.2f} s ({fl:.2f} s long)")
    r = int(fl * SR)
    out[n - r:] *= np.cos(np.linspace(0, np.pi / 2, r))[:, None]
else:
    trimmed = any("are trimmed" in t and "below -45" not in t for t in notes)
    f = int((0.8 if trimmed else 0.010) * SR)  # a trimmed natural tail gets a short fade instead of a click
    e_ = n - int(round(pad_s * SR))
    out[e_ - f:e_] *= np.cos(np.linspace(0, np.pi / 2, f))[:, None]
out[:int(0.003 * SR)] *= np.linspace(0, 1, int(0.003 * SR))[:, None]

gain_db = 0.0
if a.lufs is not None:
    import pyloudnorm as pyln
    cur = pyln.Meter(SR).integrated_loudness(out)
    gain_db = a.lufs - cur
    out *= 10 ** (gain_db / 20)
import wave  # noqa: E402
tmpw = a.out + ".tmp.wav"
with wave.open(tmpw, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(out, -1, 1) * 32767).astype("<i2").tobytes())
af = ["-af", "alimiter=limit=0.891:level=false"] if a.lufs is not None else []  # 0.891 = -1 dBFS
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmpw, *af, "-ar", str(SR), a.out], check=True)
os.remove(tmpw)
rep = {"track": a.track, "analysis": src_kind, "length": L, "bpm": info["bpm"], "bar_s": bar, "end": end_kind,
       "segments_src_s": [[round(float(p), 3) if p != "pad" else p for p in s] for s in segs],
       "joins_out_s": joins_out, "drop_at": a.drop_at, "notes": notes, "gain_db": round(gain_db, 2)}
print(f"music_fit: {os.path.basename(a.track)} -> {a.out}  {L:.2f} s, {info['bpm']} BPM (bar {bar:.3f} s), end '{end_kind}'")
for s in notes:
    print("  -", s)
print("  segments (source s):", rep["segments_src_s"])
print("  joins at output s:", joins_out)

if a.check:
    cj = a.out + ".listen.json"
    subprocess.run([PY, os.path.join(HERE, "listen.py"), a.out, "--no-words", "--out", cj], check=True, capture_output=True)
    lr = json.load(open(cj))
    beats = np.array(lr["rhythm"]["beats_s"])
    dbo = np.array(lr["rhythm"]["downbeats_s_estimated"])
    chk = []
    def phase_err(j):
        pre = beats[(beats > j - 4 * bar) & (beats < j - 0.05)]
        post = beats[(beats > j + 0.05) & (beats < j + 4 * bar)]
        if len(pre) < 3 or len(post) < 2:
            return None
        per = float(np.median(np.diff(pre)))
        pred = pre[-1] + per * np.round((post - pre[-1]) / per)
        return 1000 * float(np.median(abs(post - pred)))
    # tracker noise floor: the same measure at points with no edit (>= 1 bar from any join)
    probes = [t for t in np.arange(4 * bar, L - 4 * bar, bar) if all(abs(t - j) > bar for j in joins_out)]
    base = [v for v in (phase_err(t) for t in probes) if v is not None]
    rep_base = round(float(np.median(base)), 1) if base else None
    for j in joins_out:
        pre = beats[(beats > j - 4 * bar) & (beats < j - 0.05)]
        post = beats[(beats > j + 0.05) & (beats < j + 4 * bar)]
        ph = None
        if len(pre) >= 3 and len(post) >= 2:
            # continue the pre-join grid with the source beat period; how far are the detected post-join beats?
            per = float(np.median(np.diff(pre)))  # local period: the grid the listener has just heard
            pred = pre[-1] + per * np.round((post - pre[-1]) / per)
            ph = round(1000 * float(np.median(abs(post - pred))), 1)
        db_ = float(np.min(abs(beats - j))) if len(beats) else None
        chk.append({"join_s": j, "nearest_beat_ms": round(1000 * db_, 1) if db_ is not None else None,
                    "beat_phase_error_after_join_ms": ph})
        continue
        db_ = float(np.min(abs(beats - j))) if len(beats) else None
        chk.append({"join_s": j, "nearest_beat_ms": round(1000 * db_, 1) if db_ is not None else None,
                    "nearest_downbeat_ms": round(1000 * float(np.min(abs(dbo - j))), 1) if len(dbo) else None})
    if a.drop_at is not None and len(dbo):
        rep["drop_nearest_downbeat_ms"] = round(1000 * float(np.min(abs(dbo - a.drop_at))), 1)
        rep["drop_nearest_beat_ms"] = round(1000 * float(np.min(abs(beats - a.drop_at))), 1)
    rep["check"] = {"phase_error_no_edit_median_ms": rep_base, "bpm": lr["rhythm"]["bpm"], "beat_interval_cv": lr["rhythm"]["beat_interval_cv"],
                    "lufs": lr["loudness"]["integrated_lufs"], "true_peak_dbtp": lr["loudness"]["true_peak_dbtp_est"],
                    "clipped": lr["loudness"]["clipped_samples"], "duration_s": lr["duration_s"], "joins": chk,
                    "last_1s_rms_dbfs": round(20 * np.log10(max(1e-9, float(np.sqrt(np.mean(out[-SR:] ** 2))))), 1)}
    print("  check:", json.dumps(rep["check"]))
    if "drop_nearest_downbeat_ms" in rep:
        print(f"  drop at {a.drop_at} s: nearest detected beat {rep['drop_nearest_beat_ms']} ms, downbeat (phase estimate) {rep['drop_nearest_downbeat_ms']} ms")
json.dump(rep, open(os.path.splitext(a.out)[0] + ".json", "w"), indent=1)
