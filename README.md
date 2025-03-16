# evlog - Event Logging for Python

**evlog** is a simple and lightweight Python package for logging and tracking events such as gym or work arrivals and departures. It automatically creates structured log files and keeps a global log for easy tracking.

## Installation

Install `evlog` using pip:

```bash
pip install evlog
```

## Usage

### **Import & Log an Event**
```python
from evlog import log_event

# Log arrival at the gym
log_event("Gym", "Arrival")

# Log departure from work
log_event("Work", "Departure")
```

### **Calculate & Append Total Time Spent**
You can also calculate the total time spent at a location (e.g., Gym, Work) and append it to the log file:
```python
from evlog import calculate_total_time

total_time = calculate_total_time("Gym")
print(f"Total time spent at Gym: {total_time}")
```
📌 This will append the total time spent to `logs/Gym_Tracking.txt`:
```
Arrival at Gym: 2025-03-16 10:00:00
Departure at Gym: 2025-03-16 12:30:00
Total time spent at Gym: 2:30:00
```

### **Where Are Logs Stored?**
By default, logs are stored in the `logs/` directory inside the current working directory (`cwd`).

- **Global log file:** `logs/evlog.log` (tracks all events)
- **Location-specific logs:**
  - `logs/Gym_Logs/Gym_Tracking.txt`
  - `logs/Work_Logs/Work_Tracking.txt`

If a different directory is needed, you can specify a custom log directory:
```python
log_event("Gym", "Workout Started", log_dir="/custom/logs")
calculate_total_time("Gym", log_dir="/custom/logs")
```

## Features
> Dynamically sets log directory based on the script's location  
> Allows custom log directories for different environments  
> Tracks multiple locations (Gym, Work, Home, etc.)  
> Saves logs in structured directories  
> Keeps a global log file for easy debugging  
> Calculates and appends total time spent at locations  

## Project Setup (For Developers)
To install this package locally for development:

```bash
git clone https://github.com/Vibycat/evlog.git
cd evlog
pip install .
```

## Contributing
Contributions are welcome! Feel free to fork the repo and submit a pull request.

## License
This project is licensed under the **MIT License**.

---

