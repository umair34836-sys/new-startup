# Arrange Magenta's melody into a 90s-style romantic piece and write a MIDI file.
import json, random, sys
import mido

melody_json, out = sys.argv[1], sys.argv[2]
d = json.load(open(melody_json))
# Optional third argument picks a take by temperature; default is the best-scored take.
take = next(t for t in d["all"] if abs(t["temp"] - float(sys.argv[3])) < 1e-6) if len(sys.argv) > 3 else d["best"]
TPB = 480
BPM = 72
rnd = random.Random(19)
mid = mido.MidiFile(ticks_per_beat=TPB)
events = {}  # channel -> list of (tick, msg)

def note(ch, pitch, beat, beats, vel):
    t0 = round(beat * TPB)
    t1 = round((beat + beats) * TPB)
    v = max(1, min(127, int(vel + rnd.uniform(-6, 6))))
    events.setdefault(ch, []).append((t0, mido.Message("note_on", channel=ch, note=pitch, velocity=v)))
    events.setdefault(ch, []).append((t1, mido.Message("note_off", channel=ch, note=pitch, velocity=0)))

PROGRAMS = {0: 0, 1: 48, 2: 73, 3: 104, 4: 32, 5: 8}  # piano, strings, flute, sitar, bass, celesta
CHORDS = ["C", "Am", "F", "G", "Am|F", "C"]
TONES = {"C": [48, 52, 55, 60, 64], "Am": [45, 52, 57, 60, 64], "F": [41, 48, 53, 57, 60], "G": [43, 50, 55, 59, 62]}

def halves(bar):
    c = CHORDS[bar]
    return c.split("|") if "|" in c else [c, c]

# Piano: soft broken chords in eighths; bar 6 is one rolled chord.
for bar in range(6):
    for h, c in enumerate(halves(bar)):
        tones = TONES[c]
        base = bar * 4 + h * 2
        if bar == 5:
            if h == 0:
                for k, p in enumerate(tones + [67, 72]):
                    note(0, p + 12 if p < 55 else p, base + k * 0.06, 4.5, 48)
            continue
        pat = [tones[1] + 12, tones[2] + 12, tones[3] + 12, tones[2] + 12]
        for s in range(4):
            note(0, pat[s], base + s * 0.5, 0.9, 50 if s % 2 == 0 else 40)
# Strings: pads that swell under each chord.
for bar in range(6):
    hs = halves(bar)
    if hs[0] == hs[1]:
        for p in TONES[hs[0]][1:4]:
            note(1, p + 12, bar * 4, 4.2 if bar < 5 else 6.0, 54)
    else:
        for h, c in enumerate(hs):
            for p in TONES[c][1:4]:
                note(1, p + 12, bar * 4 + h * 2, 2.1, 54)
# Bass: root on 1 and 3 from bar 2.
for bar in range(1, 6):
    for h, c in enumerate(halves(bar)):
        root = TONES[c][0] - 12 if TONES[c][0] > 44 else TONES[c][0]
        note(4, root, bar * 4 + h * 2, 1.8 if bar < 5 else 4.5, 70)
        if bar == 5:
            break
# Sitar intro: the seed motif with a grace note before each.
for n in d["seed"]:
    beat = n["quantizedStartStep"] / 4
    dur = (n["quantizedEndStep"] - n["quantizedStartStep"]) / 4
    note(3, n["pitch"] + 2, beat - 0.08 if beat > 0 else 0, 0.08, 70)
    note(3, n["pitch"], beat + (0.0 if beat == 0 else 0), dur, 88)
# Flute: the AI melody from bar 2, with a grace note into long notes.
for n in take["notes"]:
    beat = n["quantizedStartStep"] / 4 + 4
    dur = (n["quantizedEndStep"] - n["quantizedStartStep"]) / 4
    if dur >= 2 and beat > 4:
        note(2, n["pitch"] + 2, beat - 0.1, 0.1, 72)
    note(2, n["pitch"], beat, dur * 0.97 if beat < 23 else 3.0, 92)
# Celesta sparkle at the start and on the freeze-frame bar.
for k, p in enumerate([72, 76, 79, 84, 88]):
    note(5, p, k * 0.12, 1.5, 70)
for k, p in enumerate([84, 79, 76, 72]):
    note(5, p, 20 + k * 0.1, 2.0, 62)
# Dholak-style keherwa (bars 2-5) on hand percussion, a single hit on bar 6.
DHA, GE, NA, TI = (64, 60), (64,), (60,), (62,)
keherwa = [DHA, GE, NA, TI, NA, (61,), DHA, NA]
for bar in range(1, 5):
    for i, hit in enumerate(keherwa):
        for p in hit:
            note(9, p, bar * 4 + i * 0.5, 0.25, 78 if i in (0, 6) else 58)
    note(9, 54, bar * 4 + 1.5, 0.2, 38)
    note(9, 54, bar * 4 + 3.5, 0.2, 38)
note(9, 64, 20, 0.5, 80)
note(9, 60, 20, 0.5, 70)

tempo = mido.MidiTrack()
tempo.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(BPM), time=0))
mid.tracks.append(tempo)
for ch, evs in sorted(events.items()):
    tr = mido.MidiTrack()
    if ch != 9:
        tr.append(mido.Message("program_change", channel=ch, program=PROGRAMS[ch], time=0))
    tr.append(mido.Message("control_change", channel=ch, control=91, value=70, time=0))  # reverb send
    tr.append(mido.Message("control_change", channel=ch, control=7, value={0: 92, 1: 78, 2: 112, 3: 100, 4: 96, 5: 84, 9: 90}[ch], time=0))
    last = 0
    for t, msg in sorted(evs, key=lambda e: (e[0], e[1].type == "note_on")):
        tr.append(msg.copy(time=t - last))
        last = t
    mid.tracks.append(tr)
mid.save(out)
print("midi ok", len(mid.tracks), "tracks")
