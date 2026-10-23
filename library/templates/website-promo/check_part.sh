n=$1
cd /home/user/tools
venv/bin/audio-separator /tmp/claude-0/-home-user-new-startup/af4c02a3-c74a-5491-891f-6e93ea7378ac/scratchpad/talkember/song/$n/raw.flac -m UVR-MDX-NET-Voc_FT.onnx --model_file_dir /home/user/tools/sep-models --output_dir /tmp/claude-0/-home-user-new-startup/af4c02a3-c74a-5491-891f-6e93ea7378ac/scratchpad/talkember/song/$n/sep --output_format WAV --single_stem Vocals >/dev/null 2>&1
V=$(ls /tmp/claude-0/-home-user-new-startup/af4c02a3-c74a-5491-891f-6e93ea7378ac/scratchpad/talkember/song/$n/sep/*Vocals*.wav | head -1)
venv/bin/python - "$V" "/tmp/claude-0/-home-user-new-startup/af4c02a3-c74a-5491-891f-6e93ea7378ac/scratchpad/talkember/song/$n/words_v.json" "/tmp/claude-0/-home-user-new-startup/af4c02a3-c74a-5491-891f-6e93ea7378ac/scratchpad/talkember/song/$n/raw.flac" "/tmp/claude-0/-home-user-new-startup/af4c02a3-c74a-5491-891f-6e93ea7378ac/scratchpad/talkember/song/$n/words_raw.json" <<'PY'
import sys, json, whisper
m = whisper.load_model("small")
for src, dst in ((sys.argv[1], sys.argv[2]), (sys.argv[3], sys.argv[4])):
    r = m.transcribe(src, language="hi", fp16=False, word_timestamps=True, condition_on_previous_text=False)
    json.dump([(w["start"], w["end"], w["word"]) for s in r["segments"] for w in s.get("words", [])], open(dst, "w"), ensure_ascii=False)
PY
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 /tmp/claude-0/-home-user-new-startup/af4c02a3-c74a-5491-891f-6e93ea7378ac/scratchpad/talkember/song/$n/raw.flac)
cd /tmp/claude-0/-home-user-new-startup/af4c02a3-c74a-5491-891f-6e93ea7378ac/scratchpad/talkember/video && python3 dp_align.py /tmp/claude-0/-home-user-new-startup/af4c02a3-c74a-5491-891f-6e93ea7378ac/scratchpad/talkember/song/$n.tsv /tmp/claude-0/-home-user-new-startup/af4c02a3-c74a-5491-891f-6e93ea7378ac/scratchpad/talkember/song/$n/timing.json $D /tmp/claude-0/-home-user-new-startup/af4c02a3-c74a-5491-891f-6e93ea7378ac/scratchpad/talkember/song/$n/words_v.json /tmp/claude-0/-home-user-new-startup/af4c02a3-c74a-5491-891f-6e93ea7378ac/scratchpad/talkember/song/$n/words_raw.json
echo "exit $?"
