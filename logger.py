import logging
from datetime import datetime
import os

def setup_logger():
    # Create logs directory if it doesn't exist
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    # Configure logging
    log_file = os.path.join(logs_dir, f'nova_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    # Create and return logger
    return logging.getLogger("nova")

# Create a singleton logger instance
logger = setup_logger()