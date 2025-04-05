@echo off
echo Creating virtual environment...
python -m venv env

echo Installing dependencies...
call env\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

echo Setting up Azure App Service...
:: Create folders if they don't exist
if not exist %HOME%\LogFiles mkdir %HOME%\LogFiles

echo Deployment completed successfully. 