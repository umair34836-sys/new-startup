# Saved voices

The owner said on 2026-10-27: "Default voice mujhe pasand nhi hai also usko bhi remove kro or 10 different fields or skill k hisaab se alag alag voices bana ker save rakho ta k use kerte time pata ho k konse video k lie konsa voice perfect hai".
So there is NO default voice any more. Running `vs_tts.py` without `--voice` lists these voices.

Pick the voice by the kind of video:

    python3 library/tools/vs_tts.py script.txt out.wav --voice promo-female

## Field voices

These 10 are AI-designed with VoxCPM2 voice design (Apache-2.0, OK for client/paid work). None is a real person.
- Each fixed reference wav is in this folder, because voice design is not repeatable.
- Each line of a script is cloned from that one reference, so the voice stays the same across lines.
- Measured here 2026-10-27: median f0 by pyworld harvest; "Whisper" = similarity of Whisper small's transcript to the reference line.

| Voice | Use it for | Reference line | f0 | Whisper |
|---|---|---|---|---|
| ~~`promo-male`~~ BANNED (owner 2026-10-28: never use in any session) | hosting / business / app promos, offers, ads (male) | अब शुरू करें, सिर्फ़ एक क्लिक में। | 240 Hz | 0.78 |
| `promo-female` | offers, shopping, salon, brand promos (female) | आज ही ऑर्डर करें और पाएं ख़ास ऑफ़र। | 272 Hz | 0.73 |
| `tutorial-calm` | tutorials, screen recordings, step-by-step guides | पहले इस बटन पर क्लिक कीजिए, फिर आगे बढ़िए। | 120 Hz | 0.70 |
| `explainer-pro` | explainers, corporate, product walk-throughs (female) | यह प्लान आपके बिज़नेस के लिए बनाया गया है। | 212 Hz | 0.90 |
| `gaming-hype` | Minecraft / gaming shorts, server promos, hype | भाई, ये सर्वर तो एकदम ज़बरदस्त है! | 148 Hz | 0.81 |
| `food-warm` | restaurant / food / cafe promos | गरमा गरम पिज़्ज़ा, सीधे आपके घर तक। | 320 Hz | 0.74 |
| `story-emotional` | emotional stories, shayari, memories, slow romantic edits | कुछ यादें कभी पुरानी नहीं होतीं। | 117 Hz | 0.94 |
| `kids-cheerful` | kids content, funny / cartoon style, light memes | चलो बच्चों, आज कुछ मज़ेदार सीखते हैं! | 336 Hz | 0.81 |
| `luxury-deep` | luxury, real estate, premium brand, trailers | जहाँ हर पल ख़ास है। | 139 Hz | 0.90 |
| `news-anchor` | announcements, news-style updates, launch / season news | आज की बड़ी ख़बर, सीधे आप तक। | 122 Hz | 0.80 |

### Clone test (measured here 2026-10-27)
Each voice was given the same new line through `vs_tts.py --voice <name>`: "नमस्ते दोस्तों, आज हम आपके लिए कुछ नया लेकर आए हैं।"
- Whisper small similarity: promo-male 0.90, promo-female 0.86, tutorial-calm 0.87, explainer-pro 0.77, gaming-hype 0.82, food-warm 0.76, story-emotional 0.93, kids-cheerful 0.96, luxury-deep 0.88, news-anchor 0.90.
- Clone median f0: 204, 259, 120, 187, 133, 298, 118, 318, 126 and 113 Hz (same order).
- One line took about 2-4 min each (03:15-03:41 for all 10), with the model already loaded.

### How they were made (2026-10-27)
- Each voice had 2 design takes (seeds 7 and 21). Two voices got 2 more seeds (33, 42), because their first takes "ran on" past the sentence with extra sounds: promo-male seed 7, both tutorial-calm takes, news-anchor seed 21 and promo-female seed 7.
- The take with the cleanest Whisper transcript was kept and saved as 24 kHz mono.
- The instructs and seeds are in voices.json.

## Client voices (cloned, recording never committed)

| Name | Whose voice | Added |
|---|---|---|
| `senpaispider` | the owner's client "Senpai Spider" (the owner shared the clip on 2026-10-24) | 2026-10-24 |

How the client voice is stored:
- voices.json keeps only the recipe (source link, clean step, cut).
- On first use, vs_tts.py rebuilds the reference into /home/user/tools/voices/<name>/ref.wav.
- Clone only voices the owner or their client has agreed to. Never a celebrity or voice actor without permission.

## Removed
- `default` (an AI young ad narrator, MoradoSolution reel, 2026-10-24): removed on 2026-10-27, because the owner did not like it.
