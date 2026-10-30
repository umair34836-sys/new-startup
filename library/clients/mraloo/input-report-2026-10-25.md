# Mr Aloo: input report (first job, 2026-10-25)

Everything below was measured or looked at here on 2026-10-25 from the owner's Drive folder
(drive.google.com/drive/folders/1HlOwa50KDkqBf0KIaCJnQ6JxjPTzB6gx). The media itself is NOT in the repo (scratchpad only).
Tools: ffprobe; `listen.py` / `watch.py` (perc-venv, skill listen-and-watch); Whisper medium (main venv,
language=hi, condition_on_previous_text=False, beam 5); ffmpeg contact sheets looked at with Read.
Transcripts are raw Whisper output: spellings are Whisper's, not checked word by word against the audio.
Topic and video type: NOT decided yet; the owner will say.

## Files

| File (Drive name) | What it is | Length | Measured |
| --- | --- | --- | --- |
| smp promo.mp3 | Male voiceover, Hindi/Urdu, no music | 100.4 s | -16.9 LUFS, true peak -2.46 dBTP, 0 clipped, no hum/hiss, speech 71% (Silero) |
| Indian Gamers Ignore This Warning… Until It's Too Late.mp3 | Male voiceover, Hindi/Urdu + English headings, no music | 279.7 s | -17.7 LUFS, true peak -2.08 dBTP, 0 clipped, no hum/hiss, speech 79% |
| 2026-10-25 20-34-02.mkv | Minecraft gameplay recording (shaders) on ALOO SMP | 182.6 s | 1920x1080, header 60 fps / real 58.8, 1 dropped-frame gap; own audio -32.0 LUFS, 0% speech, silent 115 s of 182 s |
| 2026-10-25 20-24-48.mkv | Minecraft gameplay: joining ALOO SMP + spawn | 51.0 s | 1920x1080, header 60 / real 58.8, no gaps; own audio -43.9 LUFS, 0% speech |
| Snowy ALOO SMP Winter Emblem.png | Server logo | 1254x1254 RGBA | looked at: golden blocky "ALOO", icy blue "SMP", potato character in red Santa hat + red checked scarf, snowy night background with lanterns |

## Video 1: 2026-10-25 20-34-02.mkv (182.6 s), what is on screen (watch.py scenes + contact sheets)

- 0-6.5 s: "Connecting to the server" screen (soft/blurred, scene 1).
- 6.5-25 s: desert with cactus; chat full of plugin update messages ("A new version of ... is available"), "Downloading
  resource pack" toast; scoreboard "ALOO SMP", "TheBiswas001", "Rank: OWNER", "Oct 25, 2026".
- 25-52 s: "YOU ARE AFK" overlay with countdown, chat + command list open.
- 52-87.5 s: indoor shop/market rooms (purple/yellow carpets, chests), other players' name tags, "MEDIA" rank tag;
  dark (luma 50-70) and magenta cast per watch.py.
- 87.5-163 s: outdoor flying shots over spawn builds, roads, gardens; shake > 1.5 px flagged in parts.
- 162.8-163.6 s: very bright frame (luma 209, near white).
- 163.6-181.6 s: market stalls / village area, warm/yellow cast.
- 181.6-182.6 s: near black (luma 20).
- Most motion: 163 s, 102 s, 105 s, 107 s, 106 s. watch.py cut list: 36 content cuts (camera jumps/teleports).

## Video 2: 2026-10-25 20-24-48.mkv (51.0 s)

- 0-5.9 s: "Play Multiplayer" server list; entry "aloo" with MOTD "ALOO SMP" / "VANILLA SURVIVAL • Play Now!", 19/27
  players, pink "ALOO SMP" server icon (frame at 1 s, cropped and read here); the address bar is blacked out in the
  recording. Then "Logging in...", "Joining world" (dark, blurred).
- 5.9-11 s: chat "ALOO SMP >> Welcome", "You have been logged in as premium player".
- 11-31.7 s: walking through spawn (big trees, paths, players); shake > 1.5 px in s 11-26; most motion 21-28 s.
- 31.7-51 s: area with coloured statues/NPCs; tab list at the end headed "ALOO SMP"; cool/blue cast.

## Audio 1: smp promo.mp3 (Whisper medium, 13 segments)

Retakes seen: the opening line twice (1.9 s and 9.9 s), the "24x7 online, no whitelist" line twice (40.0 s, 50.4 s),
"SMP journey" line twice (80.1 s, 84.5 s). Server name heard as "आलू सम्पी", which matches the "ALOO SMP" scoreboard.

| Time (s) | Whisper medium text |
| --- | --- |
| 1.9-8.0 | भाई अगर तुम माइनकाफ खेलने के लिए एक धासू इंडियन ऐसम्पी ढून रहे हो तो इस बिड़। |
| 9.9-17.0 | तो भाई अगर तुम माइनकाफ खेलने के लिए एक धासू इंडियन ऐसम्पी ढून रहे हो तो ये विडियो तुमारे लिए है। |
| 17.0-27.5 | कियोकि आज चुकाया आलू सम्पी, एक ऐसा माइन्कार्प सर्वर, जहाँ मिलेगा सर्वाइबल, ओपी पीवीपी और मज़ेदार मिनी गेम्स का तगरा कौम्बो |
| 28.7-38.8 | यहाँ है custom terrain, custom enchantments, खतरनाक PVP, spawner, crates और एक शांदर player economy |
| 40.0-49.7 | और हाँ वही server 24x7 online है और कोईवी whitelist नहीं है |
| 50.4-55.4 | और हाँ भई, सर्वर है 24x7 आउनलाइन और कोई भी वाइटलिस नहीं है |
| 55.4-59.7 | और सबसे बड़ी बाद जावा बैड्रो खिलारी साथ में खेल सकते है |
| 65.0-67.1 | बनाओ अपना बेस |
| 67.9-71.7 | तो भई देर किस बात का, बनाओ अपना बेस, कमाओ पैसे |
| 72.9-80.1 | क्रेट्स खोलो खड़ीदो ओपी आइटब अपने राइवल से और बनो सर्वर के सबसे खतरणाक प्लियर |
| 80.1-83.7 | दोस्तों के साथ आओओ और अपनी SMP जर्नी शुरू करो |
| 84.5-88.5 | तो भाई जल्दी अपने दोस्तों के साथ आओओ और अपनी SMP जर्नी शुरू करो |
| 88.5-99.3 | तो देर किस बात का भही ये रहा इपी ये रहा पॉर्ट अभी सर्वर को जॉयन करो और अगर तुम्हे सर्वर के लेते अपडेटे रहना है तो जॉयन करो अपना दिसकॉर्ट दिसक्रिपशण में लिंक है। |

## Audio 2: Indian Gamers Ignore This Warning… (Whisper medium, 61 segments)

Spoken English section headings heard: "The warning we all ignore" (20.8 s), "Why Indian Gamers Are Extra Vulnerable"
(44.4 s), "My Real Story" (76.0 s), "How this file actually work?" (113.9 s), "The biggest lie" (135.0 s),
"SIGNS YOU SHOULD NEVER IGNORE" (182.0 s). Retakes seen at 48.2/52.9 s and inside 260.9-276.7 s.

| Time (s) | Whisper medium text |
| --- | --- |
| 0.0-5.8 | आजकी विडियो किसी एक गेम के बारे में नहीं हैं, यह विडियो हर एक इंडियन गेमर के लिए हैं। |
| 7.7-15.2 | अगर तुमने कभी crack game download किया है, free mods use किया है, या FPS boost के लिए random tools install किया हैं, |
| 16.0-19.4 | तो शायएत तुमने भी एक warning ignore की होगी। |
| 20.8-23.0 | The warning we all ignore. |
| 24.0-30.5 | दाउलोड करते ते टाइप कंपुटर पे एक छोटी सी लाइन आती है, दिस वर्ल में हाँ यो दिवाइस |
| 30.5-36.5 | और हम क्या सोझते है? अरे ये सब यूस कर रहा है, यूटूवर ने बोला है तो सेफ ही होगा |
| 36.5-40.3 | और कौमेंट सक्षन में 100% वॉर्किंग बोल दी रहे है |
| 40.4-44.4 | मैं भी एक्साक्ली यही सोचता था |
| 44.4-48.2 | Why Indian Gamers Are Extra Vulnerable |
| 48.2-52.9 | तो इंडिया में गेमिंग का रियलिटी अलग हैं |
| 52.9-54.8 | इंडिया में गेमिंग का रियलिटी अलग हैं |
| 54.8-57.0 | कुछ लोक शेर लैप्टोब यूस करता हैं |
| 57.0-59.4 | किसके पास ओल्ट पीसी हैं |
| 59.4-61.9 | कोई क्रैग्ट विन्डो यूस कर रहा होता है |
| 61.9-65.1 | किसके पास कोई पेड आन्टीवारस नहीं होता |
| 65.1-67.3 | लोग के पास लिमिटेट डाता होता है |
| 67.3-69.2 | लिमिटेट मनी होता है |
| 69.2-71.8 | हम पैसा बचाने के लिए शॉर्ट्सकृस लेते हैं |
| 71.8-76.0 | सब से जादा दैंजरस होता है। |
| 76.0-77.5 | My Real Story |
| 78.9-81.7 | तो मैं एक क्रैग गेम यूस कर रहा था |
| 81.7-83.8 | और ग्राफिक बूस्ट के लिए |
| 83.8-86.7 | मैं एक एकस्रॉट टूल भी इंस्टॉल किया था |
| 86.7-88.3 | फरस्ट विक |
| 88.3-89.6 | कुछ नहीं हुआ |
| 89.6-91.9 | सेकिन विक सब नॉरमल था |
| 91.9-93.8 | लेकिन फिर एक दिन |
| 93.8-112.8 | मेरा गेमी अकांट लोगाउट हो गया, मुझे लगा कोई बग होगा, बत फिर इमेल पे मैसेज आया, नियू लोगिन अटेम्ट डिटेक्टेड, और तब समझा, प्रोब्लेम डाउनलोट करते टाइम ही हो, ये सरूरी नहीं है, प्रोब्लेम बाद में भी हो सकता है। |
| 113.9-116.6 | How this file actually work? |
| 117.3-128.1 | हर virus लाओड नहीं होता, कुछ सिर्फ data read करते हैं, कुछ background में run करते हैं, कुछ password copy करते हैं और कुछ crypto mining करते हैं |
| 128.7-134.1 | इसले PC slow होने का wait मत करो, तब तक काफी कुछ हो चुका होता हैं |
| 135.0-141.4 | The biggest lie, safe है bro चलता है, comment section सबसे बरा scam होता है |
| 142.1-149.4 | कई वार कौमेंट्स में बौट्स होते है, कई वार जो सेब बोल रहा होता है वो खुद विक्टिम होता है |
| 149.9-155.4 | और जो यूट्यूबर रिकमेंड करते है वो भी हुमैन है और गल्ती उनसे भी हो सकती है |
| 156.8-161.5 | तो अमें ऐसा भी लगता है कि क्रैक टूल्ट सेब होता है |
| 161.5-180.5 | एक रीजन यह है कि हमने त्रस्ट किया, सब लोग यूस करते है और बहुत सालो से चल रहा होता है, फ्रैन्स भी यूस करते थे और हम जब कुछ इंस्टेंटली गलत नहीं होता तो हमें लगता है कि ये सेफ है, लेकिन रेलिटी, डिलेक का मतलब सेफ नहीं होता. |
| 182.0-184.5 | SIGNS YOU SHOULD NEVER IGNORE |
| 184.5-189.0 | अगर ये चीजे हुई है तो अभी के अभी बन्द करो |
| 189.0-190.7 | RANDOM LOGOUTS |
| 190.7-195.5 | अगर तुमारा अकांट्स लोगाट हो चुका है तो मतलब तुमारे पीसी में वाईडिस है |
| 196.4-197.5 | EMAIL SECURITY ALERTS |
| 198.1-200.7 | इनको कभी भी इगनोर मत करना |
| 200.7-201.8 | PC FAN |
| 201.8-204.5 | हमेशा लाउड चल रहा होता है |
| 204.8-207.2 | unknown background processes |
| 207.2-210.4 | या फिर browser home page का change होना |
| 210.4-212.7 | ये कोई coincidence नहीं होता |
| 212.7-214.8 | तो इनको ignore मत करना |
| 216.3-220.6 | तो इन से बचने के लिए मैं अभी क्या different करता हो |
| 220.6-223.0 | आजकल मैं रूल follow करता हो |
| 223.0-225.0 | unknown tools बलकुल नहीं |
| 225.0-227.9 | random mod side बलकुल भी नहीं |
| 227.9-231.7 | disabled antivirus भाई कभी भी ये गलति मत करना |
| 231.7-234.8 | अन्टिवारस को हमेशा अंद रखना |
| 234.8-237.1 | टेलिगरम जिप्स कभी भी नहीं |
| 237.9-241.0 | फ्री होने का मतलब हाम्मलेस नहीं होता |
| 242.1-247.4 | तो इस देखा आपके लिए नहीं बना रहा हु |
| 247.4-251.9 | मैं विडियो इसलें बना रहा हू क्यूकि मैं भी वही गलती कर छुका हू |
| 251.9-259.4 | अगर तुम इस विडियो के बाद एक वर्णिंग को थोरा सिर्यस लेते हो, तो शायद एक विडियो वौर्थि थी। |
| 260.9-276.7 | अगर तुमने भी कभी वार्निंग इग्नोर की है, अगर तुमने भी कभी वार्निंग इग्नोर की है, तो कौमेंट में बस अपना एक्स्पिरियन्स लिखो, और अगर किसी फ्रेंड को जरूत है, तो विडियो को शेर कर देना. |
| 276.7-279.2 | तो आज की लिए इतना हैं मिलते हैं अगले नहीं विडियों में. |

## Notes for the edit (facts only; decisions wait for the owner)

- Both videos' own audio has no speech (Silero 0%) and is quiet (-32 / -44 LUFS).
- Both VOs are dry voice, no music: CLAUDE.md "Clip with speech -> use that person's own voice" applies; clean_voice.py
  only if needed (listen.py found no hum/hiss).
- Gameplay matches decision-guide section 12 (Gaming / Minecraft) inputs: "Game capture: brighten Nether/night shots".
