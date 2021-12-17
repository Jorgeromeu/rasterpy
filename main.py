import time

import numpy as np

from geometry import Vec3f, Tri3f
from image import Color, Image

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

    image = Image(1200, 1200)

    world_tris = read_obj_tris('obj/african_head.obj')
    light_pos = Vec3f(100, 100, -150)

    for i, world_tri in enumerate(world_tris):
        normal = world_tri.normal().normalized()
        light_dir = (world_tri.a - light_pos).normalized()

        intensity = float(np.dot(light_dir, normal))

        # project to screen vertices
        screen_vertices = [Vec3f((v.x + 1) * image.width / 2, (v.y + 1) * image.height / 2, v.z) for v in world_tri]
        tri_screen = Tri3f(screen_vertices[0], screen_vertices[1], screen_vertices[2])

        if intensity > 0:
            image.draw_tri(tri_screen, Color(1.0 * intensity, 0.5 * intensity, 0.5 * intensity))
        else:
            image.draw_tri(tri_screen, Color(0, 0, 0))

    image.savefig('render.png')
    image.save_zbuf('zbuff.png')

    stop = time.time()
    print('time', stop - start)
