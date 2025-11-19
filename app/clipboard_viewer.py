import tkinter as tk
import pyperclip

clipboard_history = []

def add_history(text):
    if text and text not in clipboard_history:
        clipboard_history.insert(0, text)
        if len(clipboard_history) > 20:
            clipboard_history.pop()


def show_clipboard_window():
    text = pyperclip.paste() or "Clipboard is empty!"
    add_history(text)

    win = tk.Toplevel()
    win.title("Clipboard Viewer")
    win.geometry("450x350")
    win.configure(bg="#1a1a1a")

    tk.Label(
        win, text="📋 Clipboard Content",
        bg="#1a1a1a", fg="white", font=("Arial", 16)
    ).pack(pady=10)

    box = tk.Text(win, bg="#222", fg="white", font=("Arial", 12), wrap="word")
    box.insert("1.0", text)
    box.config(state="disabled")
    box.pack(expand=True, fill="both", padx=15, pady=15)

    tk.Button(
        win, text="Close", bg="#ff4444", fg="white",
        font=("Arial", 12), command=win.destroy
    ).pack(pady=10)


def show_clipboard_history():
    win = tk.Toplevel()
    win.title("Clipboard History")
    win.geometry("450x350")
    win.configure(bg="#1a1a1a")

    tk.Label(
        win, text="📝 Clipboard History",
        bg="#1a1a1a", fg="white", font=("Arial", 16)
    ).pack(pady=10)

    box = tk.Text(win, bg="#222", fg="white", font=("Arial", 12), wrap="word")
    box.pack(expand=True, fill="both", padx=15, pady=15)

    if clipboard_history:
        for clip in clipboard_history:
            box.insert("end", f"- {clip}\n\n")
    else:
        box.insert("end", "No history available.")

    box.config(state="disabled")


def clear_clipboard_data():
    pyperclip.copy("")
    return "Clipboard cleared."
