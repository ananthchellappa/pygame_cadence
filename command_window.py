import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk
from typing import Callable, Optional

from command_history import CommandHistory

DEFAULT_FONT_SIZE = 14


class CommandWindow:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Commands")
        root.geometry("600x400")

        # Track family + size ourselves and re-apply a fresh font spec to each
        # widget on resize.
        #
        # On X11/WSLg, TkFixedFont resolves to the legacy 'fixed' bitmap font,
        # which can't be scaled — requesting size 20 silently renders at the
        # nearest available bitmap size (often still 10). Substitute a generic
        # scalable family in that case so size changes are actually visible.
        family = tkfont.nametofont("TkFixedFont").actual("family")
        if family.lower() == "fixed":
            family = "monospace"
        self._font_family = family
        self._font_size = DEFAULT_FONT_SIZE

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
            font=self._font_spec(),
        )
        log_scroll = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log.yview)
        self.log.configure(yscrollcommand=log_scroll.set)
        self.log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        entry_frame = ttk.Frame(paned)
        paned.add(entry_frame, weight=0)

        self.prompt_var = tk.StringVar(value=">>> ")
        self._prompt_label = ttk.Label(
            entry_frame, textvariable=self.prompt_var, font=self._font_spec()
        )
        self._prompt_label.pack(side=tk.LEFT, padx=(4, 0), pady=4)

        self.entry = ttk.Entry(entry_frame, font=self._font_spec())
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4, pady=4)
        self.entry.bind("<Return>", self._on_return)
        self.entry.bind("<Up>", self._on_up)
        self.entry.bind("<Down>", self._on_down)
        self.entry.focus_set()

        self._execute: Optional[Callable[[str], bool]] = None
        self._history = CommandHistory()

    def _font_spec(self) -> tuple:
        return (self._font_family, self._font_size)

    def set_executor(self, execute_fn: Callable[[str], bool]) -> None:
        self._execute = execute_fn

    def get_font_size(self) -> int:
        return self._font_size

    def set_font_size(self, size: int) -> None:
        self._font_size = size
        spec = self._font_spec()
        self.log.configure(font=spec)
        self._prompt_label.configure(font=spec)
        self.entry.configure(font=spec)

    def log_message(self, text: str) -> None:
        self.log.configure(state=tk.NORMAL)
        self.log.insert(tk.END, text + "\n")
        self.log.see(tk.END)
        self.log.configure(state=tk.DISABLED)

    def _on_return(self, _event):
        line = self.entry.get()
        self._history.add(line)
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

    def _on_up(self, _event):
        recalled = self._history.prev(self.entry.get())
        if recalled is not None:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, recalled)
            self.entry.icursor(tk.END)
        return "break"

    def _on_down(self, _event):
        recalled = self._history.next(self.entry.get())
        if recalled is not None:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, recalled)
            self.entry.icursor(tk.END)
        return "break"
