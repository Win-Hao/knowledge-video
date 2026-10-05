<h1 align="center">knowledge-video</h1>

<p align="center">
  <em>Turn one topic into a knowledge explainer people want to watch to the end. A path to follow, not a script: the agent designs each video itself.</em>
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

The skill stays deliberately light. It holds only a few hard rules (every fact sourced, every asset licensed, no AI-drawn faces of real people, frames that render the same every time), a path that works (research → copy → images → look and storyboard → render, showing you each step by default so a wrong direction is caught before a long render), and small tools for music edits, beat timing, sound effects and self-checks. How the video is written, looks and moves is left to the agent; what earlier videos taught sits in `references/` as examples, not rules. The steps below are the path as it was first tested.

## Six steps

| Step | What the agent does | What you check |
|---|---|---|
| ① Research | decides what shape the topic has (timeline, chain of causes, shallow to deep, side by side, Q&A, story), searches the web, writes a sourced article with more candidate points than needed; **cuts anything without a reliable source**; offers two or three options for how many points to cover | how many points (your pick), what was cut, what is second-hand |
| ② Copy | rewrites it as scene-by-scene screens, ≤ 20 characters each; the first screen is the question itself, then a story, an everyday comparison, one twist, an ending about ordinary people | the opening question, the length |
| ③ Images | either lists real images per scene (old photo, paper, object, diagram) with URL, which part to capture, license and author, public domain / CC0 first; or writes layered prompts (one background + separate subjects, one shared style prefix, no text, no real faces) for your own image generator | the licenses or the prompts; you capture or generate the images |
| ④ Look + storyboard | three clearly different looks as stills of the first screen, with a recommendation; then measures the music's tempo and bars (`scripts/beats.py`) and writes every shot to a bar and beat, with the reveal and the twist on the music's changes | pick a look; review the storyboard |
| ⑤ Review | applies your changes, re-aligns to the beats, says which hits moved | — |
| ⑥ Render | renders the opening (~10 s), checks sampled frames for clipped or tiny text, wrong years and off-beat moves, fixes them, then the full video after your OK | the opening |

## Tested

Two runs, both in an empty folder with Claude Code and Claude Opus 5.5:

- **A brief history of AI**, by typing the six steps by hand (no skill): about 58 minutes of agent time from the first prompt to the opening. The run is written up step by step in [`references/example-ai-history.md`](skills/knowledge-video/references/example-ai-history.md) (Chinese).
- **Why is the sky blue?**, with the skill and one sentence — "I want to make a knowledge video about why the sky is blue; the music is in the folder." The skill triggered by itself and stopped after every step; six rounds, about 43 minutes to the opening. Along the way it cut three claims it couldn't trace to a primary source, found 15 freely licensed images and flagged a NASA panorama whose white balance would make Mars's sky look blue, landed the reveal on the bar where the music first gets louder, and fixed six problems its own frame check found before handing over the opening.

## Without the skill: one prompt

No skill installed? Send the prompt below to an agent and replace 【】 with your topic. Before each step it fills the tags into a complete prompt for that step, shows you, then follows it (handing the filled prompt to a subagent where it can). The six original prompts from the first test are in the git history.

<details>
<summary>The prompt</summary>

```
<task>Help me turn 【your topic】 into a knowledge video, along the path research → copy → images → look and storyboard → render. Start by writing a brief, prompts/brief.md; before each step, fill in that step's prompt, save it as prompts/<step>.md, show me, then follow it. Hand large self-contained steps (research, finding images, writing the composition and rendering) to a subagent with the brief and the step's prompt, and check what it produces.</task>
<context>The brief has one context tag: the topic, audience, takeaway, length, orientation, music, what I like and dislike, what earlier steps settled, where the files are; update it after each step.
Each step's prompt has four tags: role (which role does this step and what it cares about most, e.g. knowledge editor, screenwriter, art director, storyboard artist, motion designer, picked per step); task (what it produces and where it goes); style (recommended approaches with reasons; recommendations, not rules; follow me where I've said what I want); check (what to verify, item by item, before the step is done). Leave out style where it isn't needed.
Infer what I haven't said from the topic, and ask me when unsure.</context>
<check>Every fact sourced, and anything unsourced left out; images, music, sound effects and fonts licensed, credits in credits.md; no AI-drawn faces of real people; watch the whole video yourself before handing it over.</check>
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
  SKILL.md                         the path, the hard rules, fill-then-follow prompts
  scripts/beats.py                 tempo, beats, bar lines and loudness changes (numpy + FFmpeg)
  scripts/music_loops.py           bars that repeat or cut without an audible seam
  scripts/cut_music.py             rebuild the music from a bar list, beat grid exact
  scripts/timing.py                lay every screen of the copy onto the beat grid
  scripts/sfx.py                   download Kenney's CC0 foley, mix sound-effect cues
  scripts/qa.py                    contact sheets of every screen and key beats
  references/                      examples and lessons from tested videos (not rules)
docs/hero.gif
```

## License

MIT. The photos in `docs/hero.gif` come from Wikimedia Commons: IBM 704 (NASA, public domain), blue sky (TheUltimateGrass, CC0).
