#!/usr/bin/env python3
"""Sound effects for a knowledge video: fetch real recorded foley, then mix a cue list into one track.

  python3 sfx.py kenney -o sfx/kenney        # download 4 CC0 packs from kenney.nl (casino, impact, interface, RPG audio)
  python3 sfx.py mix cues.json -o sfx-mix.wav --length 206.9

Use RECORDED sounds, not synthesized noise bursts: filtered-noise "paper" or "scribble" sounds read as hiss
once there are dozens of them over music (tested: viewers heard "just noise"). What worked:
  paper / card slapped down   kenney casino-audio  card-place-*.ogg, card-slide-*.ogg
  something heavy lands       kenney rpg-audio     bookPlace*.ogg
  rubber stamp                kenney impact-sounds impactWood_medium_*.ogg
  soft tick                   kenney interface-sounds tick_*.ogg
  whoosh, pop, ping, typing, riser, sparkle, impact-bass   HyperFrames media-use skill's bundled Pixabay set
Skip pen scribbles and error beeps altogether.

cues.json: [{"t": 8.507, "file": "sfx/kenney/impactWood_medium_000.ogg", "peak": 0.42}, ...]
Each sample is normalized to peak 1, then scaled to "peak" (default 0.3). Peaks that sat well under music
at data-volume 0.8: whoosh 0.22, pop 0.2, tick 0.16, paper 0.34, thud 0.4, stamp 0.42, big impact 0.5, riser 0.28.
Keep it sparse: a whoosh on each scene change, the key hits, and at most ~2 other sounds per screen.

Loudness: HyperFrames' render comes out quiet (about -19 LUFS). For delivery, mix music x0.8 + this track,
then bring it to -14 LUFS with a -1.5 dB ceiling and swap the audio into the rendered video:
  ffmpeg -i music.wav -i sfx-mix.wav -filter_complex "[0:a]volume=0.8[m];[m][1:a]amix=inputs=2:normalize=0[a]" -map "[a]" raw.wav
  ffmpeg -i raw.wav -af ebur128 -f null -        # read I, then: volume=<-14 - I>dB,alimiter=limit=0.84:level=false
Needs numpy and ffmpeg.
"""
import argparse, json, os, re, subprocess, urllib.request, zipfile, io
import numpy as np

SR = 48000
UA = {"User-Agent": "Mozilla/5.0"}

def kenney(out):
    os.makedirs(out, exist_ok=True)
    for pack in ["casino-audio", "impact-sounds", "interface-sounds", "rpg-audio"]:
        page = urllib.request.urlopen(urllib.request.Request(f"https://kenney.nl/assets/{pack}", headers=UA)).read().decode("utf-8", "ignore")
        m = re.search(r'(https?://kenney\.nl)?(/media/pages/assets/[^"]+\.zip)', page)
        if not m: print(f"{pack}: download link not found, get it by hand from https://kenney.nl/assets/{pack}"); continue
        data = urllib.request.urlopen(urllib.request.Request("https://kenney.nl" + m.group(2), headers=UA)).read()
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            for n in z.namelist():
                if n.endswith((".ogg", ".txt")):
                    dst = os.path.join(out, pack, os.path.basename(n))
                    os.makedirs(os.path.dirname(dst), exist_ok=True); open(dst, "wb").write(z.read(n))
        print(f"{pack}: ok (CC0, see License.txt)")

def mix(cues_path, out, length):
    cues = json.load(open(cues_path))
    total = int((length or max(c["t"] for c in cues) + 3) * SR); y = np.zeros((total, 2), np.float32); cache = {}
    for c in cues:
        f = c["file"]
        if f not in cache:
            raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
            x = np.frombuffer(raw, np.float32).reshape(-1, 2); cache[f] = x / (np.abs(x).max() + 1e-9)
        x = cache[f] * c.get("peak", 0.3); i = int(max(0, c["t"]) * SR); j = min(total, i + len(x)); y[i:j] += x[:j - i]
    peak = float(np.abs(y).max())
    if peak > 0.95: y *= 0.95 / peak   # scale down, never clip
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "pcm_s16le", out], input=y.tobytes(), check=True)
    print(f"{out}: {len(cues)} cues, {total / SR:.2f}s, peak {peak:.2f}")

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
sub = ap.add_subparsers(dest="cmd", required=True)
s1 = sub.add_parser("kenney"); s1.add_argument("-o", "--out", default="sfx/kenney")
s2 = sub.add_parser("mix"); s2.add_argument("cues"); s2.add_argument("-o", "--out", required=True); s2.add_argument("--length", type=float)
a = ap.parse_args()
kenney(a.out) if a.cmd == "kenney" else mix(a.cues, a.out, a.length)
