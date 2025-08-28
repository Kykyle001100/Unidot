import pygame
from .scene import SceneManager, Scene

class Game:
    """Scene-based game (has SceneManager)."""
    screen = None
    clock = None
    running = True

    def __init__(self, screensize=(800, 600), fps=60, title="Framework Game"):
        pygame.init()
        Game.screen = pygame.display.set_mode(screensize)
        pygame.display.set_caption(title)
        Game.clock = pygame.time.Clock()
        self.fps = fps
        self.scene_manager = SceneManager()

    @classmethod
    def quit(cls):
        cls.running = False

    def run(self):
        while Game.running and self.scene_manager.current():
            events = pygame.event.get()
            update, draw = [], []

            scene = self.scene_manager.current()
            scene.play(DrawQueue(draw), UpdateQueue(update), events)

            for u in update: u()
            for d in draw: d()

            pygame.display.flip()
            Game.clock.tick(self.fps)

        pygame.quit()


class QuickGame(Scene):
    """Quick single-scene game (the game is the scene)."""
    screen = None
    clock = None
    running = True

    def __init__(self, screensize=(800, 600), fps=60, title="QuickGame"):
        pygame.init()
        QuickGame.screen = pygame.display.set_mode(screensize)
        pygame.display.set_caption(title)
        QuickGame.clock = pygame.time.Clock()
        self.fps = fps

    @classmethod
    def quit(cls):
        cls.running = False

    def init(self):
        """Optional: called once before loop starts."""
        pass

    def play(self, draw, update, events):
        """Override this with logic (like Scene)."""
        pass

    def run(self):
        self.init()
        while QuickGame.running:
            events = pygame.event.get()
            update, draw = [], []

            self.play(DrawQueue(draw), UpdateQueue(update), events)

            for u in update: u()
            for d in draw: d()

            pygame.display.flip()
            QuickGame.clock.tick(self.fps)

        pygame.quit()


class DrawQueue:
    def __init__(self, queue): self.queue = queue
    def add(self, func): self.queue.append(func)


class UpdateQueue:
    def __init__(self, queue): self.queue = queue
    def add(self, func): self.queue.append(func)
