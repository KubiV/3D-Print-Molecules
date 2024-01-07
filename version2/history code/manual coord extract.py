import re

# Your regex pattern
#pattern1 = r'^HETATM\s+(\d+)\s+([A-Za-z]+)\s+([A-Za-z0-9]+)\s+(\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+([A-Za-z]+)\s*$'
pattern2 = r'^HETATM\s+(\d+)\s+([A-Za-z0-9]+(?:-[A-Za-z0-9]+)?)\s+([A-Za-z0-9]+)\s*([A-Za-z]?)\s*(\d*)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s*([A-Za-z]*)\s*$'
pattern3 = r'^HETATM\s+(\d+)\s+(\S+)\s+(\w+)\s+(\w+)\s+(\d+)\s+([-+]?\d*\.\d+)\s+([-+]?\d*\.\d+)\s+([-+]?\d*\.\d+)\s+([-+]?\d*\.\d+)\s+([-+]?\d*\.\d+)\s+(\S+)'

# Example string
example_string = "HETATM    1  O   UNL     1      -0.668   1.159   0.257  1.00  0.00           O"
example_string1 = "HETATM    2  H   HOH     0       3.074   0.155   0.000  1.00  0.00           H"
example_string2 = "HETATM    8  O1N NAD C 501     101.397 127.737  23.131  1.00 12.28           O1-"

def if_match():
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
        print("No match found.")
        print()

# Applying the regex pattern
pattern = pattern3
match = re.match(pattern, example_string)
if_match()
match = re.match(pattern, example_string1)
if_match()
match = re.match(pattern, example_string2)
if_match()

