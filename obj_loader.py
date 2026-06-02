# obj_loader.py

from math import sqrt

# ============================================
# LOAD OBJ
# ============================================

def load_obj(path):

    verts = []
    normals = []
    tris = []

    with open(path, "r") as f:

        for line in f:

            # ====================================
            # VERTEX
            # ====================================

            if line.startswith("v "):

                parts = line.split()

                x = float(parts[1])
                y = float(parts[2])
                z = float(parts[3])

                verts.append((x, y, z))

            # ====================================
            # NORMAL
            # ====================================

            elif line.startswith("vn "):

                parts = line.split()

                x = float(parts[1])
                y = float(parts[2])
                z = float(parts[3])

                length = sqrt(
                    x * x +
                    y * y +
                    z * z
                )

                if length != 0:

                    x /= length
                    y /= length
                    z /= length

                normals.append((x, y, z))

            # ====================================
            # FACE
            # ====================================

            elif line.startswith("f "):

                parts = line.split()[1:]

                indices = []

                for p in parts:

                    vals = p.split("/")

                    # vertex index

                    v_i = int(vals[0]) - 1

                    # normal index

                    if len(vals) >= 3 and vals[2] != "":

                        n_i = int(vals[2]) - 1

                    else:

                        n_i = -1

                    indices.append((v_i, n_i))

                # triangulate polygon

                for i in range(1, len(indices) - 1):

                    v1, n1 = indices[0]
                    v2, n2 = indices[i]
                    v3, n3 = indices[i + 1]

                    tris.append((
                        v1,
                        v2,
                        v3,
                        n1,
                        n2,
                        n3
                    ))

    # ============================================
    # AUTO GENERATE NORMALS
    # ============================================

    if len(normals) == 0:

        normals = [
            [0.0, 0.0, 0.0]
            for _ in verts
        ]

        new_tris = []

        for tri in tris:

            v1_i, v2_i, v3_i, _, _, _ = tri

            v1 = verts[v1_i]
            v2 = verts[v2_i]
            v3 = verts[v3_i]

            # edge 1

            ux = v2[0] - v1[0]
            uy = v2[1] - v1[1]
            uz = v2[2] - v1[2]

            # edge 2

            vx = v3[0] - v1[0]
            vy = v3[1] - v1[1]
            vz = v3[2] - v1[2]

            # cross product

            nx = (uy * vz) - (uz * vy)
            ny = (uz * vx) - (ux * vz)
            nz = (ux * vy) - (uy * vx)

            # accumulate normals

            normals[v1_i][0] += nx
            normals[v1_i][1] += ny
            normals[v1_i][2] += nz

            normals[v2_i][0] += nx
            normals[v2_i][1] += ny
            normals[v2_i][2] += nz

            normals[v3_i][0] += nx
            normals[v3_i][1] += ny
            normals[v3_i][2] += nz

            # triangle with generated normals

            new_tris.append((
                v1_i,
                v2_i,
                v3_i,
                v1_i,
                v2_i,
                v3_i
            ))

        # normalize normals

        final_normals = []

        for nx, ny, nz in normals:

            length = sqrt(
                nx * nx +
                ny * ny +
                nz * nz
            )

            if length == 0:

                final_normals.append((0, 1, 0))

                continue

            final_normals.append((
                nx / length,
                ny / length,
                nz / length
            ))

        normals = final_normals
        tris = new_tris

    # ============================================
    # FIX MISSING NORMAL INDICES
    # ============================================

    else:

        fixed_tris = []

        for tri in tris:

            v1, v2, v3, n1, n2, n3 = tri

            if n1 == -1:
                n1 = 0

            if n2 == -1:
                n2 = 0

            if n3 == -1:
                n3 = 0

            fixed_tris.append((
                v1,
                v2,
                v3,
                n1,
                n2,
                n3
            ))

        tris = fixed_tris

    # ============================================
    # RETURN
    # ============================================

    return verts, normals, tris