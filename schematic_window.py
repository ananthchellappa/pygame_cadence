import pygame

from document import Document

DEFAULT_BACKGROUND = (0, 0, 0)


class SchematicWindow:
    SIZE = (1000, 700)

    def __init__(self, document: Document, on_close, background=DEFAULT_BACKGROUND):
        self._document = document
        self._on_close = on_close
        self.background = background
        pygame.init()
        self.screen = pygame.display.set_mode(self.SIZE)
        pygame.display.set_caption("Schematic")

    def tick(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._on_close()
                return

        self.screen.fill(self.background)
        pygame.display.flip()
