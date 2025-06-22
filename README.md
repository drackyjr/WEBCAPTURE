# 🕸️ WEBCAPTURE

> A stealthy website screenshotting tool for recon, automation, and visual intelligence gathering.

## 🔍 Overview

`WEBCAPTURE` is a simple yet powerful utility for capturing full-page or viewport screenshots of websites. It’s built for OSINT analysts, bug bounty hunters, and security researchers who need quick visual snapshots of live web targets. Useful in reconnaissance, monitoring, or archiving website states.
<video src="https://github.com/drackyjr/WEBCAPTURE/blob/main/Screencast%20From%202025-06-16%2019-45-13.mp4" controls></video>


## 🚀 Features

- 📸 Capture full-page or viewport screenshots
- 🔍 Advanced OSINT data collection (emails, phones, links)
- 🌐 WHOIS and IP geolocation information
- 🔗 Subdomain enumeration
- 🛡️ Enhanced Port Scanning:
  - Multiple scan types (quick, stealth, comprehensive, common ports, top 1000)
  - TCP/UDP protocol support
  - Banner grabbing and service detection
  - Custom port range scanning
  - Stealth mode for evasive scanning
  - Detailed security recommendations
- 🧠 Fast and minimal footprint
- ⚙️ CLI-based usage for automation
- 🕵️‍♂️ Ideal for recon workflows and threat hunting

## 🛠️ Requirements

- Python 3.8+
- Linux / Windows / MacOS
- Google Chrome or Chromium (headless mode)
- `pip` for installing dependencies

## 🧪 Installation

```bash
git clone https://github.com/drackyjr/WEBCAPTURE.git
cd WEBCAPTURE
pip install -r requirements.txt
```

### Usage 
```bash
# Basic OSINT scan
python3 main.py --url <URL> --emails --phones --links --whois --ipinfo --subdomains

# Full scan with screenshot and enhanced port scanning
python3 main.py --url <URL> --emails --phones --links --whois --ipinfo --subdomains --screenshot --port-scan --scan-type comprehensive --grab-banner

# Stealth port scan with custom range
python3 main.py --url <URL> --port-scan --scan-type range --port-range 1 10000 --stealth --protocol both --grab-banner

# Quick security assessment
python3 main.py --url <URL> --port-scan --scan-type quick --grab-banner --whois --ipinfo

# Save results to a specific folder
python3 main.py --url <URL> --emails --phones --links --whois --ipinfo --subdomains --screenshot --port-scan --save results/
```

### Available Options

#### Basic Options
- `--url`: Target URL (required)
- `--emails`: Extract email addresses
- `--phones`: Extract phone numbers
- `--links`: Extract all links
- `--whois`: Perform WHOIS lookup
- `--ipinfo`: Get IP geolocation information
- `--subdomains`: Enumerate subdomains
- `--screenshot`: Take website screenshot
- `--check-stealer`: Check domain exposure
- `--save`: Save results to specified folder

#### Enhanced Port Scanning Options
- `--port-scan`: Enable port scanning
- `--scan-type`: Type of port scan (`common`, `top1000`, `range`, `quick`, `comprehensive`)
- `--protocol`: Protocol to scan (`tcp`, `udp`, `both`)
- `--grab-banner`: Grab service banners
- `--stealth`: Enable stealth mode
- `--port-range`: Custom port range (e.g., `1 1000`)



