import re

# Your regex patterns
pattern2 = r'^HETATM\s+(\d+)\s+([A-Za-z0-9]+(?:-[A-Za-z0-9]+)?)\s+([A-Za-z0-9]+)\s*([A-Za-z]?)\s*(\d*)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s*([A-Za-z]*)\s*$'
pattern3 = r'^HETATM\s+(\d+)\s+(\S+)\s+(\w+)\s+(\w+)\s+(\d+)\s+([-+]?\d*\.\d+)\s+([-+]?\d*\.\d+)\s+([-+]?\d*\.\d+)\s+([-+]?\d*\.\d+)\s+([-+]?\d*\.\d+)\s+(\S+)'

# Example strings
example_string = "HETATM    1  O   UNL     1      -0.668   1.159   0.257  1.00  0.00           O"
example_string1 = "HETATM    2  H   HOH     0       3.074   0.155   0.000  1.00  0.00           H"
example_string2 = "HETATM    8  O1N NAD C 501     101.397 127.737  23.131  1.00 12.28           O1-"

def extract_values(match, pattern):
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

# Applying the regex patterns
patterns = {'pattern2': pattern2, 'pattern3': pattern3}

for example_string in [example_string, example_string1, example_string2]:
    print(f"Example String: {example_string}")

    # Try the first pattern
    pattern_key = 'pattern2'
    pattern = patterns[pattern_key]
    match = re.match(pattern, example_string)
    extract_values(match, pattern)

    # If the first pattern doesn't match, try the second pattern
    if not match:
        pattern_key = 'pattern3'
        pattern = patterns[pattern_key]
        match = re.match(pattern, example_string)
        extract_values(match, pattern)
