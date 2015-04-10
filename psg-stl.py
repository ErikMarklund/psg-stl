import argparse, textwrap, math

PHI_GOLDEN = (1.0 + math.sqrt(5.0)) / 2.0

def Vector(x, y, z):
    return {
        "x": x,
        "y": y,
        "z": z
    }

def MatrixMultiply(vector, matrix):
    v = Vector(0,0,0)

    v["x"] = matrix[0] * vector["x"] + matrix[3] * vector["y"] + matrix[6] * vector["z"]
    v["y"] = matrix[1] * vector["x"] + matrix[4] * vector["y"] + matrix[7] * vector["z"]
    v["z"] = matrix[2] * vector["x"] + matrix[5] * vector["y"] + matrix[8] * vector["z"]

    return v

def RotationMatrixXAxis(angle):
    rot_matrix = [ 1, 0, 0,
                   0, math.cos(angle),  -math.sin(angle),
                   0, math.sin(angle),   math.cos(angle) ]
    return rot_matrix

def RotationMatrixYAxis(angle):
    rot_matrix = [ math.cos(angle),  0, math.sin(angle),
                   0,                1,               0,
                  -math.sin(angle),  0, math.cos(angle) ]
    return rot_matrix


class PlatonicSolid(object):
    verts = []
    indices = []

    def __init__(self, name, verts):
        self.name = name
        for idx in range(0, verts-1):
            self.verts.append(Vector(0,0,0))

    def generate(self):
        raise Exception("Unimplemented method!")

class Tetrahedron(PlatonicSolid):
    def __init__(self):
        super(Tetrahedron, self).__init__("Tetrahedron", 4)

    def generate(self):
        self.verts[0] = Vector( 1,  1,  1)
        self.verts[1] = Vector( 1, -1, -1)
        self.verts[2] = Vector(-1,  1, -1)
        self.verts[3] = Vector(-1, -1,  1)
        self.indices = [
            [ 0, 1, 2],
            [ 0, 1, 3],
            [ 0, 2, 3],
            [ 2, 1, 3]
        ]

class Cube(PlatonicSolid):
    def __init__(self):
        super(Cube, self).__init__("Cube", 8)

class Dodecahedron(PlatonicSolid):
    def __init__(self):
        super(Dodecahedron, self).__init__("Dodecahedron", 20)

    def add_face(self, indices):
        self.indices.append(
            [ indices[0], indices[1], indices[2] ])
        self.indices.append(
            [ indices[2], indices[3], indices[0] ])
        self.indices.append(
            [ indices[3], indices[4], indices[0] ])

    def orientate_to_base(self):
        # Assume a Z-up coordinate system (urgh)
        angle = (2.0 * math.atan(PHI_GOLDEN)) * 0.5
        rot_matrix = RotationMatrixXAxis(angle)

        for vertexIdx in range(0, len(self.verts)):
            self.verts[vertexIdx] = MatrixMultiply(self.verts[vertexIdx], rot_matrix)

    def generate(self):
        phi = PHI_GOLDEN
        one_over_phi = 1.0 / phi

        verts = []
        for ix in range(-1, 2, 2):
            for iy in range(-1, 2, 2):
                for iz in range(-1, 2, 2):
                    verts.append(Vector(ix * 1, iy * 1, iz * 1))

                verts.append(Vector(0,                 ix * one_over_phi, iy * phi         ))
                verts.append(Vector(ix * one_over_phi, iy * phi,          0                ))
                verts.append(Vector(ix * phi,          0,                 iy * one_over_phi))

        self.verts = verts

        # Refer to diagram in docs to see how these indices are formed
        self.add_face([15, 12, 2, 10, 14])
        self.add_face([8, 5, 12, 15, 18])
        self.add_face([8, 6, 9, 4, 5])
        self.add_face([9, 4, 0, 3, 1])
        self.add_face([6, 17, 7, 1, 9])
        self.add_face([0, 3, 13, 10, 2])
        self.add_face([13, 11, 7, 1, 3])
        self.add_face([13, 11, 19, 14, 10])
        self.add_face([14, 19, 16, 18, 15])
        self.add_face([17, 6, 8, 18, 16])
        self.add_face([11, 7, 17, 16, 19])
        self.add_face([0, 2, 12, 5, 4])

class STLWriter:
    def calculate_normal(self, a, b):
        # Cross product a x b, then normalise
        x = a["y"] * b["z"] - a["z"] * b["y"]
        y = a["z"] * b["x"] - a["x"] * b["z"]
        z = a["x"] * b["y"] - a["y"] * b["x"]
        l = math.sqrt(x*x + y*y + z*z)
        return Vector(x/l,y/l,z/l)

    def stringify_vector_with_spaces(self, vector):
        s = ""
        s += "%.6f" % vector["x"] + " "
        s += "%.6f" % vector["y"] + " "
        s += "%.6f" % vector["z"]
        return s

    def write(self, solid):
        file_name = solid.name + ".stl"
        f = open(file_name, "w")
        f.write("solid " + solid.name + "\n")

        for triangle in solid.indices:
            vertex_a = solid.verts[triangle[0]]
            vertex_b = solid.verts[triangle[1]]
            vertex_c = solid.verts[triangle[2]]
            normal   = self.calculate_normal(vertex_a, vertex_b)

            f.write("facet normal ")
            f.write(self.stringify_vector_with_spaces(normal) + "\n")
            f.write("\touter loop\n")

            # Vertex A
            f.write("\t\tvertex ")
            f.write(self.stringify_vector_with_spaces(vertex_a) + "\n")
            # Vertex B
            f.write("\t\tvertex ")
            f.write(self.stringify_vector_with_spaces(vertex_b) + "\n")
            # Vertex C
            f.write("\t\tvertex ")
            f.write(self.stringify_vector_with_spaces(vertex_c) + "\n")

            f.write("\tendloop\n")
            f.write("endfacet\n\n")

        f.write("endsolid " + solid.name + "\n")

if __name__ == '__main__':
    SOLIDS = {
        1: Tetrahedron(),
        2: Cube(),
        4: Dodecahedron()
    }

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            Platonic Solid Generator: STL Exporter
            --------------------------------
                Generates platonic solids of a given type in STL format.
                The following options denote the type:
                1. Tetrahedron
                2. Cube
                3. Octahedron
                4. Dodecahedron
                5. Icosahedron
            '''))
    parser.add_argument('--type', required=True, help='type of solid to generate.')
    args = parser.parse_args()

    solid_type = int(args.type)
    if not solid_type in SOLIDS:
        print "Invalid type. Run with --help to list type names."
    else:
        solid = SOLIDS[solid_type]
        print "Generating solid of type " + solid.name
        solid.generate()
        solid.orientate_to_base()

        writer = STLWriter()
        writer.write(solid)

        print "Done!"

