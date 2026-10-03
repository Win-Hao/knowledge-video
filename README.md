<h1 align="center">knowledge-video</h1>

<p align="center">
  <em>Turn one topic into a 1–3 minute knowledge explainer video. Six steps, and the agent stops after each one for your OK.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-111111?style=flat-square" alt="MIT">
  <img src="https://img.shields.io/badge/works%20with-any%20SKILL.md%20agent-111111?style=flat-square" alt="Agents">
  <img src="https://img.shields.io/badge/render-HyperFrames-111111?style=flat-square" alt="HyperFrames">
  <img src="https://img.shields.io/badge/tested-end%20to%20end-111111?style=flat-square" alt="Tested end to end">
</p>

<p align="center">
  <sub><a href="README.zh-CN.md">简体中文</a></sub>
</p>

---

<p align="center">
  <img src="docs/hero.gif" alt="Two openings made with knowledge-video: a classroom-notebook look asking which year the idea of AI that learns by itself comes from, and a color-swatch look asking why the sky is blue" width="800"><br>
  <sub>two tested openings — top: a brief history of AI in a classroom-notebook look; bottom: why the sky is blue, in a color-swatch look</sub>
</p>

An agent skill for the kind of knowledge video that took off under Douyin's #Vibe知识大赏 tag: animation drawn in code, short lines of on-screen text over music, two or three minutes on one idea. The agent doesn't generate video; it researches, writes, and builds a [HyperFrames](https://www.npmjs.com/package/hyperframes) project that renders to MP4.

Most of the skill is about **not wasting a render**. A two-minute video takes a long time to render, and a wrong direction wastes all of it, so the work is split into six steps and the agent stops after each one: you fix a sentence in the article, the copy or the storyboard, which is far cheaper than fixing the finished video. The last step renders only the first ten seconds; the full video comes after you approve the opening.

## Six steps

| Step | What the agent does | What you check |
|---|---|---|
| ① Research | searches the web, writes a sourced article: 8–10 key moments for a history, 5–8 points for a principle; **cuts anything without a reliable source** | what was cut, what is second-hand |
| ② Copy | rewrites it as scene-by-scene screens, ≤ 20 characters each; the first screen is the question itself, then a story, an everyday comparison, one twist, an ending about ordinary people | the opening question, the length |
| ③ Images | lists one real image per scene (old photo, paper, object, diagram) with URL, which part to capture, license and author; public domain / CC0 first; writes the attribution text | the licenses; you capture the images, or let it save them |
| ④ Look + storyboard | three clearly different looks as stills of the first screen, with a recommendation; then measures the music's tempo and bars (`scripts/beats.py`) and writes every shot to a bar and beat, with the reveal and the twist on the music's changes | pick a look; review the storyboard |
| ⑤ Review | applies your changes, re-aligns to the beats, says which hits moved | — |
| ⑥ Render | renders the opening (~10 s), checks sampled frames for clipped or tiny text, wrong years and off-beat moves, fixes them, then the full video after your OK | the opening |

## Tested

Two runs, both in an empty folder with Claude Code and Claude Opus 5.5:

- **A brief history of AI**, by typing the six steps by hand (no skill): about 58 minutes of agent time from the first prompt to the opening. The run is written up step by step in [`references/example-ai-history.md`](skills/knowledge-video/references/example-ai-history.md) (Chinese).
- **Why is the sky blue?**, with the skill and one sentence — "I want to make a knowledge video about why the sky is blue; the music is in the folder." The skill triggered by itself and stopped after every step; six rounds, about 43 minutes to the opening. Along the way it cut three claims it couldn't trace to a primary source, found 15 freely licensed images and flagged a NASA panorama whose white balance would make Mars's sky look blue, landed the reveal on the bar where the music first gets louder, and fixed six problems its own frame check found before handing over the opening.

## Doing it by hand: the six steps as prompts

The skill grew out of these prompts, which also work without it. They are the tested Chinese originals (translated here); swap the parts in 【】 for your own.

<details>
<summary>The prompts</summary>

① Research
```
<role>You are a science writer who cares most about getting facts right.</role>
<task>Search the web for 【a brief history of AI】. Pick 【8 to 10 key moments】; for each, say what year, who, what they did, and why it matters. Write it up as an article and save it as article.md.</task>
<check>Every year, name, number and quote needs a source, linked at the end of its paragraph; cut any moment you can't find a reliable source for.</check>
```

② Copy
```
<role>You write short knowledge videos and are good at explaining hard things to people who know nothing about them.</role>
<context>This becomes a 【2-minute landscape】 video with 【no narration — viewers only read the on-screen text over music】, so every line has to be short and clear at a glance.</context>
<task>Rewrite article.md as video copy, scene by scene, and save it as script.md: open with a question for viewers to guess; tell the middle as a story with at least one everyday comparison and one twist; end on what it means for an ordinary person.</task>
<avoid>Jargon without an explanation; more than 20 characters on one screen; any fact that isn't in article.md.</avoid>
```

③ Images
```
<context>The video can't be text only; every scene needs one real image (【an old photo, a paper's first page, what the machine looked like】). 【I'll capture the images from web pages myself.】</context>
<task>Go through script.md scene by scene and list the images: which URL, which part of the page to capture, which scene it's for. Save it as images.md.</task>
<avoid>Images marked "all rights reserved" or of unknown origin. Prefer public domain and freely licensed ones, and give the source and license of each.</avoid>
```

④ Look, then storyboard
```
<task>The images I captured are in the assets folder. Build this video with HyperFrames. First give me three clearly different looks, each as a 1920×1080 still of the opening scene, with one line on why it fits. Don't go further until I pick.</task>
<avoid>Dark backgrounds with neon glow; all text stacked in the center; purple gradients; everything fading in and out.</avoid>
```
```
<role>You are a motion director who cares most about rhythm.</role>
<task>Using look 【C】, write the storyboard as storyboard.md: for each shot, how many seconds, what's on screen, the text, which image, how it moves. Turn the screenshots into this look's style instead of pasting them in. The music is 【bgm.mp3】 in this folder: find its beats first and put the cuts on them. Stop when it's written and wait for my review.</task>
<specs>【Landscape 1920×1080】, 30 frames per second, length follows the copy.</specs>
```

⑤ Review — just say what to change, no tags needed, e.g. "Don't open with 'here's a quiz'; show the question in the very first second."

⑥ Render
```
<task>The storyboard is fine, build it. Render only the first 10 seconds to MP4 for me first; I'll ask for the full video once I'm happy with it.</task>
<check>When done, sample a few frames yourself: is any text outside the frame, overlapping or too small; do the years match the copy; do the cuts land on the beats. Fix anything before handing it over.</check>
```

</details>

## Quick start

Put a piece of music in an empty folder, open your agent there, and say what you want to explain:

```
I want to make a knowledge video about why the sky is blue. The music is in the folder.
```

## Requirements

- An agent that reads SKILL.md files, with web search. Tested with Claude Code 2.1.287 and Claude Opus 5.5
- Node.js 22 or newer (HyperFrames)
- Python 3 with numpy, and FFmpeg (beat analysis and audio)

## Install

Paste into any coding agent:

```
Install the knowledge-video skill from https://github.com/Win-Hao/knowledge-video
```

Or the [skills CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add Win-Hao/knowledge-video -g
```

Claude Code plugin (tracks this repo, updates on release):

```
/plugin marketplace add Win-Hao/knowledge-video
/plugin install knowledge-video@knowledge-video
```

Manual (copies the files, pins the current version):

```bash
git clone https://github.com/Win-Hao/knowledge-video.git
cp -R knowledge-video/skills/* ~/.claude/skills/   # Claude Code
```

## Before you publish

- Put the article's sources and the image credits in the description; mark modified images as modified (the skill writes `credits.md` for this)
- Turn on the platform's "AI-generated content" label if it has one
- For a platform event, follow the event page's rules

## Repo layout

```
skills/knowledge-video/
  SKILL.md                         the six steps
  scripts/beats.py                 tempo, beats, bar lines and loudness changes (numpy + FFmpeg)
  references/example-ai-history.md a full tested run, step by step (Chinese)
docs/hero.gif
```

## License

MIT. The photos in `docs/hero.gif` come from Wikimedia Commons: IBM 704 (NASA, public domain), blue sky (TheUltimateGrass, CC0).
