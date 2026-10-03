<h1 align="center">knowledge-video</h1>

<p align="center">
  <em>把一个知识点做成一条 1–3 分钟的知识视频。六步走，每一步做完都停下来，等你点头再往下。</em>
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

这个 skill 大半在管一件事：**别白渲**。一条两分钟的片子渲一遍要很久，方向错了全白做。所以拆成六步，每步做完都停下：在文章、文案、分镜上改一句话，比成片出来再改快得多。最后一步也只先渲开头 10 秒，你满意了再渲整条。

## 六步

| 步 | 它做什么 | 你看什么 |
|---|---|---|
| ① 搜集 | 上网查，写成带出处的文章：讲历史挑 8–10 个节点，讲原理拆成 5–8 个点；**找不到可靠出处的删掉** | 删了什么、哪些是转述 |
| ② 编排 | 改成一屏一句的视频文案，每屏 ≤ 20 字；第一屏就是问题本身，接着讲故事、打比方、一次反转、结尾落到普通人 | 开头那道题、总长 |
| ③ 找图 | 每幕列一张真实的图（老照片、论文、实物、示意图）：网址、截哪一块、许可、作者，优先公有领域和 CC0；署名文字写好 | 许可；你去截图，或者让它直接存 |
| ④ 定样式、写分镜 | 三个差别大的样式，各用第一屏出一张样图，并推荐一个；再测出配乐的速度和小节（`scripts/beats.py`），每个镜头写到第几小节第几拍，答案揭晓、反转落在音乐的变化上 | 选样式；检查分镜 |
| ⑤ 检查 | 按你说的改，重新对拍，告诉你哪些卡点变了 | — |
| ⑥ 直出 | 先渲开头 10 秒左右，自己抽帧查字出框、太小、年份不对、动作不在拍上，改完再给你；你满意了再渲整条 | 开头 |

## 实测

两次，都是在空文件夹里用 Claude Code + Claude Opus 5.5：

- **人工智能简史**：不装 skill，照下面六步手动一句句打，从第一句到开头出来，它前后跑了约 58 分钟。每一步的产出和用时写在 [`references/example-ai-history.md`](skills/knowledge-video/references/example-ai-history.md)
- **天空为什么是蓝的**：装上 skill，只说一句「我想做一条知识视频，讲为什么天空是蓝色的。配乐在文件夹里。」它自己用上 skill，每一步都停下，6 轮约 43 分钟出了开头。中间删了 3 条核不到原始出处的说法；找了 15 张能免费商用的图，还提醒一张 NASA 全景调过白平衡，会把火星的天调成蓝的；答案揭晓落在音乐第一次变响的那一小节；交开头之前自己抽帧查出 6 个问题并改掉

## 不装 skill，手动照着打

skill 就是从这几段提示词长出来的，不装也能用。下面是实测原文，**【】里的换成你自己的**。

<details>
<summary>六步提示词</summary>

① 搜集
```
<role>你是知识科普作者，最在意事实准确。</role>
<task>上网搜「人工智能的发展简史」，挑 8 到 10 个关键节点，每个写清哪一年、谁、做了什么、为什么重要。整理成一篇知识文章，存成 文章.md。</task>
<check>年份、人名、数字、原话都要有出处，链接写在每段后面；找不到可靠出处的节点删掉。</check>
```

② 编排
```
<role>你是抖音知识视频的编剧，擅长把复杂的事讲给完全不懂的人听。</role>
<context>这篇要做成 2 分钟左右的横屏视频，没有旁白，观众只看画面上的字配音乐，所以每句话都要短、一看就懂。</context>
<task>把 文章.md 改成视频文案，存成 文案.md，分成一幕一幕：开头先抛一个问题让观众猜；中间当故事讲，用至少一个生活里的比方，安排一次反转；结尾落到普通人身上。</task>
<avoid>不解释就用专业术语；一屏超过 20 个字；文章.md 里没有的事实。</avoid>
```

③ 找图
```
<context>视频不能只有字，每一幕都要有一张真实的图（老照片、论文首页、机器的样子），看起来才不干巴。图我自己去网页上截。</context>
<task>按 文案.md 一幕一幕列出要用的图：在哪个网址、截网页上的哪一块、用在第几幕，存成 找图.md。</task>
<avoid>标着版权所有、来路不明的图。优先用公有领域、自由许可的，每张写清出处和许可。</avoid>
```
截好的图放进文件夹里的「素材」文件夹，文件名用幕号开头（比如 `03-深蓝.png`）。

④ 定样式 + 写分镜
```
<task>素材文件夹里是我截好的图。这条视频用 HyperFrames 来做。先给我 3 个差别大的画面风格，每个用开头那一幕做一张 1920×1080 的样图，各说一句为什么适合。先别往下做，等我选。</task>
<avoid>深色背景配霓虹光；字都堆在正中间；紫色渐变；所有东西都淡入淡出。</avoid>
```
```
<role>你是动效导演，最在意节奏。</role>
<task>用 C 这个风格，写分镜脚本 分镜.md：每个镜头写几秒、画面、字、用哪张图、怎么动。截图要处理成这个风格的样子，别直接贴上去。配乐是文件夹里的 bgm.mp3，先找出拍子，镜头切换卡在拍子上。写完先停，等我检查。</task>
<specs>横屏 1920×1080，每秒 30 帧，总长跟着文案走。</specs>
```

⑤ 检查：看每个镜头的字能不能一眼读完、年份对不对、节奏拖不拖，要改的直接说，不用写标签。实测时说的是：「分镜可以，配乐照你说的剪。改一处：开头别先写『考你一个问题』，第一秒就把问题亮出来，前两秒留不住人，观众就划走了。改完先停。」

⑥ 直出
```
<task>分镜可以，照着做。先只做开头 10 秒，渲成 MP4 给我看，我满意了再做整片。</task>
<check>做完自己抽几帧看：字有没有出框、重叠、太小；年份和文案对不对；切换在不在拍子上。有问题改完再给我。</check>
```

**要改成你自己的地方**

| 卡 | 原文 | 怎么改 |
|---|---|---|
| ① | 人工智能的发展简史 | 换成你的知识点，比如「为什么天空是蓝的」 |
| ① | 8 到 10 个关键节点 | 讲原理就改成「拆成 5 到 8 个要讲清楚的点」 |
| ② | 2 分钟左右的横屏视频 | 时长按内容定；发竖屏就写「竖屏」 |
| ② | 没有旁白，观众只看画面上的字配音乐 | 自己配音就改成「有旁白，字跟着旁白走」 |
| ③ | 老照片、论文首页、机器的样子 | 换成你这个知识点会有的图，比如「光谱图、日落照片」 |
| ③ | 图我自己去网页上截 | 有生图工具就改成「图我用生图工具出，你写清每幕要什么」 |
| ④ 上 | avoid 那一行 | 后面接着写你自己不想要的，比如「不要卡通人物」 |
| ④ 下 | C | 换成你选的那张 |
| ④ 下 | bgm.mp3 | 换成你的配乐文件名 |
| ④ 下 | 横屏 1920×1080 | 竖屏就写「竖屏 1080×1920」 |

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
  SKILL.md                         六步流程
  scripts/beats.py                 测速度、拍点、小节线、响度变化（numpy + FFmpeg）
  references/example-ai-history.md 一次完整实测，每步的产出和用时
docs/hero.gif
```

## 许可

MIT。`docs/hero.gif` 里的照片来自维基共享资源：IBM 704（NASA，公有领域），蓝天（TheUltimateGrass，CC0）。
