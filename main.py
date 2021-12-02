import numpy as np
import matplotlib.pyplot as plt

def line(x0, y0, x1, y1, img, colo, precision=500):
    for t in np.linspace(0, 1, precision):
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t

        x = int(x)
        y = int(y)

        img[x, y] = colo

def read_obj(filename: str):
    vertices = []
    faces = []

    lines = open(filename).readlines()

    for line in lines:

        fields = line.split(' ')

        if fields[0] == 'v':
            vertices.append((float(fields[1]), float(fields[2]), float(fields[3])))
        elif fields[0] == 'f':
            vertex_indices = map(lambda field: int(field.split('/')[0]), fields[1:])
            faces.append(tuple(vertex_indices))

    return vertices, faces

if __name__ == "__main__":
    width = 1000
    height = 1500
    image = np.empty(shape=(height + 1, width + 1))

    vertices, faces = read_obj('obj/african_head.obj')

    for face in faces:

        # for each vertex in the face get its next one
        for i in range(3):
            v0_idx = face[i]
            v1_idx = face[(i + 1) % 3]

            if v0_idx >= len(vertices) or v1_idx >= len(vertices):
                continue

            v0 = vertices[v0_idx]
            v1 = vertices[v1_idx]

            x0 = (v0[0] + 1) * width / 2
            y0 = (v0[1] + 1) * width / 2
            x1 = (v1[0] + 1) * width / 2
            y1 = (v1[1] + 1) * width / 2
            line(x0, y0, x1, y1, image, 1)

    plt.imshow(image, cmap='gray', origin='lower')
    plt.savefig('render.png', bbox_inches='tight')
