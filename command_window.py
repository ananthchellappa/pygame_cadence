import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk
from typing import Callable, Optional

DEFAULT_FONT_SIZE = 10
ENTRY_STYLE = "Command.TEntry"


class CommandWindow:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Commands")
        root.geometry("600x400")

        # One named monospace font, shared by every text-bearing widget in this
        # window. Live resize is a single self._font.configure(size=N) — Tk's
        # named-font system propagates to widgets (including the ttk.Entry,
        # which references it through the Command.TEntry style).
        fixed = tkfont.nametofont("TkFixedFont")
        self._font = tkfont.Font(family=fixed.actual("family"), size=DEFAULT_FONT_SIZE)

        style = ttk.Style()
        style.configure(ENTRY_STYLE, font=self._font)

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
            font=self._font,
        )
        log_scroll = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log.yview)
        self.log.configure(yscrollcommand=log_scroll.set)
        self.log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        entry_frame = ttk.Frame(paned)
        paned.add(entry_frame, weight=0)

        self.prompt_var = tk.StringVar(value=">>> ")
        prompt_label = ttk.Label(
            entry_frame, textvariable=self.prompt_var, font=self._font
        )
        prompt_label.pack(side=tk.LEFT, padx=(4, 0), pady=4)

        self.entry = ttk.Entry(entry_frame, style=ENTRY_STYLE)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4, pady=4)
        self.entry.bind("<Return>", self._on_return)
        self.entry.focus_set()

        self._execute: Optional[Callable[[str], bool]] = None

    def set_executor(self, execute_fn: Callable[[str], bool]) -> None:
        self._execute = execute_fn

    def get_font_size(self) -> int:
        return int(self._font.cget("size"))

    def set_font_size(self, size: int) -> None:
        self._font.configure(size=size)

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
