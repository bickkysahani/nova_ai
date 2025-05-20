import subprocess
import webbrowser
from youtubesearchpython import VideosSearch
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'executor_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def run_applescript(script):
    logger.info("Executing AppleScript")
    logger.debug(f"AppleScript content: {script}")
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            logger.info("AppleScript executed successfully")
            if result.stdout:
                logger.debug(f"AppleScript output: {result.stdout}")
        else:
            logger.error(f"AppleScript failed with error: {result.stderr}")
        return result
    except Exception as e:
        logger.error(f"Error executing AppleScript: {str(e)}", exc_info=True)
        raise

# Spotify Controls
def play_on_spotify(song_name):
    logger.info(f"Attempting to play '{song_name}' on Spotify")
    try:
        song_uri = f"spotify:search:{song_name}"
        logger.debug(f"Generated Spotify URI: {song_uri}")

        script = f'''
        tell application "Spotify"
            activate
            play track "{song_uri}"
        end tell
        '''
        logger.info(f"Playing '{song_name}' on Spotify app...")
        result = run_applescript(script)

        if result.returncode == 0:
            logger.info(f"Successfully initiated playback of '{song_name}' on Spotify")
        else:
            logger.error(f"Failed to play '{song_name}' on Spotify")

    except Exception as e:
        logger.error(f"Error playing on Spotify: {str(e)}", exc_info=True)
        raise

def pause_spotify():
    logger.info("Attempting to pause Spotify")
    try:
        script = '''
        tell application "Spotify"
            pause
        end tell
        '''
        result = run_applescript(script)
        if result.returncode == 0:
            logger.info("Successfully paused Spotify")
        else:
            logger.error("Failed to pause Spotify")
    except Exception as e:
        logger.error(f"Error pausing Spotify: {str(e)}", exc_info=True)
        raise

def resume_spotify():
    logger.info("Attempting to resume Spotify")
    try:
        script = '''
        tell application "Spotify"
            play
        end tell
        '''
        result = run_applescript(script)
        if result.returncode == 0:
            logger.info("Successfully resumed Spotify")
        else:
            logger.error("Failed to resume Spotify")
    except Exception as e:
        logger.error(f"Error resuming Spotify: {str(e)}", exc_info=True)
        raise

def next_spotify():
    logger.info("Attempting to play next track on Spotify")
    try:
        script = '''
        tell application "Spotify"
            next track
        end tell
        '''
        result = run_applescript(script)
        if result.returncode == 0:
            logger.info("Successfully played next track on Spotify")
        else:
            logger.error("Failed to play next track on Spotify")
    except Exception as e:
        logger.error(f"Error playing next track on Spotify: {str(e)}", exc_info=True)
        raise

def previous_spotify():
    logger.info("Attempting to play previous track on Spotify")
    try:
        script = '''
        tell application "Spotify"
            previous track
        end tell
        '''
        result = run_applescript(script)
        if result.returncode == 0:
            logger.info("Successfully played previous track on Spotify")
        else:
            logger.error("Failed to play previous track on Spotify")
    except Exception as e:
        logger.error(f"Error playing previous track on Spotify: {str(e)}", exc_info=True)
        raise

# YouTube Controls
def play_on_youtube(song_name):
    logger.info(f"Attempting to play '{song_name}' on YouTube")
    try:
        logger.debug(f"Searching YouTube for: {song_name}")
        results = VideosSearch(song_name, limit=1).result()

        if not results['result']:
            logger.error(f"No results found on YouTube for: {song_name}")
            raise Exception("No YouTube results found")

        link = results['result'][0]['link']
        logger.debug(f"Found YouTube link: {link}")

        logger.info(f"Playing '{song_name}' on YouTube...")
        webbrowser.open(link)
        logger.info(f"Successfully opened YouTube link for '{song_name}'")

    except Exception as e:
        logger.error(f"Error playing on YouTube: {str(e)}", exc_info=True)
        raise

def pause_youtube():
    logger.info("Attempting to pause YouTube")
    try:
        script = '''
        tell application "Google Chrome"
            execute front window's active tab javascript "document.querySelector('video').pause()"
        end tell
        '''
        result = run_applescript(script)
        if result.returncode == 0:
            logger.info("Successfully paused YouTube")
        else:
            logger.error("Failed to pause YouTube")
    except Exception as e:
        logger.error(f"Error pausing YouTube: {str(e)}", exc_info=True)
        raise

def resume_youtube():
    logger.info("Attempting to resume YouTube")
    try:
        script = '''
        tell application "Google Chrome"
            execute front window's active tab javascript "document.querySelector('video').play()"
        end tell
        '''
        result = run_applescript(script)
        if result.returncode == 0:
            logger.info("Successfully resumed YouTube")
        else:
            logger.error("Failed to resume YouTube")
    except Exception as e:
        logger.error(f"Error resuming YouTube: {str(e)}", exc_info=True)
        raise

def next_youtube():
    logger.info("Attempting to play next video on YouTube")
    try:
        script = '''
        tell application "Google Chrome"
            execute front window's active tab javascript "document.querySelector('.ytp-next-button').click()"
        end tell
        '''
        result = run_applescript(script)
        if result.returncode == 0:
            logger.info("Successfully played next video on YouTube")
        else:
            logger.error("Failed to play next video on YouTube")
    except Exception as e:
        logger.error(f"Error playing next video on YouTube: {str(e)}", exc_info=True)
        raise

def previous_youtube():
    logger.info("Attempting to play previous video on YouTube")
    try:
        script = '''
        tell application "Google Chrome"
            execute front window's active tab javascript "document.querySelector('.ytp-prev-button').click()"
        end tell
        '''
        result = run_applescript(script)
        if result.returncode == 0:
            logger.info("Successfully played previous video on YouTube")
        else:
            logger.error("Failed to play previous video on YouTube")
    except Exception as e:
        logger.error(f"Error playing previous video on YouTube: {str(e)}", exc_info=True)
        raise

# System Volume Controls
def get_current_volume():
    logger.info("Getting current system volume")
    try:
        script = '''
        output volume of (get volume settings)
        '''
        result = run_applescript(script)
        if result.returncode == 0:
            volume = int(result.stdout.strip())
            logger.info(f"Current volume: {volume}")
            return volume
        else:
            logger.error("Failed to get current volume")
            return None
    except Exception as e:
        logger.error(f"Error getting current volume: {str(e)}", exc_info=True)
        return None

def set_volume(level):
    """Set system volume to a specific percentage (0-100)"""
    logger.info(f"Setting system volume to {level}%")
    try:
        # Ensure volume is between 0 and 100
        level = max(0, min(100, int(level)))

        script = f'''
        set volume output volume {level}
        '''
        result = run_applescript(script)
        if result.returncode == 0:
            logger.info(f"Successfully set volume to {level}%")
        else:
            logger.error(f"Failed to set volume to {level}%")
    except Exception as e:
        logger.error(f"Error setting volume: {str(e)}", exc_info=True)
        raise

def volume_up():
    """Increase volume by 10%"""
    current_volume = get_current_volume()
    if current_volume is not None:
        new_volume = min(current_volume + 10, 100)
        set_volume(new_volume)

def volume_down():
    """Decrease volume by 10%"""
    current_volume = get_current_volume()
    if current_volume is not None:
        new_volume = max(current_volume - 10, 0)
        set_volume(new_volume)

def set_volume_to_percentage(percentage):
    """Set volume to a specific percentage"""
    try:
        # Remove any non-numeric characters except decimal point
        percentage = ''.join(c for c in str(percentage) if c.isdigit() or c == '.')
        percentage = float(percentage)
        set_volume(percentage)
    except ValueError:
        logger.error(f"Invalid volume percentage: {percentage}")
        raise ValueError("Invalid volume percentage")

def lower_volume_to_percentage(percentage):
    """Lower volume to a specific percentage"""
    current_volume = get_current_volume()
    if current_volume is not None:
        try:
            # Remove any non-numeric characters except decimal point
            percentage = ''.join(c for c in str(percentage) if c.isdigit() or c == '.')
            percentage = float(percentage)
            if percentage < current_volume:
                set_volume(percentage)
            else:
                logger.info(f"Current volume ({current_volume}%) is already lower than requested ({percentage}%)")
        except ValueError:
            logger.error(f"Invalid volume percentage: {percentage}")
            raise ValueError("Invalid volume percentage")

def execute_command(command):
    """Execute a parsed command"""
    try:
        logger.info(f"Executing command: {command}")

        if command.action == "play":
            if command.platform == "spotify":
                play_on_spotify(command.song)
            elif command.platform == "youtube":
                play_on_youtube(command.song)
        elif command.action == "pause":
            if command.platform == "spotify":
                pause_spotify()
            elif command.platform == "youtube":
                pause_youtube()
        elif command.action == "resume":
            if command.platform == "spotify":
                resume_spotify()
            elif command.platform == "youtube":
                resume_youtube()
        elif command.action == "next":
            if command.platform == "spotify":
                next_spotify()
            elif command.platform == "youtube":
                next_youtube()
        elif command.action == "previous":
            if command.platform == "spotify":
                previous_spotify()
            elif command.platform == "youtube":
                previous_youtube()
        elif command.action == "volume_up":
            volume_up()
        elif command.action == "volume_down":
            volume_down()
        elif command.action == "set_volume":
            if command.volume_level is not None:
                set_volume(command.volume_level)
            else:
                logger.error("Volume level not specified for set_volume action")

        logger.info("Command executed successfully")

    except Exception as e:
        logger.error(f"Error executing command: {str(e)}", exc_info=True)
        raise
