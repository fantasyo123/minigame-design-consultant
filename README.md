# 小游戏策划与玩法设计顾问（Skill）

> 把微信小游戏的玩法创意，变成可评审、可交付给开发团队的策划方案。策划侧全流程：立项 → 核心循环 → 关卡机制 → 美术 UX → 剧情 → 变现 → 合规 → 交付规格。

一个可移植的 Agent Skill 包：WorkBuddy / Claude Code / Codex 等支持 `SKILL.md` 约定的 Agent 均可直接加载。它是**策划与体验设计顾问**，不写游戏工程代码。

## 它解决什么问题

大多数"我想做个小游戏"会卡在三个地方：玩法说不清、版号没算进排期、给开发的文档没法验收。这个 skill 用一套阶段化工作流把三件事钉住：

| 阶段 | 产出 | 解决的问题 |
|---|---|---|
| 0 · 诊断 | 立项决策卡 | 能不能做、卡在哪、要多久 |
| 1 · 核心循环 | 循环图 + 留存付费表 | 凭什么留住人 |
| 2 · 关卡机制 | 机制矩阵 + 难度曲线 + 数值表 | 内容怎么排 |
| 3 · 美术 UX | 风格三件套 + 首 60 秒脚本 | 长什么样、第一分钟怎么留人 |
| 3b · 剧情 | 体量档位 + 对话脚本格式 | 内容成本可控 |
| 4 · 合规 | 提审自测清单 + 驳回原因库 | 会不会被拒 |
| 5 · 变现 | 广告位 + 内购边界 | 靠什么赚钱 |
| 6 · 交付 | 开发规格说明书 + 验收标准 | 开发不用回来问 |

## 安装

**WorkBuddy（用户级，全局可用）**

```bash
git clone https://github.com/fantasyo123/minigame-design-consultant.git \
  ~/.workbuddy/skills/minigame-design-consultant
```

**项目级（团队共享）**

```bash
git clone https://github.com/fantasyo123/minigame-design-consultant.git \
  <project>/.workbuddy/skills/minigame-design-consultant
```

**Claude Code / 其他 Agent**

克隆到对应 skills 目录（如 `~/.claude/skills/`），或直接把 `SKILL.md` 与 `references/` 作为知识文件挂载。`SKILL.md` 只依赖标准 YAML frontmatter（`name` / `description`），无私有字段。

## 目录结构

```
minigame-design-consultant/
├── SKILL.md                      # 主入口：路由表 + 执行要点 + 输出规范
├── references/
│   ├── stage-0-project-card.md   # 形态边界、主体资质、成本排期、版号风险
│   ├── core-loop.md              # 乐趣原子、三层循环、数值反推、钩子
│   ├── level-mechanics.md        # 机制组合矩阵、四段难度曲线、角色参数谱
│   ├── art-ux.md                 # 风格三件套、反馈三层、首 60 秒脚本
│   ├── narrative.md              # 剧情体量、分支结构、对话脚本格式、VO
│   ├── monetization.md           # 广告位规划、内购边界、分享合规
│   ├── compliance-review.md      # 提审自测清单、驳回原因库、素材红线
│   └── handoff-spec.md           # 规格说明书七章结构、可验收写法
└── assets/templates/
    ├── project-card.md           # 立项决策卡模板
    ├── core-loop-table.md        # 核心循环设计表模板
    └── dev-spec.md               # 开发规格说明书模板
```

## 三条硬边界（本 skill 的立场）

1. **形态差异**：小游戏 ≠ 小程序。无 WXML/WXSS，Canvas/WebGL 渲染，`game.js` + `game.json` 入口，包体与开放数据域能力都不同。
2. **主体资格**：个人主体不能注册微信小游戏，需企业/组织主体。
3. **版号前置**：国内上线的微信小游戏需提供版号，无版号不可上线、更不可开内购。版号周期以月计，必须从 Day 1 并行。

> 政策与平台限额会更新。本仓库只给判断框架与查证入口，具体数字以[国家新闻出版署](https://www.nppa.gov.cn/)与[微信开放社区](https://developers.weixin.qq.com/community/)最新公告为准。

## 使用示例

```
我想做一款以"整理行李"为核心玩法的休闲小游戏，帮我看看能不能立项。
帮我设计这款游戏的核心循环，要求单日时长 10 分钟左右。
我的小游戏要接激励视频广告，广告位怎么排才不会掉留存？
小游戏上线需要软著和版号吗？给我一份提审自测清单。
把上面的方案整理成能直接交给开发的规格说明书。
```

## 范围边界

- ✅ 创意策划、核心循环、关卡机制、美术 UX、剧情规划、变现设计、合规要点、交付规格
- ❌ 不写游戏工程代码（只给行为描述与接口契约）
- ❌ 不代申请版号软著、不伪造材料、不提供绕过审核的方法
- ❌ 不出具具有法律效力的合规背书（由持证出版单位与法务承担）

## License

MIT
