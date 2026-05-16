import sys, os, math, random, shutil, platform, subprocess, time, threading, json
from datetime import datetime
from pathlib import Path
import customtkinter as ctk
import psutil, os, sys, time, threading, random, shutil, platform, subprocess
from datetime import datetime
from tkinter import messagebox, simpledialog, filedialog
import tkinter as tk
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QIcon
import sys
import psutil
from PyQt6.QtCore import Qt, QTimer, QTime, QDate, QPoint, QRect, QSize, pyqtSignal, QThread, pyqtSlot, QEvent
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QLineEdit, QMenu, QInputDialog, QMessageBox,
    QGridLayout, QSizePolicy, QGraphicsDropShadowEffect, QTextEdit,
    QProgressBar, QListWidget, QListWidgetItem, QTableWidget, QTableWidgetItem,
    QHeaderView, QTabWidget, QDialog, QComboBox, QStackedWidget, QSlider,
    QFontComboBox, QSpinBox, QSplitter, QSizeGrip, QCheckBox, QFileDialog
)
from PyQt6.QtGui import (
    QPainter, QLinearGradient, QRadialGradient, QColor, QFont, QPen,
    QBrush, QCursor, QTextCursor, QFontMetrics, QPixmap
)
# Settings file path
SETTINGS_FILE = Path.home() / ".novaos_settings.json"
SCRIPT_DIR = Path(os.path.abspath(__file__)).parent
import ctypes

try:
    import cv2
    from PIL import Image, ImageTk
    HAS_VIDEO = True
except ImportError:
    HAS_VIDEO = False
# ═══════════════════════════════════════════════════════════════════════════════
#  THEME / COLORS
# ═══════════════════════════════════════════════════════════════════════════════
ACCENT   = "#00D4FF"
ACCENT2  = "#7B2FFF"
SUCCESS  = "#00E676"
WARNING  = "#FFB300"
DANGER   = "#FF3D57"
BG_DEEP  = "#0A0E1A"
BG_PANEL = "#0F1628"
BG_CARD  = "#141E35"
BG_HOVER = "#1C2A47"
TEXT     = "#E8F0FF"
TEXT_DIM = "#6B7FA3"

WALLPAPERS = {
    "gradient_blue":   [QColor("#0d1117"), QColor("#0f2744"), QColor("#0d1b2e")],
    "gradient_purple": [QColor("#1a0a2e"), QColor("#2d1b4e"), QColor("#1a0a2e")],
    "gradient_green":  [QColor("#0a1f0a"), QColor("#0d3320"), QColor("#0a1a0a")],
    "gradient_dark":   [QColor("#0a0a0a"), QColor("#1a1a1a"), QColor("#0a0a0a")],
    "gradient_sunset": [QColor("#1a0808"), QColor("#2e1a0a"), QColor("#1a0808")],
    "gradient_nova":   [QColor("#0A0E1A"), QColor("#0F1628"), QColor("#0A0E1A")],
    "gradient_cyber":  [QColor("#050510"), QColor("#0d0d2e"), QColor("#050510")],
}

WALLPAPER_NAMES = {
    "gradient_blue":   "🌊 Ocean Blue",
    "gradient_purple": "🌌 Deep Space",
    "gradient_green":  "🌲 Forest",
    "gradient_dark":   "⚫ Midnight",
    "gradient_sunset": "🌅 Sunset",
    "gradient_nova":   "🔷 NOVA Blue",
    "gradient_cyber":  "💜 Cyber Dark",
}

CUSTOM_WALLPAPERS = {}

# Global reference — keeps the LoginScreen alive after all other windows close
_LOGIN_SCREEN_REF = None

ACCENT_COLORS = {
    "Cyan":   "#00D4FF",
    "Purple": "#7B2FFF",
    "Blue":   "#0078D4",
    "Green":  "#00E676",
    "Orange": "#FFB300",
    "Pink":   "#FF3D57",
    "Gold":   "#FFB900",
}


DESKTOP_APPS = [
    {"name": "File Manager",  "icon": "📁", "type": "app",    "action": "file_manager",  "color": "#00BCF2"},
    {"name": "Terminal",      "icon": "⌨️", "type": "app",    "action": "terminal",      "color": "#00E676"},
    {"name": "Task Manager",  "icon": "📊", "type": "app",    "action": "task_manager",  "color": "#7B2FFF"},
    {"name": "Memory",        "icon": "🧠", "type": "app",    "action": "memory",        "color": "#00D4FF"},
    {"name": "I/O Devices",   "icon": "🔌", "type": "app",    "action": "io_devices",    "color": "#FFB300"},
    {"name": "Calculator",    "icon": "🧮", "type": "app",    "action": "calculator",    "color": "#FF3D57"},
    {"name": "Text Editor",   "icon": "📝", "type": "app",    "action": "text_editor",   "color": "#00E676"},
    {"name": "Notes",         "icon": "📒", "type": "app",    "action": "notes",         "color": "#FFB900"},
    {"name": "Browser",       "icon": "🌐", "type": "app",    "action": "browser",       "color": "#00BCF2"},
    {"name": "Paint",         "icon": "🎨", "type": "app",    "action": "paint",         "color": "#FF6B9D"},
    {"name": "Calendar",      "icon": "📅", "type": "app",    "action": "calendar",      "color": "#00D4FF"},
    {"name": "WiFi",          "icon": "🛜", "type": "app",    "action": "wifi",          "color": "#00E676"},
    {"name": "Settings",      "icon": "⚙️", "type": "app",    "action": "settings",      "color": "#888888"},
    {"name": "Recycle Bin",   "icon": "🗑️", "type": "system", "action": "recycle_bin",   "color": "#FF3D57"},
    {"name": "About",         "icon": "ℹ️", "type": "app",    "action": "about",         "color": "#7B2FFF"},
]

PINNED_APPS = [
    ("⌨️", "Terminal",      "terminal"),
    ("📁", "File Manager",  "file_manager"),
    ("📊", "Task Manager",  "task_manager"),
    ("🧠", "Memory",        "memory"),
    ("🔌", "I/O Devices",   "io_devices"),
    ("🧮", "Calculator",    "calculator"),
    ("📝", "Text Editor",   "text_editor"),
    ("📒", "Notes",         "notes"),
    ("🌐", "Browser",       "browser"),
    ("🎨", "Paint",         "paint"),
    ("📅", "Calendar",      "calendar"),
    ("⚙️", "Settings",      "settings"),
]

APP_SIZES = {
    "terminal":     (720, 480),
    "file_manager": (820, 540),
    "text_editor":  (700, 500),
    "calculator":   (340, 500),
    "settings":     (750, 600),
    "task_manager": (700, 480),
    "recycle_bin":  (500, 400),
    "browser":      (900, 620),
    "paint":        (820, 580),
    "calendar":     (520, 460),
    "notes":        (500, 420),
    "about":        (500, 400),
    "io_devices":   (700, 500),
    "wifi":         (420, 400),
    "memory":       (740, 540),
}

APP_COLORS = {
    "terminal":     "#0A1520",
    "file_manager": "#0f1a28",
    "text_editor":  "#1e1e2e",
    "calculator":   "#1a1a2e",
    "settings":     "#0f1628",
    "task_manager": "#0f1820",
    "recycle_bin":  "#1f1010",
    "browser":      "#0f1a2a",
    "paint":        "#1a1a1a",
    "calendar":     "#0d1a30",
    "notes":        "#1a1e10",
    "about":        "#0d1020",
    "io_devices":   "#0f1030",
    "wifi":         "#0f1a20",
    "memory":       "#0A0E1A",
}

# Apps restricted to admin role only – non-admins get "Permission Denied"
ADMIN_ONLY_APPS = {"terminal", "task_manager", "settings"}

ICON_MAP = {
    ".py":"🐍",".js":"🟨",".ts":"🔷",".html":"🌐",".css":"🎨",
    ".json":"📋",".md":"📝",".txt":"📄",".csv":"📊",".xml":"📰",
    ".png":"🖼",".jpg":"🖼",".jpeg":"🖼",".gif":"🖼",".svg":"🖼",
    ".mp4":"🎬",".mp3":"🎵",".wav":"🎵",
    ".zip":"📦",".tar":"📦",".gz":"📦",".rar":"📦",
    ".pdf":"📕",".docx":"📘",".xlsx":"📗",".pptx":"📙",
    ".exe":"⚙️",".sh":"📜",".bat":"📜",".c":"💾",".cpp":"💾",
    ".h":"💾",".java":"☕",".go":"🐹",".rs":"🦀",".rb":"💎",
}

def file_icon(path):
    if os.path.isdir(path): return "📁"
    ext = Path(path).suffix.lower()
    return ICON_MAP.get(ext, "📄")

def fmt_size(n):
    for u in ["B","KB","MB","GB","TB"]:
        if n < 1024: return f"{n:.1f} {u}"
        n /= 1024
    return f"{n:.1f} PB"

# ═══════════════════════════════════════════════════════════════════════════════
#  BACKEND MANAGERS
# ═══════════════════════════════════════════════════════════════════════════════
class ProcessManager:
    def __init__(self):
        self.custom = {}
        self.next_pid = 9000

    def spawn(self, name):
        pid = self.next_pid; self.next_pid += 1
        self.custom[pid] = {
            "pid": pid, "name": name, "state": "running",
            "cpu": round(random.uniform(0.1, 10), 1),
            "mem": round(random.uniform(0.1, 5), 1),
            "priority": 5, "started": datetime.now().strftime("%H:%M:%S"),
            "threads": random.randint(1, 4),
        }
        return pid

    def kill_custom(self, pid):
        if pid in self.custom:
            name = self.custom.pop(pid)["name"]
            return f"Process {pid} ({name}) terminated."
        return f"Simulated process PID {pid} not found. (Only PIDs 9000-9999 are simulated)"

    def suspend_custom(self, pid):
        if pid in self.custom:
            self.custom[pid]["state"] = "suspended"
            return f"Process {pid} suspended."
        return f"Simulated process PID {pid} not found."

    def resume_custom(self, pid):
        if pid in self.custom:
            self.custom[pid]["state"] = "running"
            return f"Process {pid} resumed."
        return f"Simulated process PID {pid} not found."

    def all_processes(self):
        result = []
        for p in self.custom.values():
            result.append({**p, "real": False})
        return result

    def fluctuate(self):
        for p in self.custom.values():
            if p["state"] == "running":
                p["cpu"] = round(max(0, p["cpu"] + random.uniform(-1, 1)), 1)
                p["mem"] = round(max(0.1, p["mem"] + random.uniform(-0.2, 0.2)), 1)


class MemoryManager:
    def __init__(self, total_mb=2048):
        self.total = total_mb
        self.pages = [None] * (total_mb // 4)
        self.allocs = {}
        for name, n in [("kernel", 8), ("gui", 12), ("scheduler", 4), ("fs_drv", 6)]:
            base = sum(len(v) for v in self.allocs.values())
            idxs = list(range(base, base + n))
            self.allocs[name] = idxs
            for i in idxs:
                if i < len(self.pages): self.pages[i] = name

    def allocate(self, name, mb):
        need = max(1, mb // 4)
        free = [i for i, p in enumerate(self.pages) if p is None]
        if len(free) < need:
            return None, f"Not enough memory ({len(free)*4} MB free, need {mb} MB)."
        chosen = free[:need]
        for i in chosen: self.pages[i] = name
        self.allocs[name] = chosen
        return chosen, f"Allocated {need*4} MB ({need} pages) to '{name}'."

    def free(self, name):
        if name not in self.allocs: return f"'{name}' not in memory."
        for i in self.allocs.pop(name): self.pages[i] = None
        return f"'{name}' freed successfully."

    @property
    def used_mb(self): return sum(1 for p in self.pages if p) * 4
    @property
    def free_mb(self): return self.total - self.used_mb
    @property
    def pct(self): return self.used_mb / self.total * 100


class IOManager:
    INPUT_DEVICES = {
        "Keyboard":   {"icon": "⌨️", "type": "USB HID",    "port": "USB 3.0", "driver": "HID Standard", "irq": 1},
        "Mouse":      {"icon": "🖱️", "type": "USB HID",    "port": "USB 2.0", "driver": "HID Standard", "irq": 12},
        "Webcam":     {"icon": "📷", "type": "USB Video",  "port": "USB 3.0", "driver": "UVC Driver",   "irq": 9},
        "Microphone": {"icon": "🎙️", "type": "Audio In",   "port": "3.5mm",   "driver": "HD Audio",     "irq": 5},
        "Scanner":    {"icon": "📠", "type": "USB",        "port": "USB 2.0", "driver": "WIA Driver",   "irq": 7},
        "Touchpad":   {"icon": "🖐️", "type": "I2C HID",   "port": "Internal","driver": "Precision TD", "irq": 13},
    }
    OUTPUT_DEVICES = {
        "Monitor":    {"icon": "🖥️", "type": "Display",    "port": "HDMI",    "driver": "GPU Display",  "irq": 0},
        "Speaker":    {"icon": "🔊", "type": "Audio Out",  "port": "3.5mm",   "driver": "HD Audio",     "irq": 5},
        "Printer":    {"icon": "🖨️", "type": "USB Print",  "port": "USB 2.0", "driver": "PCL Driver",   "irq": 7},
        "USB Drive":  {"icon": "💾", "type": "Mass Storage","port": "USB 3.0","driver": "USB MSC",      "irq": 9},
        "HDMI Out":   {"icon": "📺", "type": "Display",    "port": "HDMI 2.0","driver": "GPU Display",  "irq": 0},
        "Headphones": {"icon": "🎧", "type": "Audio Out",  "port": "3.5mm",   "driver": "HD Audio",     "irq": 5},
    }
    DEFAULT_CONNECTED = {
        "Keyboard": True, "Mouse": True, "Webcam": False,
        "Microphone": True, "Scanner": False, "Touchpad": True,
        "Monitor": True, "Speaker": True, "Printer": False,
        "USB Drive": True, "HDMI Out": False, "Headphones": False,
    }

    def __init__(self):
        self.connected = dict(self.DEFAULT_CONNECTED)
        self.ops = {k: 0 for k in list(self.INPUT_DEVICES) + list(self.OUTPUT_DEVICES)}
        self.log = []

    def toggle(self, name):
        self.connected[name] = not self.connected.get(name, False)
        return self.connected[name]

    def simulate_io(self):
        for name in self.ops:
            if self.connected.get(name, False):
                self.ops[name] += random.randint(0, 20)

    def all_devices(self):
        return {**self.INPUT_DEVICES, **self.OUTPUT_DEVICES}


# ═══════════════════════════════════════════════════════════════════════════════
#  STATE MANAGER WITH PERSISTENT STORAGE
# ═══════════════════════════════════════════════════════════════════════════════
class StateManager:
    def __init__(self):
        self.current_user = None
        self.theme = "dark"
        self.accent_color = "#00D4FF"
        self.wallpaper = "gradient_nova"
        self.custom_wallpaper_path = None
        self.volume = 70
        self.language = "en"
        self.total_ram = 8192
        self.used_ram = 1024
        self.processes = []
        self.next_pid = 1000
        self.open_windows = {}
        self.notifications = []
        self.clipboard = None
        self.clipboard_op = None
        self.recycle_bin = []
        self.wifi_connected = True
        self.wifi_name = "NOVA OS-Network"
        self.notes = {"Quick Note": "Write your notes here..."}

        self.pm = ProcessManager()
        self.mm = MemoryManager()
        self.io = IOManager()

        self._running = True
        self._init_filesystem()
        self._init_users()
        
        # Load saved settings
        self._load_settings()

        t = threading.Thread(target=self._update_loop, daemon=True)
        t.start()
    
    def _load_settings(self):
        try:
            if SETTINGS_FILE.exists():
                with open(SETTINGS_FILE, 'r') as f:
                    data = json.load(f)
                    self.theme = data.get('theme', 'dark')
                    self.accent_color = data.get('accent_color', '#00D4FF')
                    self.wallpaper = data.get('wallpaper', 'gradient_nova')
                    self.custom_wallpaper_path = data.get('custom_wallpaper_path', None)
                    self.volume = data.get('volume', 70)
                    self.wifi_connected = data.get('wifi_connected', True)
                    self.wifi_name = data.get('wifi_name', 'NOVA OS-Network')
                    if self.custom_wallpaper_path and not os.path.exists(self.custom_wallpaper_path):
                        self.custom_wallpaper_path = None
                    # Restore saved user passwords
                    if 'users' in data:
                        for uname, udata in data['users'].items():
                            if uname in self.users and 'password' in udata:
                                self.users[uname]['password'] = udata['password']
        except Exception as e:
            print(f"Error loading settings: {e}")
    
    def save_settings(self):
        try:
            data = {
                'theme': self.theme,
                'accent_color': self.accent_color,
                'wallpaper': self.wallpaper,
                'custom_wallpaper_path': self.custom_wallpaper_path,
                'volume': self.volume,
                'wifi_connected': self.wifi_connected,
                'wifi_name': self.wifi_name,
                'users': self.users,
            }
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def set_accent(self, color):
        self.accent_color = color
        self.save_settings()
    
    def set_theme(self, theme):
        self.theme = theme
        self.save_settings()
    
    def set_wallpaper(self, wallpaper, custom_path=None):
        self.wallpaper = wallpaper
        if custom_path:
            self.custom_wallpaper_path = custom_path
        self.save_settings()
    
    def set_volume(self, volume):
        self.volume = volume
        self.save_settings()

    def _init_filesystem(self):
        self.fs = {
            "Documents": {"type": "folder", "children": {
                "Welcome.txt": {"type": "file", "content": "Welcome to NOVA OS!\nThis is your Documents folder."},
                "Notes.txt":   {"type": "file", "content": "NOVA OS Notes\n==============\n"},
            }},
            "Downloads": {"type": "folder", "children": {}},
            "Pictures":  {"type": "folder", "children": {
                "Wallpaper1.png": {"type": "file", "content": "[image data]"},
            }},
            "Music":     {"type": "folder", "children": {}},
            "Videos":    {"type": "folder", "children": {}},
        }

    def _init_users(self):
        self.users = {
            "admin":   {"password": "admin123",   "role": "admin", "display": "Administrator"},
            "student": {"password": "student123", "role": "user",  "display": "Student"},
            "guest":   {"password": "guest",      "role": "guest", "display": "Guest"},
        }

    def _update_loop(self):
        while self._running:
            self.pm.fluctuate()
            self.io.simulate_io()
            time.sleep(3)

    def authenticate(self, username, password):
        user = self.users.get(username)
        if user and user["password"] == password:
            self.current_user = username
            return True
        return False

    def get_display_name(self):
        if self.current_user:
            return self.users[self.current_user]["display"]
        return "User"

    def get_role(self):
        if self.current_user:
            return self.users[self.current_user]["role"]
        return "guest"

    def add_process(self, name, memory_mb=64):
        pid = self.next_pid; self.next_pid += 1
        self.processes.append({"pid": pid, "name": name, "memory": memory_mb, "cpu": 0})
        self.used_ram = min(self.total_ram, self.used_ram + memory_mb)
        return pid

    def remove_process(self, pid):
        for p in self.processes:
            if p["pid"] == pid:
                self.used_ram = max(0, self.used_ram - p["memory"])
                self.processes.remove(p)
                return

    def add_notification(self, message, icon="ℹ️"):
        self.notifications.append({"msg": message, "icon": icon})
        if len(self.notifications) > 20: self.notifications.pop(0)

    def delete_to_recycle(self, name, content):
        self.recycle_bin.append({"name": name, "content": content})


# ═══════════════════════════════════════════════════════════════════════════════
#  LOGIN SCREEN
# ═══════════════════════════════════════════════════════════════════════════════
class LoginScreen(QWidget):
    def __init__(self, state):
        super().__init__()
        self.state = state
        self.setWindowTitle("NOVA OS")
        self.setMinimumSize(1024, 720)
        self.showMaximized()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self._setup_ui()
        self._start_clock()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        top = QWidget(); top.setFixedHeight(70)
        top.setStyleSheet("background: transparent;")
        tl = QHBoxLayout(top)
        tl.setContentsMargins(30, 16, 30, 16)
        tl.addStretch()
        self.clock_lbl = QLabel("")
        self.clock_lbl.setStyleSheet("color: rgba(255,255,255,0.85); font-size: 18px; font-weight: 300;")
        tl.addWidget(self.clock_lbl)
        layout.addWidget(top)
        layout.addStretch()

        cc = QHBoxLayout()
        cc.addStretch()
        card = QFrame()
        card.setFixedSize(440, 500)
        card.setStyleSheet("""
            QFrame {
                background: rgba(10, 20, 40, 0.88);
                border-radius: 22px;
                border: 1px solid rgba(0, 212, 255, 0.2);
            }
        """)
        sh = QGraphicsDropShadowEffect()
        sh.setBlurRadius(80); sh.setColor(QColor(0, 212, 255, 60)); sh.setOffset(0, 10)
        card.setGraphicsEffect(sh)
        cl = QVBoxLayout(card)
        cl.setContentsMargins(48, 44, 48, 44)
        cl.setSpacing(14)

        logo = QLabel("⬡")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet("font-size: 52px; color: #00D4FF; background: transparent; border: none;")
        cl.addWidget(logo)
        title = QLabel("NOVA OS")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: white; font-size: 24px; font-weight: 300; letter-spacing: 6px; background: transparent; border: none;")
        cl.addWidget(title)
        sub = QLabel("NOVA OS Edition")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub.setStyleSheet("color: rgba(0,212,255,0.6); font-size: 11px; letter-spacing: 3px; background: transparent; border: none;")
        cl.addWidget(sub)
        cl.addSpacing(8)

        ul = QLabel("USER")
        ul.setStyleSheet("color: rgba(255,255,255,0.4); font-size: 10px; letter-spacing: 2px; background: transparent; border: none;")
        cl.addWidget(ul)
        self.user_combo = QComboBox()
        for uname, ud in self.state.users.items():
            self.user_combo.addItem(f"  {ud['display']} ({uname})", uname)
        self.user_combo.setStyleSheet("""
            QComboBox {
                background: rgba(255,255,255,0.07);
                color: white;
                border: 1px solid rgba(0,212,255,0.25);
                border-radius: 10px;
                padding: 11px 14px;
                font-size: 13px;
            }
            QComboBox:hover { border-color: rgba(0,212,255,0.5); }
            QComboBox::drop-down { border: none; width: 30px; }
            QComboBox QAbstractItemView {
                background: #0f1a30;
                color: white;
                selection-background-color: #0078D4;
                border: 1px solid rgba(0,212,255,0.2);
            }
        """)
        cl.addWidget(self.user_combo)

        pl = QLabel("PASSWORD")
        pl.setStyleSheet("color: rgba(255,255,255,0.4); font-size: 10px; letter-spacing: 2px; background: transparent; border: none;")
        cl.addWidget(pl)
        self.pw_input = QLineEdit()
        self.pw_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pw_input.setPlaceholderText("Enter password...")
        self.pw_input.setFixedHeight(46)
        self.pw_input.setStyleSheet("""
            QLineEdit {
                background: rgba(255,255,255,0.07);
                color: white;
                border: 1px solid rgba(0,212,255,0.25);
                border-radius: 10px;
                padding: 0 16px;
                font-size: 14px;
            }
            QLineEdit:focus { border-color: #00D4FF; background: rgba(0,212,255,0.08); }
        """)
        self.pw_input.returnPressed.connect(self._do_login)
        cl.addWidget(self.pw_input)

        self.err_lbl = QLabel("")
        self.err_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.err_lbl.setStyleSheet("color: #FF3D57; font-size: 12px; background: transparent; border: none;")
        cl.addWidget(self.err_lbl)
        cl.addStretch()

        login_btn = QPushButton("SIGN IN  →")
        login_btn.setFixedHeight(48)
        login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        login_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #00D4FF,stop:1 #7B2FFF);
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 14px;
                font-weight: 600;
                letter-spacing: 2px;
            }
            QPushButton:hover { opacity: 0.85; }
        """)
        login_btn.clicked.connect(self._do_login)
        cl.addWidget(login_btn)

        hint = QLabel("admin / admin123  •  student / student123  •  guest / guest")
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint.setStyleSheet("color: rgba(255,255,255,0.2); font-size: 10px; background: transparent; border: none;")
        cl.addWidget(hint)

        cc.addWidget(card)
        cc.addStretch()
        layout.addLayout(cc)
        layout.addStretch()

        bot = QLabel("NOVA OS v1.0  •  NOVAOS Edition  •  University Project")
        bot.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bot.setStyleSheet("color: rgba(255,255,255,0.2); font-size: 11px;")
        layout.addWidget(bot)
        layout.addSpacing(20)

    def _start_clock(self):
        self._tick()
        t = QTimer(self); t.timeout.connect(self._tick); t.start(1000)

    def _tick(self):
        now = QTime.currentTime(); date = QDate.currentDate()
        self.clock_lbl.setText(f"{date.toString('dddd, MMMM d, yyyy')}   {now.toString('hh:mm:ss AP')}")

    def _do_login(self):
        username = self.user_combo.currentData()
        password = self.pw_input.text()
        if self.state.authenticate(username, password):
            self.state.add_notification("Welcome to NOVAOS!", "⬡")
            desktop = Desktop(self.state)
            desktop.show()
            self.close()
        else:
            self.err_lbl.setText("❌  Incorrect password. Please try again.")
            self.pw_input.clear()
            QTimer.singleShot(2500, lambda: self.err_lbl.setText(""))

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        colors = WALLPAPERS["gradient_nova"]
        g = QLinearGradient(0, 0, self.width(), self.height())
        for i, c in enumerate(colors):
            g.setColorAt(i / max(len(colors) - 1, 1), c)
        p.fillRect(self.rect(), g)


# ═══════════════════════════════════════════════════════════════════════════════
#  DESKTOP ICON
# ═══════════════════════════════════════════════════════════════════════════════
class DesktopIcon(QWidget):
    double_clicked = pyqtSignal(dict)
    right_clicked = pyqtSignal(dict, QPoint)

    def __init__(self, item, parent=None):
        super().__init__(parent)
        self.item = item
        self.selected = False
        self.hovered = False
        self.color = QColor(item.get("color", "#00D4FF"))
        self.setFixedSize(88, 100)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMouseTracking(True)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 8, 6, 6)
        layout.setSpacing(4)

        self.icon_lbl = QLabel(self.item.get("icon", "📄"))
        self.icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_lbl.setStyleSheet("font-size: 30px; background: transparent; border: none;")
        layout.addWidget(self.icon_lbl)

        self.name_lbl = QLabel(self.item.get("name", "App"))
        self.name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_lbl.setWordWrap(True)
        self.name_lbl.setStyleSheet("color: white; font-size: 10px; font-weight: 500; background: transparent; border: none;")
        layout.addWidget(self.name_lbl)

    def mouseDoubleClickEvent(self, e):
        self.double_clicked.emit(self.item)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.selected = True; self.update()
        elif e.button() == Qt.MouseButton.RightButton:
            self.right_clicked.emit(self.item, self.mapToGlobal(e.pos()))

    def mouseReleaseEvent(self, e):
        self.selected = False; self.update()

    def enterEvent(self, e):
        self.hovered = True; self.update()

    def leaveEvent(self, e):
        self.hovered = False; self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = self.rect().adjusted(2, 2, -2, -2)
        icon_r = QRect(r.x() + (r.width()-54)//2, r.y(), 54, 54)

        c = QColor(self.color)
        if self.hovered or self.selected:
            c.setAlpha(80)
        else:
            c.setAlpha(45)
        p.setBrush(QBrush(c))
        border_c = QColor(self.color); border_c.setAlpha(160 if (self.hovered or self.selected) else 90)
        p.setPen(QPen(border_c, 1.5))
        p.drawRoundedRect(icon_r, 14, 14)

        if self.selected:
            sel_c = QColor(self.color); sel_c.setAlpha(40)
            p.setBrush(QBrush(sel_c))
            p.setPen(QPen(QColor(self.color), 1.5))
            p.drawRoundedRect(r, 10, 10)

        super().paintEvent(event)

class VolumePopup(QWidget):
    def __init__(self, state, parent=None):
        super().__init__(parent)
        self.state = state

        self.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(240, 130)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        card = QFrame(self)
        card.setStyleSheet("""
            QFrame {
                background: rgba(10, 16, 30, 245);
                border-radius: 14px;
                border: 1px solid rgba(0,212,255,0.25);
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 212, 255, 80))
        shadow.setOffset(0, 4)
        card.setGraphicsEffect(shadow)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(10)

        # Top row: icon + label + percentage
        top_row = QHBoxLayout()
        top_row.setSpacing(8)

        self._icon_lbl = QLabel()
        self._icon_lbl.setFixedWidth(24)
        self._icon_lbl.setStyleSheet("font-size: 18px; background: transparent; border: none;")
        top_row.addWidget(self._icon_lbl)

        vol_title = QLabel("Volume")
        vol_title.setStyleSheet("color: rgba(255,255,255,0.6); font-size: 12px; background: transparent; border: none;")
        top_row.addWidget(vol_title)
        top_row.addStretch()

        self.pct_lbl = QLabel()
        self.pct_lbl.setStyleSheet("color: #00D4FF; font-size: 14px; font-weight: 700; background: transparent; border: none;")
        top_row.addWidget(self.pct_lbl)

        layout.addLayout(top_row)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(self.state.volume)
        self.slider.setFixedHeight(22)
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 6px;
                background: rgba(255,255,255,0.12);
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: qradialgradient(cx:0.5,cy:0.5,radius:0.5,fx:0.5,fy:0.5,stop:0 white,stop:0.5 #00D4FF,stop:1 rgba(0,212,255,0));
                width: 16px;
                height: 16px;
                margin: -5px 0;
                border-radius: 8px;
            }
            QSlider::sub-page:horizontal {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #7B2FFF,stop:1 #00D4FF);
                border-radius: 3px;
            }
        """)
        self.slider.valueChanged.connect(self._change_volume)
        layout.addWidget(self.slider)

        # Mute toggle row
        mute_row = QHBoxLayout()
        self._mute_btn = QPushButton("Mute")
        self._mute_btn.setFixedHeight(24)
        self._mute_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._mute_btn.setStyleSheet("""
            QPushButton { background: rgba(255,255,255,0.07); color: rgba(255,255,255,0.6);
                          border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; font-size: 11px; padding: 0 10px; }
            QPushButton:hover { background: rgba(255,61,87,0.3); color: white; }
        """)
        self._mute_btn.clicked.connect(self._toggle_mute)
        mute_row.addStretch()
        mute_row.addWidget(self._mute_btn)
        layout.addLayout(mute_row)

        outer.addWidget(card)
        self._prev_vol = self.state.volume
        self._muted = False
        self._update_display(self.state.volume)

    def _vol_icon(self, v):
        if v == 0: return "🔇"
        if v < 35: return "🔈"
        if v < 70: return "🔉"
        return "🔊"

    def _update_display(self, value):
        self._icon_lbl.setText(self._vol_icon(value))
        self.pct_lbl.setText(f"{value}%")

    def _change_volume(self, value):
        self._muted = False
        self._mute_btn.setText("Mute")
        self.state.volume = value
        self.state.save_settings()
        self._update_display(value)
        # Sync taskbar volume button icon
        if hasattr(self.parent(), 'vol_btn'):
            self.parent().vol_btn.setText(self._vol_icon(value))
            self.parent().vol_btn.setToolTip(f"Volume: {value}%")
        # Sync any open SettingsApp windows so they stay in real-time sync
        for w in QApplication.instance().topLevelWidgets():
            for child in w.findChildren(SettingsApp):
                if hasattr(child, 'volume_slider'):
                    child.volume_slider.blockSignals(True)
                    child.volume_slider.setValue(value)
                    child.volume_slider.blockSignals(False)
                child._update_vol_display(value)

    def _toggle_mute(self):
        if self._muted:
            self._muted = False
            self.slider.setValue(self._prev_vol)
            self._mute_btn.setText("Mute")
        else:
            self._prev_vol = self.state.volume
            self._muted = True
            self.slider.setValue(0)
            self._mute_btn.setText("Unmute")

    def showEvent(self, e):
        self.slider.setValue(self.state.volume)
        self._update_display(self.state.volume)
        super().showEvent(e)
# ═══════════════════════════════════════════════════════════════════════════════
#  TASKBAR
# ═══════════════════════════════════════════════════════════════════════════════
class Taskbar(QWidget):
    def __init__(self, state, desktop):
        super().__init__(desktop)
        self.state = state
        self.desktop = desktop
        self.setFixedHeight(52)
        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 6, 10, 6)
        layout.setSpacing(4)

        self.start_btn = QPushButton("⬡  NOVA")
        self.start_btn.setFixedSize(110, 38)
        self.start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.start_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 {self.state.accent_color},stop:1 #7B2FFF);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 13px;
                font-weight: 600;
                letter-spacing: 1px;
            }}
            QPushButton:hover {{ opacity: 0.85; }}
        """)
        self.start_btn.clicked.connect(self.desktop.toggle_start_menu)
        layout.addWidget(self.start_btn)

        layout.addSpacing(4)

        self.search = QLineEdit()
        self.search.setPlaceholderText("🔍  Search apps...")
        self.search.setFixedSize(200, 36)
        self.search.setStyleSheet("""
            QLineEdit {
                background: rgba(255,255,255,0.08);
                color: white;
                border: 1px solid rgba(255,255,255,0.12);
                border-radius: 18px;
                padding: 0 14px;
                font-size: 12px;
            }
            QLineEdit:focus { border-color: #00D4FF; }
        """)
        layout.addWidget(self.search)
        layout.addStretch()

        self.app_bar = QHBoxLayout()
        self.app_bar.setSpacing(2)
        layout.addLayout(self.app_bar)
        layout.addStretch()

        for icon, tip, slot in [
            ("🛜", "WiFi", lambda: self.desktop.open_app("WiFi", "wifi")),
            ("🔊", f"Volume: {self.state.volume}%", self.toggle_volume_popup),            ("🔔", "Notifications", self.desktop.show_notifications),
            ("⚡",  "Power", self.desktop.show_power_menu),
        ]:
            btn = QPushButton(icon)
            btn.setFixedSize(36, 36)
            btn.setToolTip(tip)
            btn.setStyleSheet("""
                QPushButton { background: transparent; color: white; border: none; border-radius: 6px; font-size: 16px; }
                QPushButton:hover { background: rgba(255,255,255,0.1); }
            """)
            if slot: btn.clicked.connect(slot)
            if tip.startswith("Volume"):
                self.vol_btn = btn
            layout.addWidget(btn)

        self.clock_lbl = QLabel("")
        self.clock_lbl.setStyleSheet("color: white; font-size: 12px; min-width: 75px; padding: 0 4px;")
        self.clock_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.clock_lbl)

        t = QTimer(self); t.timeout.connect(self._tick); t.start(5000)
        self._tick()

    def _tick(self):
        now = QTime.currentTime(); date = QDate.currentDate()
        self.clock_lbl.setText(f"{now.toString('hh:mm AP')}\n{date.toString('MM/dd')}")
    def toggle_volume_popup(self):
     if not hasattr(self, "volume_popup"):
        self.volume_popup = VolumePopup(self.state, self)

     btn = self.sender()
     pos = btn.mapToGlobal(btn.rect().bottomLeft())

     self.volume_popup.move(pos.x() - 60, pos.y() - 180)
     self.volume_popup.show()

    def add_app_button(self, name, pid, callback):
        btn = QPushButton(f"  {name[:12]}")
        btn.setFixedSize(130, 36)
        btn.setStyleSheet("""
            QPushButton { background: rgba(0,212,255,0.15); color: white; border: 1px solid rgba(0,212,255,0.3); border-radius: 7px; font-size: 12px; }
            QPushButton:hover { background: rgba(0,212,255,0.25); }
        """)
        btn.clicked.connect(callback)
        btn.setProperty("pid", pid)
        self.app_bar.addWidget(btn)
        return btn

    def remove_app_button(self, pid):
        for i in range(self.app_bar.count()):
            w = self.app_bar.itemAt(i)
            if w and w.widget() and w.widget().property("pid") == pid:
                w.widget().deleteLater()
                break

    def paintEvent(self, event):
        p = QPainter(self)
        p.fillRect(self.rect(), QColor(10, 14, 26, 230))
        p.setPen(QPen(QColor(0, 212, 255, 40), 1))
        p.drawLine(0, 0, self.width(), 0)


# ═══════════════════════════════════════════════════════════════════════════════
#  APP WINDOW
# ═══════════════════════════════════════════════════════════════════════════════
class AppWindow(QWidget):
    closed = pyqtSignal()

    def __init__(self, title, app_type, state, desktop, extra=None):
        super().__init__(desktop, Qt.WindowType.Window)
        self.title = title
        self.app_type = app_type
        self.state = state
        self.desktop = desktop
        self.extra = extra
        self.pid = None
        self._drag_pos = None
        self._maximized = False
        self._restore_geo = None

        w, h = APP_SIZES.get(app_type, (640, 480))
        self.resize(w, h)
        dg = desktop.geometry()
        self.move((dg.width() - w) // 2, (dg.height() - h) // 2 - 26)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.title_bar = QWidget()
        self.title_bar.setFixedHeight(38)
        bg = APP_COLORS.get(self.app_type, "#1a2030")
        self.title_bar.setStyleSheet(f"background: {bg}; border-radius: 12px 12px 0 0; border-bottom: 1px solid rgba(0,212,255,0.15);")
        tb = QHBoxLayout(self.title_bar)
        tb.setContentsMargins(14, 0, 10, 0)
        tb.setSpacing(6)

        self.title_lbl = QLabel(f" {self.title}")
        self.title_lbl.setStyleSheet("color: rgba(255,255,255,0.9); font-size: 13px; font-weight: 500;")
        tb.addWidget(self.title_lbl)
        tb.addStretch()

        for sym, act, hover in [("−", self._minimize, "#555"), ("□", self._toggle_max, "#00D4FF"), ("✕", self._close, "#FF3D57")]:
            btn = QPushButton(sym)
            btn.setFixedSize(28, 24)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{ background: transparent; color: rgba(255,255,255,0.6); border: none; border-radius: 5px; font-size: 13px; }}
                QPushButton:hover {{ background: {hover}; color: white; }}
            """)
            btn.clicked.connect(act)
            tb.addWidget(btn)

        self.title_bar.mousePressEvent = self._title_press
        self.title_bar.mouseMoveEvent = self._title_move
        layout.addWidget(self.title_bar)

        self.content = QWidget()
        self.content.setStyleSheet(f"background: {APP_COLORS.get(self.app_type, '#1a2030')}; border-radius: 0 0 12px 12px;")
        cl = QVBoxLayout(self.content)
        cl.setContentsMargins(0, 0, 0, 0)

        widget = self._get_app_widget()
        if widget:
            cl.addWidget(widget)

        layout.addWidget(self.content, 1)

    def _get_app_widget(self):
        t = self.app_type
        s = self.state
        if t == "terminal":       return TerminalApp(s)
        if t == "file_manager":   return FileManagerApp(s, self.extra)
        if t == "text_editor":    return TextEditorApp(s)
        if t == "calculator":     return CalculatorApp(s)
        if t == "settings":       return SettingsApp(s, self.desktop)
        if t == "task_manager":   return TaskManagerApp(s)
        if t == "recycle_bin":    return RecycleBinApp(s)
        if t == "browser":        return BrowserApp(s)
        if t == "paint":          return PaintApp(s)
        if t == "calendar":       return CalendarApp(s)
        if t == "notes":          return NotesApp(s)
        if t == "about":          return AboutApp(s)
        if t == "io_devices":     return IODevicesApp(s)
        if t == "wifi":           return WiFiApp(s)
        if t == "memory":         return MemoryApp(s)
        return None

    def _title_press(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = e.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def _title_move(self, e):
        if self._drag_pos and e.buttons() == Qt.MouseButton.LeftButton:
            self.move(e.globalPosition().toPoint() - self._drag_pos)

    def _minimize(self):
        self.showMinimized()

    def _toggle_max(self):
        if self._maximized:
            self.setGeometry(self._restore_geo)
            self._maximized = False
        else:
            self._restore_geo = self.geometry()
            dg = self.desktop.geometry()
            self.setGeometry(0, 0, dg.width(), dg.height() - 52)
            self._maximized = True

    def _close(self):
        self.closed.emit()
        self.deleteLater()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setBrush(QBrush(QColor(APP_COLORS.get(self.app_type, "#1a2030"))))
        p.setPen(QPen(QColor(0, 212, 255, 50), 1))
        p.drawRoundedRect(self.rect().adjusted(0, 0, -1, -1), 12, 12)


# ═══════════════════════════════════════════════════════════════════════════════
#  DESKTOP
# ═══════════════════════════════════════════════════════════════════════════════
class Desktop(QWidget):
    def __init__(self, state):
        super().__init__()
        self.state = state
        self.setWindowTitle(" NOVAOS")
        self.setMinimumSize(1366, 768)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.start_menu_widget = None
        self.notif_panel = None
        self._setup_ui()
        
        # Apply saved accent to taskbar
        self.taskbar.start_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 {self.state.accent_color},stop:1 #7B2FFF);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 13px;
                font-weight: 600;
                letter-spacing: 1px;
            }}
            QPushButton:hover {{ opacity: 0.85; }}
        """)

    def _setup_ui(self):
        ml = QVBoxLayout(self)
        ml.setContentsMargins(0, 0, 0, 0)
        ml.setSpacing(0)

        self.desktop_area = QWidget()
        self.desktop_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        ml.addWidget(self.desktop_area, 1)

        self.icon_grid = QGridLayout(self.desktop_area)
        self.icon_grid.setContentsMargins(24, 24, 24, 24)
        self.icon_grid.setSpacing(12)
        self.icon_grid.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.taskbar = Taskbar(self.state, self)
        ml.addWidget(self.taskbar)

        self._load_icons()

    def _load_icons(self):
        while self.icon_grid.count():
            item = self.icon_grid.takeAt(0)
            if item.widget(): item.widget().deleteLater()

        cols = 2
        for i, item in enumerate(DESKTOP_APPS):
            iw = DesktopIcon(item, self.desktop_area)
            iw.double_clicked.connect(self._on_icon_dbl)
            iw.right_clicked.connect(self._on_icon_right)
            row, col = divmod(i, cols)
            self.icon_grid.addWidget(iw, row, col)

    def _on_icon_dbl(self, item):
        self._launch(item.get("action", ""))

    def _on_icon_right(self, item, pos):
        menu = QMenu(self)
        menu.setStyleSheet(self._menu_css())
        menu.addAction(f"Open {item['name']}", lambda: self._launch(item.get("action", "")))
        menu.exec(pos)

    def _launch(self, action):
        if action:
            self.open_app(action.replace("_", " ").title(), action)

    def open_app(self, name, app_type, extra=None):
        # ── Permission check ────────────────────────────────────────────────
        if app_type in ADMIN_ONLY_APPS and self.state.get_role() != "admin":
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Permission Denied")
            dlg.setIcon(QMessageBox.Icon.Critical)
            dlg.setText(
                f"🔒  Permission Denied\n\n"
                f"<b>{name}</b> requires Administrator privileges.\n"
                f"You are logged in as <b>{self.state.get_display_name()}</b> "
                f"({self.state.get_role()}).\n\n"
                f"Please log in as <b>Administrator</b> to access this app."
            )
            dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
            dlg.setStyleSheet("""
                QMessageBox {
                    background: #0F1628;
                    color: white;
                }
                QLabel { color: white; font-size: 13px; }
                QPushButton {
                    background: #FF3D57;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 6px 22px;
                    font-size: 13px;
                }
                QPushButton:hover { background: #cc2f45; }
            """)
            dlg.exec()
            return None
        # ────────────────────────────────────────────────────────────────────

        win = AppWindow(name, app_type, self.state, self, extra)
        win.setParent(self, Qt.WindowType.Window)
        pid = self.state.add_process(name, 128)
        win.pid = pid

        def on_close():
            self.state.remove_process(pid)
            self.taskbar.remove_app_button(pid)
            if name in self.state.open_windows:
                del self.state.open_windows[name]

        win.closed.connect(on_close)
        self.taskbar.add_app_button(name, pid, lambda c=False, w=win: (w.raise_(), w.showNormal()))
        win.show(); win.raise_()
        self.state.open_windows[name] = win
        return win

    def toggle_start_menu(self):
        if self.start_menu_widget and self.start_menu_widget.isVisible():
            self.start_menu_widget.close()
            self.start_menu_widget = None
        else:
            self.start_menu_widget = StartMenu(self.state, self)
            th = self.taskbar.height()
            w, h = 380, 520
            x, y = 8, self.height() - th - h
            self.start_menu_widget.setGeometry(x, y, w, h)
            self.start_menu_widget.show(); self.start_menu_widget.raise_()
            self.start_menu_widget.app_launched.connect(lambda a: (self._launch(a), self.toggle_start_menu()))

    def show_notifications(self):
        if self.notif_panel and self.notif_panel.isVisible():
            self.notif_panel.close(); return
        self.notif_panel = NotificationPanel(self.state, self)
        th = self.taskbar.height()
        w, h = 330, 420
        self.notif_panel.setGeometry(self.width() - w - 10, self.height() - th - h - 10, w, h)
        self.notif_panel.show(); self.notif_panel.raise_()

    def show_power_menu(self):
        pm = PowerMenu(self.state, self)
        pm.exec()

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        menu.setStyleSheet(self._menu_css())
        menu.addAction("🔄 Refresh Desktop", self._load_icons)
        menu.addSeparator()
        menu.addAction("⚙️ Settings", lambda: self.open_app("Settings", "settings"))
        menu.exec(event.globalPos())

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        if self.state.wallpaper.startswith("custom_") and self.state.custom_wallpaper_path and os.path.exists(self.state.custom_wallpaper_path):
            pixmap = QPixmap(self.state.custom_wallpaper_path)
            if not pixmap.isNull():
                scaled = pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
                p.drawPixmap(0, 0, scaled)
                return
        
        colors = WALLPAPERS.get(self.state.wallpaper, WALLPAPERS["gradient_nova"])
        g = QLinearGradient(0, 0, self.width(), self.height())
        for i, c in enumerate(colors):
            g.setColorAt(i / max(len(colors) - 1, 1), c)
        p.fillRect(self.rect(), g)
        
        p.setPen(QPen(QColor(0, 212, 255, 10), 1))
        for x in range(0, self.width(), 60):
            for y in range(0, self.height(), 60):
                p.drawPoint(x, y)

    def _menu_css(self):
        return """
            QMenu {
                background: rgba(10,16,30,0.97);
                color: white;
                border: 1px solid rgba(0,212,255,0.2);
                border-radius: 10px;
                padding: 6px;
                font-size: 13px;
            }
            QMenu::item { padding: 7px 22px 7px 12px; border-radius: 6px; }
            QMenu::item:selected { background: rgba(0,212,255,0.25); }
            QMenu::separator { height: 1px; background: rgba(255,255,255,0.08); margin: 4px 0; }
        """


# ═══════════════════════════════════════════════════════════════════════════════
#  START MENU
# ═══════════════════════════════════════════════════════════════════════════════
class StartMenu(QWidget):
    app_launched = pyqtSignal(str)

    def __init__(self, state, parent=None):
        super().__init__(parent)
        self.state = state
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(50)
        shadow.setColor(QColor(0, 212, 255, 100))
        shadow.setOffset(0, -8)
        self.setGraphicsEffect(shadow)
        
        self._setup_ui()

    def _setup_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: rgba(8, 14, 28, 0.98);
                border-radius: 20px;
                border: 1px solid rgba(0,212,255,0.2);
            }
        """)
        outer.addWidget(card)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        header = QFrame()
        header.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 {self.state.accent_color},stop:1 #7B2FFF);
                border-radius: 12px;
            }}
        """)
        header.setFixedHeight(80)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(16, 0, 16, 0)
        
        avatar = QLabel("👤")
        avatar.setStyleSheet("font-size: 36px; background: transparent; border: none;")
        header_layout.addWidget(avatar)
        
        user_info = QVBoxLayout()
        user_info.setSpacing(2)
        user_name = QLabel(self.state.get_display_name())
        user_name.setStyleSheet("color: white; font-size: 15px; font-weight: 700;")
        user_info.addWidget(user_name)
        user_role = QLabel(self.state.get_role().capitalize())
        user_role.setStyleSheet("color: rgba(255,255,255,0.7); font-size: 11px;")
        user_info.addWidget(user_role)
        header_layout.addLayout(user_info)
        header_layout.addStretch()
        
        layout.addWidget(header)
        
        search = QLineEdit()
        search.setPlaceholderText("🔍  Search apps...")
        search.setFixedHeight(42)
        search.setStyleSheet("""
            QLineEdit {
                background: rgba(0,212,255,0.08);
                color: white;
                border: 1px solid rgba(0,212,255,0.2);
                border-radius: 12px;
                padding: 0 16px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #00D4FF;
                background: rgba(0,212,255,0.12);
            }
        """)
        layout.addWidget(search)
        
        pinned_title = QLabel("PINNED APPS")
        pinned_title.setStyleSheet("color: rgba(0,212,255,0.5); font-size: 10px; letter-spacing: 2px; margin-top: 4px;")
        layout.addWidget(pinned_title)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent; border: none;")
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        grid_widget = QWidget()
        grid_widget.setStyleSheet("background: transparent;")
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setSpacing(8)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        
        for i, (icon, name, action) in enumerate(PINNED_APPS):
            btn = QPushButton()
            btn.setFixedSize(100, 80)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            
            btn_layout = QVBoxLayout(btn)
            btn_layout.setContentsMargins(0, 12, 0, 12)
            btn_layout.setSpacing(4)
            
            icon_lbl = QLabel(icon)
            icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon_lbl.setStyleSheet("font-size: 28px; background: transparent; border: none;")
            btn_layout.addWidget(icon_lbl)
            
            name_lbl = QLabel(name)
            name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            name_lbl.setStyleSheet("color: white; font-size: 10px; background: transparent; border: none;")
            btn_layout.addWidget(name_lbl)
            
            btn.setStyleSheet("""
                QPushButton {
                    background: rgba(0,212,255,0.06);
                    border: 1px solid rgba(0,212,255,0.12);
                    border-radius: 12px;
                }
                QPushButton:hover {
                    background: rgba(0,212,255,0.2);
                    border-color: rgba(0,212,255,0.4);
                }
            """)
            btn.clicked.connect(lambda checked, a=action: self.app_launched.emit(a))
            grid_layout.addWidget(btn, i // 3, i % 3)
        
        scroll.setWidget(grid_widget)
        layout.addWidget(scroll, 1)
        
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background: rgba(0,212,255,0.1); border: none; max-height: 1px;")
        layout.addWidget(sep)
        
        footer = QHBoxLayout()
        footer.setSpacing(8)
        
        power_btn = QPushButton("⚡  Power")
        power_btn.setFixedHeight(38)
        power_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        power_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255,61,87,0.3);
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 12px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: rgba(255,61,87,0.6);
            }
        """)
        power_btn.clicked.connect(self._power)
        footer.addWidget(power_btn)
        
        settings_btn = QPushButton("⚙️  Settings")
        settings_btn.setFixedHeight(38)
        settings_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        settings_btn.setStyleSheet("""
            QPushButton {
                background: rgba(0,212,255,0.2);
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 12px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: rgba(0,212,255,0.4);
            }
        """)
        settings_btn.clicked.connect(lambda: self.app_launched.emit("settings"))
        footer.addWidget(settings_btn)
        
        layout.addLayout(footer)

    def _power(self):
        self.close()
        parent = self.parent()
        while parent and not hasattr(parent, 'show_power_menu'):
            parent = parent.parent()
        if parent:
            parent.show_power_menu()


# ═══════════════════════════════════════════════════════════════════════════════
#  NOTIFICATION PANEL
# ═══════════════════════════════════════════════════════════════════════════════
class NotificationPanel(QWidget):
    def __init__(self, state, parent=None):
        super().__init__(parent)
        self.state = state
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        sh = QGraphicsDropShadowEffect()
        sh.setBlurRadius(30)
        sh.setColor(QColor(0, 0, 0, 160))
        sh.setOffset(-4, 0)
        self.setGraphicsEffect(sh)
        self._setup_ui()

    def _setup_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        card = QFrame()
        card.setStyleSheet("QFrame { background: rgba(8,14,28,0.97); border-radius: 14px; border: 1px solid rgba(0,212,255,0.15); }")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)

        hdr = QHBoxLayout()
        title = QLabel("🔔  Notifications")
        title.setStyleSheet("color: white; font-size: 14px; font-weight: 600;")
        hdr.addWidget(title)
        hdr.addStretch()
        cb = QPushButton("Clear All")
        cb.setFixedHeight(26)
        cb.setStyleSheet("QPushButton { background: rgba(255,255,255,0.08); color: rgba(255,255,255,0.6); border: none; border-radius: 5px; font-size: 11px; padding: 0 10px; } QPushButton:hover { background: rgba(255,255,255,0.15); }")
        cb.clicked.connect(self._clear)
        hdr.addWidget(cb)
        layout.addLayout(hdr)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent; border: none;")
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.nw = QWidget()
        self.nw.setStyleSheet("background: transparent;")
        self.nl = QVBoxLayout(self.nw)
        self.nl.setContentsMargins(0, 0, 0, 0)
        self.nl.setSpacing(6)
        scroll.setWidget(self.nw)
        layout.addWidget(scroll, 1)
        outer.addWidget(card)
        self._populate()

    def _populate(self):
        while self.nl.count():
            item = self.nl.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        notifs = list(reversed(self.state.notifications))
        if not notifs:
            e = QLabel("No notifications")
            e.setAlignment(Qt.AlignmentFlag.AlignCenter)
            e.setStyleSheet("color: rgba(255,255,255,0.3); font-size: 12px; padding: 20px;")
            self.nl.addWidget(e)
        else:
            for n in notifs:
                c = QFrame()
                c.setStyleSheet("QFrame { background: rgba(0,212,255,0.06); border-radius: 8px; border: 1px solid rgba(0,212,255,0.12); }")
                r = QHBoxLayout(c)
                r.setContentsMargins(10, 8, 10, 8)
                r.setSpacing(8)
                il = QLabel(n.get("icon", "ℹ️"))
                il.setStyleSheet("font-size: 16px; background: transparent; border: none;")
                r.addWidget(il)
                ml = QLabel(n.get("msg", ""))
                ml.setStyleSheet("color: rgba(255,255,255,0.8); font-size: 12px; background: transparent; border: none;")
                ml.setWordWrap(True)
                r.addWidget(ml, 1)
                self.nl.addWidget(c)
        self.nl.addStretch()

    def _clear(self):
        self.state.notifications.clear()
        self._populate()


# ═══════════════════════════════════════════════════════════════════════════════
#  POWER MENU (FIXED)
# ═══════════════════════════════════════════════════════════════════════════════
class PowerMenu(QDialog):
    def __init__(self, state, parent=None):
        super().__init__(parent)
        self.state = state
        self.parent_window = parent
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(360, 400)
        self._setup_ui()
        if parent:
            g = parent.geometry()
            self.move(g.x() + (g.width() - self.width()) // 2, g.y() + (g.height() - self.height()) // 2)

    def _setup_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        
        card = QFrame()
        card.setStyleSheet("""
            QFrame { 
                background: rgba(8,14,28,0.98); 
                border-radius: 20px; 
                border: 1px solid rgba(0,212,255,0.25);
            }
        """)
        sh = QGraphicsDropShadowEffect()
        sh.setBlurRadius(50)
        sh.setColor(QColor(0, 0, 0, 200))
        sh.setOffset(0, 8)
        card.setGraphicsEffect(sh)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(12)

        title = QLabel("⚠️  Power Options")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: white; font-size: 18px; font-weight: 700; letter-spacing: 1px;")
        layout.addWidget(title)
        
        sub = QLabel(f"Logged in as: {self.state.get_display_name()}")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub.setStyleSheet("color: rgba(255,255,255,0.5); font-size: 12px;")
        layout.addWidget(sub)
        layout.addSpacing(8)

        for label, color, action in [
            ("🔴  Shut Down", "#FF3D57", self._shutdown),
            ("↺   Restart", "#00D4FF", self._restart),
            ("🚪  Log Out", "#888888", self._logout),
        ]:
            btn = QPushButton(label)
            btn.setFixedHeight(48)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{ 
                    background: rgba(255,255,255,0.06); 
                    color: white; 
                    border: 1px solid rgba(255,255,255,0.1); 
                    border-radius: 12px; 
                    font-size: 14px; 
                    font-weight: 500;
                    text-align: left; 
                    padding-left: 20px;
                }}
                QPushButton:hover {{ 
                    background: {color}; 
                    border-color: transparent;
                }}
            """)
            btn.clicked.connect(action)
            layout.addWidget(btn)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedHeight(38)
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setStyleSheet("""
            QPushButton { 
                background: transparent; 
                color: rgba(255,255,255,0.6); 
                border: 1px solid rgba(255,255,255,0.15);
                border-radius: 10px;
                font-size: 13px;
            } 
            QPushButton:hover { 
                color: white; 
                background: rgba(255,255,255,0.1);
                border-color: rgba(255,255,255,0.3);
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(cancel_btn)
        
        outer.addWidget(card)

    def _shutdown(self):
        reply = QMessageBox.question(self, "Shut Down", "Are you sure you want to shut down?",
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.accept()
            self.state.save_settings()
            QTimer.singleShot(300, QApplication.instance().quit)

    def _restart(self):
     reply = QMessageBox.question(self, "Restart", "Are you sure you want to restart?",
                                  QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
     if reply == QMessageBox.StandardButton.Yes:
        self.accept()
        self.state.save_settings()
        self._do_restart()

    def _do_restart(self):
     global _LOGIN_SCREEN_REF
     self.state.save_settings()

     main_window = None
     for w in QApplication.instance().topLevelWidgets():
        if isinstance(w, Desktop):
            main_window = w
            break

     if main_window:
        main_window.hide()

     self.state.current_user = None

     def after_video():
        global _LOGIN_SCREEN_REF
        if main_window:
            main_window.close()
        _LOGIN_SCREEN_REF = LoginScreen(self.state)
        _LOGIN_SCREEN_REF.show()

     self._video_loading_ref = VideoLoadingScreen(on_complete=after_video)

    def _open_login(self):
        pass

    def _lock(self):
        self.accept()
        self.state.save_settings()
        lock = LockScreen(self.state)
        lock.show()

    def _logout(self):
        reply = QMessageBox.question(self, "Log Out", "Are you sure you want to log out?",
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.accept()
            self._do_logout()

    def _do_logout(self):
        self.state.save_settings()
        self.state.current_user = None
        _show_login(self.state)

    def _open_login_logout(self):
        pass


# ═══════════════════════════════════════════════════════════════════════════════
#  LOCK SCREEN (FIXED)
# ═══════════════════════════════════════════════════════════════════════════════
class LockScreen(QWidget):
    def __init__(self, state):
        super().__init__()
        self.state = state
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.showFullScreen()
        self._setup_ui()
        t = QTimer(self)
        t.timeout.connect(self._tick)
        t.start(1000)
        self._tick()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch(2)
        
        self.clock_lbl = QLabel("")
        self.clock_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.clock_lbl.setFont(QFont("Segoe UI Light", 72))
        self.clock_lbl.setStyleSheet("color: white; background: transparent;")
        layout.addWidget(self.clock_lbl)
        
        self.date_lbl = QLabel("")
        self.date_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.date_lbl.setStyleSheet("color: rgba(255,255,255,0.6); font-size: 18px; font-weight: 300; letter-spacing: 2px;")
        layout.addWidget(self.date_lbl)
        layout.addStretch(1)
        
        ch = QHBoxLayout()
        ch.addStretch()
        
        card = QFrame()
        card.setFixedSize(340, 220)
        card.setStyleSheet("""
            QFrame { 
                background: rgba(8,14,28,0.95); 
                border-radius: 18px; 
                border: 1px solid rgba(0,212,255,0.3);
            }
        """)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 212, 255, 80))
        shadow.setOffset(0, 5)
        card.setGraphicsEffect(shadow)
        
        cl = QVBoxLayout(card)
        cl.setContentsMargins(28, 22, 28, 22)
        cl.setSpacing(12)
        
        ul = QLabel(self.state.get_display_name())
        ul.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ul.setStyleSheet("color: white; font-size: 16px; font-weight: 600; background: transparent; border: none;")
        cl.addWidget(ul)
        
        self.pi = QLineEdit()
        self.pi.setEchoMode(QLineEdit.EchoMode.Password)
        self.pi.setPlaceholderText("Enter password to unlock...")
        self.pi.setFixedHeight(44)
        self.pi.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pi.setStyleSheet("""
            QLineEdit { 
                background: rgba(255,255,255,0.1); 
                color: white; 
                border: 1px solid rgba(0,212,255,0.4); 
                border-radius: 10px; 
                padding: 0 14px; 
                font-size: 13px;
            } 
            QLineEdit:focus { 
                border-color: #00D4FF; 
                background: rgba(0,212,255,0.1);
            }
        """)
        self.pi.returnPressed.connect(self._unlock)
        cl.addWidget(self.pi)
        
        ub = QPushButton("Unlock →")
        ub.setFixedHeight(40)
        ub.setCursor(Qt.CursorShape.PointingHandCursor)
        ub.setStyleSheet("""
            QPushButton { 
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #00D4FF,stop:1 #7B2FFF); 
                color: white; 
                border: none; 
                border-radius: 10px; 
                font-size: 14px; 
                font-weight: 600;
            } 
            QPushButton:hover { opacity: 0.85; }
        """)
        ub.clicked.connect(self._unlock)
        cl.addWidget(ub)
        
        self.el = QLabel("")
        self.el.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.el.setStyleSheet("color: #FF3D57; font-size: 11px; background: transparent; border: none;")
        cl.addWidget(self.el)
        
        ch.addWidget(card)
        ch.addStretch()
        layout.addLayout(ch)
        layout.addStretch(2)
        
        QTimer.singleShot(100, self.pi.setFocus)

    def _tick(self):
        self.clock_lbl.setText(QTime.currentTime().toString("hh:mm"))
        self.date_lbl.setText(QDate.currentDate().toString("dddd, MMMM d"))

    def _unlock(self):
        pw = self.pi.text()
        user = self.state.users.get(self.state.current_user, {})
        if user.get("password") == pw:
            self.close()
        else:
            self.el.setText("❌ Incorrect password")
            self.pi.clear()
            QTimer.singleShot(2000, lambda: self.el.setText(""))
            self.pi.setFocus()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        super().keyPressEvent(event)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        if self.state.custom_wallpaper_path and os.path.exists(self.state.custom_wallpaper_path):
            pixmap = QPixmap(self.state.custom_wallpaper_path)
            if not pixmap.isNull():
                scaled = pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
                p.drawPixmap(0, 0, scaled)
                p.setBrush(QBrush(QColor(0, 0, 0, 100)))
                p.drawRect(self.rect())
                return
        
        colors = WALLPAPERS.get(self.state.wallpaper, WALLPAPERS["gradient_nova"])
        g = QLinearGradient(0, 0, self.width(), self.height())
        for i, c in enumerate(colors):
            g.setColorAt(i / max(len(colors)-1, 1), c)
        p.fillRect(self.rect(), g)


# ═══════════════════════════════════════════════════════════════════════════════
#  TERMINAL APP
# ═══════════════════════════════════════════════════════════════════════════════
class TerminalApp(QWidget):
    def __init__(self, state):
        super().__init__()
        self.state = state
        self.history = []
        self.hist_idx = 0
        self.cwd = Path(os.path.expanduser("~"))
        self._setup_ui()
        self._print_welcome()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: #060A15;
                border-radius: 8px;
                border: 1px solid rgba(0,212,255,0.15);
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(0)

        self.terminal = QTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setFont(QFont("Courier New", 11))
        self.terminal.setStyleSheet("""
            QTextEdit {
                background: #060A15;
                color: #00FF88;
                border: none;
                padding: 12px;
            }
            QScrollBar:vertical {
                background: #0F1628;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #1C2A47;
                border-radius: 4px;
            }
        """)
        card_layout.addWidget(self.terminal, 1)

        input_frame = QFrame()
        input_frame.setStyleSheet("background: transparent;")
        input_frame.setFixedHeight(46)
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(12, 6, 12, 6)
        input_layout.setSpacing(8)

        self.prompt_lbl = QLabel()
        self.prompt_lbl.setFont(QFont("Courier New", 11))
        self.prompt_lbl.setStyleSheet("color: #00D4FF; background: transparent;")
        input_layout.addWidget(self.prompt_lbl)

        self.cmd_entry = QLineEdit()
        self.cmd_entry.setFont(QFont("Courier New", 11))
        self.cmd_entry.setStyleSheet("""
            QLineEdit {
                background: #060A15;
                color: #00FF88;
                border: 1px solid rgba(0,212,255,0.3);
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 11px;
            }
            QLineEdit:focus {
                border-color: #00D4FF;
            }
        """)
        self.cmd_entry.returnPressed.connect(self._run_command)
        self.cmd_entry.installEventFilter(self)
        input_layout.addWidget(self.cmd_entry, 1)

        run_btn = QPushButton("▶ Run")
        run_btn.setFixedSize(70, 32)
        run_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        run_btn.setStyleSheet("""
            QPushButton {
                background: rgba(0,212,255,0.2);
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 11px;
            }
            QPushButton:hover { background: rgba(0,212,255,0.4); }
        """)
        run_btn.clicked.connect(self._run_command)
        input_layout.addWidget(run_btn)

        clear_btn = QPushButton("Clear")
        clear_btn.setFixedSize(60, 32)
        clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        clear_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255,61,87,0.2);
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 11px;
            }
            QPushButton:hover { background: rgba(255,61,87,0.4); }
        """)
        clear_btn.clicked.connect(self._clear)
        input_layout.addWidget(clear_btn)

        card_layout.addWidget(input_frame)
        layout.addWidget(card, 1)

        self._update_prompt()

    def _update_prompt(self):
        short = str(self.cwd).replace(str(Path.home()), "~")
        self.prompt_lbl.setText(f"nova@os:{short}$ ")

    def _print_welcome(self):
        self._print("╔══════════════════════════════════════════╗", "#00D4FF")
        self._print("║        NOVA OS Terminal  v1.0            ║", "#00D4FF")
        self._print("╚══════════════════════════════════════════╝", "#00D4FF")
        self._print(f"Logged in as: {self.state.current_user or 'user'}", "#6B7FA3")
        self._print('Type "help" for commands.\n', "#6B7FA3")

    def _print(self, text, color="#00FF88"):
        self.terminal.setTextColor(QColor(color))
        self.terminal.append(text)
        self.terminal.ensureCursorVisible()

    def _clear(self):
        self.terminal.clear()
        self._print_welcome()

    def _run_command(self):
        cmd = self.cmd_entry.text().strip()
        if not cmd:
            return
        
        self.history.append(cmd)
        self.hist_idx = len(self.history)
        self.cmd_entry.clear()
        
        short = str(self.cwd).replace(str(Path.home()), "~")
        self._print(f"\nnova@os:{short}$ {cmd}", "#00D4FF")
        
        self._execute(cmd)
        self._update_prompt()

    def _execute(self, line):
        parts = line.split()
        cmd = parts[0].lower() if parts else ""
        args = parts[1:]
        
        pm = self.state.pm
        mm = self.state.mm
        io = self.state.io

        if cmd == "help":
            self._print("  File Ops:   ls [path]  cd <path>  mkdir <n>  touch <f>  rm <f>  cat <f>  pwd  tree", "#00D4FF")
            self._print("              cp <src> <dst>  mv <src> <dst>  echo <text>", "#00D4FF")
            self._print("  Process:    ps  spawn <n>  kill <pid>  suspend <pid>  resume <pid>", "#7B2FFF")
            self._print("  Memory:     mem  memalloc <n> <mb>  memfree <n>  memmap", "#00E676")
            self._print("  I/O:        lsdev  devlog", "#FFB300")
            self._print("  System:     uname  date  sysinfo  df  clear  whoami", "#6B7FA3")
        elif cmd == "ls":
            target = self.cwd / args[0] if args else self.cwd
            try:
                entries = sorted(target.iterdir(), key=lambda e: (not e.is_dir(), e.name.lower()))
                for e in entries:
                    icon = "📁" if e.is_dir() else file_icon(str(e))
                    sz = f"  [{fmt_size(e.stat().st_size)}]" if e.is_file() else ""
                    self._print(f"  {icon}  {e.name}{sz}")
                if not entries:
                    self._print("  (empty)")
            except Exception as ex:
                self._print(f"Error: {ex}", "#FF3D57")
        elif cmd == "cd":
            target = (self.cwd / args[0]).resolve() if args else Path.home()
            if target.is_dir():
                self.cwd = target
                self._print(f"Changed to {target}", "#00E676")
            else:
                self._print("Error: not a directory", "#FF3D57")
        elif cmd == "pwd":
            self._print(str(self.cwd))
        elif cmd == "mkdir":
            if args:
                try:
                    (self.cwd / args[0]).mkdir(exist_ok=True)
                    self._print(f"Directory '{args[0]}' created.", "#00E676")
                except Exception as ex:
                    self._print(f"Error: {ex}", "#FF3D57")
            else:
                self._print("Usage: mkdir <name>", "#FFB300")
        elif cmd == "touch":
            if args:
                try:
                    (self.cwd / args[0]).touch()
                    self._print(f"File '{args[0]}' created.", "#00E676")
                except Exception as ex:
                    self._print(f"Error: {ex}", "#FF3D57")
            else:
                self._print("Usage: touch <file>", "#FFB300")
        elif cmd == "cat":
            if args:
                try:
                    content = (self.cwd / args[0]).read_text(encoding="utf-8", errors="ignore")
                    self._print(content[:2000])
                except Exception as ex:
                    self._print(f"Error: {ex}", "#FF3D57")
            else:
                self._print("Usage: cat <file>", "#FFB300")
        elif cmd == "rm":
            if args:
                try:
                    p = self.cwd / args[0]
                    if p.is_dir():
                        shutil.rmtree(p)
                    else:
                        p.unlink()
                    self._print(f"'{args[0]}' removed.", "#FFB300")
                except Exception as ex:
                    self._print(f"Error: {ex}", "#FF3D57")
            else:
                self._print("Usage: rm <name>", "#FFB300")
        elif cmd == "cp":
            if len(args) >= 2:
                try:
                    shutil.copy2(self.cwd / args[0], self.cwd / args[1])
                    self._print("Copied.", "#00E676")
                except Exception as ex:
                    self._print(f"Error: {ex}", "#FF3D57")
            else:
                self._print("Usage: cp <src> <dst>", "#FFB300")
        elif cmd == "mv":
            if len(args) >= 2:
                try:
                    (self.cwd / args[0]).rename(self.cwd / args[1])
                    self._print("Moved.", "#00E676")
                except Exception as ex:
                    self._print(f"Error: {ex}", "#FF3D57")
            else:
                self._print("Usage: mv <src> <dst>", "#FFB300")
        elif cmd == "tree":
            lines = []
            def walk(p, pre=""):
                try:
                    items = sorted(p.iterdir(), key=lambda e: (not e.is_dir(), e.name.lower()))
                    for i, e in enumerate(items):
                        c = "└── " if i == len(items)-1 else "├── "
                        lines.append(pre + c + file_icon(str(e)) + " " + e.name)
                        if e.is_dir():
                            walk(e, pre + ("    " if i == len(items)-1 else "│   "))
                except:
                    lines.append(pre + "  [permission denied]")
            self._print(str(self.cwd))
            walk(self.cwd)
            self._print("\n".join(lines[:150]))
        elif cmd == "echo":
            self._print(" ".join(args))
        elif cmd == "ps":
            self._print(f"{'PID':<8}{'Name':<25}{'State':<12}{'CPU%':<8}{'MEM%':<8}{'Type'}", "#00D4FF")
            self._print("─" * 70, "#1C2A47")
            for p in sorted(pm.all_processes(), key=lambda x: x["pid"])[:50]:
                self._print(f"{p['pid']:<8}{p['name']:<25}{p['state']:<12}{p['cpu']:<8.1f}{p['mem']:<8.2f}custom")
        elif cmd == "spawn":
            if args:
                pid = pm.spawn(args[0])
                self._print(f"'{args[0]}' spawned as PID {pid}.", "#00E676")
            else:
                self._print("Usage: spawn <name>", "#FFB300")
        elif cmd == "kill":
            if args:
                self._print(pm.kill_custom(int(args[0])), "#FFB300")
            else:
                self._print("Usage: kill <pid>", "#FFB300")
        elif cmd == "suspend":
            if args:
                self._print(pm.suspend_custom(int(args[0])), "#FFB300")
            else:
                self._print("Usage: suspend <pid>", "#FFB300")
        elif cmd == "resume":
            if args:
                self._print(pm.resume_custom(int(args[0])), "#00E676")
            else:
                self._print("Usage: resume <pid>", "#FFB300")
        elif cmd == "mem":
            vm = psutil.virtual_memory()
            self._print("=== Real RAM ===", "#00D4FF")
            self._print(f"Total: {fmt_size(vm.total)}  Used: {fmt_size(vm.used)}  Free: {fmt_size(vm.available)}  Usage: {vm.percent}%")
            self._print("=== Simulated ===", "#7B2FFF")
            self._print(f"Total: {mm.total} MB  Used: {mm.used_mb} MB  Free: {mm.free_mb} MB  Usage: {mm.pct:.1f}%")
        elif cmd == "memalloc":
            if len(args) >= 2:
                _, msg = mm.allocate(args[0], int(args[1]))
                self._print(msg, "#00E676")
            else:
                self._print("Usage: memalloc <name> <mb>", "#FFB300")
        elif cmd == "memfree":
            if args:
                self._print(mm.free(args[0]), "#FFB300")
            else:
                self._print("Usage: memfree <name>", "#FFB300")
        elif cmd == "memmap":
            self._print(f"Pages: {len(mm.pages)} | Used: {sum(1 for p in mm.pages if p)} | Free: {sum(1 for p in mm.pages if not p)}", "#7B2FFF")
            for n, v in mm.allocs.items():
                self._print(f"  {n}: {len(v)} pages = {len(v)*4} MB")
        elif cmd == "lsdev":
            self._print(f"{'Device':<14}{'Type':<12}{'Port':<12}{'Driver':<16}{'Connected'}", "#00D4FF")
            self._print("─" * 60, "#1C2A47")
            for n, d in {**io.INPUT_DEVICES, **io.OUTPUT_DEVICES}.items():
                conn = "✅" if io.connected.get(n, False) else "⛔"
                self._print(f"{n:<14}{d['type']:<12}{d['port']:<12}{d['driver']:<16}{conn}")
        elif cmd == "uname":
            self._print(f"NOVA OS v1.0   NOVAOS Edition  {platform.machine()}  {platform.system()} {platform.release()}")
        elif cmd == "date":
            self._print(datetime.now().strftime("%A %d %B %Y  %H:%M:%S"))
        elif cmd == "whoami":
            self._print(self.state.current_user or "unknown", "#00E676")
        elif cmd == "df":
            for part in psutil.disk_partitions():
                try:
                    u = psutil.disk_usage(part.mountpoint)
                    self._print(f"{part.device:<20} {fmt_size(u.total):<12} {fmt_size(u.used):<12} {fmt_size(u.free):<12} {u.percent}%")
                except:
                    pass
        elif cmd == "sysinfo":
            vm = psutil.virtual_memory()
            self._print(f"Host: {platform.node()}  OS: {platform.system()} {platform.release()}", "#00D4FF")
            self._print(f"CPU: {psutil.cpu_count()} cores @ {psutil.cpu_percent():.0f}%  RAM: {fmt_size(vm.total)} ({vm.percent}% used)")
            self._print(f"User: {self.state.get_display_name()} ({self.state.current_user})")
        elif cmd == "clear":
            self._clear()
        elif cmd == "exit":
            self._print("Use the window close button to exit.", "#FFB300")
        else:
            self._print(f"nova: command not found: {cmd}  (type 'help')", "#FF3D57")

    def eventFilter(self, obj, event):
        if obj == self.cmd_entry and event.type() == QEvent.Type.KeyPress:
            key = event.key()
            if key == Qt.Key.Key_Up:
                if self.hist_idx > 0:
                    self.hist_idx -= 1
                    self.cmd_entry.setText(self.history[self.hist_idx])
                return True
            elif key == Qt.Key.Key_Down:
                if self.hist_idx < len(self.history) - 1:
                    self.hist_idx += 1
                    self.cmd_entry.setText(self.history[self.hist_idx])
                else:
                    self.hist_idx = len(self.history)
                    self.cmd_entry.clear()
                return True
        return super().eventFilter(obj, event)


# ═══════════════════════════════════════════════════════════════════════════════
#  TASK MANAGER APP
# ═══════════════════════════════════════════════════════════════════════════════
class TaskManagerApp(QWidget):
    def __init__(self, state):
        super().__init__()
        self.state = state
        self.process_rows = {}
        self._setup_ui()
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self._refresh)
        self.refresh_timer.start(3000)
        self._refresh()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        # Header
        header = QHBoxLayout()
        title = QLabel("📊  Task Manager")
        title.setStyleSheet("color: white; font-size: 15px; font-weight: 700;")
        header.addWidget(title)
        header.addStretch()
        
        self.status_lbl = QLabel("")
        self.status_lbl.setStyleSheet("color: rgba(255,255,255,0.4); font-size: 11px;")
        header.addWidget(self.status_lbl)
        layout.addLayout(header)

        # Warning label for simulated processes only
        warning = QFrame()
        warning.setStyleSheet("background: rgba(0,212,255,0.1); border-radius: 6px; border: 1px solid rgba(0,212,255,0.2);")
        warning_layout = QHBoxLayout(warning)
        warning_layout.setContentsMargins(10, 5, 10, 5)
        warning_icon = QLabel("ℹ️")
        warning_icon.setStyleSheet("font-size: 14px; background: transparent; border: none;")
        warning_layout.addWidget(warning_icon)
        warning_text = QLabel("Showing simulated processes only. Check the box below to view real OS processes.")
        warning_text.setStyleSheet("color: #00D4FF; font-size: 11px; background: transparent; border: none;")
        warning_layout.addWidget(warning_text)
        warning_layout.addStretch()
        layout.addWidget(warning)

        # Toolbar
        toolbar = QHBoxLayout()
        toolbar.setSpacing(6)
        
        self.search_var = QLineEdit()
        self.search_var.setPlaceholderText("🔍 Filter processes...")
        self.search_var.setFixedHeight(30)
        self.search_var.setStyleSheet("QLineEdit { background: rgba(255,255,255,0.07); color: white; border: 1px solid rgba(0,212,255,0.2); border-radius: 6px; padding: 0 10px; font-size: 12px; }")
        self.search_var.textChanged.connect(self._refresh)
        toolbar.addWidget(self.search_var, 1)
        
        # Checkbox for showing real processes (OFF by default)
        self.show_real = QCheckBox("Show real OS processes (⚠️ read-only)")
        self.show_real.setChecked(False)  # Default to FALSE - only show simulated
        self.show_real.setStyleSheet("color: rgba(255,255,255,0.6); font-size: 11px;")
        self.show_real.stateChanged.connect(self._refresh)
        toolbar.addWidget(self.show_real)
        
        # Action buttons (only affect simulated processes)
        for text, color, slot in [
            ("➕ Spawn", "#7B2FFF", self._spawn),
            ("💀 Kill", "#FF3D57", self._kill),
            ("⏸ Suspend", "#FFB300", self._suspend),
            ("▶ Resume", "#00E676", self._resume),
        ]:
            btn = QPushButton(text)
            btn.setFixedSize(75, 28)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(f"QPushButton {{ background: {color}; color: white; border: none; border-radius: 5px; font-size: 11px; }} QPushButton:hover {{ opacity: 0.85; }}")
            btn.clicked.connect(slot)
            toolbar.addWidget(btn)
        
        layout.addLayout(toolbar)

        # Table header
        header_frame = QFrame()
        header_frame.setFixedHeight(28)
        header_frame.setStyleSheet("background: rgba(0,212,255,0.08); border-radius: 5px;")
        hl = QHBoxLayout(header_frame)
        hl.setContentsMargins(10, 0, 10, 0)
        
        for text, w in [("PID", 60), ("Name", 180), ("State", 90), ("CPU%", 55), ("MEM%", 55), ("Type", 70)]:
            lbl = QLabel(text)
            lbl.setStyleSheet("color: #00D4FF; font-size: 10px; font-weight: 700;")
            lbl.setFixedWidth(w)
            hl.addWidget(lbl)
        
        layout.addWidget(header_frame)

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent; border: none;")
        
        self.container = QWidget()
        self.container.setStyleSheet("background: transparent;")
        self.process_layout = QVBoxLayout(self.container)
        self.process_layout.setContentsMargins(0, 0, 0, 0)
        self.process_layout.setSpacing(1)
        
        scroll.setWidget(self.container)
        layout.addWidget(scroll, 1)
        
        # Performance bar
        perf_frame = QFrame()
        perf_frame.setFixedHeight(50)
        perf_frame.setStyleSheet("background: rgba(15,22,40,0.8); border-radius: 6px; margin-top: 5px;")
        perf_layout = QHBoxLayout(perf_frame)
        perf_layout.setContentsMargins(10, 5, 10, 5)
        
        self.cpu_bar = QProgressBar()
        self.cpu_bar.setRange(0, 100)
        self.cpu_bar.setFixedHeight(8)
        self.cpu_bar.setTextVisible(False)
        self.cpu_bar.setStyleSheet("QProgressBar { background: rgba(255,255,255,0.08); border-radius: 4px; } QProgressBar::chunk { background: #00D4FF; border-radius: 4px; }")
        perf_layout.addWidget(QLabel("CPU:"))
        perf_layout.addWidget(self.cpu_bar, 1)
        
        self.ram_bar = QProgressBar()
        self.ram_bar.setRange(0, 100)
        self.ram_bar.setFixedHeight(8)
        self.ram_bar.setTextVisible(False)
        self.ram_bar.setStyleSheet("QProgressBar { background: rgba(255,255,255,0.08); border-radius: 4px; } QProgressBar::chunk { background: #7B2FFF; border-radius: 4px; }")
        perf_layout.addWidget(QLabel("RAM:"))
        perf_layout.addWidget(self.ram_bar, 1)
        
        self.perf_lbl = QLabel("")
        self.perf_lbl.setStyleSheet("color: rgba(255,255,255,0.4); font-size: 10px; min-width: 80px;")
        perf_layout.addWidget(self.perf_lbl)
        
        layout.addWidget(perf_frame)

    def _refresh(self):
        search = self.search_var.text().lower()
        
        # Get processes based on checkbox state
        if self.show_real.isChecked():
            # Show real OS processes + simulated
            all_processes = self._get_all_processes()
        else:
            # Show ONLY simulated processes (default)
            all_processes = self.state.pm.all_processes()
        
        if search:
            all_processes = [p for p in all_processes if search in p["name"].lower() or search in str(p["pid"])]
        
        # Sort by CPU usage
        all_processes = sorted(all_processes, key=lambda x: x.get("cpu", 0), reverse=True)
        
        current_pids = set()
        
        # Update existing rows
        for p in all_processes:
            pid = p["pid"]
            current_pids.add(pid)
            
            if pid in self.process_rows:
                # Update existing row
                row_widgets = self.process_rows[pid]
                state = p.get("state", "unknown")
                state_color = "#00E676" if "run" in state else ("#FFB300" if "sleep" in state or state == "suspended" else "#FF3D57")
                row_widgets["state"].setText(state[:10])
                row_widgets["state"].setStyleSheet(f"color: {state_color}; font-size: 11px;")
                row_widgets["cpu"].setText(f"{p.get('cpu', 0):.1f}%")
                row_widgets["mem"].setText(f"{p.get('mem', 0):.1f}%")
            else:
                # Add new row
                self._add_process_row(p)
        
        # Remove rows for processes that no longer exist
        for pid in list(self.process_rows.keys()):
            if pid not in current_pids:
                row = self.process_rows[pid]["row"]
                self.process_layout.removeWidget(row)
                row.deleteLater()
                del self.process_rows[pid]
        
        # Update status
        sim_count = len(self.state.pm.all_processes())
        if self.show_real.isChecked():
            self.status_lbl.setText(f"📊 {len(all_processes)} total processes ({sim_count} simulated)")
        else:
            self.status_lbl.setText(f"📊 {len(all_processes)} simulated processes (check box to see real OS processes)")
        
        # Update performance
        self._update_performance()

    def _get_all_processes(self):
        """Get both real OS processes and simulated processes"""
        result = []
        
        # Get real OS processes
        try:
            for p in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_percent']):
                try:
                    info = p.info
                    result.append({
                        "pid": info['pid'],
                        "name": (info['name'] or "?")[:22],
                        "state": info['status'] or "running",
                        "cpu": round(info['cpu_percent'] or 0, 1),
                        "mem": round(info['memory_percent'] or 0, 2),
                        "real": True,
                    })
                except:
                    pass
        except:
            pass
        
        # Add simulated processes
        for p in self.state.pm.all_processes():
            result.append(p)
        
        return result

    def _add_process_row(self, p):
        row = QFrame()
        row.setFixedHeight(30)
        
        # Different styling based on whether it's real or simulated
        is_real = p.get("real", False)
        if is_real:
            row.setStyleSheet("QFrame { background: rgba(50,30,30,0.4); border-radius: 4px; } QFrame:hover { background: rgba(255,61,87,0.1); }")
        else:
            row.setStyleSheet("QFrame { background: rgba(20,30,53,0.5); border-radius: 4px; } QFrame:hover { background: rgba(0,212,255,0.1); }")
        
        rl = QHBoxLayout(row)
        rl.setContentsMargins(10, 0, 10, 0)
        rl.setSpacing(0)
        
        state = p.get("state", "unknown")
        state_color = "#00E676" if "run" in state else ("#FFB300" if "sleep" in state or state == "suspended" else "#FF3D57")
        
        # PID - different color for real vs simulated
        pid_lbl = QLabel(str(p["pid"]))
        pid_lbl.setFixedWidth(60)
        if is_real:
            pid_lbl.setStyleSheet("color: #FF6B9D; font-size: 11px; font-family: monospace;")
        else:
            pid_lbl.setStyleSheet("color: #00D4FF; font-size: 11px; font-family: monospace; font-weight: bold;")
        rl.addWidget(pid_lbl)
        
        # Name
        name_lbl = QLabel(p["name"])
        name_lbl.setFixedWidth(180)
        name_lbl.setStyleSheet("color: white; font-size: 11px;")
        rl.addWidget(name_lbl)
        
        # State
        state_lbl = QLabel(state[:10])
        state_lbl.setFixedWidth(90)
        state_lbl.setStyleSheet(f"color: {state_color}; font-size: 11px;")
        rl.addWidget(state_lbl)
        
        # CPU%
        cpu_lbl = QLabel(f"{p.get('cpu', 0):.1f}%")
        cpu_lbl.setFixedWidth(55)
        cpu_lbl.setStyleSheet("color: #00D4FF; font-size: 11px; font-family: monospace;")
        rl.addWidget(cpu_lbl)
        
        # MEM%
        mem_lbl = QLabel(f"{p.get('mem', 0):.1f}%")
        mem_lbl.setFixedWidth(55)
        mem_lbl.setStyleSheet("color: #7B2FFF; font-size: 11px; font-family: monospace;")
        rl.addWidget(mem_lbl)
        
        # Type
        if is_real:
            type_lbl = QLabel("system")
            type_lbl.setFixedWidth(70)
            type_lbl.setStyleSheet("color: #FF6B9D; font-size: 11px;")
        else:
            type_lbl = QLabel("simulated")
            type_lbl.setFixedWidth(70)
            type_lbl.setStyleSheet("color: #00D4FF; font-size: 11px;")
        rl.addWidget(type_lbl)
        
        self.process_layout.addWidget(row)
        self.process_rows[p["pid"]] = {
            "row": row, "state": state_lbl, "cpu": cpu_lbl, "mem": mem_lbl
        }

    def _update_performance(self):
        try:
            cpu = psutil.cpu_percent()
            mem = psutil.virtual_memory()
            self.cpu_bar.setValue(int(cpu))
            self.ram_bar.setValue(int(mem.percent))
            self.perf_lbl.setText(f"CPU: {cpu:.0f}%  RAM: {mem.percent:.0f}%")
        except:
            pass

    def _spawn(self):
        name, ok = QInputDialog.getText(self, "Spawn Simulated Process", "Process name:")
        if ok and name.strip():
            pid = self.state.pm.spawn(name.strip())
            QMessageBox.information(self, "Spawned", f"✅ Simulated process '{name.strip()}' started with PID {pid}")
            self._refresh()

    def _kill(self):
        pid, ok = QInputDialog.getInt(self, "Kill Simulated Process", "Enter simulated PID:", min=1)
        if ok:
            result = self.state.pm.kill_custom(pid)
            if "terminated" in result:
                QMessageBox.information(self, "Killed", f"✅ {result}")
            else:
                msg = QMessageBox(self)
                msg.setWindowTitle("Protected")
                msg.setText("❌ Cannot kill real OS processes!\n\nOnly simulated processes (PID ≥ 9000) can be resumed.")
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setStyleSheet("QMessageBox { background-color: #0F1628; color: white; } QMessageBox QLabel { color: white; }")
                msg.exec()
                self._refresh()

    def _suspend(self):
        pid, ok = QInputDialog.getInt(self, "Suspend Simulated Process", "Enter simulated PID:", min=1)
        if ok:
            result = self.state.pm.suspend_custom(pid)
            if "suspended" in result:
                QMessageBox.information(self, "Suspended", f"✅ {result}")
            else:
                msg = QMessageBox(self)
                msg.setWindowTitle("Protected")
                msg.setText("❌ Cannot suspend real OS processes!\n\nOnly simulated processes (PID ≥ 9000) can be resumed.")
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setStyleSheet("QMessageBox { background-color: #0F1628; color: white; } QMessageBox QLabel { color: white; }")
                msg.exec()
                self._refresh()

    def _resume(self):
        pid, ok = QInputDialog.getInt(self, "Resume Simulated Process", "Enter simulated PID:", min=1)
        if ok:
            result = self.state.pm.resume_custom(pid)
            if "resumed" in result:
                QMessageBox.information(self, "Resumed", f"✅ {result}")
            else:
                msg = QMessageBox(self)
                msg.setWindowTitle("Protected")
                msg.setText("❌ Cannot resume real OS processes!\n\nOnly simulated processes (PID ≥ 9000) can be resumed.")
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setStyleSheet("QMessageBox { background-color: #0F1628; color: white; } QMessageBox QLabel { color: white; }")
                msg.exec()
                self._refresh()

# ═══════════════════════════════════════════════════════════════════════════════
#  MEMORY APP
# ═══════════════════════════════════════════════════════════════════════════════
class MemoryApp(QWidget):
    def __init__(self, state):
        super().__init__()
        self.state = state
        self._setup_ui()
        t = QTimer(self)
        t.timeout.connect(self._refresh)
        t.start(3000)
        self._refresh()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        top = QHBoxLayout()
        top.setSpacing(10)

        rc = self._card("Real System RAM")
        top.addWidget(rc, 1)
        rcl = QVBoxLayout()
        rcl.setContentsMargins(14, 4, 14, 10)
        rcl.setSpacing(4)
        self.real_labels = {}
        for k in ["Total", "Used", "Free", "Usage%"]:
            r = QHBoxLayout()
            kl = QLabel(k)
            kl.setStyleSheet("color: rgba(255,255,255,0.5); font-size: 11px;")
            kl.setFixedWidth(65)
            r.addWidget(kl)
            vl = QLabel("–")
            vl.setStyleSheet("color: #00D4FF; font-size: 12px; font-weight: 600;")
            r.addWidget(vl)
            rcl.addLayout(r)
            self.real_labels[k] = vl
        self.real_bar = QProgressBar()
        self.real_bar.setFixedHeight(10)
        self.real_bar.setTextVisible(False)
        self.real_bar.setStyleSheet("QProgressBar { background: rgba(255,255,255,0.08); border-radius: 5px; border: none; } QProgressBar::chunk { background: #00D4FF; border-radius: 5px; }")
        rcl.addWidget(self.real_bar)
        rc.layout().addLayout(rcl)

        sc = self._card("Simulated RAM (2048 MB)")
        top.addWidget(sc, 1)
        scl = QVBoxLayout()
        scl.setContentsMargins(14, 4, 14, 10)
        scl.setSpacing(4)
        self.sim_labels = {}
        for k in ["Total", "Used", "Free", "Usage%"]:
            r = QHBoxLayout()
            kl = QLabel(k)
            kl.setStyleSheet("color: rgba(255,255,255,0.5); font-size: 11px;")
            kl.setFixedWidth(65)
            r.addWidget(kl)
            vl = QLabel("–")
            vl.setStyleSheet("color: #7B2FFF; font-size: 12px; font-weight: 600;")
            r.addWidget(vl)
            scl.addLayout(r)
            self.sim_labels[k] = vl
        self.sim_bar = QProgressBar()
        self.sim_bar.setFixedHeight(10)
        self.sim_bar.setTextVisible(False)
        self.sim_bar.setStyleSheet("QProgressBar { background: rgba(255,255,255,0.08); border-radius: 5px; border: none; } QProgressBar::chunk { background: #7B2FFF; border-radius: 5px; }")
        scl.addWidget(self.sim_bar)
        sc.layout().addLayout(scl)

        cc = self._card("Controls")
        cc.setFixedWidth(160)
        top.addWidget(cc)
        ccl = QVBoxLayout()
        ccl.setContentsMargins(14, 4, 14, 10)
        ccl.setSpacing(6)
        for txt, cb, col in [("➕ Allocate", self._alloc, "#7B2FFF"), ("🗑 Free", self._free, "#FF3D57"), ("🔃 Refresh", self._refresh, "#00D4FF")]:
            btn = QPushButton(txt)
            btn.setFixedHeight(32)
            btn.setStyleSheet(f"QPushButton {{ background: {col}; color: white; border: none; border-radius: 7px; font-size: 12px; }} QPushButton:hover {{ opacity: 0.85; }}")
            btn.clicked.connect(cb)
            ccl.addWidget(btn)
        ccl.addStretch()
        cc.layout().addLayout(ccl)

        layout.addLayout(top)

        mc = self._card("Memory Map  (each cell = 4 MB)")
        layout.addWidget(mc, 1)
        self.map_canvas = MemoryCanvas()
        self.map_canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        mc.layout().addWidget(self.map_canvas)

        self.alloc_box = QTextEdit()
        self.alloc_box.setReadOnly(True)
        self.alloc_box.setFixedHeight(90)
        self.alloc_box.setFont(QFont("Courier New", 10))
        self.alloc_box.setStyleSheet("QTextEdit { background: rgba(10,14,26,0.8); color: #E8F0FF; border: 1px solid rgba(0,212,255,0.15); border-radius: 6px; padding: 6px; }")
        layout.addWidget(self.alloc_box)

    def _card(self, title):
        f = QFrame()
        f.setStyleSheet("QFrame { background: rgba(15,22,40,0.8); border-radius: 10px; border: 1px solid rgba(0,212,255,0.12); }")
        fl = QVBoxLayout(f)
        fl.setContentsMargins(0, 0, 0, 0)
        fl.setSpacing(0)
        lbl = QLabel(f"  {title}")
        lbl.setFixedHeight(34)
        lbl.setStyleSheet("color: #00D4FF; font-size: 12px; font-weight: 600; background: rgba(0,212,255,0.07); border-radius: 10px 10px 0 0; border-bottom: 1px solid rgba(0,212,255,0.1); padding: 0 8px;")
        fl.addWidget(lbl)
        return f

    def _refresh(self):
        vm = psutil.virtual_memory()
        self.real_labels["Total"].setText(fmt_size(vm.total))
        self.real_labels["Used"].setText(fmt_size(vm.used))
        self.real_labels["Free"].setText(fmt_size(vm.available))
        self.real_labels["Usage%"].setText(f"{vm.percent:.1f}%")
        self.real_bar.setValue(int(vm.percent))

        mm = self.state.mm
        self.sim_labels["Total"].setText(f"{mm.total} MB")
        self.sim_labels["Used"].setText(f"{mm.used_mb} MB")
        self.sim_labels["Free"].setText(f"{mm.free_mb} MB")
        self.sim_labels["Usage%"].setText(f"{mm.pct:.1f}%")
        self.sim_bar.setValue(int(mm.pct))

        self.map_canvas.update_pages(mm.pages, mm.allocs)

        lines = [f"{'Name':<20}{'Pages':>6}  {'MB':>6}", "─"*36]
        for n, pages in mm.allocs.items():
            lines.append(f"{n:<20}{len(pages):>6}  {len(pages)*4:>6}")
        self.alloc_box.setPlainText("\n".join(lines))

    def _alloc(self):
        n, ok = QInputDialog.getText(self, "Allocate", "Name:")
        if ok and n.strip():
            mb, ok2 = QInputDialog.getInt(self, "Allocate", "Size (MB):", 64, 4, 256)
            if ok2:
                _, msg = self.state.mm.allocate(n.strip(), mb)
                QMessageBox.information(self, "Allocate", msg)
                self._refresh()

    def _free(self):
        n, ok = QInputDialog.getText(self, "Free", "Name to free:")
        if ok and n.strip():
            QMessageBox.information(self, "Free", self.state.mm.free(n.strip()))
            self._refresh()


class MemoryCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.pages = []
        self.allocs = {}
        self.setMinimumHeight(120)
        PALETTE = ["#00D4FF","#7B2FFF","#00E676","#FFB300","#FF6B9D","#00BCD4","#FF9800","#8BC34A","#E040FB","#26C6DA"]
        self.palette = PALETTE

    def update_pages(self, pages, allocs):
        self.pages = pages
        self.allocs = allocs
        self.update()

    def paintEvent(self, event):
        if not self.pages:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.fillRect(self.rect(), QColor(6, 10, 21))
        n = len(self.pages)
        cols = 32
        cw = max(1, self.width() // cols)
        ch = 18
        unique = list(dict.fromkeys(pg for pg in self.pages if pg))
        color_map = {nm: self.palette[i % len(self.palette)] for i, nm in enumerate(unique)}
        for i, owner in enumerate(self.pages):
            col = i % cols
            row = i // cols
            x1, y1 = col*cw+1, row*ch+1
            x2, y2 = cw-2, ch-2
            fill = color_map.get(owner, "#1C2A47") if owner else "#1C2A47"
            p.setBrush(QBrush(QColor(fill)))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawRoundedRect(x1, y1, x2, y2, 2, 2)
        ly = (n // cols + 1) * ch + 8
        for i, (nm, col) in enumerate(list(color_map.items())[:10]):
            lx = 8 + i * 110
            p.setBrush(QBrush(QColor(col)))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawRoundedRect(lx, ly, 12, 12, 2, 2)
            p.setPen(QPen(QColor(TEXT_DIM)))
            p.setFont(QFont("Courier New", 8))
            p.drawText(lx + 16, ly + 10, nm)


# ═══════════════════════════════════════════════════════════════════════════════
#  I/O DEVICES APP
# ═══════════════════════════════════════════════════════════════════════════════
class IODevicesApp(QWidget):
    def __init__(self, state):
        super().__init__()
        self.state = state
        for k, v in self.state.io.DEFAULT_CONNECTED.items():
            self.state.io.connected.setdefault(k, v)
        # Per-tab layout/container references (keyed by category string)
        self._tab_layouts = {}   # category -> QVBoxLayout
        self._row_widgets = {}   # category -> {device_name -> (row_frame, status_lbl, ops_lbl, toggle_btn)}
        self._setup_ui()
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self._refresh)
        self.refresh_timer.start(3000)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        header = QHBoxLayout()
        title = QLabel("🔌  I/O Device Manager")
        title.setStyleSheet("color: white; font-size: 16px; font-weight: 700;")
        header.addWidget(title)
        header.addStretch()

        self.summary_lbl = QLabel("")
        self.summary_lbl.setStyleSheet("color: rgba(255,255,255,0.5); font-size: 12px;")
        header.addWidget(self.summary_lbl)

        refresh_btn = QPushButton("⟳  Refresh")
        refresh_btn.setFixedSize(90, 32)
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background: rgba(0,212,255,0.2);
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 12px;
            }
            QPushButton:hover { background: rgba(0,212,255,0.4); }
        """)
        refresh_btn.clicked.connect(self._refresh)
        header.addWidget(refresh_btn)

        layout.addLayout(header)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                background: rgba(15,22,40,0.6);
                border-radius: 8px;
                border: 1px solid rgba(0,212,255,0.1);
            }
            QTabBar::tab {
                background: rgba(255,255,255,0.05);
                color: rgba(255,255,255,0.6);
                padding: 8px 20px;
                border-radius: 6px;
                margin-right: 2px;
                font-size: 12px;
            }
            QTabBar::tab:selected {
                background: rgba(0,212,255,0.25);
                color: white;
                border-bottom: 2px solid #00D4FF;
            }
        """)
        layout.addWidget(self.tabs, 1)

        # Build each tab once; store references for in-place updates
        for category, label in [("all", "🔌  All Devices"), ("input", "⌨️  Input Devices"), ("output", "🔊  Output Devices")]:
            tab_widget = self._create_device_table(category)
            self.tabs.addTab(tab_widget, label)

        self._update_summary()

    def _create_device_table(self, category):
        """Build the tab widget once and populate rows into it."""
        widget = QWidget()
        widget.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(0)

        header = QFrame()
        header.setFixedHeight(32)
        header.setStyleSheet("background: rgba(0,212,255,0.1); border-radius: 6px; border: 1px solid rgba(0,212,255,0.15);")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(10, 0, 10, 0)
        header_layout.setSpacing(0)

        columns = [
            ("Device", 130), ("Type", 90), ("Status", 90), ("Bus", 80),
            ("Driver", 110), ("IRQ", 45), ("Ops", 70), ("", 80)
        ]
        for text, width in columns:
            lbl = QLabel(text)
            lbl.setStyleSheet("color: #00D4FF; font-size: 10px; font-weight: 700;")
            lbl.setFixedWidth(width)
            header_layout.addWidget(lbl)

        layout.addWidget(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent; border: none;")

        # Each tab gets its own container — store per-category
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        vbox = QVBoxLayout(container)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(2)
        self._tab_layouts[category] = vbox

        scroll.setWidget(container)
        layout.addWidget(scroll, 1)

        self._populate_devices(category)
        return widget

    def _populate_devices(self, category):
        """Build all device rows for a category (called once per tab)."""
        vbox = self._tab_layouts[category]
        # Clear any existing rows
        while vbox.count():
            item = vbox.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self._row_widgets[category] = {}
        io = self.state.io
        all_devices = {**io.INPUT_DEVICES, **io.OUTPUT_DEVICES}

        for name, info in all_devices.items():
            dev_type = "Input" if name in io.INPUT_DEVICES else "Output"
            if category == "input" and dev_type != "Input":
                continue
            if category == "output" and dev_type != "Output":
                continue

            connected = io.connected.get(name, False)
            status_color = "#00E676" if connected else "#6B7FA3"
            status_text = "● active" if connected else "○ inactive"

            row = QFrame()
            row.setFixedHeight(36)
            row.setStyleSheet("""
                QFrame {
                    background: rgba(20,30,53,0.6);
                    border-radius: 5px;
                }
                QFrame:hover {
                    background: rgba(0,212,255,0.1);
                }
            """)
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(10, 0, 10, 0)
            row_layout.setSpacing(0)

            icon = info.get("icon", "📦")
            name_lbl = QLabel(f"{icon}  {name}")
            name_lbl.setFixedWidth(130)
            name_lbl.setStyleSheet("color: white; font-size: 12px;")
            row_layout.addWidget(name_lbl)

            type_lbl = QLabel(info.get("type", dev_type))
            type_lbl.setFixedWidth(90)
            type_lbl.setStyleSheet("color: rgba(255,255,255,0.6); font-size: 11px;")
            row_layout.addWidget(type_lbl)

            status_lbl = QLabel(status_text)
            status_lbl.setFixedWidth(90)
            status_lbl.setStyleSheet(f"color: {status_color}; font-size: 11px;")
            row_layout.addWidget(status_lbl)

            bus_lbl = QLabel(info.get("port", "-"))
            bus_lbl.setFixedWidth(80)
            bus_lbl.setStyleSheet("color: rgba(255,255,255,0.6); font-size: 11px;")
            row_layout.addWidget(bus_lbl)

            driver_lbl = QLabel(info.get("driver", "-"))
            driver_lbl.setFixedWidth(110)
            driver_lbl.setStyleSheet("color: rgba(255,255,255,0.6); font-size: 11px;")
            row_layout.addWidget(driver_lbl)

            irq_lbl = QLabel(str(info.get("irq", "-")))
            irq_lbl.setFixedWidth(45)
            irq_lbl.setStyleSheet("color: rgba(255,255,255,0.6); font-size: 11px;")
            row_layout.addWidget(irq_lbl)

            ops_lbl = QLabel(str(io.ops.get(name, 0)))
            ops_lbl.setFixedWidth(70)
            ops_lbl.setStyleSheet("color: #00D4FF; font-size: 11px; font-family: monospace;")
            row_layout.addWidget(ops_lbl)

            toggle_btn = QPushButton("Disconnect" if connected else "  Connect")
            toggle_btn.setFixedSize(85, 28)
            btn_color = "rgba(255,61,87,0.4)" if connected else "rgba(0,212,255,0.3)"
            toggle_btn.setStyleSheet(f"""
                QPushButton {{
                    background: {btn_color};
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-size: 11px;
                }}
                QPushButton:hover {{
                    background: {"rgba(255,61,87,0.7)" if connected else "rgba(0,212,255,0.6)"};
                }}
            """)
            toggle_btn.clicked.connect(lambda checked, n=name: self._toggle_device(n))
            row_layout.addWidget(toggle_btn)

            vbox.addWidget(row)
            self._row_widgets[category][name] = (status_lbl, ops_lbl, toggle_btn)

        vbox.addStretch()

    def _toggle_device(self, name):
        self.state.io.toggle(name)
        self._update_rows()
        self._update_summary()

    def _update_rows(self):
        """Update only the dynamic labels/buttons in existing rows — no widget rebuilding."""
        io = self.state.io
        for category, rows in self._row_widgets.items():
            for name, (status_lbl, ops_lbl, toggle_btn) in rows.items():
                connected = io.connected.get(name, False)
                status_color = "#00E676" if connected else "#6B7FA3"
                status_lbl.setText("● active" if connected else "○ inactive")
                status_lbl.setStyleSheet(f"color: {status_color}; font-size: 11px;")
                ops_lbl.setText(str(io.ops.get(name, 0)))
                btn_color = "rgba(255,61,87,0.4)" if connected else "rgba(0,212,255,0.3)"
                btn_hover = "rgba(255,61,87,0.7)" if connected else "rgba(0,212,255,0.6)"
                toggle_btn.setText("Disconnect" if connected else "  Connect")
                toggle_btn.setStyleSheet(f"""
                    QPushButton {{
                        background: {btn_color};
                        color: white;
                        border: none;
                        border-radius: 5px;
                        font-size: 11px;
                    }}
                    QPushButton:hover {{ background: {btn_hover}; }}
                """)

    def _refresh(self):
        """Periodic refresh: simulate I/O counter ticks, update labels in-place."""
        self.state.io.simulate_io()
        self._update_rows()
        self._update_summary()

    def _update_summary(self):
        io = self.state.io
        total = len(io.connected)
        connected = sum(1 for v in io.connected.values() if v)
        cin = sum(1 for n in io.INPUT_DEVICES if io.connected.get(n, False))
        cout = sum(1 for n in io.OUTPUT_DEVICES if io.connected.get(n, False))
        self.summary_lbl.setText(f"{connected}/{total} devices connected  |  Input: {cin}  •  Output: {cout}")


# ═══════════════════════════════════════════════════════════════════════════════
#  FILE MANAGER APP
# ═══════════════════════════════════════════════════════════════════════════════
class FileManagerApp(QWidget):
    def __init__(self, state, start_folder=None):
        super().__init__()
        self.state = state
        self.cwd = Path(os.path.expanduser("~"))
        self.selected_item = None
        self.history = [self.cwd]
        self.hist_idx = 0
        self._setup_ui()
        self._refresh()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        nav = QWidget()
        nav.setFixedHeight(48)
        nav.setStyleSheet("background: rgba(0,212,255,0.05); border-bottom: 1px solid rgba(0,212,255,0.12);")
        nav_layout = QHBoxLayout(nav)
        nav_layout.setContentsMargins(10, 6, 10, 6)
        nav_layout.setSpacing(6)

        for icon, tip, action in [("←", "Back", self._go_back), ("→", "Forward", self._go_forward),
                                   ("⬆", "Up", self._go_up), ("🏠", "Home", self._go_home)]:
            btn = QPushButton(icon)
            btn.setFixedSize(36, 34)
            btn.setToolTip(tip)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background: rgba(255,255,255,0.07);
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-size: 14px;
                }
                QPushButton:hover { background: rgba(0,212,255,0.2); }
            """)
            btn.clicked.connect(action)
            nav_layout.addWidget(btn)

        self.path_lbl = QLabel()
        self.path_lbl.setStyleSheet("color: #00D4FF; font-size: 12px; font-family: monospace; padding: 0 8px;")
        self.path_lbl.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        nav_layout.addWidget(self.path_lbl, 1)

        go_btn = QPushButton("Go")
        go_btn.setFixedSize(50, 34)
        go_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        go_btn.setStyleSheet("""
            QPushButton {
                background: rgba(0,212,255,0.2);
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 12px;
            }
            QPushButton:hover { background: rgba(0,212,255,0.4); }
        """)
        go_btn.clicked.connect(self._nav_to_typed)
        nav_layout.addWidget(go_btn)

        layout.addWidget(nav)

        toolbar = QWidget()
        toolbar.setFixedHeight(46)
        toolbar.setStyleSheet("background: rgba(0,0,0,0.15); border-bottom: 1px solid rgba(0,212,255,0.08);")
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(10, 4, 10, 4)
        toolbar_layout.setSpacing(8)

        for text, action, color in [
            ("📁 New Folder", self._new_folder, "#7B2FFF"),
            ("📄 New File", self._new_file, "#00D4FF"),
            ("✏️ Rename", self._rename_item, "#FFB300"),
            ("🗑 Delete", self._delete_item, "#FF3D57"),
            ("📋 Copy Path", self._copy_path, "#6B7FA3"),
            ("📂 Open In OS", self._open_external, "#00E676"),
            ("🔃 Refresh", self._refresh, "#00D4FF"),
        ]:
            btn = QPushButton(text)
            btn.setFixedHeight(32)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: {color};
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-size: 11px;
                    padding: 0 12px;
                }}
                QPushButton:hover {{ opacity: 0.85; }}
            """)
            btn.clicked.connect(action)
            toolbar_layout.addWidget(btn)

        toolbar_layout.addStretch()

        search_lbl = QLabel("🔍")
        search_lbl.setStyleSheet("color: rgba(255,255,255,0.4); font-size: 12px;")
        toolbar_layout.addWidget(search_lbl)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search...")
        self.search_input.setFixedWidth(180)
        self.search_input.setFixedHeight(30)
        self.search_input.setStyleSheet("""
            QLineEdit {
                background: rgba(255,255,255,0.07);
                color: white;
                border: 1px solid rgba(0,212,255,0.2);
                border-radius: 5px;
                padding: 0 10px;
                font-size: 11px;
            }
            QLineEdit:focus { border-color: #00D4FF; }
        """)
        self.search_input.textChanged.connect(self._refresh)
        toolbar_layout.addWidget(self.search_input)

        layout.addWidget(toolbar)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setStyleSheet("QSplitter::handle { background: rgba(0,212,255,0.1); width: 1px; }")

        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)

        header = QFrame()
        header.setFixedHeight(32)
        header.setStyleSheet("background: rgba(0,212,255,0.08); border-bottom: 1px solid rgba(0,212,255,0.15);")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(12, 0, 12, 0)
        header_layout.setSpacing(0)

        for text, width in [("Name", 280), ("Type", 100), ("Size", 90), ("Modified", 150)]:
            lbl = QLabel(text)
            lbl.setStyleSheet("color: #00D4FF; font-size: 10px; font-weight: 700;")
            lbl.setFixedWidth(width)
            header_layout.addWidget(lbl)

        left_layout.addWidget(header)

        self.file_scroll = QScrollArea()
        self.file_scroll.setWidgetResizable(True)
        self.file_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.file_scroll.setStyleSheet("background: transparent; border: none;")
        
        self.file_container = QWidget()
        self.file_container.setStyleSheet("background: transparent;")
        self.file_layout = QVBoxLayout(self.file_container)
        self.file_layout.setContentsMargins(0, 0, 0, 0)
        self.file_layout.setSpacing(1)
        
        self.file_scroll.setWidget(self.file_container)
        left_layout.addWidget(self.file_scroll, 1)

        right_panel = QFrame()
        right_panel.setFixedWidth(320)
        right_panel.setStyleSheet("background: rgba(15,22,40,0.8); border-left: 1px solid rgba(0,212,255,0.1);")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(12, 12, 12, 12)
        right_layout.setSpacing(8)

        prop_title = QLabel("📋  Properties")
        prop_title.setStyleSheet("color: #00D4FF; font-size: 13px; font-weight: 600;")
        right_layout.addWidget(prop_title)

        self.prop_text = QTextEdit()
        self.prop_text.setReadOnly(True)
        self.prop_text.setFont(QFont("Courier New", 10))
        self.prop_text.setStyleSheet("""
            QTextEdit {
                background: rgba(10,14,26,0.6);
                color: #E8F0FF;
                border: 1px solid rgba(0,212,255,0.1);
                border-radius: 6px;
                padding: 8px;
            }
        """)
        right_layout.addWidget(self.prop_text, 1)

        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([800, 320])

        layout.addWidget(splitter, 1)

        self.status_bar = QLabel("")
        self.status_bar.setFixedHeight(24)
        self.status_bar.setStyleSheet("color: rgba(255,255,255,0.4); font-size: 11px; padding: 0 12px; background: rgba(0,0,0,0.2);")
        layout.addWidget(self.status_bar)

    def _refresh(self):
        while self.file_layout.count():
            item = self.file_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        search_text = self.search_input.text().lower()
        
        try:
            entries = list(self.cwd.iterdir())
        except PermissionError:
            self.status_bar.setText("  ⛔ Permission denied")
            return

        dirs = [e for e in entries if e.is_dir()]
        files = [e for e in entries if e.is_file()]
        
        dirs.sort(key=lambda x: x.name.lower())
        files.sort(key=lambda x: x.name.lower())
        items = dirs + files
        
        if search_text:
            items = [e for e in items if search_text in e.name.lower()]

        folders_count = 0
        files_count = 0

        for entry in items:
            is_dir = entry.is_dir()
            if is_dir:
                folders_count += 1
            else:
                files_count += 1
                
            try:
                stat = entry.stat()
                size = fmt_size(stat.st_size) if not is_dir else "–"
                mtime = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
                ftype = "Folder" if is_dir else (entry.suffix.upper().lstrip(".") + " File" if entry.suffix else "File")
            except:
                size = "–"
                mtime = "–"
                ftype = "–"

            icon = file_icon(str(entry))
            
            row = QFrame()
            row.setFixedHeight(34)
            row.setStyleSheet("""
                QFrame {
                    background: rgba(20,30,53,0.4);
                    border-radius: 4px;
                }
                QFrame:hover {
                    background: rgba(0,212,255,0.1);
                }
            """)
            row.setCursor(Qt.CursorShape.PointingHandCursor)
            
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(12, 0, 12, 0)
            row_layout.setSpacing(0)
            
            name_lbl = QLabel(f"{icon}  {entry.name}")
            name_lbl.setFixedWidth(280)
            name_lbl.setStyleSheet(f"color: {'#00D4FF' if is_dir else 'white'}; font-size: 12px;")
            row_layout.addWidget(name_lbl)
            
            type_lbl = QLabel(ftype)
            type_lbl.setFixedWidth(100)
            type_lbl.setStyleSheet("color: rgba(255,255,255,0.5); font-size: 11px;")
            row_layout.addWidget(type_lbl)
            
            size_lbl = QLabel(size)
            size_lbl.setFixedWidth(90)
            size_lbl.setStyleSheet("color: rgba(255,255,255,0.5); font-size: 11px;")
            row_layout.addWidget(size_lbl)
            
            mtime_lbl = QLabel(mtime)
            mtime_lbl.setFixedWidth(150)
            mtime_lbl.setStyleSheet("color: rgba(255,255,255,0.4); font-size: 11px;")
            row_layout.addWidget(mtime_lbl)
            
            row.setProperty("path", str(entry))
            
            row.mousePressEvent = lambda e, p=entry: self._on_item_click(e, p)
            row.mouseDoubleClickEvent = lambda e, p=entry: self._on_item_double_click(e, p)
            
            self.file_layout.addWidget(row)
        
        self.file_layout.addStretch()
        
        self.path_lbl.setText(str(self.cwd))
        self.status_bar.setText(f"  {folders_count} folders  •  {files_count} files")
        
        if not self.selected_item:
            self.prop_text.clear()

    def _on_item_click(self, event, path):
        self.selected_item = path
        self._show_properties(path)

    def _on_item_double_click(self, event, path):
        if path.is_dir():
            self._navigate(path)
        else:
            self._show_properties(path)

    def _show_properties(self, path):
        try:
            stat = path.stat()
            is_dir = path.is_dir()
            lines = [
                f"Name:      {path.name}",
                f"Type:      {'Directory' if is_dir else 'File'}",
                f"Extension: {path.suffix or 'None'}",
                f"Size:      {fmt_size(stat.st_size) if not is_dir else 'N/A'}",
                f"Modified:  {datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}",
                f"Created:   {datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')}",
                f"Path:      {path}",
            ]
            
            if not is_dir and path.suffix.lower() in ['.txt', '.py', '.md', '.json', '.csv', '.js', '.html', '.css', '.xml']:
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        preview = f.read(500)
                    lines.append("\n─── Preview ───")
                    lines.append(preview)
                except:
                    lines.append("\n(Preview not available)")
            
            self.prop_text.setPlainText("\n".join(lines))
        except Exception as e:
            self.prop_text.setPlainText(f"Error: {e}")

    def _navigate(self, path):
        self.cwd = path
        self.history = self.history[:self.hist_idx + 1]
        self.history.append(path)
        self.hist_idx = len(self.history) - 1
        self._refresh()

    def _nav_to_typed(self):
        p = Path(self.path_lbl.text())
        if p.is_dir():
            self._navigate(p)

    def _go_back(self):
        if self.hist_idx > 0:
            self.hist_idx -= 1
            self.cwd = self.history[self.hist_idx]
            self._refresh()

    def _go_forward(self):
        if self.hist_idx < len(self.history) - 1:
            self.hist_idx += 1
            self.cwd = self.history[self.hist_idx]
            self._refresh()

    def _go_up(self):
        parent = self.cwd.parent
        if parent != self.cwd:
            self._navigate(parent)

    def _go_home(self):
        self._navigate(Path.home())

    def _new_folder(self):
        name, ok = QInputDialog.getText(self, "New Folder", "Folder name:")
        if ok and name.strip():
            try:
                (self.cwd / name.strip()).mkdir(exist_ok=True)
                self._refresh()
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))

    def _new_file(self):
        name, ok = QInputDialog.getText(self, "New File", "File name:")
        if ok and name.strip():
            try:
                (self.cwd / name.strip()).touch()
                self._refresh()
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))

    def _rename_item(self):
        if not self.selected_item:
            QMessageBox.warning(self, "Rename", "Select a file/folder first.")
            return
        new_name, ok = QInputDialog.getText(self, "Rename", "New name:", text=self.selected_item.name)
        if ok and new_name.strip():
            try:
                self.selected_item.rename(self.cwd / new_name.strip())
                self.selected_item = None
                self._refresh()
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))

    def _delete_item(self):
        if not self.selected_item:
            QMessageBox.warning(self, "Delete", "Select a file/folder first.")
            return
        if QMessageBox.question(self, "Delete", f"Delete '{self.selected_item.name}'?",
                                 QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            try:
                if self.selected_item.is_dir():
                    shutil.rmtree(self.selected_item)
                else:
                    self.selected_item.unlink()
                self.selected_item = None
                self._refresh()
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))

    def _copy_path(self):
        if self.selected_item:
            QApplication.clipboard().setText(str(self.selected_item))
            QMessageBox.information(self, "Copied", f"Path copied:\n{self.selected_item}")
        else:
            QApplication.clipboard().setText(str(self.cwd))
            QMessageBox.information(self, "Copied", f"Current directory copied:\n{self.cwd}")

    def _open_external(self):
        target = self.selected_item or self.cwd
        try:
            if platform.system() == "Windows":
                os.startfile(str(target))
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", str(target)])
            else:
                subprocess.Popen(["xdg-open", str(target)])
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))


# ═══════════════════════════════════════════════════════════════════════════════
#  TEXT EDITOR APP
# ═══════════════════════════════════════════════════════════════════════════════
class TextEditorApp(QWidget):
    def __init__(self, state):
        super().__init__()
        self.state = state
        self.current_file = None
        self.modified = False
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        mb = QWidget()
        mb.setFixedHeight(36)
        mb.setStyleSheet("background: rgba(255,255,255,0.04); border-bottom: 1px solid rgba(0,212,255,0.1);")
        mbl = QHBoxLayout(mb)
        mbl.setContentsMargins(8, 2, 8, 2)
        mbl.setSpacing(2)
        
        for lbl, act in [("New", self._new), ("Open", self._open), ("Save", self._save), ("Save As", self._save_as)]:
            b = QPushButton(lbl)
            b.setFixedHeight(28)
            b.setStyleSheet("QPushButton { background: transparent; color: rgba(255,255,255,0.75); border: none; border-radius: 5px; padding: 0 12px; font-size: 13px; } QPushButton:hover { background: rgba(0,212,255,0.15); }")
            b.clicked.connect(act)
            mbl.addWidget(b)
        
        mbl.addStretch()
        self.fs = QSpinBox()
        self.fs.setRange(8, 72)
        self.fs.setValue(12)
        self.fs.setFixedWidth(55)
        self.fs.setStyleSheet("background: rgba(255,255,255,0.08); color: white; border: none; border-radius: 4px; padding: 2px;")
        self.fs.valueChanged.connect(self._update_font)
        mbl.addWidget(self.fs)
        layout.addWidget(mb)
        
        self.editor = QTextEdit()
        self.editor.setFont(QFont("Courier New", 12))
        self.editor.setStyleSheet("QTextEdit { background: #1e1e2e; color: #cdd6f4; border: none; padding: 16px; selection-background-color: #363a4f; }")
        self.editor.textChanged.connect(lambda: setattr(self, 'modified', True))
        layout.addWidget(self.editor, 1)
        
        self.status = QLabel("  New Document  |  Ln 1, Col 1")
        self.status.setFixedHeight(22)
        self.status.setStyleSheet("color: rgba(255,255,255,0.35); font-size: 11px; background: rgba(0,0,0,0.2); padding: 0 10px;")
        layout.addWidget(self.status)
        self.editor.cursorPositionChanged.connect(self._update_status)

    def _update_font(self):
        self.editor.setFont(QFont("Courier New", self.fs.value()))
    
    def _update_status(self):
        c = self.editor.textCursor()
        ln = c.blockNumber() + 1
        col = c.columnNumber() + 1
        self.status.setText(f"  {self.current_file or 'Untitled'}{'●' if self.modified else ''}  |  Ln {ln}, Col {col}")
    
    def _new(self):
        self.editor.clear()
        self.current_file = None
        self.modified = False
    
    def _open(self):
        docs = self.state.fs.get("Documents", {}).get("children", {})
        names = list(docs.keys())
        if not names:
            QMessageBox.information(self, "Open", "No files in Documents.")
            return
        n, ok = QInputDialog.getItem(self, "Open File", "Select file:", names, 0, False)
        if ok:
            self.editor.setPlainText(docs[n].get("content", ""))
            self.current_file = n
            self.modified = False
    
    def _save(self):
        if not self.current_file:
            self._save_as()
            return
        docs = self.state.fs.setdefault("Documents", {"type": "folder", "children": {}})["children"]
        docs.setdefault(self.current_file, {"type": "file", "content": ""})["content"] = self.editor.toPlainText()
        self.modified = False
        self._update_status()
    
    def _save_as(self):
        n, ok = QInputDialog.getText(self, "Save As", "File name:")
        if ok and n.strip():
            self.current_file = n.strip() if n.strip().endswith(".txt") else n.strip() + ".txt"
            self._save()


# ═══════════════════════════════════════════════════════════════════════════════
#  CALCULATOR APP
# ═══════════════════════════════════════════════════════════════════════════════
class CalculatorApp(QWidget):
    def __init__(self, state):
        super().__init__()
        self.state = state
        self.expression = ""
        self.result_shown = False
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        
        self.display = QLabel("0")
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.display.setFixedHeight(80)
        self.display.setFont(QFont("Segoe UI Light", 36))
        self.display.setStyleSheet("QLabel { background: rgba(0,212,255,0.06); color: white; border-radius: 10px; padding: 0 16px; border: 1px solid rgba(0,212,255,0.15); }")
        layout.addWidget(self.display)
        
        self.expr_lbl = QLabel("")
        self.expr_lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.expr_lbl.setStyleSheet("color: rgba(255,255,255,0.4); font-size: 12px; padding-right: 6px;")
        layout.addWidget(self.expr_lbl)
        
        grid = QGridLayout()
        grid.setSpacing(6)
        buttons = [
            [("C", "clear"), ("±", "sign"), ("%", "%"), ("÷", "/")],
            [("7", "7"), ("8", "8"), ("9", "9"), ("×", "*")],
            [("4", "4"), ("5", "5"), ("6", "6"), ("−", "-")],
            [("1", "1"), ("2", "2"), ("3", "3"), ("+", "+")],
            [("0", "0"), (".", "."), ("=", "=")],
        ]
        for row, btn_row in enumerate(buttons):
            col_offset = 0
            for col, (label, value) in enumerate(btn_row):
                btn = QPushButton(label)
                if value in ("+", "-", "*", "/"):
                    bg, hov = "#00D4FF", "#00B8E0"
                elif value == "=":
                    bg, hov = "#7B2FFF", "#6928E0"
                elif value == "clear":
                    bg, hov = "#FF3D57", "#E03550"
                else:
                    bg, hov = "rgba(255,255,255,0.1)", "rgba(0,212,255,0.2)"
                btn.setStyleSheet(f"QPushButton {{ background: {bg}; color: white; border: none; border-radius: 10px; font-size: 18px; }} QPushButton:hover {{ background: {hov}; }}")
                btn.setFixedHeight(52)
                btn.setCursor(Qt.CursorShape.PointingHandCursor)
                if label == "0":
                    btn.setFixedWidth(114)
                    grid.addWidget(btn, row + 2, col, 1, 2)
                    col_offset = 1
                else:
                    grid.addWidget(btn, row + 2, col + col_offset)
                btn.clicked.connect(lambda c=False, v=value: self._on_btn(v))
        layout.addLayout(grid)

    def _on_btn(self, value):
        if value == "clear":
            self.expression = ""
            self.display.setText("0")
            self.expr_lbl.setText("")
            self.result_shown = False
        elif value == "=":
            if self.expression:
                try:
                    result = eval(self.expression)
                    if isinstance(result, float) and result.is_integer():
                        result = int(result)
                    self.expr_lbl.setText(self.expression + " =")
                    self.display.setText(str(result))
                    self.expression = str(result)
                    self.result_shown = True
                except:
                    self.display.setText("Error")
                    self.expression = ""
        elif value == "sign":
            if self.expression:
                try:
                    self.expression = str(-eval(self.expression))
                    self.display.setText(self.expression)
                except:
                    pass
        elif value == "%":
            if self.expression:
                try:
                    self.expression = str(eval(self.expression) / 100)
                    self.display.setText(self.expression)
                except:
                    pass
        else:
            if self.result_shown and value.isdigit():
                self.expression = value
                self.result_shown = False
            else:
                self.expression += value
                self.result_shown = False
            disp = self.expression.replace("*", "×").replace("/", "÷").replace("-", "−")
            self.display.setText(disp[-12:] if len(disp) > 12 else disp)


# ═══════════════════════════════════════════════════════════════════════════════
#  NOTES APP
# ═══════════════════════════════════════════════════════════════════════════════
class NotesApp(QWidget):
    def __init__(self, state):
        super().__init__()
        self.state = state
        if not hasattr(state, 'notes'):
            state.notes = {"Quick Note": "Write your notes here..."}
        self.current_note = None
        self._setup_ui()
        self._refresh_list()

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        sb = QWidget()
        sb.setFixedWidth(170)
        sb.setStyleSheet("background: rgba(0,0,0,0.2); border-right: 1px solid rgba(0,212,255,0.12);")
        sl = QVBoxLayout(sb)
        sl.setContentsMargins(8, 10, 8, 10)
        sl.setSpacing(6)
        
        hdr = QHBoxLayout()
        lbl = QLabel("Notes")
        lbl.setStyleSheet("color: white; font-size: 14px; font-weight: 600;")
        hdr.addWidget(lbl)
        ab = QPushButton("+")
        ab.setFixedSize(26, 26)
        ab.setStyleSheet("QPushButton { background: #00D4FF; color: white; border: none; border-radius: 13px; font-size: 16px; font-weight: bold; } QPushButton:hover { background: #00B8E0; }")
        ab.clicked.connect(self._new_note)
        hdr.addWidget(ab)
        sl.addLayout(hdr)
        
        self.note_list = QListWidget()
        self.note_list.setStyleSheet("QListWidget { background: transparent; border: none; color: white; font-size: 12px; } QListWidget::item { padding: 8px 6px; border-radius: 6px; margin: 1px; } QListWidget::item:selected { background: rgba(0,212,255,0.3); } QListWidget::item:hover { background: rgba(0,212,255,0.1); }")
        self.note_list.currentItemChanged.connect(self._load_note)
        sl.addWidget(self.note_list, 1)
        
        db = QPushButton("🗑 Delete")
        db.setFixedHeight(28)
        db.setStyleSheet("QPushButton { background: rgba(255,61,87,0.25); color: white; border: none; border-radius: 6px; font-size: 11px; } QPushButton:hover { background: rgba(255,61,87,0.5); }")
        db.clicked.connect(self._delete_note)
        sl.addWidget(db)
        layout.addWidget(sb)
        
        ew = QWidget()
        el = QVBoxLayout(ew)
        el.setContentsMargins(0, 0, 0, 0)
        el.setSpacing(0)
        
        tb = QWidget()
        tb.setFixedHeight(38)
        tb.setStyleSheet("background: rgba(255,255,255,0.03); border-bottom: 1px solid rgba(0,212,255,0.1);")
        tbl = QHBoxLayout(tb)
        tbl.setContentsMargins(14, 4, 14, 4)
        
        self.note_title = QLabel("Select a note")
        self.note_title.setStyleSheet("color: rgba(255,255,255,0.7); font-size: 13px;")
        tbl.addWidget(self.note_title)
        tbl.addStretch()
        
        sb2 = QPushButton("💾 Save")
        sb2.setFixedHeight(28)
        sb2.setStyleSheet("QPushButton { background: rgba(0,212,255,0.3); color: white; border: none; border-radius: 6px; font-size: 12px; padding: 0 12px; } QPushButton:hover { background: rgba(0,212,255,0.5); }")
        sb2.clicked.connect(self._save)
        tbl.addWidget(sb2)
        el.addWidget(tb)
        
        self.editor = QTextEdit()
        self.editor.setFont(QFont("Segoe UI", 12))
        self.editor.setStyleSheet("QTextEdit { background: #1e2030; color: #cdd6f4; border: none; padding: 16px; font-size: 13px; }")
        self.editor.setPlaceholderText("Start writing...")
        el.addWidget(self.editor, 1)
        layout.addWidget(ew, 1)

    def _refresh_list(self):
        self.note_list.clear()
        for name in self.state.notes:
            self.note_list.addItem(f"📒  {name}")
        if self.note_list.count() > 0:
            self.note_list.setCurrentRow(0)

    def _load_note(self, item):
        if not item:
            return
        name = item.text().replace("📒  ", "")
        self.current_note = name
        self.note_title.setText(name)
        self.editor.setPlainText(self.state.notes.get(name, ""))

    def _new_note(self):
        n, ok = QInputDialog.getText(self, "New Note", "Note title:")
        if ok and n.strip():
            self.state.notes[n.strip()] = ""
            self._refresh_list()

    def _save(self):
        if self.current_note:
            self.state.notes[self.current_note] = self.editor.toPlainText()

    def _delete_note(self):
        if self.current_note and self.current_note in self.state.notes:
            del self.state.notes[self.current_note]
            self.current_note = None
            self.editor.clear()
            self.note_title.setText("Select a note")
            self._refresh_list()


# ═══════════════════════════════════════════════════════════════════════════════
#  BROWSER APP
# ═══════════════════════════════════════════════════════════════════════════════
class BrowserApp(QWidget):
    PAGES = {
        "novaos.home": "<div style='padding:30px;background:#0d1a30;color:white;'><h1 style='color:#00D4FF;'>⬡ NOVA OS Browser</h1><p style='color:#6B7FA3;'>NOVA OS Edition v1.0</p><hr style='border:1px solid #1C2A47;'/><h3>Quick Links</h3><ul><li>NOVAOS Home</li><li>Documentation</li><li>Settings</li></ul></div>",
        "google.com": "<div style='padding:40px;text-align:center;background:#fff;'><h1 style='color:#4285F4;font-size:72px;letter-spacing:-2px;'>Google</h1><p style='color:#888;'>[Simulated Browser — No internet access]</p></div>",
    }

    def __init__(self, state):
        super().__init__()
        self.state = state
        self.current_url = "novaos.home"
        self.history = []
        self._setup_ui()
        self._navigate("novaos.home")

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        nav = QWidget()
        nav.setFixedHeight(44)
        nav.setStyleSheet("background: rgba(0,212,255,0.05); border-bottom: 1px solid rgba(0,212,255,0.12);")
        nl = QHBoxLayout(nav)
        nl.setContentsMargins(8, 4, 8, 4)
        nl.setSpacing(4)
        
        for icon, act in [("←", self._go_back), ("↺", lambda: self._navigate(self.current_url))]:
            b = QPushButton(icon)
            b.setFixedSize(32, 32)
            b.clicked.connect(act)
            b.setStyleSheet("QPushButton { background: rgba(255,255,255,0.07); color: white; border: none; border-radius: 6px; font-size: 15px; } QPushButton:hover { background: rgba(0,212,255,0.2); }")
            nl.addWidget(b)
        
        self.url_bar = QLineEdit(self.current_url)
        self.url_bar.setFixedHeight(32)
        self.url_bar.setStyleSheet("QLineEdit { background: rgba(255,255,255,0.08); color: white; border: 1px solid rgba(0,212,255,0.2); border-radius: 16px; padding: 0 14px; font-size: 13px; } QLineEdit:focus { border-color: #00D4FF; }")
        self.url_bar.returnPressed.connect(lambda: self._navigate(self.url_bar.text().strip()))
        nl.addWidget(self.url_bar, 1)
        
        go = QPushButton("Go")
        go.setFixedSize(40, 32)
        go.setStyleSheet("QPushButton { background: #00D4FF; color: white; border: none; border-radius: 6px; font-size: 12px; } QPushButton:hover { background: #00B8E0; }")
        go.clicked.connect(lambda: self._navigate(self.url_bar.text().strip()))
        nl.addWidget(go)
        layout.addWidget(nav)
        
        self.content = QTextEdit()
        self.content.setReadOnly(True)
        self.content.setStyleSheet("background: #f5f5f5; color: #222; border: none; padding: 10px;")
        layout.addWidget(self.content, 1)
        
        self.status = QLabel("  Ready")
        self.status.setFixedHeight(22)
        self.status.setStyleSheet("color: rgba(255,255,255,0.4); font-size: 11px; background: rgba(0,0,0,0.2); padding: 0 10px;")
        layout.addWidget(self.status)

    def _navigate(self, url):
        if not url:
            return
        self.history.append(url)
        self.current_url = url
        self.url_bar.setText(url)
        page = self.PAGES.get(url.lower())
        if page:
            self.content.setHtml(page)
        else:
            self.content.setHtml(f"<div style='padding:30px;text-align:center;background:#f5f5f5;'><h2 style='color:#666;'>🌐 {url}</h2><p style='color:#888;'>Simulated browser — no internet access.</p><p style='color:#aaa;'>NOVA OS Browser v1.0</p></div>")
        self.status.setText(f"  {url}")

    def _go_back(self):
        if len(self.history) > 1:
            self.history.pop()
            self._navigate(self.history[-1])


# ═══════════════════════════════════════════════════════════════════════════════
#  PAINT APP
# ═══════════════════════════════════════════════════════════════════════════════
class PaintApp(QWidget):
    def __init__(self, state):
        super().__init__()
        self.state = state
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        tb = QWidget()
        tb.setFixedHeight(44)
        tb.setStyleSheet("background: rgba(0,212,255,0.05); border-bottom: 1px solid rgba(0,212,255,0.12);")
        tbl = QHBoxLayout(tb)
        tbl.setContentsMargins(8, 4, 8, 4)
        tbl.setSpacing(6)
        
        self.pen_size = QSlider(Qt.Orientation.Horizontal)
        self.pen_size.setRange(1, 30)
        self.pen_size.setValue(4)
        self.pen_size.setFixedWidth(100)
        self.pen_size.setStyleSheet("QSlider::groove:horizontal { background: rgba(0,212,255,0.2); height: 6px; border-radius: 3px; } QSlider::handle:horizontal { background: #00D4FF; width: 16px; height: 16px; border-radius: 8px; margin: -5px 0; } QSlider::sub-page:horizontal { background: #00D4FF; border-radius: 3px; }")
        tbl.addWidget(QLabel("Size:"))
        tbl.addWidget(self.pen_size)
        
        self.current_color = QColor("#00D4FF")
        colors = ["#FFFFFF", "#FF3D57", "#00D4FF", "#7B2FFF", "#00E676", "#FFB300", "#FF6B9D", "#000000"]
        for c in colors:
            b = QPushButton()
            b.setFixedSize(28, 28)
            b.setStyleSheet(f"QPushButton {{ background: {c}; border: 2px solid rgba(255,255,255,0.3); border-radius: 14px; }} QPushButton:hover {{ border-color: white; }}")
            b.clicked.connect(lambda chk=False, col=c: setattr(self, 'current_color', QColor(col)))
            tbl.addWidget(b)
        
        clr = QPushButton("Clear Canvas")
        clr.setStyleSheet("QPushButton { background: rgba(255,61,87,0.3); color: white; border: none; border-radius: 6px; font-size: 12px; padding: 0 12px; } QPushButton:hover { background: rgba(255,61,87,0.5); }")
        clr.clicked.connect(self._clear)
        tbl.addWidget(clr)
        tbl.addStretch()
        layout.addWidget(tb)
        
        self.canvas = PaintCanvas()
        layout.addWidget(self.canvas, 1)
        self.canvas.pen_size_ref = self.pen_size
        self.canvas.color_ref = self

    def _clear(self):
        self.canvas.clear()


class PaintCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.paths = []
        self.current_path = []
        self.drawing = False
        self.pen_size_ref = None
        self.color_ref = None
        self.setStyleSheet("background: #1a1a1a;")
        self.setMouseTracking(True)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.drawing = True
            self.current_path = [(e.pos(), self._get_color(), self._get_size())]

    def mouseMoveEvent(self, e):
        if self.drawing:
            self.current_path.append((e.pos(), self._get_color(), self._get_size()))
            self.update()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton and self.drawing:
            self.drawing = False
            self.paths.append(list(self.current_path))
            self.current_path = []

    def _get_color(self):
        return self.color_ref.current_color if self.color_ref else QColor("white")
    
    def _get_size(self):
        return self.pen_size_ref.value() if self.pen_size_ref else 4

    def clear(self):
        self.paths = []
        self.current_path = []
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.fillRect(self.rect(), QColor("#1a1a1a"))
        for path in self.paths + [self.current_path]:
            for i in range(1, len(path)):
                p1, c1, s1 = path[i-1]
                p2, c2, s2 = path[i]
                pen = QPen(c1, s1, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
                p.setPen(pen)
                p.drawLine(p1, p2)


# ═══════════════════════════════════════════════════════════════════════════════
#  CALENDAR APP
# ═══════════════════════════════════════════════════════════════════════════════
class CalendarApp(QWidget):
    def __init__(self, state):
        super().__init__()
        self.state = state
        self.today = QDate.currentDate()
        self.current = self.today
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        nav = QHBoxLayout()
        pb = QPushButton("◀")
        pb.setFixedSize(32, 32)
        pb.setStyleSheet("QPushButton { background: rgba(0,212,255,0.15); color: white; border: none; border-radius: 7px; font-size: 14px; } QPushButton:hover { background: rgba(0,212,255,0.3); }")
        pb.clicked.connect(self._prev)
        nav.addWidget(pb)
        
        self.month_lbl = QLabel("")
        self.month_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.month_lbl.setStyleSheet("color: white; font-size: 18px; font-weight: 600;")
        nav.addWidget(self.month_lbl, 1)
        
        nb = QPushButton("▶")
        nb.setFixedSize(32, 32)
        nb.setStyleSheet(pb.styleSheet())
        nb.clicked.connect(self._next)
        nav.addWidget(nb)
        layout.addLayout(nav)
        
        self.grid = QGridLayout()
        self.grid.setSpacing(4)
        for i, day in enumerate(["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]):
            lbl = QLabel(day)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("color: rgba(0,212,255,0.6); font-size: 12px; font-weight: 700;")
            self.grid.addWidget(lbl, 0, i)
        layout.addLayout(self.grid)
        layout.addStretch()
        self._render()

    def _render(self):
        for i in range(self.grid.count() - 7):
            item = self.grid.itemAt(i + 7)
            if item and item.widget():
                item.widget().deleteLater()
        self.month_lbl.setText(self.current.toString("MMMM yyyy"))
        first = QDate(self.current.year(), self.current.month(), 1)
        dow = first.dayOfWeek() - 1
        days = self.current.daysInMonth()
        for d in range(1, days + 1):
            date = QDate(self.current.year(), self.current.month(), d)
            pos = dow + d - 1
            row = pos // 7 + 1
            col = pos % 7
            btn = QPushButton(str(d))
            btn.setFixedSize(44, 38)
            is_today = date == self.today
            is_weekend = col >= 5
            bg = "rgba(0,212,255,0.3)" if is_today else ("rgba(123,47,255,0.15)" if is_weekend else "rgba(255,255,255,0.05)")
            border = "1px solid #00D4FF" if is_today else "1px solid rgba(255,255,255,0.06)"
            btn.setStyleSheet(f"QPushButton {{ background: {bg}; color: white; border: {border}; border-radius: 8px; font-size: 13px; {'font-weight: 700;' if is_today else ''} }} QPushButton:hover {{ background: rgba(0,212,255,0.2); }}")
            self.grid.addWidget(btn, row, col)

    def _prev(self):
        self.current = self.current.addMonths(-1)
        self._render()

    def _next(self):
        self.current = self.current.addMonths(1)
        self._render()


# ═══════════════════════════════════════════════════════════════════════════════
#  RECYCLE BIN APP
# ═══════════════════════════════════════════════════════════════════════════════
class RecycleBinApp(QWidget):
    def __init__(self, state):
        super().__init__()
        self.state = state
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)
        
        hdr = QHBoxLayout()
        title = QLabel("🗑️  Recycle Bin")
        title.setStyleSheet("color: white; font-size: 16px; font-weight: 600;")
        hdr.addWidget(title)
        hdr.addStretch()
        
        eb = QPushButton("🗑 Empty")
        eb.setStyleSheet("QPushButton { background: rgba(255,61,87,0.3); color: white; border: none; border-radius: 7px; font-size: 12px; padding: 0 14px; height: 30px; } QPushButton:hover { background: rgba(255,61,87,0.5); }")
        eb.setFixedHeight(30)
        eb.clicked.connect(self._empty)
        hdr.addWidget(eb)
        layout.addLayout(hdr)
        
        self.list = QListWidget()
        self.list.setStyleSheet("QListWidget { background: rgba(255,255,255,0.03); color: white; border: 1px solid rgba(255,61,87,0.15); border-radius: 8px; padding: 6px; font-size: 13px; } QListWidget::item { padding: 8px 12px; border-radius: 6px; margin: 1px; } QListWidget::item:hover { background: rgba(255,61,87,0.1); } QListWidget::item:selected { background: rgba(255,61,87,0.3); }")
        layout.addWidget(self.list, 1)
        
        rb = QPushButton("↩ Restore Selected")
        rb.setFixedHeight(36)
        rb.setStyleSheet("QPushButton { background: rgba(0,212,255,0.2); color: white; border: none; border-radius: 8px; font-size: 13px; } QPushButton:hover { background: rgba(0,212,255,0.35); }")
        rb.clicked.connect(self._restore)
        layout.addWidget(rb)
        self._refresh()

    def _refresh(self):
        self.list.clear()
        for item in self.state.recycle_bin:
            self.list.addItem(f"🗑️  {item['name']}")

    def _empty(self):
        if QMessageBox.question(self, "Empty", "Permanently delete all items?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            self.state.recycle_bin.clear()
            self._refresh()

    def _restore(self):
        idx = self.list.currentRow()
        if idx >= 0:
            item = self.state.recycle_bin.pop(idx)
            self.state.add_notification(f"Restored: {item['name']}", "↩")
            self._refresh()


# ═══════════════════════════════════════════════════════════════════════════════
#  ABOUT APP
# ═══════════════════════════════════════════════════════════════════════════════
class AboutApp(QWidget):
    def __init__(self, state):
        super().__init__()
        self.state = state
        self._setup_ui()
        t = QTimer(self)
        t.timeout.connect(self._update_ram)
        t.start(3000)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 24, 30, 24)
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        logo = QLabel("⬡  NOVA OS")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setFont(QFont("Segoe UI Light", 40))
        logo.setStyleSheet("color: #00D4FF; letter-spacing: 6px;")
        layout.addWidget(logo)
        
        tag = QLabel(" NOVAOS Edition — University OS Simulator")
        tag.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tag.setStyleSheet("color: rgba(255,255,255,0.45); font-size: 12px; letter-spacing: 2px;")
        layout.addWidget(tag)
        layout.addSpacing(10)
        
        for label, value in [
            ("Version", "NOVA OS 1.0 / NOVAOS Edition"),
            ("Framework", "Python 3.x + PyQt6"),
            ("Architecture", "x86_64 (Simulated)"),
            ("Kernel", "NOVA OS Kernel 1.0"),
            ("Desktop", "NOVA OS Desktop Environment"),
            ("Total RAM", f"{self.state.total_ram} MB (Simulated)"),
        ]:
            row = QFrame()
            row.setStyleSheet("background: rgba(0,212,255,0.05); border-radius: 8px; border: 1px solid rgba(0,212,255,0.1);")
            rl = QHBoxLayout(row)
            rl.setContentsMargins(14, 8, 14, 8)
            kl = QLabel(label)
            kl.setStyleSheet("color: rgba(255,255,255,0.45); font-size: 12px; min-width: 110px;")
            vl = QLabel(value)
            vl.setStyleSheet("color: white; font-size: 12px;")
            rl.addWidget(kl)
            rl.addWidget(vl)
            rl.addStretch()
            layout.addWidget(row)
        
        layout.addSpacing(8)
        self.ram_bar = QProgressBar()
        self.ram_bar.setRange(0, self.state.total_ram)
        self.ram_bar.setFixedHeight(8)
        self.ram_bar.setTextVisible(False)
        self.ram_bar.setStyleSheet("QProgressBar { background: rgba(255,255,255,0.08); border-radius: 4px; border: none; } QProgressBar::chunk { background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #00D4FF,stop:1 #7B2FFF); border-radius: 4px; }")
        layout.addWidget(self.ram_bar)
        
        self.ram_lbl = QLabel()
        self.ram_lbl.setStyleSheet("color: rgba(255,255,255,0.4); font-size: 11px;")
        layout.addWidget(self.ram_lbl)
        self._update_ram()
        layout.addStretch()
        
        copy = QLabel("© 2026 NOVA OS Project – University Edition\nBuilt with PyQt6 and ❤️")
        copy.setAlignment(Qt.AlignmentFlag.AlignCenter)
        copy.setStyleSheet("color: rgba(255,255,255,0.2); font-size: 11px;")
        layout.addWidget(copy)

    def _update_ram(self):
        self.ram_bar.setValue(self.state.used_ram)
        self.ram_lbl.setText(f"  RAM: {self.state.used_ram} MB used of {self.state.total_ram} MB")


# ═══════════════════════════════════════════════════════════════════════════════
#  WIFI APP
# ═══════════════════════════════════════════════════════════════════════════════
FAKE_NETWORKS = [
    {"ssid": "NOVA OS-Network", "strength": 95, "secured": False},
    {"ssid": "Home_5G", "strength": 78, "secured": True},
    {"ssid": "Work", "strength": 62, "secured": True},
    {"ssid": "Guest", "strength": 55, "secured": False},
    {"ssid": "AndroidHotspot", "strength": 40, "secured": True},
    {"ssid": "Neighbor", "strength": 25, "secured": True},
]

class WiFiApp(QWidget):
    def __init__(self, state):
        super().__init__()
        self.state = state
        self._setup_ui()
        self._apply_initial_status()
        self._refresh()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(10)
        
        hdr = QHBoxLayout()
        title = QLabel("📶  WiFi Manager")
        title.setStyleSheet("color: white; font-size: 16px; font-weight: 600;")
        hdr.addWidget(title)
        hdr.addStretch()
        
        sb = QPushButton("⟳  Scan")
        sb.setFixedHeight(30)
        sb.clicked.connect(self._refresh)
        sb.setStyleSheet("QPushButton { background: rgba(0,212,255,0.25); color: white; border: none; border-radius: 6px; font-size: 12px; padding: 0 12px; } QPushButton:hover { background: rgba(0,212,255,0.45); }")
        hdr.addWidget(sb)
        layout.addLayout(hdr)
        
        self.status_card = QFrame()
        self.status_card.setStyleSheet("background: rgba(0,212,255,0.12); border: 1px solid rgba(0,212,255,0.3); border-radius: 10px;")
        scl = QHBoxLayout(self.status_card)
        scl.setContentsMargins(14, 10, 14, 10)
        
        self.status_icon = QLabel("📶")
        self.status_icon.setStyleSheet("font-size: 22px; background: transparent; border: none;")
        scl.addWidget(self.status_icon)
        
        si = QVBoxLayout()
        si.setSpacing(2)
        self.status_title = QLabel("Connected")
        self.status_title.setStyleSheet("color: #00E676; font-size: 13px; font-weight: 600; background: transparent; border: none;")
        si.addWidget(self.status_title)
        self.status_net = QLabel(self.state.wifi_name)
        self.status_net.setStyleSheet("color: rgba(255,255,255,0.6); font-size: 12px; background: transparent; border: none;")
        si.addWidget(self.status_net)
        scl.addLayout(si)
        scl.addStretch()
        
        db = QPushButton("Disconnect")
        db.setFixedSize(100, 28)
        db.setStyleSheet("QPushButton { background: rgba(255,61,87,0.3); color: white; border: none; border-radius: 6px; font-size: 12px; } QPushButton:hover { background: rgba(255,61,87,0.6); }")
        db.clicked.connect(self._disconnect)
        scl.addWidget(db)
        layout.addWidget(self.status_card)
        
        nl = QLabel("Available Networks")
        nl.setStyleSheet("color: rgba(255,255,255,0.45); font-size: 11px; letter-spacing: 0.5px; font-weight: 600;")
        layout.addWidget(nl)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent; border: none;")
        
        self.nc = QWidget()
        self.nc.setStyleSheet("background: transparent;")
        self.nl = QVBoxLayout(self.nc)
        self.nl.setContentsMargins(0, 0, 0, 0)
        self.nl.setSpacing(6)
        scroll.setWidget(self.nc)
        layout.addWidget(scroll, 1)

    def _apply_initial_status(self):
        if self.state.wifi_connected:
            self.status_card.setStyleSheet("background: rgba(0,212,255,0.12); border: 1px solid rgba(0,212,255,0.3); border-radius: 10px;")
            self.status_title.setText("Connected")
            self.status_title.setStyleSheet("color: #00E676; font-size: 13px; font-weight: 600; background: transparent; border: none;")
            self.status_net.setText(self.state.wifi_name)
        else:
            self.status_card.setStyleSheet("background: rgba(255,61,87,0.1); border: 1px solid rgba(255,61,87,0.35); border-radius: 10px;")
            self.status_title.setText("Disconnected")
            self.status_title.setStyleSheet("color: #FF3D57; font-size: 13px; font-weight: 600; background: transparent; border: none;")
            self.status_net.setText("Not connected")

    def _refresh(self):
        while self.nl.count():
            item = self.nl.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        for net in FAKE_NETWORKS:
            s = net["strength"]
            sig = "▂▄▆█" if s >= 80 else ("▂▄▆░" if s >= 60 else ("▂▄░░" if s >= 40 else "▂░░░"))
            card = QFrame()
            is_conn = net["ssid"] == self.state.wifi_name and self.state.wifi_connected
            card.setStyleSheet(f"QFrame {{ background: {'rgba(0,212,255,0.1)' if is_conn else 'rgba(255,255,255,0.04)'}; border: 1px solid {'rgba(0,212,255,0.3)' if is_conn else 'rgba(255,255,255,0.08)'}; border-radius: 10px; }}")
            cl = QHBoxLayout(card)
            cl.setContentsMargins(14, 10, 14, 10)
            lock = QLabel("🔒" if net["secured"] else "🔓")
            lock.setStyleSheet("font-size: 14px; background: transparent; border: none;")
            cl.addWidget(lock)
            info = QVBoxLayout()
            info.setSpacing(2)
            nn = QLabel(net["ssid"])
            nn.setStyleSheet(f"color: {'#00D4FF' if is_conn else 'white'}; font-size: 13px; font-weight: 600; background: transparent; border: none;")
            info.addWidget(nn)
            st = QLabel(f"{sig}  {net['strength']}%  {'• Connected' if is_conn else ''}")
            st.setStyleSheet("color: rgba(255,255,255,0.5); font-size: 11px; background: transparent; border: none;")
            info.addWidget(st)
            cl.addLayout(info, 1)
            if not is_conn:
                cb = QPushButton("Connect")
                cb.setFixedSize(80, 28)
                cb.setStyleSheet("QPushButton { background: rgba(0,212,255,0.25); color: white; border: none; border-radius: 6px; font-size: 12px; } QPushButton:hover { background: rgba(0,212,255,0.45); }")
                cb.clicked.connect(lambda c=False, ssid=net["ssid"]: self._connect(ssid))
                cl.addWidget(cb)
            self.nl.addWidget(card)
        self.nl.addStretch()

    def _connect(self, ssid):
        self.state.wifi_connected = True
        self.state.wifi_name = ssid
        self.state.save_settings()
        self.status_card.setStyleSheet("background: rgba(0,212,255,0.12); border: 1px solid rgba(0,212,255,0.3); border-radius: 10px;")
        self.status_title.setText("Connected")
        self.status_title.setStyleSheet("color: #00E676; font-size: 13px; font-weight: 600; background: transparent; border: none;")
        self.status_net.setText(ssid)
        self.state.add_notification(f"Connected to {ssid}", "📶")
        self._refresh()

    def _disconnect(self):
        self.state.wifi_connected = False
        self.state.save_settings()
        self.status_card.setStyleSheet("background: rgba(255,61,87,0.1); border: 1px solid rgba(255,61,87,0.35); border-radius: 10px;")
        self.status_title.setText("Disconnected")
        self.status_title.setStyleSheet("color: #FF3D57; font-size: 13px; font-weight: 600; background: transparent; border: none;")
        self.status_net.setText("Not connected")
        self._refresh()


# ═══════════════════════════════════════════════════════════════════════════════
#  SETTINGS APP
# ═══════════════════════════════════════════════════════════════════════════════
class SettingsApp(QWidget):
    def __init__(self, state, desktop):
        super().__init__()
        self.state = state
        self.desktop = desktop
        self.custom_wallpaper_path = None
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        header = QFrame()
        header.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 {self.state.accent_color},stop:1 #7B2FFF);
                border-radius: 12px;
            }}
        """)
        header.setFixedHeight(80)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(24, 0, 24, 0)
        
        icon_lbl = QLabel("⚙️")
        icon_lbl.setStyleSheet("font-size: 36px; background: transparent; border: none;")
        header_layout.addWidget(icon_lbl)
        
        title_lbl = QLabel("Settings")
        title_lbl.setStyleSheet("color: white; font-size: 24px; font-weight: 700; background: transparent; border: none;")
        header_layout.addWidget(title_lbl)
        header_layout.addStretch()
        
        layout.addWidget(header)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setStyleSheet("QSplitter::handle { background: rgba(0,212,255,0.1); width: 1px; }")

        sidebar = QFrame()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("""
            QFrame {
                background: rgba(15,22,40,0.6);
                border-radius: 12px;
            }
        """)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(8, 16, 8, 16)
        sidebar_layout.setSpacing(4)

        categories = [
            ("🎨", "Appearance", 0),
            ("🖼️", "Wallpaper", 1),
            ("🔊", "Sound", 2),
            ("👤", "Account", 3),
            ("🔐", "Security", 4),
            ("ℹ️", "About", 5),
        ]

        for icon, name, idx in categories:
            btn = QPushButton(f"  {icon}  {name}")
            btn.setFixedHeight(44)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    color: rgba(255,255,255,0.7);
                    border: none;
                    border-radius: 8px;
                    font-size: 13px;
                    text-align: left;
                    padding-left: 12px;
                }
                QPushButton:hover {
                    background: rgba(0,212,255,0.15);
                    color: white;
                }
            """)
            btn.clicked.connect(lambda checked, i=idx: self.stack.setCurrentIndex(i))
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()
        splitter.addWidget(sidebar)

        self.stack = QStackedWidget()
        self.stack.setStyleSheet("""
            QStackedWidget {
                background: rgba(15,22,40,0.6);
                border-radius: 12px;
            }
        """)
        
        self.stack.addWidget(self._make_appearance())
        self.stack.addWidget(self._make_wallpaper())
        self.stack.addWidget(self._make_sound())
        self.stack.addWidget(self._make_account())
        self.stack.addWidget(self._make_security())
        self.stack.addWidget(self._make_about())
        
        splitter.addWidget(self.stack)
        splitter.setSizes([220, 600])
        
        layout.addWidget(splitter, 1)

    def _card(self, title):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: rgba(10,14,26,0.8);
                border-radius: 12px;
                border: 1px solid rgba(0,212,255,0.1);
            }
        """)
        
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(0)
        
        header = QLabel(f"  {title}")
        header.setFixedHeight(40)
        header.setStyleSheet("""
            color: #00D4FF;
            font-size: 13px;
            font-weight: 600;
            background: rgba(0,212,255,0.08);
            border-radius: 12px 12px 0 0;
            border-bottom: 1px solid rgba(0,212,255,0.1);
            padding: 0 12px;
        """)
        card_layout.addWidget(header)
        
        content = QWidget()
        content.setStyleSheet("background: transparent;")
        card_layout.addWidget(content)
        
        return card, content

    def _make_appearance(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        accent_card, accent_content = self._card("Accent Color")
        layout.addWidget(accent_card)
        
        accent_layout = QHBoxLayout(accent_content)
        accent_layout.setContentsMargins(16, 16, 16, 16)
        accent_layout.setSpacing(12)
        
        for name, color in ACCENT_COLORS.items():
            btn = QPushButton(name)
            btn.setFixedSize(90, 40)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            is_selected = self.state.accent_color == color
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: {color};
                    color: white;
                    border: {3 if is_selected else 0}px solid white;
                    border-radius: 8px;
                    font-size: 11px;
                    font-weight: 600;
                }}
                QPushButton:hover {{
                    opacity: 0.85;
                }}
            """)
            btn.clicked.connect(lambda checked, col=color: self._set_accent(col))
            accent_layout.addWidget(btn)
        accent_layout.addStretch()
        
        theme_card, theme_content = self._card("Theme")
        layout.addWidget(theme_card)
        
        theme_layout = QHBoxLayout(theme_content)
        theme_layout.setContentsMargins(16, 16, 16, 16)
        theme_layout.setSpacing(16)
        
        dark_btn = QPushButton("🌙  Dark")
        dark_btn.setFixedSize(140, 50)
        dark_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        dark_btn.setStyleSheet("""
            QPushButton {
                background: rgba(0,212,255,0.15);
                color: white;
                border: 2px solid #00D4FF;
                border-radius: 10px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: rgba(0,212,255,0.3);
            }
        """)
        dark_btn.clicked.connect(lambda: self._set_theme("dark"))
        theme_layout.addWidget(dark_btn)
        
        theme_layout.addStretch()
        layout.addStretch()
        return widget

    def _set_accent(self, color):
        self.state.set_accent(color)
        global ACCENT
        ACCENT = color

        # Update taskbar start button immediately
        if hasattr(self.desktop, 'taskbar'):
            self.desktop.taskbar.start_btn.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 {color},stop:1 #7B2FFF);
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-size: 13px;
                    font-weight: 600;
                    letter-spacing: 1px;
                }}
                QPushButton:hover {{ opacity: 0.85; }}
            """)
            self.desktop.taskbar.repaint()

        # Update Settings header gradient
        for child in self.findChildren(QFrame):
            ss = child.styleSheet()
            if 'qlineargradient' in ss and '7B2FFF' in ss and child.height() == 80:
                child.setStyleSheet(f"""
                    QFrame {{
                        background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 {color},stop:1 #7B2FFF);
                        border-radius: 12px;
                    }}
                """)
                break

        # Rebuild Appearance tab so accent button borders refresh instantly
        current_index = self.stack.currentIndex()
        old_widget = self.stack.widget(0)
        new_widget = self._make_appearance()
        self.stack.removeWidget(old_widget)
        old_widget.deleteLater()
        self.stack.insertWidget(0, new_widget)
        self.stack.setCurrentIndex(current_index)

        self.desktop.update()
        accent_name = [k for k, v in ACCENT_COLORS.items() if v == color]
        if accent_name:
            self.state.add_notification(f"Accent color changed to {accent_name[0]}", "🎨")

    def _set_theme(self, theme):
        self.state.set_theme(theme)
        app = QApplication.instance()
        
        if theme == "dark":
            app.setStyleSheet("""
                QToolTip { background: #0F1628; color: white; border: 1px solid rgba(0,212,255,0.3); padding: 4px 8px; border-radius: 6px; font-size: 12px; }
                QScrollBar:vertical { background: #0A0E1A; width: 8px; border-radius: 4px; }
                QScrollBar::handle:vertical { background: #1C2A47; border-radius: 4px; }
                QScrollBar:horizontal { background: #0A0E1A; height: 8px; border-radius: 4px; }
                QScrollBar::handle:horizontal { background: #1C2A47; border-radius: 4px; }
                QMenu { background: rgba(10,16,30,0.97); color: white; border: 1px solid rgba(0,212,255,0.2); border-radius: 10px; padding: 6px; }
                QMenu::item { padding: 7px 22px 7px 12px; border-radius: 6px; }
                QMenu::item:selected { background: rgba(0,212,255,0.25); }
            """)
        else:
            app.setStyleSheet("""
                QToolTip { background: #E8F0FF; color: #0A0E1A; border: 1px solid #00D4FF; padding: 4px 8px; border-radius: 6px; }
                QScrollBar:vertical { background: #E8F0FF; width: 8px; border-radius: 4px; }
                QScrollBar::handle:vertical { background: #6B7FA3; border-radius: 4px; }
                QScrollBar:horizontal { background: #E8F0FF; height: 8px; border-radius: 4px; }
                QScrollBar::handle:horizontal { background: #6B7FA3; border-radius: 4px; }
                QMenu { background: #E8F0FF; color: #0A0E1A; border: 1px solid #00D4FF; border-radius: 10px; }
                QMenu::item { padding: 7px 22px 7px 12px; border-radius: 6px; }
                QMenu::item:selected { background: #00D4FF; color: white; }
            """)
        
        self.state.add_notification(f"Theme changed to {theme}", "🎨")
        self.desktop.update()

    def _make_wallpaper(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        builtin_card, builtin_content = self._card("Built-in Wallpapers")
        layout.addWidget(builtin_card)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent; border: none;")
        
        wallpaper_grid = QWidget()
        grid_layout = QGridLayout(wallpaper_grid)
        grid_layout.setSpacing(12)
        grid_layout.setContentsMargins(16, 16, 16, 16)
        
        all_wallpapers = {**WALLPAPER_NAMES}
        if hasattr(self.state, 'custom_wallpaper_path') and self.state.custom_wallpaper_path:
            custom_key = f"custom_{Path(self.state.custom_wallpaper_path).stem}"
            all_wallpapers[custom_key] = f"📷 {Path(self.state.custom_wallpaper_path).name}"
        
        for i, (key, label) in enumerate(all_wallpapers.items()):
            row, col = divmod(i, 3)
            
            preview = QFrame()
            preview.setFixedSize(180, 120)
            preview.setCursor(Qt.CursorShape.PointingHandCursor)
            
            if key.startswith("custom_") and hasattr(self.state, 'custom_wallpaper_path') and self.state.custom_wallpaper_path:
                preview.setStyleSheet(f"""
                    QFrame {{
                        background: rgba(0,0,0,0.5);
                        border-radius: 10px;
                        border: {2 if self.state.wallpaper == key else 1}px solid {('white' if self.state.wallpaper == key else 'rgba(255,255,255,0.2)')};
                        background-image: url({self.state.custom_wallpaper_path});
                        background-position: center;
                        background-repeat: no-repeat;
                        background-size: cover;
                    }}
                    QFrame:hover {{
                        border: 2px solid #00D4FF;
                    }}
                """)
            else:
                colors = WALLPAPERS.get(key, WALLPAPERS["gradient_nova"])
                gradient = f"qlineargradient(x1:0,y1:0,x2:1,y2:1,"
                for j, c in enumerate(colors):
                    if hasattr(c, 'name'):
                        gradient += f"stop:{j/len(colors)} {c.name()},"
                    else:
                        gradient += f"stop:{j/len(colors)} {c},"
                gradient = gradient.rstrip(',') + ")"
                
                preview.setStyleSheet(f"""
                    QFrame {{
                        background: {gradient};
                        border-radius: 10px;
                        border: {2 if self.state.wallpaper == key else 1}px solid {('white' if self.state.wallpaper == key else 'rgba(255,255,255,0.2)')};
                    }}
                    QFrame:hover {{
                        border: 2px solid #00D4FF;
                    }}
                """)
            
            preview_layout = QVBoxLayout(preview)
            preview_layout.setContentsMargins(0, 0, 0, 0)
            
            name_lbl = QLabel(label)
            name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            name_lbl.setStyleSheet("color: white; background: rgba(0,0,0,0.5); border-radius: 0 0 10px 10px; padding: 6px; font-size: 11px;")
            preview_layout.addStretch()
            preview_layout.addWidget(name_lbl)
            
            preview.mousePressEvent = lambda e, k=key: self._set_wallpaper(k)
            
            grid_layout.addWidget(preview, row, col)
        
        scroll.setWidget(wallpaper_grid)
        
        builtin_content_layout = QVBoxLayout(builtin_content)
        builtin_content_layout.setContentsMargins(0, 0, 0, 0)
        builtin_content_layout.addWidget(scroll)
        
        custom_card, custom_content = self._card("Custom Wallpaper")
        layout.addWidget(custom_card)
        
        custom_layout = QVBoxLayout(custom_content)
        custom_layout.setContentsMargins(16, 16, 16, 16)
        custom_layout.setSpacing(12)
        
        browse_btn = QPushButton("📁  Browse for Image...")
        browse_btn.setFixedHeight(48)
        browse_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        browse_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #7B2FFF,stop:1 #00D4FF);
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover {
                opacity: 0.85;
            }
        """)
        browse_btn.clicked.connect(self._browse_wallpaper)
        custom_layout.addWidget(browse_btn)
        
        self.custom_preview = QLabel("No custom wallpaper selected")
        self.custom_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.custom_preview.setFixedHeight(100)
        self.custom_preview.setStyleSheet("""
            QLabel {
                background: rgba(255,255,255,0.05);
                border-radius: 8px;
                color: rgba(255,255,255,0.4);
                font-size: 12px;
            }
        """)
        custom_layout.addWidget(self.custom_preview)
        
        if hasattr(self.state, 'custom_wallpaper_path') and self.state.custom_wallpaper_path:
            self.custom_preview.setText(f"✅ Loaded: {Path(self.state.custom_wallpaper_path).name}")
            self.custom_preview.setStyleSheet("""
                QLabel {
                    background: rgba(0,212,255,0.1);
                    border-radius: 8px;
                    color: #00E676;
                    font-size: 12px;
                }
            """)
        
        layout.addStretch()
        return widget

    def _set_wallpaper(self, key):
        if key.startswith("custom_"):
            self.state.set_wallpaper(key, self.state.custom_wallpaper_path)
        else:
            self.state.set_wallpaper(key)
        self.desktop.update()
        
        current_index = self.stack.currentIndex()
        self.stack.widget(1).deleteLater()
        self.stack.insertWidget(1, self._make_wallpaper())
        self.stack.setCurrentIndex(current_index)
        
        if key.startswith("custom_"):
            self.state.add_notification("Custom wallpaper applied", "🖼️")
        else:
            self.state.add_notification(f"Wallpaper changed to {WALLPAPER_NAMES.get(key, key)}", "🖼️")

    def _browse_wallpaper(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Wallpaper Image",
            str(Path.home()),
            "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        
        if file_path:
            self.state.set_wallpaper(f"custom_{Path(file_path).stem}", file_path)
            self.desktop.update()
            
            self.custom_preview.setText(f"✅ Loaded: {Path(file_path).name}")
            self.custom_preview.setStyleSheet("""
                QLabel {
                    background: rgba(0,212,255,0.1);
                    border-radius: 8px;
                    color: #00E676;
                    font-size: 12px;
                }
            """)
            
            current_index = self.stack.currentIndex()
            self.stack.widget(1).deleteLater()
            self.stack.insertWidget(1, self._make_wallpaper())
            self.stack.setCurrentIndex(current_index)
            
            self.state.add_notification(f"Custom wallpaper loaded: {Path(file_path).name}", "🖼️")

    def _make_sound(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        sound_card, sound_content = self._card("🔊  Volume Control")
        layout.addWidget(sound_card)

        sound_layout = QVBoxLayout(sound_content)
        sound_layout.setContentsMargins(20, 20, 20, 20)
        sound_layout.setSpacing(16)

        # Icon + percentage row
        top_row = QHBoxLayout()
        self._vol_icon_lbl = QLabel()
        self._vol_icon_lbl.setStyleSheet("font-size: 32px; background: transparent; border: none;")
        top_row.addWidget(self._vol_icon_lbl)

        vol_info = QVBoxLayout()
        vol_info.setSpacing(2)
        self.vol_lbl = QLabel()
        self.vol_lbl.setStyleSheet("color: white; font-size: 18px; font-weight: 700; background: transparent; border: none;")
        vol_info.addWidget(self.vol_lbl)

        vol_sub = QLabel("Drag to adjust system volume")
        vol_sub.setStyleSheet("color: rgba(255,255,255,0.4); font-size: 11px; background: transparent; border: none;")
        vol_info.addWidget(vol_sub)
        top_row.addLayout(vol_info)
        top_row.addStretch()
        sound_layout.addLayout(top_row)

        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(self.state.volume)
        self.volume_slider.setFixedHeight(28)
        self.volume_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: rgba(255,255,255,0.08);
                height: 8px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: qradialgradient(cx:0.5,cy:0.5,radius:0.5,fx:0.5,fy:0.5,stop:0 white,stop:0.45 #00D4FF,stop:1 rgba(0,212,255,0));
                width: 20px;
                height: 20px;
                border-radius: 10px;
                margin: -6px 0;
            }
            QSlider::sub-page:horizontal {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #7B2FFF,stop:1 #00D4FF);
                border-radius: 4px;
            }
        """)
        self.volume_slider.valueChanged.connect(self._change_volume)
        sound_layout.addWidget(self.volume_slider)

        # Quick preset buttons
        presets_row = QHBoxLayout()
        presets_row.setSpacing(8)
        for label, val in [("🔇 Mute", 0), ("🔈 Low", 25), ("🔉 Mid", 60), ("🔊 Max", 100)]:
            pb = QPushButton(label)
            pb.setFixedHeight(30)
            pb.setCursor(Qt.CursorShape.PointingHandCursor)
            pb.setStyleSheet("""
                QPushButton { background: rgba(0,212,255,0.1); color: rgba(255,255,255,0.7);
                              border: 1px solid rgba(0,212,255,0.2); border-radius: 8px; font-size: 11px; }
                QPushButton:hover { background: rgba(0,212,255,0.3); color: white; }
            """)
            pb.clicked.connect(lambda c=False, v=val, sl=self.volume_slider: sl.setValue(v))
            presets_row.addWidget(pb)
        sound_layout.addLayout(presets_row)

        layout.addStretch()
        # Initialise display
        self._update_vol_display(self.state.volume)
        return widget

    def _update_vol_display(self, value):
        icon = "🔇" if value == 0 else ("🔈" if value < 35 else ("🔉" if value < 70 else "🔊"))
        if hasattr(self, '_vol_icon_lbl'):
            self._vol_icon_lbl.setText(icon)
        if hasattr(self, 'vol_lbl'):
            self.vol_lbl.setText(f"{value}%")

    def _change_volume(self, value):
        self.state.set_volume(value)
        icon = "🔇" if value == 0 else ("🔈" if value < 35 else ("🔉" if value < 70 else "🔊"))
        self._update_vol_display(value)
        self.vol_lbl.setText(f"{value}%")
        if hasattr(self.desktop, 'taskbar') and hasattr(self.desktop.taskbar, 'vol_btn'):
            self.desktop.taskbar.vol_btn.setText(icon)
            self.desktop.taskbar.vol_btn.setToolTip(f"Volume: {value}%")

    def _make_account(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        profile_card, profile_content = self._card("Profile Information")
        layout.addWidget(profile_card)
        
        profile_layout = QVBoxLayout(profile_content)
        profile_layout.setContentsMargins(20, 20, 20, 20)
        profile_layout.setSpacing(16)
        
        avatar = QLabel("👤")
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet("font-size: 64px; background: transparent; border: none;")
        profile_layout.addWidget(avatar)
        
        info_frame = QFrame()
        info_frame.setStyleSheet("background: rgba(255,255,255,0.05); border-radius: 10px;")
        info_layout = QVBoxLayout(info_frame)
        info_layout.setSpacing(8)
        
        for label, value in [
            ("Display Name:", self.state.get_display_name()),
            ("Username:", self.state.current_user or "?"),
            ("Role:", self.state.get_role().capitalize())
        ]:
            row = QHBoxLayout()
            lbl = QLabel(label)
            lbl.setStyleSheet("color: rgba(255,255,255,0.5); font-size: 12px; min-width: 110px;")
            val = QLabel(value)
            val.setStyleSheet("color: white; font-size: 13px; font-weight: 600;")
            row.addWidget(lbl)
            row.addWidget(val)
            row.addStretch()
            info_layout.addLayout(row)
        
        profile_layout.addWidget(info_frame)
        layout.addStretch()
        return widget

    def _make_security(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        security_card, security_content = self._card("Security Options")
        layout.addWidget(security_card)
        
        security_layout = QVBoxLayout(security_content)
        security_layout.setContentsMargins(20, 20, 20, 20)
        security_layout.setSpacing(12)
        
        for text, icon, color, action in [
            ("Change Password", "🔑", "rgba(0,212,255,0.2)", self._chg_pw),
            ("Logout", "🚪", "rgba(255,61,87,0.2)", self._logout),
        ]:
            btn = QPushButton(f"  {icon}  {text}")
            btn.setFixedHeight(48)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: {color};
                    color: white;
                    border: 1px solid rgba(255,255,255,0.1);
                    border-radius: 10px;
                    font-size: 13px;
                    text-align: left;
                    padding-left: 16px;
                }}
                QPushButton:hover {{
                    background: rgba(0,212,255,0.3);
                }}
            """)
            btn.clicked.connect(action)
            security_layout.addWidget(btn)
        
        layout.addStretch()
        return widget

    def _make_about(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        about_card, about_content = self._card("About NOVA OS")
        layout.addWidget(about_card)
        
        about_layout = QVBoxLayout(about_content)
        about_layout.setContentsMargins(30, 30, 30, 30)
        about_layout.setSpacing(16)
        about_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        logo = QLabel("⬡")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet("font-size: 48px; color: #00D4FF; background: transparent; border: none;")
        about_layout.addWidget(logo)
        
        title = QLabel("NOVA OS")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: white; font-size: 28px; font-weight: 300; letter-spacing: 4px;")
        about_layout.addWidget(title)
        
        version = QLabel("Version 1.0.0")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version.setStyleSheet("color: rgba(0,212,255,0.6); font-size: 12px;")
        about_layout.addWidget(version)
        
        info_frame = QFrame()
        info_frame.setStyleSheet("background: rgba(255,255,255,0.05); border-radius: 10px;")
        info_layout = QVBoxLayout(info_frame)
        info_layout.setSpacing(8)
        
        for label, value in [
            ("Edition", "NOVA OS University Edition"),
            ("Framework", "Python 3.x + PyQt6"),
            ("Architecture", platform.machine()),
            ("Kernel", "NOVA Kernel 1.0"),
        ]:
            row = QHBoxLayout()
            lbl = QLabel(f"{label}:")
            lbl.setStyleSheet("color: rgba(255,255,255,0.5); font-size: 12px; min-width: 100px;")
            val = QLabel(value)
            val.setStyleSheet("color: white; font-size: 12px;")
            row.addWidget(lbl)
            row.addWidget(val)
            row.addStretch()
            info_layout.addLayout(row)
        
        about_layout.addWidget(info_frame)
        
        copyright_lbl = QLabel("© 2026 NOVA OS Project – University Edition\nBuilt with ❤️ using PyQt6")
        copyright_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        copyright_lbl.setStyleSheet("color: rgba(255,255,255,0.2); font-size: 11px;")
        about_layout.addWidget(copyright_lbl)
        
        layout.addStretch()
        return widget

    def _chg_pw(self):
        old, ok = QInputDialog.getText(self, "Change Password", "Current password:", QLineEdit.EchoMode.Password)
        if not ok:
            return
        user = self.state.users.get(self.state.current_user, {})
        if user.get("password") != old:
            QMessageBox.warning(self, "Error", "Incorrect current password.")
            return
        new, ok2 = QInputDialog.getText(self, "Change Password", "New password:", QLineEdit.EchoMode.Password)
        if ok2 and new.strip():
            user["password"] = new.strip()
            self.state.save_settings()
            QMessageBox.information(self, "Success", "Password changed.")
            self.state.add_notification("Password changed successfully", "🔑")

    def _lock(self):
        self.state.save_settings()
        lock = LockScreen(self.state)
        lock.show()

    def _logout(self):
        if QMessageBox.question(self, "Logout", "Are you sure?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            self.state.save_settings()
            self.state.current_user = None
            _show_login(self.state)

    def _open_login(self):
        pass

# ═══════════════════════════════════════════════════════════════════════════════
#  GLOBAL LOGIN HELPER  (keeps reference alive so Qt can't GC it)
# ═══════════════════════════════════════════════════════════════════════════════
def _show_login(state):
    global _LOGIN_SCREEN_REF
    # Close all existing windows synchronously first
    for w in list(QApplication.instance().topLevelWidgets()):
        w.close()
    # Now create and show login — app is still alive because quitOnLastWindowClosed=False
    _LOGIN_SCREEN_REF = LoginScreen(state)
    _LOGIN_SCREEN_REF.show()

# ═══════════════════════════════════════════════════════════════════════════════
class VideoLoadingScreen:
    def __init__(self, on_complete=None):
        self.on_complete = on_complete
        self.root = ctk.CTk()
        self.root.overrideredirect(True)
        self.root.configure(fg_color=BG_DEEP)
        w, h = 854, 480
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        self.root.update_idletasks()

        self.label = tk.Label(self.root, bg=BG_DEEP, bd=0)
        self.label.pack(expand=True, fill="both")
        self.label.bind("<Button-1>", self.skip)

        video_path = os.path.join(SCRIPT_DIR, "download.mp4")
        self.cap = None
        if HAS_VIDEO and os.path.exists(video_path):
            self.cap = cv2.VideoCapture(video_path)
            self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30
            self.delay = int(1000 / self.fps)
            self._after_id = None
            self.play()
        else:
            self.label.config(text="NOVA OS\nLoading...", font=("Arial", 24, "bold"), fg="white", bg=BG_DEEP)
            self.root.after(2000, self.finish)
        
        self.root.mainloop()

    def play(self):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.resize(frame, (854, 480))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.label.imgtk = imgtk
                self.label.configure(image=imgtk)
                self._after_id = self.root.after(self.delay, self.play)
            else:
                self.finish()
        else:
            self.finish()

    def skip(self, event=None):
        if self._after_id:
            self.root.after_cancel(self._after_id)
        self.finish()

    def finish(self):
        if self.cap:
            self.cap.release()
        self.root.destroy()
        if self.on_complete:
            # Use QTimer to call the callback after a short delay
            QTimer.singleShot(100, self.on_complete)
            

# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    
    app = QApplication(sys.argv)
    app.setApplicationName("NOVA OS")
    app.setFont(QFont("Segoe UI", 10))
    app.setQuitOnLastWindowClosed(False)
    app.setWindowIcon(QIcon("nova1.ico"))
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("novaos.app")

    app.setStyleSheet("""
        QToolTip { background: #0F1628; color: white; border: 1px solid rgba(0,212,255,0.3); padding: 4px 8px; border-radius: 6px; font-size: 12px; }
        QScrollBar:vertical { background: #0A0E1A; width: 8px; border-radius: 4px; }
        QScrollBar::handle:vertical { background: #1C2A47; border-radius: 4px; }
        QScrollBar:horizontal { background: #0A0E1A; height: 8px; border-radius: 4px; }
        QScrollBar::handle:horizontal { background: #1C2A47; border-radius: 4px; }
        QMenu { background: rgba(10,16,30,0.97); color: white; border: 1px solid rgba(0,212,255,0.2); border-radius: 10px; padding: 6px; }
        QMenu::item { padding: 7px 22px 7px 12px; border-radius: 6px; }
        QMenu::item:selected { background: rgba(0,212,255,0.25); }
        QMenu::separator { height: 1px; background: rgba(255,255,255,0.08); margin: 4px 0; }
    """)

    state = StateManager()
    
    # Show video loading screen first
    video_loading = VideoLoadingScreen()
    
    # After video loading, show login screen
    login = LoginScreen(state)
    login.show()

    sys.exit(app.exec())
    

if __name__ == "__main__":
    video_path = os.path.join(SCRIPT_DIR, "download.mp4")

    main()