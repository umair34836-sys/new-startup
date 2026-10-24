#!/home/user/tools/perc-venv/bin/python
# Usage: /home/user/tools/perc-venv/bin/python library/tools/listen.py AUDIO_OR_VIDEO [--json] [--out report.json]
#        [--no-words] [--whisper-model small] [--bpm-hint 120]
# Turns a sound file (or a video's audio) into facts Claude can reason about, because Claude can't listen:
#   tempo + beat grid (librosa and essentia, with their agreement), estimated downbeats/bars (4/4 assumed),
#   onsets and the strongest hits, EBU R128 loudness (integrated + short-term curve, true-peak estimate),
#   sections from a self-similarity novelty curve, silences, speech/vocal activity (Silero VAD ONNX),
#   key (essentia KeyExtractor), mood descriptors, clipping / noise floor / mains hum / hiss report,
#   and Whisper words with timestamps when there is speech (uses the main venv's whisper if installed).
# Setup: bash library/tools/setup-specialist-a.sh   (venv /home/user/tools/perc-venv, models /home/user/tools/perc-models)
# Accuracy notes and limits: library/research/perception-tools.md
import argparse, json, os, subprocess, sys, tempfile
import numpy as np

MODELS = "/home/user/tools/perc-models"
MAIN_PY = "/home/user/tools/venv/bin/python"

ap = argparse.ArgumentParser()
ap.add_argument("inp")
ap.add_argument("--json", action="store_true", help="print the full JSON report to stdout after the summary")
ap.add_argument("--out", help="write the JSON report here")
ap.add_argument("--no-words", action="store_true", help="skip Whisper even when speech is found")
ap.add_argument("--whisper-model", default="small")
ap.add_argument("--vocals", action="store_true",
                help="also separate the vocal stem (MDX-Net Voc FT, ~0.7x real time) and report when singing/voice is present")
ap.add_argument("--bpm-hint", type=float, default=None, help="prior tempo for librosa (helps half/double errors)")
a = ap.parse_args()


def decode(path, sr, ch=1):
    cmd = ["ffmpeg", "-v", "error", "-i", path, "-vn", "-ac", str(ch), "-ar", str(sr), "-f", "f32le", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.float32)
    return x.reshape(-1, ch) if ch > 1 else x


def db(x, floor=-120.0):
    return float(max(floor, 20 * np.log10(max(float(x), 1e-12))))


def r(x, n=2):
    return float(round(float(x), n))


import librosa  # noqa: E402

SR = 22050
y = decode(a.inp, SR)
if y.size < SR // 2:
    sys.exit("audio shorter than 0.5 s or no audio stream")
dur = y.size / SR
rep = {"file": os.path.abspath(a.inp), "duration_s": r(dur, 3)}

# ---------- tempo and beats ----------
hop = 512
onset_env = librosa.onset.onset_strength(y=y, sr=SR, hop_length=hop)
kw = {"start_bpm": a.bpm_hint} if a.bpm_hint else {}
tempo_l, beats_f = librosa.beat.beat_track(onset_envelope=onset_env, sr=SR, hop_length=hop, units="frames", **kw)
tempo_l = float(np.atleast_1d(tempo_l)[0])
beats = librosa.frames_to_time(beats_f, sr=SR, hop_length=hop)
tempo_e, beats_e, conf_e = None, None, None
try:
    import essentia
    essentia.log.infoActive = False
    import essentia.standard as es
    y44 = decode(a.inp, 44100)
    bpm, ticks, conf, _, _ = es.RhythmExtractor2013(method="multifeature")(y44)
    tempo_e, beats_e, conf_e = float(bpm), np.asarray(ticks), float(conf)
except Exception as e:  # essentia optional
    rep["essentia_error"] = str(e)[:200]
agree = None
if tempo_e:
    ratio = tempo_e / max(tempo_l, 1e-6)
    agree = "same" if abs(ratio - 1) < 0.04 else ("double/half" if min(abs(ratio - 2), abs(ratio - 0.5)) < 0.08 else "differ")
# essentia multifeature is the primary grid when it is confident (its confidence: <1 poor, >3.5 excellent)
use_e = tempo_e is not None and conf_e is not None and conf_e >= 1.5 and len(beats_e) > 4
grid = beats_e if use_e else beats
bpm = tempo_e if use_e else tempo_l
if len(grid) > 3:
    ibi = np.diff(grid)
    bpm_from_grid = 60.0 / np.median(ibi)
    beat_stability = float(np.std(ibi) / np.mean(ibi))
else:
    bpm_from_grid, beat_stability = bpm, None

# downbeats: 4/4 assumed; pick the beat phase whose beats carry the most low-frequency onset energy
S = np.abs(librosa.stft(y, n_fft=2048, hop_length=hop))
freqs = librosa.fft_frequencies(sr=SR, n_fft=2048)
low = S[freqs < 200].sum(axis=0)
low_on = np.maximum(0, np.diff(low, prepend=low[:1]))
downbeats, phase_score = [], None
if len(grid) >= 8:
    bf = np.clip(librosa.time_to_frames(grid, sr=SR, hop_length=hop), 0, len(low_on) - 1)
    strength = low_on[bf] / (low_on.max() + 1e-9) + onset_env[np.clip(bf, 0, len(onset_env) - 1)] / (onset_env.max() + 1e-9)
    scores = [float(strength[p::4].mean()) for p in range(4)]
    p = int(np.argmax(scores))
    downbeats = grid[p::4]
    srt = sorted(scores)
    phase_score = r((srt[-1] - srt[-2]) / (srt[-1] + 1e-9), 3)  # 0 = no preference, higher = clearer
alt = None
if (conf_e is None or conf_e < 1.5) and bpm:
    alt = r(bpm / 2, 1) if bpm >= 120 else r(bpm * 2, 1)
rep["rhythm"] = {
    "tempo_octave_ambiguous": alt is not None, "bpm_alternative": alt,
    "bpm": r(bpm, 1), "bpm_source": "essentia multifeature" if use_e else "librosa beat_track",
    "bpm_librosa": r(tempo_l, 1), "bpm_essentia": r(tempo_e, 1) if tempo_e else None,
    "essentia_confidence": r(conf_e, 2) if conf_e is not None else None, "librosa_vs_essentia": agree,
    "bpm_median_interbeat": r(bpm_from_grid, 1),
    "beat_interval_cv": r(beat_stability, 3) if beat_stability is not None else None,
    "bar_s_4_4": r(4 * 60 / bpm, 3) if bpm else None,
    "beats_s": [r(t, 3) for t in grid],
    "downbeats_s_estimated": [r(t, 3) for t in downbeats],
    "downbeat_phase_clarity": phase_score,
}

# ---------- onsets / hits ----------
on_f = librosa.onset.onset_detect(onset_envelope=onset_env, sr=SR, hop_length=hop, backtrack=False)
on_t = librosa.frames_to_time(on_f, sr=SR, hop_length=hop)
on_s = onset_env[on_f] if len(on_f) else np.array([])
order = np.argsort(-on_s)[:20]
hits = sorted([(float(on_t[i]), float(on_s[i] / (onset_env.max() + 1e-9))) for i in order])
rep["onsets"] = {
    "count": int(len(on_t)), "per_second": r(len(on_t) / dur, 2),
    "onsets_s": [r(t, 3) for t in on_t],
    "strongest_hits": [{"t": r(t, 3), "strength": r(s, 2)} for t, s in hits],
}

# ---------- loudness (EBU R128 via pyloudnorm, 48 kHz stereo) ----------
import pyloudnorm as pyln  # noqa: E402
from scipy.signal import resample_poly  # noqa: E402
st = decode(a.inp, 48000, 2)
meter = pyln.Meter(48000)
try:
    lufs_i = float(meter.integrated_loudness(st))
except Exception:
    lufs_i = float("-inf")
win, hopS = 3.0, 1.0
curve = []
for t0 in np.arange(0, max(dur - win, 0) + 1e-6, hopS):
    seg = st[int(t0 * 48000): int((t0 + win) * 48000)]
    try:
        v = meter.integrated_loudness(seg) if len(seg) > 0.5 * 48000 else float("-inf")
    except Exception:
        v = float("-inf")
    curve.append([r(t0 + win / 2, 1), r(v, 1) if np.isfinite(v) else None])
vals = np.array([c[1] for c in curve if c[1] is not None and c[1] > -70])
lra = float(np.percentile(vals, 95) - np.percentile(vals, 10)) if vals.size > 3 else None
sample_peak = float(np.abs(st).max())
tp = float(np.abs(resample_poly(st, 4, 1, axis=0)).max())  # 4x oversampled peak = true-peak estimate
clip = int((np.abs(st) >= 0.999).sum())
rep["loudness"] = {
    "integrated_lufs": r(lufs_i, 1) if np.isfinite(lufs_i) else None,
    "short_term_lufs_3s": curve,
    "loudness_range_lu_approx": r(lra, 1) if lra is not None else None,
    "sample_peak_dbfs": r(db(sample_peak), 2), "true_peak_dbtp_est": r(db(tp), 2),
    "clipped_samples": clip, "loudest_3s_at": curve[int(np.nanargmax([c[1] if c[1] is not None else -999 for c in curve]))][0] if curve else None,
}

# ---------- silence ----------
rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=hop)[0]
rms_db = 20 * np.log10(np.maximum(rms, 1e-9))
quiet = rms_db < -50
sil, start = [], None
ft = librosa.frames_to_time(np.arange(len(rms)), sr=SR, hop_length=hop)
for i, q in enumerate(np.append(quiet, False)):
    if q and start is None:
        start = i
    elif not q and start is not None:
        t0, t1 = ft[start], ft[min(i, len(ft) - 1)]
        if t1 - t0 >= 0.3:
            sil.append([r(t0, 2), r(t1, 2)])
        start = None
rep["silence"] = {"threshold_dbfs": -50, "min_len_s": 0.3, "spans_s": sil,
                  "total_s": r(sum(b - a_ for a_, b in sil), 2)}

# ---------- sections (self-similarity novelty, beat-synchronous) ----------
sections = []
try:
    chroma = librosa.feature.chroma_cqt(y=y, sr=SR, hop_length=hop)
    mfcc = librosa.feature.mfcc(y=y, sr=SR, hop_length=hop, n_mfcc=13)
    bfr = librosa.time_to_frames(grid, sr=SR, hop_length=hop) if len(grid) > 8 else np.arange(0, len(rms), 43)
    feat = np.vstack([librosa.util.normalize(chroma, axis=0), librosa.util.normalize(mfcc, axis=1)])
    sync = librosa.util.sync(feat, bfr, aggregate=np.median)
    sync_t = librosa.frames_to_time(librosa.util.fix_frames(bfr, x_max=feat.shape[1]), sr=SR, hop_length=hop)
    R = librosa.segment.recurrence_matrix(sync, mode="affinity", sym=True, width=3)
    n = R.shape[0]
    L = 8 if n > 40 else max(2, n // 6)
    g = np.outer(np.hanning(2 * L)[:, None].ravel(), np.hanning(2 * L))
    ker = g * np.block([[np.ones((L, L)), -np.ones((L, L))], [-np.ones((L, L)), np.ones((L, L))]])
    Rp = np.pad(R + np.eye(n), L, mode="constant")
    nov = np.array([(Rp[i:i + 2 * L, i:i + 2 * L] * ker).sum() for i in range(n)])
    nov = np.maximum(nov, 0)
    nov /= nov.max() + 1e-9
    min_gap = max(4, int(round(8 * (60 / bpm) / np.median(np.diff(sync_t))))) if bpm and len(sync_t) > 2 else 8
    peaks = librosa.util.peak_pick(nov, pre_max=min_gap, post_max=min_gap, pre_avg=min_gap, post_avg=min_gap,
                                   delta=0.1, wait=min_gap)
    bounds = [0.0] + [float(sync_t[min(p, len(sync_t) - 1)]) for p in peaks if 4.0 < sync_t[min(p, len(sync_t) - 1)] < dur - 4.0] + [dur]
    rms_t = librosa.frames_to_time(np.arange(len(rms)), sr=SR, hop_length=hop)
    energies = []
    for b0, b1 in zip(bounds[:-1], bounds[1:]):
        m = (rms_t >= b0) & (rms_t < b1)
        energies.append(db(np.sqrt(np.mean(rms[m] ** 2))) if m.any() else -120)
    hi, lo = max(energies), min(energies)
    for k, (b0, b1, e) in enumerate(zip(bounds[:-1], bounds[1:], energies)):
        rel = (e - lo) / (hi - lo + 1e-9)
        lvl = "high" if rel > 0.75 else ("low" if rel < 0.35 else "mid")
        if hi - lo < 3.0:  # under 3 dB spread the energy labels are noise: only the boundary (texture change) is real
            sections.append({"start": r(b0, 2), "end": r(b1, 2), "rms_db": r(e, 1), "energy": "steady",
                             "label_guess": f"part {k + 1}"})
            continue
        if k == 0 and lvl != "high":
            guess = "intro"
        elif k == len(energies) - 1 and lvl != "high":
            guess = "outro"
        else:
            guess = {"high": "drop/chorus", "mid": "verse/build", "low": "break"}[lvl]
        sections.append({"start": r(b0, 2), "end": r(b1, 2), "rms_db": r(e, 1), "energy": lvl, "label_guess": guess})
except Exception as e:
    rep["sections_error"] = str(e)[:200]
rep["sections"] = sections

# ---------- speech / vocal activity (Silero VAD, ONNX) ----------
vad = {"segments_s": [], "speech_fraction": None}
try:
    import onnxruntime as ort
    so = ort.SessionOptions(); so.intra_op_num_threads = 1; so.inter_op_num_threads = 1
    sess = ort.InferenceSession(os.path.join(MODELS, "silero_vad.onnx"), so, providers=["CPUExecutionProvider"])
    y16 = decode(a.inp, 16000)
    state = np.zeros((2, 1, 128), np.float32); ctx = np.zeros(64, np.float32)
    probs = []
    for i in range(0, len(y16) - 512 + 1, 512):
        chunk = np.concatenate([ctx, y16[i:i + 512]]).astype(np.float32)[None]
        out, state = sess.run(None, {"input": chunk, "state": state, "sr": np.array(16000, np.int64)})
        ctx = y16[i + 512 - 64:i + 512]
        probs.append(float(out[0][0]))
    probs = np.array(probs); step = 512 / 16000
    on = probs > 0.5
    segs, s0, last = [], None, None
    for i, v in enumerate(on):
        t = i * step
        if v:
            if s0 is None:
                s0 = t
            last = t + step
        elif s0 is not None and t - last > 0.3:  # bridge pauses < 0.3 s
            if last - s0 >= 0.25:
                segs.append([r(s0, 2), r(last, 2)])
            s0 = None
    if s0 is not None and last - s0 >= 0.25:
        segs.append([r(s0, 2), r(last, 2)])
    tot = sum(b - a_ for a_, b in segs)
    per_s = [r(probs[int(k / step):int((k + 1) / step)].mean(), 2) for k in range(int(dur)) if int(k / step) < len(probs)]
    vad = {"model": "silero_vad.onnx (speech detector; sung vocals are only partly detected)",
           "segments_s": segs, "speech_fraction": r(tot / dur, 3), "prob_per_second": per_s}
except Exception as e:
    vad["error"] = str(e)[:200]
rep["voice_activity"] = vad

# ---------- vocal stem presence (optional, separation in the main venv) ----------
if a.vocals:
    sep = "/home/user/tools/venv/bin/audio-separator"
    vs = {"method": "UVR-MDX-NET-Voc_FT vocal stem, 100 ms RMS within 30 dB of its peak and above -50 dBFS"}
    if os.path.exists(sep):
        td = tempfile.mkdtemp(prefix="listen_sep_")
        subprocess.run([sep, os.path.abspath(a.inp), "-m", "UVR-MDX-NET-Voc_FT.onnx", "--model_file_dir",
                        "/home/user/tools/sep-models", "--output_format", "WAV", "--single_stem", "Vocals",
                        "--output_dir", td], capture_output=True, text=True)
        stems = [os.path.join(td, f) for f in os.listdir(td) if f.lower().endswith(".wav")]
        if stems:
            v16 = decode(stems[0], 16000)
            fr = 1600
            vr = np.array([np.sqrt(np.mean(v16[i * fr:(i + 1) * fr] ** 2)) for i in range(len(v16) // fr)])
            vdb = 20 * np.log10(vr + 1e-9)
            act = (vdb > vdb.max() - 30) & (vdb > -50)
            segs_v, s0, gap = [], None, 0
            for i, v in enumerate(np.append(act, False)):
                if v:
                    s0 = i if s0 is None else s0; gap = 0; last_i = i
                elif s0 is not None:
                    gap += 1
                    if gap > 3 or i == len(act):
                        if (last_i + 1 - s0) >= 3:
                            segs_v.append([r(s0 / 10, 1), r((last_i + 1) / 10, 1)])
                        s0, gap = None, 0
            vs.update({"segments_s": segs_v, "vocal_fraction": r(act.mean(), 3),
                       "vocal_stem_peak_dbfs": r(vdb.max(), 1)})
            for f in os.listdir(td):
                os.unlink(os.path.join(td, f))
        else:
            vs["error"] = "separation produced no stem"
        os.rmdir(td)
    else:
        vs["error"] = "audio-separator not installed (bash library/tools/setup-all.sh heavy)"
    rep["vocal_stem"] = vs

# ---------- key and mood descriptors ----------
keyinfo = {}
try:
    import essentia.standard as es
    y44 = decode(a.inp, 44100) if "y44" not in dir() else y44
    for prof in ("edma", "temperley", "krumhansl"):
        k, sc, strength = es.KeyExtractor(profileType=prof)(y44)
        keyinfo[prof] = {"key": k, "scale": sc, "strength": r(strength, 3)}
    dance, _ = es.Danceability()(y44)
    keyinfo["danceability_essentia_0_3"] = r(dance, 3)
except Exception as e:
    keyinfo["error"] = str(e)[:200]
votes = [v["key"] + " " + v["scale"] for kk, v in keyinfo.items() if isinstance(v, dict) and "key" in v]
centroid = float(np.mean(librosa.feature.spectral_centroid(y=y, sr=SR)))
loud_rms = db(np.sqrt(np.mean(y ** 2)))
mood = {"key_votes": votes, "key_best": max(set(votes), key=votes.count) if votes else None,
        "spectral_centroid_hz": r(centroid, 0), "rms_dbfs": r(loud_rms, 1)}
if votes and bpm:
    major = mood["key_best"].endswith("major")
    fast = bpm >= 110
    bright = centroid > 2500
    mood["mood_heuristic"] = ("bright/upbeat" if major and fast else "calm/warm" if major else
                              "tense/driving" if fast else "sad/reflective") + (", bright timbre" if bright else ", dark/soft timbre")
    mood["mood_heuristic_rule"] = "major/minor x bpm>=110 x centroid>2500 Hz; a rule of thumb, not a trained mood model"
rep["key_and_mood"] = {**keyinfo, **mood}

# ---------- quality: noise floor, hum, hiss ----------
qual = {"clipped_samples": clip}
frame_db = rms_db[np.isfinite(rms_db)]
qual["noise_floor_dbfs_p10"] = r(np.percentile(frame_db, 10), 1)
qual["dynamic_spread_db_p95_p10"] = r(np.percentile(frame_db, 95) - np.percentile(frame_db, 10), 1)
# hum: 1 s spectra of the quietest 30% of the file (where hum is audible), 50/60 Hz (+ harmonics) vs neighbouring bins
y8 = decode(a.inp, 8000)
nfft = 8000
segs = [y8[i:i + nfft] for i in range(0, len(y8) - nfft + 1, nfft // 2)]
if segs:
    en = np.array([np.mean(s ** 2) for s in segs])
    keep = [s for s, e in zip(segs, en) if e <= np.percentile(en, 30) and e > 0] or segs
    P = np.mean([np.abs(np.fft.rfft(s * np.hanning(nfft))) ** 2 for s in keep], axis=0)
    f = np.fft.rfftfreq(nfft, 1 / 8000)
    hum = {}
    for base in (50, 60):
        ex = []
        for h in (1, 2, 3):
            fc = base * h
            pk = P[(f >= fc - 1) & (f <= fc + 1)].max()
            nb = np.median(P[((f >= fc - 10) & (f <= fc - 3)) | ((f >= fc + 3) & (f <= fc + 10))])
            ex.append(10 * np.log10(pk / (nb + 1e-20)))
        hum[f"{base}hz_peak_over_neighbours_db"] = [r(v, 1) for v in ex]
    best = max((50, 60), key=lambda b: max(hum[f"{b}hz_peak_over_neighbours_db"]))
    qual["hum"] = hum
    quiet_db = 10 * np.log10(np.mean([np.mean(s ** 2) for s in keep]) + 1e-20)
    qual["hum_quiet_windows_dbfs"] = r(quiet_db, 1)
    if quiet_db > -35:  # no quiet stretch: music masks any hum and bass notes look like hum
        qual["hum_suspected"] = None
        qual["hum_note"] = "not testable: the quietest parts are louder than -35 dBFS"
    else:
        qual["hum_suspected"] = bool(max(hum[f"{best}hz_peak_over_neighbours_db"]) > 12)
    qual["hum_hz"] = best if qual["hum_suspected"] else None
    qual["hum_rule"] = "quietest 30% of 1 s windows: any of the first 3 harmonics > 12 dB above bins 3-10 Hz away (sustained bass notes can trigger it in music)"
# hiss: share of energy above 8 kHz inside the quiet frames (needs 44.1 kHz)
try:
    yq = y44 if "y44" in dir() else decode(a.inp, 44100)
    Sq = np.abs(librosa.stft(yq, n_fft=2048, hop_length=1024)) ** 2
    fq = librosa.fft_frequencies(sr=44100, n_fft=2048)
    fr = 10 * np.log10(Sq.sum(axis=0) + 1e-20)
    qmask = fr <= np.percentile(fr, 15)
    hf = Sq[fq > 8000][:, qmask].sum() / (Sq[:, qmask].sum() + 1e-20)
    qual["quiet_frames_hf_share"] = r(hf, 3)
    qual["hiss_suspected"] = bool(hf > 0.3 and np.percentile(frame_db, 10) > -70)
    qual["hiss_rule"] = "in the quietest 15% of frames, >30% of energy above 8 kHz and floor above -70 dBFS"
except Exception as e:
    qual["hiss_error"] = str(e)[:200]
rep["quality"] = qual

# ---------- Whisper words ----------
words = None
if not a.no_words and vad.get("speech_fraction") and vad["speech_fraction"] > 0.1:
    if os.path.exists(MAIN_PY):
        code = r'''
import sys, json, whisper
m = whisper.load_model(sys.argv[2])
res = m.transcribe(sys.argv[1], word_timestamps=True, condition_on_previous_text=False, fp16=False)
out = {"language": res.get("language"), "text": res.get("text", "").strip(), "words": []}
for s in res["segments"]:
    for w in s.get("words", []):
        out["words"].append([round(w["start"], 2), round(w["end"], 2), w["word"].strip(), round(w.get("probability", 0), 2)])
print("JSON:" + json.dumps(out, ensure_ascii=False))
'''
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as fh:
            fh.write(code)
        p = subprocess.run([MAIN_PY, fh.name, a.inp, a.whisper_model], capture_output=True, text=True)
        os.unlink(fh.name)
        line = [l for l in p.stdout.splitlines() if l.startswith("JSON:")]
        words = json.loads(line[0][5:]) if line else {"error": (p.stderr or "no output")[-300:]}
    else:
        words = {"error": "main venv with whisper not installed (bash library/tools/setup-all.sh heavy)"}
rep["speech"] = words

# ---------- what kind of audio ----------
sf_ = vad.get("speech_fraction") or 0
ec = conf_e if conf_e is not None else 0
if sf_ > 0.5 and ec < 1.0:
    kind = "speech (tempo, key, mood and section labels are not meaningful)"
elif sf_ > 0.15:
    kind = "music with vocals or speech over music"
elif ec >= 1.0 or (len(grid) > 8 and beat_stability is not None and beat_stability < 0.05):
    kind = "music (no speech-like voice detected)"
else:
    kind = "unclear (no steady beat, little speech): ambience / sfx / free-time music"
rep["content_type_guess"] = kind
rep["content_type_rule"] = "speech_fraction>0.5 and essentia beat confidence<1 -> speech; >0.15 -> vocals/speech over music"

# ---------- summary ----------
def fmt_secs(lst, n=8):
    return ", ".join(f"{x:.2f}" for x in lst[:n]) + (" ..." if len(lst) > n else "")


rh, ld = rep["rhythm"], rep["loudness"]
lines = [f"LISTEN {os.path.basename(a.inp)}  ({dur:.1f} s)  type: {kind}",
         f"tempo {rh['bpm']} BPM ({rh['bpm_source']}; librosa {rh['bpm_librosa']}, essentia {rh['bpm_essentia']} conf {rh['essentia_confidence']}, {agree}), bar(4/4) {rh['bar_s_4_4']} s, beat-interval CV {rh['beat_interval_cv']}" + (f"  LOW CONFIDENCE: could be {rh['bpm_alternative']} BPM (rerun with --bpm-hint)" if rh['tempo_octave_ambiguous'] else ""),
         f"beats: {fmt_secs(rh['beats_s'])}",
         f"downbeats (est., clarity {rh['downbeat_phase_clarity']}): {fmt_secs(rh['downbeats_s_estimated'])}",
         f"hits (strongest): " + ", ".join(f"{h['t']:.2f}" for h in rep['onsets']['strongest_hits'][:10]),
         f"loudness {ld['integrated_lufs']} LUFS, LRA~{ld['loudness_range_lu_approx']} LU, true peak~{ld['true_peak_dbtp_est']} dBTP, clipped samples {ld['clipped_samples']}, loudest 3 s around {ld['loudest_3s_at']} s",
         "sections: " + " | ".join(f"{s['start']:.1f}-{s['end']:.1f} {s['label_guess']} ({s['rms_db']} dB)" for s in sections),
         f"silence (<-50 dBFS, >=0.3 s): {len(sil)} spans, {rep['silence']['total_s']} s total" + (f": {sil[:6]}" if sil else ""),
         f"voice activity: {vad.get('speech_fraction')} of the time, {len(vad.get('segments_s', []))} segments " + str(vad.get('segments_s', [])[:6]),
         *( [f"vocal stem: {rep['vocal_stem'].get('vocal_fraction')} of the time, segments {rep['vocal_stem'].get('segments_s', [])[:8]} {rep['vocal_stem'].get('error', '')}"] if a.vocals else []),
         f"key: {mood.get('key_best')} (votes {votes}), mood (heuristic): {mood.get('mood_heuristic')}",
         f"quality: noise floor p10 {qual['noise_floor_dbfs_p10']} dBFS, hum {qual.get('hum_suspected')}, hiss {qual.get('hiss_suspected')}"]
if isinstance(words, dict) and "text" in words:
    lines.append(f"speech ({words['language']}): {words['text'][:300]}")
elif isinstance(words, dict):
    lines.append(f"speech: {words.get('error')}")
print("\n".join(lines))
if a.out:
    with open(a.out, "w") as fh:
        json.dump(rep, fh, ensure_ascii=False, indent=1)
    print(f"report -> {a.out}")
if a.json:
    print(json.dumps(rep, ensure_ascii=False))
