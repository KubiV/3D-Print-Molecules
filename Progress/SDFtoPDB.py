import subprocess

sdf_file = "input.sdf"  # Replace with the path to your SDF file
pdb_file = "output.pdb"  # Desired name for the output PDB file

# Run the obabel command
command = ["obabel", sdf_file, "-O", pdb_file]
subprocess.run(command, check=True)

print("SDF to PDB conversion completed.")
