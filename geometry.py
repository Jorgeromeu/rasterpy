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

    def __sub__(self, other):
        return Vec3f(self.x - other.x, self.y - other.y, self.z - other.z)

    def __add_(self, other):
        return Vec3f(self.x + other.x, self.y + other.y, self.z + other.z)

    def __div__(self, other):
        return Vec3f(self.x / other, self.y / other, self.z / other)

    def __iter__(self):
        for pt in [self.x, self.y, self.z]:
            yield pt

    def __array__(self, dtype=None):
        return np.array([self.x, self.y, self.z], dtype=dtype)

    def cross(self, other):
        x, y, z = np.cross(self, other)
        return Vec3f(x, y, z)

    def norm(self):
        return np.linalg.norm(self)

    def normalized(self):
        length = self.norm()
        return Vec3f(self.x / length, self.y / length, self.z / length)

@dataclass
class Tri3f:
    a: Vec3f
    b: Vec3f
    c: Vec3f

    def __iter__(self):
        for pt in [self.a, self.b, self.c]:
            yield pt

    def normal(self):
        e1 = self.b - self.a
        e2 = self.c - self.a
        return e1.cross(e2)

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

        return int(min_x), int(min_y), int(max_x), int(max_y)

    def contains_point(self, point: Vec2i) -> bool:
        """
        Returns true if the point is inside the tri
        """
        wa, wb, wc = self.barycentric(point)
        return wa >= 0 and wb >= 0 and wc >= 0
