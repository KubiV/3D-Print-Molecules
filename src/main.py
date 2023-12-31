"""
Multi-coloured Molecules STL Generator

Version: 1.0.0
Description: Generate a one file including separate atoms to 3D print molecule in color

Author: Jakub Vávra
Email: j.vavra@sh.cvut.cz
License: CC0 1.0 DEED
GitHub Repository: https://github.com/KubiV/3D-Print-Molecules
"""

import subprocess
import os
import re
import importlib
from helper_functions import generate_model

modules_to_install = ["tkinter", "Pillow", "io", "requests", "zipfile", "shutil", "tempfile", "platform", "webbrowser"]

for module in modules_to_install:
    try:
        importlib.import_module(module)
        print(f"{module} is already installed.")
    except ImportError:
        try:
            subprocess.check_call(['pip3', 'install', module])
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {module}: {e}")

import tkinter as tk
from tkinter import messagebox, Label
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO
import requests
import zipfile
import shutil
import time
import tempfile
import platform
import webbrowser

def browse_folder():
    global folder_path
    # Set the initial directory to the Downloads folder
    initial_dir = os.path.expanduser("~/Downloads")
    folder_path = filedialog.askdirectory(initialdir=initial_dir)
    if folder_path:
        # Update your GUI or store the selected folder_path as needed
        os.chdir(folder_path)
        selected_folder_label.config(text="Složka pro export: " + folder_path)
        print("Destination directory:" + folder_path)

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDB soubory", "*.pdb")])
    if file_path:
        systematic_name_entry.delete(0, tk.END)  # Clear the current entry
        systematic_name_entry.insert(0, file_path)  # Insert the selected file path
        fetch_data()  # Call fetch_data with the selected file path   

def open_link(url):
    webbrowser.open(url)

def show_custom_message_box():
    custom_box = tk.Toplevel()
    custom_box.title("Install missing programs")
    message1 = "Please download the Incentive PyMOL app"
    message_label = tk.Label(custom_box, text=message1)
    message_label.pack()
    open_button = tk.Button(custom_box, text="Open Web Link to PyMOL", command=lambda:open_link("https://pymol.org/2/"))
    open_button.pack()
    message2 = "Please also download Open Babel"
    message_label = tk.Label(custom_box, text=message2)
    message_label.pack()
    open_button2 = tk.Button(custom_box, text="Open Web Link to Open Babel macOS", command=lambda:open_link("https://formulae.brew.sh/formula/open-babel"))
    open_button3 = tk.Button(custom_box, text="Open Web Link to Open Babel Windows", command=lambda:open_link("https://github.com/openbabel/openbabel/releases"))
    open_button2.pack()
    open_button3.pack()

def update_value(value):
    # Update the variable with the selected value
    selected_value.set(value)

def update_label():
    # Get the selected value from the DoubleVar
    current_value = selected_value.get()

    # Round the selected value to one decimal place
    rounded_value = round(current_value, 1)

    # Update the label text
    value_label.config(text=f"Kvalita: {rounded_value}")

    # Print the rounded value
    print("Rounded Value:", rounded_value)

    # Store the rounded value in the variable
    rounded_value_var.set(rounded_value)

def determine_input_type(input_str):
    if input_str.isdigit() or input_str.isalpha():
        return "CID"
    elif re.match(r'^[a-zA-Z0-9]{4}$', input_str):
        return "PDB"
    elif os.path.exists(input_str):
        return "File"
    else:
        return "Unknown"
    
model_template = None 

def fetch_data():
    input_str = systematic_name_entry.get()
    input_type = determine_input_type(input_str)

    if input_type == "CID":
        fetch_pubchem_data()
    elif input_type == "PDB":
        fetch_pdb_data()
    elif input_type == "File":
        fetch_file_data()
        print("File input detected.")
    else:
        messagebox.showerror("Chyba", "Nepodařilo se určit typ vstupu.")

def fetch_file_data():
    file_path = systematic_name_entry.get()
    global model_template
    model_template = file_path
    print(model_template)

    # Add labels for the columns in the first row
    iupac_label1 = Label(table_frame, text="Soubor", borderwidth=1, relief="solid", width=20)
    iupac_label1.grid(row=0, column=0)

    # Update the labels in the second row with the fetched data
    iupac_label2.config(text= str(file_path))   

def fetch_pubchem_data():
    systematic_name = systematic_name_entry.get()
    global model_template
    all_digits = True

    for char in systematic_name:
        if not char.isdigit():
            all_digits = False
            break

    if all_digits == False:

        pubchem_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{systematic_name}/cids/JSON"
        response = requests.get(pubchem_url)

        if response.status_code == 200:
            data = response.json()
            cid = data['IdentifierList']['CID'][0]
            model_template = cid
            print(model_template)
            #print(cid)     
        
    if all_digits == True:
        cid = systematic_name

    pubchem_property_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/property/IUPACName,MolecularFormula,MolecularWeight,CanonicalSMILES,IsomericSMILES/JSON"
    response = requests.get(pubchem_property_url)

    if response.status_code == 200:

        # Add labels for the columns in the first row
        iupac_label1 = Label(table_frame, text="IUPAC Název", borderwidth=1, relief="solid", width=20)
        iupac_label1.grid(row=0, column=0)

        trivial_label1 = Label(table_frame, text="Vzorec", borderwidth=1, relief="solid", width=20)
        trivial_label1.grid(row=0, column=1)

        cid_label1 = Label(table_frame, text="CID", borderwidth=1, relief="solid", width=20)
        cid_label1.grid(row=0, column=2)

        cid_label1 = Label(table_frame, text="Schéma", borderwidth=1, relief="solid", width=20)
        cid_label1.grid(row=0, column=3)

        data = response.json()
        iupac_name = data['PropertyTable']['Properties'][0]['IUPACName']
        trivial_name = data['PropertyTable']['Properties'][0]['MolecularFormula']
        cid = data['PropertyTable']['Properties'][0]['CID']
        image_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/PNG"

        # Download and display the image in the Tkinter window
        download_and_display_image(image_url)

        # Update the labels in the second row with the fetched data
        iupac_label2.config(text=str(iupac_name))
        trivial_label2.config(text=str(trivial_name))
        cid_label2.config(text=str(cid))
        #image_label2.config(text=str(image_url))
            
    else:
        messagebox.showerror("Chyba")    

def fetch_pdb_data():
    global model_template
    pdb_code = systematic_name_entry.get()
    model_template = pdb_code
    print(model_template)
    fetch_pdb_data_from_api(pdb_code)

def fetch_pdb_data_from_api(pdb_code):
    pdb = pdb_code.lower()
    graphql_url = "https://data.rcsb.org/graphql"  # Updated base URL
    image_url = f"https://cdn.rcsb.org/images/structures/{pdb}_assembly-1.jpeg"
    download_and_display_image(image_url)
    graphql_query = """
    query ($id: String!) {
        entry(entry_id: $id) {
            struct {
                title
            }
            rcsb_entry_info {
                molecular_weight
            }
            # Add any other fields you need
        }
    }
    """

    variables = {"id": pdb_code}

    headers = {
        "Content-Type": "application/json",
        # Add any other headers if needed
    }

    try:
        response = requests.post(graphql_url, json={"query": graphql_query, "variables": variables}, headers=headers)
        response.raise_for_status()

        data = response.json()["data"]["entry"]
        protein_name = data["struct"]["title"]
        molecular_mass = data["rcsb_entry_info"]["molecular_weight"]
        # Add any other relevant properties you need

        # Add labels for the columns in the first row
        iupac_label1 = Label(table_frame, text="Název", borderwidth=1, relief="solid", width=20)
        iupac_label1.grid(row=0, column=0)

        trivial_label1 = Label(table_frame, text="Molekulová hmotnost", borderwidth=1, relief="solid", width=20)
        trivial_label1.grid(row=0, column=1)

        cid_label1 = Label(table_frame, text="PDB", borderwidth=1, relief="solid", width=20)
        cid_label1.grid(row=0, column=2)

        cid_label1 = Label(table_frame, text="Schéma", borderwidth=1, relief="solid", width=20)
        cid_label1.grid(row=0, column=3)

        # Update the labels in the second row with the fetched data
        iupac_label2.config(text= str(protein_name))
        trivial_label2.config(text=str(molecular_mass)+ " Da")
        cid_label2.config(text=str(pdb_code))    

    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"An unexpected error occurred: {err}")


def download_and_display_image(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        image_data = BytesIO(response.content)
        image = Image.open(image_data)
        image = image.resize((100, 100))  # Resize the image as needed
        image = ImageTk.PhotoImage(image)

        # Create a label for the fourth column and display the image
        image_label = Label(table_frame, image=image, borderwidth=1, relief="solid")
        image_label.image = image  # Keep a reference to the image to prevent it from being garbage collected
        image_label.grid(row=1, column=3)  # Place it in the second row
    else:
        messagebox.showerror("Chyba", "Nepodařilo se načíst obrázek.")

# Create the main Tkinter window
root = tk.Tk()
root.title("3D print Multi-color Molecules")

# OS selection
os_type = platform.system()

if os_type == "Darwin":
    path_to_pymol = os.path.normpath("/Applications/PyMOL.app/Contents/MacOS/PyMOL")
    print ("macOS - PyMOL")

if os_type == "Linux": # needs to be finished!
    path_to_pymol = ""
    print ("Linux - PyMOL")

if os_type == "Windows":
    path_to_pymol = r"C:\Users\Admin\AppData\Local\Schrodinger\PyMOL2\PyMOLWin.exe"
    print("Windows - PyMOL")

if os.path.exists(path_to_pymol):
    print("PyMOL exists at the specified path.")
else:
    show_custom_message_box()
    print("PyMOL does not exist at the specified path.")

# Create widgets for input and data fetching
systematic_name_label = tk.Label(root, text="Zadej systémový název:")
systematic_name_label.pack()
systematic_name_entry = tk.Entry(root)
systematic_name_entry.pack()

# Create a button for browsing files
browse_file_button = tk.Button(root, text="Procházej soubory", command=browse_file)
browse_file_button.pack()

def fetch_data_on_enter(event):
    fetch_data()

systematic_name_entry.bind('<Return>', fetch_data_on_enter)  # Bind Enter key to fetch_data function

fetch_button = tk.Button(root, text="Získat data", command=fetch_data)
fetch_button.pack()

# Create a table with two rows and four columns
table_frame = tk.Frame(root)
table_frame.pack()

# Add labels for the columns in the second row
iupac_label2 = Label(table_frame, text="", borderwidth=0, relief="solid", width=20)
iupac_label2.grid(row=1, column=0)

trivial_label2 = Label(table_frame, text="", borderwidth=0, relief="solid", width=20)
trivial_label2.grid(row=1, column=1)

cid_label2 = Label(table_frame, text="", borderwidth=0, relief="solid", width=20)
cid_label2.grid(row=1, column=2)

image_label2 = Label(table_frame, text="", borderwidth=0, relief="solid", width=20)
image_label2.grid(row=1, column=3)

# File browsing
downloads_path = os.path.expanduser("~/Downloads")
try:
    os.chdir(downloads_path)
    print("Current working directory:", os.getcwd())
except FileNotFoundError:
    print("Downloads directory not found.")
except Exception as e:
    print("An error occurred:", str(e))

browse_button = tk.Button(root, text="Procházej složky", command=browse_folder)
browse_button.pack(pady=10)

selected_folder_label = tk.Label(root, text="Složka pro export: " + downloads_path)
selected_folder_label.pack()

# Quality picker
selected_value = tk.DoubleVar()

value_scale = ttk.Scale(root, from_=0, to=5, orient=tk.HORIZONTAL, length=200, variable=selected_value, command=update_value)
value_scale.pack(padx=20, pady=20)

value_label = ttk.Label(root, text="Kvalita: 0.0")
value_label.pack()

rounded_value_var = tk.DoubleVar()

update_button = ttk.Button(root, text="Ulož kvalitu (nefunguje)", command=update_label)
update_button.pack(pady=10)

if determine_input_type(systematic_name_entry.get()) == "CID":
    rounded_value_var.set(3)

# Button for generating the model
generate_model_button = tk.Button(root, text="Generuj model", command=lambda:generate_model(model_template, determine_input_type(systematic_name_entry.get()), path_to_pymol))
generate_model_button.pack()


# Start the Tkinter main loop
root.mainloop()
