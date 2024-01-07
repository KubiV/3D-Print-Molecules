import re
import numpy as np
from multisphere import create_and_save_multiple_spheres 

# Your regex patterns
pattern1 = r'^HETATM\s+(\d+)\s+([A-Za-z0-9]+(?:-[A-Za-z0-9]+)?)\s+([A-Za-z0-9]+)\s*([A-Za-z]?)\s*(\d*)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s*([A-Za-z]*)\s*$'
pattern2 = r'^HETATM\s+(\d+)\s+(\S+)\s+(\w+)\s+(\w+)\s+(\d+)\s+([-+]?\d*\.\d+)\s+([-+]?\d*\.\d+)\s+([-+]?\d*\.\d+)\s+([-+]?\d*\.\d+)\s+([-+]?\d*\.\d+)\s+(\S+)'

patterns = {'pattern1': pattern1, 'pattern2': pattern2}

# Example strings
example_string = "HETATM    1  O   UNL     1      -0.668   1.159   0.257  1.00  0.00           O"
example_string1 = "HETATM    2  H   HOH     0       3.074   0.155   0.000  1.00  0.00           H"
example_string2 = "HETATM    8  O1N NAD C 501     101.397 127.737  23.131  1.00 12.28           O1-"
a = [example_string, example_string1, example_string2]

# Example usage
pdb_lines = [
    'HETATM   1  H  H2  A   1       96.012 124.771  24.383  1.00  0.00           H',
    'HETATM   2  H  H2  A   1      100.542 138.616  18.783  1.00  0.00           H',
    'HETATM   3  H  H2  A   1       91.179 127.363  26.151  1.00  0.00           H',
    'HETATM   4  H  H2  A   1       89.556 127.102  25.55   1.00  0.00           H',
    'HETATM   5  H  H2  A   1       97.748 129.913  20.409  1.00  0.00           H',
    'HETATM   6  H  H2  A   1       99.759 126.507  25.112  1.00  0.00           H',
    'HETATM   7  H  H2  A   1      101.481 137.266  19.379  1.00  0.00           H',
]

def match_values(match, pattern):
    if match:
        # Extracting values from the match object
        atom_number = int(match.group(1))
        atom_type = match.group(2)
        molecule_name = match.group(3)
        chain_identifier = match.group(4)
        residue_number = int(match.group(5)) if match.group(5) else None  # Handle optional residue number
        x_coord = float(match.group(6))
        y_coord = float(match.group(7))
        z_coord = float(match.group(8))
        occupancy = float(match.group(9))
        temp_factor = float(match.group(10))
        element_symbol = match.group(11)

        # Printing the extracted values
        print("Atom Number:", atom_number)
        print("Atom Type:", atom_type)
        print("Molecule Name:", molecule_name)
        print("Chain Identifier:", chain_identifier)
        print("Residue Number:", residue_number)
        print("X Coordinate:", x_coord)
        print("Y Coordinate:", y_coord)
        print("Z Coordinate:", z_coord)
        print("Occupancy:", occupancy)
        print("Temperature Factor:", temp_factor)
        print("Element Symbol:", element_symbol)
        print()
    else:
        print("No match found. Trying the other pattern.")
        print()

def extract_values(data_lines):
    for line in data_lines:
        print(f"Example Line: {line}")

        # Try the first pattern
        pattern_key = 'pattern1'
        pattern = patterns[pattern_key]
        match = re.match(pattern, line)
        match_values(match, pattern)

        # If the first pattern doesn't match, try the second pattern
        if not match:
            pattern_key = 'pattern2'
            pattern = patterns[pattern_key]
            match = re.match(pattern, line)
            match_values(match, pattern)

#--------------

def match_coord(match, pattern):
    if match:
        atom_type = match.group(2)
        x_coord = float(match.group(6))
        y_coord = float(match.group(7))
        z_coord = float(match.group(8))

        return atom_type, x_coord, y_coord, z_coord
    else:
        print("No match found. Trying the other pattern.")
        print()

def extract_coord(data_lines):
    # Dictionary to store coordinates for each atom type
    atom_coordinates = {}

    for line in data_lines:
        # Try the first pattern
        pattern_key = 'pattern1'
        pattern = patterns[pattern_key]
        match = re.match(pattern, line)
        result = match_coord(match, pattern)

        # If the first pattern doesn't match, try the second pattern
        if not match:
            pattern_key = 'pattern2'
            pattern = patterns[pattern_key]
            match = re.match(pattern, line)
            result = match_coord(match, pattern)

        # If coordinates are found, save them to the NumPy array
        if result:
            atom_type, x_coord, y_coord, z_coord = result

            print(f"{atom_type}, {x_coord, y_coord, z_coord}")

            if atom_type not in atom_coordinates:
                atom_coordinates[atom_type] = []
            atom_coordinates[atom_type].append([x_coord, y_coord, z_coord])

    # Convert the dictionary values to NumPy arrays
    for atom_type, coords_list in atom_coordinates.items():
        atom_coordinates[atom_type] = np.array(coords_list)

    return atom_coordinates

# Read PDB file and extract lines
pdb_filename = '/Users/jakubvavra/Documents/GitHub/3D-Print-Molecules/version2/example pdb/NAD.pdb'  # Replace with the actual file name
with open(pdb_filename, 'r') as pdb_file:
    pdb_lines = pdb_file.readlines()

coordinates = extract_coord(pdb_lines)
print(coordinates)

# Accessing coordinates for specific atom types
#h_coordinates = coordinates.get('H', [])
#o_coordinates = coordinates.get('O', [])
#c_coordinates = coordinates.get('C', [])

#print('Hydrogen:', h_coordinates)
#print('Oxygen:', o_coordinates)
#print('Carbon:', c_coordinates)

radius = 0.7
resolution = 100

#create_and_save_multiple_spheres(1.2*radius, resolution, h_coordinates, "h_atoms.stl")
#create_and_save_multiple_spheres(1.52*radius, resolution, o_coordinates, "o_atoms.stl")
#create_and_save_multiple_spheres(1.7*radius, resolution, c_coordinates, "c_atoms.stl")