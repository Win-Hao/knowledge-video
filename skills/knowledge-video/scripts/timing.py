#!/usr/bin/env python3
"""Lay every screen of 文案.md onto the beat grid of the (edited) music; write plan.json.

Usage:
  python3 timing.py 文案.md 拍子.json --bars 5-21 14-30 17-36 41-44 45-57 50-74 75-end \
      --anchor 3:9 --anchor 39:41 --anchor 42:45 --anchor 73:75 [--fix 1:7 --fix 2:9] [-o plan.json]

What it does
- Reads the screen rows of 文案.md: table rows starting with "| <number> |", text in the 2nd column.
  A "## ..." heading before a table starts a new scene (幕).
- Gives each screen whole beats: about 0.6 s + 1 s per 6 characters (Chinese characters and
  Latin words count one each), at least 3 beats. --fix n:beats overrides a screen.
- Every scene, and every anchored screen, starts on a bar line (downbeat).
- --bars is the same bar playlist you give cut_music.py (default: the whole track).
- --anchor n:bar puts screen n on the downbeat of ORIGINAL bar `bar` (its first occurrence in the
  playlist after the previous anchor). Use it for the answer reveal, the twist, the last screen.
  Spare bars between two anchors go to the scenes in between (the longest scene first), then to
  their screens (first and last screen first).
- If the screens between two anchors need more bars than the music has there, it stops and says
  how many bars are missing: repeat that many bars with music_loops.py + cut_music.py, or cut copy.
- The last screen runs to the end of the music when it is anchored; otherwise the plan says
  how much music is left over.

Output: plan.json (screens with start t, duration, beats, video bar.beat, original bar, scene) and a
timing table on stdout to paste into 分镜.md. Needs only the standard library.
"""
import argparse, json, math, re, sys

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("copy"); ap.add_argument("beats_json")
ap.add_argument("--bars", nargs="+")
ap.add_argument("--anchor", action="append", default=[])
ap.add_argument("--fix", action="append", default=[])
ap.add_argument("-o", "--out", default="plan.json")
a = ap.parse_args()

J = json.load(open(a.beats_json)); B = J["beat_seconds"]; M = J["meter"]; BAR = B * M; nbars = len(J["bars"])
bar_t = lambda k: J["first_downbeat"] + (k - 1) * BAR
# bar playlist: video bar i (0-based) = original bar playlist[i]
specs = a.bars or [f"1-end"]
playlist, tail = [], None
for sp in specs:
    s, e = sp.split("-")
    if e == "end":
        playlist += list(range(int(s), nbars + 1)); tail = J["duration"] - bar_t(int(s))
    else:
        playlist += list(range(int(s), int(e) + 1))
music_len = (len(playlist) * BAR) if tail is None else (len(playlist) - (nbars - int(specs[-1].split("-")[0]) + 1)) * BAR + tail

# read the copy
screens, scene = [], "(no scene)"
for line in open(a.copy, encoding="utf-8"):
    h = re.match(r"#{2,3}\s+(.+)", line)
    if h: scene = h.group(1).strip(); continue
    m = re.match(r"\|\s*(\d+)\s*\|([^|]*)\|", line)
    if m:
        text = m.group(2).strip()
        units = len(re.findall(r"[一-鿿]", text)) + len(re.findall(r"[A-Za-z0-9][A-Za-z0-9.\-]*", text))
        screens.append({"n": int(m.group(1)), "text": text, "units": units, "scene": scene,
                        "beats": max(3, round((0.6 + units / 6) / B + 0.2))})
if not screens: sys.exit("no screen rows like | <number> | <text> | found in the copy file")
idx = {s["n"]: i for i, s in enumerate(screens)}
for f in a.fix:
    n, k = map(int, f.split(":")); screens[idx[n]]["beats"] = k
anchors = sorted((int(n), int(b)) for n, b in (x.split(":") for x in a.anchor))

# groups: every scene start and every anchored screen starts on a bar line
starts = sorted({0} | {i for i in range(1, len(screens)) if screens[i]["scene"] != screens[i - 1]["scene"]} | {idx[n] for n, _ in anchors})
groups = [list(range(s, e)) for s, e in zip(starts, starts[1:] + [len(screens)])]
gbars = [math.ceil(sum(screens[i]["beats"] for i in g) / M) for g in groups]
gstart = {g[0]: k for k, g in enumerate(groups)}

# anchors -> video bars
targets, last = [(0, 0)], -1
for n, ob in anchors:
    try: vb = next(i for i in range(last + 1, len(playlist)) if playlist[i] == ob)
    except StopIteration: sys.exit(f"anchor {n}:{ob}: original bar {ob} does not occur in the bar playlist after video bar {last + 1}")
    targets.append((idx[n], vb)); last = vb
problems = []
for (i0, v0), (i1, v1) in zip(targets, targets[1:]):
    ks = [gstart[i] for i in range(i0, i1) if i in gstart]
    have, need = v1 - v0, sum(gbars[k] for k in ks)
    if need > have:
        problems.append(f"screens {screens[i0]['n']}-{screens[i1 - 1]['n']} need {need} bars but the music has {have} there: {need - have} bars ({(need - have) * BAR:.1f}s) short")
        continue
    order = sorted(ks, key=lambda k: -sum(screens[i]["beats"] for i in groups[k]))  # longest scene first
    for t in range(have - need): gbars[order[t % len(order)]] += 1
if problems:
    print("Does not fit:\n  " + "\n  ".join(problems) + "\nRepeat bars (music_loops.py, then a longer --bars playlist) or cut copy."); sys.exit(1)

# fill each group to whole bars: first and last screen first
for k, g in enumerate(groups):
    extra = gbars[k] * M - sum(screens[i]["beats"] for i in g)
    order = [g[0], g[-1]] + g[1:-1] if len(g) > 1 else g
    for t in range(extra): screens[order[t % len(order)]]["beats"] += 1

beat = 0
for s in screens:
    vb = beat // M
    s.update(t=round(beat * B, 3), vbar=vb + 1, beat_in_bar=beat % M + 1, orig_bar=playlist[vb] if vb < len(playlist) else None)
    s["dur"] = round(s["beats"] * B, 3); beat += s["beats"]
end = beat * B
if anchors and anchors[-1][0] == screens[-1]["n"]:
    screens[-1]["dur"] = round(music_len - screens[-1]["t"], 3); screens[-1]["beats"] = None; end = music_len
json.dump({"B": B, "meter": M, "bars": specs, "duration": round(end, 3), "music": round(music_len, 3), "screens": screens},
          open(a.out, "w"), ensure_ascii=False, indent=1)

print(f"Total {end:.2f}s ({int(end // 60)}:{end % 60:05.2f}), music {music_len:.2f}s" + ("" if abs(music_len - end) < 0.05 else f", music is {abs(music_len - end):.2f}s {'longer' if music_len > end else 'shorter'}"))
print("\n| screen | time (s) | frames @30fps | video bar.beat | original bar | text |\n|---|---|---|---|---|---|")
for s in screens:
    print(f"| {s['n']} | {s['t']:.2f}–{s['t'] + s['dur']:.2f} | {round(s['t'] * 30)}–{round((s['t'] + s['dur']) * 30) - 1} | {s['vbar']}.{s['beat_in_bar']} | {s['orig_bar']} | {s['text']} |")
print(f"\nwrote {a.out}")
