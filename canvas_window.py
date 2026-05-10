import pygame


class CanvasWindow:
    SIZE = (1000, 700)
    BACKGROUND = (255, 255, 255)

    def __init__(self, on_quit):
        self._on_quit = on_quit
        pygame.init()
        self.screen = pygame.display.set_mode(self.SIZE)
        pygame.display.set_caption("Schematic Canvas")

    def tick(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._on_quit()
                return

        self.screen.fill(self.BACKGROUND)
        pygame.display.flip()
