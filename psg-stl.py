import argparse, textwrap, math

def Vector(x, y, z):
    return {
        "x": x,
        "y": y,
        "z": z
    }

def StringifyVectorWithSpaces(vector):
    s = ""
    s += "%.6f" % vector["x"] + " "
    s += "%.6f" % vector["y"] + " "
    s += "%.6f" % vector["z"]
    return s

def CalculateNormal(a, b):
    # Cross product a x b, then normalise
    x = a["y"] * b["z"] - a["z"] * b["y"]
    y = a["z"] * b["x"] - a["x"] * b["z"]
    z = a["x"] * b["y"] - a["y"] * b["x"]
    l = math.sqrt(x*x + y*y + z*z)
    return Vector(x/l,y/l,z/l)

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
        super(Cube, self).__init__("Cube", 6)

SOLIDS = {
    1: Tetrahedron(),
    2: Cube()
}

class PlatonicSolidGenerator:
    def generate(self, solid_type):
        if not solid_type in SOLIDS:
            print "Invalid type. Run with --help to list type names."
            return None

        print "Generating solid of type " + SOLIDS[solid_type].name
        solid = SOLIDS[solid_type]
        solid.generate()

        return solid

class STLWriter:
    def write(self, solid):
        file_name = solid.name + ".stl"
        f = open(file_name, "w")
        f.write("solid " + solid.name + "\n")

        for face in solid.indices:
            vertex_a = solid.verts[face[0]]
            vertex_b = solid.verts[face[1]]
            vertex_c = solid.verts[face[2]]
            normal   = CalculateNormal(vertex_a, vertex_b)

            f.write("facet normal ")
            f.write(StringifyVectorWithSpaces(normal) + "\n")
            f.write("\touter loop\n")

            # Vertex A
            f.write("\t\tvertex ")
            f.write(StringifyVectorWithSpaces(vertex_a) + "\n")
            # Vertex B
            f.write("\t\tvertex ")
            f.write(StringifyVectorWithSpaces(vertex_b) + "\n")
            # Vertex C
            f.write("\t\tvertex ")
            f.write(StringifyVectorWithSpaces(vertex_c) + "\n")

            f.write("\tendloop\n")
            f.write("endfacet\n\n")

        f.write("endsolid " + solid.name + "\n")

if __name__ == '__main__':
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

    generator = PlatonicSolidGenerator()
    writer    = STLWriter()

    solid     = generator.generate(int(args.type))
    writer.write(solid)
    print "Done!"

