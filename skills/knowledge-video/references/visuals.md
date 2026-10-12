# Visuals: approaches and lessons from tested videos

What tested videos confirmed, kept for reference, not as rules. Design each video for its own topic first; use these when you hit the same problem or the user asks for the same style.

## Dense collage (tested 2025-10, approved by the author)

What "lots of cut-outs layered together" / "the Vox look" turned into: one full-frame scene background per scene (torn paper, halftone, old newspaper in the corners), 3–6 transparent subjects on top, scraps flying in at the corners; one torn-paper title label per scene (4–6 words) and each screen's line in a black subtitle bar at the bottom (key word highlighted); four parallax layers (background, subjects, foreground subjects, scraps) drifting; comparisons told with the picture (a person at a fork in the road, a robot arm playing Go…); a retro palette (cream, red-orange, navy, mustard) in the image-prompt prefix; number stamps, handwritten notes, logo tags and torn-paper cards drawn in code.

Movements that video used (examples, not a checklist): slow push-in on backgrounds, subject layers bobbing, scraps fluttering, titles popping in letter by letter, the subtitle's key word bouncing, photo cards wobbling as they settle, numbers counting, bars growing, lines drawing, transitions rotating between whip pan, vertical whip and zoom-through. The author's note was "richer motion": the picture shouldn't freeze.

## Make a timeline's moments visible

With years only in the subtitles, viewers lost track of where they were in the history (the author's note). What worked: a big year stamp opening each scene, shrinking into a corner as the screen ends, and a timeline in the corner whose label moves along each scene, visited dots changing color.

## Photo cards for real people

Named people get freely licensed photos as printed photo cards: white border, tape, the name under the photo, a small "photo: author · license · cropped" line; list them in `credits.md` too.

## Generated phone, laptop and terminal screens

- Measure the blank screen first: the largest connected region in the screen's center color (it isn't always pure white); keep text and buttons inside it with `white-space: nowrap`, converting coordinates by the displayed width
- Screens are often in perspective (a skewed quadrilateral): take the four corners and compute a `matrix3d` (a homography, an 8-unknown linear system) that maps the rectangular UI onto it. A plain rectangle on top looked pasted on, and the author noticed at once

## Draw in code what code should draw

Generated images carry scenes and objects; processes (a chain folding bead by bead, bars growing, a dial turning), data (charts, proportions), interfaces (chat windows, terminals, keyboards) and exact pointers (circling one stone, a line to one person) are SVG / DOM, animated from time (one progress value, onUpdate computing every point). The author's words: "where it matters, draw it in code; don't lean only on generated images".

## Red-pen marks on top

Red circles, lines and crosses sit above photo cards, logo tags and stickers (below only titles, year stamps, the timeline and subtitles), or they get hidden.

## Company and product logos

LobeHub's open icons (npm `@lobehub/icons-static-svg`, MIT; `npm pack` gives a folder of SVGs: openai, deepmind-color, deepseek-color, anthropic, claudecode-color, google-color…) as small "logo + name" tags, used only to refer to the company, shape and color unchanged.

## Night-sky particles (the *Information Theory* look, tested 10-06 on *Fish and Bear's Paw*)

The author's verdict on the first version: "the motion barely changes; it looks far worse than *Information Theory*". One scatter plot held the screen for over half the video, the camera never moved, and the background was a single layer of stars. The author found the second version "better, not so stiff". Below is what it did; with a new topic, rethink the pictures for that topic. What carries over is the thinking, not these scenes.

- **Find something that moves for each idea**: "one up, the other down" became a seesaw, "all alike" a row of identical empty shells, "not noticed" a sieve sweeping across. 18 scenes in 3 minutes; no picture held the screen for long
- **The last picture becomes the next** instead of cutting: the title's particles fall into the windows of a night city, then rise from the windows into the plot; the opening seesaw comes back sitting on the red line
- The camera pushes in, pulls out, whips to another scene, and turns 45° and pushes in for the payoff line
- **Light** (technique, useful whatever the topic): a radial-gradient sprite drawn with `lighter` blending (not `shadowBlur` on thousands of dots); lines stroked three times (wide and faint, medium, thin and bright) for glow, with a comet head while drawing; a slowly drifting nebula, three parallax star layers, a few shooting stars, a vignette
- Colors mean something: gold = people still in your eyes, grey-blue = sifted out, pale cyan = taken by someone else, red = the line the sieves drew
- Changes in the data are actions: people sifted out fall like sand, people taken rise away as lanterns, the restoration plays it backwards; the key step of the reasoning is labelled in the picture ("plain, but very kind ✓", "average at both · never noticed ✗")
- Particle title: render the title in the same font to a bitmap and take 1000 points by farthest-point sampling
- **Keep the caption strip clear when the camera pushes in**: a push-in moves the axis and its labels down into the captions (at 80 s the "looks →" label sat on the caption). For each camera keyframe, check where the lowest thing lands: screen y = 540 + (scene y − camera center y) × zoom
- Film grain as one **static** tile at low opacity. Grain that changes every frame bloats the file (1.8 GB for 3 minutes), and the platform's re-encode turns it into blocks
