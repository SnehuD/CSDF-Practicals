import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Setup logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])

# Directory to watch and log file path
log_directory = "C:/Users/rayra/Desktop/God_Codes/PY_programs/CyberSec/LOG"
log_file = os.path.join(log_directory, "example.log")
alert_log_file = os.path.join(log_directory, "alert.log")

# Define event correlation rules
def write_alert(message):
    with open(alert_log_file, 'a') as f:
        f.write(message + "\n")

def correlate_events(log_lines):
    error_count = 0
    failed_login_count = 0
    for line in log_lines:
        if "ERROR" in line:
            error_count += 1
            alert_message = f"Error detected: {line.strip()}"
            logging.info(alert_message)
            write_alert(alert_message)
        if "Failed login attempt" in line:
            failed_login_count += 1
            alert_message = f"Failed login attempt detected: {line.strip()}"
            logging.info(alert_message)
            write_alert(alert_message)

    if error_count > 5:
        alert_message = "Multiple errors detected!"
        logging.warning(alert_message)
        write_alert(alert_message)

    if failed_login_count > 3:
        alert_message = "Multiple failed login attempts detected!"
        logging.warning(alert_message)
        write_alert(alert_message)

# Log handler class
class LogHandler(FileSystemEventHandler):
    def __init__(self, file_path):
        self.file_path = file_path

    def on_modified(self, event):
        if event.src_path == self.file_path:
            while True:
                try:
                    with open(self.file_path, 'r') as file:
                        lines = file.readlines()
                        correlate_events(lines)
                    break
                except PermissionError:
                    logging.warning(f"Permission denied when trying to read {self.file_path}. Retrying...")
                    time.sleep(1)
                except Exception as e:
                    logging.error(f"An error occurred: {e}")
                    break

def start_log_monitoring(log_file_path):
    event_handler = LogHandler(log_file_path)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(log_file_path), recursive=False)
    observer.start()
    logging.info(f"Started monitoring log file: {log_file_path}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info("Stopping log monitoring...")
    observer.join()

def generate_test_logs(log_file):
    test_entries = [
        "2024-07-02 15:00:00 INFO Starting application\n",
        "2024-07-02 15:01:00 ERROR An unexpected error occurred\n",
        "2024-07-02 15:02:00 INFO Process completed\n",
        "2024-07-02 15:03:00 WARNING Failed login attempt\n"
    ]
    
    with open(log_file, 'a') as f:
        for entry in test_entries:
            f.write(entry)
            time.sleep(1)  # Sleep to simulate real-time log generation

if __name__ == "__main__":
    # Start log monitoring in a separate thread
    import threading
    monitor_thread = threading.Thread(target=start_log_monitoring, args=(log_file,))
    monitor_thread.start()
    
    # Generate test logs
    generate_test_logs(log_file)
