# 🐻 Simple Python Honeypot

**Educational low-interaction honeypot** built step-by-step for cybersecurity beginners. Mimics vulnerable SSH/FTP/HTTP services to capture attacker reconnaissance, banner grabbing, and brute-force attempts. 100% Python standard library—no external dependencies.

**Status: Production-ready** | **Tested: Windows 11 + VS Code** | **Author: l1ght-man**

## 🎯 What It Does

```
Attackers scan → Connect to ports 22/21/80 → Get fake service banners → Send credentials → ALL LOGGED → ANALYZED
```

- **SSH (22)**: Fake "SSH-2.0-FakeSSH" banner → logs usernames/passwords
- **FTP (21)**: Fake "220 Fake FTP Server ready" → logs USER/PASS commands  
- **HTTP (80)**: **AI-generated** fake admin panel → logs GET/POST requests + form submissions
- **Log Analyzer**: HTML dashboard → top IPs, paths, scanners

## 🚀 Quick Start 

```bash
# Clone repo
git clone https://github.com/l1ght-man/HoneyPot.git
cd HoneyPot

# Run honeypot (logs attacks)
python honeypot.py

# Analyze logs (creates attack_report.html)
python analyze_logs.py
```

**Expected console:**
```
[*] Listening on port 22 (SSH)
[*] Listening on port 21 (FTP)  
[*] Listening on port 80 (HTTP)
```

**Test:** `telnet localhost 22` or browser: `http://localhost/` → **instant logs!**

## 🗂️ File Structure
```
honeypot/
├── honeypot.py          # 🐍 Main honeypot + HTTP parser (human-written)
├── fake_website.html    # 🎨 **AI-GENERATED** fake vulnerable website
│   └── 100% AI-created - NO HUMAN CREDIT TAKEN - Public domain
├── analyze_logs.py      # 📊 Log analyzer + HTML dashboard (human-written)
├── README.md           # 📖 This file
└── Honeypot_logs/      # 📊 Auto-created daily logs
    └── honeypot_YYYY-MM-DD.jsonl
```

## 📊 Log Analyzer Dashboard

```bash
python analyze_logs.py
```

**Generates:** `attack_report.html` with:
- **Top 10 attacking IPs** (most hits)
- **Targeted ports** (SSH/FTP/HTTP breakdown)
- **HTTP paths** (what attackers target: /admin, /login.php, etc.)
- **Scanner User-Agents** (Nmap, Nikto, curl, etc.)

**Example report entry:**
```
🥇 Top Attacking IPs
192.168.100.200 — 247 hits
8.8.8.8 — 89 hits
10.0.0.5 — 34 hits

🔌 Most Targeted Ports
HTTP (80) — 185 hits
SSH (22) — 145 hits
FTP (21) — 30 hits

🌐 Top HTTP Paths
/ — 92 hits
/login.php — 45 hits
/admin — 38 hits
/favicon.ico — 25 hits

🕷️ Top Scanners
Mozilla/5.0 (Nmap NSE script) — 56 hits
curl/8.17.0 — 34 hits
```

## 📋 Sample Attack Logs

**Raw JSONL format (honeypot_2026-01-22.jsonl):**
```json
{"timestamp": "2026-01-22T14:20:01.123Z", "ip": "192.168.100.200", "port": 22, "data": "banner sent"}
{"timestamp": "2026-01-22T14:20:02.456Z", "ip": "192.168.100.200", "port": 22, "data": "📥 root"}
{"timestamp": "2026-01-22T14:20:03.789Z", "ip": "192.168.100.200", "port": 22, "data": "📥 password123"}
{"timestamp": "2026-01-22T14:20:10.012Z", "ip": "8.8.8.8", "port": 80, "data": "🌐 HTTP GET '/admin'"}
{"timestamp": "2026-01-22T14:20:11.345Z", "ip": "8.8.8.8", "port": 80, "data": "🕷️ Mozilla/5.0 (Nmap)"}
```

## 📈 What You'll Learn From Real Attackers

**Most common patterns:**
- SSH brute-force: `root`, `admin`, `test` + `123456`, `password`, `admin` credentials
- HTTP scanners: Nikto, Nmap NSE, OpenVAS finding `/admin`, `/wp-login.php`, `/phpmyadmin`
- Post-compromise: Command attempts on SSH, SQLi in URLs, LFI attempts

**Why it matters:**
- See **real attacker behavior** without honeypot framework complexity
- Build **security awareness** — attackers ARE trying these paths/creds
- Learn **log analysis** — spot patterns, anomalies, coordinated attacks

## 🔧 How It Works (Beginner-Friendly)

### honeypot.py
```
Class Honeypot:
  ├─ __init__() → Setup ports [22, 21, 80] + fake banners + load HTML
  ├─ log_activity() → Save to JSONL (timestamp, IP, port, data)
  ├─ handle_client() → Per-connection: send banner → log data → close
  └─ listen_port() → Multi-threaded socket listener
```

**Key Python concepts learned:**
- Classes + `self` (object organization)
- Socket programming (TCP servers)
- Multithreading (handle multiple attackers)
- JSON logging (structured data)
- Error handling (`try/except/finally`)

### analyze_logs.py
```
Main functions:
  ├─ load_logs() → Read all JSONL files
  ├─ analyze_logs() → Counter() each: IPs, ports, paths, User-Agents
  └─ generate_html_report() → Create beautiful dashboard HTML
```

**Key concepts:**
- `glob` module (find files with wildcards)
- `Counter` (automatic counting + ranking)
- String splitting (extract paths from logs)
- HTML templating with f-strings

## ⚠️ Safety & OPSEC

| Network | Risk | Recommendation |
|---------|------|---------------|
| 🟢 **localhost** | **Safe** | Perfect for learning |
| 🟡 **Local LAN** | Medium | Firewall required |
| 🔴 **Internet** | **DANGER** | VM + strict firewall ONLY |

**Best practices:**
- Never expose to internet without VM/isolation
- Logs contain attacker IPs — handle responsibly
- Don't run on production systems
- Firewall allow Python through before testing

## 🔮 Roadmap / Next Features

- [x] Multi-port SSH/FTP/HTTP listener
- [x] HTTP request parsing (paths, User-Agents)
- [x] AI-generated fake website lure
- [x] JSONL logging with timestamps
- [x] Log analyzer dashboard
- [ ] Telnet (port 23) + SMTP (port 25) services
- [ ] Real-time web dashboard (running stats)
- [ ] GeoIP mapping (attacker locations)
- [ ] Docker containerization
- [ ] Integration with threat intelligence feeds

## 🙏 Credits & Full Transparency

### Human-Written (Full Credit to l1ght-man)
- **honeypot.py**: Python socket logic, threading, HTTP parser, emoji logging
- **analyze_logs.py**: Counter-based analytics, HTML report generation, glob file finding
- **Project structure**: Modular open-source architecture
- **README documentation**: Educational explanations

### AI-Generated (Public Domain — NO CREDIT TAKEN)
- **fake_website.html**: 100% AI-created HTML/CSS/JavaScript
  - Hacker-themed login UI
  - Form submission handler
  - Fake vulnerability hints (debug params, sql hints)
  - **Fully customizable** — edit freely for your honeypot variations

### Learning Resources Referenced
- Python socket programming (RealPython.com)
- Low-interaction honeypot tutorials (OWASP, Hacker's Arise)
- HTTP server patterns (MDN Web Docs)
- Cybersecurity best practices

## 📄 License

**MIT License** — Free for:
- ✅ Educational use
- ✅ Personal projects
- ✅ Forks & modifications
- ✅ Redistribution with credit

**NOT for:**
- ❌ Malicious purposes
- ❌ Attacking systems without consent

## 🚀 Contributing

1. Fork the repository
2. Add features (new services, better analytics, visualizations)
3. Test thoroughly
4. Submit pull request with description

**Ideas:**
- More service emulations (Telnet, MySQL, SMTP)
- GeoIP visualization
- Email alerts on specific attack patterns
- Machine learning for attacker classification

## 📞 Support & Questions

- **Issues?** GitHub Issues tab
- **Want to learn more?** Check out inline code comments
- **Customize HTML?** Edit `fake_website.html` — it's just HTML!

---

**"Built by a beginner, for beginners. Security through transparency and open-source learning."**

*Last updated: January 22, 2026*
*Status: ✅ Fully functional — Ready for real attack capture*
