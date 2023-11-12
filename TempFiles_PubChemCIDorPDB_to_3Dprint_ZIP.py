# Fist of all install the Incentive PyMOL app - https://pymol.org/
# Search the CID of the molecule on PubChem - https://pubchem.ncbi.nlm.nih.gov
# Or search the PDB code of the protein and choose which way do you want to enter the molecule
# Make sure that you have set the right executable file of PyMOL an Open Babel for your operating system - PyMOL: app_to_open_with = "executable_file"

import os
import requests
import subprocess
import zipfile
import shutil
import time
import tempfile
import platform

os_type = platform.system()

choice = input("CID number / PDB code / PDB file path (cid/pdb/file.pdb): ")

if choice == "CID" or choice == "cid":
    CID = input("PubChem CID: ")
    url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/"+ CID +"/record/SDF?record_type=3d&response_type=display"

    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Create a temporary file to store the SDF data
        with tempfile.NamedTemporaryFile(suffix=".sdf", delete=False) as temp_sdf_file:
            temp_sdf_filename = temp_sdf_file.name
            temp_sdf_file.write(response.content)

        print(f"File saved as {temp_sdf_filename}")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")
        exit(1)


    # Check if the temporary SDF file exists
    if not os.path.exists(temp_sdf_filename):
        print(f"Error: Temporary SDF file not found at {temp_sdf_filename}")
        exit(1)

    with tempfile.NamedTemporaryFile(suffix=".pdb", delete=False) as temp_pdb_file:
        temp_pdb_filename = temp_pdb_file.name

    # Run the obabel command
    if os_type == "Darwin":
        print ("macOS - obabel")
        command = ["obabel", temp_sdf_filename, "-O", temp_pdb_filename]
        subprocess.run(command, check=True)
        print("SDF to PDB conversion completed.")

    if os_type == "Linux": # needs to be finished!
        print ("Linux - obabel")
        command = ["obabel", temp_sdf_filename, "-O", temp_pdb_filename]
        subprocess.run(command, check=True)
        print("SDF to PDB conversion completed.")

    if os_type == "Windows":
        print("Windows - obabel")
        command = ["C:\Program Files\OpenBabel-3.1.1\obabel.exe", temp_sdf_filename, "-O", temp_pdb_filename] #"C:\\path\\to\\obabel.exe"
        try:
            # Run the obabel command
            subprocess.run(command, check=True)
            print("SDF to PDB conversion completed.")
        except subprocess.CalledProcessError as e:
            print(f"Error running obabel: {e}")

    var = 'cmd.load("'+ temp_pdb_filename +'")'
    var2 = 'cmd.set("sphere_quality", 3)' # Lower the number is lower the quality - 3 is high
    TimeT = 5 # Sets the time delay needed for processing the 3D models

if choice == "PDB" or choice == "pdb":
    PDB = input("PDB: ")
    var = 'cmd.fetch("'+ PDB +'")'
    var2 = 'cmd.set("sphere_quality", 0)' # Lower the number is lower the quality - 0 is suitable for really big mocules
    TimeT = 30 # Sets the time delay needed for processing the 3D models

if choice.endswith(".pdb") or choice.endswith(".pdb ") or choice.endswith(".pdb'"):
    print("Own pdb file")
    var = 'cmd.load("'+ choice +'")'
    var2 = 'cmd.set("sphere_quality", 3)'
    TimeT = 5
else:
    print("The input does not end with '.pdb'")

with tempfile.NamedTemporaryFile(suffix=".pml", delete=False) as temp_pml_script:
    temp_pml_scriptname = temp_pml_script.name


def elem_stl_output(elem):
  # Create a list of commands to generate the STL for the specified element
    return [
        'cmd.hide("everything")',
        'cmd.select("'+elem+'_atoms", "elem '+elem+'")',
        'cmd.show("sphere", "'+elem+'_atoms")',
        'cmd.save("'+elem+'_output.stl", "'+elem+'_atoms")'
    ]

# PyMOL script to execute a list of PyMOL commands
lines_to_write = [
  var,
  'cmd.set("sphere_scale", 0.7, "all")',
  'cmd.set("sphere_mode", 0)',
  var2,

  *elem_stl_output("C"),
  *elem_stl_output("O"),
  *elem_stl_output("H"),
  *elem_stl_output("N"),
  *elem_stl_output("S"),
  *elem_stl_output("P"),

  'cmd.show("spheres", "all")',
  #'cmd.save("Molecule.stl", "all")'
  # Add more lines as needed
]

with open(temp_pml_scriptname, 'w') as file:
    for line in lines_to_write:
        file.write(line + '\n')

if os_type == "Darwin":
    app_to_open_with = "/Applications/PyMOL.app/Contents/MacOS/PyMOL"
    print ("macOS - PyMOL")

if os_type == "Linux": # needs to be finished!
    app_to_open_with = ""
    print ("Linux - PyMOL")

if os_type == "Windows":
    app_to_open_with = r"C:\Users\Admin\AppData\Local\Schrodinger\PyMOL2\PyMOLWin.exe"
    print("Windows - PyMOL")

# Use the subprocess module to open the file with the specified application
try:
    subprocess.Popen([app_to_open_with, temp_pml_scriptname])
    print(f"Opening {temp_pml_scriptname} with {app_to_open_with}...")
except FileNotFoundError:
    print(f"Error: The specified application '{app_to_open_with}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")

# Define the directory where your files are located
source_folder = '.'
zip_file_name = 'MultiBody_molecule.zip'
files_to_move = ['C_output.stl', 'O_output.stl', 'H_output.stl', 'N_output.stl', 'S_output.stl', 'P_output.stl']

temp_dir = tempfile.TemporaryDirectory()
temp_dir_path = temp_dir.name

def wait_for_files(files, polling_interval=1):
    while True:
        all_stopped = True
        for filename in files:
            if os.path.exists(filename):
                initial_size = os.path.getsize(filename)
                time.sleep(polling_interval)
                current_size = os.path.getsize(filename)
                if current_size != initial_size:
                    all_stopped = False
            else:
                all_stopped = False
        if all_stopped:
            break
        time.sleep(polling_interval)

wait_for_files(files_to_move)

# Sleep for timer TimeT seconds
#time.sleep(TimeT) #spis se koukat jak se mění velikost nebo existence souborů - kontrola, když nemění tak jsi dál

# Move the files to the new folder
for file in files_to_move:
    source_path = os.path.join(source_folder, file)
    destination_path = os.path.join(temp_dir_path, file)

    try:
        shutil.move(source_path, destination_path)
        print(f"Moved {file} to {temp_dir_path}.")
    except FileNotFoundError:
        print(f"File not found: {file}")
    except Exception as e:
        print(f"An error occurred while moving {file}: {e}")

# Create a ZipFile object in write mode
with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for foldername, subfolders, filenames in os.walk(temp_dir_path):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            relative_path = os.path.relpath(file_path, temp_dir_path)
            zipf.write(file_path, relative_path)

print(f'{zip_file_name} has been created with the files from {temp_dir_path}.')

# Sleep for 5 seconds
time.sleep(5)

# List of file paths to be deleted
files_delete = [
    temp_sdf_filename,
    temp_pdb_filename,
    temp_pml_scriptname,
    temp_dir_path,
]

for file_to_delete in files_delete:
    try:
        os.remove(file_to_delete)
        print(f"{file_to_delete} has been deleted.")
    except FileNotFoundError:
        print(f"File not found: {file_to_delete}")
    except Exception as e:
        print(f"An error occurred while deleting {file_to_delete}: {e}")
