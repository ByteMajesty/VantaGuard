# 🛡️ VantaGuard

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.6+](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Platform: Linux](https://img.shields.io/badge/Platform-Linux-lightgrey.svg)](https://www.linux.org/)

**VantaGuard** is a high-performance, real-time Intrusion Detection System (IDS) and automated security auditor designed specifically for Linux environments. Built for scale and simplicity.

---

## ✨ Key Features

- **🔍 Real-time Log Monitoring:** Instantly detects failed logins, unauthorized access attempts, and critical system errors.
- **🛡️ Automated Hardening Audit:** Scans for insecure file permissions, weak SSH configurations, and exposed network ports.
- **⚙️ Process Surveillance:** Identifies suspicious process executions (e.g., reverse shells, scanning tools).
- **📊 Structured Alerting:** Categorized alerts (INFO to CRITICAL) with color-coded console output and persistent logging.
- **📦 Modular Architecture:** Easily extendable to include custom security rules and monitoring modules.

---

## 🚀 Installation

### From Source
```bash
git clone https://github.com/ByteMajesty/VantaGuard.git
cd VantaGuard
pip install .
```

---

## 🛠️ Usage

Once installed, you can run VantaGuard directly from your terminal:

```bash
vantaguard --config config.yaml
```

### Options
- `--config`: Path to your custom configuration file.
- `--audit-only`: Run the security auditor and exit.
- `--version`: Show the current version.

---

## ⚙️ Configuration

VantaGuard uses a simple `config.yaml` file to define its behavior. You can customize log paths, suspicious process names, and sensitive files to audit.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 👤 Author

**ByteMajesty**
- GitHub: [@ByteMajesty](https://github.com/ByteMajesty)
- Project Link: [https://github.com/ByteMajesty/VantaGuard](https://github.com/ByteMajesty/VantaGuard)

---
*Developed with a focus on performance and absolute security.*
