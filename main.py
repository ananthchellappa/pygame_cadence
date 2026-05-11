import tkinter as tk
from pathlib import Path

import pygame

from command_context import CommandContext, FontTarget
from command_window import CommandWindow
from document import Document
from graphics_api import build_namespace
from interpreter import CommandInterpreter
from schematic_window import SchematicWindow
from transcript import TranscriptLogger, next_free_path

FRAME_MS = 16


def main() -> None:
    root = tk.Tk()
    shutting_down = {"flag": False}
    state = {"schematic": None}

    transcript = TranscriptLogger(next_free_path(Path.cwd() / "CDS.log"))

    def close_schematic():
        if state["schematic"] is None:
            return
        state["schematic"] = None
        pygame.display.quit()

    def open_schematic():
        if state["schematic"] is not None:
            return
        state["schematic"] = SchematicWindow(document, on_close=close_schematic)

    def shutdown():
        if shutting_down["flag"]:
            return
        shutting_down["flag"] = True
        if state["schematic"] is not None:
            close_schematic()
        try:
            pygame.quit()
        finally:
            try:
                window.transcript.close()
            except Exception:
                pass
            try:
                root.destroy()
            except tk.TclError:
                pass

    document = Document()

    def on_load_file(path: str) -> None:
        call = f"load({path!r})"
        window.transcript.record("INPUT", call)
        window.log_message(">>> " + call)
        interpreter.execute(call)

    window = CommandWindow(
        root,
        transcript=transcript,
        on_new_schematic=open_schematic,
        on_load_file=on_load_file,
        on_exit=shutdown,
    )

    context = CommandContext(document=document)
    context.font_targets["Command"] = FontTarget(window.get_font_size, window.set_font_size)

    def log_and_record(text: str) -> None:
        window.log_message(text)
        window.transcript.record("OUTPUT", text)

    interpreter = CommandInterpreter(build_namespace(context), log_and_record)
    window.set_executor(interpreter.execute)

    root.protocol("WM_DELETE_WINDOW", shutdown)

    def pump():
        if shutting_down["flag"]:
            return
        schematic = state["schematic"]
        if schematic is not None:
            schematic.tick()
        if shutting_down["flag"]:
            return
        root.after(FRAME_MS, pump)

    root.after(FRAME_MS, pump)
    root.mainloop()


if __name__ == "__main__":
    main()
