import tkinter as tk
from tkinter import ttk


class CommandWindow:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Commands")
        root.geometry("600x400")

        paned = ttk.PanedWindow(root, orient=tk.VERTICAL)
        paned.pack(fill=tk.BOTH, expand=True)

        log_frame = ttk.Frame(paned)
        paned.add(log_frame, weight=1)

        self.log = tk.Text(
            log_frame,
            state=tk.DISABLED,
            wrap=tk.WORD,
            background="#f0f0f0",
            borderwidth=0,
        )
        log_scroll = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log.yview)
        self.log.configure(yscrollcommand=log_scroll.set)
        self.log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        entry_frame = ttk.Frame(paned)
        paned.add(entry_frame, weight=0)

        self.entry = ttk.Entry(entry_frame)
        self.entry.pack(fill=tk.X, padx=4, pady=4)
        self.entry.bind("<Return>", self._on_return)
        self.entry.focus_set()

    def log_message(self, text: str) -> None:
        self.log.configure(state=tk.NORMAL)
        self.log.insert(tk.END, text + "\n")
        self.log.see(tk.END)
        self.log.configure(state=tk.DISABLED)

    def _on_return(self, _event):
        self.entry.delete(0, tk.END)
        return "break"
