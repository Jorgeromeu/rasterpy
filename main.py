import random
import time

import numpy as np

import image as img
from geometry import Vec3f, Vec2i, Tri2i, Tri3f

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

def read_obj_tris(filename: str):
    vertices, faces = read_obj(filename)
    return [Tri3f(vertices[f[0]], vertices[f[1]], vertices[f[2]]) for f in faces]

if __name__ == "__main__":

    start = time.time()

    image = img.Image(200, 200)

    world_tris = read_obj_tris('obj/monke_noback.obj')
    light_pos = Vec3f(100, 100, -100)

    print('tris:', len(world_tris))

    for i, world_tri in enumerate(world_tris):

        normal = world_tri.normal().normalized()
        light_dir = (world_tri.a - light_pos).normalized()

        color = np.dot(light_dir, normal)

        screen_vertices = [Vec2i(int((v.x + 1) * image.width / 2), int((v.y + 1) * image.height / 2)) for v in
                           world_tri]

        tri_screen = Tri2i(screen_vertices[0], screen_vertices[1], screen_vertices[2])
        image.draw_tri(tri_screen, color)
        print(i)

    image.savefig('render.png')

    stop = time.time()
    print('time', stop - start)
