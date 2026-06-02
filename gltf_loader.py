from pygltflib import GLTF2
import struct

def load_gltf(filename):

    gltf = GLTF2().load(filename)

    verts = []
    tris = []

    blob = gltf.binary_blob()

    # =========================
    # POSITIONS
    # =========================

    accessor = gltf.accessors[0]
    view = gltf.bufferViews[accessor.bufferView]

    start = view.byteOffset
    length = accessor.count * 12

    data = blob[start:start+length]

    for i in range(accessor.count):

        x, y, z = struct.unpack_from(
            "<fff",
            data,
            i * 12
        )

        verts.append((x, y, z))

    # =========================
    # INDICES
    # =========================

    accessor = gltf.accessors[1]
    view = gltf.bufferViews[accessor.bufferView]

    start = view.byteOffset

    data = blob[start:]

    for i in range(0, accessor.count, 3):

        a, b, c = struct.unpack_from(
            "<HHH",
            data,
            i * 2
        )

        tris.append((a, b, c))

    return verts, tris