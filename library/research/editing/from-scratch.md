# Building a video from scratch (no footage)

How to make a complete video when the owner gives no clips at all: format, script, beat map, no-credit visuals, voice, music, assembly, mix, export and QA.

Researched 2026-10-24.

## 1. Pick format, goal and length

- Write the one thing first: what the film is in one line, the one thing the viewer remembers, and one viewer doing one real task as the spine [repo: .claude/skills/hyperframes/references/story.md §1].
- A new HyperFrames video is 1920x1080 at 30 fps, with no new aspect ratio unless the request or the source calls for it [repo: .claude/skills/hyperframes/SKILL.md].
- Vertical is 1080x1920; a landscape film is recomposed for it, not squeezed [repo: .claude/skills/hyperframes/references/types/vertical.md].
- Explainers usually run 30-90 s, built on one concrete example worked through [repo: .claude/skills/hyperframes/references/types/explainer.md].
- YouTube Shorts: in Adobe's creator study, under 30 s was named the best length for views, shares, click-throughs and saves (avg 46% of creators); 30-60 s matched under-30 s only for subscriber growth (34% each) [Adobe, https://www.adobe.com/express/learn/blog/youtube-shorts-length-study].
- Opus reports Shorts of 15-30 s get the highest retention, often over 80% [Opus Clip, https://www.opus.pro/blog/ideal-youtube-shorts-length-format-retention, 2025-11-11].
- Benchmark: the median YouTube Short holds about 45% average view-through; the top 10% hold about 91% [Quso, https://quso.ai/research/video-retention-benchmarks].
- TunePocket's analysis of trending Shorts: 57% were under 20 s or close to the 60 s limit; Shorts can now be up to 3 minutes [TunePocket, https://www.tunepocket.com/best-length-youtube-shorts/, 2024-10-03].
- Instagram Reels can be up to 3 minutes (raised from 90 s in 2025) [Amplitude Marketing, https://amplitudemktg.com/social-media/instagram-reels-everything-you-need-to-know-in-2025/, 2025-07-04].
- TikTok: uploads up to 60 minutes, in-app recording up to 10 minutes, minimum 3 seconds [Shopify, https://www.shopify.com/blog/tiktok-video-size, 2024-09-10].
- Faceless videos (no presenter) work as voiceover over B-roll, screen recordings, animation or archive footage, and need only licensed footage and music [Pacing House, https://pacinghouse.com/guides/faceless-youtube-video-editing/, 2026-10-17].

## 2. Script

### Write it first
- A faceless video is usually written before anything else; the script decides structure, pace and which visuals are needed [Kredos Media, https://www.kredosmedia.com/article/faceless-youtube-video-editing].
- Start from the script, not the footage [Pacing House, https://pacinghouse.com/guides/faceless-youtube-video-editing/, 2026-10-17].
- Keep facts apart from creative choices; every on-screen claim traces to a source; never derive a claim the source did not make [repo: .claude/skills/hyperframes/references/story.md §1].
- In HyperFrames, write three storylines (different world, device, form) in words before building, then write the picked one as SPEC.md [repo: .claude/skills/hyperframes/references/story.md §2].

### Hook (first seconds)
- The hook is the first 1-3 seconds: a visual plus a line that gives a reason to stay; start mid-action [Click Pop, https://www.clickpop.ai/guides/hooks-for-the-first-three-seconds, 2026-10-14].
- 3-second test: watch only the first 3 s with sound off and ask if you can tell what it is about, who should care, and why to keep watching [CapCut, https://www.capcut.com/create/short-form-video-hooks, 2026-06-12].
- Frame 0 is the thumbnail: never black, never a logo alone; the first two seconds are the densest [repo: .claude/skills/hyperframes/references/story.md §3].
- The hook must work with sound off; many viewers scroll muted [ScreenWeaver, https://www.screenweaver.ai/blog/writing-short-film-tiktok-youtube-shorts-reels, 2026-03-19].
- Write three hooks in different styles and pick the strongest [DEV Community, https://dev.to/agentworkshop/from-rough-idea-to-filmable-tiktok-script-a-hook-build-payoff-cta-template-1a06, 2026-10-14].
- Skip channel intros and greetings; open on the most interesting frame, claim or question, and tell the viewer explicitly what they will get within the first 15-30 s [Infinite Creation, https://infinitecreation.io/tutorial-story-structure].
- Open loop: raise a question or promise early and pay it off later, adding small loops between sections [Asendify, https://www.asendify.co/blog/open-loops-video-editing/, 2026-10-11].
- Trailers now stress the first 6 seconds, many on YouTube opening with a 6 s teaser; in medias res (starting in the middle of the story) is probably the most common cold open [Derek Lieu, https://www.derek-lieu.com/blog/2019/10/2/editing-an-engaging-trailer-opening, 2019-10-02].

### Structure
- Four beats: Hook (why stop scrolling), Setup (needed context), Payoff (deliver the promise), CTA (next action) [Viral.new, https://viral.new/blog/how-to-write-a-short-video-script, 2026-08-20].
- 30-second story: Hook 0-3 s (7-8 words), Turn 3-20 s (40-45 words), Payoff 20-30 s (25-30 words); a new beat or visual change every 2-4 s [WowReveal, https://wowreveal.com/blog/story-structure-30-second-shorts-hook-turn-payoff, 2026-10-10].
- Hook-Retain-Reward: hook under 3 s, retain with concrete content and proof, reward with something usable [aiskillstore hook-archetypes, https://github.com/aiskillstore/marketplace/blob/36e07d5e13068e5be64447e8f20b427cf2cbd21a/skills/vyralcontent/viral-hooks/references/hook-archetypes.md].
- Three acts: Act I 25%, Act II 50%, Act III 25% of runtime [Austen Menges, https://www.austenmenges.com/blog/three-act-story-structure-editing].
- AIDA for 15-60 s ads: Attention 0-3 s, Interest 3-10 s, Desire 10-25 s, Action last 3-5 s [AdConvert, https://adconvert.org/blog/how-to-write-video-ad-scripts, 2025-08-05].
- PAS (Problem-Agitate-Solution) works best at 30-45 s; about 8 s on the cost; the common mistake is agitating too long [Cutroom, https://cutroomai.com/formats/problem-agitate-solve-ad].
- Launch shape (~35 s): Hook ~8%, Tension ~12%, Reveal ~8%, Proof ~40%, Payoff ~20%, Claim ~8%, End card ~8% [repo: .claude/skills/hyperframes/references/story.md §4].
- Faceless long-form template: hook 8-15 s teasing the main takeaway, 5-8 headed sections, recap and CTA [Lean Ecommerce / n8n template, https://the-lean-ecommerce.hashnode.dev/build-a-faceless-youtube-automation-system-with-ai-and-n8n, 2026-01-26].
- Educational: keep asking "why would somebody care about this?" [Descript, https://www.descript.com/blog/article/making-better-educational-videos, 2024-09-10].

### Word count per minute of speech
- Professional English narration averages about 150 wpm (range 140-160). By type: commercials/promos 160-180, explainers 150-160, corporate/documentary 140-155, e-learning 130-145, audiobooks 150-155, meditation 100-120 [Parlixa, https://www.parlixa.com/blog/words-per-minute-voice-over, 2026-07-11].
- Parlixa word targets at ~150 wpm: 15 s = 35-40 words, 30 s = 75-80, 60 s = 150-160, 90 s = 210-230, 2 min ~300; these assume continuous narration [Parlixa, https://www.parlixa.com/blog/words-per-minute-voice-over, 2026-07-11].
- Voice Realm calculator: 140 wpm slow (audiobooks), 160 regular (explainers, corporate, e-learning), 180 fast (commercials); 1 min = 160 words at regular pace [The Voice Realm, https://www.thevoicerealm.com/count-script.php].
- Leave room to breathe: at 140 wpm a 30 s read is ~70 words flat out or ~63 with breathing room; 60 s ~140 (~126 with pauses); most VO is 110-170 wpm, 1.8-2.8 words/s [VoiceDeck, https://voicedeck.io/tools/vo-word-budget-calculator/].
- Pauses, emphasis, names and numbers take longer; leave a buffer for a strict time limit [VoiceoverGuy, https://www.voiceoverguy.co.uk/voice-over-word-count-calculator].
- Measured: median audiobook narration is 154 wpm across 1,585 audiobooks (137 sci-fi slowest, 189 young adult fastest) [The Books Insider, https://thebooksinsider.com/insights/audiobook-narration-speed/, 2026-07-26].
- Audible uses an average of 155 wpm, 9,300 words per finished hour [Karen Commins, https://karencommins.com/2011/06/some_simple_math_about_audiobo.html, 2011-06-13].
- Normal English speaking rate is 150-190 wpm; audiobooks are recorded at the low end, ~150-160 wpm [Psychology Today, https://www.psychologytoday.com/us/blog/small-talk-and-big-questions/202307/is-speed-listening-right-for-you, 2023-07-27].
- For TTS in HyperFrames: about 2.2 words/s; keep a scene to ~19 words (9 s), at most two scenes up to 26 words (12 s); 30-90 s is about 155 words or fewer, a whole film about 400 at most [repo: .claude/skills/hyperframes/references/film.md "Script and pacing"].
- A voiceover longer than its visuals makes visuals pad; trim the script, never stretch the motion [repo: .claude/skills/hyperframes/references/film.md "Script and pacing"].

## 3. Storyboard / beat map

- A storyboard turns the SHOTS line of SPEC.md into one still per shot, each with its `reads` and `sound` [repo: .claude/skills/hyperframes/references/storyboard.md].
- Run: pose each shot in `index.html` at its key moment (copy the film to `boards/.film.html` first), snapshot all stills in one run (`npx hyperframes snapshot --at <seconds...> --no-end --describe false -o boards/stills`), write `boards/storyboard.html`, put the film back, and stop for the owner's go [repo: .claude/skills/hyperframes/references/storyboard.md §1].
- Each frame box has `class="frame"`, an image, a `title` "NN: name", a `time` range; optional `words` and `act` headings [repo: .claude/skills/hyperframes/references/storyboard.md §2].
- `STORYBOARD.md` at the project root names the same frames in the same order, with `- status: outline` until posed [repo: .claude/skills/hyperframes/references/storyboard.md §3].
- Narrated: the voice is the clock; time each beat to its anchor word, and text lands on the word that says it [repo: .claude/skills/hyperframes/references/sound.md §2].
- Reveal each part when the voice names it, across the back half of the scene; write the VO as separate phrases so it has cue points [repo: .claude/skills/hyperframes/references/film.md "Script and pacing"].
- Change the picture often: one guide says a new visual every 3-5 s (120-200 visual changes for 10 minutes) [Stitchr, https://stitchr.app/blog/faceless-youtube-video-production-pipeline, 2026-07-03]; another says visual changes every 3-7 s [Editing Machine, https://editingmachine.com/blog/youtube-video-editor-for-retention-beyond-just-cuts, 2026-03-06].
- Show what is said: every detail named in the audio should be shown (close-ups, text, annotations, images) [Smarthistory, https://smarthistory.org/principles-of-smarthistory-video-editing/].
- B-roll lets you show and not just tell [Wistia, https://wistia.com/blog/b-roll, 2015-08-11].
- Lock one style for all generated images; 60 images in 60 styles reads as a slideshow [Longform Studio, https://longformstudio.app/articles/how-to-make-faceless-youtube-videos, 2026-08-11].

## 4. Visual sources that need NO credit

Owner rule: background music/songs must need no credit (CC0, public domain or made by us; CC BY is not acceptable) [repo: CLAUDE.md "Environment facts"]. Only download CC/public-domain/royalty-free media, check the licence, and never copyrighted material [repo: CLAUDE.md "Environment facts"].

### Stock and archive
- Pexels: all photos and videos free to use, attribution not required, modification allowed; not allowed: identifiable people in a bad light, selling unaltered copies, implying endorsement [Pexels, https://www.pexels.com/license/]. Commercial use is allowed [Pexels Help, https://help.pexels.com/hc/en-us/articles/360042295214-Can-I-use-the-photos-and-videos-for-a-commercial-project]. Most photos are under the Pexels license; some are CC0 and marked "CC0" on the photo page [Pexels, https://www.pexels.com/creative-commons-images/].
- Pixabay: use for free, no attribution needed, may modify; prohibited: selling/distributing unaltered content standalone, commercial use of content with recognisable trademarks/logos for goods, immoral/illegal or misleading use, use as a trademark [Pixabay Content License Summary, https://pixabay.com/service/license-summary/]. Pixabay content is mostly royalty-free licensed, not copyright-free; CC0 is no longer the standard for new items [Pixabay, https://pixabay.com/blog/posts/intellectual-property-explained-441/, 2025-10-06]. pixabay is on this container's network allowlist history [repo: CLAUDE.md "Environment facts"].
- Wikimedia Commons: "PD" means not copyrighted and free for any use [Wikimedia Commons, https://commons.wikimedia.org/wiki/Commons:PD_files]. Non-copyright restrictions can still apply and it is the reuser's responsibility to check [Wikimedia Commons, https://commons.wikimedia.org/wiki/Commons:Licensing]. A non-US file needs a tag showing it is PD in the US too [Wikimedia Commons, https://commons.wikimedia.org/wiki/Commons:Copyright_tags]. For no-credit use pick files whose page shows a PD or CC0 tag; the owner's no-credit rule (written for music) rejects CC BY [repo: CLAUDE.md "Environment facts"].
- NASA: content generally not copyrighted in the US, usable for educational/informational purposes; NASA should be acknowledged as the source; the insignia, logotype and identifiers are not public domain; third-party images are marked copyrighted; commercial use with NASA logos or employees may need clearance [NASA, https://www.nasa.gov/nasa-brand-center/images-and-media/]. Because NASA asks to be acknowledged as the source, it is not a no-credit source [NASA, https://www.nasa.gov/nasa-brand-center/images-and-media/]. Library: [NASA, https://images.nasa.gov/].
- Openverse: 876 million openly licensed images and 4 million audio tracks indexed as of 2024-09-26 [Invest in Open Infrastructure, https://infrafinder.investinopen.org/solutions/openverse]; all content is CC-licensed or public domain and searchable by licence [University of Oklahoma Libraries, https://guides.ou.edu/cc/image_search, 2024-07-02]. Use the CC0 filter, e.g. `https://openverse.org/search/?license=cc0&q=...` [Openverse, https://openverse.org/search/?license=cc0&q=Animals]. api.openverse.org is reachable here [repo: CLAUDE.md "Environment facts"].
- Internet Archive / Prelinger: about 65% of the Prelinger Archives holdings are public domain, so check each item [Wikipedia, https://en.wikipedia.org/wiki/Prelinger_Archives, 2025-12-05]. Collection: [Internet Archive, https://archive.org/details/prelinger].
- Public domain = not restricted by copyright, because it expired or was dedicated; CC0 dedicates a work to the public domain [Creative Commons, https://creativecommons.org/public-domain/].
- Stills need motion: the Ken Burns effect is a pan and zoom over still images, used mainly when film or video material is not available [Wikipedia, https://en.wikipedia.org/wiki/Ken_Burns_effect]; ease in and out to simulate friction [Apple Final Cut Pro guide, https://support.apple.com/guide/final-cut-pro/pan-and-zoom-clips-verb8e5de9c/10.5/mac/10.15.6]. 2.5D parallax moves separate parts of the image, unlike Ken Burns which moves the whole picture [Motion Array, https://blog.motionarray.com/learn/after-effects/animate-flat-2d-images-after-effects/, 2021-02-09].

### Generated here (no licence questions)
- HyperFrames registry: about 450 blocks and components (transitions, overlays, titles, kinetic type, captions, charts, maps, 3D, camera moves); find with `npx hyperframes catalog --query "<beat>" --json`, install with `npx hyperframes add <name> --json`; query in English [repo: .claude/skills/hyperframes-registry/SKILL.md].
- Search the registry before hand-writing a named effect, transition, caption style, chart or card [repo: .claude/skills/hyperframes/SKILL.md].
- Registry blocks point at the GSAP CDN: change them to the vendored file [repo: CLAUDE.md "HyperFrames learnings"].
- Kinetic type: 3-7 English words per scene; a count-up runs 1.2-1.6 s, then holds [repo: .claude/skills/hyperframes/references/film.md]. Not narrated: large lines up to about 10 words, each held 0.5 s + 0.3 s a word [repo: .claude/skills/hyperframes/references/types/explainer.md].
- Charts: real data only with a source line; build in reading order (axis, reference line, data, one annotation); highlight one series; registry charts first [repo: .claude/skills/hyperframes/references/types/data.md].
- Explainer devices: the object is the explanation, one diagram that grows, continuous transformation, the worked example [repo: .claude/skills/hyperframes/references/types/explainer.md].
- CSS 3D voxel worlds: `library/tools/voxel_world.py` (`World.box/plane`, `html()`, `css()`, `camera_js`) [repo: library/tools/voxel_world.py]. Rules: no `mix-blend-mode`/opacity/filter on the preserve-3d container, tile ground into 4x4-block quads, apply initial states with `gsap.set`, keep the camera out of buildings, ~1,200 faces + 2 characters render fine [repo: CLAUDE.md "CSS 3D voxel films"].
- Default host: when a video needs a host/presenter/character, use `library/characters/host-skin.png` built with `library/tools/blocky_character.py` unless another is named [repo: CLAUDE.md "Rules from the owner"]. Command: `python3 blocky_character.py OUT.html --skin assets/characters/host-skin.png --id host --duration 6 --scale 16 --moves '[[0,"idle"],[1,"wave"],[3,"talk"],[5,"idle"]]'`; poses idle, wave, talk, walk, run, point, hold, spin [repo: library/tools/blocky_character.py]. Copy the skin into the project's assets first [repo: library/README.md].
- Character acting: offset parts, anticipation and settle, hold the reaction [repo: .claude/skills/hyperframes/references/types/character.md].
- `library/tools/ember_background.py`: dark ember background scene (36 rising embers + glow) from the FireCraft video [repo: library/README.md].
- `library/tools/floating_hearts.py OUT.html [--duration 20] [--count 20] [--burst-at 16.4] [--width 1080] [--height 1920]`: deterministic floating hearts + bokeh overlay [repo: library/tools/floating_hearts.py].
- Show real things from their source (product screens, brand logo, a real place's imagery); draw only what has none [repo: .claude/skills/hyperframes/SKILL.md].

## 5. Voice

- "Voice over / narration / awaaz" = spoken voice with zero music, every line present -> `library/tools/ai_voice.py`; "song / gaana" -> `ai_song.py`; skill `.claude/skills/voice-or-song` [repo: CLAUDE.md "Voice and songs with words"].
- `ai_voice.py --script lines.txt --out DIR`: lines in Devanagari, one per row; output voice.wav (48 kHz, -16 LUFS), voice.mp3, report.json [repo: library/tools/ai_voice.py]. Lines are generated in groups of 6, ~6.5 min per round of 3 takes [repo: CLAUDE.md "Voice and songs with words"].
- VoiceStudio: `bash library/tools/voicestudio.sh start`, then `python3 vs_tts.py SCRIPT.txt OUT.mp3 --lang ur --instruct "male, young adult"`; script in the language's own script [repo: library/tools/vs_tts.py]. OmniVoice: Urdu 100%/97%, Hindi 92% Whisper match; its weights are NON-COMMERCIAL, so client/paid work uses `--model voxcpm2` (Apache-2.0) or ai_voice.py [repo: CLAUDE.md "Voice and songs with words"].
- Do NOT use ElevenLabs unless the owner explicitly asks in that request [repo: CLAUDE.md "Rules from the owner"].
- If the owner's material already has a voice, use that voice cleaned with `clean_voice.py`, not a new one [repo: CLAUDE.md "Voice and songs with words"].
- Never run two heavy torch jobs at once on this 4-core box; queue them [repo: CLAUDE.md "Environment facts"].
- A robotic AI voice hurts retention; a natural-sounding voice keeps people watching [Faceless, https://faceless.my/youtube/how-to-make-a-faceless-youtube-channel/, 2026-05-19].

## 6. Music

- Use free open-source music made by others (CC0/public domain); the owner does NOT want our own ACE-Step tracks used unless asked [repo: CLAUDE.md "Environment facts"].
- Library: `library/music/cc0/` (OpenGameArt pages whose licence links only to CC0 1.0; CC BY pages skipped), listed with mood and length in its README [repo: library/music/cc0/README.md].
- More CC0 sources: SoundSafari/CC0-1.0-Music (~7000 songs, ~40 GB) [GitHub, https://github.com/SoundSafari/CC0-1.0-Music]; FreePD has closed (2025) [Wikimedia Commons, https://commons.wikimedia.org/wiki/Commons:Free_media_resources/Music/en]. Findings: library/research/free-music-sources.md [repo: CLAUDE.md "Environment facts"].
- A film over ~15 s that tells something gets music and sound on its visible actions unless silence was asked for [repo: .claude/skills/hyperframes/SKILL.md].

## 7. Assemble in HyperFrames

- `npx hyperframes init <dir>`; `index.html` is the root, one scene per sub-composition in `compositions/`, media and fonts in `assets/` [repo: .claude/skills/hyperframes/SKILL.md].
- Contract: every timed element has `class="clip"`, `data-start`, `data-duration`; one paused timeline registered in `window.__timelines`; no `Date.now()`, unseeded random, timers or `repeat: -1`; root-relative asset paths [repo: .claude/skills/hyperframes/SKILL.md "Contract"].
- Load GSAP from `assets/vendor/gsap-3.14.2.min.js`, never the CDN (render fails with `sub_timeline_script_failure`) [repo: CLAUDE.md "HyperFrames learnings"].
- Every `<audio>` needs `data-duration` = the clip's real length and an `id`; overlapping clips need different `data-track-index` lanes [repo: CLAUDE.md "HyperFrames learnings"; .claude/skills/hyperframes/SKILL.md "Contract"].
- First frame = thumbnail: put a title or key image on screen at 0 s [repo: CLAUDE.md "HyperFrames learnings"].
- `tl.set(..., 0)` does not render on frame 0; also apply initial states with `gsap.set` [repo: CLAUDE.md "CSS 3D voxel films"].
- Keep content inside the 90% action-safe box, captions and key text in 80% title-safe [repo: .claude/skills/hyperframes/SKILL.md]. Vertical: nothing in the top 168 px, words inside 168-1330 px, no text under the right-hand action rail [repo: .claude/skills/hyperframes/references/types/vertical.md].
- Work loop: after the last edit run `npx hyperframes check --json` and fix every error; a film gets `npx hyperframes snapshot --review` + `references/review.md` ending in REVIEW.md; render after check and review [repo: .claude/skills/hyperframes/SKILL.md "Work loop"].
- Captions: Netflix limits 42 characters per line, max two lines, prefer one line [Netflix, https://studiopartner.netflix.net/studio/us-english-timed-text-style-guide]. Repo caption style: per-word blur-in, 0.12 s stagger, over a bottom gradient, one gold accent word per line [repo: CLAUDE.md "Editing a phone video"].
- Light text on a bright background fails contrast: use a deep colour with a light glow, or captions over a bottom gradient veil [repo: CLAUDE.md "HyperFrames learnings"].

## 8. Mix and loudness

- `library/tools/voice_over_music.py spec.json out.wav`: places voice lines on the bed at set times, ducks the bed (`duck_db`), normalises to `lufs` [repo: library/tools/voice_over_music.py]. ffmpeg 6.1 drops `adelay` after concat+atempo, so lines are placed in numpy [repo: CLAUDE.md "Voice and songs with words"].
- Music under a voice sits around 0.14 volume; true peak at -1 dBTP or lower; mix around -16 to -14 LUFS for social; check with `npx hyperframes audio <video> --json` [repo: .claude/skills/hyperframes/references/sound.md].
- Platform targets: TikTok, YouTube and Instagram -14 LUFS-i, -1 dBTP [Level Rebel, https://levelrebel.net/specs/]. YouTube -14 LUFS / -1.0 dBTP [APU Software, https://apu.software/loudness-standards/, 2025-11-26]. Spotify normalises to -14 LUFS per ITU 1770 [Spotify, https://support.spotify.com/us/artists/article/loudness-normalization/].
- LUFS meters use K-weighting: less sensitive below ~100 Hz, more above ~2 kHz [iZotope, https://www.izotope.com/community/blog/mastering-for-streaming-platforms, 2025-07-23].
- Repo-tested levels: music 1.0, impact-bass 0.35-0.4, whoosh 0.6-0.8; measure the render per 0.5 s and with `ebur128` (target about -16 LUFS) [repo: CLAUDE.md "Client phone-video edits"].
- Measure: `ffmpeg -i out.mp4 -af ebur128=peak=true -f null -` [ffmpeg docs, https://ffmpeg.org/ffmpeg-filters.html#ebur128] (ran OK locally).
- Normalise: `ffmpeg -i in.mp4 -af loudnorm=I=-14:TP=-1:LRA=11 -c:v copy -c:a aac -b:a 160k out.mp4` [ffmpeg docs, https://ffmpeg.org/ffmpeg-filters.html#loudnorm] (ran OK locally; re-run 2026-10-24: -21.8 -> -14.0 LUFS, but the output audio came out at 96 kHz, so add `-ar 48000` for 48 kHz).
- A `data-fade-out` on music must start after the last spoken word [repo: CLAUDE.md "Voice and songs with words"].

## 9. Export

- YouTube: MP4, AAC-LC (or Opus), H.264 High Profile, progressive, closed GOP of half the frame rate, 4:2:0, same frame rate as made; SDR bitrates 1080p 8 Mbps (12 at 48-60 fps), 4K 35-45 Mbps; stereo audio 384 kbps; BT.709 [YouTube Help, https://support.google.com/youtube/answer/1722171?hl=en].
- Instagram Reels: aspect 1.91:1 to 9:16, min 30 fps and 720 px [Instagram Help, https://help.instagram.com/1038071743007909]; 1080x1920 recommended, max 4 GB [Hootsuite, https://blog.hootsuite.com/instagram-video-sizes/, 2025-03-12]. API: MP4/MOV, moov atom at the front, AAC max 48 kHz, H.264/HEVC, closed GOP, 4:2:0, 23-60 fps [Justin Searls quoting Instagram API docs, https://justin.searls.co/posts/a-script-to-validate-videos-for-the-instagram-api/, 2025-02-14].
- TikTok: 9:16 ideal [Shopify, https://www.shopify.com/blog/tiktok-video-size, 2024-09-10]; recommended 1080x1920 MP4 [Cloud Campaign, https://cloudcampaignsupport.zendesk.com/hc/en-us/articles/42274647925267-TikTok-Media-Guidelines-Video-Specs-Captions-Limitations]; 23-60 fps, 360-4096 px per side, over 3 s [SmarterQueue, https://help.smarterqueue.com/article/640-tiktok-error-unsupported-media-size-see-video-restrictions-and-photo-restrictions].
- Deliver full quality plus a WhatsApp copy: `ffmpeg -i in.mp4 -c:v libx264 -crf 23 -preset slow -c:a aac -b:a 160k -movflags +faststart out.mp4` [repo: CLAUDE.md "Editing a phone video"; ffmpeg docs, https://ffmpeg.org/ffmpeg-formats.html#MOV_002fMPEG_002d4_002fISOMBFF-muxers] (ran OK locally).
- Hand personal media over with SendUserFile; never commit videos [repo: CLAUDE.md "Rules from the owner"].

## 10. QA checklist

- [ ] Frame 0 shows a title or key image, not black or a logo [repo: CLAUDE.md "HyperFrames learnings"; .claude/skills/hyperframes/references/story.md §3].
- [ ] The first 3 s pass the sound-off test [CapCut, https://www.capcut.com/create/short-form-video-hooks, 2026-06-12].
- [ ] Script word count fits the length (~150 wpm human, ~2.2 words/s TTS) [Parlixa, https://www.parlixa.com/blog/words-per-minute-voice-over, 2026-07-11; repo: .claude/skills/hyperframes/references/film.md].
- [ ] Every visual and track is CC0/PD/no-credit or made here, with its licence page saved [repo: CLAUDE.md "Environment facts"].
- [ ] Every on-screen claim traces to a source [repo: .claude/skills/hyperframes/references/story.md §1].
- [ ] `npx hyperframes check --json` clean; every `<audio>` has `id` and real `data-duration`; GSAP from vendor path [repo: .claude/skills/hyperframes/SKILL.md; CLAUDE.md "HyperFrames learnings"].
- [ ] Snapshots at the QA times looked at before render [repo: CLAUDE.md "CSS 3D voxel films"].
- [ ] `npx hyperframes audio` shows sound where the picture hits; loudness -16 to -14 LUFS, true peak <= -1 dBTP [repo: .claude/skills/hyperframes/references/sound.md].
- [ ] Captions <= 42 characters per line, max 2 lines [Netflix, https://studiopartner.netflix.net/studio/us-english-timed-text-style-guide].
- [ ] Vertical: text inside the 168-1330 px band [repo: .claude/skills/hyperframes/references/types/vertical.md].
- [ ] Export matches the platform spec; WhatsApp copy made [YouTube Help, https://support.google.com/youtube/answer/1722171?hl=en; repo: CLAUDE.md "Editing a phone video"].
- [ ] No ElevenLabs used unless asked; OmniVoice not used for paid work [repo: CLAUDE.md "Rules from the owner"; "Voice and songs with words"].
