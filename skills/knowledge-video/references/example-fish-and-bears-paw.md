# Example: Fish and Bear's Paw — Berkson's paradox (10-05 / 10-06, Chinese original)

> Kept in the original Chinese, like `example-ai-history.md`. A 3-minute explainer with no narration in the night-sky particle look of the Douyin hit *Information Theory*, revised three times on the author's feedback: in v1 one scatter plot held half the video; v2 split it into 18 scenes with a moving camera; v3 filled in the missing steps of the reasoning. The lessons are folded into `notes.md`, `visuals.md`, `sound.md` and `pitfalls.md`.

《信息论》那种夜空光点风的一条，3:01，没有旁白，中英双语字幕。看它是怎么一轮轮改好的，题材和画面别照抄。

## 怎么来的

1. 先拆了两条头部（《信息论》《运气的形状》），得出爆的公式：生活问题 + 硬核原理、第 0 帧就让观众作答、先体验后命名、每个点配一个看得见的小实验、中段反转、结尾落到观众身上再请观众互动
2. 第一个选题《词语的地图》（词向量）被作者否了：讲的是 AI 内部原理，够不着头部
3. 作者从两个备选里选了伯克森悖论，样式要《信息论》那种，加粒子动效

## 改了三轮

| 轮 | 作者的话 | 改了什么 |
|---|---|---|
| v1 | — | 夜空 + 一张散点图撑了一半时间 |
| v2 | 「动效变化很单调，质感比《信息论》差很多」 | 拆成 18 个场景，上一个画面变成下一个，镜头一直动，加星云、视差星空、流星、暗角；音效 8 → 29 处 |
| v3 | 「画面好一点了，不会这么死板」「文案有点看不懂」 | 补上推理缺的几步（「长得一般的，得性格特别好你才会注意」「没糖尿病还住了进来，多半是因为胆囊炎」），「筛子」第一次出现就在字幕里点名，例子各补一句原因，相关系数和人数旁边写人话，画面上标出 √ / ×；「个个都有胆囊炎」改成「反而多得多」；拆开的句子按字数重新分时间；镜头推近时坐标轴压到字幕，镜头抬高 |

## 数据

- 1000 人的模拟，颜值、性格独立（随机种子 1946）：全体相关 −0.005；只留「两项相加够分」的 355 人，−0.547；再拿走「两样都好」的 65 人，剩 290 人，−0.833。画面上的人数和相关系数都是这次实算
- 医院、馆子、演员都标「示意」

## 用时参考

查证 + 模拟 + 片名取点约 20 分钟；v1 画面约 1 小时；v2 重做画面约 1.5 小时；v3 改文案约 40 分钟；每次整条渲染 5–6 分钟（画布 1000 个光点 + 星空）
