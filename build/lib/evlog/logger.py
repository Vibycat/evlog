import os
import logging
from datetime import datetime

# Default Log Directory
DEFAULT_LOG_DIR = os.path.join(os.getcwd(),"logs")

# Function to set up logging dynamically
def setup_logger(log_dir=DEFAULT_LOG_DIR):
    """
    Allows the user to specify a custom log directory.
    Defaults to /config/logs if not specified.

    :param log_dir: Directory where logs will be stored.
    :return: Configured logger instance.
    """
    os.makedirs(log_dir, exist_ok=True)  # Ensure the directory exists
    log_file = os.path.join(log_dir, "evlog.log")

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    return logging.getLogger(__name__)

# Initialize the global logger (users can override this)
log = setup_logger()


def log_event(location: str, action: str, log_dir=None):
    """
    Logs an event for a specific location and action.

    Parameters:
        location (str): The location (e.g., 'Gym', 'Work', 'Home').
        action (str): The action (e.g., 'Arrival', 'Departure').
        log_dir (str, optional): Custom log directory for event tracking.
                                 Defaults to global log directory.

    Example Usage:
        log_event('Gym', 'Arrival')
        log_event('Work', 'Departure')
    """
    
    # If the user provides a log directory, override the default
    event_log_dir = log_dir if log_dir else DEFAULT_LOG_DIR
    os.makedirs(event_log_dir, exist_ok=True)  

    log_file = os.path.join(event_log_dir, f"{location}_Tracking.txt")

    # Get the current timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Append the log entry
    try:
        with open(log_file, "a") as file:
            log.info(f"Logging {action} at {location} to {log_file}")
            file.write(f"{action} at {location}: {current_time}\n")
            log.info(f"Finished logging {action} at {location}")
    except Exception as e:
        log.error(f"Error logging {action} at {location}: {e}")
