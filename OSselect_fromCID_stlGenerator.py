import os
import requests
import subprocess
import zipfile
import shutil
import time
import tempfile
import platform

os_type = platform.system()

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
    app_to_open_with = "/Applications/PyMOL.app/Contents/MacOS/PyMOL"
    print ("macOS")
    command = ["obabel", temp_sdf_filename, "-O", temp_pdb_filename]
    subprocess.run(command, check=True)
    print("SDF to PDB conversion completed.")

if os_type == "Linux": # needs to be finished!
    app_to_open_with = ""
    print ("Linux")
    command = ["obabel", temp_sdf_filename, "-O", temp_pdb_filename]
    subprocess.run(command, check=True)
    print("SDF to PDB conversion completed.")

if os_type == "Windows":
    app_to_open_with = r"C:\Users\Admin\AppData\Local\Schrodinger\PyMOL2\PyMOLWin.exe"
    print("Windows")
    command = ["C:\Program Files\OpenBabel-3.1.1\obabel.exe", temp_sdf_filename, "-O", temp_pdb_filename] #"C:\\path\\to\\obabel.exe"
    try:
        # Run the obabel command
        subprocess.run(command, check=True)
        print("SDF to PDB conversion completed.")
    except subprocess.CalledProcessError as e:
        print(f"Error running obabel: {e}")

def elem_stl_output(elem):
  # Create a list of commands to generate the STL for the specified element
    return [
        'cmd.hide("everything")',
        'cmd.select("'+elem+'_atoms", "elem '+elem+'")',
        'cmd.show("sphere", "'+elem+'_atoms")',
        'cmd.save("'+elem+'_output.stl", "'+elem+'_atoms")'
    ]

var = 'cmd.load(r"'+ temp_pdb_filename +'")'
var2 = 'cmd.set("sphere_quality", 3)' # Lower the number is lower the quality - 3 is high
TimeT = 5 # Sets the time delay needed for processing the 3D models

with tempfile.NamedTemporaryFile(suffix=".pml", delete=False) as temp_pml_script:
    temp_pml_scriptname = temp_pml_script.name

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

# Use the subprocess module to open the file with the specified application
try:
    subprocess.Popen([app_to_open_with, temp_pml_scriptname])
    print(f"Opening {temp_pml_scriptname} with {app_to_open_with}...")
except FileNotFoundError:
    print(f"Error: The specified application '{app_to_open_with}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")


