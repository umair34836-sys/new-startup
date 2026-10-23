# Write a HyperFrames scene of floating hearts and warm bokeh (deterministic, seeded).
# Usage: python3 floating_hearts.py OUT.html [--duration 20] [--count 20] [--burst-at 16.4]
#        [--burst-count 14] [--width 1080] [--height 1920] [--seed 1019] [--id hearts]
import argparse
import random

ap = argparse.ArgumentParser()
ap.add_argument("out")
ap.add_argument("--duration", type=float, default=20)
ap.add_argument("--count", type=int, default=20)
ap.add_argument("--burst-at", type=float, default=None, help="extra hearts rising from this time (e.g. the end card)")
ap.add_argument("--burst-count", type=int, default=14)
ap.add_argument("--bokeh", type=int, default=16)
ap.add_argument("--width", type=int, default=1080)
ap.add_argument("--height", type=int, default=1920)
ap.add_argument("--seed", type=int, default=1019)
ap.add_argument("--id", default="hearts")
a = ap.parse_args()

rnd = random.Random(a.seed)
W, H, D, P = a.width, a.height, a.duration, a.id
heart = '<svg viewBox="0 0 24 22"><path d="M12 21s-9-6.2-9-12.2A5.2 5.2 0 0 1 12 5.6a5.2 5.2 0 0 1 9 3.2C21 14.8 12 21 12 21z" /></svg>'
els, tw = [], []
total = a.count + (a.burst_count if a.burst_at is not None else 0)
for i in range(total):
    burst = i >= a.count
    t0 = rnd.uniform(a.burst_at, a.burst_at + 1.2) if burst else rnd.uniform(-2, D - 5)
    life = rnd.uniform(3.5, 6.5)
    x = rnd.uniform(0.04 * W, 0.96 * W)
    size = rnd.uniform(34, 80) if burst else rnd.uniform(26, 64)
    y0 = rnd.uniform(0.78 * H, 1.04 * H)
    rise = rnd.uniform(0.26 * H, 0.57 * H)
    color = rnd.choice(["#ff5a78", "#ff8fa3", "#ffc2cf", "#ffd59a"])
    op = round(rnd.uniform(0.45, 0.8), 2)
    els.append(f'    <div id="{P}-h{i}" class="{P}-heart" style="left:{x:.0f}px;top:{y0:.0f}px;width:{size:.0f}px;height:{size * 0.92:.0f}px;fill:{color}">{heart}</div>')
    start = max(0.0, t0)
    pre = start - t0
    tw.append(f'    tl.fromTo("#{P}-h{i}", {{ opacity: 0, y: {-rise * pre / life:.0f}, x: 0, rotation: {rnd.uniform(-20, 20):.0f} }}, {{ opacity: {op}, duration: 0.6, ease: "power1.out" }}, {start:.2f});')
    tw.append(f'    tl.to("#{P}-h{i}", {{ y: {-rise:.0f}, x: {rnd.uniform(-90, 90):.0f}, rotation: {rnd.uniform(-25, 25):.0f}, duration: {life - pre:.2f}, ease: "none" }}, {start:.2f});')
    tw.append(f'    tl.to("#{P}-h{i}", {{ opacity: 0, duration: 0.8, ease: "power1.in" }}, {min(D - 0.1, start + life - pre - 0.8):.2f});')
for i in range(a.bokeh):
    x, y, s = rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(40, 140)
    els.append(f'    <div id="{P}-b{i}" class="{P}-bokeh" style="left:{x:.0f}px;top:{y:.0f}px;width:{s:.0f}px;height:{s:.0f}px;opacity:{rnd.uniform(0.12, 0.3):.2f}"></div>')
    tw.append(f'    tl.fromTo("#{P}-b{i}", {{ x: 0, y: 0 }}, {{ x: {rnd.uniform(-80, 80):.0f}, y: {rnd.uniform(-160, -40):.0f}, duration: {D:g}, ease: "none" }}, 0);')
nl = "\n"
open(a.out, "w").write(f'''<template>
  <style>
    #root {{ position: absolute; inset: 0; overflow: hidden; pointer-events: none; }}
    .{P}-heart {{ position: absolute; filter: drop-shadow(0 0 10px rgba(255, 90, 120, 0.6)); }}
    .{P}-heart svg {{ width: 100%; height: 100%; }}
    .{P}-bokeh {{ position: absolute; border-radius: 50%; background: radial-gradient(circle, rgba(255, 214, 170, 0.9), rgba(255, 160, 140, 0.25) 60%, transparent 72%); mix-blend-mode: screen; }}
  </style>
  <div id="root" data-composition-id="{P}" data-layout-allow-overflow data-width="{W}" data-height="{H}">
{nl.join(els)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{nl.join(tw)}
    window.__timelines["{P}"] = tl;
  </script>
</template>
''')
print(f"wrote {a.out}: {total} hearts, {a.bokeh} bokeh, {D:g}s")
