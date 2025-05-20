def parse_command(text):
    if not text:
        return None

    text = text.lower().strip()

    # Media control commands
    media_commands = {
        "pause": ["pause", "stop"],
        "resume": ["resume", "play", "continue"],
        "next": ["next", "skip", "next song", "next track"],
        "previous": ["previous", "back", "last song", "last track"]
    }

    # Platform keywords
    platforms = {
        "spotify": ["spotify", "on spotify", "in spotify"],
        "youtube": ["youtube", "on youtube", "in youtube", "yt"]
    }

    # Volume commands
    volume_commands = {
        "up": ["volume up", "increase volume", "louder", "turn up"],
        "down": ["volume down", "decrease volume", "quieter", "turn down"]
    }

    # Check for volume commands first
    for action, keywords in volume_commands.items():
        if any(keyword in text for keyword in keywords):
            return {"action": f"volume_{action}"}

    # Check for media control commands
    for action, keywords in media_commands.items():
        if any(keyword in text for keyword in keywords):
            # Determine platform
            platform = None
            for p, platform_keywords in platforms.items():
                if any(keyword in text for keyword in platform_keywords):
                    platform = p
                    break

            # If no platform specified, default to Spotify
            if not platform:
                platform = "spotify"

            return {
                "action": action,
                "platform": platform
            }

    # Check for play commands
    if "play" in text:
        # Determine platform
        platform = None
        for p, keywords in platforms.items():
            if any(keyword in text for keyword in keywords):
                platform = p
                break

        # If no platform specified, default to Spotify
        if not platform:
            platform = "spotify"

        return {
            "action": "play",
            "platform": platform,
            "song": extract_song(text, platform)
        }

    return None

def extract_song(text, platform):
    # Remove play commands
    play_commands = ["play", "start", "begin", "put on"]
    for cmd in play_commands:
        text = text.replace(cmd, "")

    # Remove platform commands
    platform_commands = {
        "spotify": ["spotify", "on spotify", "in spotify"],
        "youtube": ["youtube", "on youtube", "in youtube", "yt"]
    }
    for cmd in platform_commands[platform]:
        text = text.replace(cmd, "")

    # Clean up the text
    return text.strip()
