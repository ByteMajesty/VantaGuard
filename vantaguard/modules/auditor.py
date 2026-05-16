import os
import stat

class SecurityAuditor:
    def __init__(self, config, alert_callback):
        self.config = config
        self.alert_callback = alert_callback

    def audit_file_permissions(self):
        self.alert_callback("AUDIT", "Starting file permissions audit...", "INFO")
        for file_path in self.config.get('sensitive_files', []):
            if os.path.exists(file_path):
                st = os.stat(file_path)
                # Check if file is world-readable or world-writable
                if bool(st.st_mode & stat.S_IROTH) or bool(st.st_mode & stat.S_IWOTH):
                    self.alert_callback("AUDIT", f"Insecure permissions on {file_path}: {oct(st.st_mode)}", "HIGH")
            else:
                self.alert_callback("AUDIT", f"Sensitive file missing: {file_path}", "WARNING")

    def check_ssh_config(self):
        if not self.config.get('check_ssh_root_login'):
            return
        
        sshd_config = "/etc/ssh/sshd_config"
        if os.path.exists(sshd_config):
            try:
                with open(sshd_config, 'r') as f:
                    content = f.read()
                    if "PermitRootLogin yes" in content:
                        self.alert_callback("AUDIT", "SSH Root Login is enabled! Recommended: No", "CRITICAL")
            except Exception as e:
                self.alert_callback("SYSTEM", f"Error reading sshd_config: {str(e)}", "ERROR")

    def check_open_ports(self):
        if not self.config.get('check_open_ports'):
            return
        
        try:
            with os.popen('ss -lntu') as stream:
                output = stream.read()
                self.alert_callback("AUDIT", f"Open ports summary:\n{output}", "INFO")
        except Exception as e:
            self.alert_callback("SYSTEM", f"Error checking open ports: {str(e)}", "ERROR")

    def run_full_audit(self):
        self.audit_file_permissions()
        self.check_ssh_config()
        self.check_open_ports()
