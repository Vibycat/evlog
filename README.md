# evlog - Event Logging for Python

**evlog** is a simple and lightweight Python package for logging and tracking events such as gym or work arrivals and departures. It automatically creates structured log files and keeps a global log for easy tracking.

## 👥 Installation

Install `evlog` using pip:

```bash
pip install evlog
```

##  Usage

### ** Import & Log an Event**
```python
from evlog import log_event

# Log arrival at the gym
log_event("Gym", "Arrival")

# Log departure from work
log_event("Work", "Departure")
```

### **Where Are Logs Stored?**
- **Global log file:** `logs/evlog.log` (tracks all events)
- **Location-specific logs:**
  - `logs/Gym_Logs/Gym_Tracking.txt`
  - `logs/Work_Logs/Work_Tracking.txt`

##  Features
> Automatically creates log directories when needed  
> Tracks multiple locations (Gym, Work, Home, etc.)  
> Saves logs in structured directories  
> Keeps a global log file for easy debugging  

##  Project Setup (For Developers)
To install this package locally for development:

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/evlog.git
cd evlog
pip install .
```

##  Contributing
Contributions are welcome! Feel free to fork the repo and submit a pull request.

##  License
This project is licensed under the **MIT License**.

---

