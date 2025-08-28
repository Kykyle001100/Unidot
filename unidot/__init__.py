"""
Unidot, a game engine-framework hybrid for Python.
It provides a set of modules to help you build games quickly and easily in a clean, structured way without getting trapped in boilerplates.
"""

from functools import wraps

def screen(func):
    """Decorator that injects screen, clock, and dt automatically."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Import inside to avoid circular issues
        from .game import Game, QuickGame
        # figure out which class is active
        screen = Game.screen or QuickGame.screen
        clock = Game.clock or QuickGame.clock
        dt = (clock.get_time() / 1000.0) if clock else 0
        return func(*args, screen=screen, clock=clock, dt=dt, **kwargs)
    return wrapper
