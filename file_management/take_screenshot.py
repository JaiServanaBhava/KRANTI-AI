import pyautogui
import datetime
import os
import sys
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from backend.app.voice_recognition.voice_feedback import speak

import time


def take_screenshot(save_dir="Screenshots"):
    try:
        # Create directory if not exists
        os.makedirs(save_dir, exist_ok=True)

        # Take screenshot
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filepath = os.path.join(save_dir, f"screenshot_{timestamp}.png")
        screenshot = pyautogui.screenshot()
        screenshot.save(filepath)
        speak(f"Screenshot saved as {filepath}")

        # -------- GUI -------- #
        root = tk.Tk()
        root.title("Screenshot Preview")

        # Convert screenshot to ImageTk
        screenshot_tk = ImageTk.PhotoImage(screenshot)
        label = tk.Label(root, image=screenshot_tk)
        label.pack()

        # -------- Button Functions -------- #
        def save_screenshot():
            # Ask user where to save
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                initialfile=f"screenshot_{int(time.time())}.png"
            )
            if file_path:
                screenshot.save(file_path)
                speak(f"Screenshot saved as {file_path}")
                messagebox.showinfo("Saved", f"Screenshot saved as:\n{file_path}")

        def delete_screenshot():
            nonlocal screenshot
            if messagebox.askyesno("Delete", "Are you sure you want to delete this screenshot?"):
                screenshot = None
                label.config(image='')  # Clear the image
                speak("Screenshot deleted.")
                messagebox.showinfo("Deleted", "Screenshot deleted.")

        # -------- Buttons -------- #
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        save_btn = tk.Button(button_frame, text="Save", command=save_screenshot, width=10, bg="green", fg="white")
        save_btn.pack(side="left", padx=10)

        delete_btn = tk.Button(button_frame, text="Delete", command=delete_screenshot, width=10, bg="red", fg="white")
        delete_btn.pack(side="left", padx=10)

        # Run GUI
        root.mainloop()

    except Exception as e:
        speak(f"Failed to take screenshot. Error: {str(e)}")
