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
            log.info(f"Logging {action} at {location} to {log_file}")
            file.write(f"{action} at {location}: {current_time}\n")
            log.info(f"Finished logging {action} at {location}")
    except Exception as e:
        log.error(f"Error logging {action} at {location}: {e}")


# Function to calculate and append total time spent at a location
def calculate_total_time(location: str, log_dir=None):
    """
    Calculates the total time spent at a given location based on timestamps in log files,
    and appends the total duration to the same log file.

    Parameters:
        location (str): The location name (e.g., "Gym", "Work").
        log_dir (str, optional): Custom log directory. Defaults to the script's log directory.

    Returns:
        total_time (timedelta): Total duration spent at the location.
    """
    
    # Determine log directory
    log_dir = log_dir if log_dir else os.path.join(os.getcwd(), "logs")
    log_file = os.path.join(log_dir, f"{location}_Tracking.txt")

    if not os.path.exists(log_file):
        logging.warning(f"Log file not found: {log_file}")
        return timedelta()  # Return zero time if no log file exists

    arrival_times = []
    departure_times = []

    # Read log file and extract timestamps
    with open(log_file, "r") as file:
        for line in file:
            parts = line.strip().split(": ", 1)  # Example: "Arrival at Gym: 2025-03-16 10:00:00"
            if len(parts) == 2:
                action, timestamp = parts
                try:
                    dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                    if "Arrival" in action:
                        arrival_times.append(dt)
                    elif "Departure" in action:
                        departure_times.append(dt)
                except ValueError:
                    logging.error(f"Invalid timestamp format in log: {line}")

    # Ensure we have equal pairs of arrivals & departures
    total_time = timedelta()
    for arrival, departure in zip(arrival_times, departure_times):
        total_time += (departure - arrival)

    # Log total time spent
    total_time_str = str(total_time)
    logging.info(f"Total time spent at {location}: {total_time_str}")

    # Append total time to the log file
    with open(log_file, "a") as file:
        file.write(f"Total time spent at {location}: {total_time_str}\n")

    return total_time
