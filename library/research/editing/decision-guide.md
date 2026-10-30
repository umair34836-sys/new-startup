# Video type decision guide: what kind of video is this, and exactly how to edit it

How to use it: find the input in the triage table, jump to that type's section, and follow its bullets top to bottom ("Steps here" maps the job to this repo's tools).
Every line ends with its source; repo sources are this repo's own tested notes. Researched 2026-10-24.

## Input triage (what came in -> which section)

| Input kind | First check | Go to section | Source |
| --- | --- | --- | --- |
| Phone clip | ffprobe (rotation, fps), contact sheet every ~0.4 s, find the best moments | Client phone-clip reel, Vlog/travel, Birthday/family | [repo: CLAUDE.md "Editing a phone video into a professional edit (recipe that worked)"] |
| WhatsApp low-fps / low-res clip | r_frame_rate can read 28.4 while the clip is really ~12 fps: check frame pts with `ffprobe -show_entries frame=pts_time` (ran OK locally) | Client phone-clip reel | [repo: CLAUDE.md "Client phone-video edits"]; [FFmpeg Cookbook, https://ffmpeg-cookbook.com/en/articles/change-framerate/, 2026-04-08] |
| Screen recording | Cut dead time first, then zooms and callouts | Tutorial/screen recording/course, Product demo, App/website promo | [TechSmith, https://www.techsmith.com/blog/edit-demo-recording/, 2026-07-07] |
| Talking head | Hook in the first sentence, cut on breaths | Talking-head YouTube, Interview/testimonial | [The Beans Media, https://thebeansmedia.com/how-to-edit-talking-head-videos-for-youtube]; [Addaly, https://addaly.com/learn/video-editing/cutting-a-dialogue-scene] |
| Clip with speech | Use that person's own voice, cleaned: clean_voice.py | Talking head, Interview, Vlog, Podcast | [repo: CLAUDE.md "Voice and songs with words"] |
| Silent clip (Whisper finds no speech) | It becomes a music reel: title at 0 s, one shot per bar | Client phone-clip reel, Dance/trend reel, Slideshow | [repo: CLAUDE.md "Client phone-video edits"] |
| Event footage | Decide the audience first (attendees, sponsors, future buyers) | Event aftermovie, Wedding highlight | [Omebly, https://omebly.com/blog/how-to-edit-an-event-recap-video/, 2026-10-16] |
| Product shots | Edit toward hook, problem, benefit, proof, offer, CTA | Product ad/UGC ad, Product demo/unboxing | [FrameNotion, https://framenotion.com/blog/how-to-edit-product-videos-for-social-ads, 2026-10-08] |
| Photos only | 3 to 5 s per photo, one motion style for all | Slideshow from photos, Birthday/family | [Woven Video, https://www.woven.video/guides/photo-slideshow, 2026-10-19] |
| No footage | Host = the owner's blocky skin (blocky_character.py); voice from ai_voice.py / vs_tts.py | Faceless channel, Explainer, App/website promo | [repo: CLAUDE.md "Rules from the owner"]; [repo: library/README.md "Tools (tools/)"] |
| Game capture | Brighten Nether/night shots; keep game audio under the voice | Gaming/Minecraft | [Reddit r/youtubers, https://www.reddit.com/r/youtubers/comments/11w1lk6/editing_minecraft_videos_protips/, 2023-03-19]; [Umbrella Creators, https://umbrellacreators.com/blog/how-to-edit-gaming-videos-for-youtube, 2026-09-27] |

## Rules that apply to every type

- MUSIC (every type, owner 2026-10-27): pick, cut and mix it with the skill `.claude/skills/music-for-video`: know the type/structure/length -> `find_music.py "<type mood>"` -> listen.py on the top picks -> choose by written reasons -> `music_fit.py --length N [--drop-at T] --check` (bar/phrase joins, drop on the reveal, real ending) -> `mix_vo_music.py` under a VO (no vocals, duck ~10 dB, voice ~15 LU over the bed) -> QA with listen.py -> log the reasons. Type-by-type music profiles with sources: library/research/music-for-video.md section 2. [repo: library/research/music-for-video.md]
- Music must need no credit: use CC0 tracks made by others from `library/music/cc0` (OpenGameArt, Freesound/FreePD and FMA tracks, each licence checked for CC0/public domain only; moods and files in library/music/cc0/README.md); our own ACE-Step songs only when the owner asks. [repo: CLAUDE.md "Environment facts (cloud container)"]; [repo: library/README.md "music/cc0"]; [repo: library/music/cc0/README.md]
- Never commit videos, photos, voices or family data; work on personal media in the session scratchpad and hand it over with SendUserFile. [repo: CLAUDE.md "Rules from the owner"]
- The first frame is the thumbnail: put a title or key image on screen at 0 s. [repo: CLAUDE.md "HyperFrames learnings"]; [Simplified Help, https://help.simplified.com/en/articles/7232323-how-to-add-a-cover-to-instagram-reels, 2024-04-10]
- Vertical export: 1080x1920, 9:16, H.264 MP4, 25 or 30 fps, AAC 48 kHz; keep must-read text out of the top 15% and bottom 20%. [Addaly, https://addaly.com/learn/video-editing/export-settings-per-destination]
- Loudness: no platform publishes a LUFS number (YouTube Help, Meta, TikTok checked 2026-10-27, library/research/music-for-video.md section 8); -14 LUFS is a secondary-source figure; deliver -16 to -14 LUFS, -1 dBTP; our tested target for reels was about -16 LUFS measured with `ebur128` (ran OK locally). [Level Rebel, https://levelrebel.net/specs/]; [repo: CLAUDE.md "Client phone-video edits"]; [ffmpeg docs, https://ffmpeg.org/ffmpeg-filters.html#ebur128]
- WhatsApp copy: `ffmpeg -i in.mp4 -c:v libx264 -crf 23 -preset slow -c:a aac -b:a 160k -movflags +faststart out.mp4` (ran OK locally). [repo: CLAUDE.md "Editing a phone video into a professional edit (recipe that worked)"]; [FFmpeg-cvslog (movenc faststart moves the moov atom to the front), https://ffmpeg.org/pipermail/ffmpeg-cvslog/2013-August/067635.html]
- HyperFrames loop for every type: `npx hyperframes check` before render, then `snapshot --at ...` and look at the frames, then render. [repo: CLAUDE.md "HyperFrames learnings"]
- Grades: compare 2-3 candidates with `npx hyperframes grade-compare` on a real frame, then apply the winner with `media-treatment --apply` (tested payloads: "Cinematic muted", "Romantic glow"). [repo: CLAUDE.md "Editing a phone video into a professional edit (recipe that worked)"]; [repo: library/README.md "Colour grades that worked"]

## 1. Talking-head YouTube

- Goal: the first 30 seconds decide everything; open on the most interesting sentence and end on value, not a wind-down. [The Beans Media, https://thebeansmedia.com/how-to-edit-talking-head-videos-for-youtube]
- Length/aspect: 16:9 long-form for YouTube; vertical cut-downs at 1080x1920. [Woven Video, https://www.woven.video/guides/social-media-video-sizes, 2026-10-19]
- Structure: keep the face on screen for the hook, personal reactions and the final instruction; B-roll enters on the phrase that names the subject. [Zupum, https://zupum.com/learning-hub]
- Cut rhythm: cut on energy, not just silence, and give a new visual every 5 to 7 seconds (punch-in, B-roll, text, angle switch). [The Beans Media, https://thebeansmedia.com/how-to-edit-talking-head-videos-for-youtube]
- Cut rhythm: move every cut to a breath; a cut inside a phrase sounds wrong. [Addaly, https://addaly.com/learn/video-editing/cutting-a-dialogue-scene]
- Transitions: jump cuts are an accepted style; alternate a subtle 105-110% zoom on every other cut so they read as intentional. [Pristine Podcasts, https://app.pristinepodcasts.com/blog/editing-talking-head-video-podcast, 2026-02-11]
- Captions: captions are a retention tool, not optional. [The Beans Media, https://thebeansmedia.com/how-to-edit-talking-head-videos-for-youtube]
- Music/SFX: lay continuous room tone under all speech cuts so the joins disappear; J/L-cut every join. [Addaly, https://addaly.com/learn/video-editing/cutting-a-dialogue-scene]
- Common mistakes: covering the speaker with B-roll just because a few seconds passed; bad audio kills retention faster than bad light. [Zupum, https://zupum.com/learning-hub]; [The Beans Media, https://thebeansmedia.com/how-to-edit-talking-head-videos-for-youtube]
- Steps here: clean the speaker's own voice with `clean_voice.py` (`--fast` MDX-Net in ~43 s for 26 s, full BS-RoFormer ~8 min); captions per word blur-in, 0.12 s stagger, bottom gradient, one gold accent word; check/snapshot/render. [repo: CLAUDE.md "Voice and songs with words"]; [repo: CLAUDE.md "Editing a phone video into a professional edit (recipe that worked)"]

## 2. Podcast / video podcast + clips

- Goal: one full episode plus vertical clips for Shorts, with chapters. [Pacing House, https://pacinghouse.com/guides/how-to-edit-a-podcast-video/, 2026-10-16]
- Length/aspect: clips in 9:16, 1:1, 4:5 and 16:9 from one transcript. [Castmagic, https://www.castmagic.io/tools/podcast-clip-generator]
- Structure: group every camera and the sound recording into one multicam clip, switch to whoever talks, then tighten pauses, then a sound pass per mic, then pull clips. [B/side, https://bside.video/learn/how-to-edit-a-multicam-podcast/, 2026-10-06]
- Cut rhythm: the camera follows whoever is speaking; the microphones show who that is. [podswitch, https://www.usepodswitch.com/guides/how-to-edit-a-multicam-podcast, 2026-10-06]
- Cut rhythm (clips): start every clip on a full sentence. [FastClip, https://fastclips.app/podcast-clip-maker]
- Transitions: in vertical clips, a split screen stacks both people when both are in the shot. [Clyps, https://clyps.ai/podcast-clip-generator]
- Grade: match colour across cameras. [Pacing House, https://pacinghouse.com/guides/how-to-edit-a-podcast-video/, 2026-10-16]
- Captions: about 25 characters a line, up to three lines on vertical (BBC); contrast at least 4.5:1 (WCAG); fix names and numbers in auto captions. [FastClip, https://fastclips.app/podcast-clip-maker]
- Common mistakes: waveform sync fails with no shared sound, steady room hum, or non-overlapping recordings. [Addaly, https://addaly.com/learn/video-editing/syncing-and-multicam]
- Steps here: clean each voice with `clean_voice.py`; hook-proof-payoff clips that end where a rewatch feels natural; check/snapshot/render; vertical export numbers above. [repo: CLAUDE.md "Voice and songs with words"]; [Hookspring, https://hookspring.com/blog/first-three-seconds, 2026-10-20]

## 3. Interview / testimonial

- Goal: open on tension, find the first line with stakes, go quickly to the decision moment, end on change. [Testimonial.to, https://testimonial.to/resources/testimonial-video-editing, 2026-06-18]
- Length/aspect: 30 seconds to two minutes depending on the platform. [Pippit, https://www.pippit.ai/resource/best-practices-for-editing-customer-testimonial-videos, 2025-05-19]
- Structure: condense rambling answers into one punchy statement ("frankenbite") without changing the meaning. [7 Hills Productions, https://7hillsproductions.com/advanced-techniques-for-editing-testimonial-videos/, 2024-03-17]
- Cut rhythm: with two cameras on the same side of the eyeline (~30 degrees apart), hide joins by switching angles, leaving B-roll free to show what the speaker describes. [MediaScaleUp, https://mediascaleup.com/post/a-practical-guide-to-interview-and-talking-head-editing-video, 2025-09-12]
- Transitions: B-roll covers jump cuts, gives visual evidence for claims and breaks up a single-camera setup. [Cutback, https://cutback.video/blog/how-to-add-broll-to-a-longform-interview-or-podcast]
- Captions: subtitles matter because many feed videos play without sound. [Pippit, https://www.pippit.ai/resource/best-practices-for-editing-customer-testimonial-videos, 2025-05-19]
- Music/SFX: if the story is weak, don't fake force with music or motion. [Testimonial.to, https://testimonial.to/resources/testimonial-video-editing, 2026-06-18]
- Common mistakes: switching eye contact between lens and off-lens, and unnecessary jump cuts. [Larry Jordan, https://larryjordan.com/articles/better-one-camera-editing-techniques/, 2020-04-05]
- Steps here: `clean_voice.py` on the real voice (never a generated one for a video that has a voice); `voice_over_music.py`-style ducking keeps a bed 8 dB under speech; CC0 bed from library/music/cc0. [repo: CLAUDE.md "Voice and songs with words"]; [repo: library/README.md "Tools (tools/)"]; [repo: library/README.md "music/cc0"]

## 4. Documentary / mini-doc

- Goal: interviews (or their audio) anchor each sequence and the editor backs up what is said with images that give evidence for it (evidentiary editing). [Beverly Boy Productions, https://beverlyboy.com/filmmaking/how-does-continuity-cutting-differ-from-evidentiary-editing/, 2021-05-05]
- Structure: make selects, then a rough assembly from the strongest selects only, starting with an audio-only "radio cut" of interviews and narration. [LibreTexts, https://human.libretexts.org/Bookshelves/Theater_Film_and_Storytelling/Documentary_Culture/15%3A_Editing_the_Documentary/15.03%3A_Building_Assemblies, 2026-01-17]
- Cut rhythm: tell a story with the B-roll too; rather keep a jump cut in than cover it with random footage that doesn't fit. [NYFA, https://www.nyfa.edu/student-resources/how-to-edit-an-interview-for-a-documentary/, 2014-05-28]
- Transitions: the Ken Burns effect puts still photographs in motion with slow zooms and pans (named after the documentarian; used when film or video material is not available). [Wikipedia, https://en.wikipedia.org/wiki/Ken_Burns_effect, checked 2026-10-24]
- Common mistakes: treating archival as just "wallpaper" B-roll. [Sundance Institute, https://www.sundance.org/blogs/contemplating-the-cut-takeaways-and-tips-for-documentary-editors-3/, 2017-06-26]; [IDA, https://documentary.org/feature/no-longer-just-wallpaper-archival-footage-can-inform-and-shape-your-films-story, 2013-04-01]
- Common mistakes: no naming system for archive sources; use a consistent shorthand and numbering. [IDA, https://www.documentary.org/blog/6-essential-tips-using-archival-footage, 2013-08-14]
- Steps here: spoken narration with zero music via `ai_voice.py` or `vs_tts.py` (VoiceStudio; OmniVoice is non-commercial, client work uses `--model voxcpm2` or ai_voice.py); mix with `voice_over_music.py`; cinematic/piano CC0 bed. [repo: CLAUDE.md "Voice and songs with words"]; [repo: library/README.md "music/cc0"]

## 5. Vlog / travel

- Goal and length: a 2-4 minute travel film from many clips. [Aerial Media, https://aerialmedia.com/resources/cinematic-travel-video-photographers-guide/, 2026-02-27]
- Structure: rough selects first at 2-4x shuttle speed, marking in/out; aim to cut 60-70% of the footage at this stage. [EditBuddy, https://editbuddy.app/blog/how-to-edit-travel-vlogs-premiere-pro, 2026-04-29]
- Cut rhythm: pacing is not just cut speed; it is also the frame you cut on and the length of each sequence (unverified). [YouTube (Aidin Robbins, "How to Nail the PACING of your Travel Film"), https://www.youtube.com/watch?v=W0ssQOv7s4c, 2020-03-28]
- Cut rhythm: jump-cutting a direct-address monologue is a core vlog convention. [First Monday, https://firstmonday.org/ojs/index.php/fm/article/download/10547/11266]
- Transitions: change scene on a beat or during a pause in the track. [Splice, https://spliceapp.com/blog/editing-travel-vlogs-with-music/, 2026-06-22]
- Music/SFX: let the place's own sound play 2-3 s on establishing shots, with a music bed underneath for continuity. [Umbrella Creators, https://umbrellacreators.com/blog/youtube-editor-for-travel-vlogs, 2026-04-24]
- Steps here: phone recipe (ffprobe, contact sheet, cut on bars, grade-compare); `clean_voice.py` on spoken parts; travel-ambient CC0 tracks; WhatsApp copy. [repo: CLAUDE.md "Editing a phone video into a professional edit (recipe that worked)"]; [repo: library/music/cc0/README.md]

## 6. Wedding highlight

- Goal: build the film on what people said (vows, toasts, private words); deliver a 3-5 min highlight, the full ceremony, each speech, and a one-minute vertical teaser. [Eddie AI, https://www.heyeddie.ai/how-to/edit-wedding-videos]
- Structure: Opening (one universal emotional line over slow details), Build (speeches tell the love story, 2-3 speakers max), Ceremony/climax (best vow lines, rings, kiss; music peaks), Resolution (recessional, lighter toast), Closing (one final line, couple walking away, music fades to black). [RoughCut, https://roughcut.com/blog/how-to-structure-wedding-highlight-film, 2026-04-05]
- Structure: build the "spine" of 5-8 moments with no music or dissolves first; music serves the structure, not creates it. [Wedit, https://wedit.video/wedding-video-editing/, 2026-08-04]
- Cut rhythm: keep clips 3-15 s; pick a track with soft intro, build and peak at 90-110 BPM. [Pulse Edit, https://pulseedit.com/blog/wedding-highlight-reel-davinci-resolve.html, 2026-04-28]
- Grade: "Romantic glow" payload for indoor phone footage with harsh window light. [repo: library/README.md "Colour grades that worked"]
- Music/SFX: natural audio (vows, speeches, officiant) gives the film its emotional direction. [Blue Moon Video, https://www.bluemoonvideoproductions.com/post/wedding-film-editing-process, 2026-07-06]
- Common mistakes: starting with the vows, a joke or a long speech; rushing the vows; cutting vows with speech audio. [RoughCut, https://roughcut.com/blog/how-to-structure-wedding-highlight-film, 2026-04-05]
- Steps here: personal media stays in the scratchpad; `clean_voice.py` for vows; `floating_hearts.py` overlay, light-leak block; `desi-eastern--wedding-ceremony-music.mp3` from library/music/cc0; SendUserFile. [repo: CLAUDE.md "Rules from the owner"]; [repo: library/music/cc0/README.md]; [repo: library/README.md "Tools (tools/)"]; [repo: library/README.md "Blocks (blocks/)"]

## 7. Event aftermovie / corporate recap

- Goal: make someone who wasn't there wish they had been. [Cevylo, https://cevylo.com/festival-aftermovie-editing-guide, 2026-08-05]
- Length/aspect: 90 s to 3 min main cut, plus a 60 s vertical version from the same project. [Cevylo, https://cevylo.com/festival-aftermovie-editing-guide, 2026-08-05]
- Structure (aftermovie): cold open 0-10 s, arrival 10-30 s, build 30-60 s, drop at ~1:00 on the best crowd moment, peak 1:00-2:00 (varied), comedown, tag with logo and next dates. [Cevylo, https://cevylo.com/festival-aftermovie-editing-guide, 2026-08-05]
- Structure (corporate): radio edit of the best speaker lines first, then match B-roll to each line. [Shafin Taosif Studio, https://shafintaosifstudio.com/blog/how-to-edit-an-event-video/, 2026-10-14]
- Cut rhythm: open on the most visually compelling moment, not chronologically; cut on the beat; alternate wides with tight speaker and audience close-ups; 2-3 short quotes; close forward-looking. [Editing Machine, https://editingmachine.com/blog/event-recap-video-editing, 2026-07-19]
- Transitions: cut between synced multicam angles: wide, close-ups of key moments, crowd reactions. [Adobe Video World, https://adobevideoworld.com/event-video-editing/, 2026-06-26]
- Music/SFX: choose one track with a real build and drop before touching clips. [Cevylo, https://cevylo.com/festival-aftermovie-editing-guide, 2026-08-05]
- Common mistakes: editing from clips sent through messaging apps; missing a promised sponsor, person or logo. [Omebly, https://omebly.com/blog/how-to-edit-an-event-recap-video/, 2026-10-16]; [AutoEdit, https://autoedit.elevenpercent.net/learn/blog/corporate-event-recap]
- Steps here: CC0 upbeat/electronic track from library/music/cc0, cut on bars; mix levels music 1.0, impact-bass 0.35-0.4, whoosh 0.6-0.8; vertical export. [repo: library/music/cc0/README.md]; [repo: CLAUDE.md "Client phone-video edits"]

## 8. Birthday / family memory

- Goal: a clear feeling, a few meaningful photos, a simple structure (e.g. childhood-to-now). [PhotoForVideo, https://photoforvideo.com/blog/birthday-video-ideas]
- Structure: ideas that work: slideshow, video greeting card, year recap, gift reveal, life story. [InVideo, https://invideo.io/blog/birthday-video-ideas/, 2022-01-27]; [Clipchamp, https://clipchamp.com/en/blog/birthday-video-ideas-friends-family-colleagues/, 2021-10-05]
- Cut rhythm: two or three strong images can say more than twenty random ones. [PhotoForVideo, https://photoforvideo.com/blog/birthday-video-ideas]
- Transitions: slow-mo for emotion, freeze frame end made seamless from the last slow-mo frame. [repo: CLAUDE.md "Editing a phone video into a professional edit (recipe that worked)"]
- Captions: add the age or a short message as a caption. [PhotoForVideo, https://photoforvideo.com/blog/birthday-video-ideas]
- Common mistakes: committing family media, names or captions about family to GitHub. [repo: CLAUDE.md "Rules from the owner"]
- Steps here: work only in the scratchpad; smooth slow-mo `minterpolate=fps=<30/rate>:mi_mode=mci:mc_mode=aobmc:vsbmc=1,setpts=PTS/<rate>` (ran OK locally); `floating_hearts.py --burst-at` for the end card; kids-cute or happy CC0 track; SendUserFile + WhatsApp copy. [repo: CLAUDE.md "Editing a phone video into a professional edit (recipe that worked)"]; [ffmpeg docs, https://ffmpeg.org/ffmpeg-filters.html#minterpolate]; [repo: library/README.md "Tools (tools/)"]; [repo: library/music/cc0/README.md]

## 9. Product ad / UGC ad

- Goal: one video, one primary objection. [Nereo, https://www.nereo.io/blog/ecommerce-product-video, 2026-09-28]
- Length/aspect: 15-30 s, 9:16 primary, built to work with sound off. [FrameNotion, https://framenotion.com/blog/how-to-edit-product-videos-for-social-ads, 2026-10-08]
- Structure: 0-2 s hook (product in use + bold claim), 2-8 s problem, 8-20 s demo with benefit captions, 20-28 s proof, last 4 s CTA with offer. [Vortex Xcel, https://vortexxcel.com/ugc-ads-ecommerce-editing/, 2026-07-11]
- Cut rhythm: 2-3 s cuts in the hook, 4-5 s in the body, back to 2-3 s into the CTA, one clean hold at the close. [Flare, https://joinflare.app/blog/ugc-video-editing-pacing-conversions, 2026-08-13]
- Transitions: jump cuts for momentum; B-roll inserts for proof of a claim and to bridge two takes. [Flare, https://joinflare.app/blog/ugc-video-editing-pacing-conversions, 2026-08-13]
- Captions: punchy captions with the spoken word highlighted; keep them inside UI safe zones. [Eddie AI, https://www.heyeddie.ai/how-to/edit-ugc-ads]; [Editing Machine, https://editingmachine.com/blog/ugc-video-editing-for-ads-scaling-authenticity, 2026-03-07]
- Music/SFX: light music under the creator. [Eddie AI, https://www.heyeddie.ai/how-to/edit-ugc-ads]
- Common mistakes: a slow brand intro before the product moment; over-polishing so it reads as an ad. [Billo, https://billo.app/blog/ugc-video-editing/, 2025-04-29]; [Vortex Xcel, https://vortexxcel.com/ugc-ads-ecommerce-editing/, 2026-07-11]
- Steps here: build one body and one version per hook (3-5 hooks); clean voice with `clean_voice.py`; CC0 bed; check/snapshot/render each variant. [Eddie AI, https://www.heyeddie.ai/how-to/edit-ugc-ads]; [repo: CLAUDE.md "Voice and songs with words"]; [repo: CLAUDE.md "HyperFrames learnings"]

## 10. Product demo / unboxing

- Goal: write one sentence first: "after this demo the viewer should believe they can do X". [FrameCompose, https://www.framecompose.com/guides/how-to-make-a-product-demo-video, 2026-08-30]
- Structure: trim dead air, zoom on what matters, add captions, tighten pacing; raw demos are often 40-60% filler. [InstaDemo, https://instademo.app/blog/how-to-edit-a-product-demo-video-beginner-guide, 2026-10-16]
- Cut rhythm: cut mistakes, pauses and dead air before any effects, branding or captions. [TechSmith, https://www.techsmith.com/blog/edit-demo-recording/, 2026-07-07]
- Transitions: picture-in-picture of a close-up angle over the wide reaction shot. [Clipchamp, https://clipchamp.com/en/blog/how-to-edit-unboxing-videos/, 2023-08-30]
- Structure (unboxing): reveal the product name as it enters frame, show it doing its thing, keep it short, use cutaways. [Epidemic Sound, https://www.epidemicsound.com/blog/unboxing-videos/, 2024-04-11]
- Common mistakes: empty states and fake-looking data; use a realistic account. [FrameCompose, https://www.framecompose.com/guides/how-to-make-a-product-demo-video, 2026-08-30]
- Steps here: voiceover with `vs_tts.py` / `ai_voice.py` (zero music) then `voice_over_music.py` over a CC0 bed; HyperFrames zoom tweens on a wrapper div; check/snapshot/render. [repo: CLAUDE.md "Voice and songs with words"]; [repo: CLAUDE.md "Editing a phone video into a professional edit (recipe that worked)"]

## 11. Real-estate walkthrough

- Goal: show the property clearly, in a logical route, leading with the strongest feature. [Async, https://async.com/blog/how-to-make-a-real-estate-video/, 2026-10-01]
- Length/aspect: plan horizontal and vertical-safe options for the opening, signature feature and close. [Westby, https://www.westby.ai/resources/real-estate-video-shot-list, 2026-07-26]
- Structure: exterior, entry, living, kitchen, primary bedroom, standout detail, outdoor, call to action, without doubling back. [Async, https://async.com/blog/how-to-make-a-real-estate-video/, 2026-10-01]
- Structure: first a silent spatial cut, then the property argument, then style, then finish. [Flickspeed, https://www.flickspeed.ai/guides/real-estate-video-editing]
- Cut rhythm: 2-4 s clips cut on the beat; split a room that needs longer into wide + detail. [Propfade, https://propfade.com/real-estate-video/walkthrough-videos/, 2026-06-05]
- Cut rhythm: slow down in high-stakes rooms, speed through connectors. [VirtualTourEasy, https://virtualtoureasy.com/articles/video-editing-real-estate/, 2026-06-11]
- Transitions: motion-matched cuts for continuity; dissolves only for softer shifts. [VirtualTourEasy, https://virtualtoureasy.com/articles/video-editing-real-estate/, 2026-06-11]
- Grade: one colour pass to even brightness and warmth across rooms (window shots run cool). [Propfade, https://propfade.com/real-estate-video/walkthrough-videos/, 2026-06-05]
- Captions: price, beds/baths and address on screen in the first ten seconds. [Propfade, https://propfade.com/real-estate-video/walkthrough-videos/, 2026-06-05]
- Music/SFX: pick the track first; warm acoustic/piano for period and family homes, minimal electronic for modern builds. [Macourt Media, https://macourtmedia.com/blog/listing-video-music-and-pacing/, 2026-08-15]
- Steps here: piano or lofi CC0 track; grade-compare on a real frame; vertical + 16:9 renders; WhatsApp copy for the agent. [repo: library/README.md "music/cc0"]; [repo: CLAUDE.md "Editing a phone video into a professional edit (recipe that worked)"]

## 12. Gaming / Minecraft (FireCraft SMP promo)

- Goal: watch time drives the algorithm; a consistent, recognisable thumbnail style conditions clicks. [VideoHighlight (Dream analysis), https://videohighlight.com/v/PVsLIPTdm6U, 2024-05-24]
- Structure: no intro longer than 3 seconds (no intro is preferable for many). [Reddit r/youtubers, https://www.reddit.com/r/youtubers/comments/11w1lk6/editing_minecraft_videos_protips/, 2023-03-19]
- Cut rhythm: zooms, SFX hits and labels only point at moments that already work; add text for context the viewer lacks (a name, a number, a rule). [Umbrella Creators, https://umbrellacreators.com/blog/how-to-edit-gaming-videos-for-youtube, 2026-09-27]
- Grade: brighten Nether and night footage. [Reddit r/youtubers, https://www.reddit.com/r/youtubers/comments/11w1lk6/editing_minecraft_videos_protips/, 2023-03-19]
- Common mistakes: environment sounds too loud for viewers; nonstop flashing, SFX and subtitles (the kids-video style) can feel like overstimulation. [Reddit r/youtubers, https://www.reddit.com/r/youtubers/comments/11w1lk6/editing_minecraft_videos_protips/, 2023-03-19]; [Plugged In, https://www.pluggedin.com/youtube-reviews/eystreem/, 2026-10-13]
- Music/SFX: the CC0 set has a cinematic group (epic, choir, battle, boss-battle symphonic metal) for promos. [repo: library/README.md "music/cc0"]; [repo: library/music/cc0/README.md]
- Steps here: start from the repo `video/` folder (FireCraft Season 2 launch video, template for promos); `ember_background.py` background; blocky host from `host-skin.png`; server facts from library/research/firecraft-smp.md; capture firecraft.fun with `web_capture.py`. [repo: CLAUDE.md "Rules from the owner"]; [repo: library/README.md "Tools (tools/)"]; [repo: library/README.md "research/"]; [repo: CLAUDE.md "Environment facts (cloud container)"]

## 13. Music video / lip-sync

- Goal: three formats: wild picture cut to music, lip-sync performance, or both. [Video Edit Systems, http://www.videoeditsystems.com/358_CTVA/Shooting%20to%20Sync%20Playback%202.pdf]
- Structure: drop markers on downbeats; calm cutting in the verse, faster in the chorus or drop; edit to one reference mix. [Hanna Eng, https://www.hanna-eng.com/guides/monter-un-clip-musical/, 2026-06-03]
- Cut rhythm: lock sync on a sharp moment: a snare or plosive spike in the take lines up with the same spike in the track. [Hanna Eng, https://www.hanna-eng.com/guides/monter-un-clip-musical/, 2026-06-03]
- Cut rhythm: fold cuts along the lyrics first, then punctuate on the beat; cutting only on beats gets predictable. [Chief, https://www.chief.tv/post/the-nuance-of-editing-music-videos, 2024-07-31]
- Transitions: land cuts on visual cues (a performer moving or turning) or audio cues. [Mineral Sound, https://www.mineralsound.com/blog/timing-your-cuts]
- Transitions: close-up on the hook and vocal, wide on the instrumental; change angle on section changes. [Hanna Eng, https://www.hanna-eng.com/guides/monter-un-clip-musical/, 2026-06-03]
- Common mistakes: mouth shapes drifting from the lyric even when the waveform is close; use consonants and breaths. [MelodicPal, https://www.melodicpal.ai/blog/sync-video-to-audio]
- Steps here: the `blocky-monsoon` template is a full 60 s voxel music video; songs with vocals only when the owner asks (`ai_song.py`, loved recipe seed 7, 80 BPM); align lines with dp_align.py, never greedy. [repo: library/README.md "Templates (templates/)"]; [repo: CLAUDE.md "Environment facts (cloud container)"]; [repo: CLAUDE.md "Voice and songs with words"]

## 14. Dance / trend reel

- Goal: trends are repeatable formats (a hook, a few beats, often a sound) copied by many accounts at once. [Postdom, https://postdom.com/blog/tiktok-trends, 2026-10-08]
- Length/aspect: 9:16 vertical fills the phone screen [Superprofile, https://superprofile.bio/guides/instagram-reel-size, checked 2026-10-24]; quick-trend clips of 10-15 s can rack up views through high replay value and completion rate. [Shortimize, https://www.shortimize.com/blog/video-length-sweet-spots-tiktok-reels-shorts, 2025-12-01]
- Structure: add the music first, mark beats manually where you hear strong drops (auto beats add extras), split clips on the beat points. [Ka Production, https://thekaproduction.com/2026/01/26/trending-transition-reels-editing-capcut/, 2026-01-26]
- Transitions: cut-out transition: freeze just before the beat, remove background, white stroke, keyframe it with a cubic ease. [Ka Production, https://thekaproduction.com/2026/01/26/trending-transition-reels-editing-capcut/, 2026-01-26]
- Transitions: make it loop: end on a frame that leads into the first, trim music to whole bars before a downbeat. [EasyReels, https://easyreels.io/blog/seamless-loop-reel, 2026-10-10]
- Common mistakes: using a trending copyrighted song; we never download copyrighted songs (ask the owner to upload an MP3 they have). [repo: CLAUDE.md "Environment facts (cloud container)"]
- Steps here: CC0 upbeat track, cut one shot per bar; interpolate every clip to 30 fps; check/snapshot/render. [repo: library/README.md "music/cc0"]; [repo: library/music/cc0/README.md]; [repo: CLAUDE.md "Client phone-video edits"]; [repo: CLAUDE.md "HyperFrames learnings"]

## 15. Tutorial / screen recording / course

- Goal: outline 3-5 key steps before recording; record at 1080p, 30 fps, in a clean workspace. [Screenify Studio, https://www.screenify.studio/record/how-to/record-a-tutorial]
- Structure: beginning (topic and why it matters), core content with examples, summary of takeaways. [Teachers Institute, https://teachers.institute/design-development-and-delivery-of-courseware/shoot-edit-educational-videos/, 2025-10-02]
- Cut rhythm: cut loading screens, long typing, menu hunting and hesitations; speed-ramp what must stay. [Kredos Media, https://www.kredosmedia.com/article/screen-recording-editing]
- Transitions: push in on the part of the screen that matters, then pull back out for context [Kredos Media, https://www.kredosmedia.com/article/screen-recording-editing]; back-to-back manual zooms make a pan without zooming out. [Tella, https://www.tella.com/help/editing/edit-a-video]
- Captions: accurate captions and mobile readability. [Udemy, https://teach.udemy.com/recording/editing-tips/, 2025-09-15]
- Common mistakes: tiny text from huge screens, personal data on screen; use demo data and record one step per take. [Kredos Media, https://www.kredosmedia.com/article/screen-recording-editing]
- Common mistakes: over-cutting. [Udemy, https://teach.udemy.com/recording/editing-tips/, 2025-09-15]
- Steps here: narration with `vs_tts.py` or `ai_voice.py`, or the recorder's own voice through `clean_voice.py`; HyperFrames scale/x/y tweens on a wrapper for zooms; check/snapshot/render. [repo: CLAUDE.md "Voice and songs with words"]; [repo: CLAUDE.md "Editing a phone video into a professional edit (recipe that worked)"]; [repo: CLAUDE.md "HyperFrames learnings"]

## 16. Explainer / educational

- Goal: make a concept clear: problem or topic, then the explanation, then a takeaway. [Adobe Video World, https://adobevideoworld.com/explainer-video-editing/, 2026-06-26]
- Structure: keep asking "so what?" and connect the subject to everyday life. [Descript, https://www.descript.com/blog/article/making-better-educational-videos, 2024-09-10]
- Cut rhythm: remove long pauses, filler words, false starts and tangents. [Teachers Institute, https://teachers.institute/design-development-and-delivery-of-courseware/shoot-edit-educational-videos/, 2025-10-02]
- Transitions: explainers use stock footage + motion graphics + text overlays. [faceless-content-guide (GitHub), https://github.com/jakeolschewski/faceless-content-guide]
- Captions: add only visuals that support key ideas, not clutter. [Udemy, https://teach.udemy.com/recording/editing-tips/, 2025-09-15]
- Steps here: blocky host (`blocky_character.py --moves` idle/wave/talk/point) presents; voice from `vs_tts.py`/`ai_voice.py`; CC0 background/lofi bed ducked by `voice_over_music.py`. [repo: library/README.md "Tools (tools/)"]; [repo: CLAUDE.md "Rules from the owner"]; [repo: library/README.md "music/cc0"]

## 17. Faceless channel

- Goal: voiceover over B-roll, screen recordings, animation or archive; cut to the voiceover and change the picture with purpose. [Pacing House, https://pacinghouse.com/guides/faceless-youtube-video-editing/, 2026-10-17]
- Structure: script first: hook, promise, sections, payoff; note what the viewer sees on every line. [Pacing House, https://pacinghouse.com/guides/faceless-youtube-video-editing/, 2026-10-17]
- Cut rhythm: cuts fall on stressed words or phrase ends; a visual change every few seconds, each with a reason. [Pacing House, https://pacinghouse.com/guides/faceless-youtube-video-editing/, 2026-10-17]
- Grade: lock one style prompt / look for every image so it doesn't read as slideshow chaos. [Longform Studio, https://longformstudio.app/articles/how-to-make-faceless-youtube-videos, 2026-08-11]
- Captions: fonts, colours, caption style, lower-third and grade stay the same every video. [Pacing House, https://pacinghouse.com/guides/faceless-youtube-video-editing/, 2026-10-17]
- Music/SFX: music changes with sections and ducks under the voice; whoosh on transitions, click on text pops. [Pacing House, https://pacinghouse.com/guides/faceless-youtube-video-editing/, 2026-10-17]
- Common mistakes: random clips that only loosely match the narration; stock clips every other channel uses. [Pacing House, https://pacinghouse.com/guides/faceless-youtube-video-editing/, 2026-10-17]; [Stitchr, https://stitchr.app/blog/faceless-youtube-video-production-pipeline, 2026-07-03]
- Steps here: `ai_voice.py` / `vs_tts.py` narration; bundled SFX via `npx hyperframes media-use resolve --type sfx`; CC0 bed. [repo: CLAUDE.md "Voice and songs with words"]; [repo: library/README.md "Sound effects (sfx/)"]; [repo: library/README.md "music/cc0"]

## 18. News / explainer short

- Goal and length: a package of ~90 s to 2 min, understandable to someone who knows nothing of the story. [Infinite Creation, https://infinitecreation.io/tutorial-news-package-editing]
- Structure: hook, narration context, first interview clip, more detail, a second voice, close that resolves or points forward. [Infinite Creation, https://infinitecreation.io/tutorial-news-package-editing]
- Cut rhythm: open on the strongest image with natural sound, never narration over silence. [Infinite Creation, https://infinitecreation.io/tutorial-news-package-editing]
- Captions: social newsreels must work with or without audio; "innertitles" over moving or still backgrounds. [Wikimedia Foundation, https://wikimediafoundation.org/news/2018/01/11/how-to-video-newsreel/, 2018-01-11]
- Music/SFX: mobile news is watched in crowded places, so music is common; edit to the beat with markers. [Multimedia Train, http://www.multimediatrain.com/short-news-video-editing/]
- Common mistakes: narration over unrelated or repeated B-roll; shoot about three times the finished duration. [Infinite Creation, https://infinitecreation.io/tutorial-news-package-editing]
- Steps here: free images from Wikimedia Commons (allowed host), verify licence; narration via `vs_tts.py`; check/snapshot/render. [repo: CLAUDE.md "Environment facts (cloud container)"]; [repo: CLAUDE.md "Voice and songs with words"]; [repo: CLAUDE.md "HyperFrames learnings"]

## 19. Reaction

- Goal: the viewer follows the original while seeing your response at the moments that matter. [CapCut, https://www.capcut.com/create/picture-in-picture-editing-reaction-videos, 2026-08-12]
- Structure: source on the lower layer, face cam above; sync on a marker; show the face only when it adds something. [CapCut, https://www.capcut.com/create/picture-in-picture-editing-reaction-videos, 2026-08-12]
- Transitions: PiP, split screen, jump cuts and zoom-ins on dramatic moments. [Clipchamp, https://clipchamp.com/en/blog/youtube-reaction-videos/, 2022-03-10]
- Common mistakes: PiP covering subtitles, HUDs or lower thirds; assuming one alignment holds for the whole recording. [CapCut, https://www.capcut.com/create/picture-in-picture-editing-reaction-videos, 2026-08-12]
- Common mistakes: not using headphones while recording; dead air. [Kapwing, https://www.kapwing.com/resources/how-to-make-a-reaction-video/, 2021-01-13]
- Steps here: `clean_voice.py` on the commentary; captions over a bottom veil; check/snapshot/render. [repo: CLAUDE.md "Voice and songs with words"]; [repo: CLAUDE.md "HyperFrames learnings"]

## 20. Sports / montage highlights

- Goal: a compact story, not a pile of exciting clips. [CapCut, https://www.capcut.com/create/sports-highlight-editing-that-gets-shared, 2026-08-12]
- Structure: hook, context, setup, action, clarification, reaction; lead with the payoff (e.g. begin with the save), then return to the cross or shot that created the chance. [CapCut, https://www.capcut.com/create/sports-highlight-editing-that-gets-shared, 2026-08-12]
- Captions: one clean context card (minute, score, label like "Winning Goal"). [CapCut, https://www.capcut.com/create/sports-highlight-editing-that-gets-shared, 2026-08-12]
- Cut rhythm: show key action at full speed first; replay only to answer a real question. [CapCut, https://www.capcut.com/create/sports-highlight-editing-that-gets-shared, 2026-08-12]
- Transitions: slow motion sparingly, for emotional moments. [Studio 91, https://www.studio91media.co.uk/2021/04/30/how-to-use-slow-motion-to-create-emotion/, 2021-04-30]
- Structure: gather 20-40 short raw clips for a single reel; most get cut down to a few seconds or dropped. [ReelWorkshop, https://reelworkshop.com/use-cases/sports-highlight-compilation]
- Steps here: minterpolate slow-mo (ran OK locally); cinematic/battle CC0 track; impact-bass 0.35-0.4 to avoid impacts 8 dB over music. [repo: CLAUDE.md "Editing a phone video into a professional edit (recipe that worked)"]; [repo: CLAUDE.md "Client phone-video edits"]; [repo: library/README.md "music/cc0"]; [ffmpeg docs, https://ffmpeg.org/ffmpeg-filters.html#minterpolate]

## 21. Fitness

- Goal: decide first: demonstration, correction (form check) or follow-along session; they are three different films. [Vidmoat, https://www.vidmoat.com/blog/edit-fitness-videos, 2026-09-04]
- Cut rhythm: demo at real speed with one slow repeat; correction at 0.25-0.5x with freezes; session at exactly 1x for its whole length. [Vidmoat, https://www.vidmoat.com/blog/edit-fitness-videos, 2026-09-04]
- Structure: keep hands, feet and the whole movement in frame. [Vidmoat, https://www.vidmoat.com/use-cases/fitness]
- Captions: text overlays and graphics give the instructions. [CapCut, https://www.capcut.com/create/fitness-video-maker]
- Common mistakes: one edit doing all three jobs (slow-mo + timer + hype track + caption in 20 s); speeding up a follow-along. [Vidmoat, https://www.vidmoat.com/blog/edit-fitness-videos, 2026-09-04]
- Steps here: set the frame rate from the highest-fps footage; minterpolate slow-mo for form (ran OK locally); upbeat-electronic CC0. [Vidmoat, https://www.vidmoat.com/blog/edit-fitness-videos, 2026-09-04]; [repo: CLAUDE.md "Editing a phone video into a professional edit (recipe that worked)"]; [repo: library/README.md "music/cc0"]; [repo: library/music/cc0/README.md]

## 22. Cooking / recipe

- Goal: overhead is the default spine; it makes the hands feel like the viewer's own. [Animoto (Tasty), https://animoto.com/blog/video-ideas/tips-tasty-style-recipe-video, 2018-10-18]
- Structure: overhead for instructions, low angles as punctuation for sear, pour, fold, cut-through. [Vidmoat, https://www.vidmoat.com/blog/edit-cooking-videos, 2026-09-04]
- Cut rhythm: cut to the side angle a beat before the moment; back overhead as it resolves. [Vidmoat, https://www.vidmoat.com/blog/edit-cooking-videos, 2026-09-04]
- Captions: ingredient visible ~0.5 s before it moves; quantity on screen ~2 s ("show it, name it, do it"). [Vidmoat, https://www.vidmoat.com/blog/edit-cooking-videos, 2026-09-04]
- Common mistakes: only overhead, which gets repetitive. [Animoto, https://animoto.com/blog/video-ideas/tips-tasty-style-recipe-video, 2018-10-18]
- Steps here: happy/lofi CC0 bed; per-word captions over a bottom gradient; vertical export. [repo: library/README.md "music/cc0"]; [repo: CLAUDE.md "Editing a phone video into a professional edit (recipe that worked)"]; [Vidmoat, https://www.vidmoat.com/blog/edit-cooking-videos, 2026-09-04]

## 23. Trailer / teaser

- Goal: trailers start big and end big; the cold open is its own act. [Derek Lieu, https://derek-lieu.medium.com/the-matrix-and-movie-trailer-3-act-structure-b06a68e01214, 2018-05-03]
- Structure: hook (first 5-15 s), setup, turn (the drop, on a beat or smash cut), escalation montage, button, title & info. [Filmmaker Genius, https://filmmakergenius.com/academy/how-to-make-a-film-trailer/film-trailer-structure]
- Cut rhythm: acts with a key plot point and a music change between each; title and button at the end. [Neil Oseman, https://neiloseman.com/trailer-tips/]
- Transitions: clear, readable shots; think about connective tissue between sections. [Derek Lieu, https://www.derek-lieu.com/start-here]
- Common mistakes: opening slow or with logos. [Filmmaker Genius, https://filmmakergenius.com/academy/how-to-make-a-film-trailer/film-trailer-structure]
- Steps here: cinematic CC0 track; riser SFX crests at 3.47 s, place it with `data-media-start`; title at 0 s for the thumbnail. [repo: library/README.md "music/cc0"]; [repo: CLAUDE.md "HyperFrames learnings"]

## 24. Short film

- Structure: assemble the whole film first, rough and long; start scenes late, end early; nail the opening and ending. [Filmmaker Genius, https://filmmakergenius.com/academy/film-editing-workflow/how-to-edit-a-short-film]
- Cut rhythm: each cut should show something new; vary shot size and angle; cutaways hide jumpy edits. [NFI, https://www.nfi.edu/film-editors/, 2021-06-21]
- Common mistakes: lots of narration and cliché stories; scenes that overstay; neglected sound and no conflict. [Jonny Elwyn, https://jonnyelwyn.co.uk/film-and-video-editing/tips-on-editing-short-films/, 2017-03-30]; [Maximilien Blanc, https://www.maximilien-blanc.com/video-editing-blog/short-film-editing-tips-think-like-a-pro-editor, 2025-05-02]
- Grade: grading shifts colour, contrast, shadows and highlights to set mood. [RMIT Colour Theory, https://rmit.pressbooks.pub/colourtheory1/chapter/colour-correction-and-grading-in-photography-and-film/, 2023-02-23]
- Steps here: grade-compare candidates; CSS 3D voxel films follow the "CSS 3D voxel films" rules; check/snapshot at QA times before render. [repo: CLAUDE.md "Editing a phone video into a professional edit (recipe that worked)"]; [repo: CLAUDE.md "CSS 3D voxel films (learned on the Blocky Monsoon video)"]

## 25. Slideshow from photos

- Length: 3-5 s per photo (4-5 for group photos); photos needed = song length / seconds each. [Woven Video, https://www.woven.video/guides/photo-slideshow, 2026-10-19]
- Structure: remove near-duplicates, order by time or story, open strong, end calm. [Woven Video, https://www.woven.video/guides/photo-slideshow, 2026-10-19]
- Transitions: a slow zoom or pan keeps a still alive; use one motion for every photo. [Woven Video, https://www.woven.video/guides/photo-slideshow, 2026-10-19]
- Grade: one mood and one consistent treatment for all images. [CapCut, https://www.capcut.com/features/how-to-make-a-slideshow-look-aesthetic]
- Captions: combine photos and captions so the slideshow both shows and tells. [VideoStudio, https://www.videostudiopro.com/en/tips/slideshows/]
- Music/SFX: slow instrumental unless the song is the point; fade the end; check rights. [Woven Video, https://www.woven.video/guides/photo-slideshow, 2026-10-19]
- Steps here: personal photos stay in the scratchpad; piano CC0 track; `floating_hearts.py` for warm memories; HyperFrames scale tweens for Ken Burns; WhatsApp copy. [repo: CLAUDE.md "Rules from the owner"]; [repo: library/README.md "music/cc0"]; [repo: library/README.md "Tools (tools/)"]; [repo: CLAUDE.md "Editing a phone video into a professional edit (recipe that worked)"]

## 26. App / website promo

- Goal: walk through the REAL site: full-page screenshots scrolling in a browser frame, side panel with the site's headings, blocky host, captions, intro and end card. [repo: library/templates/website-promo/README.md]
- Structure: research pages from the sitemap with Agent-Reach, save facts to library/research/<site>.md, only facts from the site in the script. [repo: library/templates/website-promo/README.md]
- Transitions: device mockup videos with phone and laptop frames for app marketing and social. [PromoGen, https://www.promogen.app/]
- Music/SFX: CC0 track by default; a promo song only when the owner asks. [repo: CLAUDE.md "Environment facts (cloud container)"]
- Common mistakes: spending Firecrawl credits; capture with `web_capture.py` (network is full now). [repo: CLAUDE.md "Environment facts (cloud container)"]; [repo: CLAUDE.md "Agent tools (library/tools/setup-agent-tools.sh)"]
- Steps here: edit `build.py` S table, `python3 build.py`, `npx hyperframes check`, snapshot ~20 times, render 1920x1080. [repo: library/templates/website-promo/README.md]

## 27. Livestream highlight clip

- Goal: a live moment is worth most in the minutes after it happens. [ClipLive, https://cliplive.com/]
- Structure: mark in/out on the stream's waveform (or grab the last 30 s), auto-frame the speaker into 9:16, captions in the same pass. [ClipLive, https://cliplive.com/]
- Structure: hook (a stranger gets it), proof (one idea), payoff that ends where a rewatch feels natural. [Hookspring, https://hookspring.com/blog/first-three-seconds, 2026-10-20]
- Captions: few words at a time, word-timed, active word in one colour; keep out of the bottom 420 px and the right edge of a 1080x1920 video. [Clyper, https://www.clyper.io/guides/how-to-caption-short-videos, 2026-10-10]
- Steps here: download only CC/public-domain media with yt-dlp; `clean_voice.py` on speech; vertical export. [repo: CLAUDE.md "Environment facts (cloud container)"]; [repo: CLAUDE.md "Voice and songs with words"]; [ClipLive, https://cliplive.com/]

## 28. Client phone-clip reel

- Goal: one short phone clip into a 9:16 reel: one shot per bar at 105 BPM, title card at 0 s, varied transitions, slow-mo end, end card on a hero frame. [repo: library/README.md "Templates (templates/)"]
- Structure: no usable speech -> music reel with Roman Urdu attitude lines that claim nothing specific about the client's business. [repo: CLAUDE.md "Client phone-video edits"]
- Cut rhythm: motion-interpolate EVERY clip to 30 fps (`minterpolate ...:scd=none`), not only slow-mo ones. [repo: CLAUDE.md "Client phone-video edits"]; [ffmpeg docs, https://ffmpeg.org/ffmpeg-filters.html#minterpolate]
- Transitions: zoom-through, whip, light leak, punch-in, flash. [repo: library/README.md "Templates (templates/)"]
- Grade: "Cinematic muted" payload for office/shop footage with loud cyan surfaces. [repo: library/README.md "Colour grades that worked"]
- Captions: Plus Jakarta 800 + Anton titles, gold accent words; don't tween letterSpacing (use scaleX). [repo: library/README.md "Templates (templates/)"]; [repo: CLAUDE.md "Client phone-video edits"]
- Music/SFX: music 1.0, impact-bass 0.35-0.4, whoosh 0.6-0.8, ring 0.5; measure per 0.5 s and ebur128 (~-16 LUFS). [repo: CLAUDE.md "Client phone-video edits"]
- Common mistakes: an <img> over 2 MB isn't inlined (use JPG); a scene's media data-duration must equal the scene length. [repo: CLAUDE.md "Client phone-video edits"]
- Steps here: `assets/clips/c1..c6.mp4` (2.3 s each, 1080x1920) + `hero.jpg`, `python3 build.py`, check/snapshot/render, then WhatsApp copy. [repo: library/README.md "Templates (templates/)"]; [repo: CLAUDE.md "Editing a phone video into a professional edit (recipe that worked)"]

## 29. Pakistani / Indian social-media reel style

- Goal: Pakistani entertainment vloggers turn everyday situations (family, friends, milestones) into episodes, with an informal tone that narrates the story over visuals. [UMT Media and Communication Review, https://journals.umt.edu.pk/index.php/MCR/article/download/6353/3439, 2024-12-26]
- Transitions: seamless and often humorous transitions, unexpected cuts, meme templates and playful sound effects (Ducky Bhai style). [UMT MCR, https://doi.org/10.32350/mcr.42.07, 2024-12-26]
- Transitions: beat-synced cut-out and freeze-frame transitions on Hindi and romantic songs. [Ka Production, https://thekaproduction.com/2026/01/26/trending-transition-reels-editing-capcut/, 2026-01-26]
- Music/SFX: Reels revive old Bollywood songs through 15-second dances, fashion transitions and wedding videos. [Brut India, https://www.brut.media/in/articles/from-in-the-night-no-control-to-sajna-hai-mujhe-how-instagram-is-bringing-old-bollywood-songs-back]
- Grade: grade with mood: warm shadows, desaturated highlights, soft contrast; don't go full filter. [JL Agency, https://jl.agency/social/how-cinematic-transitions-moody-audio-are-shaping-reels-in-2025/, 2025-10-16]
- Captions: Roman Urdu captions; Pashto "Manana" (thank you) as a touch for Pashto-speaking clients. [repo: CLAUDE.md "Client phone-video edits"]
- Common mistakes: using the Bollywood song itself; we never download copyrighted songs: use desi-eastern CC0 (tabla, sitar style, bollywood groove, damal drumming) or the owner's own MP3. [repo: CLAUDE.md "Environment facts (cloud container)"]; [repo: library/music/cc0/README.md]
- Steps here: phone-clip-reel template, Roman Urdu replies/captions, light text on bright walls in deep #6e0c20 with glow; `vs_tts.py` (Urdu 100%/97%) for Urdu narration. [repo: library/README.md "Templates (templates/)"]; [repo: CLAUDE.md "Rules from the owner"]; [repo: CLAUDE.md "HyperFrames learnings"]; [repo: CLAUDE.md "Voice and songs with words"]

## 30. Phonk / velocity edit (beat-driven promo)

- Goal: attitude and impact on a dark, beat-driven track; "hit hard on the drop and breathe in between". [Vikas Editing, https://editingbyvikas.com/phonk-capcut-template/, 2026-06-13]
- Cut rhythm: a hard cut on every beat; 808 kick -> 4-6% impact zoom with snap-back; snare -> 2-3 px RGB split; drop -> 1-frame white flash ~120 ms. [Onset Engine, https://onsetengine.com/guides/make-phonk-drift-edits/, 2026-03-15]
- Grade: desaturate 15-20%, contrast +30-40%, shadows to blue. [Onset Engine, same page]
- Common mistakes: shake on everything or too strong (amateur); shake belongs on the beat, rest between. [Vikas Editing, https://editingbyvikas.com/alight-motion-shake-preset-xml/, 2026-06-16]
- Steps here: CC0 phonk via fetch_free_music.py "phonk" (HoliznaCC0 "Phonk Aura Farming"); beat_events.py for kicks/snares; template library/templates/phonk-3d-promo (v2 builder + post.sh); full notes library/research/phonk-edit-formula.md. [repo: library/research/phonk-edit-formula.md]
