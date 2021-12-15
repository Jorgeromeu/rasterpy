from unittest import TestCase

from geometry import Triangle, Vec2i

class TestTriangle(TestCase):

    def test_barycentric(self):
        point = Vec2i(1, 1)
        a = Vec2i(0, 0)
        b = Vec2i(2, 1)
        c = Vec2i(2, 0)
        tri = Triangle(a, b, c)

        wa, wb, wc = tri.barycentric(Vec2i(1, 1))
        self.assertTrue((point == wa * a + wb * b + wc * c).all())

    def test_iterator(self):
        a = Vec2i(0, 0)
        b = Vec2i(2, 1)
        c = Vec2i(2, 0)
        tri = Triangle(a, b, c)

        pts = [pt for pt in tri]

        self.assertTrue(pts[0], a)
        self.assertTrue(pts[1], b)
        self.assertTrue(pts[2], c)

    def test_contains_point(self):
        a = Vec2i(0, 0)
        b = Vec2i(1, 2)
        c = Vec2i(2, 0)
        tri = Triangle(a, b, c)

        in_point = Vec2i(1, 1)
        out_point = Vec2i(2, 2)

        self.assertTrue(tri.contains_point(in_point))
        self.assertFalse(tri.contains_point(out_point))
