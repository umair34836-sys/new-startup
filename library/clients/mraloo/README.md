# Mr Aloo (ALOO SMP) — special client: everything in one place

Owner rule (2026-10-26/28): "is client ka sara data apne pass ek folder me save ker lia kro, ye special client hai".
Repo rule still applies: NO videos / voice recordings / photos of people in git. Media stays in the client's Drive
folders below and is re-downloaded by ID; everything else (docs, scripts, transcripts, briefs, edit logs, logo) is here.

Re-download any Drive file into the scratchpad:
`curl -L "https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t" -o <name>`
List a shared folder without the Drive MCP (works for "anyone with the link" folders):
`curl -sL "https://drive.google.com/embeddedfolderview?id=<FOLDER_ID>#list"` (parse the flip-entry-title / file/d/<ID> links).

## Files in this folder
| Path | What |
| --- | --- |
| brief.md | verified client facts (IP, port, Discord, brand colours), Drive folders, owner rules for this client |
| input-report-2026-10-25.md | first analysis of the client's inputs (transcripts, watch/listen facts) |
| (not in git) aloo-smp-winter-emblem.png | client logo "Snowy ALOO SMP Winter Emblem.png" (2.6 MB PNG): client images are never committed; re-download per job from Drive ID 1Lrh9ySfQthZ68dVMwWZaojNyjQm-8kyg (use a JPG copy in HyperFrames, >2 MB is not inlined) |
| edit-log-short-v1.md | ALOO SMP YouTube Short v1/v2: every decision -> source, QA |
| edit-log-warning-explainer.md | "Indian Gamers Ignore This Warning" explainer v1/v2: decisions, client feedback, QA |
| projects/gta5-under-10mb/ | GTA 5 for Android under 10 MB?! — client's editing guide + script (PDF + text), inputs index, transcript, plan |
| projects/smp-short/, projects/warning-explainer/ | inputs index for the earlier jobs |

## Client Drive folders (inputs)
| Folder | ID | Contents (listed 2026-10-28) |
| --- | --- | --- |
| Main input folder | 1HlOwa50KDkqBf0KIaCJnQ6JxjPTzB6gx | 2026-10-25 20-24-48.mkv (16nhkyo2QlKAAevAWaIz2osWhvI8kQOri, gameplay rec, 650.9 MB), 2026-10-25 20-34-02.mkv (1SmJKT0fOUn--o94gnSx_Pg3D4gq5wpwA, spawn rec, 236.4 MB), smp promo.mp3 (1-Dqep2c4cjBOqR9zZZX-Sx20Zxsiq_k_), Indian Gamers Ignore This Warning… Until It’s Too Late.mp3 (17SBdZSkLsSSEUNUTo0LsgvTTCHGxCG26), Snowy ALOO SMP Winter Emblem.png (1Lrh9ySfQthZ68dVMwWZaojNyjQm-8kyg) |
| "gta 10mb" (owner rahulbiswas1812, created 2026-10-27) | 1vFRvwVgAN-g1JMkrxTuvmM1ISWll911s | 2026-10-27 23-34-30.mp4 (12yBLfTxrN9RkarWj_5e60lc4q6aRi5cF, Google search screen rec, 26.9 s 1920x1080 60 fps), gta 10mb.mp3 (1aObjrk974YADkUBi3oaJEPB5IPRmCePk, VO 453.5 s), Mr_Aloo_GTA5_Hinglish_Editing_Guide.pdf (1gVidWNIvJr1rRtShhDRdofr3IQ2Ht5A1), Mr_Aloo_GTA5_Hinglish_Video_Script.pdf (1JhOORG4VR4CW2_80pFFUws8Nh9po63z7) |

## Owner's own folders for this client
- Owner Drive "Mr_Aloo" folder 1dNd_UTL3Gv1-lr0XObfR1-D7kN2pyWoC (Drive MCP can't upload ~100 MB videos; deliver with SendUserFile).
- Music the owner gave (YouTube Audio Library, YouTube use only), owner Drive music library parent 1P7Ec_od5iAWNu2xTQp_bdkMkhvPfne-7:
  folders funny 1kXyHy9wnUxCfofC4BJXF_5AnudskOUNQ, happy 1TYxG6OfPQY41jf50psDcn8MT7LK2KyLI, emotional 1eTsRgP0Qb-Q6egD_oVxMc0om1bWsljVp,
  upbeat 1pac71XVrTeUbdkszH04rcN6p4SaWcevv, suspense 1HAbiRMbPbeOfFYnqOo6epWHvt_6p1yUO, mixkit 1N8SSaIKgzzdcRvuOtikKBBCnxFLuDWN9,
  lofi 12qn3T3aTl6NmLOohlWXZAVfWVlneV13n, desi 1rzg3RW__WAJVBUi8_byisQRbHs7bDFeV, sting 1cDsF9FE9gp2TXS76gF3yeZDi7jBNNdtt,
  tutorial 1wlhRydlW_iOLrBzI1hOvu_uiatK8WS8i, promo 1t_d0q8UwPdvVdJd9Hun8iY6i2DuJ13lS / 1hBm6utUph-YHZ3-Rxvbj3fmktq-ZMdyp (all checked 2026-10-26).

## Delivered (files sent to the owner; not in git)
| Date | Video | Notes |
| --- | --- | --- |
| 2026-10-25 | ALOO-SMP-Short-FINAL-v1.mp4 | 62.6 s 1080x1920 |
| 2026-10-26 | ALOO-SMP-Short-FINAL-v2.mp4 (+ NO-MUSIC variant) | spawn overlays, Java/Bedrock devices |
| 2026-10-26 | Indian-Gamers-Warning-16x9-FINAL.mp4 (v1) | replaced by v2 |
| 2026-10-26 | Indian-Gamers-Warning-16x9-FINAL-v2.mp4 | 220.6 s 1080p; client feedback applied |

## Owner / client rules for this client
- Zero guesswork, every decision logged with its source; preview before the final render; Roman Urdu (Hinglish) captions.
- Visuals must match the narration (no loose images); motion graphics when no licence-clean image fits.
- No client gameplay recordings in the warning explainer (owner 2026-10-26); the GTA guide asks for GTA 5 gameplay.
- No WhatsApp copy (owner 2026-10-26); deliver the full-quality file only.

## GTA 5 under 10 MB (2026-10-28)
- Inputs: VO 1aObjrk974YADkUBi3oaJEPB5IPRmCePk; search recording 12yBLfTxrN9RkarWj_5e60lc4q6aRi5cF; GTA gameplay 1nZX4fI3_pHjqgs6-Ci4jE8YZxzBV5fSI (client allowed; credit the source channel); ALOO SMP spawn 1SmJKT0fOUn--o94gnSx_Pg3D4gq5wpwA (Minecraft cut).
- Delivered: FINAL-v1 (3:59.9) and FINAL-v2 (3:57.9, client fixes: repeat at 2:05, varied pops, real-footage backgrounds, client GTA 6 picture) + thumbnail PNG, 2026-10-28, via SendUserFile. Log: projects/gta5-under-10mb/edit-log.md.
