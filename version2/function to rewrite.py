import subprocess
import os
import re
import importlib
from PIL import Image, ImageTk
from io import BytesIO
import requests
import zipfile
import shutil
import time
import tempfile
import platform
import webbrowser

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
