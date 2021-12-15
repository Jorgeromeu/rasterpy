import math
from dataclasses import dataclass

import numpy as np

@dataclass
class Vec2i:
    x: int
    y: int

    def __iter__(self):
        for pt in [self.x, self.y]:
            yield pt

    def __array__(self, dtype=None):
        return np.array([self.x, self.y], dtype=dtype)

@dataclass
class Vec3f:
    x: float
    y: float
    z: float

    def __iter__(self):
        for pt in [self.x, self.y, self.z]:
            yield pt

    def __array__(self, dtype=None):
        return np.array([self.x, self.y, self.z], dtype=dtype)

@dataclass
class Triangle:
    a: Vec2i
    b: Vec2i
    c: Vec2i

    def __iter__(self):
        for pt in [self.a, self.b, self.c]:
            yield pt

    def barycentric(self, point: Vec2i) -> (float, float, float):
        """
        Returns the barycentric coordinates of the points with respect to the triangle
        """

        u = np.cross([self.c.x - self.a.x, self.b.x - self.a.x, self.a.x - point.x],
                     [self.c.y - self.a.y, self.b.y - self.a.y, self.a.y - point.y])
        u = Vec3f(u[0], u[1], u[2])

        if np.abs(u.z) < 1:
            return Vec3f(-1, 1, 1)

        return 1.0 - (u.x + u.y) / u.z, u.y / u.z, u.x / u.z

    def bbox(self) -> (int, int, int, int):
        """
        :return: min_x, min_y, max_x, max_y coordinates of triangle bounding box
        """
        min_x = self.a.x
        min_y = self.a.y
        max_x = self.a.x
        max_y = self.a.y
        for v in [self.b, self.c]:
            min_x = min(min_x, v.x)
            min_y = min(min_y, v.y)
            max_x = max(max_x, v.x)
            max_y = max(max_y, v.y)

        return min_x, min_y, max_x, max_y

    def contains_point(self, point: Vec2i) -> bool:
        """
        Returns true if the point is inside the tri
        """
        wa, wb, wc = self.barycentric(point)
        return wa >= 0 and wb >= 0 and wc >= 0
