#!/usr/bin/env python3
"""Rebuild a music track from a list of bar ranges, keeping the beat grid exact.

Usage:
  python3 cut_music.py bgm.mp3 拍子.json --bars 5-21 14-30 17-36 41-44 45-57 50-74 75-end -o 配乐-剪辑.wav

Bars are inclusive and 1-based, as printed by beats.py / music_loops.py; "end" means to the
end of the file. Each join sits on a bar line with a 20 ms equal-power crossfade centred on
it, so the output's beat grid stays exactly (number of bars) x (bar length) — video bar k
starts at (k-1) x bar length. Re-run beats.py on the output to confirm the beats.
Needs numpy + ffmpeg.
"""
import argparse, json, subprocess
import numpy as np

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("audio"); ap.add_argument("beats_json")
ap.add_argument("--bars", nargs="+", required=True)
ap.add_argument("-o", "--out", required=True)
ap.add_argument("--fade-ms", type=float, default=20)
a = ap.parse_args()

j = json.load(open(a.beats_json)); SR = 48000
bar_len = j["meter"] * j["beat_seconds"]; d0 = j["first_downbeat"]
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", a.audio, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
x = np.frombuffer(raw, dtype=np.float32).reshape(-1, 2)
bar_t = lambda k: d0 + (k - 1) * bar_len
X = int(a.fade_ms / 2000 * SR)
out, prev_end = [], None
for spec in a.bars:
    s, e = spec.split("-")
    i0 = int(round(bar_t(int(s)) * SR))
    i1 = len(x) if e == "end" else int(round(bar_t(int(e) + 1) * SR))
    seg = x[i0:i1].copy()
    if out:
        w = np.linspace(0, np.pi / 2, 2 * X)[:, None]
        tail = np.concatenate([out[-1][-X:], x[prev_end:prev_end + X]])
        head = np.concatenate([x[max(0, i0 - X):i0], seg[:X]])
        out[-1] = out[-1][:-X]
        seg = np.concatenate([tail * np.cos(w) + head * np.sin(w), seg[X:]])
    out.append(seg); prev_end = i1
y = np.concatenate(out)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "pcm_s16le", a.out],
               input=y.astype(np.float32).tobytes(), check=True)
print(f"{a.out}: {len(y) / SR:.3f}s; one bar = {bar_len:.4f}s; the first bar of the output starts at 0")
