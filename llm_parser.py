from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Optional, Literal
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Get API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set. Please set it in your .env file or environment.")

class Command(BaseModel):
    """Schema for parsed voice commands"""
    action: Literal[
        "play", "pause", "resume", "next", "previous",
        "volume_up", "volume_down", "set_volume"
    ] = Field(description="The action to perform")

    platform: Optional[Literal["spotify", "youtube"]] = Field(
        default=None,
        description="The platform to perform the action on (spotify or youtube)"
    )

    song: Optional[str] = Field(
        default=None,
        description="The song name or query to play (only for play action)"
    )

    volume_level: Optional[int] = Field(
        default=None,
        description="The volume level to set (0-100, only for set_volume action)"
    )

# Create the parser at module level
parser = PydanticOutputParser(pydantic_object=Command)

def create_llm_parser():
    """Create and configure the LLM parser"""
    try:
        # Initialize the LLM
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            api_key=OPENAI_API_KEY
        )

        # Create the prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a voice command parser for a media control assistant.
Your task is to parse natural language commands into structured actions.
Available actions are: play, pause, resume, next, previous, volume_up, volume_down, set_volume.
Available platforms are: spotify, youtube.

Examples:
- "play hotel california on spotify" -> {{"action": "play", "platform": "spotify", "song": "hotel california"}}
- "pause the music" -> {{"action": "pause", "platform": "spotify"}}
- "next song" -> {{"action": "next", "platform": "spotify"}}
- "volume up" -> {{"action": "volume_up"}}
- "set volume to 75%" -> {{"action": "set_volume", "volume_level": 75}}

If no platform is specified, default to spotify.
For volume commands, don't include a platform.
Only include the song field for play actions.
For set_volume action, include the volume_level field (0-100).

{format_instructions}"""),
            ("user", "{input}")
        ])

        # Create the chain
        chain = prompt | llm | parser

        return chain

    except Exception as e:
        logger.error(f"Error creating LLM parser: {str(e)}", exc_info=True)
        raise

def parse_command(text: str) -> Optional[Command]:
    """Parse a voice command using the LLM"""
    if not text:
        return None

    try:
        logger.info(f"Parsing command: {text}")

        # Create the parser
        chain = create_llm_parser()

        # Parse the command
        result = chain.invoke({"input": text, "format_instructions": parser.get_format_instructions()})

        logger.info(f"Parsed command: {result}")
        return result

    except Exception as e:
        logger.error(f"Error parsing command: {str(e)}", exc_info=True)
        return None