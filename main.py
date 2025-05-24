from wake import detect_wake_word
from speech import listen_to_command
from llm_parser import parse_command
from executor import (
    play_on_spotify, play_on_youtube,
    pause_spotify, resume_spotify, next_spotify, previous_spotify,
    pause_youtube, resume_youtube, next_youtube, previous_youtube,
    volume_up, volume_down, set_volume
)
from logger import logger
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def execute_command(command):
    if not command:
        logger.error("No command received")
        return False

    action = command.action
    platform = command.platform

    try:
        if action == "play":
            song = command.song
            if not song:
                logger.error("No song specified for play action")
                return False

            if platform == "spotify":
                logger.info(f"Playing on Spotify: {song}")
                play_on_spotify(song)
            elif platform == "youtube":
                logger.info(f"Playing on YouTube: {song}")
                play_on_youtube(song)

        elif action == "pause":
            if platform == "spotify":
                pause_spotify()
            elif platform == "youtube":
                pause_youtube()

        elif action == "resume":
            if platform == "spotify":
                resume_spotify()
            elif platform == "youtube":
                resume_youtube()

        elif action == "next":
            if platform == "spotify":
                next_spotify()
            elif platform == "youtube":
                next_youtube()

        elif action == "previous":
            if platform == "spotify":
                previous_spotify()
            elif platform == "youtube":
                previous_youtube()

        elif action == "volume_up":
            volume_up()

        elif action == "volume_down":
            volume_down()

        elif action == "set_volume":
            if command.volume_level is not None:
                logger.info(f"Setting volume to {command.volume_level}%")
                set_volume(command.volume_level)
            else:
                logger.error("No volume level specified for set_volume action")
                return False

        return True

    except Exception as e:
        logger.error(f"Error executing command: {str(e)}", exc_info=True)
        return False

def main():
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        logger.error("OPENAI_API_KEY environment variable not set!")
        print("Error: OPENAI_API_KEY environment variable not set!")
        return

    logger.info("Starting Nova Assistant")
    while True:
        try:
            logger.info("Waiting for wake word...")
            detect_wake_word()
            logger.info("Wake word detected!")

            logger.info("Listening for command...")
            command_text = listen_to_command()
            logger.info(f"Received command: {command_text}")

            if not command_text:
                logger.warning("No command received")
                print("Sorry, I didn't understand that command.")
                continue

            logger.info("Parsing command...")
            command = parse_command(command_text)

            if command:
                logger.info(f"Executing command: {command}")
                if execute_command(command):
                    logger.info("Command executed successfully")
                else:
                    logger.error("Failed to execute command")
                    print("Sorry, I couldn't execute that command.")
            else:
                logger.warning(f"Could not parse command: {command_text}")
                print("Sorry, I didn't understand that command.")

        except Exception as e:
            logger.error(f"Error in main loop: {str(e)}", exc_info=True)
            print("An error occurred. Please try again.")

if __name__ == "__main__":
    main()
