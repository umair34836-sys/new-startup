# Vocal / language scan of library/music (measured here on 2026-10-24)

Method: Whisper small on a 30 s window from the middle of each track; segments kept if no_speech_prob < 0.5 and avg_logprob > -1.0. A track counts as 'vocals' when >= 6 words were heard. Only the middle 30 s were checked, so vocals elsewhere in a track can be missed.

Result: 145 tracks, 6.8 hours. Vocals heard in 6:

| File | Seconds | Whisper language | Words heard |
|---|---|---|---|
| `baarish-ki-pehli-shaam-ai-song.mp3` | 60 | ur | 28 |
| `cc0/cinematic--holiznacc0--manic-warlord-mother.mp3` | 159 | en | 44 |
| `own/pashto-song-zama-watan.mp3` | 90 | fa | 16 |
| `own/urdu-song-naya-safar.mp3` | 90 | ur | 23 |
| `own/urdu-song-tumhari-baat.mp3` | 90 | hi | 22 |
| `talkember-studio-promo-song.mp3` | 363 | hi | 47 |

All other 139 tracks: no words heard (instrumental in the checked window).
