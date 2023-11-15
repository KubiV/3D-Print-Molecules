import requests
import subprocess

# Prompt the user for the URL of the file they want to download
url = input("URL: PubChem - Download - 3D Conformer - SDF - Display (Copy Link): ")

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
