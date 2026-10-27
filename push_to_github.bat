@echo off
setlocal
cls

echo ======================================================================
echo    Upload Olympic Analytics to GitHub (Lashika19)
echo ======================================================================
echo.

set "GIT_EXE=C:\Users\ESHU RAGHUWANSHI\AppData\Local\Microsoft\WinGet\Packages\Git.MinGit_Microsoft.Winget.Source_8wekyb3d8bbwe\cmd\git.exe"
set "REPO_URL=https://github.com/Lashika19/olympic-sports-performance-analysis.git"

echo Target Repository: %REPO_URL%
echo Target Branch:     main
echo.
echo NOTE ON GITHUB AUTHENTICATION:
echo 1. When prompted for Username: enter your GitHub username (Lashika19)
echo 2. When prompted for Password: enter your GitHub Personal Access Token (PAT)
echo    (Generate one at: https://github.com/settings/tokens with 'repo' scope)
echo.
echo ----------------------------------------------------------------------
echo Press any key to start git push...
pause >nul

echo.
echo Pushing to GitHub...
"%GIT_EXE%" push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ======================================================================
    echo   SUCCESS! All 36 files pushed to https://github.com/Lashika19/olympic-sports-performance-analysis
    echo ======================================================================
) else (
    echo.
    echo ======================================================================
    echo   Push encountered an error. 
    echo   Please verify your Personal Access Token (PAT) has 'repo' permissions.
    echo ======================================================================
)

echo.
pause
