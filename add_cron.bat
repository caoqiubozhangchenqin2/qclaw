@echo off
chcp 65001 >nul
openclaw cron add --name "daily-backup" --cron "0 16 * * *" --session isolated --agent agent-71ec60f0 --message "Execute daily backup task: 1.Backup chat records and important files to workspace directory 2.git add -A 3.git commit -m daily-backup with todays date 4.git push origin qclaw-backup 5.Report backup results. Note: This is an actual operation task, execute directly, not just a reminder. Do not reply HEARTBEAT_OK" --announce --channel openclaw-weixin --to o9cq8039msH2o9EJp56OikcRc_CY@im.wechat --account 7cdca2e9ce9d-im-bot
echo EXIT_CODE=%ERRORLEVEL%
