import tkinter as tk

import pygame

from command_context import CommandContext, FontTarget
from command_window import CommandWindow
from document import Document
from graphics_api import build_namespace
from interpreter import CommandInterpreter
from schematic_window import SchematicWindow

FRAME_MS = 16


def main() -> None:
    root = tk.Tk()
    shutting_down = {"flag": False}
    state = {"schematic": None}

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
                root.destroy()
            except tk.TclError:
                pass

    document = Document()

    def on_load_file(path: str) -> None:
        call = f"load({path!r})"
        window.log_message(">>> " + call)
        interpreter.execute(call)

    window = CommandWindow(
        root,
        on_new_schematic=open_schematic,
        on_load_file=on_load_file,
        on_exit=shutdown,
    )

    context = CommandContext(document=document)
    context.font_targets["Command"] = FontTarget(window.get_font_size, window.set_font_size)

    interpreter = CommandInterpreter(build_namespace(context), window.log_message)
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
