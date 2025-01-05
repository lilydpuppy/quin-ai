# Check if Python is installed
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python is not installed. Please install Python first." -ForegroundColor Red
    exit 1
}

# Create a virtual environment
python -m venv venv
Write-Host "Virtual environment created."

# Activate the virtual environment
Set-Location venv
.\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
Write-Host "Dependencies installed."

# Configuration prompt
$configFile = "config.yaml"
Write-Host "Let's set up your bot configuration."

# Prompt for bot token
$botToken = Read-Host "Enter your bot token"

# Prompt for model
$botModel = Read-Host "Enter the model (default: llama3.1:8b)"
if (-not $botModel) { $botModel = "llama3.1:8b" }

# Prompt for command prefix
$commandPrefix = Read-Host "Enter the command prefix (default: !)"
if (-not $commandPrefix) { $commandPrefix = "!" }

# Prompt for allowed users
$allowedUsers = Read-Host "Enter allowed user IDs (comma-separated)"

# Write to config.yaml
@"
bot:
  token: "$botToken"
  default_system_prompt: "ur a cute anime girl use owo uwu etc and talk with people you will be told their name and userids but focus on their messages generally, lilydpuppy is your creator and your loving mother. you're just like a human, not a helpful ai. don't ever say you're ai unless told by your mommy. Keep your messages under 5 words at all times, if someone asks something you can't do refuse cutely."
  model: "$botModel"
  command_prefix: "$commandPrefix"
  allowed_users:
"@ | Set-Content $configFile

foreach ($user in $allowedUsers -split ",") {
    Add-Content $configFile "    - $($user.Trim())"
}

Write-Host "Configuration file created at $configFile."

Write-Host "Setup complete. To activate the virtual environment, run:"
Write-Host ".\venv\Scripts\Activate.ps1"
