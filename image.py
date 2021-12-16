from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np

from geometry import Vec2i, Tri2i

@dataclass
class Image:
    width: int
    height: int
    arr: np.ndarray

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.arr = np.empty(shape=(height + 1, width + 1))

    def savefig(self, filename):
        plt.imshow(self.arr, cmap='gray', origin='lower')
        plt.savefig(filename, bbox_inches='tight')

    def set_pixel(self, x, y, color):
        if x < len(self.arr) and y < len(self.arr[0]):
            self.arr[y, x] = color

    def draw_line(self, v0: Vec2i, v1: Vec2i, color, precision=500):
        for t in np.linspace(0, 1, precision):
            x = v0.x + (v1.x - v0.x) * t
            y = v0.y + (v1.y - v0.y) * t
            self.set_pixel(int(x), int(y), color)

    def draw_tri(self, tri: Tri2i, color):

        # compute bounding box
        bbox_min_x, bbox_min_y, bbox_max_x, bbox_max_y = tri.bbox()

        # for each pixel in bounding box, if inside triangle color it
        for pix_x in range(bbox_min_x, bbox_max_x+1):
            for pix_y in range(bbox_min_y, bbox_max_y + 1):
                if tri.contains_point(Vec2i(pix_x, pix_y)):
                    self.set_pixel(pix_x, pix_y, color)
