<h1 align="center">🗝️ WalkLogger</h1>

<p align="center">
  <img src="https://github.com/Krishna845-prog/WalkLogger/blob/main/Walkloggerlogo.jpg" alt="WalkLogger Logo" width="400">
</p>


> **"Unseen, Unheard, Unstoppable. Capture Every Keystroke."**

![Made With Python](https://img.shields.io/badge/Made%20With-Python-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20MacOS-orange)

---

## 🧠 What is WalkLogger?

**WalkLogger** is an advanced, stealth-mode keylogger tool made for cybersecurity research, red-teaming, and digital behavior analysis. It runs in the background, captures every keystroke, takes a screenshot every 10 seconds, and alerts users when potentially dangerous terminal commands are detected.

The GUI is built with a dark hacker aesthetic — perfect for demos, testing, and adding flair to your resume. WalkLogger hides in the system tray and continues running silently until you choose to exit.

---

## 🔥 Features

- 🔐 **Keylogging** in real-time with GUI display
- 🖼️ **Screenshot capture every 10 seconds** (stored locally)
- 🚨 **Suspicious behavior detection** using keyword matching
- 👻 **Stealth Mode** — Hide to system tray, click to reveal
- 💡 **Dark hacker GUI** with green-on-black theme
- 🛠️ Lightweight and cross-platform (Windows, Linux, macOS)
- 🔔 Popup alerts when malicious activity is detected

---

## 📸 Tool Previews

<p align="center">
  <img src="https://github.com/Krishna845-prog/WalkLogger/blob/main/keylogger%20output.jpg" alt="WalkLogger Recording Preview" width="600">
</p>

<p align="center">
  <img src="https://github.com/Krishna845-prog/WalkLogger/blob/main/keylogger%20output.jpg" alt="WalkLogger Recording Preview" width="600">
</p>

## 🚀 Installation & Usage

```bash
# Clone the repo
git clone https://github.com/yourusername/walklogger.git
cd walklogger

# Install dependencies
pip install -r requirements.txt

# Run the logger
python walklogger.py
```
## 📂 Output Files

| File/Folder              | Description                                      |
|--------------------------|--------------------------------------------------|
| `keylog.txt`             | All logged keystrokes                           |
| `screenshots/`           | Screenshots captured every 10 seconds           |
| `suspicious_behavior.txt`| Logs of any suspicious commands typed           |

## 🧠 How Suspicious Behavior Detection Works

WalkLogger uses a list of keywords commonly associated with malicious or admin-level behavior (like `sudo`, `rm -rf`, `nmap`, etc.).  
If any of these are typed, an alert is triggered and the activity is logged.

### 🔍 Behavior Detection Code Snippet

```python
suspicious_keywords = [
    "cmd", "powershell", "rm -rf", "sudo", "nmap", 
    "proxychains", "curl", "python", "reverse", "malware"
]

def analyze_behavior(current_log):
    suspicious_hits = []
    for word in suspicious_keywords:
        pattern = r"\b" + re.escape(word) + r"\b"
        if re.search(pattern, current_log.lower()):
            suspicious_hits.append(word)

    if suspicious_hits:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open("suspicious_behavior.txt", "a") as f:
            f.write(f"[{timestamp}] Suspicious: {', '.join(suspicious_hits)}\n")
        messagebox.showwarning("Alert!", f"Suspicious behavior detected: {', '.join(suspicious_hits)}")

```

## 💻 Supported Platforms

✅ Windows  
✅ macOS  
✅ Linux  

> **Note:** Screenshot capture might not work in headless environments like remote CLI servers.

---

## 🛠 Usage Tips

- Change screenshot interval with: `screenshot_interval = 10`
- Update suspicious keywords to customize behavior alerts
- Click “Hide Window” to move to tray — icon shows “WL” in green
- Access the tool again by clicking the tray icon

---

## 🗺️ Roadmap

✅ Keylogger Core  
✅ Screenshot Every 10s  
✅ Popup Behavior Alert  
✅ Stealth Tray Integration  

🔜 Flask Web Dashboard (Encrypted Logs)  
🔜 Email Notification System  
🔜 Encrypted Log Upload to Webhook  
🔜 Cloud Integration (Optional)

---

## 🤝 Contributing

We ❤️ the open-source community! Here's how you can contribute:

```bash
# 1. Fork the repo
# 2. Create your feature branch:
git checkout -b awesome-feature

# 3. Commit your changes:
git commit -m "Added awesome feature"

# 4. Push to the branch:
git push origin awesome-feature

# 5. Open a Pull Request
```

## 📚 Use Cases

🔍 Red-Team Simulation Projects  
💻 Offensive Security Labs  
🎓 Cybersecurity Education & Practice  
🧪 Suspicious Behavior Monitoring  
📈 Digital Forensics & Incident Response (DFIR)

---

## ✨ Author

👨‍💻 **Krishna Arun Iyer**  
Cybersecurity Enthusiast | Ethical Hacker | Developer  
🧪 Focused on malware analysis, keyloggers, ethical red-teaming

---

## 🛡️ License

**MIT License** — free to use, modify, and distribute for educational or ethical use.

---

## ⚠️ Disclaimer

This tool is created solely for **educational and ethical cybersecurity research**.  **Misuse** of this tool for illegal or malicious purposes is **strictly prohibited**.  The author takes **no responsibility** for any damages caused by misuse.

---

## 💥 Like the Project?

If you like this project, give it a ⭐ on GitHub and share it with your cyber crew!  Let’s make **WalkLogger** the most powerful ethical keylogging toolkit out there.



