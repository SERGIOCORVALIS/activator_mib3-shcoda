@echo off
REM Automated build for LG MEN3 Activator for Windows
REM Usage: auto_build.bat [--update|--verify|--no-backup|--quiet]

python auto_build.py %*

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo BUILD COMPLETED SUCCESSFULLY
    echo ========================================
) else (
    echo.
    echo ========================================
    echo BUILD COMPLETED WITH ERRORS
    echo ========================================
    exit /b %ERRORLEVEL%
)

