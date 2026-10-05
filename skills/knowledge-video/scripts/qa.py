#!/usr/bin/env python3
"""Self-check a rendered video against plan.json (from timing.py).

Usage: python3 qa.py 成片.mp4 plan.json [--anchor 3 42 73] [-o qa]

- One frame at 80% of every screen, tiled into contact sheets (qa/sheet-1.jpg ..., 24 per sheet):
  look for text out of frame, overlaps, things hidden behind other things, wrong years/numbers.
- For each --anchor screen, the frame just before and just after its start (qa/anchor<n>-before/after.png):
  the cut or the landing should happen exactly between the two.
- Prints the video and audio streams and the duration against the plan.
Needs ffmpeg; uses Pillow for labelled sheets if it is installed, otherwise ffmpeg's tile filter.
"""
import argparse, json, os, subprocess

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("video"); ap.add_argument("plan")
ap.add_argument("--anchor", type=int, nargs="*", default=[])
ap.add_argument("-o", "--out", default="qa")
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
P = json.load(open(a.plan)); S = {s["n"]: s for s in P["screens"]}
pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,width,height,r_frame_rate",
                                "-of", "json", a.video], capture_output=True, text=True).stdout)
print("duration", pr["format"]["duration"], "planned", P["duration"], [(s["codec_type"], s.get("width"), s.get("height"), s.get("r_frame_rate")) for s in pr["streams"]])

def grab(t, f, w=480):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(0, t):.3f}", "-i", a.video, "-frames:v", "1", "-vf", f"scale={w}:-1", f], check=True)

vdur = float(pr["format"]["duration"])
cells = []
for n, s in S.items():
    t = s["t"] + s["dur"] * 0.8
    if t >= vdur - 0.05: continue  # e.g. checking a short opening preview against the full plan
    f = os.path.join(a.out, f"screen{n:02d}.png"); grab(t, f); cells.append((f"{n} · {t:.1f}s", f))
for n in [n for n in a.anchor if S[n]["t"] < vdur]:
    grab(S[n]["t"] - 1 / 30, os.path.join(a.out, f"anchor{n}-before.png"), 640); grab(S[n]["t"] + 1 / 30, os.path.join(a.out, f"anchor{n}-after.png"), 640)
try:
    from PIL import Image, ImageDraw
    W, H, C = 480, 270, 6
    for k in range(0, len(cells), 24):
        part = cells[k:k + 24]; rows = (len(part) + C - 1) // C
        sheet = Image.new("RGB", (W * C, (H + 22) * rows), (30, 30, 30)); d = ImageDraw.Draw(sheet)
        for i, (lab, f) in enumerate(part):
            x, y = (i % C) * W, (i // C) * (H + 22); sheet.paste(Image.open(f).resize((W, H)), (x, y + 22)); d.text((x + 6, y + 5), lab, fill=(255, 255, 255))
        sheet.save(os.path.join(a.out, f"sheet-{k // 24 + 1}.jpg"), quality=85)
except ImportError:
    names = [f for _, f in cells]
    for k in range(0, len(names), 24):
        part = names[k:k + 24]; inputs = sum((["-i", f] for f in part), [])
        subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", f"{''.join(f'[{i}:v]' for i in range(len(part)))}concat=n={len(part)}:v=1:a=0,tile=6x4",
                        "-frames:v", "1", os.path.join(a.out, f"sheet-{k // 24 + 1}.jpg")], check=True)
print("ok ->", a.out)
