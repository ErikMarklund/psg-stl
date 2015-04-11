import argparse, textwrap, math

PHI_GOLDEN = (1.0 + math.sqrt(5.0)) / 2.0

def Vector(x, y, z):
    return {
        "x": x,
        "y": y,
        "z": z
    }

def Triangle(indices, normal):
    return {
        "indices": indices,
        "normal": normal
    }

def MatrixMultiply(vector, matrix):
    v = Vector(0,0,0)

    v["x"] = matrix[0] * vector["x"] + matrix[3] * vector["y"] + matrix[6] * vector["z"]
    v["y"] = matrix[1] * vector["x"] + matrix[4] * vector["y"] + matrix[7] * vector["z"]
    v["z"] = matrix[2] * vector["x"] + matrix[5] * vector["y"] + matrix[8] * vector["z"]

    return v

def Translate(source, translation):
    v = Vector(0,0,0)

    v["x"] = source["x"] + translation["x"]
    v["y"] = source["y"] + translation["y"]
    v["z"] = source["z"] + translation["z"]

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

def RotationMatrixZAxis(angle):
    rot_matrix = [ math.cos(angle), -math.sin(angle), 0,
                   math.sin(angle),  math.cos(angle), 0,
                   0,                0,               1 ]
    return rot_matrix


class PlatonicSolid(object):
    verts = []
    tris  = []

    def __init__(self, name, verts):
        self.name = name
        for idx in range(0, verts-1):
            self.verts.append(Vector(0,0,0))

    def generate(self, split):
        raise Exception("Unimplemented method!")

    def orientate_to_base(self):
        raise Exception("Unimplemented method!")

    def perform_rotation(self, rot_matrix):
        for vertexIdx in range(0, len(self.verts)):
            self.verts[vertexIdx] = MatrixMultiply(self.verts[vertexIdx], rot_matrix)

    def perform_translation(self, trans_vector):
        for vertexIdx in range(0, len(self.verts)):
            self.verts[vertexIdx] = Translate(self.verts[vertexIdx], trans_vector)

    def calculate_normal(self, a, b):
        # Cross product a x b, then normalise
        x = a["y"] * b["z"] - a["z"] * b["y"]
        y = a["z"] * b["x"] - a["x"] * b["z"]
        z = a["x"] * b["y"] - a["y"] * b["x"]
        l = math.sqrt(x*x + y*y + z*z)

        return Vector(x/l,y/l,z/l)

class Tetrahedron(PlatonicSolid):
    def __init__(self):
        super(Tetrahedron, self).__init__("Tetrahedron", 4)

    def add_face(self, indices):
        vertex_a = self.verts[indices[0]]
        vertex_b = self.verts[indices[1]]
        normal = self.calculate_normal(vertex_a, vertex_b)
        self.tris.append(Triangle(indices, normal))

    def orientate_to_base(self):
        z_trans = 1.0 / math.sqrt(2.0)
        self.perform_translation(Vector(-1, 0, z_trans))

        angleX = math.atan(math.sqrt(2.0))
        rot_matrix = RotationMatrixXAxis(angleX)
        self.perform_rotation(rot_matrix)

    def generate(self, split):
        z = 1.0 / math.sqrt(2.0)

        self.verts[0] = Vector(-1, 0, -z)
        self.verts[1] = Vector( 1, 0, -z)
        self.verts[2] = Vector( 0,-1,  z)
        self.verts[3] = Vector( 0, 1,  z)

        self.add_face([0, 2, 1])
        self.add_face([0, 3, 1])
        self.add_face([2, 1, 3])
        self.add_face([0, 2, 3])

class Cube(PlatonicSolid):
    def __init__(self):
        super(Cube, self).__init__("Cube", 8)

    def add_face(self, indices):
        vertex_a = self.verts[indices[0]]
        vertex_b = self.verts[indices[1]]
        normal = self.calculate_normal(vertex_a, vertex_b)
        self.tris.append(Triangle([ indices[0], indices[1], indices[2] ], normal))
        self.tris.append(Triangle([ indices[2], indices[3], indices[0] ], normal))

    def orientate_to_base(self):
        self.perform_translation(Vector(1, 1, 1))

    def generate(self, split):
        index = 0
        for ix in range(-1, 2, 2):
            for iy in range(-1, 2, 2):
                for iz in range(-1, 2, 2):
                    self.verts[index] = Vector(ix * 1, iy * 1, iz * 1)
                    index += 1

        self.add_face([0, 2, 3, 1])
        self.add_face([0, 4, 6, 2])
        self.add_face([4, 5, 7, 6])
        self.add_face([1, 3, 7, 5])
        self.add_face([2, 6, 7, 3])
        self.add_face([0, 1, 5, 4])

class Octohedron(PlatonicSolid):
    def __init__(self):
        super(Octohedron, self).__init__("Octohedron", 6)

    def add_face(self, indices, normal=None):
        if not normal:
            vertex_a = self.verts[indices[0]]
            vertex_b = self.verts[indices[1]]
            normal = self.calculate_normal(vertex_a, vertex_b)

        self.tris.append(Triangle([ indices[0], indices[1], indices[2] ], normal))

    def orientate_to_base(self):
        self.perform_rotation(RotationMatrixZAxis(math.pi * 0.25))
        if self.is_split:
            self.perform_translation(Vector(-1,1,0))
        else:
            self.perform_translation(Vector(-1,1,1))

    def generate(self, split):
        self.is_split = split

        self.verts[0] = Vector(-1, 0, 0)
        self.verts[1] = Vector( 1, 0, 0)
        self.verts[2] = Vector( 0,-1, 0)
        self.verts[3] = Vector( 0, 1, 0)
        self.verts[4] = Vector( 0, 0,-1)
        self.verts[5] = Vector( 0, 0, 1)

        self.add_face([1, 2, 5])
        self.add_face([5, 2, 0])
        self.add_face([1, 5, 3])
        self.add_face([5, 0, 3])
        if split:
            self.add_face([0, 1, 3], normal=Vector(0,0,-1))
            self.add_face([0, 2, 1], normal=Vector(0,0,-1))
        else:
            self.add_face([4, 2, 1])
            self.add_face([0, 2, 4])
            self.add_face([0, 4, 3])
            self.add_face([4, 1, 3])

class Dodecahedron(PlatonicSolid):
    def __init__(self):
        super(Dodecahedron, self).__init__("Dodecahedron", 20)

    def add_face(self, indices):
        vertex_a = self.verts[indices[0]]
        vertex_b = self.verts[indices[1]]
        normal = self.calculate_normal(vertex_a, vertex_b)
        self.tris.append(
            Triangle([ indices[0], indices[1], indices[2] ], normal))
        self.tris.append(
            Triangle([ indices[2], indices[3], indices[0] ], normal))
        self.tris.append(
            Triangle([ indices[3], indices[4], indices[0] ], normal))

    def orientate_to_base(self):
        angle = (2.0 * math.atan(PHI_GOLDEN)) * 0.5
        rot_matrix = RotationMatrixXAxis(angle)
        self.perform_rotation(rot_matrix)

        e = math.sqrt(5.0) - 1.0 # This is the edge length
        r = e * 0.5 * math.sqrt((5.0/2.0) + (11.0/10.0) * math.sqrt(5.0)) # This is the radius of an
                                                                          # inscribed sphere.
        c = math.sqrt(3.0) # This is the radius of a containing sphere.
        self.perform_translation(Vector(-c, c, r))

    def generate(self, split):
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

class Icosahedron(PlatonicSolid):
    def __init__(self):
        super(Icosahedron, self).__init__("Icosahedron", 12)

    def add_face(self, indices):
        vertex_a = self.verts[indices[0]]
        vertex_b = self.verts[indices[1]]
        normal = self.calculate_normal(vertex_a, vertex_b)
        self.tris.append(
            Triangle([ indices[0], indices[1], indices[2] ], normal))

    def orientate_to_base(self):
        angleY = (math.pi - math.acos(-math.sqrt(5.0)/3.0)) * 0.5
        rot_matrix = RotationMatrixYAxis(angleY)
        self.perform_rotation(rot_matrix)

        ri = (math.sqrt(3.0) / 12.0) * (3.0 + math.sqrt(5.0)) * 2.0 # Inscribed sphere
        self.perform_translation(Vector(-2,2,ri))

    def generate(self, split):
        phi = PHI_GOLDEN

        # I couldn't be bothered to calculate these verts and indices myself so
        # I took them from Andreas Kahler's blog:
        # (http://blog.andreaskahler.com/2009/06/creating-icosphere-mesh-in-code.html)
        self.verts[0] = Vector(-1, phi, 0)
        self.verts[1] = Vector( 1, phi, 0)
        self.verts[2] = Vector(-1,-phi, 0)
        self.verts[3] = Vector( 1,-phi, 0)

        self.verts[4] = Vector(0,-1, phi)
        self.verts[5] = Vector(0, 1, phi)
        self.verts[6] = Vector(0,-1,-phi)
        self.verts[7] = Vector(0, 1,-phi)

        self.verts[8]  = Vector( phi, 0,-1)
        self.verts[9]  = Vector( phi, 0, 1)
        self.verts[10] = Vector(-phi, 0,-1)
        self.verts[11] = Vector(-phi, 0, 1)

        self.add_face([0, 11, 5]);
        self.add_face([0, 5,  1]);
        self.add_face([0, 1,  7]);
        self.add_face([0, 7,  10]);
        self.add_face([0, 10, 11]);

        self.add_face([1,  5,  9]);
        self.add_face([5,  11, 4]);
        self.add_face([11, 10, 2]);
        self.add_face([10, 7,  6]);
        self.add_face([7,  1,  8]);

        self.add_face([3, 9, 4]);
        self.add_face([3, 4, 2]);
        self.add_face([3, 2, 6]);
        self.add_face([3, 6, 8]);
        self.add_face([3, 8, 9]);

        self.add_face([4, 9, 5]);
        self.add_face([2, 4, 11]);
        self.add_face([6, 2, 10]);
        self.add_face([8, 6, 7]);
        self.add_face([9, 8, 1]);

class STLWriter:
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

        for triangle in solid.tris:
            vertex_a = solid.verts[triangle["indices"][0]]
            vertex_b = solid.verts[triangle["indices"][1]]
            vertex_c = solid.verts[triangle["indices"][2]]
            normal   = triangle["normal"]

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
        3: Octohedron(),
        4: Dodecahedron(),
        5: Icosahedron()
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
                3. Octahedron (can be split)
                4. Dodecahedron
                5. Icosahedron
            '''))
    parser.add_argument('--type', required=True, help='type of solid to generate.')
    parser.add_argument('--split', required=False, action='store_true', help='splits the solid for ease of printing.')
    args = parser.parse_args()

    solid_type = int(args.type)
    if not solid_type in SOLIDS:
        print "Invalid type. Run with --help to list type names."
    else:
        solid = SOLIDS[solid_type]
        print "Generating solid of type " + solid.name
        solid.generate(args.split)
        solid.orientate_to_base()

        writer = STLWriter()
        writer.write(solid)

        print "Done!"

