import pygame 

class Visualizer:
    def __init__(self, size) -> None:
        # self.screen = pygame.display.set_mode((3*N*game_map.width, N*game_map.height))
        self.screen_size = (size*4, size*4)
        self.tile_width = min(self.screen_size[0] // size, self.screen_size[1] // size)
        self.WINDOW_SIZE = (self.tile_width * size, self.tile_width * size)
        self.surf = pygame.Surface(self.WINDOW_SIZE)
        self.surf.fill([239, 120, 79])
        pygame.font.init()
        self.screen = None

    def init_window(self):
        pygame.init()
        pygame.display.init()
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)


    def render(self, state):
        self.surf = pygame.surfarray.make_surface(state)
        pygame.display.update()
        resized = pygame.transform.scale(self.surf, self.screen.get_rect().size)
        self.screen.blit(resized, (0, 0))