import os
import requests
import subprocess
import zipfile
import shutil
import time
import tempfile
import platform

os_type = platform.system()

PDB = input("PDB: ")
var = 'cmd.fetch("'+ PDB +'")'
var2 = 'cmd.set("sphere_quality", 1)' # Lower the number is lower the quality - 0 is suitable for really big mocules
TimeT = 30 # Sets the time delay needed for processing the 3D models


with tempfile.NamedTemporaryFile(suffix=".pml", delete=False) as temp_pml_script:
    temp_pml_scriptname = temp_pml_script.name


def elem_stl_output(elem):
  # Create a list of commands to generate the STL for the specified element
    return [
        'cmd.hide("everything")',
        'cmd.select("'+elem+'_atoms", "elem '+elem+'")',
        'cmd.show("surface", "'+elem+'_atoms")',
        'cmd.save("'+elem+'_output.stl", "'+elem+'_atoms")'
    ]

# PyMOL script to execute a list of PyMOL commands
lines_to_write = [
  var,
  #'cmd.set("sphere_scale", 0.7, "all")',
  #'cmd.set("sphere_mode", 0)',
  'cmd.set("solvent_radius", 0.5)',
  'cmd.set("surface_quality", 1)',
  var2,

  *elem_stl_output("C"),
  *elem_stl_output("O"),
  *elem_stl_output("H"),
  *elem_stl_output("N"),
  *elem_stl_output("S"),
  *elem_stl_output("P"),

  'cmd.show("surface", "all")',
  'cmd.save("Molecule.stl", "all")'
  # Add more lines as needed
]

with open(temp_pml_scriptname, 'w') as file:
    for line in lines_to_write:
        file.write(line + '\n')

if os_type == "Darwin":
    app_to_open_with = "/Applications/PyMOL.app/Contents/MacOS/PyMOL"
    print ("macOS - PyMOL")

# Use the subprocess module to open the file with the specified application
try:
    subprocess.Popen([app_to_open_with, temp_pml_scriptname])
    print(f"Opening {temp_pml_scriptname} with {app_to_open_with}...")
except FileNotFoundError:
    print(f"Error: The specified application '{app_to_open_with}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")

# Sleep for timer TimeT seconds
#time.sleep(TimeT) #spis se koukat jak se mění velikost nebo existence souborů - kontrola, když nemění tak jsi dál

# Sleep for 5 seconds
time.sleep(5)

# List of file paths to be deleted
files_delete = [
    temp_pml_scriptname,
    PDB + ".cif",
]

for file_to_delete in files_delete:
    try:
        os.remove(file_to_delete)
        print(f"{file_to_delete} has been deleted.")
    except FileNotFoundError:
        print(f"File not found: {file_to_delete}")
    except Exception as e:
        print(f"An error occurred while deleting {file_to_delete}: {e}")
