# Filled prompts (tested video "AI, 2016–2026", third version)

To see how detailed they get. Swap in your own topic and style; don't copy. (Translated from the Chinese originals.)

## brief.md

```
<context>The topic is AI from 2016 to 2026, for ordinary people who use or want to use AI. Takeaway: in ten years AI went from playing one board game to a helper that does your work. 10 moments, all facts in article.md. Music music.mp3, starting at bar 3, 2:36, no repeats. Landscape 1920×1080, no narration; viewers only read.
The author likes: Vox-style collage where one scene is layered from many cut-outs (torn-paper titles, a subtitle bar at the bottom, retro palette); rich motion; sound effects; real photos for named people. The author dislikes: a too-plain look, every scene in one template ("flat"), synthesized noise as sound effects, screen text spilling off screens.
Settled: collage look; 10 moments; company logos from LobeHub.
Files: article.md, script.md, assets/collage/ (layers), video/assets/photos/, video/assets/logos/, video/plan.json (timing); the project is video/.</context>
```

## The copy step

```
<role>Screenwriter for short-video explainers who cares most about whether viewers swipe away: a hook in the first two seconds, and every scene ending on a reason to watch the next.</role>
<task>Write script.md: scenes, one line per screen, with time on screen and a visual idea for each.</task>
<style>(Recommended) Open with three counter-intuitive flashes (the company that played Go produced Nobel laureates / a paper about translation became GPT's foundation / the work it can do alone doubles every 7 months), then "rewind" to 2016: three hooks pull harder than one guessable question. End each scene by "unlocking" a new AI ability, a thread that keeps filling up. Pay off the first line in the Nobel scene. Shorter scenes toward the end, so the pacing follows the "faster and faster" theme. Vary the structure between scenes instead of one template.</style>
<check>Every line traces to article.md; the opening lines and the ending callback checked for overclaiming; at most 20 characters per screen; timing.py fits it to the music.</check>
```

## The visuals step (the kind handed to a subagent)

```
<role>Motion designer who cares most about what each movement explains, then about landing on the beat.</role>
<task>Write video/src/scenes.html and scenes.js, build, run check, grab one frame per screen, fix until nothing is hidden, then hand back.</task>
<style>(Recommended) Give each scene a movement of its own: a grid of 10,000 dots with one red for "1 in 10,000"; a code-drawn chain folding bead by bead for proteins; a chat window fitted to the laptop screen's perspective. Generated images carry the scenes; code carries the explanation. Rotate transitions between whip pan, vertical whip and zoom-through. Red-pen marks on top; screen text inside the measured screen area.</style>
<check>qa.py one frame per screen: all text visible, years and numbers match the copy, settle frames on beats; check reports only intended overlaps.</check>
```
