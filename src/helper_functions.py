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

def get_filename_without_extension(pdb_file_path):
    # Check if the given path is a file
    if os.path.isfile(pdb_file_path):
        # Split the file path into the directory and the file name with extension
        directory, full_filename = os.path.split(pdb_file_path)
        
        # Split the file name and extension
        filename, file_extension = os.path.splitext(full_filename)
        
        # Return the file name without extension
        return filename
    else:
        print(f"{pdb_file_path} is not a valid file path.")
        return pdb_file_path

def close_application(app_name, app_path):
    system_platform = platform.system()

    if system_platform == "Darwin":  # macOS
        subprocess.run(['pkill', '-f', app_name], shell=True)
        print("Quitting app")
    elif system_platform == "Windows":
        try:
            subprocess.run(['taskkill', '/f', '/im', os.path.basename(app_path)], check=True)
            print("Quitting app")
        except subprocess.CalledProcessError:
            print(f"Failed to quit {app_name}")
    else:
        print("Unsupported operating system")

def generate_model(input_str, input_type, path_to_pymol):

    quality = str(3)
    input_str = str(input_str)

    # Initialize with a default value
    temp_sdf_filename = None  
    temp_pdb_filename = None

    if input_type == "CID":
        url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/"+ input_str +"/record/SDF?record_type=3d&response_type=display"

        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Create a temporary file to store the SDF data
            with tempfile.NamedTemporaryFile(suffix=".sdf", delete=False) as temp_sdf_file:
                temp_sdf_filename = temp_sdf_file.name
                temp_sdf_file.write(response.content)
                temp_sdf_path = os.path.join(tempfile.gettempdir(), temp_sdf_filename)

            print(f"File saved as {temp_sdf_filename}")
        else:
            print(f"Failed to download the file. Status code: {response.status_code}")
            exit(1)

        # Check if the temporary SDF file exists
        if not os.path.exists(temp_sdf_path):
            print(f"Error: Temporary SDF file not found at {temp_sdf_filename}")
            exit(1)

        with tempfile.NamedTemporaryFile(suffix=".pdb", delete=False) as temp_pdb_file:
            temp_pdb_filename = temp_pdb_file.name
            temp_pdb_path = os.path.join(tempfile.gettempdir(), temp_pdb_filename)

        # Run the obabel command
        if os_type == "Darwin":
            print ("macOS - obabel")
            command = ["obabel", temp_sdf_path, "-O", temp_pdb_filename]
            subprocess.run(command, check=True)
            print("SDF to PDB conversion completed.")

        if os_type == "Linux": # needs to be finished!
            print ("Linux - obabel")
            command = ["obabel", temp_sdf_path, "-O", temp_pdb_filename]
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

        var1 = 'cmd.load(r"'+ temp_pdb_path +'")'
        var2 = 'cmd.set("sphere_quality", '+quality+')' # Lower the number is lower the quality - 3 is high - we use default sphere quality 3
        model_type = "sphere"
        save_all = None
        #TimeT = 5 # Sets the time delay needed for processing the 3D models

    if input_type == "PDB":
        temp_pdb_filename = None
        var1 = 'cmd.fetch("'+ input_str +'")'
        var2 = 'cmd.set("sphere_quality", '+quality+')' # Lower the number is lower the quality - 0 is suitable for really big mocules - we use default surface quality 1
        model_type = "surface"
        save_all = 'cmd.save("Molecule.stl", "all")'
        #TimeT = 30 # Sets the time delay needed for processing the 3D models
    
    if input_type == "File":
        if input_str.endswith(".pdb") or input_str.endswith(".pdb ") or input_str.endswith(".pdb'"):
            print("Own pdb file")
            var1 = 'cmd.load(r"'+ input_str +'")'
            var2 = 'cmd.set("sphere_quality", '+quality+')'#default sphere quality 3
            model_type = "sphere"
            save_all = None
            #TimeT = 5
    else:
        print("The input does not end with '.pdb'")

    with tempfile.NamedTemporaryFile(suffix=".pml", delete=False) as temp_pml_script:
        temp_pml_scriptname = temp_pml_script.name
        temp_pml_script_path = os.path.join(tempfile.gettempdir(), temp_pml_scriptname)

    def elem_stl_output(elem):
    # Create a list of commands to generate the STL for the specified element
        return [
            'cmd.hide("everything")',
            'cmd.select("'+elem+'_atoms", "elem '+elem+'")',
            'cmd.show("'+model_type+'", "'+elem+'_atoms")',
            'cmd.save("'+elem+'_output.stl", "'+elem+'_atoms")'
        ]

    # PyMOL script to execute a list of PyMOL commands
    lines_to_write = [
        var1,
        'cmd.set("sphere_scale", 0.7, "all")',
        'cmd.set("sphere_mode", 0)',
        'cmd.set("solvent_radius", 0.5)',
        'cmd.set("surface_quality", 1)',# default surface quality 1
        var2,

        *elem_stl_output("C"),
        *elem_stl_output("O"),
        *elem_stl_output("H"),
        *elem_stl_output("N"),
        *elem_stl_output("S"),
        *elem_stl_output("P"),

        'cmd.show("'+ model_type +'", "all")', # here model_type probably "spheres" (final s)
        save_all,
        # Add more lines as needed
    ]

    with open(temp_pml_scriptname, 'w') as file:
        for line in lines_to_write:
            if line is not None:
                file.write(str(line) + '\n')

    # Use the subprocess module to open the file with the specified application
    try:
        subprocess.Popen([path_to_pymol, temp_pml_script_path])
        print(f"Opening {temp_pml_scriptname} with {path_to_pymol}...")
    except FileNotFoundError:
        print(f"Error: The specified application '{path_to_pymol}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Define the directory where your files are located
    zip_name = get_filename_without_extension(input_str)
    source_folder = '.'
    zip_file_name = 'MultiBody_molecule_'+ zip_name +'.zip'
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

    file_name = input_str + ".cif"

    # List of file paths to be deleted
    files_delete = [
        temp_sdf_filename,
        temp_pdb_filename,
        temp_pml_scriptname,
        temp_dir_path,
        file_name,
    ]

    for file_to_delete in files_delete:
        try:
            os.remove(file_to_delete)
            print(f"{file_to_delete} has been deleted.")
        except FileNotFoundError:
            print(f"File not found: {file_to_delete}")
        except Exception as e:
            print(f"An error occurred while deleting {file_to_delete}: {e}")

    close_application("PyMOL", path_to_pymol)