#!/bin/bash

# Nova AI Setup Script
# This script automates the installation and setup process for Nova AI

echo "Starting Nova AI setup..."

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Add Homebrew to PATH if needed
    if [[ $(uname -m) == "arm64" ]]; then
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
        eval "$(/opt/homebrew/bin/brew shellenv)"
    else
        echo 'eval "$(/usr/local/bin/brew shellenv)"' >> ~/.zprofile
        eval "$(/usr/local/bin/brew shellenv)"
    fi
else
    echo "Homebrew already installed."
fi

# Install OS-level dependencies
echo "Installing ffmpeg and portaudio..."
brew install ffmpeg portaudio

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "Installing uv package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # Source the shell configuration to make uv available
    source ~/.zshrc
else
    echo "uv already installed."
fi

# Create and activate virtual environment
echo "Setting up Python virtual environment..."
uv venv
source .venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
uv pip install -r requirements.txt

# Create assets directory if it doesn't exist
echo "Creating assets directory..."
mkdir -p assets

# Create template .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating template .env file..."
    cat > .env << EOL
OPENAI_API_KEY=your_openai_api_key_here
PICOVOICE_ACCESS_KEY=your_picovoice_access_key_here
EOL
    echo "Please update the .env file with your actual API keys."
else
    echo ".env file already exists."
fi

echo ""
echo "Nova AI setup completed!"
echo ""
echo "Next steps:"
echo "1. Update the .env file with your API keys"
echo "2. Download the 'Hey Nova' wake word model from Picovoice Console"
echo "3. Place the wake word model in the 'assets' directory as 'hey-nova.ppn'"
echo "4. Run Nova AI with: python main.py"
echo ""
echo "Enjoy using Nova AI!" 