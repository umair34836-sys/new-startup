# Music for video: how a professional editor picks and handles it

Why this file exists: the owner (2026-10-27): "menay lagbhag her ek video me notice kia hai k sessions sahi tariqay se
music sahi sitution ya sahi video me sahi se music pickup nhi kerte ... as a pro editor ye music wala kam bhi bilkul
theek or professional ho". The workflow that turns this file into steps is the skill `.claude/skills/music-for-video`.
Tools: `library/tools/find_music.py`, `music_fit.py`, `mix_vo_music.py`, catalogue `library/music/catalogue.md`.
Measured proof: `library/research/music-for-video-tests.md`.

Sources: every web item was opened and read on 2026-10-27 by this study (PRIMARY = the standards body or platform
itself; everything else is secondary). Items marked `skills #N` were read and cited by the Self-study sessions on
2026-10-24 (`python3 library/tools/find_skill.py "#N"` shows the link). Repo items are measurements made here.
Nothing here is from memory; what could not be verified is listed at the end.

## 1. What music is for, and picking by emotion and tempo

- Music's jobs: set the emotional register, pace the edit, bridge cuts, build and release, mark section changes; music
  doing none of these is decoration. [skills #354: Lumira Studio, updated 2026-05-08]
- Name the scene's emotion in one word (calm, tense, triumphant ...) before searching; that removes most options.
  [skills #355: Duende Sounds, 2026-06-02]
- "It always starts with attributes and the emotion ... Genre is irrelevant if the song hits the emotion" (editor
  Lucas Harger). [Musicbed, https://www.musicbed.com/articles/resources/choose-demo-reel-music/, checked 2026-10-27]
- Tone dictates style; music can play against the action on purpose; consider the viewer's age ("a corporate
  executive may not identify with hard rock or hip-hop"); prefer real instrumentation over "corny" MIDI sounds.
  [PremiumBeat, https://www.premiumbeat.com/blog/how-to-pick-the-perfect-music-for-your-video-projects/, checked 2026-10-27]
- Tempo bands: 60-90 BPM slow vlogs/emotional, 90-120 talking head/tutorial/corporate, 120-150 montages/sports/ads/short
  videos (RFTracks); slow 60-80, mid 90-110 for most corporate work, fast 120+ (Lumira). [skills #356]
- BPM detectors often report half or double (170 -> 85); 1 BPM off is a full beat off after about a minute.
  [skills #357, #358] Here: listen.py flags this as `tempo_octave_ambiguous` with a `bpm_alternative`; the catalogue
  keeps both and find_music.py matches either.

## 2. Music by video type (the profiles find_music.py uses)

| Video type | What the sources say | Energy / BPM used here | Sources |
|---|---|---|---|
| Promo / product ad | brand fit first ("high-class jewelry? Hip hop might not be the right choice"); with a lot of talking, "a score that will carry your visuals without creating a distraction"; with no VO "a song with vocals can work well"; cut the song's parts to the footage | high/mid, 110-140 | Artlist https://artlist.io/blog/royalty-free-music-for-commercials/ and https://artlist.io/blog/choosing-music-for-videos-how-to-pick-the-right-song (2026-10-27) |
| Hosting / tech / SaaS explainer | music that "doesn't drown out or overpower" the VO and "doesn't steal the spotlight"; marketing tools "brighter, lighter"; cybersecurity "dramatic", "more ominous", "ramping up"; unboxing "upbeat electronica" | mid/high, 100-130 | Epidemic Sound https://www.epidemicsound.com/blog/part-one-a-guide-to-picking-the-best-music-for-explainer-videos/ ; PremiumBeat https://www.premiumbeat.com/blog/complete-video-editors-guide-to-music/ (2026-10-27) |
| Food / restaurant | "light, breezy music"; or "a track that matches the cuisine" (Middle Eastern for shawarma); cooking collections = "jazz, soft beats" | mid, 95-125 | PremiumBeat https://www.premiumbeat.com/blog/mr/royalty-free-music-mouthwatering-food-videos/ ; Epidemic Sound https://www.epidemicsound.com/music/themes/cooking/ (2026-10-27) |
| Tutorial / screen video | "engaging but not obtrusive", instrumental acoustic or electronic, no "overly catchy hooks"; "Instrumental, non-vocal tracks work best" | low/mid, 85-115 | PremiumBeat https://www.premiumbeat.com/blog/mr/royalty-free-music-for-tutorial-videos/ (2026-10-27) |
| Explainer (warning, info) | as tutorial; an issue/impact explainer: "subtle", urgency developing into optimism | low/mid, 85-115 | Epidemic Sound (above) |
| Gaming / Minecraft | high-intensity games pair with "high-energy music genres such as Trap", narrative games with Action music; action: "high energy level, fast tempo", "builds up to climactic moments", "crescendos, drops" | high, 115-160 | Epidemic Sound https://www.epidemicsound.com/blog/sound-of-gamers/ ; Musicbed https://www.musicbed.com/articles/resources/instrumental-vs-vocal-music/ (2026-10-27) |
| Emotional / story / charity | "Powerful, soaring, majestic" (donations make a difference) or "solemn, moody, and mournful" (show the problem); sound beds under dialogue, bookended themes | low, 60-95 | Universal Production Music https://www.universalproductionmusic.com/en-us/news/music-for-charities-nonprofits (2026-10-27) |
| Wedding / desi | "romantic and uplifting" for highlights, "sentimental or nostalgic" for vows/speeches, upbeat for entrances/dances, lyrics must not overshadow dialogue; "light or sparse vocals can work" | mid/low, 70-120 | Musicbed (both pages above) |
| Kids / funny | major scales, "ukulele, piano, whistling, glockenspiel, and mallets", simple repetitive structures, avoid "overwhelming or intense"; comedy music "tells the audience: don't take this seriously" | mid/high, 100-140 | RouteNote https://licensing.routenote.com/blog/how_to_find_music_for_kids_content/ (secondary, weaker); PremiumBeat https://www.premiumbeat.com/blog/mr/royalty-free-comedy-tracks/ (2026-10-27) |
| Luxury / fashion | lookbook "pulsing electronica"; with dialogue "subdued, mellow"; jewelry: not hip hop | low/mid, 60-100 | Artlist https://artlist.io/blog/fashion-runway-music/ (only one source found) |
| News / announcement | intro "alarm ... You don't want to instill panic"; bed under the anchor "low in the mix", "keep the intensity level high without distracting" | mid/high, 100-130 | Universal Production Music https://www.universalproductionmusic.com/en-us/news/choosing-the-most-impactful-breaking-news-intro-music (only one source) |
| Brand / logo reveal | no authoritative source found (search results were vendor/AI pages); the repo's own reveal template counts every scene in beats from the drop and lands the logo on it | high/mid, 100-140, needs a drop | repo: library/templates/brand-identity-reveal/README.md |
| Showreel | one track, "an intro you can trim, a build, a drop or peak you can land your best shot on, and a real ending"; viewers decide "in the first 10 to 15 seconds"; "Nobody waits 20 seconds" | high, 115-140 | Musicbed https://www.musicbed.com/articles/resources/choose-demo-reel-music/ (2026-10-27) |

What went wrong before (repo history, 2026-10-24..27): the MoradoSolution hosting offer reel used
`desi-eastern--bollywood-groove` (library/templates/hosting-promo-reel/README.md) and the Pizza Base PK reel used the
same track (library/templates/food-promo-reel/README.md): a tech brand and a pizza place got one Bollywood groove,
against the brand-fit and "match the cuisine" rules above. Under the VO the music sat at one fixed volume (0.16 / 0.18
in those READMEs; no ducking found in either template, grep for "duck"/"sidechain" on 2026-10-27).

## 3. Energy arc and structure

- Social ads: hook / body / close; "90% of ad recall impact is captured within the first six seconds"; "Faster scene
  changes typically draw viewers in early"; end on a strong CTA. [TikTok for Business, PRIMARY,
  https://www.tiktok.com/business/en-US/blog/creative-best-practices-top-performing-ads, checked 2026-10-27]
- Sound matters on TikTok: "88% of TikTok users" say sound is vital (Kantar); 73% "stop and look" at ads with audio.
  [TikTok for Business, PRIMARY, same page + https://www.tiktok.com/business/en-US/blog/kantar-report-how-brands-are-making-noise-and-driving-impact-with-sound-on-tiktok, checked 2026-10-27]
- Meta: "only 3 seconds to catch someone's attention"; one page says design for sound off, another that ads "should
  communicate clearly without sound, but get better or funnier with sound on" (both undated): design for both, i.e.
  captions + music that lands in the first second. [Meta for Business, PRIMARY,
  https://en-gb.facebook.com/business/news/mobile-moves-people-stop-thumbs-in-their-tracks and
  https://www.facebook.com/business/news/want-to-better-video-ads-for-mobile-well-show-you-how, checked 2026-10-27]
- Google ABCDs: "Jump in", "Support the story with audio ... Avoid competing elements", "Reinforce your onscreen CTA
  with voice-over". [Google Ads Help, PRIMARY, https://support.google.com/google-ads/answer/14783551, checked 2026-10-27]
- => Rule here: the music must be "in" within the first 1-2 s (catalogue `first_full_s`); a slow intro is skipped by
  starting later in the track or by placing the drop early (music_fit `--drop-at`).
- Build to the reveal: land "your best shot" on the drop/peak; sync key visual moments "with shifts in the music, like a
  beat drop or crescendo". [Musicbed demo-reel page, checked 2026-10-27] Choose one track with a real build and drop
  before touching clips. [decision-guide.md: Cevylo, 2026-08-05]
- Endings: "A musical sting is the sonic hit that ends a track"; "one of the biggest mistakes editors can make is just
  slapping on a crossfade": move the composer's final sting to where the music must end. If it doesn't fit, cut right
  after an earlier hit and add reverb to make a new sting. [Frame.io Insider 2017,
  https://blog.frame.io/2017/11/08/make-music-fit-your-video/, checked 2026-10-27]
- "Avoid tracks that fade out ... End on a hard button instead." [Musicbed demo-reel page, checked 2026-10-27]
  Editors "will almost always choose music that has edit points, buttoned/stinger endings, and a developmental arc".
  [TAXI, https://www.taxi.com/transmitter/2504/edit-points-buttoned-stinger-endings-and-developmental-arcs-explained/, checked 2026-10-27]
- Backtiming = cueing the music so it ends with the narration/picture; the edit is placed by its out point.
  [Delta Media glossary https://www.deltamedia.com/pages/glossary-of-recording-terms ; Larry Jordan
  https://larryjordan.com/articles/fcpx-backtime-edit/, checked 2026-10-27] Keep the composer's start and real ending
  and hide the edit in the middle. [skills #363]
- Never let music stop mid-phrase: fade over 2-4 s or let the natural ending meet the video's end. [skills #365]

## 4. Music under a voice-over

- No vocals under VO: "Vocals under dialogue ... can be distracting"; "Good non-vocal tracks ... are a safer bet"
  [PremiumBeat pick-music page, checked 2026-10-27]; lyrics "collide with any dialogue or voiceover" [Musicbed, checked
  2026-10-27]; BBC: "avoid the use of music with vocals" [BBC, PRIMARY,
  https://www.bbc.co.uk/editorialguidelines/guidance/visually-and-hearing-impaired-audiences, checked 2026-10-27].
  => find_music.py drops every track with vocals when a VO is present.
- Instrument choice: "a 'wash' of strings is much less intrusive than a solo trumpet. Certain styles of piano music
  and percussion can be very difficult to mix satisfactorily with speech"; choose music "that is not too dynamic".
  [BBC, same page, PRIMARY] => find_music.py prefers a low loudness range (LRA <= 6 LU) under VO.
- How far under: AES TD1009: speech at least 15 dB above a steady masker keeps all speech cues audible; at -15 dB all
  are masked; music masks less than steady noise; children, non-native listeners and many hearing-impaired listeners
  need a higher ratio. [AES TD1009 (2025), PRIMARY, https://aes.org/wp-content/uploads/2025/12/5297fea6-25ba-4865-92f6-dc1d0ba52ce4.pdf, secs 3.3.3-3.3.4, checked 2026-10-27]
  BBC: after the final mix "taking the music down 4db". [BBC Sound Mixing guide v5.0.3, PRIMARY,
  https://www.bbc.com/editorialguidelines/documents/technicaldeliverystandardsbbcaudiomixguidlines.pdf, checked 2026-10-27]
  Music 15-25 dB below the voice while someone talks [skills #313: RFTracks]. No primary "N dB under VO" number for
  social video was found. => mix_vo_music.py default: voice 15 LU over the ducked music during speech.
- Ducking: 6-12 dB, attack 30-80 ms, release 250-700 ms; 15-20 dB on every line makes the automation audible
  [skills #315: CapCut]; 9-12 dB with attack under ~300 ms [skills #314]; duck the music bus, not the master [#317].
  => mix_vo_music.py: -10 dB, attack 60 ms, release 400 ms, 0.5 s hold across word gaps.
- EQ room for speech: making room for VO "usually ... means turning down the 1-4 kHz band in the music"; better: compress
  only the music's 1.5-4 kHz band keyed from the dialogue, so the music is not "muffled" when no one talks.
  [iZotope, https://www.izotope.com/community/blog/mixing-audio-for-video-part-4-mixing-techniques, checked 2026-10-27]
  => mix_vo_music.py dips 1.5-4 kHz of the bed by a further 4 dB only while the voice is on.
- Low-frequency sounds cover speech more ("traffic, fans ... rumbling"). [BBC accessibility page, PRIMARY]
- Workflow: set the dialogue to the target by meter, blend music/effects to it by ear [AES TD1009 sec 5.2]; check on a
  phone speaker as well [PremiumBeat VO/music tutorial, https://www.premiumbeat.com/blog/video-tutorial-mixing-voice-over-with-music-bed-using-dynamic-controls/, checked 2026-10-27].
  Claude can't listen: measure instead (listen.py, mix_vo_music.py report).
- Explainers: "Whenever the narrator interjects, the background music volume is lowered a bit".
  [Epidemic Sound explainer guide, checked 2026-10-27]

## 5. Cutting music to length

- A 4/4 bar lasts 240 / BPM seconds; cut scenes on multiples of the bar. [skills #359]
- Cut on the downbeat (its kick/bass/chord masks the splice), a few ms before the transient. [skills #360]
- Music is built in 4-bar phrases; cut at phrase ends, on a zero crossing, with a 5-20 ms fade. [skills #361]
- Join look-alike moments (chorus 2 downbeat -> chorus 3 downbeat is undetectable). [skills #362]
- If the ending join sounds wrong, move it back 4 bars. [skills #364]
- Shorten by cutting the middle on beats at a section change. [skills #367] "Don't be tied to the duration of your music
  ... loop parts of the track ... bringing in a chorus or emotional climax at just the right time."
  [PremiumBeat pick-music page, checked 2026-10-27]
- Micro-fades: a 10 ms fade puts a splice click ~61.5 dB below the tone [skills #281]; equal-power crossfades avoid the
  mid-fade dip [#283]; speech edits want a few ms, music transitions 1-2 s [#282].
- Fade lengths: short-video BGM in 0.3-0.5 s, out 0.5-1 s; long YouTube 1-2 s in, 2-3 s out. [skills #366]
- Listen without picture: joins the visuals hid become audible. [skills #368] Here: music_fit.py `--check` re-measures
  the beat phase across every join against the beat-tracker's own noise floor (tests file).

## 6. Cutting picture on the beat (and when not to)

- "Choosing an edit point exactly on a noticeable music beat calls attention to the edit"; "More often than not ... keep
  the edit point OFF the beat ... and let the ACTION in the shot do the talking"; beat cuts are for when you WANT the
  edit noticed (energy for dull material). [The Power Edit, https://www.thepoweredit.com/why-cutting-on-the-beat-is-killing-your-edit/, checked 2026-10-27]
- Don't cut on every beat (frantic); slow-mo in quiet sections, ramp into the drop. [skills #187] Phrases of 2/4/8
  beats. [#186] Cutting to the music drives energy, "cutting against can create tension". [PremiumBeat pick-music page]
- => Music reels / montages / reveals: cut on bars and land the key shot on the drop. Talking/VO videos: cut on the
  voice and the action; only section changes and reveals sit on downbeats.

## 7. SFX vs music, and when to use no music

- "Question whether background music is necessary"; cut or fade music/SFX "whilst words are being spoken"; "maintain a
  clear distinction between background and foreground sound". [BBC accessibility page, PRIMARY, checked 2026-10-27]
- A corporate video or film "may actually benefit from only sporadic music or a bookended approach"; forced
  wall-to-wall music fatigues the viewer; montages and reels are end-to-end. [PremiumBeat pick-music page]
- Silence as a tool: "If you just are getting bombarded, it ceases to mean anything"; when the rhythm stops "you pay
  attention" (Chris McCaleb). [Frame.io, https://blog.frame.io/2017/05/08/edit-with-silence/, checked 2026-10-27]
  A dip to black with the music dropping out builds the most anticipation. [skills #121, #89, #353]
- Strip the original audio from client clips: "Two soundtracks fighting each other is the fastest way to make a reel
  feel amateur"; avoid an "Overcrowded Mix". [Musicbed, both pages, checked 2026-10-27]
- Dynamic animation: interesting SFX can be enough; slow emotive pieces: just a soundtrack. [Epidemic Sound,
  https://www.epidemicsound.com/blog/animation-music-and-processes/, checked 2026-10-27]
- Kids content tolerates more SFX than adult content. [RouteNote, secondary]
- Repo levels that worked: music 1.0, impact-bass 0.35-0.4, whoosh 0.6-0.8; at 0.8-0.9 impacts were 8 dB over the music
  for 2 s. [repo: CLAUDE.md "Client phone-video edits"] No primary source for ducking music under SFX hits was found.

## 8. Loudness targets

- EBU R 128: -23.0 LUFS, true peak max -1 dBTP; short-form (ads/promos, up to ~2 min) also max short-term loudness
  -18 LUFS (+5 LU) [R 128 s1]. Streaming: "should be streamed unchanged" at -23, or an interim -20 to -16 LUFS where no
  metadata controls device gain [R 128 s2]. [EBU, PRIMARY, https://tech.ebu.ch/docs/r/r128.pdf,
  https://tech.ebu.ch/docs/r/r128s1.pdf, https://tech.ebu.ch/docs/r/r128s2.pdf, checked 2026-10-27]
- ATSC A/85 (July 2026): -24 LKFS, true peak -2 dBTP; streaming services a single target between -23 and -27; short-form
  measured on the full mix and never louder than the programme around it. [ATSC, PRIMARY,
  https://www.atsc.org/wp-content/uploads/2026/07/A85-2026-07-Annex-M.pdf, checked 2026-10-27]
- Netflix: -27 LKFS +-2 LU dialog-gated, -2 dBTP. [https://studiopartner.netflix.net/studio/branded-sound-mix-spec-and-best-practices, PRIMARY, checked 2026-10-27]
- Devices: home theatre -31, TV/soundbar -24, mobile -16 LKFS normalised output. [AES TD1009 sec 5.2, PRIMARY]
- YouTube: Help documents NO LUFS number; Stable volume is on by default, YouTube may adjust volume, creators can opt out
  of "Let YouTube enhance audio quality". [YouTube Help, PRIMARY, https://support.google.com/youtube/answer/14106294 and
  /16619284, checked 2026-10-27] "YouTube doesn't turn up quieter videos" (stats for nerds "content loudness") [Ian
  Shepherd, secondary, https://productionadvice.co.uk/stats-for-nerds/]; -14 LUFS reference appears only in secondary
  sources (Gearspace, Valmera). Instagram/Facebook: Meta normalises Reels/Stories with xHE-AAC loudness metadata but
  publishes no number [Engineering at Meta 2023-04-11, PRIMARY]. TikTok: no primary spec found. Secondary sites give
  -10 to -18 for these platforms and disagree; the repo's skills #321 (-14) and #322 (-16 social) are secondary too.
- => Rule here: deliver short social/YouTube videos at -16 to -14 LUFS integrated, true peak <= -1 dBTP, 0 clipped
  samples. -16 is the top of R 128 s2's interim range and AES TD1009's mobile level (primary); quieter uploads are not
  turned up on YouTube (secondary). CLAUDE.md's measured reels sat at -14.6..-16.6 LUFS. mix_vo_music.py defaults to -16.
- Short ads: avoid huge loud/quiet swings ("volume surfing" complaints at R128-legal -22.8 LUFS). [BBC Sound Mixing
  guide, PRIMARY] The R 128 s1 short-term cap (+5 LU over integrated) is a useful check for promos (listen.py curve).

## 9. Licence rules (repo owner rules + what the sources say)

- Owner rules (CLAUDE.md): no-credit music only: CC0, public domain, or made by us; our own ACE-Step tracks only when the
  owner asks; never copyrighted songs; CC BY is not acceptable.
- CC0: copy, modify, distribute, perform "even for commercial purposes, all without asking permission"; do not imply
  endorsement. PDM: same, but "may not be free of known copyright restrictions in all jurisdictions". CC BY 4.0: "You
  must give appropriate credit" (why it fails the no-credit rule). [creativecommons.org deeds, PRIMARY, checked 2026-10-27]
- YouTube Audio Library: Help says its music is "copyright-safe" and "won't be claimed ... through the Content ID
  system"; a filter shows tracks that don't require attribution [YouTube Help 3376882, PRIMARY]. The Help page does NOT
  state whether standard-licence tracks may be used outside YouTube; "only on YouTube videos" comes from a community
  Product Expert answer and LicenseOrg (secondary; the in-Studio licence text needs a login). The repo keeps the safe
  reading: YT Audio Library tracks (owner's Drive) = the owner's YouTube videos only, never client reels.
- Mixkit (owner's Drive): no credit needed per owner-drive/README.md, but it is not CC0/PD, so the catalogue marks it
  "not for client work" under the owner rule.
- desi-vocal: public domain by age (1905-1919 recordings; law texts in library/music/desi-vocal/README.md).

## 10. Measured here (this study, 2026-10-27)

- 174 repo tracks measured with listen.py (`music_catalogue.py`, numbers in library/music/catalogue.json).
- music_fit.py joins: the beat-phase error after each join equals the beat tracker's own error at unedited points
  (e.g. 33.0 / 39.5 / 1.0 ms at joins vs 33.7 ms median with no edit, loading-screen-loop stretched to 45 s).
- mix_vo_music.py: voice 15 LU over the ducked bed during speech, final within 0.2 LU of the target, 0 clipped samples.
- Full numbers and the three worked examples: library/research/music-for-video-tests.md.

## Could not verify

- Official YouTube / Instagram / TikTok LUFS targets (none published; only secondary measurements).
- AES TD1008 / AES71 / AES77 numbers (aes.org returned 403 to every reader on 2026-10-27).
- A primary "music N dB under VO" figure for social video (only BBC -4 dB after the mix, AES TD1009 masking figures,
  and secondary numbers).
- An authoritative source on logo-reveal/sting music and a second source for luxury music.
- The in-Studio text of the YouTube Audio Library standard licence (needs a login).
- The study behind PremiumBeat's "mildly upbeat, mid-tempo music helps learning" (no citation on its page).
