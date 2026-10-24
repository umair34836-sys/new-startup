# Whisper-check wavs against script lines: python wcheck.py script.txt a.wav [b.wav ...] (line i <-> wav i, or all vs line 1 with --same)
import sys, difflib, whisper, re
args = sys.argv[1:]; same = '--same' in args; args = [a for a in args if a != '--same']
lines = [l.strip() for l in open(args[0], encoding='utf-8') if l.strip()]
m = whisper.load_model('small')
norm = lambda s: re.sub(r'[^\w\s]', '', s).replace('़', '').split()
for i, w in enumerate(args[1:]):
    ref = lines[0] if same else lines[i]
    r = m.transcribe(w, language='hi', condition_on_previous_text=False, fp16=False)
    hyp = r['text'].strip()
    sim = difflib.SequenceMatcher(None, norm(ref), norm(hyp)).ratio()
    segs = r['segments']; end = segs[-1]['end'] if segs else 0
    print(f"{w}\t{sim*100:.0f}%\tlast_word_end={end:.2f}\n  REF {ref}\n  HYP {hyp}", flush=True)
