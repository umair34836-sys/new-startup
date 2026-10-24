#!/usr/bin/env python3
"""Cut a stock clip into the library format and measure it.

    python3 library/tools/stock_prep.py in.webm out.mp4 --start 15 --dur 10 [--crop 1080x1080+420+0]

H.264 yuv420p, no audio, short side at most 1080 (never upscaled), fps capped at 30, max 12 s,
maxrate 5 Mbit/s so a 12 s clip stays under ~8 MB. Prints JSON: width, height, fps, duration, MB.
"""
import argparse
import json
import subprocess


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height,r_frame_rate:format=duration,size", "-of", "json", path],
                         capture_output=True, text=True, check=True).stdout
    d = json.loads(out)
    s, f = d["streams"][0], d["format"]
    n, m = s["r_frame_rate"].split("/")
    return {"width": s["width"], "height": s["height"], "fps": round(int(n) / int(m), 3),
            "duration": round(float(f["duration"]), 2), "mb": round(int(f["size"]) / 1e6, 2)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--start", type=float, default=0)
    ap.add_argument("--dur", type=float, default=10)
    ap.add_argument("--crop", default="", help="WxH+X+Y in source pixels")
    a = ap.parse_args()
    info = probe(a.src)
    vf = []
    if a.crop:
        wh, x, y = a.crop.split("+")
        w, h = wh.split("x")
        vf.append(f"crop={w}:{h}:{x}:{y}")
        info["width"], info["height"] = int(w), int(h)
    short = min(info["width"], info["height"])
    if short > 1080:
        vf.append("scale=-2:1080" if info["width"] >= info["height"] else "scale=1080:-2")
    if info["fps"] > 30.5:
        vf.append("fps=30")
    vf.append("format=yuv420p")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a.start), "-t", str(min(a.dur, 12)), "-i", a.src, "-an",
                    "-vf", ",".join(vf), "-c:v", "libx264", "-preset", "slow", "-crf", "21", "-maxrate", "5M",
                    "-bufsize", "10M", "-movflags", "+faststart", a.dst], check=True)
    print(json.dumps(probe(a.dst)))


if __name__ == "__main__":
    main()
