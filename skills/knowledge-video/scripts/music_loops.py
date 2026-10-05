#!/usr/bin/env python3
"""Find where a music track can be lengthened or shortened without an audible seam.

Usage:
  python3 music_loops.py bgm.mp3 拍子.json                 # default lengths 4 8 12 14 16
  python3 music_loops.py bgm.mp3 拍子.json --len 8 14 --from 9 --to 74

Needs only numpy + ffmpeg. 拍子.json comes from beats.py.

Every bar gets an average log spectrum; two bars that sound alike score close to 1.
A span a..b can be REPEATED (after bar b, jump back to bar a) or CUT (after bar a-1, jump
to bar b+1); both are seamless under the same condition: bar b sounds like bar a-1.
So one list serves both.
Above ~0.99 is usually inaudible with a 20 ms crossfade on the bar line; check by ear
or re-run beats.py on the edited file and see that the loudness changes still land where you expect.
"""
import argparse, json, subprocess, sys
import numpy as np

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("audio"); ap.add_argument("beats_json")
ap.add_argument("--len", type=int, nargs="+", default=[4, 8, 12, 14, 16], help="span lengths in bars")
ap.add_argument("--from", dest="lo", type=int, default=2, help="first bar allowed in a span")
ap.add_argument("--to", dest="hi", type=int, default=0, help="last bar allowed in a span (default: second-to-last)")
ap.add_argument("--top", type=int, default=4)
a = ap.parse_args()

j = json.load(open(a.beats_json))
SR = 22050
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", a.audio, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
x = np.frombuffer(pcm, dtype=np.float32)
bar_len = j["meter"] * j["beat_seconds"]
starts = [b["start"] for b in j["bars"]]
feats = []
for s in starts:
    seg = x[int(s * SR):int((s + bar_len) * SR)]
    if len(seg) < 4096:
        feats.append(None); continue
    win = np.lib.stride_tricks.sliding_window_view(seg, 2048)[::512] * np.hanning(2048)
    f = np.log1p(np.abs(np.fft.rfft(win, axis=1))).mean(0)
    feats.append(f / np.linalg.norm(f))
n = len(starts)
hi = a.hi or n - 1

def sim(p, q):
    if not (1 <= p <= n and 1 <= q <= n) or feats[p - 1] is None or feats[q - 1] is None:
        return 0.0
    return float(feats[p - 1] @ feats[q - 1])

print(f"{n} bars, one bar = {bar_len:.3f}s. Spans are inclusive bar numbers (1-based, as in beats.py).")
for L in a.len:
    best = sorted(((sim(b, s - 1), s, b) for b in range(a.lo, hi + 1) for s in [b - L + 1] if s >= a.lo), reverse=True)[:a.top]
    print(f"{L:>3} bars ({L * bar_len:5.1f}s), repeat or cut:  " + "  ".join(f"{s}-{b} ({v:.4f})" for v, s, b in best))
