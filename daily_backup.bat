@echo off
chcp 65001 >nul
setlocal

set REPO=C:\Users\Administrator\.qclaw\backup-qclaw
set WORKSPACE=C:\Users\Administrator\.qclaw\workspace-agent-71ec60f0
set LOG=%WORKSPACE%\backup.log

echo [%date% %time%] ====== 备份开始 ====== >> %LOG%

cd /d %REPO%
git fetch origin >> %LOG% 2>&1

for %%F in (AGENTS.md HEARTBEAT.md IDENTITY.md MEMORY.md SOUL.md TOOLS.md USER.md 上课记录.md schedule.md) do (
    if exist "%WORKSPACE%\%%F" copy /Y "%WORKSPACE%\%%F" "%REPO%\%%F" >> %LOG% 2>&1
)

xcopy /Y /E "%WORKSPACE%\memory\*" "%REPO%\memory\" >> %LOG% 2>&1

for %%F in (
    .consolidate-state.json add_cron.bat all_windows.py auto_confirm_qbt.py
    backup-report-*.md backup.log batch_*.py check_*.ps1 chrome_*.ps1
    click_*.py config_qbt.ps1 cron_list.bat daily_backup.bat debug_tk.py
    dl_*.bat dl_remaining.py enable_dht.py extract_magnet.py
    find_*.ps1 find_*.py fix_mida523.py get_ch_magnet.py get_magnet.py
    hawa_utf8.txt list_windows.py magnets.txt mudr363_search.html
    open_all*.bat open_mudr363ch.bat package*.json page_structure.ps1
    pil_screen.py press_enter.py qbt_window_tree.py read_prefs.py
    results*.txt scrape_*.py screen_*.ps1 search_chuanmei.py search_news*.js
    solid_check.py start_downloads.py sunderland-add*.md task-summary*.md
    test_thunder.bat thunder_*.ps1 tk_*.py tmp_search.js try_keys.py
    weekly-guide*.md 上课记录.md 观赛指南*.md 观赛指南*.md
    观赛指南制作SOP.md
) do (
    if exist "%WORKSPACE%\%%F" copy /Y "%WORKSPACE%\%%F" "%REPO%\%%F" >> %LOG% 2>&1
)

cd /d %REPO%
git add -A >> %LOG% 2>&1
git status --short >> %LOG% 2>&1

for /f "delims=" %%i in ('git status --short') do (
    git commit -m "每日备份 %date% %time%" --author "QClaw Agent <agent@qclaw>" >> %LOG% 2>&1
    git push origin qclaw-backup >> %LOG% 2>&1
    echo [%date% %time%] 备份已推送 >> %LOG%
    goto :done
)

:done
echo [%date% %time%] 无变化，跳过推送 >> %LOG%
endlocal