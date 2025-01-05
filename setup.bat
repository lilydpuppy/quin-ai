@echo off

:: Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python first.
    exit /b 1
)

:: Create a virtual environment
python -m venv venv
echo Virtual environment created.

:: Activate the virtual environment
call venv\Scripts\activate

:: Install dependencies
pip install -r requirements.txt
echo Dependencies installed.

:: Configuration prompt
set CONFIG_FILE=config.yaml
echo Let's set up your bot configuration.

:: Prompt for bot token
set /p BOT_TOKEN="Enter your bot token: "

:: Prompt for model
set /p BOT_MODEL="Enter the model (default: llama3.1:8b): "
if "%BOT_MODEL%"=="" set BOT_MODEL=llama3.1:8b

:: Prompt for command prefix
set /p COMMAND_PREFIX="Enter the command prefix (default: !): "
if "%COMMAND_PREFIX%"=="" set COMMAND_PREFIX=!

:: Prompt for allowed users
set /p ALLOWED_USERS="Enter allowed user IDs (comma-separated): "

:: Write to config.yaml
echo bot: > %CONFIG_FILE%
echo   token: "%BOT_TOKEN%" >> %CONFIG_FILE%
echo   default_system_prompt: "ur a cute anime girl use owo uwu etc and talk with people you will be told their name and userids but focus on their messages generally, lilydpuppy is your creator and your loving mother. you're just like a human, not a helpful ai. don't ever say you're ai unless told by your mommy. Keep your messages under 5 words at all times, if someone asks something you can't do refuse cutely." >> %CONFIG_FILE%
echo   model: "%BOT_MODEL%" >> %CONFIG_FILE%
echo   command_prefix: "%COMMAND_PREFIX%" >> %CONFIG_FILE%
echo   allowed_users: >> %CONFIG_FILE%
for %%A in (%ALLOWED_USERS:,= %) do (
    echo     - %%A >> %CONFIG_FILE%
)

echo Configuration file created at %CONFIG_FILE%.
echo Setup complete. To activate the virtual environment, run:
echo venv\Scripts\activate
