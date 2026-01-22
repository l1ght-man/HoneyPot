# 🐻 Simple Python Honeypot

**Educational low-interaction honeypot** built step-by-step for cybersecurity beginners. Mimics vulnerable SSH/FTP/HTTP services to capture attacker reconnaissance, banner grabbing, and brute-force attempts. 100% Python standard library—no external dependencies.

**Status: Working prototype** | **Tested: Windows 11 + VS Code** | **Author:l1ght-man**

## 🎯 What It Does

Attackers scan → Connect to ports 22/21/80 → Get fake service banners → Send credentials → ALL LOGGED

- **SSH (22)**: Fake "SSH-2.0-FakeSSH" banner → logs usernames/passwords
- **FTP (21)**: Fake "220 Fake FTP Server ready" → logs USER/PASS commands  
- **HTTP (80)**: Fake webpage → logs GET/POST requests

## 🚀 Quick Start 
1. git clone
```bash
git clone https://github.com/l1ght-man/HoneyPot.git
```
 2. run it
```bash
python honeypot.py
```
## 🛠️ File Structure
```bash
honeypot/
├── honeypot.py          # Main honeypot code
├── README.md           # This file
└── Honeypot_logs/      # Auto-created daily logs
    └── honeypot_YYYY-MM-DD.jsonl
```
## 📈 What You'll Learn From Attackers

-**Most common**: SSH brute-force (root, admin, test + 123456 passwords)
-**Watch for**: Port scanners, vulnerability scanners, exploit attempts