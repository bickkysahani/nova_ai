# Nova AI

Nova AI is an advanced voice-controlled AI assistant that currently focuses on media control but is designed to evolve into a comprehensive personal AI assistant. It uses state-of-the-art wake word detection and natural language processing to understand and execute complex commands with high accuracy.

## Current Features

- **Wake Word Detection**: Activates the AI when you say "Hey Nova"
- **Voice Command Processing**: Converts speech to text and parses commands
- **Media Controls**:
  - Spotify integration for music playback
  - YouTube integration for video playback
  - Play, pause, resume, next, and previous track controls
- **Volume Controls**:
  - Volume up/down
  - Set specific volume level

## Comparison with Siri

| Feature | Siri | Nova AI |
|---------|------|---------|
| **Music Control** | Basic play/pause/next | Advanced control with exact song matching |
| **YouTube Control** | Limited to basic playback | Full control including search and play |
| **Volume Control** | Basic up/down | Precise percentage control |
| **Command Understanding** | Limited to predefined phrases | Natural language understanding |
| **Response Time** | Variable | Optimized for quick response |
| **Customization** | Limited | Highly customizable |

## Prerequisites

- Python 3.8 or higher
- macOS (required for AppleScript integration)
- Spotify Desktop app installed
- Google Chrome installed (for YouTube controls)
- OpenAI API key
- Picovoice Access Key (for wake word detection)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/nova-ai.git
cd nova-ai
```

2. Install uv (Python package installer and resolver):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. Create and activate a virtual environment using uv:
```bash
uv venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```

4. Install dependencies:
```bash
uv pip install -r requirements.txt
```

5. Create a `.env` file in the project root and add your API keys:
```
OPENAI_API_KEY=your_openai_api_key_here
PICOVOICE_ACCESS_KEY=your_picovoice_access_key_here
```

6. Download the wake word model:
   - Sign up for a free account at [Picovoice Console](https://console.picovoice.ai/)
   - Navigate to the Wake Word section
   - Create a new wake word model with the phrase "Hey Nova"
   - Download the `.ppn` file
   - Create an `assets` directory in the project root if it doesn't exist:
     ```bash
     mkdir -p assets
     ```
   - Move the downloaded `.ppn` file to the `assets` directory and rename it to `hey-nova.ppn`

To get your Picovoice Access Key:
1. Sign up for a free account at [Picovoice Console](https://console.picovoice.ai/)
2. Navigate to the Access Keys section
3. Create a new access key
4. Copy the key and paste it in your `.env` file

Note: The free tier of Picovoice includes:
- 100 wake word activations per month
- Support for custom wake words
- Real-time wake word detection

## Project Structure

```
nova-ai/
├── assets/                # Resource files
│   └── hey-nova.ppn      # Wake word model file
├── .env                  # Environment variables
├── .gitignore           # Git ignore file
├── README.md            # This file
├── requirements.txt     # Project dependencies
├── main.py             # Main application entry point
├── wake.py            # Wake word detection module
├── speech.py          # Speech recognition module
├── llm_parser.py      # Command parsing using OpenAI
├── command_parser.py  # Command parsing utilities
└── executor.py        # Media control execution module
```

Note: The `__pycache__` directory and `.venv` directory are not shown as they are automatically generated and ignored by git.

## Usage

1. Start Nova AI:
```bash
python main.py
```

2. Wait for the wake word "Hey Nova"

3. After the wake word is detected, speak your command. Examples:
   - "Play Hotel California on Spotify"
   - "Pause the music"
   - "Next song"
   - "Volume up"
   - "Set volume to 75%"

## Available Commands

### Spotify Controls
- "Play [song name] on Spotify"
- "Pause the music"
- "Resume the music"
- "Next song"
- "Previous song"

### YouTube Controls
- "Play [video name] on YouTube"
- "Pause the video"
- "Resume the video"
- "Next video"
- "Previous video"

### Volume Controls
- "Volume up"
- "Volume down"
- "Set volume to [0-100]%"

## Development

### Adding New Features

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### Running Tests

```bash
python -m pytest tests/
```

## Troubleshooting

1. **Wake Word Not Detecting**:
   - Ensure your microphone is properly connected and has permissions
   - Check if the wake word model is properly loaded

2. **Media Controls Not Working**:
   - Verify that Spotify/YouTube is installed and running
   - Check if the applications have necessary permissions

3. **Volume Controls Not Working**:
   - Ensure you have the necessary system permissions
   - Check if the AppleScript commands are working

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for providing the language model
- The open-source community for various libraries used in this project