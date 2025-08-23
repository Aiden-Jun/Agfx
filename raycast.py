from Agfx import *
import math

# ----------------------
# Engine & Scene Setup
# ----------------------
eg = Engine(fps=30)
maze_scene = Scene(90, 40)
eg.register_scene("scene", maze_scene)

# ----------------------
# Maze Definition
# ----------------------
mbitmap = [
    ['#', '#', '#', '#', '#', '#', '#', '#', '#'],
    ['#', ' ', '#', '#', ' ', ' ', '#', '#', '#'],
    ['#', ' ', '#', '#', ' ', ' ', '#', '#', '#'],
    ['#', ' ', '#', '#', ' ', ' ', '#', ' ', '#'],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', '#', '#', '#', '#', '#', '#', '#', '#']
]

# ----------------------
# Maze & Player Class
# ----------------------
class RaycastMaze:
    def __init__(self):
        self.p_x = 1.5  # float x position
        self.p_y = 1.5  # float y position
        self.angle = 0.0 # float degrees, continuous rotation
        self.fov = 100  # field of view

    def move(self, forward=True):
        step = 0.15 if forward else -0.15
        rad = math.radians(self.angle)
        nx = self.p_x + math.cos(rad) * step
        ny = self.p_y + math.sin(rad) * step
        if mbitmap[int(ny)][int(nx)] != '#':
            self.p_x, self.p_y = nx, ny

    def turn_cw(self):
        self.angle += 10
        self.angle %= 360

    def turn_ccw(self):
        self.angle -= 10
        self.angle %= 360

    def raycast(self, scene):
        width = scene.fwidth
        height = scene.fheight
        half_fov = self.fov / 2
        num_rays = width
        max_depth = 10

        for col in range(num_rays):
            ray_angle = (self.angle - half_fov + (col / num_rays) * self.fov) % 360
            rad = math.radians(ray_angle)
            dx = math.cos(rad) * 0.05
            dy = math.sin(rad) * 0.05

            distance = 0
            x, y = self.p_x, self.p_y
            while distance < max_depth:
                x += dx
                y += dy
                distance += 0.05
                if mbitmap[int(y)][int(x)] == '#':
                    break

            wall_height = int(height / (distance + 0.01))
            wall_height = min(wall_height, height)
