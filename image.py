import math
from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np

from geometry import Vec2i, Tri3f

@dataclass
class Color:
    r: float
    g: float
    b: float

    def to_int(self):
        r_int = int(self.r * 255)
        g_int = int(self.g * 255)
        b_int = int(self.b * 255)
        return r_int, g_int, b_int

@dataclass
class Image:
    width: int
    height: int
    arr: np.ndarray
    zbuff: np.ndarray

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.arr = np.empty(shape=(height + 1, width + 1, 3))
        self.zbuff = np.full((height+1, width+1), -math.inf)

    def savefig(self, filename):
        plt.imshow(self.arr, origin='lower')
        plt.savefig(filename, bbox_inches='tight')
        plt.cla()

    def save_zbuf(self, filename):
        plt.imshow(self.zbuff, origin='lower')
        plt.savefig(filename, bbox_inches='tight')
        plt.cla()

    def set_pixel(self, x, y, color: Color):
        if x < len(self.arr) and y < len(self.arr[0]):
            self.arr[y, x, 0] = color.r
            self.arr[y, x, 1] = color.g
            self.arr[y, x, 2] = color.b

    def draw_line(self, v0: Vec2i, v1: Vec2i, color: Color, precision=500):
        for t in np.linspace(0, 1, precision):
            x = v0.x + (v1.x - v0.x) * t
            y = v0.y + (v1.y - v0.y) * t
            self.set_pixel(int(x), int(y), color)

    def draw_tri(self, tri: Tri3f, color: Color):

        # compute bounding box
        bbox_min_x, bbox_min_y, bbox_max_x, bbox_max_y = tri.bbox()

        # clamp bbox to image
        bbox_min_x = max(bbox_min_x, 0)
        bbox_max_x = min(bbox_max_x, self.width)
        bbox_min_y = max(bbox_min_y, 0)
        bbox_max_y = min(bbox_max_y, self.height)

        # for each pixel in bounding box, if inside triangle color it
        for pix_x in range(bbox_min_x, bbox_max_x + 1):
            for pix_y in range(bbox_min_y, bbox_max_y + 1):

                wa, wb, wc = tri.barycentric(Vec2i(pix_x, pix_y))

                z = sum(v.z*bcoord for v, bcoord in zip(tri, [wa, wb, wc]))

                if wa >= 0 and wb >= 0 and wc >= 0:
                    if self.zbuff[pix_y, pix_x] <= z:
                        self.zbuff[pix_y, pix_x] = z
                        self.set_pixel(pix_x, pix_y, color)
