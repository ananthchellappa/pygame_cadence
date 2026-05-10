import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional


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

        self.prompt_var = tk.StringVar(value=">>> ")
        prompt_label = ttk.Label(
            entry_frame, textvariable=self.prompt_var, font=("TkFixedFont", 10)
        )
        prompt_label.pack(side=tk.LEFT, padx=(4, 0), pady=4)

        self.entry = ttk.Entry(entry_frame)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4, pady=4)
        self.entry.bind("<Return>", self._on_return)
        self.entry.focus_set()

        self._execute: Optional[Callable[[str], bool]] = None

    def set_executor(self, execute_fn: Callable[[str], bool]) -> None:
        self._execute = execute_fn

    def log_message(self, text: str) -> None:
        self.log.configure(state=tk.NORMAL)
        self.log.insert(tk.END, text + "\n")
        self.log.see(tk.END)
        self.log.configure(state=tk.DISABLED)

    def _on_return(self, _event):
        line = self.entry.get()
        self.entry.delete(0, tk.END)
        prompt = self.prompt_var.get()
        self.log_message(prompt + line)
        if self._execute is None:
            return "break"
        # NOTE: execute() runs on the tkinter main thread, so long-running user
        # code will block the UI and stall the pygame frame loop. Revisit by
        # moving execution to a worker thread with a queue back to the log.
        more = self._execute(line)
        self.prompt_var.set("... " if more else ">>> ")
        return "break"
