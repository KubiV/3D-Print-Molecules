
import re

example_string = "HETATM    1  O   UNL     1      -0.668   1.159   0.257  1.00  0.00           O"
example_string1 = "HETATM    2  H   HOH     0       3.074   0.155   0.000  1.00  0.00           H"
example_string2 = "HETATM    8  O1N NAD C 501     101.397 127.737  23.131  1.00 12.28           O1-"

pdb_regex = r"^(ATOM|HETATM|ANISOU|TER|SEQRES|HELIX|SHEET|LINK|CISPEP|SITE|REMARK)\s+(\d+)\s+(\w+)\s+(\w+)\s+(\w+)\s+([-+]?\d*\.\d+|\d+)\s+([-+]?\d*\.\d+|\d+)\s+([-+]?\d*\.\d+|\d+)\s+([-+]?\d*\.\d+|\d+)\s+([-+]?\d*\.\d+|\d+)\s+(\w+|-?)"

for string in [example_string, example_string1, example_string2]:
    match = re.match(pdb_regex, string)
    if match:
        record_type, serial_number, atom_name, residue_name, chain_id, x, y, z, occupancy, temperature_factor, element_symbol = match.groups()
        print(f"Record Type: {record_type}, Serial Number: {serial_number}, Atom Name: {atom_name}, Residue Name: {residue_name}, Chain ID: {chain_id}, X: {x}, Y: {y}, Z: {z}, Occupancy: {occupancy}, Temperature Factor: {temperature_factor}, Element Symbol: {element_symbol}")
