- **2026-04-15**：记忆系统启用

## 观赛指南（每周五执行）

**Skill 已创建**：`D:\Qclaw\resources\openclaw\config\skills\weekly-football-guide\SKILL.md`
**SOP 文档**：`观赛指南制作SOP.md`（workspace，同步记录）

**关注球队：**
- 英超：阿森纳(57)、切尔西(61)、利物浦(64)、桑德兰(71)、曼联(66)
- ⚠️ 注意：API中切尔西ID是61，利物浦ID是64，之前记录有误
- 中甲：苏州东吴
- 苏超：苏州队（数据由用户手动提供）

**格式规范（最终确认版，2026-04-17）：**
- 英超对阵：格式`主队 vs 客队｜时间｜地点`，不加颜色点，不加⚫
- 积分榜：`🥇 阿森纳 70分｜32场｜21/7/4`，只用胜/平/负，不显示进球/失球/净胜球
- 桑德兰积分榜中不加⚫
- 中甲苏州东吴：**必须上网搜索确认**（ProSearch），不能用 TheSportsDB
- 新闻每条约100字，带来源和日期
- 赔率来源：okooo / 威廉希尔 / Opta，注明来源

**数据来源：**
- football-data.org API (key: c4906718aabe4287b5963a412e4c81ce)
- ProSearch (online-search skill)：苏州东吴、赔率、新闻
- 用户提供：苏超苏州队数据

**已确认赔率（2026-04-19 第33轮）：**
- 切尔西 vs 曼联(03:00)：主胜2.03 / 平3.55 / 客胜2.82（okooo）
- 曼城 vs 阿森纳(23:30)：机构均势盘主胜2.15-2.25（多数机构）
- 维拉 vs 桑德兰(21:00)：主胜1.61 / 平3.90 / 客胜5.25（威廉希尔）
- 苏州东吴主场场地：昆山市体育中心（第6轮起）

## 当前项目与关注

- GitHub 仓库：https://github.com/caoqiubozhangchenqin2/qclaw

## 经验与决策

- `openclaw cron add` CLI在当前环境不稳定（QQBOT警告导致超时kill），但任务实际会写入；可先CLI创建再手动编辑 `C:\Users\Administrator\.qclaw\cron\jobs.json` 清理重复任务
- git push 在 PowerShell 下可能误报 exit code 1（git 将正常提示写入 stderr），实际推送成功；wincred 凭证管理器已配置，GitHub 账号 `caoqiubozhangchenqin2` 认证正常
