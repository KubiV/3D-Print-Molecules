from Bio import PDB
import numpy as np

from multisphere import create_and_save_multiple_spheres 

def extract_coordinates(pdb_filename):
    # Create a PDB parser
    parser = PDB.PDBParser(QUIET=True)

    # Load the structure from the PDB file
    structure = parser.get_structure('protein', pdb_filename)

    # Dictionary to store coordinates for each atom type
    atom_coordinates = {}

    # Iterate over all models in the structure
    for model in structure:
        # Iterate over all chains in the model
        for chain in model:
            # Iterate over all residues in the chain
            for residue in chain:
                # Iterate over all atoms in the residue
                for atom in residue:
                    atom_type = atom.element
                    
                    coordinates = atom.coord

                    # Check if atom_type is already in the dictionary
                    if atom_type not in atom_coordinates:
                        atom_coordinates[atom_type] = []

                    # Append the modified coordinates to the corresponding atom type
                    atom_coordinates[atom_type].append(coordinates)
                    
    return atom_coordinates

# Example usage
pdb_filename = '/Users/jakubvavra/Documents/GitHub/3D-Print-Molecules/version2/NAD.pdb'
coordinates = extract_coordinates(pdb_filename)

for key in coordinates:
    print(key)

#specific_atom_coordinates = {}
#for key in coordinates:
#    specific_atom_coordinates[f'{key}_coordinates'] = coordinates.get(key, [])



# Accessing coordinates for specific atom types
h_coordinates = coordinates.get('H', [])
o_coordinates = coordinates.get('O', [])
c_coordinates = coordinates.get('C', [])
p_coordinates = coordinates.get('P', [])
n_coordinates = coordinates.get('N', [])


#print(coordinates)

#print('Hydrogen:', hydrogen_coordinates)
#print('Oxygen:', oxygen_coordinates)
#print('Carbon:', carbon_coordinates)

radius = 1.0
resolution = 100

create_and_save_multiple_spheres(radius, resolution, h_coordinates, "h_atoms.stl")
create_and_save_multiple_spheres(radius, resolution, p_coordinates, "p_atoms.stl")
create_and_save_multiple_spheres(radius, resolution, o_coordinates, "o_atoms.stl")
create_and_save_multiple_spheres(radius, resolution, n_coordinates, "n_atoms.stl")
create_and_save_multiple_spheres(radius, resolution, c_coordinates, "c_atoms.stl")