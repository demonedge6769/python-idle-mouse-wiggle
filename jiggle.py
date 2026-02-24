import pyautogui
import threading
import time
from random import randrange
import tkinter as tk
import ctypes
import keyboard
import sys

pyautogui.FAILSAFE = False
running = False

# --- Prevent Windows sleep ---
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002


def prevent_sleep():
    ctypes.windll.kernel32.SetThreadExecutionState(
        ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED
    )


def allow_sleep():
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)


def move_mouse():
    global running
    prevent_sleep()
    while running:
        x_offset = randrange(-20, 21)
        y_offset = randrange(-20, 21)
        pyautogui.move(x_offset, y_offset, duration=0.2)
        time.sleep(0.5)
    allow_sleep()


def stop_and_center():
    """Global hotkey: Ctrl + Shift + A + C"""
    global running
    running = False
    w, h = pyautogui.size()
    pyautogui.moveTo(w // 2, h // 2, duration=0.3)
    update_ui()


def update_ui():
    if running:
        start_btn.config(bg="green", fg="red", font=("Arial", 10, "bold"))
        stop_btn.config(bg="SystemButtonFace", fg="black", font=("Arial", 10))
        status_label.config(
            text="Status: RUNNING",
            fg="green",
            font=("Arial", 10, "bold")
        )
    else:
        stop_btn.config(bg="red", fg="yellow", font=("Arial", 10, "bold"))
        start_btn.config(bg="SystemButtonFace", fg="black", font=("Arial", 10))
        status_label.config(
            text="Status: NOT RUNNING",
            fg="red",
            font=("Arial", 10, "bold")
        )


def start():
    global running
    if not running:
        running = True
        threading.Thread(target=move_mouse, daemon=True).start()
    update_ui()


def stop():
    global running
    running = False
    update_ui()


def on_close():
    global running
    running = False
    allow_sleep()
    keyboard.unhook_all_hotkeys()
    root.destroy()


# --- Register global hotkey ---
keyboard.add_hotkey('ctrl+shift+a+c', stop_and_center)

# --- GUI ---
root = tk.Tk()
root.title("Mouse Mover")

start_btn = tk.Button(root, text="Start", width=15, command=start)
start_btn.pack(pady=5)

stop_btn = tk.Button(root, text="Stop", width=15, command=stop)
stop_btn.pack(pady=5)

status_label = tk.Label(root)
status_label.pack(pady=8)

update_ui()
root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
