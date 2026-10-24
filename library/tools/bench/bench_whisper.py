# Used for library/research/cpu-speed.md (2026-10-24). usage: /home/user/tools/venv/bin/python bench_whisper.py AUDIO THREADS fp32|int8
import sys, time, torch, whisper, json
th, q = int(sys.argv[2]), sys.argv[3] == "int8"
torch.set_num_threads(th)
m = whisper.load_model("small", device="cpu")
if q:
    m = torch.quantization.quantize_dynamic(m, {torch.nn.Linear}, dtype=torch.qint8)
t0 = time.perf_counter()
r = m.transcribe(sys.argv[1], fp16=False, condition_on_previous_text=False, language="en")
print(json.dumps({"threads": th, "int8": q, "s": round(time.perf_counter() - t0, 1), "text": r["text"][:4000]}))
