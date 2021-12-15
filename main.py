import numpy as np

import image as img
from geometry import Vec3f, Vec2i, Triangle

def line(x0, y0, x1, y1, image, color, precision=500):
    for t in np.linspace(0, 1, precision):
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t
        image.set_pixel(int(x), int(y), color)

def read_obj(filename: str):
    vertices = [None]
    faces = []

    lines = open(filename).readlines()

    for line in lines:

        fields = line.split(' ')

        if fields[0] == 'v':
            vertices.append(Vec3f(float(fields[1]), float(fields[2]), float(fields[3])))
        elif fields[0] == 'f':
            vertex_indices = map(lambda field: int(field.split('/')[0]), fields[1:])
            faces.append(tuple(vertex_indices))

    return vertices, faces

if __name__ == "__main__":

    image = img.Image(1000, 1000)

    # vertices, faces = read_obj('obj/african_head.obj')
    #
    # for face in faces:
    #
    #     # for each edge in the face
    #     for i in range(3):
    #         v0 = vertices[face[i]]
    #         v1 = vertices[face[(i + 1) % 3]]
    #
    #         x0 = int((v0.x + 1) * image.width / 2)
    #         y0 = int((v0.y + 1) * image.height / 2)
    #         x1 = int((v1.x + 1) * image.width / 2)
    #         y1 = int((v1.y + 1) * image.height / 2)
    #
    #         image.draw_line(Vec2i(x0, y0), Vec2i(x1, y1), 1)

    a = Vec2i(100, 100)
    b = Vec2i(400, 100)
    c = Vec2i(100, 1000)
    image.draw_tri(Triangle(a, b, c), 1)

    image.savefig('render.png')
