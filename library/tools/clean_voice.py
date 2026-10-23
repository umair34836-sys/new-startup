# Keep only the person's voice from a video (or audio) file: music, TV, crowd, fan/AC hum, hiss, wind and other
# background sounds are removed, then the clean voice goes back into the video in place of the old sound.
# Run inside /home/user/tools/venv (setup-all.sh heavy). Personal videos stay in the scratchpad, never in git.
#
#   python clean_voice.py INPUT.mp4 --out /path/to/outdir [--dereverb] [--fast]
#
# Steps:
#   1. ffmpeg pulls the audio out (44.1 kHz stereo)
#   2. BS-RoFormer vocals stem: drops music, TV, crowd and most other non-voice sound
#      (--fast uses UVR-MDX-NET Voc FT instead: several times quicker on CPU, a little less clean)
#   3. Mel-RoFormer Denoise (aufr33) "dry" stem: drops steady noise left under the voice (fan, hiss, wind, hum)
#   4. --dereverb: UVR DeEcho-DeReverb "no reverb" stem for echoey rooms (off by default: it can thin a voice)
#   5. 70 Hz high-pass, -16 LUFS; written as voice.wav, and for a video INPUT also clean.mp4 (video copied as is)
#   6. Whisper transcript of the clean voice in report.json, so the words can be checked
import argparse, json, os, shutil, subprocess, time

ap = argparse.ArgumentParser()
ap.add_argument("input")
ap.add_argument("--out", required=True)
ap.add_argument("--dereverb", action="store_true", help="also remove room echo")
ap.add_argument("--fast", action="store_true", help="quicker vocal model (MDX-Net Voc FT)")
ap.add_argument("--no-denoise", action="store_true", help="skip the denoise pass")
ap.add_argument("--lang", default=None, help="Whisper language for the check (default: auto)")
ap.add_argument("--whisper-model", default="small")
a = ap.parse_args()

MODELS = "/home/user/tools/sep-models"
VOCALS = "UVR-MDX-NET-Voc_FT.onnx" if a.fast else "model_bs_roformer_ep_368_sdr_12.9628.ckpt"
DENOISE = "denoise_mel_band_roformer_aufr33_sdr_27.9959.ckpt"
DEREVERB = "UVR-DeEcho-DeReverb.pth"
os.makedirs(a.out, exist_ok=True)
work = os.path.join(a.out, "work")
os.makedirs(work, exist_ok=True)
log = lambda m: print(f"[{time.strftime('%H:%M:%S')}] {m}", flush=True)
ff = lambda *args: subprocess.run(["ffmpeg", "-v", "error", "-y", *args], check=True)

has_video = bool(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=codec_type",
                                 "-of", "csv=p=0", a.input], capture_output=True, text=True).stdout.strip())
src = os.path.join(work, "0-original.wav")
ff("-i", a.input, "-vn", "-ac", "2", "-ar", "44100", src)
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src],
                           capture_output=True, text=True).stdout)
log(f"audio extracted: {dur:.1f}s")

from audio_separator.separator import Separator

def stem(inp, model, want, name):
    """Run one separation model and keep the stem whose name contains `want` (case-insensitive)."""
    out = os.path.join(work, name)
    if os.path.exists(out):
        return out
    t0 = time.time()
    sep = Separator(model_file_dir=MODELS, output_dir=work, output_format="WAV")
    sep.load_model(model_filename=model)
    files = [os.path.join(work, os.path.basename(f)) for f in sep.separate(inp)]
    keep = [f for f in files if f"({want.lower()})" in os.path.basename(f).lower()]
    if not keep:
        raise SystemExit(f"{model}: no '{want}' stem in {files}")
    shutil.move(keep[0], out)
    for f in files:
        if f != keep[0] and os.path.exists(f):
            os.remove(f)
    log(f"{name}: {model} in {time.time() - t0:.0f}s")
    return out

x = stem(src, VOCALS, "vocals", "1-voice.wav")
if not a.no_denoise:
    x = stem(x, DENOISE, "dry", "2-denoised.wav")
if a.dereverb:
    x = stem(x, DEREVERB, "no reverb", "3-dereverb.wav")

voice = os.path.join(a.out, "voice.wav")
ff("-i", x, "-af", "highpass=f=70,loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", voice)
log("voice.wav written")
if has_video:
    clean = os.path.join(a.out, "clean.mp4")
    ff("-i", a.input, "-i", voice, "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
       "-shortest", "-movflags", "+faststart", clean)
    log("clean.mp4 written (video untouched, new clean sound)")

import whisper
r = whisper.load_model(a.whisper_model).transcribe(voice, language=a.lang, fp16=False)
json.dump({"input": os.path.basename(a.input), "duration": round(dur, 2), "vocal_model": VOCALS,
           "denoise": not a.no_denoise, "dereverb": a.dereverb, "language": r.get("language"),
           "transcript": r["text"].strip()}, open(os.path.join(a.out, "report.json"), "w"), ensure_ascii=False, indent=1)
log(f"transcript ({r.get('language')}): {r['text'].strip()[:200]}")
