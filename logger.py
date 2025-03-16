import os
import logging
from datetime import datetime

# Setup Global Script Logging:
cwd = os.getcwd()
logs_filepath = os.path.join(cwd, "logs")
global_logging_filepath = os.path.join(logs_filepath, "Global_Logging.log")

# Ensure Global Log Directory Exists
os.makedirs(logs_filepath, exist_ok=True)

# Setup Logging
logging.basicConfig(
    filename=global_logging_filepath,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

log = logging.getLogger(__name__)

def log_event(location: str, action: str):
    """
    Logs an event for a specific location and action.

    Parameters:
        location (str): The location (e.g., 'Gym', 'Work', 'Home').
        action (str): The action (e.g., 'Arrival', 'Departure').

    Example Usage:
        log_event('Gym', 'Arrival')
        log_event('Work', 'Departure')
    """
    
    # Define function-specific folder path
    log_dir = os.path.join(logs_filepath, f"{location}_Logs")
    os.makedirs(log_dir, exist_ok=True)  # Create only if function is called

    log_file = os.path.join(log_dir, f"{location}_Tracking.txt")

    # Get the current timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Append the log entry
    try:
        with open(log_file, "a") as file:
            log.info(f"Writing {action} time to {log_dir}")
            file.write(f"{action} at {location}: {current_time}\n")
            log.info(f"Finished writing {action} time to: {log_dir}")

    except Exception as e:
        log.error(f"Error writing {action} to {location} log file: {e}")
