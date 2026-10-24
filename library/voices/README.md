# Saved voices (clone references)

The owner names a voice once; later "is voice mein banao" uses it by name:

    python3 library/tools/vs_tts.py script.txt out.wav --voice senpaispider

`voices.json` keeps only the recipe (source link, clean step, cut, model, measurements). The voice recording itself
is NEVER committed (owner rule): on first use in a new container vs_tts.py downloads the source, runs clean_voice.py,
cuts the reference and caches it in /home/user/tools/voices/<name>/ref.wav (~8 min the first time).
Clone only voices the owner or their client has agreed to; never a celebrity or voice actor without permission.

| Name | Whose voice | Added |
|---|---|---|
| `senpaispider` | the owner's client "Senpai Spider" (owner shared the clip, 2026-10-24) | 2026-10-24 |
