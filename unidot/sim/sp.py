"""
unidot.sim.sp is a module within unidot.sim that contains Spatial Partitioning classes for performance in physics simulations.
"""

import pygame

class Quadtree:
    def __init__(self, boundary, capacity=4, level=0, max_level=5):
        self.boundary = boundary  # pygame.Rect
        self.capacity = capacity
        self.level = level
        self.max_level = max_level
        self.objects = []
        self.divided = False
        self.children = []

    def insert(self, obj):
        if not self.boundary.colliderect(obj.rect):
            return False
        if len(self.objects) < self.capacity or self.level == self.max_level:
            self.objects.append(obj)
            return True
        if not self.divided:
            self.subdivide()
        for child in self.children:
            if child.insert(obj):
                return True
        return False

    def subdivide(self):
        x, y, w, h = self.boundary
        hw, hh = w // 2, h // 2
        self.children = [
            Quadtree(pygame.Rect(x, y, hw, hh), self.capacity, self.level+1, self.max_level),
            Quadtree(pygame.Rect(x+hw, y, hw, hh), self.capacity, self.level+1, self.max_level),
            Quadtree(pygame.Rect(x, y+hh, hw, hh), self.capacity, self.level+1, self.max_level),
            Quadtree(pygame.Rect(x+hw, y+hh, hw, hh), self.capacity, self.level+1, self.max_level)
        ]
        for obj in self.objects:
            for child in self.children:
                if child.insert(obj):
                    break
        self.objects = []
        self.divided = True

    def query(self, range_rect, found=None):
        if found is None:
            found = []
        if not self.boundary.colliderect(range_rect):
            return found
        for obj in self.objects:
            if range_rect.colliderect(obj.rect):
                found.append(obj)
        if self.divided:
            for child in self.children:
                child.query(range_rect, found)
        return found

class Grid:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.cols = width // cell_size
        self.rows = height // cell_size
        self.cells = {}
    
    def _cell_coords(self, rect):
        x1 = rect.left // self.cell_size
        y1 = rect.top // self.cell_size
        x2 = rect.right // self.cell_size
        y2 = rect.bottom // self.cell_size
        return [(x, y) for x in range(x1, x2+1) for y in range(y1, y2+1)]
    
    def insert(self, obj):
        for coord in self._cell_coords(obj.rect):
            if coord not in self.cells:
                self.cells[coord] = []
            self.cells[coord].append(obj)
    
    def query(self, rect):
        found = set()
        for coord in self._cell_coords(rect):
            for obj in self.cells.get(coord, []):
                if rect.colliderect(obj.rect):
                    found.add(obj)
        return list(found)

class Octtree:
    pass

class ObjectManager:
    def __init__(self, screensize, mode="quadtree"):
        sp = None
        if mode.lower() in ["quadtree", "qt", "qdt", "qdtree", "quad"]:
            sp = Quadtree(pygame.rect(0, 0, screensize), 8)