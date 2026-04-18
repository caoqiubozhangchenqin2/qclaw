@echo off
chcp 65001 >nul
openclaw cron list
echo EXIT_CODE=%ERRORLEVEL%
