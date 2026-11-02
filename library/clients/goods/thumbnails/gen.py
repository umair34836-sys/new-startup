# GOOD's thumbnails: 2 directions x 2 languages x 2 sizes. Hallmark floor: headline one colour (no accent word),
# no glow, no emoji, single-hue navy background, client's own G mark and real site frame.
import json
NAVY, NAVY2, INK, GOLD = "#060b17", "#0d1526", "#f0f6ff", "#e8c02f"
H = {"en": ("Currency & crypto exchange", "See it before you send"),
     "hi": ("Currency aur crypto exchange", "Bhejne se pehle dekhein")}
for lang, (ha, hb) in H.items():
    for size in ("yt", "short"):
        yt = size == "yt"
        # A: brand mark
        A = {"size": size, "bg": {"gradient": [NAVY2, NAVY], "angle": 160}, "vignette": 0.25,
             "subject": {"image": "gmark.png", "side": "right" if yt else "center", "height": 0.78 if yt else 0.36,
                         "stroke": 0, **({} if yt else {"bottom": 0.5})},
             "texts": [{"text": "GOOD's", "x": 0.05, "y": 0.12 if yt else 0.56, "w": 0.55 if yt else 0.9, "size": 150 if yt else 190,
                        "font": "Outfit", "weight": 800, "color": INK, "stroke": 0, "align": "left" if yt else "center", "tracking": -0.01},
                       {"text": ha, "x": 0.05, "y": 0.42 if yt else 0.68, "w": 0.52 if yt else 0.9, "size": 84 if yt else 92,
                        "font": "Outfit", "weight": 700, "color": INK, "stroke": 0, "align": "left" if yt else "center"},
                       {"text": "Where trust is built.", "x": 0.05, "y": 0.78 if yt else 0.86, "w": 0.55 if yt else 0.9, "size": 60 if yt else 66,
                        "font": "Outfit", "weight": 600, "color": GOLD, "stroke": 0, "align": "left" if yt else "center"}]}
        json.dump(A, open(f"A-{lang}-{size}.json", "w"), indent=1)
        # B: real calculator frame + the site's own result
        B = {"size": size, "bg": {"image": "calc169.png" if yt else "calc916.png", "blur": 0, "darken": 0.55, "zoom": 1.0,
                                  "pos": "50% 60%"}, "vignette": 0.3,
             "texts": [{"text": hb, "x": 0.05, "y": 0.08 if yt else 0.1, "w": 0.9, "size": 104 if yt else 118,
                        "font": "Outfit", "weight": 800, "color": INK, "stroke": 0, "align": "left" if yt else "center"},
                       {"text": "32,500 PKR = $100", "x": 0.05, "y": 0.52 if yt else 0.5, "w": 0.9, "size": 96 if yt else 104,
                        "font": "Outfit", "weight": 800, "color": "#14110a", "box": GOLD, "stroke": 0, "align": "left" if yt else "center"},
                       {"text": "Rates as of 2 Nov 2026", "x": 0.05, "y": 0.72 if yt else 0.62, "w": 0.6 if yt else 0.9, "size": 34,
                        "font": "Outfit", "weight": 500, "color": "#c9d2e0", "stroke": 0, "align": "left" if yt else "center"}],
             "stickers": [{"image": "gmark.png", "x": 0.76 if yt else 0.35, "y": 0.6 if yt else 0.72, "w": 0.2 if yt else 0.3}],
             }
        json.dump(B, open(f"B-{lang}-{size}.json", "w"), indent=1)
print("ok")
