import sys
import time
import yaml
import logging
import argparse
import os
from datetime import datetime

# Use absolute imports within the package to avoid relative import issues when run directly
try:
    from vantaguard.modules.monitor import LogMonitor, ProcessMonitor
    from vantaguard.modules.auditor import SecurityAuditor
except ImportError:
    # Fallback for when running from within the package directory
    from .modules.monitor import LogMonitor, ProcessMonitor
    from .modules.auditor import SecurityAuditor

class VantaGuard:
    def __init__(self, config_path):
        self.load_config(config_path)
        self.setup_logging()
        self.alert_count = 0

    def load_config(self, path):
        if not os.path.exists(path):
            print(f"Error: Configuration file '{path}' not found.")
            sys.exit(1)
        try:
            with open(path, 'r') as f:
                self.config = yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            sys.exit(1)

    def setup_logging(self):
        log_file = self.config.get('alerts', {}).get('log_file', 'vantaguard.log')
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s'
        )

    def alert(self, source, message, severity):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        alert_msg = f"[{timestamp}] [{severity}] [{source}] {message}"
        
        logging.info(alert_msg)
        
        if self.config.get('alerts', {}).get('console_output', True):
            color = ""
            if severity == "CRITICAL": color = "\033[91m"
            elif severity == "HIGH": color = "\033[93m"
            elif severity == "INFO": color = "\033[94m"
            reset = "\033[0m"
            print(f"{color}{alert_msg}{reset}")
        
        self.alert_count += 1

    def run(self, audit_only=False):
        # Clear screen for a clean UI
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # Use raw strings (r"") to avoid SyntaxWarnings with backslashes
        print("\033[92m")
        print(r"  _   _             _        _____                      _ ")
        print(r" | | | |           | |      |  __ \                    | |")
        print(r" | | | | __ _ _ __ | |_ __ _| |  | |_   _  __ _ _ __ __| |")
        print(r" | | | |/ _` | '_ \| __/ _` | |  | | | | |/ _` | '__/ _` |")
        print(r" \ \_/ / (_| | | | | || (_| | |__| | |_| | (_| | | | (_| |")
        print(r"  \___/ \__,_|_| |_|\__\__,_|_____/ \__,_|\__,_|_|  \__,_|")
        print("                                                          ")
        print(" VantaGuard Security Suite - Real-time IDS & Auditor")
        print("\033[0m")
        
        auditor = SecurityAuditor(self.config.get('auditor', {}), self.alert)
        auditor.run_full_audit()
        
        if audit_only:
            print("\n[+] Audit complete. Exiting.")
            return

        log_monitor = LogMonitor(self.config.get('monitoring', {}).get('logs', []), self.alert)
        log_monitor.start()
        
        proc_monitor = ProcessMonitor(self.config.get('monitoring', {}).get('processes', {}).get('suspicious_names', []), self.alert)
        proc_monitor.start()
        
        print("\n[*] VantaGuard is now monitoring your system. Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[!] Stopping VantaGuard...")

def main():
    parser = argparse.ArgumentParser(description="VantaGuard - Linux Security Suite")
    parser.add_argument("--config", default="config.yaml", help="Path to config file")
    parser.add_argument("--audit-only", action="store_true", help="Run only the security auditor")
    parser.add_argument("--version", action="version", version="VantaGuard 1.0.2")
    
    args = parser.parse_args()
    
    vg = VantaGuard(args.config)
    vg.run(audit_only=args.audit_only)

if __name__ == "__main__":
    main()
