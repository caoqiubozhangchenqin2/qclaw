@echo off
chcp 65001 >nul
echo Opening magnets in Thunder...

REM MIDA-551 UC
start "" "thunder://QU1vW2NvZGU9aHR0cDovL3RyYWNrZXIua3R4cC5jb206Njg2OC9hbm5vdW5jZSZ0cj1odHRwOi8vdHJhY2tlci5rdHhwLmNvbTo3MDcwL2Fubm91bmNlJnRyPXVkcDovL3RyYWNrZXIua3R4cC5jb206Njg2OC9hbm5vdW5jZSZ0cj11ZHA6Ly90cmFja2VyLmt0eHAuY29tOjcwNzAvYW5ub3VuY2Vd"

REM 或者直接用 magnet
start "" "magnet:?xt=urn:btih:F3E5D8C9A2E8B4D7C1A9F2E5B8D7C3A6F1E9B5D8&dn=MIDA-551-UC"
timeout /t 2 /nobreak >nul

echo Done
