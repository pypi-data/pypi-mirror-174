@echo off
for /f %%i in ('git log -1 --oneline') do git branch bak-%%i
for /f "tokens=1,2,3" %%i in ('git log --reverse --format^="%%H %%at %%ct"') do (
    set GIT_COMMITTER_DATE=%%j
    if defined first (
        git cherry-pick %%i
    ) else if not %%j == %%k (
        set first=1
        git reset --hard %%i
        git commit --amend --no-edit --quiet
    )
)
pause
