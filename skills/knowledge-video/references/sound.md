# Sound: music edits, effects, loudness

## Editing the music

- Find seams: `python3 <this skill's directory>/scripts/music_loops.py music.mp3 beats.json [--len 8 14] [--from 9 --to 74]` compares each bar's spectrum and lists spans you can repeat or cut without an audible seam (0.99+ is usually inaudible). Cuts can also put key lines on the music, e.g. dropping a few intro bars so the reveal lands on the first big hit
- Build: `python3 <this skill's directory>/scripts/cut_music.py music.mp3 beats.json --bars 5-21 14-30 … 75-end -o music-edit.wav`, a 20 ms crossfade on each bar line, beat grid exact. Run `beats.py` on the result to confirm the loudness changes are where you want them
- Give `timing.py` the same `--bars` list

## Sound effects

- Use **recorded** sounds. In testing, dozens of code-synthesized paper and scribble sounds over music came across as "nothing but noise"
- Foley: Kenney's CC0 packs (`python3 <this skill's directory>/scripts/sfx.py kenney`): paper slapped down = card place / slide, something heavy lands = book placed, rubber stamp = dull wood impact, light tap = tick
- Whooshes, pops, pings, the low hit on a big reveal, risers: the Pixabay set bundled with HyperFrames' media-use skill (commercial use, no attribution)
- **Sparse**: one whoosh per scene change, the few key hits (reveal, twist, stamps), one or two others per screen; rotate between recordings of the same sound; skip sounds that are noise by nature (pen scribbles, error beeps)
- List the times in a cues.json and mix with `sfx.py mix` (each sample normalized first; volume guidance at the top of the script)

## Loudness and delivery

- For the render, set each `<audio>`'s `data-volume` to about 0.45: stacked tracks over -1 dBFS true peak make HyperFrames fail at the very last step
- Afterwards, mix the delivery track (music x0.8 + effects), bring it to -14 LUFS with a -1.5 dB ceiling, and swap it into the render with ffmpeg (`-map 0:v -map 1:a -c:v copy`, no re-render). Commands at the top of `sfx.py`; later effect changes go the same way
- Before swapping audio or re-encoding, check the render is newer than `index.html`: `render | grep` hides a failed exit code, and you'd put new audio on old picture

## Public-domain music; snap to notes, not bars (10-05 / 10-06)

- Wikimedia Commons has public-domain recordings you can use commercially; check the license through the API (as in `images.md`). Bach's Prelude in C major, BWV 846 (Kimiko Ishizaka) and Satie's Gymnopédie No. 1 (Robin Alciatore) have both been used. One piece often has several recordings: look at a spectrogram for the noise floor first; two other "public domain" recordings were too noisy
- **Don't reuse the hit's music**: its source was unclear, many commenters recognised it, and reusing it reads as copying
- For rubato or triple-meter pieces, `beats.py`'s steady 4/4 fit drifts. Snap each screen change to the strongest note onset within ±0.6 s instead (librosa `onset_strength` + `peak_pick`), so changes land on a piano note
- This video used 29 sound effects, all quiet, each on a visible action; the payoff line got none
- Solo piano is very quiet raw (−26 to −33 LUFS): compress gently first (threshold −30 dB, ratio 2), then bring it to −15 LUFS rather than forcing −14
