import time
import os
import threading
import re

class LogMonitor:
    def __init__(self, log_configs, alert_callback):
        self.log_configs = log_configs
        self.alert_callback = alert_callback
        self.threads = []

    def tail_file(self, path, patterns):
        try:
            if not os.path.exists(path):
                self.alert_callback("SYSTEM", f"Log file not found: {path}", "WARNING")
                return

            with open(path, 'r') as f:
                f.seek(0, os.SEEK_END)
                while True:
                    line = f.readline()
                    if not line:
                        time.sleep(0.1)
                        continue
                    
                    for pattern in patterns:
                        if re.search(pattern, line, re.IGNORECASE):
                            self.alert_callback("MONITOR", f"Pattern '{pattern}' detected in {path}: {line.strip()}", "CRITICAL")
        except Exception as e:
            self.alert_callback("SYSTEM", f"Error monitoring {path}: {str(e)}", "ERROR")

    def start(self):
        for config in self.log_configs:
            t = threading.Thread(target=self.tail_file, args=(config['path'], config['patterns']))
            t.daemon = True
            t.start()
            self.threads.append(t)

class ProcessMonitor:
    def __init__(self, suspicious_names, alert_callback):
        self.suspicious_names = suspicious_names
        self.alert_callback = alert_callback

    def check_processes(self):
        try:
            # Using a more robust way to list processes
            with os.popen('ps -eo comm') as stream:
                processes = stream.read().split('\n')
                for proc in processes:
                    name = proc.strip()
                    if name in self.suspicious_names:
                        self.alert_callback("PROCESS", f"Suspicious process detected: {name}", "HIGH")
        except Exception as e:
            self.alert_callback("SYSTEM", f"Error checking processes: {str(e)}", "ERROR")

    def start(self, interval=10):
        def run():
            while True:
                self.check_processes()
                time.sleep(interval)
        
        t = threading.Thread(target=run)
        t.daemon = True
        t.start()
