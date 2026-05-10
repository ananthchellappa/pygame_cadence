import tkinter as tk

import pygame

from canvas_window import CanvasWindow
from command_window import CommandWindow

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

    CommandWindow(root)
    canvas = CanvasWindow(on_quit=shutdown)

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
