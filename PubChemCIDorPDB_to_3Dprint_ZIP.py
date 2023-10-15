# Fist of all install the Incentive PyMOL app - https://pymol.org/
# Search the CID of the molecule on PubChem - https://pubchem.ncbi.nlm.nih.gov
# Or search the PDB code of the protein and choose which way do you want to enter the molecule
# Make sure that you have set the right executable file of PyMOL for your operating system - app_to_open_with = "executable_file"

import os
import requests
import subprocess
import zipfile
import shutil
import time

choice = input("CID/PDB: ")

if choice == "CID":
    CID = input("PubChem CID: ")
    url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/"+ CID +"/record/SDF?record_type=3d&response_type=display"

    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
    # Specify the local file path where you want to save the downloaded file
        file_path = "input.sdf"
    
    # Open the local file in binary write mode and write the content from the response
        with open(file_path, 'wb') as file:
            file.write(response.content)
    
        print(f"File saved as {file_path}")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")

    sdf_file = "input.sdf"  # Replace with the path to your SDF file
    pdb_file = "output.pdb"  # Desired name for the output PDB file

    # Run the obabel command
    command = ["obabel", sdf_file, "-O", pdb_file]
    subprocess.run(command, check=True)

    print("SDF to PDB conversion completed.")

    var = 'cmd.load("output.pdb")'
    var2 = 'cmd.set("sphere_quality", 3)' # Lower the number is lower the quality - 3 is high
    TimeT = 5 # Sets the time delay needed for processing the 3D models
if choice == "PDB":
    PDB = input("PDB: ")
    var = 'cmd.fetch("' + PDB + '")'
    var2 = 'cmd.set("sphere_quality", 0)' # Lower the number is lower the quality - 0 is suitable for really big mocules
    TimeT = 30 # Sets the time delay needed for processing the 3D models
else:
    print("Not a valid input")


file_name = "script.pml"

# PyMOL script to execute a list of PyMOL commands
lines_to_write = [
  var,
  'cmd.load("output.pdb")',
  'cmd.set("sphere_scale", 0.7, "all")',
  'cmd.set("sphere_mode", 0)',
  var2,

  'cmd.hide("everything")',
  'cmd.select("carbon_atoms", "elem C")',
  'cmd.show("spheres", "carbon_atoms")',
  'cmd.save("C_output.stl", "carbon_atoms")',

  'cmd.hide("everything")',
  'cmd.select("hydrogen_atoms", "elem H")',
  'cmd.show("spheres", "hydrogen_atoms")',
  'cmd.save("H_output.stl", "hydrogen_atoms")',

  'cmd.hide("everything")',
  'cmd.select("nitrogen_atoms", "elem N")',
  'cmd.show("spheres", "nitrogen_atoms")',
  'cmd.save("N_output.stl", "nitrogen_atoms")',

  'cmd.hide("everything")',
  'cmd.select("oxygen_atoms", "elem O")',
  'cmd.show("spheres", "oxygen_atoms")',
  'cmd.save("O_output.stl", "oxygen_atoms")',

  'cmd.show("spheres", "all")',
  'cmd.save("Molecule.stl", "all")'
  # Add more lines as needed
]

with open(file_name, 'w') as file:
    for line in lines_to_write:
        file.write(line + '\n')

# Specify the path to the file you want to open
file_path = "script.pml"

# Specify the application or program you want to use to open the file
app_to_open_with = "/Applications/PyMOL.app/Contents/MacOS/PyMOL" # !!! Make sure to set the adress of the executable !!!

# Use the subprocess module to open the file with the specified application
try:
    subprocess.Popen([app_to_open_with, file_path])
    print(f"Opening {file_path} with {app_to_open_with}...")
except FileNotFoundError:
    print(f"Error: The specified application '{app_to_open_with}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")

# Define the directory where your files are located
source_folder = '.'
new_folder = 'new_folder'
zip_file_name = 'MultiBody_molecule.zip'
files_to_move = ['C_output.stl', 'O_output.stl', 'H_output.stl', 'N_output.stl']

# Create the new folder
os.mkdir(new_folder)  # Use os.makedirs(new_folder) to create parent directories if they don't exist

# Create the new folder if it doesn't exist
if not os.path.exists(new_folder):
    os.mkdir(new_folder)

# Sleep for timer TimeT seconds
time.sleep(TimeT)

# Move the files to the new folder
for file in files_to_move:
    source_path = os.path.join(source_folder, file)
    destination_path = os.path.join(new_folder, file)

    try:
        shutil.move(source_path, destination_path)
        print(f"Moved {file} to {new_folder}.")
    except FileNotFoundError:
        print(f"File not found: {file}")
    except Exception as e:
        print(f"An error occurred while moving {file}: {e}")

# Create a ZipFile object in write mode
with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for foldername, subfolders, filenames in os.walk(new_folder):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            relative_path = os.path.relpath(file_path, new_folder)
            zipf.write(file_path, relative_path)

print(f'{zip_file_name} has been created with the files from {new_folder}.')

# Sleep for 5 seconds
time.sleep(5)

# List of file paths to be deleted
files_delete = [
    "input.sdf",
    "output.pdb",
    "script.pml",
    "new_folder/C_output.stl",
    "new_folder/O_output.stl",
    "new_folder/H_output.stl",
    "new_folder/N_output.stl",
]

for file_to_delete in files_delete:
    try:
        os.remove(file_to_delete)
        print(f"{file_to_delete} has been deleted.")
    except FileNotFoundError:
        print(f"File not found: {file_to_delete}")
    except Exception as e:
        print(f"An error occurred while deleting {file_to_delete}: {e}")

# Check if the folder exists before attempting to delete it
if os.path.exists(new_folder):
    # Remove the folder and its contents
    os.rmdir(new_folder)  # Use os.rmdir() to delete an empty folder
    # Alternatively, use shutil.rmtree() to delete a folder and its contents, including subdirectories
    # shutil.rmtree(new_folder)
    print(f"{new_folder} has been deleted.")
else:
    print(f"{new_folder} does not exist.")