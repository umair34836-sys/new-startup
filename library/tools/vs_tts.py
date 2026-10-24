# Voiceover with VoiceStudio (local ElevenLabs replacement): one line of the script per request, joined with short
# pauses and loudness-normalised. Start the backend first: bash library/tools/voicestudio.sh start
#
#   python3 vs_tts.py SCRIPT.txt OUT.mp3 --lang ur --instruct "male, young adult" [--seed 7] [--gap 0.45]
#          [--model omnivoice|voxcpm2] [--ref voice.wav --ref-text "words in voice.wav"]   (cloning)
#
# Script: one line per sentence, in the language's own script (Urdu/Pashto in Nastaliq, Hindi in Devanagari).
# Licence: omnivoice weights are NON-COMMERCIAL (personal videos only); voxcpm2 is Apache-2.0 (client/paid work).
import argparse, json, os, subprocess, tempfile, urllib.request

ap = argparse.ArgumentParser()
ap.add_argument("script")
ap.add_argument("out")
ap.add_argument("--lang", default="ur")
ap.add_argument("--instruct", default="male, young adult")
ap.add_argument("--seed", type=int, default=7)
ap.add_argument("--gap", type=float, default=0.45)
ap.add_argument("--model", default="omnivoice")
ap.add_argument("--ref", help="reference voice wav for cloning (only voices you may use)")
ap.add_argument("--ref-text", default="", help="exact words spoken in --ref")
ap.add_argument("--host", default="http://127.0.0.1:3900")
ap.add_argument("--parts", help="keep each line's wav here (001.wav ...) and write lines.json = [start, end] of each line in OUT")
a = ap.parse_args()

lines = [l.strip() for l in open(a.script, encoding="utf-8") if l.strip()]
tmp = a.parts or tempfile.mkdtemp(prefix="vs_tts_")
os.makedirs(tmp, exist_ok=True)


def speech(text, path):
    if a.ref:  # native endpoint takes a reference clip for zero-shot cloning
        cmd = ["curl", "-sf", "-o", path, "-X", "POST", a.host + "/generate", "-F", f"text={text}",
               "-F", f"language={a.lang}", "-F", f"seed={a.seed}", "-F", f"ref_audio=@{a.ref}"]
        if a.ref_text:
            cmd += ["-F", f"ref_text={a.ref_text}"]
        if a.model != "omnivoice":
            cmd += ["-F", f"engine={a.model}"]
        subprocess.run(cmd, check=True)
        return
    body = {"model": a.model, "input": text, "language": a.lang, "instruct": a.instruct,
            "response_format": "wav", "seed": a.seed}
    req = urllib.request.Request(a.host + "/v1/audio/speech", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        open(path, "wb").write(urllib.request.urlopen(req, timeout=1800).read())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"VoiceStudio {e.code}: {e.read().decode()[:400]}")


parts = []
for i, line in enumerate(lines):
    p = os.path.join(tmp, f"{i:03d}.wav")
    speech(line, p)
    d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                       capture_output=True, text=True).stdout.strip()
    print(f"{i + 1}/{len(lines)} {float(d):.1f}s  {line[:60]}", flush=True)
    parts.append(p)

# concat with silence between lines, resampled to 44.1k, -16 LUFS
inputs, chains = [], []
for i, p in enumerate(parts):
    inputs += ["-i", p]
    chains.append(f"[{i}]aresample=44100,aformat=channel_layouts=mono,apad=pad_dur={a.gap}[a{i}]")
graph = ";".join(chains) + ";" + "".join(f"[a{i}]" for i in range(len(parts))) + \
    f"concat=n={len(parts)}:v=0:a=1,loudnorm=I=-16:TP=-1.5[out]"
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", graph, "-map", "[out]", "-ar", "44100",
                *(["-b:a", "192k"] if a.out.endswith(".mp3") else []), a.out], check=True)
if a.parts:  # line i spans [start, start + its own duration] in OUT (each line is followed by --gap of silence)
    spans, t = [], 0.0
    for p in parts:
        d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                 capture_output=True, text=True).stdout)
        spans.append([round(t, 3), round(t + d, 3)]); t += d + a.gap
    json.dump(spans, open(os.path.join(a.parts, "lines.json"), "w"))
print("wrote", a.out)
