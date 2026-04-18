@echo off
set LOGFILE=C:\Users\Administrator\.qclaw\workspace-agent-71ec60f0\backup.log
set DATESTR=

:: Get date string
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set DATESTR=%datetime:~0,4%-%datetime:~4,2%-%datetime:~6,2%

echo [%DATESTR% %time%] Starting daily backup... >> %LOGFILE%

cd /d C:\Users\Administrator\.qclaw\workspace-agent-71ec60f0\qclaw

:: Check if there are changes
git add -A
git diff --cached --quiet
if %errorlevel% equ 0 (
    echo [%DATESTR% %time%] No changes to commit. >> %LOGFILE%
    goto notify
)

:: Commit and push
git commit -m "daily-backup-%DATESTR%" >> %LOGFILE% 2>&1
git push origin qclaw-backup >> %LOGFILE% 2>&1
echo [%DATESTR% %time%] Backup completed with changes. >> %LOGFILE%
goto notify

:notify
:: Send notification via OpenClaw
curl -s -X POST "http://localhost:3737/api/message/send" ^
  -H "Content-Type: application/json" ^
  -d "{\"channel\":\"openclaw-weixin\",\"to\":\"o9cq8039msH2o9EJp56OikcRc_CY@im.wechat\",\"message\":\"[备份完成] %DATESTR% 下午4点备份已执行，详见 backup.log\"}" >> %LOGFILE% 2>&1

echo [%DATESTR% %time%] Notification sent. >> %LOGFILE%
