from Bio import PDB
import numpy as np
from stl import mesh

def get_atom_radius(atom_name):
    # Define radii for C, O, H, and N atoms
    radius_dict = {'C': 1.7, 'O': 1.52, 'H': 1.2, 'N': 1.55}
    return radius_dict.get(atom_name, 1.0)  # Default radius if atom is not C, O, H, or N

def create_sphere(center, radius, num_points=20):
    # Create a sphere mesh using numpy-stl
    phi = np.linspace(0, np.pi, num_points)
    theta = np.linspace(0, 2 * np.pi, num_points)
    phi, theta = np.meshgrid(phi, theta)

    x = center[0] + radius * np.sin(phi) * np.cos(theta)
    y = center[1] + radius * np.sin(phi) * np.sin(theta)
    z = center[2] + radius * np.cos(phi)

    return np.array([x, y, z]).T.reshape(-1, 3)

def pdb_to_stl_with_spheres(pdb_file_path, stl_file_path):
    parser = PDB.PDBParser(QUIET=True)
    structure = parser.get_structure('my_structure', pdb_file_path)

    vertices = []
    faces = []

    for model in structure:
        for chain in model:
            for residue in chain:
                for atom in residue:
                    atom_coord = atom.coord
                    atom_name = atom.get_id()[0]

                    # Get atom radius based on atom type
                    radius = get_atom_radius(atom_name)

                    # Create a sphere around the atom
                    sphere_vertices = create_sphere(atom_coord, radius)
                    vertices.extend(sphere_vertices)

    # Create a mesh using numpy-stl
    vertices = np.array(vertices)
    faces = np.arange(len(vertices)).reshape(-1, 3)
    
    mesh_data = mesh.Mesh(np.zeros(len(faces), dtype=mesh.Mesh.dtype))
    mesh_data.vectors = vertices[faces]

    # Write the mesh to an STL file
    mesh_data.save(stl_file_path)

# Replace 'your_input.pdb' and 'output.stl' with your actual file paths
pdb_to_stl_with_spheres('meth.pdb', 'output.stl')
