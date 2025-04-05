@echo off

:: Setup
echo Deployment started
setlocal enabledelayedexpansion

:: 1. Set variables
set PYTHON_EXE=python.exe
set KUDU_SYNC_CMD=kudusync

:: 2. Install Python if not installed
where %PYTHON_EXE% >nul 2>&1
if %ERRORLEVEL% neq 0 (
  echo Python not found in PATH, installing...
  powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.9.13/python-3.9.13-amd64.exe' -OutFile 'python-installer.exe'; Start-Process -FilePath 'python-installer.exe' -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1' -Wait"
)

:: 3. Create virtual environment if it doesn't exist
if not exist "%DEPLOYMENT_TARGET%\env\" (
  echo Creating virtual environment...
  cd "%DEPLOYMENT_TARGET%"
  %PYTHON_EXE% -m venv env
)

:: 4. Activate virtual environment and install dependencies
echo Installing dependencies...
call "%DEPLOYMENT_TARGET%\env\Scripts\activate.bat"
%PYTHON_EXE% -m pip install --upgrade pip
pip install -r "%DEPLOYMENT_TARGET%\requirements.txt"

:: 5. Setup completed
echo Deployment completed successfully.
endlocal
exit /b 0 