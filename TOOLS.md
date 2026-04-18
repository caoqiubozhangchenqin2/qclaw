# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

### Football APIs

- **TheSportsDB** — 查中甲苏州东吴比赛信息
  - API Key: `123`
  - Base: https://www.thesportsdb.com/api/v1/json/{key}/

- **football-data.org** — 查其他比赛
  - API Key: `c4906718aabe4287b5963a412e4c81ce`
  - Base: https://api.football-data.org/v4/

### 观赛指南模板

用户关注的球队：英超四队（阿森纳、切尔西、桑德兰、曼联）+ 中甲苏州东吴 + 苏超苏州队

每周观赛指南结构：
1. 🏆 标题：本周观赛指南 + 日期范围（周X到周X）
2. ⚽ 英超四队对阵：逐场列出时间和对阵
   - **格式**：`主队 vs 客队｜时间｜地点`
   - **不加颜色点**（如阿森纳主场就写"阿森纳 vs xxx"，不加🔵）
   - **重点比赛加简短标注**（如"⚔️枪手客场天王山！"）
3. 🇨🇳 中甲苏州东吴：比赛信息
   - **先上网搜索确认数据**，不要直接用 TheSportsDB
   - 包括：本轮比赛时间地点 + 上轮比分结果（如有）
4. 🏟️ 苏超苏州队：比赛信息（同上，用户手动提供）
5. 📊 英超完整排行榜：20队积分榜
   - **格式**：`🥇 阿森纳 70分｜32场｜21/7/4`
   - **只用排名emoji + 队名 + 积分 + 场次 + 胜/平/负**
   - **不显示进球数、失球数、净胜球**
   - **不给桑德兰加⚫**
6. 📰 本周五大联赛热门新闻：5条
   - **每条约100字**，不能太短
   - **带来源和日期**（如📌 4月11日）
7. 🔥 本周其他焦点之战：德甲/西甲/意甲/欧冠等重头戏

### 完整 SOP（每周五执行）

📄 **详细操作手册** → `观赛指南制作SOP.md`（同一目录下）

**快速执行清单：**
1. 获取英超积分榜 → football-data.org API
2. 获取英超四队比赛 → football-data.org API
3. 搜索苏州东吴 → ProSearch（必须！不用 TheSportsDB）
4. 搜索赔率 → ProSearch（okooo / 威廉希尔 / Opta）
5. 搜索新闻 5 条 → ProSearch
6. 按模板格式输出
7. 发送

数据来源：
- 英超排行+英超比赛 → football-data.org（team ID: 57阿森纳、64切尔西、71桑德兰、66曼联）
- 苏州东吴 → **上网搜索确认**（TheSportsDB key: 123 仅作备用）
- 新闻 → ProSearch（online-search skill）
- 赔率 → ProSearch 搜索 okooo / 威廉希尔 / Opta
- 比分预测 → 搜索 "天空体育预测 英超 第X轮"
