<h1 align="center">knowledge-video</h1>

<p align="center">
  <em>把一个知识点做成一条让人想看完的知识视频。给一条可走的路，不给剧本：每条片子怎么设计由 agent 自己定。</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-111111?style=flat-square" alt="MIT">
  <img src="https://img.shields.io/badge/works%20with-any%20SKILL.md%20agent-111111?style=flat-square" alt="Agents">
  <img src="https://img.shields.io/badge/render-HyperFrames-111111?style=flat-square" alt="HyperFrames">
  <img src="https://img.shields.io/badge/tested-end%20to%20end-111111?style=flat-square" alt="Tested end to end">
</p>

<p align="center">
  <sub><a href="README.md">English</a></sub>
</p>

---

<p align="center">
  <img src="docs/hero.gif" alt="用 knowledge-video 做的两段开头：课堂笔记风的「今天 AI 会自己学，这思路源自哪年？」，色卡风的「天空为什么是蓝的？」" width="800"><br>
  <sub>两段实测开头 —— 上：人工智能简史，课堂笔记风；下：天空为什么是蓝的，色卡风</sub>
</p>

一个 agent skill，做抖音 #Vibe知识大赏 里那种知识视频：代码画的动画，画面上一句一句的字配音乐，两三分钟讲清一件事。AI 不直接生成视频，它查资料、写文案、搭一个 [HyperFrames](https://www.npmjs.com/package/hyperframes) 工程，再渲成 MP4。

这个 skill 故意写得很轻。它只守几条底线（事实有出处、素材能用、不用 AI 画真人的脸、同一帧每次渲出来都一样），给一条走得通的路（查证 → 文案 → 配图 → 样式和分镜 → 出片，默认每步给你看一眼，免得方向错了白渲），再加几个剪配乐、排拍子、配音效、自查的小工具。片子怎么写、长什么样、怎么动，交给 agent 自己设计；做过的片子留下的经验放在 `references/` 里，是范例，不是规定。下面的六步是这条路第一次实测时的样子。

## 六步

| 步 | 它做什么 | 你看什么 |
|---|---|---|
| ① 搜集 | 先看知识长什么样（时间线、因果链、由浅到深、对照、一问一答、故事），上网查，写成带出处的文章，多找几个点备选；**找不到可靠出处的删掉**；按时长给两三个「讲几个点」的方案 | 讲几个点（你来选）、删了什么、哪些是转述 |
| ② 编排 | 改成一屏一句的视频文案，每屏 ≤ 20 字；第一屏就是问题本身，接着讲故事、打比方、一次反转、结尾落到普通人 | 开头那道题、总长 |
| ③ 配图 | 两条路：列真实的图（老照片、论文、实物、示意图：网址、截哪一块、许可、作者，优先公有领域和 CC0）；或者写分层的生图提示词（每幕一张背景 + 主体单独出，统一画风前缀，图里不带字、不画真人脸），交给你自己的生图工具 | 许可或提示词；你去截图或出图 |
| ④ 定样式、写分镜 | 三个差别大的样式，各用第一屏出一张样图，并推荐一个；再测出配乐的速度和小节（`scripts/beats.py`），每个镜头写到第几小节第几拍，答案揭晓、反转落在音乐的变化上 | 选样式；检查分镜 |
| ⑤ 检查 | 按你说的改，重新对拍，告诉你哪些卡点变了 | — |
| ⑥ 直出 | 先渲开头 10 秒左右，自己抽帧查字出框、太小、年份不对、动作不在拍上，改完再给你；你满意了再渲整条 | 开头 |

## 实测

两次，都是在空文件夹里用 Claude Code + Claude Opus 5.5：

- **人工智能简史**：不装 skill，照下面六步手动一句句打，从第一句到开头出来，它前后跑了约 58 分钟。每一步的产出和用时写在 [`references/example-ai-history.md`](skills/knowledge-video/references/example-ai-history.md)
- **天空为什么是蓝的**：装上 skill，只说一句「我想做一条知识视频，讲为什么天空是蓝色的。配乐在文件夹里。」它自己用上 skill，每一步都停下，6 轮约 43 分钟出了开头。中间删了 3 条核不到原始出处的说法；找了 15 张能免费商用的图，还提醒一张 NASA 全景调过白平衡，会把火星的天调成蓝的；答案揭晓落在音乐第一次变响的那一小节；交开头之前自己抽帧查出 6 个问题并改掉

## 不装 skill：一段总提示词

不装 skill 也能用：把下面这段发给 agent，【】换成你的知识点。它会在每一步动手前，按你的需求把标签填成一份完整的提示词，给你看过再照着做（能派 subagent 的，就把填好的提示词交给 subagent 去做）。早先实测用的六段原文在 git 历史里。

<details>
<summary>总提示词</summary>

```
<task>帮我把【你的知识点】做成一条知识视频，按 查证 → 文案 → 配图 → 样式和分镜 → 出片 这条路走。开工先写一份简报 提示词/简报.md；每一步动手前，再把这一步的提示词填好，存成 提示词/步骤名.md，给我看一眼，然后照着做。量大、能独立做完的步骤（查资料、找图、写画面代码和渲染），把简报和这一步的提示词交给 subagent 去做，你检查它的产出。</task>
<context>简报只有一个 context 标签：讲什么、给谁看、看完记住什么、多长、横竖、配乐、我喜欢和不喜欢什么、前面定下的东西、文件在哪；每步做完更新。
每一步的提示词四个标签：role（这一步由什么角色来做、最在意什么，比如知识整理师、编剧、美术指导、分镜师、动效设计师，按步骤挑）；task（产出什么、存到哪）；style（推荐的做法和理由，只是推荐、不是规定，我说过的照我说的）；check（做完逐条看什么才算完成）。style 用不上就不写。
我没说的你按知识点推断着填，拿不准的问我。</context>
<check>事实都要有出处，找不到的不讲；图、音乐、音效、字体都要许可允许，署名写进 出处和署名.md；不用 AI 画真人的脸；成片交给我之前自己从头看一遍。</check>
```

</details>

## 快速开始

在一个空文件夹里放一首配乐，在这个文件夹里打开你的 agent，说你想讲什么：

```
我想做一条知识视频，讲为什么天空是蓝色的。配乐在文件夹里。
```

## 需要什么

- 能读 SKILL.md、能上网搜索的 agent。实测用的是 Claude Code 2.1.287 + Claude Opus 5.5
- Node.js 22 以上（HyperFrames 要用）
- Python 3（要有 numpy）和 FFmpeg（测拍子、处理配乐）

## 安装

把这句话贴给任何一个编程 agent：

```
Install the knowledge-video skill from https://github.com/Win-Hao/knowledge-video
```

或者用 [skills CLI](https://github.com/vercel-labs/skills)：

```bash
npx skills add Win-Hao/knowledge-video -g
```

Claude Code 插件（跟着仓库更新）：

```
/plugin marketplace add Win-Hao/knowledge-video
/plugin install knowledge-video@knowledge-video
```

手动（拷文件，固定在当前版本）：

```bash
git clone https://github.com/Win-Hao/knowledge-video.git
cp -R knowledge-video/skills/* ~/.claude/skills/   # Claude Code
```

## 发布之前

- 简介里写上文章的出处和图的署名，改过的图注明「已修改」（skill 会写一份 `credits.md`）
- 发布页有「AI 生成内容」声明的，选上
- 参加平台活动的，照活动页的规则

## 仓库结构

```
skills/knowledge-video/
  SKILL.md                         一条可走的路、几条底线、先填提示词再照着做
  scripts/beats.py                 测速度、拍点、小节线、响度变化（numpy + FFmpeg）
  scripts/music_loops.py           找配乐里能无缝重复或剪掉的小节
  scripts/cut_music.py             按小节表拼出新配乐，拍子网格不偏
  scripts/timing.py                把文案的每一屏排到拍子上
  scripts/sfx.py                   下载 Kenney 的 CC0 拟音、混音效轨
  scripts/qa.py                    每屏抽帧拼总览、关键拍点前后帧
  references/                      做过的片子留下的范例和经验（参考，不是规定）
docs/hero.gif
```

## 许可

MIT。`docs/hero.gif` 里的照片来自维基共享资源：IBM 704（NASA，公有领域），蓝天（TheUltimateGrass，CC0）。
