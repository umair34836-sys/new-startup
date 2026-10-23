GOAL:    the viewer feels a small, warm first-love moment: two blocky people meet in the rain at a chai stall
         and the whole village lights up gold for them.
OUTPUT:  HyperFrames, 1920 x 1080, 30 fps
TIME:    60 s x 30 = 1800 frames. Song sections: intro 0-13.05, verse 13.05-37.19, chorus 37.19-56.14
         (peak hit 45.30), outro 56.14-60. Vocals 12.9-19.4, 28.6-44.8, 53.6-56.4.
LOOK:    medium = a Minecraft-style voxel village built from 16x16 pixel textures (nearest-neighbour, no smoothing),
         one block = 64 px at the world origin. Night palette: sky #0b1c2e -> #1d3b55 (top->horizon), rain #9fc3e8 at
         35% opacity; warm light = lantern amber #ffb347 (windows, stall lantern, lamps). Accent gold #ffd36b only in
         the chorus (rain turns gold, lamps on) and the end card. Faces shaded by direction: top 1.0, front 0.9,
         sides 0.75, bottom 0.5, plus a night multiply layer #2a3f66 at 55% that lifts to 20% in the chorus.
         Display type: "Archivo Black" for Roman, Devanagari in "Noto Sans Devanagari" 800 (bundled fallback check),
         title 120 px; small line 44 px. Vignette 18%.
OBJECTS: chai stall (oak counter, red/white striped wool awning, lantern, wooden sign "चाय"), two white cups with
         brown chai and voxel steam, cobblestone lane with puddles, 8 houses (planks / cobble / stone brick walls,
         dark-oak roofs, warm lit glass windows, doors), 6 street lamps (fence post + lantern), oak trees, him (owner's
         skin), her (long black hair, maroon kurti, gold dupatta edge), a red blocky umbrella.
MOTION:  camera moves power2.inOut 1.2-3 s; character arrivals power2.out; umbrella pop back.out(1.6) on the 45.30
         hit (tl.set start 0.1 s early); lamps light in 0.15 s steps, 0.6 s apart. Walk cycle 0.5 s per step.
SHOTS:   S1 0-4.3     macro on the cup on the counter; a voxel raindrop falls and splashes at 1.04; title lands 1.6-4.0
         S2 4.3-13.05 crane in from above the rooftops down the lane to the stall (rain, warm windows)
         S3 13.05-19.5 "baarish ki pehli shaam thi" - he runs down the lane in the rain and ducks under the awning
         S4 19.5-28.6  she arrives from the other side, soaked; he turns and waves; two-shot
         S5 28.6-37.19 "chai ke do cup" - two cups slide to them, steam rises into a pixel heart
         S6 37.19-45.3 chorus build - camera pulls back and up, lamps light one by one, rain warms to gold
         S7 45.3-56.14 peak - the umbrella pops open over both, crane up over the glowing village
         S8 56.14-60   end card over the two under the umbrella: "बारिश की पहली शाम" + "hamesha tumhara", hold 2.5 s
BANNED:  dark void with small floating things (the frame is always a filled village), decorative glow/particles
         (only rain, steam, lamp light that belong to the story), purple/blue gradients as ground, lyrics as subtitles,
         everything centred, text drifting after it lands, logo in a corner.
QA:      frames 0.5, 1.1, 3.0, 8, 15, 18, 22, 26, 32, 35, 40, 45.4, 50, 58: each shows a filled world, characters
         readable, title legible only in S1 and S8.
