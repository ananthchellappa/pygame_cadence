import pygame


class CanvasWindow:
    SIZE = (1000, 700)
    BACKGROUND = (255, 255, 255)

    def __init__(self, on_quit):
        self._on_quit = on_quit
        self.cursor = (0, 0)
        pygame.init()
        self.screen = pygame.display.set_mode(self.SIZE)
        pygame.display.set_caption("Schematic Canvas")

    def move_to(self, x, y) -> None:
        self.cursor = (x, y)
        print(f"move_to({x}, {y})")

    def tick(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._on_quit()
                return

        self.screen.fill(self.BACKGROUND)
        pygame.display.flip()
