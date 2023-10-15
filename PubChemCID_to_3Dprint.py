# Fist of all install the Incentive PyMOL app - https://pymol.org/
# Search the CID of the molecule on PubChem - https://pubchem.ncbi.nlm.nih.gov 
# Make sure that you have set the right executable file of PyMOL for your operating system - line 78
import os
import requests
import subprocess

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

file_name = "script.pml"

# PyMOL script to execute a list of PyMOL commands
lines_to_write = [
  'cmd.load("output.pdb")',
  'cmd.set("sphere_scale", 0.7, "all")',
  'cmd.set("sphere_mode", 0)',
  'cmd.set("sphere_quality", 3)',

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
  'cmd.save("All_output.stl", "all")'
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

# List of file paths to be deleted
files_delete = [
    "input.sdf",
    "output.pdb",
    "script.pml",
]
"""
for file_to_delete in files_delete:
    try:
        os.remove(file_to_delete)
        print(f"{file_to_delete} has been deleted.")
    except FileNotFoundError:
        print(f"File not found: {file_to_delete}")
    except Exception as e:
        print(f"An error occurred while deleting {file_to_delete}: {e}")
"""
