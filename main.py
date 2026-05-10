import tkinter as tk

import pygame

from canvas_window import CanvasWindow
from command_context import CommandContext, FontTarget
from command_window import CommandWindow
from document import Document
from graphics_api import build_namespace
from interpreter import CommandInterpreter

FRAME_MS = 16


def main() -> None:
    root = tk.Tk()
    shutting_down = {"flag": False}

    def shutdown():
        if shutting_down["flag"]:
            return
        shutting_down["flag"] = True
        try:
            pygame.quit()
        finally:
            try:
                root.destroy()
            except tk.TclError:
                pass

    document = Document()
    canvas = CanvasWindow(document, on_quit=shutdown)
    window = CommandWindow(root)

    context = CommandContext(document=document)
    context.font_targets["Command"] = FontTarget(window.get_font_size, window.set_font_size)

    interpreter = CommandInterpreter(build_namespace(context), window.log_message)
    window.set_executor(interpreter.execute)

    root.protocol("WM_DELETE_WINDOW", shutdown)

    def pump():
        if shutting_down["flag"]:
            return
        canvas.tick()
        if shutting_down["flag"]:
            return
        root.after(FRAME_MS, pump)

    root.after(FRAME_MS, pump)
    root.mainloop()


if __name__ == "__main__":
    main()
