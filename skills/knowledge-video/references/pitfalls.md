# HyperFrames pitfalls

Check here first when a render fails, the picture is off, something vanishes or the sound is wrong. All hit in a tested video (2025-10).

- **Two tweens on the same element and property must not overlap in time** (e.g. a push-in still running when the reset starts): a snapshot jumps to one moment and looks fine, but a render plays forward and the earlier tween wins. End one before the next begins; keep separate properties apart (parallax on x, bobbing on y)
- **Later `fromTo`s get `immediateRender: false`**: only the first on a property should apply immediately, or a later state (camera moves especially) shows from the start
- **ids unique across the page**: a duplicate silently sends an animation to the wrong element (a parallax layer and a note both named `s10-l1` left that layer, and its image, never moving into view). Scan the built page for duplicates
- `data-start` on an `<svg>` is ignored; put timing on a wrapping `<div>`
- Animating `clip-path: inset(...)` with GSAP can make the element vanish; animate the width of an `overflow: hidden` wrapper, or `scaleX`
- When splitting text into per-character spans at runtime (typewriter, letter pops), styles written for `.head span` hit every character; scope container styles as `.head > span`
- Douyin Sans' GSUB table can't be subset; add `--drop-tables+=GSUB,GPOS`
- Deliberate overlaps trip check's layout audit; when intended, add `data-layout-allow-overlap` / `-occlusion` / `-overflow`
- Audio peaks failing the last step, failed renders hidden by a pipe: see `sound.md`
- Detailed pictures render large at `--quality delivery` (about 870 MB for 3.5 minutes); re-encode with `-c:v libx264 -preset slow -crf 19 -pix_fmt yuv420p -c:a aac -b:a 256k -movflags +faststart` (about 400 MB, no visible difference)
- Render time on an Apple-silicon Mac: 13-second opening about 35 s; 3.5 minutes 4.5 min (plain) to 8 min (dense collage)

## Canvas animation (10-06, *Fish and Bear's Paw*)

- One full-screen `<canvas>`, every dot and line drawn by `draw(t)`; a proxy tween from 0 to the full duration on the main timeline calls `draw(proxy.t)` in `onUpdate`, so every rendered frame is right. Seed the PRNG
- Labels that move with the camera are drawn on the canvas (`fillText`); text that stays put on screen (captions, readouts) is DOM. Hide on-screen readouts while the camera rotates, or they sit on top of the turned picture
- Keep the template in `src/`, not the project root: a second HTML with `data-composition-id` in the root fails lint with `multiple_root_compositions`
- If `pyftsubset` isn't on PATH, use `python3 -m fontTools.subset`
- Typewriter text: a centered line revealed by hidden spans sits off to the left at frame 0; show the first line whole at frame 0 and type the second
- Film grain that changes every frame bloats the render (1.8 GB for 3 minutes, still 900 MB re-encoded); one static grain tile brings the re-encoded file to about 135 MB
