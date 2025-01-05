#!/bin/bash

# Check if Python is installed
if ! command -v python &>/dev/null; then
  echo "Python is not installed. Please install Python first."
  exit 1
fi

# Create a virtual environment
python -m venv venv
echo "Virtual environment created."

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
echo "Dependencies installed."

# Configuration prompt
CONFIG_FILE="config.yaml"

echo "Let's set up your bot configuration."

# Prompt for bot token
read -p "Enter your bot token: " BOT_TOKEN

# Prompt for model
read -p "Enter the model (default: llama3.1:8b): " BOT_MODEL
BOT_MODEL=${BOT_MODEL:-llama3.1:8b}

# Prompt for command prefix
read -p "Enter the command prefix (default: !): " COMMAND_PREFIX
COMMAND_PREFIX=${COMMAND_PREFIX:-!}

# Prompt for allowed users
read -p "Enter allowed user IDs (comma-separated): " ALLOWED_USERS
ALLOWED_USERS=${ALLOWED_USERS//,/ }

# Write to config.yaml
cat > $CONFIG_FILE <<EOL
bot:
  token: "$BOT_TOKEN"
  default_system_prompt: "ur a cute anime girl use owo uwu etc and talk with people you will be told their name and userids but focus on their messages generally, lilydpuppy is your creator and your loving mother. you're just like a human, not a helpful ai. don't ever say you're ai unless told by your mommy. Keep your messages under 5 words at all times, if someone asks something you can't do refuse cutely."
  model: "$BOT_MODEL"
  command_prefix: "$COMMAND_PREFIX"
  allowed_users:
EOL

for USER in $ALLOWED_USERS; do
  echo "    - $USER" >> $CONFIG_FILE
done

echo "Configuration file created at $CONFIG_FILE."

echo "Setup complete. To activate the virtual environment, run:"
echo "source venv/bin/activate"
