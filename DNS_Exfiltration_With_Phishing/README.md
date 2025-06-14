# Phishing Simulation with DNS Exfiltration

## Overview

This tool simulates a phishing campaign with the following capabilities:

- Sends custom phishing emails with adaptive templates.
- Attaches a payload executable (`attachment.exe`) that:
  - Collects basic system information.
  - Runs enumeration tools (`LinEnum` for Linux, `winPEAS` for Windows).
  - Exfiltrates the gathered data via DNS queries to a local DNS server (e.g., `bind9`).

## Components

- `phising.py`: Python script for crafting and sending phishing emails.
- `attach_create.py`: Python script compiled into `attachment.exe`.
- `attachment.exe`: Payload sent in the phishing email, performs collection & exfiltration.
- `templates/`: Directory of phishing email text templates for different user profiles.

---

## How to Use

### Step 1: Setup Mail Server (MailHog)

To receive phishing emails:
```bash
docker run -d -p 1025:1025 -p 8025:8025 mailhog/mailhog
```
Access it at: [http://localhost:8025](http://localhost:8025)

---

### Step 2: Run the Email Generator

Install dependencies:
```bash
pip install requests
```

Run the script:
```bash
python phising.py
```

Follow the prompts to select a template and send an email with an attachment (`attachment.exe`).

---

## Windows Notes

To run `attachment.exe` on Windows:

1. Make sure the machine is using your local Linux DNS server:
   ```powershell
   Set-DnsClientServerAddress -InterfaceAlias "Wi-Fi" -ServerAddresses ("192.168.1.228")
   ```
   - Requires admin PowerShell.

2. Double-click `attachment.exe` or run it from PowerShell:
   ```powershell
   .\attachment.exe
   ```

3. You can monitor DNS traffic from the Linux side using:
   ```bash
   sudo tcpdump -i lo port 53
   ```

---

## Requirements

- Python 3.8+
- MailHog (for testing email)
- `bind9` running on `192.168.1.228` (for DNS exfiltration)
- Linux or Windows test machine

---