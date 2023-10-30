import subprocess
import os

modules_to_install = ["tkinter", "PIL"]

for module in modules_to_install:
    try:
        subprocess.check_call(['pip3', 'install', module])
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {module}: {e}")

import tkinter as tk
from tkinter import messagebox, Label
from PIL import Image, ImageTk
import requests
from io import BytesIO

def PyMOL_downloadpage():
    import webbrowser
    webbrowser.open("https://pymol.org/2/")

def show_custom_message_box():
    custom_box = tk.Toplevel()
    custom_box.title("Install PyMOL")
    message = "Please download the Incentive PyMOL app"
    message_label = tk.Label(custom_box, text=message)
    message_label.pack()
    open_button = tk.Button(custom_box, text="Open Web Link to PyMOL", command=PyMOL_downloadpage)
    open_button.pack()

def fetch_pubchem_data():
    systematic_name = systematic_name_entry.get()

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
            print(cid)
        
    if all_digits == True:
        cid = systematic_name

    pubchem_property_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/property/IUPACName,MolecularFormula,MolecularWeight,CanonicalSMILES,IsomericSMILES/JSON"
    response = requests.get(pubchem_property_url)

    if response.status_code == 200:
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
root.title("PubChem Data")

# Chech if PyMOL installed
path_to_pymol = "/Applications/PyMOL.app/Contents/MacOS/PyMOL"

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
fetch_button = tk.Button(root, text="Získat data z PubChem", command=fetch_pubchem_data)
fetch_button.pack()

# Create a table with two rows and four columns
table_frame = tk.Frame(root)
table_frame.pack()

# Add labels for the columns in the first row
iupac_label1 = Label(table_frame, text="IUPAC Název", borderwidth=1, relief="solid", width=20)
iupac_label1.grid(row=0, column=0)

trivial_label1 = Label(table_frame, text="Vzorec", borderwidth=1, relief="solid", width=20)
trivial_label1.grid(row=0, column=1)

cid_label1 = Label(table_frame, text="CID", borderwidth=1, relief="solid", width=20)
cid_label1.grid(row=0, column=2)

cid_label1 = Label(table_frame, text="Schéma", borderwidth=1, relief="solid", width=20)
cid_label1.grid(row=0, column=3)

# Add labels for the columns in the second row
iupac_label2 = Label(table_frame, text="", borderwidth=0, relief="solid", width=20)
iupac_label2.grid(row=1, column=0)

trivial_label2 = Label(table_frame, text="", borderwidth=0, relief="solid", width=20)
trivial_label2.grid(row=1, column=1)

cid_label2 = Label(table_frame, text="", borderwidth=0, relief="solid", width=20)
cid_label2.grid(row=1, column=2)

image_label2 = Label(table_frame, text="", borderwidth=0, relief="solid", width=20)
image_label2.grid(row=1, column=3)

# Start the Tkinter main loop
root.mainloop()
