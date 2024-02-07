import re
import numpy as np
import csv
import os
import zipfile
import shutil
import tempfile
import json
from ModelGenerating import create_and_save_multiple_spheres
from PDBfileParse import extract_coordinates2 
import PeriodicTable

def load_setting(key):
    """Load a specific setting by key from a JSON file."""
    settings_file_path = os.path.join(os.path.dirname(__file__), 'Settings.json')
    try:
        with open(settings_file_path, 'r') as file:
            settings = json.load(file)
        return settings.get(key)
    except FileNotFoundError:
        print("Settings file not found.")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON from the settings file.")
        return None

#--- Example data ---#

# Your regex patterns
pattern1 = r'^HETATM\s+(\d+)\s+([A-Za-z0-9]+(?:-[A-Za-z0-9]+)?)\s+([A-Za-z0-9]+)\s*([A-Za-z]?)\s*(\d*)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s*([A-Za-z]*)\s*$'
pattern2 = r'^HETATM\s+(\d+)\s+(\S+)\s+(\w+)\s+(\w+)\s+(\d+)\s+([-+]?\d*\.\d+)\s+([-+]?\d*\.\d+)\s+([-+]?\d*\.\d+)\s+([-+]?\d*\.\d+)\s+([-+]?\d*\.\d+)\s+(\S+)'
pattern3 = r"\s*([-+]?\d*\.\d+)\s+([-+]?\d*\.\d+)\s+([-+]?\d*\.\d+)\s+(\w+)\s*"

patterns = {
    'pattern1': pattern1, 
    'pattern2': pattern2,
    'pattern3': pattern3
}

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

#--- Testing code ---#

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

#--- Used code ---#

def match_coord(match, pattern, a, b, c, d):
    if match:
        atom = match.group(a) #2 for patter2, 11 for pattern1
        atom_type = re.sub(r'\d.*', '', atom)
        x_coord = float(match.group(b))
        y_coord = float(match.group(c))
        z_coord = float(match.group(d))

        return atom_type, x_coord, y_coord, z_coord
    #else:
        #print()

def extract_coord(data_lines):
    # Dictionary to store coordinates for each atom type
    atom_coordinates = {}

    # Check if the file_path is indeed a path to an existing file
    if os.path.isfile(data_lines):
        # If it is, open the file and read its contents
        with open(data_lines, 'r') as data_lines:
            data_lines = data_lines.readlines()

    for line in data_lines:
        # Try the first pattern
        pattern_key = 'pattern1'
        pattern = patterns[pattern_key]
        match = re.match(pattern, line)
        result = match_coord(match, pattern, 11, 6, 7, 8)

        # If the first pattern doesn't match, try the second pattern
        if not match:
            pattern_key = 'pattern2'
            pattern = patterns[pattern_key]
            match = re.match(pattern, line)
            result = match_coord(match, pattern, 2, 6, 7, 8)

            if not match:
                pattern_key = 'pattern3'
                pattern = patterns[pattern_key]
                match = re.match(pattern, line)
                result = match_coord(match, pattern, 4, 1, 2, 3)

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

def find_radius_csv(csv_filename, target_value):
    with open(csv_filename, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(csvfile)  # Skip the header row if it exists
        for row in reader:
            # Check if the value in the 2nd column (index 1) matches the target_value
            if len(row) > 1 and row[1] == target_value:
                # If the condition is met, print the value in the 8th column (index 7)
                if len(row) > 7:
                    return (float(row[7])/100)  
    # If no match is found, return None or an appropriate value
    return None
                     
def find_radius_pymodule(data, target_value):
    for element in data:
        # Check if the value in the 'Symbol' key matches the target_value
        if element.get('Symbol') == target_value:
            # If the condition is met, return the value in the 'AtomicRadius' key divided by 100
            return float(element.get('AtomicRadius', 0)) / 100
    # If no match is found, return None or an appropriate value
    return None
    # Example usage: print(find_radius_pymodule(PeriodicTable.PeriodicTableData, "H"))

def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            total_size += os.path.getsize(file_path)
    return total_size

def count_carbons(input):
    c_count = len(input.get('C', []))
    return c_count

def choose_function(function1, function2, *args, **kwargs):
    # Call the first function
    output1 = function1(*args, **kwargs)

    # Count 'C' in the output
    c_count = count_carbons(output1)
    print("C in atom: "+ str(c_count))
    # Check if there are less than 2 'C'
    if c_count < 2:
        output2 = function2(*args, **kwargs)
        return output2
    else:
        return output1

def make_molecule_stl_VanDerWaals(pdb_filename, resolution, csv_filename, radius_factor, hydrogens):

    coordinates_dict = choose_function(extract_coordinates2, extract_coord, pdb_filename)

    # Long C chain -> big file protection
    c_count = count_carbons(coordinates_dict)
    if c_count > load_setting('large_c_chain_protection'):
        print("Large file protection ACTIVATED")
        if resolution > load_setting('resolution_limit'):
            resolution = load_setting('resolution_limit')
        print("Resolution: "+str(resolution))

    # Generate for all atoms their 3D model
    #for key, coordinates in coordinates_dict.items():
    #    coordinates = coordinates_dict.get(key, [])
    #    radius = find_radius_pymodule(PeriodicTable.PeriodicTableData, key)
    #    if radius is None:
    #        continue
    #    radius_final = radius * radius_factor
    #    create_and_save_multiple_spheres(radius_final, resolution, coordinates, f"{key}_atoms.stl")
    for key, coordinates in coordinates_dict.items():
        # Skip hydrogen atoms if hydrogens is False
        if not hydrogens and key == "H":
            continue
        coordinates = coordinates_dict.get(key, [])
        radius = find_radius_pymodule(PeriodicTable.PeriodicTableData, key)
        if radius is None:
            continue
        radius_final = radius * radius_factor
        create_and_save_multiple_spheres(radius_final, resolution, coordinates, f"{key}_atoms.stl")
   
def ZIPmolecule(model ,pdb_filename, resolution, csv_filename, radius_factor, filename, hydrogens):
    #base_pdb_filename, _ = os.path.splitext(os.path.basename(pdb_filename))
    #zip_filename = f"Molecule_{base_pdb_filename}.zip"
    zip_filename = "Molecule_"+str(filename)+".zip"

    print("model for: "+pdb_filename)

    original_directory = os.getcwd()
    try:
        # Create a temporary directory
        temp_directory = tempfile.mkdtemp()
        initial_size = get_folder_size(temp_directory)

        generate_model = True

        # Change the working directory to the temporary directory
        os.chdir(temp_directory)

        # Perform your function here
        if model == "VDW":
            make_molecule_stl_VanDerWaals(pdb_filename, resolution, csv_filename, radius_factor, hydrogens)
        elif model =="BS":
            generate_model = False
            print("Can not create ball and stick model")

        while True:

            current_size = get_folder_size(temp_directory)

            if current_size > initial_size:
                print(f"Folder size is increasing: {current_size} bytes")
                initial_size = current_size
            else:
                print(f"Folder size is not increasing.")
                break
                
        # For example, you can create files, manipulate data, etc.
        print("Current working directory:", os.getcwd())

    finally:
        # Change the working directory back to the original directory
        os.chdir(original_directory)

        if generate_model == True:
            with zipfile.ZipFile(zip_filename, 'w') as zip_file:
                # Add files from temp_dir to the zip file
                for foldername, subfolders, filenames in os.walk(temp_directory):
                    for filename in filenames:
                        file_path = os.path.join(foldername, filename)
                        zip_file.write(file_path, os.path.relpath(file_path, temp_directory))

            print(f"Files moved to {zip_filename}")

        # Comment the next line if you want to keep the temporary directory
        shutil.rmtree(temp_directory)
        #os.rmdir(temp_directory)

        print("Back to original working directory:", os.getcwd())

#--- Example test usage ---#

# Set output path
output_directory = "/Users/jakubvavra/Desktop"
os.chdir(output_directory)

# Load data from the CSV file
csv_filename = 'PubChemElements_all.csv'
csv_path = os.path.abspath(__file__)
csv_absolute_path = os.path.join(os.path.dirname(csv_path), csv_filename)

# Load data from the PDB file
#pdb_filename = '/Users/jakubvavra/Documents/GitHub/3D-Print-Molecules/version2/ExamplePDB/atp.pdb'  # Replace with the actual file name
pdb_filename = '/Users/jakubvavra/Documents/GitHub/3D-Print-Molecules/version2/ExamplePDB/4WB5.pdb' 
file_path = os.path.abspath(__file__)
pdb_absolute_path = os.path.join(os.path.dirname(file_path), pdb_filename)

# Atom model settings
radius_factor = 0.7
resolution = 10
filename = ""

#make_molecule_stl_VanDerWaals(pdb_absolute_path, resolution, csv_absolute_path, radius_factor)
#ZIPmolecule("VDW", pdb_absolute_path, resolution, csv_absolute_path, radius_factor, filename)