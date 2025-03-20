import os
import json
import csv
import logging
from datetime import datetime, timedelta

# Default Log Directory
DEFAULT_LOG_DIR = os.path.join(os.getcwd(), "logs")

# Function to set up logging dynamically
def setup_logger(log_dir=DEFAULT_LOG_DIR):
    """
    Sets up a logger for tracking log events.
    """
    os.makedirs(log_dir, exist_ok=True)  # Ensure the directory exists
    log_file = os.path.join(log_dir, "evlog.log")

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    return logging.getLogger(__name__)

# Initialize the global logger
log = setup_logger()


### --- TXT Log Functions --- ###
def log_event_txt(location: str, action: str, log_dir=DEFAULT_LOG_DIR):
    """Logs an event in a TXT file."""
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{location}_Tracking.txt")

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with open(log_file, "a") as file:
            file.write(f"{action} logged to {location}: {current_time}\n")
    except Exception as e:
        log.error(f"Error writing to TXT log: {e}")

def calculate_total_time_txt(location: str, log_dir=DEFAULT_LOG_DIR):
    """Calculates total time from TXT log format and appends it to the same TXT file."""
    log_file = os.path.join(log_dir, f"{location}_Tracking.txt")

    if not os.path.exists(log_file):
        log.warning(f"TXT log file not found: {log_file}")
        return None

    event_times = []

    with open(log_file, "r") as file:
        for line in file:
            parts = line.strip().split(": ", 1)  # Extract action & timestamp
            if len(parts) == 2:
                action, timestamp = parts
                try:
                    dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                    event_times.append(dt)
                except ValueError:
                    log.error(f"Invalid timestamp format in TXT log: {line}")

    # Ensure we have an even number of events (pairs)
    if len(event_times) % 2 != 0:
        log.warning(f"Uneven log entries for {location}, ignoring last entry.")
        event_times = event_times[:-1]  # Ignore the last unpaired entry

    # Calculate total time
    total_time = timedelta()
    for start, end in zip(event_times[0::2], event_times[1::2]):
        total_time += (end - start)

    total_time_str = str(total_time)
    log.info(f"Total time logged at {location}: {total_time_str}")

    # Append total time to the TXT log file
    with open(log_file, "a") as file:
        file.write(f"Total time for {location}: {total_time_str}\n")

    return total_time



### --- CSV Log Functions --- ###
def log_event_csv(location: str, action: str, log_dir=DEFAULT_LOG_DIR):
    """Logs an event in a CSV file."""
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{location}_Tracking.csv")

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with open(log_file, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([location, action, current_time])
    except Exception as e:
        log.error(f"Error writing to CSV log: {e}")

def calculate_total_time_csv(location: str, log_dir=DEFAULT_LOG_DIR):
    """Calculates total time from CSV log format and appends it to the same CSV file."""
    log_file = os.path.join(log_dir, f"{location}_Tracking.csv")

    if not os.path.exists(log_file):
        log.warning(f"CSV log file not found: {log_file}")
        return None

    event_times = []

    with open(log_file, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 3:  # Ensure row contains (location, action, timestamp)
                try:
                    dt = datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S")
                    event_times.append(dt)
                except ValueError:
                    log.error(f"Invalid timestamp format in CSV log: {row}")

    # Ensure we have an even number of events (pairs)
    if len(event_times) % 2 != 0:
        log.warning(f"Uneven log entries for {location}, ignoring last entry.")
        event_times = event_times[:-1]  # Ignore the last unpaired entry

    # Calculate total time
    total_time = timedelta()
    for start, end in zip(event_times[0::2], event_times[1::2]):
        total_time += (end - start)

    total_time_str = str(total_time)
    log.info(f"Total time logged at {location}: {total_time_str}")

    # Append total time to the CSV log file
    with open(log_file, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([location, "Total Time", total_time_str])

    return total_time



### --- JSON Log Functions --- ###
def log_event_json(location: str, action: str, log_dir=DEFAULT_LOG_DIR):
    """Logs an event in a JSON file."""
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{location}_Tracking.json")

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {"location": location, "action": action, "timestamp": current_time}

    try:
        if os.path.exists(log_file):
            with open(log_file, "r") as file:
                data = json.load(file)
        else:
            data = []
    except json.JSONDecodeError:
        log.error(f"Corrupt JSON file detected at {log_file}, resetting...")
        data = []

    data.append(log_entry)

    with open(log_file, "w") as file:
        json.dump(data, file, indent=4)

def calculate_total_time_json(location: str, log_dir=DEFAULT_LOG_DIR):
    """Calculates total time from JSON log format and appends it to the same JSON file."""
    log_file = os.path.join(log_dir, f"{location}_Tracking.json")

    if not os.path.exists(log_file):
        log.warning(f"JSON log file not found: {log_file}")
        return None

    event_times = []

    try:
        # Read JSON log file
        with open(log_file, "r") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        log.error(f"Invalid JSON format in {log_file}")
        return None

    # Extract timestamps from JSON data
    for entry in data:
        try:
            dt = datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S")
            event_times.append(dt)
        except ValueError:
            log.error(f"Invalid timestamp format in JSON log: {entry}")

    # Ensure we have an even number of events (pairs)
    if len(event_times) % 2 != 0:
        log.warning(f"Uneven log entries for {location}, ignoring last entry.")
        event_times = event_times[:-1]  # Ignore the last unpaired entry

    # Calculate total time
    total_time = timedelta()
    for start, end in zip(event_times[0::2], event_times[1::2]):
        total_time += (end - start)

    total_time_str = str(total_time)
    log.info(f"Total time logged at {location}: {total_time_str}")

    # Append total time to the JSON log file
    summary_entry = {
        "location": location,
        "total_time": total_time_str,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    data.append(summary_entry)

    # Write updated log back to JSON file
    with open(log_file, "w") as file:
        json.dump(data, file, indent=4)

    return total_time



### --- Unified Functions for Logging & Time Calculation --- ###
def log_event(location: str, action: str, file_format="txt", log_dir=DEFAULT_LOG_DIR):
    """Logs an event based on the chosen file format."""
    if file_format == "txt":
        log_event_txt(location, action, log_dir)
    elif file_format == "csv":
        log_event_csv(location, action, log_dir)
    elif file_format == "json":
        log_event_json(location, action, log_dir)
    else:
        log.error(f"Unsupported file format: {file_format}")

def calculate_total_time(location: str, file_format="txt", log_dir=DEFAULT_LOG_DIR):
    """Calculates total time based on the chosen file format."""
    if file_format == "txt":
        return calculate_total_time_txt(location, log_dir)
    elif file_format == "csv":
        return calculate_total_time_csv(location, log_dir)
    elif file_format == "json":
        return calculate_total_time_json(location, log_dir)
    else:
        log.error(f"Unsupported file format: {file_format}")
        return None

def calculate_time(event_times, location, log_file):
    """Helper function to calculate total time."""
    if len(event_times) % 2 != 0:
        log.warning(f"Uneven log entries for {location}, ignoring last entry.")
        event_times = event_times[:-1]

    total_time = timedelta()
    for start, end in zip(event_times[0::2], event_times[1::2]):
        total_time += (end - start)

    total_time_str = str(total_time)
    log.info(f"Total time logged at {location}: {total_time_str}")

    return total_time

# Extract action events from log files
def extract_event(location: str, event_type: str, action_filter: str = None, log_dir=DEFAULT_LOG_DIR):
    """
    Extracts the latest event of a specific type from a JSON log file.
    
    Parameters:
        location (str): The location to track (e.g., "gym", "work").
        event_type (str): The event type to extract (e.g., "action", "total_time").
        action_filter (str, optional): The specific action to filter (e.g., "arrival", "departure").
        log_dir (str): The directory where log files are stored (default: "logs").

    Returns:
        dict or None: A dictionary with extracted event data or None if no matching event is found.
    """
    log_file = os.path.join(log_dir, f"{location}_Tracking.json")

    if not os.path.exists(log_file):
        log.warning(f"JSON log file not found: {log_file}")
        return None

    try:
        with open(log_file, "r") as file:
            data = json.load(file)

            if not data:
                log.warning(f"No data found in JSON log: {log_file}")
                return None

            # Filter only entries that contain the requested event type
            filtered_entries = [entry for entry in data if event_type in entry]

            # If action_filter is specified, filter only matching actions
            if action_filter and event_type == "action":
                filtered_entries = [entry for entry in filtered_entries if entry.get("action") == action_filter]

            if not filtered_entries:
                log.warning(f"No valid '{event_type}' entries found in {log_file} with filter: {action_filter}")
                return None

            latest_entry = filtered_entries[-1]  # Get the latest valid event

            return {
                "location": latest_entry["location"],
                event_type: latest_entry[event_type],
                "timestamp": latest_entry["timestamp"]
            }

    except json.JSONDecodeError:
        log.error(f"Error decoding JSON in {log_file}")
        return None

# Erase old log files 
def cleanup_old_logs(days=30, log_dir=DEFAULT_LOG_DIR):
    """
    Deletes log files older than the specified number of days.
    
    Parameters:
        days (int): Number of days to retain logs.
        log_dir (str): Directory where log files are stored.
    """
    threshold_date = datetime.now() - timedelta(days=days)

    for file_name in os.listdir(log_dir):
        file_path = os.path.join(log_dir, file_name)
        if os.path.isfile(file_path):
            file_modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            if file_modified_time < threshold_date:
                try:
                    os.remove(file_path)
                    log.info(f"Deleted old log file: {file_path}")
                except Exception as e:
                    log.error(f"Error deleting log file {file_path}: {e}")

# create a summary report 
def generate_summary_report(log_dir=DEFAULT_LOG_DIR, file_format="json"):
    """
    Generates a summary report of total time spent at different locations.
    
    Parameters:
        log_dir (str): Directory where log files are stored.
        file_format (str): Format of the log files to process (txt, csv, json).
    
    Returns:
        dict: A dictionary with location names and total time spent.
    """
    summary = {}

    for file_name in os.listdir(log_dir):
        if file_name.endswith(f"_Tracking.{file_format}"):
            location = file_name.replace(f"_Tracking.{file_format}", "")
            total_time = calculate_total_time(location, file_format, log_dir)
            if total_time:
                summary[location] = str(total_time)

    log.info(f"Generated summary report: {summary}")
    return summary

# Merge Log files ( example, merge work location and time punches files )
def merge_logs(locations: list, output_format="json", log_dir=DEFAULT_LOG_DIR):
    """
    Merges logs from multiple locations into a single file.

    Parameters:
        locations (list): List of locations whose logs need merging.
        output_format (str): Output file format (txt, csv, json).
        log_dir (str): Directory where log files are stored.
    
    Returns:
        str: Path to the merged log file.
    """
    merged_data = []
    output_file = os.path.join(log_dir, f"Merged_Logs.{output_format}")

    for location in locations:
        log_file = os.path.join(log_dir, f"{location}_Tracking.{output_format}")

        if not os.path.exists(log_file):
            log.warning(f"Log file not found: {log_file}")
            continue

        if output_format == "json":
            with open(log_file, "r") as file:
                data = json.load(file)
                merged_data.extend(data)

    if output_format == "json":
        with open(output_file, "w") as file:
            json.dump(merged_data, file, indent=4)

    log.info(f"Merged logs saved to: {output_file}")
    return output_file
