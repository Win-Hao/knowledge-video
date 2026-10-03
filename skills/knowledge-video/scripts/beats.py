#!/usr/bin/env python3
"""Music analysis for storyboarding: tempo (BPM), every beat, bar lines, loudness per bar.

Usage:
  python3 beats.py music.mp3                  # print a summary
  python3 beats.py music.mp3 --json beats.json  # also save the full data

Needs only python3, numpy and ffmpeg (no librosa). Assumes 4/4; pass --meter 3 etc. otherwise.
Use it to put cuts on beats and the story's key lines (reveal, twist, ending) on the first beat
of a bar, or on the bar where the music suddenly gets louder.
"""
import argparse
import json
import subprocess
import sys

import numpy as np

SR = 22050
HOP = 128
NFFT = 2048
# A log spectrum shows an onset as soon as it enters the window, so each frame is timed at the
# window's end (checked against librosa's beats: within one video frame).


def load(path):
    cmd = ["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def features(y):
    n = 1 + (len(y) - NFFT) // HOP
    frames = np.lib.stride_tricks.as_strided(
        y, shape=(n, NFFT), strides=(y.strides[0] * HOP, y.strides[0]))
    win = np.hanning(NFFT).astype(np.float32)
    flux = np.zeros(n, dtype=np.float64)
    low = np.zeros(n, dtype=np.float64)
    rms = np.zeros(n, dtype=np.float64)
    freqs = np.fft.rfftfreq(NFFT, 1 / SR)
    lowmask = freqs < 150
    prev = None
    for i in range(0, n, 512):  # in blocks, to save memory
        blk = frames[i:i + 512]
        S = np.abs(np.fft.rfft(blk * win, axis=1))
        L = np.log1p(10 * S)
        if prev is not None:
            L2 = np.vstack([prev[None, :], L])
        else:
            L2 = np.vstack([L[:1], L])
        flux[i:i + len(blk)] = np.maximum(0, np.diff(L2, axis=0)).sum(axis=1)
        low[i:i + len(blk)] = S[:, lowmask].sum(axis=1)
        rms[i:i + len(blk)] = np.sqrt((blk.astype(np.float64) ** 2).mean(axis=1))
        prev = L[-1]
    return flux, low, rms


def normalize(x, width):
    k = np.ones(width) / width
    m = np.convolve(x, k, mode="same")
    z = np.maximum(0, x - m)
    return z / (z.std() + 1e-9)


def tempo(env, fps, lo=70, hi=180):
    ac = np.correlate(env, env, mode="full")[len(env) - 1:]
    lags = np.arange(len(ac))
    bpm = 60 * fps / np.maximum(lags, 1)
    ok = (bpm >= lo) & (bpm <= hi)
    # prefer 90–150 BPM to avoid double / half tempo
    weight = np.exp(-0.5 * (np.log2(np.maximum(bpm, 1) / 120) / 0.9) ** 2)
    score = np.where(ok, ac * weight, -np.inf)
    lag = int(np.argmax(score))
    if 1 <= lag < len(ac) - 1:  # parabolic interpolation to a fractional frame
        a, b, c = ac[lag - 1], ac[lag], ac[lag + 1]
        d = 0.5 * (a - c) / (a - 2 * b + c + 1e-12)
        return lag + d
    return float(lag)


def fit_grid(env, times, period):
    """period in seconds. Find the phase on a 2 ms grid, then fit a line through the actual peak near
    each beat to correct tempo and start."""
    best, best_phase = -1.0, 0.0
    for ph in np.arange(0, period, 0.002):
        grid = ph + np.arange(0, times[-1] - ph, period)
        s = np.interp(grid, times, env).mean()
        if s > best:
            best, best_phase = s, ph
    ks, ts = [], []
    k = 0
    while True:
        c = best_phase + k * period
        if c >= times[-1]:
            break
        m = (times > c - 0.06) & (times < c + 0.06)
        if m.any():
            j = np.argmax(np.where(m, env, -1))
            if env[j] > 1.0:  # only clear onsets
                ks.append(k)
                ts.append(times[j])
        k += 1
    ks, ts = np.array(ks, float), np.array(ts, float)
    if len(ks) > 8:
        A = np.vstack([ks, np.ones_like(ks)]).T
        (p, ph), *_ = np.linalg.lstsq(A, ts, rcond=None)
        resid = ts - (ph + p * ks)
        return p, ph, len(ks), float(np.abs(resid).mean()), float(np.abs(resid).max())
    return period, best_phase, len(ks), float("nan"), float("nan")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("audio")
    ap.add_argument("--json")
    ap.add_argument("--meter", type=int, default=4)
    a = ap.parse_args()

    y = load(a.audio)
    dur = len(y) / SR
    fps = SR / HOP
    flux, low, rms = features(y)
    times = (np.arange(len(flux)) * HOP + NFFT) / SR
    env = normalize(flux, int(fps))
    lag = tempo(env, fps)
    period, first, used, err_mean, err_max = fit_grid(env, times, lag / fps)
    while first - period >= 0:
        first -= period
    beats = [first + i * period for i in range(int((dur - first) / period) + 1)]

    # downbeat: the beat phase with the heaviest low end (kick)
    lenv = normalize(np.log1p(low), int(fps))
    def at(t):
        i = int(np.searchsorted(times, t))
        return lenv[max(0, i - 4):i + 5].max() if i < len(lenv) else 0
    off = int(np.argmax([np.mean([at(t) for t in beats[o::a.meter]]) for o in range(a.meter)]))
    bar_starts = beats[off::a.meter]

    # loudness per bar (dB): where the music thins out and where it comes back
    bars = []
    for i, t0 in enumerate(bar_starts):
        t1 = bar_starts[i + 1] if i + 1 < len(bar_starts) else dur
        seg = rms[np.searchsorted(times, t0):np.searchsorted(times, t1)]
        db = 20 * np.log10(seg.mean() + 1e-9) if len(seg) else -120
        bars.append({"bar": i + 1, "start": round(t0, 3), "db": round(float(db), 1)})
    marks = []
    for i in range(2, len(bars)):
        prev = (bars[i - 1]["db"] + bars[i - 2]["db"]) / 2
        diff = bars[i]["db"] - prev
        if diff >= 3:
            marks.append({"bar": bars[i]["bar"], "start": bars[i]["start"], "change": "louder (good for a reveal or a twist)", "db": round(diff, 1)})
        elif diff <= -3:
            marks.append({"bar": bars[i]["bar"], "start": bars[i]["start"], "change": "thinner (good for a turn or suspense)", "db": round(diff, 1)})

    bpm = 60 / period
    out = {
        "audio": a.audio, "duration": round(dur, 3), "bpm": round(bpm, 2),
        "beat_seconds": round(period, 5), "first_beat": round(first, 4), "meter": a.meter,
        "first_downbeat": round(bar_starts[0], 4) if bar_starts else None,
        "fit": {"beats_used": used, "mean_error_ms": round(err_mean * 1000, 1), "max_error_ms": round(err_max * 1000, 1)},
        "beats": [round(t, 4) for t in beats],
        "bars": bars, "changes": marks,
    }
    print(f"duration {dur:.2f}s | {bpm:.1f} BPM | one beat {period:.4f}s (~{period * 30:.1f} frames at 30 fps) | first beat {first:.3f}s | first bar line {out['first_downbeat']}s")
    print(f"fit: {used} beats used, mean error {out['fit']['mean_error_ms']} ms, max {out['fit']['max_error_ms']} ms")
    print("loudness changes (each bar vs. the two before it, 3 dB or more):")
    for m in marks:
        print(f"  bar {m['bar']:>3} at {m['start']:>7.2f}s  {m['change']}  {m['db']:+.1f} dB")
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=1)
        print(f"full data: {a.json}")


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError:
        sys.exit("ffmpeg not found: install ffmpeg first")
    except subprocess.CalledProcessError as e:
        sys.exit(f"ffmpeg could not read the file: {e.stderr.decode(errors='ignore')[:200]}")
