@echo off
chcp 65001
setlocal EnableDelayedExpansion
set cnt=0
for /f "tokens=1,2,3,*" %%i in ('git log --format^="%%aI %%cI %%h %%s"') do (
    set /a cnt += 1
    if not %%i == %%j echo !cnt! %%i %%k %%l
)

for /f "tokens=1,2" %%i in ('git log --format^="%%H %%at"') do for /f %%k in ('git log %%i~1 -1 --format^=%%at') do if %%j leq %%k echo %%i
pause
