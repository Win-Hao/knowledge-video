---
name: knowledge-video
description: "Turn one topic into a 1–3 minute knowledge explainer video that is easy to follow and good to look at: animation drawn in code, on-screen text over music (the kind of explainer that took off under Douyin's #Vibe知识大赏), rendered with HyperFrames. Six steps, stopping after each one for the user's OK: research and fact-check into a sourced article → rewrite as scene-by-scene video copy → list freely licensed images → three look samples to pick from → analyze the music's beats and write the storyboard → render the first 10 seconds, then the whole video once the opening is approved. Use it whenever someone wants a knowledge, science, history or how-it-works video about a topic — 'make a video explaining X', 'turn the history of X into a short video', 'explainer video', '做一条知识视频', '科普视频', 'Vibe知识大赏' — even if they don't name this skill. For a single short animation or just a new look, use code-video instead."
---

# Knowledge video

**In one line**: turn one topic into one knowledge video. Six steps; after each, stop, show the user, and continue only when they say OK. If they say "just do it" / "go all the way", stop only to wait for images and report once at the end.

Talk to the user in their language. The file names below are defaults; in a Chinese conversation Chinese names are fine (the tested run used 文章.md, 文案.md, 找图.md, 分镜.md).

| Step | Output | Stop and show |
|---|---|---|
| ① Research | `article.md` | how many points, what was cut, what is second-hand |
| ② Copy | `script.md` | the opening question, number of scenes, total length |
| ③ Images | `images.md`, `assets/` | which images, their licenses; wait for the images |
| ④ Look + storyboard | `looks/`, `storyboard.md` | three samples (wait for a pick); the storyboard (wait for review) |
| ⑤ Review | revised `storyboard.md` | what changed, which beat hits moved |
| ⑥ Render | `opening-preview.mp4` → `final.mp4` | what the self-check found; the full video only after the opening is approved |

Why stop: a two-minute video takes a long time to render, and a wrong direction wastes all of it. Changing a sentence in the article, the copy or the storyboard is far cheaper than changing the finished video.

`references/example-ai-history.md` is a full tested run (a brief history of AI, in Chinese) with each step's output and timing. Read it when unsure how detailed a step should be.

## Before starting (one round of questions)

Ask at most these four. Don't ask what the user already said or what you can infer; if they say "you decide", use every default. None of them affects step ①, so don't stop to ask: do ① right away and put the open questions and the defaults you'd use at the end of the ① report (saves a round).

| Ask | Default |
|---|---|
| Which topic; what should viewers remember | — (must know) |
| Length; landscape or portrait | about 2 minutes, landscape 1920×1080 |
| Narration or not | none: on-screen text over music, no voice tools needed. If the user recorded narration, cut shots to its pauses and let the text follow the voice |
| Music | use the audio file in the folder; if there is none, ask the user to drop one in, or synthesize a track in code |

Check the environment: `node` ≥ 22 / `npx`, `python3` with numpy, `ffmpeg`. If something is missing, tell the user what and how to get it; install only with their OK.

Everything goes in the folder the user opened the agent in (layout at the end).

## ① Research → `article.md`

You are a science writer who cares most about getting facts right.

- Search the web. For a history: pick 8–10 key moments, each with year, who, what, and why it matters. For a principle or concept: break it into 5–8 points that need explaining
- Every year, name, number and quote needs a source, linked at the end of its paragraph; prefer primary sources (papers, institutions, archives, the person's own words)
- **Cut anything without a reliable source.** Don't use claims seen only on blogs or social media; label estimates as estimates; if a site blocks scripts and you only saw a second-hand account, say whose account it is. Comment sections under knowledge videos check facts — one wrong year gets called out, and misleading people is worse than covering one point fewer
- Report: how many points; what you cut and why; what is second-hand

## ② Copy → `script.md`

You write knowledge videos for short-video feeds and are good at explaining hard things to people who know nothing about them. An article is read; a video is scrolled past.

- Scene by scene, one line per screen. With no narration viewers only read: at most 20 Chinese characters (about 8–10 English words) per screen
- What most of the best-liked videos of this kind do:
  - **The first screen is the question itself**, for viewers to guess — multiple choice works best. No warm-up like "here's a quiz": if the first two seconds don't hold people, they swipe away
  - Tell it as a story, with names and years
  - At least one everyday comparison
  - One twist
  - End on what it means for an ordinary person
- No jargon without an explanation; no facts that aren't in `article.md`; estimates stay labeled
- For each screen, a suggested duration and one line of visual idea
- Report: the opening question, scenes and screens, total length, which points you dropped for time

## ③ Images → `images.md`

Text alone looks dry. Give each scene one real image: an old photo, a paper's first page, the object itself, a diagram, a screenshot.

- **Licenses**: prefer public domain and CC0; CC BY and CC BY-SA are fine with attribution, and a modified CC BY-SA image must be shared under the same license. Don't use "all rights reserved", unknown-source or non-commercial-only images; list them under "not used" with the reason
- For each image: the URL (its file page), which part to capture, which scene and screen, license, author
- Take the license from the file page itself, not from what you expect of the site or photographer. For Wikimedia Commons you can query `https://commons.wikimedia.org/w/api.php?action=query&prop=imageinfo&iiprop=extmetadata&format=json&titles=File:NAME` and read `LicenseShortName` and `Artist`
- Write the attribution text ready to paste into the video description
- Flag easy mismatches: the same model but not the same machine, a later version of an interface… so on-screen text never claims "this is the one"
- Let the user choose how images arrive:
  - they capture them (default): into `assets/`, file names starting with the scene number, e.g. `03-deep-blue.png`, so you know which goes where
  - you save them into `assets/`: only what the license allows
  - they have their own image generator: turn the list into a description of what each scene needs
  - the listed site doesn't open for them: switch to another freely licensed source, or ask for their own images
- Report, then stop until the images are in place

## ④ Look and storyboard

Build with HyperFrames: `npx hyperframes init <name> --non-interactive` to start a project; read its built-in docs where unsure, `npx hyperframes docs <topic>` (compositions, data-attributes, gsap, rendering); `npx hyperframes check` when done; `npx hyperframes snapshot` for stills; `npx hyperframes render` for the video. If HyperFrames' own skills are installed, follow them for writing compositions; the flow and the stops follow this skill.

### Look → `looks/`

- Offer three clearly different directions, each as one 1920×1080 sample of the first screen (a small project each, one still). One line on why each suits this topic; then recommend one and say why
- Avoid by default: dark backgrounds with neon glow, all text stacked in the center, purple gradients, everything fading in and out. That's the look you get with no constraints, and when everyone uses it, videos look the same. Add whatever the user doesn't want
- Use fonts that are open and free for commercial use (Source Han Sans / Serif, LXGW WenKai, Smiley Sans…) and put the font files in the project
- Stop until the user picks

### Storyboard → `storyboard.md`

You are a motion director who cares most about rhythm.

1. **Analyze the music first**: `python3 <this skill's directory>/scripts/beats.py music.mp3 --json beats.json` gives tempo, every beat, bar lines and loudness changes per bar. HyperFrames' own `beats` reports onsets (roughly every half beat), not the beat itself; use it only as a cross-check
2. **Put the story's key lines on the music**: the reveal and the twist on the first beat of the bar where the music suddenly gets louder; turns and suspense where it thins out; the last screen waits for the final hit and lets the tail ring out
3. **Music and copy of different lengths**: if the music is longer, cut a section on bar lines (20 ms crossfade at each cut); if shorter, repeat a section. Whether and where to cut goes into the storyboard for the user to decide
4. **For each shot**: seconds, frame numbers, which bar and beat it lands on, text, which image, what is on screen and how it moves
5. Cuts land on beats; for moves that take time (page turn, drop, push-in), start early so the frame where it **settles** lands on the beat
6. Turn screenshots into objects of this look's world (a printed photo, a photocopy, lines traced onto paper…); never paste the raw image, or it looks like a slide deck
7. **Frame 0 must already show the first screen's question**; that frame can double as the cover
8. At most 20 characters of text in any one frame

Stop for the user's review.

## ⑤ Review

The user checks three things: can each shot's text be read at a glance, are the years right, does the pace drag. Make their changes; if a change shifts timing, re-align to the beats (move the music cut if needed) and report which beat hits moved and which didn't. Then stop.

## ⑥ Render

1. **First render only the opening, about 10 seconds**, ending on the beat where a shot ends, as `opening-preview.mp4` with music. If the opening isn't right, the whole video won't be; get 10 seconds right before waiting on the rest
2. **Check before handing over**, using sampled frames:
   - text outside the frame, overlapping, or too small (at 1080p, nothing much below 90 px)
   - years and numbers match the copy
   - the frame where each move settles is on a beat; music and picture line up
   Fix and re-render. Report what you found and what you changed
3. Stop for the user. Once they approve, make the full `final.mp4` the same way with the same checks; it renders slowly, so render in segments if needed
4. Deliver `final.mp4` plus `credits.md` (the article's sources + image attributions, for the description). Remind the user:
   - put sources and image credits in the description, and mark modified images as modified
   - turn on the platform's "AI-generated content" label if it has one
   - for a platform event, follow the event page (e.g. Douyin #vibe知识大赏: title starts with 「Vibe知识大赏」 and carries the hashtag)

## While building

- **Chinese fonts** must be declared with `@font-face` in the page (HyperFrames' check looks for it). Use fontTools to make sure the font has every character you need
- **Image treatment**: prefer CSS / SVG filters or canvas in the page; if ImageMagick or Pillow is available, pre-processing to PNG gives fixed results and steadier renders
- **Low-resolution images** (under ~1000 px wide): don't scale them past their size; use them as small prints or crops
- The picture depends only on time (HyperFrames' timeline); seed any randomness so a frame renders the same every time

## Folder

```
(the folder the user opened the agent in)
  music.mp3            the user's music (any name)
  article.md  script.md  images.md  storyboard.md  beats.json
  assets/              captured images, file names start with the scene number
  looks/               three samples and their small projects
  video/               the HyperFrames project
  opening-preview.mp4  final.mp4  credits.md
```
