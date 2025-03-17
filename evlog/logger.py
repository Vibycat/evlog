import os
import logging
from datetime import datetime , timedelta

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
            log.info(f"Logging {action} to {location} at {log_file}")
            file.write(f"{action} logged to {location}: {current_time}\n")
            log.info(f"Sucessfully logged {action} to {location} at {log_file}")
    except Exception as e:
        log.error(f"Error logging {action} at {location}: {e}")


# Function to calculate and append total time spent at a location
def calculate_total_time(location: str, log_dir=None):
    """
    Calculates and appends the total time between matching log events at a location.

    Parameters:
        location (str): The location name (e.g., "Gym", "Work", "Door_Logs").
        log_dir (str, optional): Custom log directory. Defaults to the script's log directory.

    Returns:
        total_time (timedelta): Total duration for the event type.
    """

    # Determine log directory
    log_dir = log_dir if log_dir else os.path.join(os.getcwd(), "logs")
    log_file = os.path.join(log_dir, f"{location}_Tracking.txt")

    if not os.path.exists(log_file):
        logging.warning(f"Log file not found: {log_file}")
        return None  # Return nothing if error

    event_times = []
    
    # Read log file and extract timestamps
    with open(log_file, "r") as file:
        for line in file:
            parts = line.strip().split(": ", 1)  # Extract action & timestamp
            if len(parts) == 2:
                action, timestamp = parts
                try:
                    dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                    event_times.append(dt)
                except ValueError:
                    logging.error(f"Invalid timestamp format in log: {line}")

    # Ensure we have an even number of events (pairs)
    if len(event_times) % 2 != 0:
        logging.warning(f"Uneven log entries for {location}, ignoring last entry.")
        event_times = event_times[:-1]  # Ignore the last unpaired entry

    # Calculate total time
    total_time = timedelta()
    for start, end in zip(event_times[0::2], event_times[1::2]):  # Pairing events
        total_time += (end - start)

    # Log and append total time
    total_time_str = str(total_time)
    logging.info(f"Total time logged at {location}: {total_time_str}")

    with open(log_file, "a") as file:
        file.write(f"Total time spent at {location}: {total_time_str}\n")

    return total_time
