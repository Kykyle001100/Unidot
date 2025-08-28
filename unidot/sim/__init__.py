"""
unidot.sim.* has modules useful for simulators that have physics and more.
"""

import pygame

class Entity:
    def __init__(self, pos):
        self.x, self.y = pos

    def update(self):
        pass

    def draw(self, surface):
        pass

    def _draw(self, pos, surface):
        pass

    def __getattribute__(self, name):
        if name in "hw":
            return 0

class StaticObject(Entity):
    def __init__(self, pos, size, color=(255, 0, 0)):
        super().__init__(pos)
        self.width, self.height = size
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def _draw(self, pos, surface):
        rect = pygame.Rect(pos[0], pos[1], self.width, self.height)
        pygame.draw.rect(surface, self.color, rect)

    def __getattribute__(self, name):
        if name in ["vx", "vy"]:
            return 0
        if name == "w":
            return self.width
        if name == "h":
            return self.height

class KinematicObject(Entity):
    def __init__(self, pos, size, color=(0, 255, 0)):
        super().__init__(pos)
        self.width, self.height = size
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = color
        self.vx, self.vy = 0, 0

    def set_velocity(self, vx, vy):
        self.vx, self.vy = vx, vy

    def update(self, dt, friction=0.98):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.rect.topleft = (self.x, self.y)
        self.vx *= friction
        self.vy *= friction

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def _draw(self, pos, surface):
        rect = pygame.Rect(pos[0], pos[1], self.width, self.height)
        pygame.draw.rect(surface, self.color, rect)

    def move_slide(self, neighbors, bounce=False):
        for neighbor in neighbors:
            if self.rect.colliderect(neighbor.rect):
                if self.rect.right > neighbor.rect.left and self.vx > 0:
                    self.x = neighbor.rect.left - self.width
                    self.vx = -self.vx if bounce else 0
                if self.rect.left < neighbor.rect.right and self.vx < 0:
                    self.x = neighbor.rect.right
                    self.vx = -self.vx if bounce else 0
                if self.rect.bottom > neighbor.rect.top and self.vy > 0:
                    self.y = neighbor.rect.top - self.height
                    self.vy = -self.vy if bounce else 0
                if self.rect.top < neighbor.rect.bottom and self.vy < 0:
                    self.y = neighbor.rect.bottom
                    self.vy = -self.vy if bounce else 0
                self.rect.topleft = (self.x, self.y)

    def __getattribute__(self, name):
        if name == "vx":
            return self.vx
        if name == "vy":
            return self.vy
        if name == "w":
            return self.width
        if name == "h":
            return self.height

class TextureObject(pygame.sprite.Sprite):
    def __init__(self, pos, image_data):
        super().__init__()
        self.image = pygame.image.load(image_data).convert_alpha()
        self.x, self.y = pos
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def _draw(self, pos, surface):
        surface.blit(self.image, pos)

    def __getattribute__(self, name):
        if name in ["vx", "vy"]:
            return 0
        if name == "w":
            return self.rect.width
        if name == "h":
            return self.rect.height

class KinTextureObject(TextureObject):
    def __init__(self, pos, image_data):
        super().__init__(pos, image_data)
        self.vx, self.vy = 0, 0

    def set_velocity(self, vx, vy):
        self.vx, self.vy = vx, vy

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.topleft = (self.x, self.y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def _draw(self, pos, surface):
        surface.blit(self.image, pos)

    def move_slide(self, neighbors, bounce=False):
        for neighbor in neighbors:
            if self.rect.colliderect(neighbor.rect):
                if self.rect.right > neighbor.rect.left and self.vx > 0:
                    self.x = neighbor.rect.left - self.rect.width
                    self.vx = -self.vx if bounce else 0
                if self.rect.left < neighbor.rect.right and self.vx < 0:
                    self.x = neighbor.rect.right
                    self.vx = -self.vx if bounce else 0
                if self.rect.bottom > neighbor.rect.top and self.vy > 0:
                    self.y = neighbor.rect.top - self.rect.height
                    self.vy = -self.vy if bounce else 0
                if self.rect.top < neighbor.rect.bottom and self.vy < 0:
                    self.y = neighbor.rect.bottom
                    self.vy = -self.vy if bounce else 0
                self.rect.topleft = (self.x, self.y)

    def __getattribute__(self, name):
        if name == "vx":
            return self.vx
        if name == "vy":
            return self.vy
        if name == "w":
            return self.rect.width
        if name == "h":
            return self.rect.height

class StaticTextureObj(TextureObject):
    def __init__(self, pos, image_data):
        super().__init__(pos, image_data)
