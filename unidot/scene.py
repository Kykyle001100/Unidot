class Scene:
    def __init__(self):
        self.manager = None  # Set when attached to SceneManager

    def init(self):
        """Called when the scene is first created/entered."""
        pass

    def play(self, draw, update, events):
        """Main loop: handle events, logic, drawing."""
        pass

    def on_enter(self):
        """Optional: called when scene becomes active."""
        pass

    def on_exit(self):
        """Optional: called when scene is left."""
        pass


class SceneManager:
    def __init__(self):
        self.scenes = []

    def push(self, scene: Scene):
        if self.scenes:
            self.scenes[-1].on_exit()
        scene.manager = self
        self.scenes.append(scene)
        scene.init()
        scene.on_enter()

    def pop(self):
        if self.scenes:
            scene = self.scenes.pop()
            scene.on_exit()
        if self.scenes:
            self.scenes[-1].on_enter()

    def switch(self, scene: Scene):
        """Replace current scene with a new one."""
        self.pop()
        self.push(scene)

    def current(self):
        if self.scenes:
            return self.scenes[-1]
        return None
