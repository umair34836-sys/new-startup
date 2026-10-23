# Generate several songs with ONE model load (loading + INT8 quantization takes ~11 min on this CPU box).
import os, shutil, sys, time
os.environ.setdefault("HF_HUB_DISABLE_XET", "1"); os.environ.setdefault("ACESTEP_GENERATION_TIMEOUT", "5400")
from acestep.handler import AceStepHandler
from acestep.inference import GenerationParams, GenerationConfig, generate_music
P = sys.argv[1]
CAP = "upbeat hindi pop jingle, bright synths, acoustic guitar, punchy drums, dholak, energetic and positive, warm male vocals, clear hindi lyrics"
parts = [("part2", 130), ("part3", 150)]
dit = AceStepHandler()
st, ok = dit.initialize_service(project_root="/home/user/tools/ACE-Step-1.5", config_path="acestep-v15-turbo", device="cpu",
                                prefer_source="huggingface", quantization="int8_weight_only")
print(time.strftime("[%H:%M:%S]"), "model ready", ok, flush=True)
for name, dur in parts:
    out = f"{P}/{name}/raw.flac"
    if os.path.exists(out):
        continue
    os.makedirs(f"{P}/{name}", exist_ok=True)
    lyrics = open(f"{P}/{name}.txt").read()
    params = GenerationParams(task_type="text2music", caption=CAP, lyrics=lyrics, vocal_language="hi", duration=dur, bpm=112,
                              inference_steps=8, seed=7, thinking=False, use_cot_metas=False, use_cot_caption=False, use_cot_language=False)
    res = generate_music(dit, None, params, GenerationConfig(batch_size=1, use_random_seed=False, seeds=[7], audio_format="flac"),
                         save_dir=f"{P}/{name}/tmp")
    print(time.strftime("[%H:%M:%S]"), name, "ok" if res.success else res.error, flush=True)
    if res.success:
        shutil.copy(res.audios[0]["path"], out); shutil.rmtree(f"{P}/{name}/tmp", ignore_errors=True)
