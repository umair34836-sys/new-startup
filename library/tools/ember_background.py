import random, sys
rnd = random.Random(2511)
embers, tweens = [], []
for i in range(36):
    x = rnd.uniform(60, 1860); y = rnd.uniform(240, 1120)
    s = rnd.choice([3, 4, 4, 5, 6, 7]); c = rnd.choice(["#FF6A1A", "#FFA827", "#FF8A3D", "#E0281A"])
    o = round(rnd.uniform(0.35, 0.9), 2)
    rise = rnd.uniform(260, 620); dx = rnd.uniform(-60, 60)
    embers.append(f'      <i id="bg-e{i}" class="bg-ember" style="left:{x:.0f}px;top:{y:.0f}px;width:{s}px;height:{s}px;background:{c};opacity:{o}"></i>')
    tweens.append(f'    tl.fromTo("#bg-e{i}", {{ x: 0, y: 0 }}, {{ x: {dx:.0f}, y: {-rise:.0f}, duration: 10, ease: "none" }}, 0);')
open(sys.argv[1], "w").write(f'''<template>
  <style>
    #root {{
      position: absolute;
      inset: 0;
      background: #060202;
      overflow: hidden;
    }}
    #bg-glow {{
      position: absolute;
      inset: 0;
      background:
        radial-gradient(ellipse 70% 55% at 50% 108%, rgba(255, 106, 26, 0.34), rgba(224, 40, 26, 0.12) 45%, transparent 75%),
        radial-gradient(ellipse 50% 40% at 50% 45%, rgba(255, 106, 26, 0.08), transparent 70%);
    }}
    .bg-ember {{
      position: absolute;
      border-radius: 1px;
      box-shadow: 0 0 10px 2px rgba(255, 120, 40, 0.55);
    }}
  </style>
  <div id="root" data-composition-id="bg" data-width="1920" data-height="1080">
    <div id="bg-glow"></div>
    <div id="bg-embers">
{chr(10).join(embers)}
    </div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.fromTo("#bg-glow", {{ opacity: 0.75 }}, {{ opacity: 1, duration: 10, ease: "sine.inOut" }}, 0);
{chr(10).join(tweens)}
    window.__timelines["bg"] = tl;
  </script>
</template>
''')
