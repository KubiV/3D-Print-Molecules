import tkinter as tk
import requests
from PIL import ImageTk, Image
from io import BytesIO
from prettytable import PrettyTable

def search():
    query = search_box.get()
    url = f"https://data.rcsb.org/rest/v1/core/entry/{query}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        pdb_code = data.get("rcsb_id", "N/A")

        # Check if the key exists before accessing it
        identifiers = data.get("rcsb_polymer_entity_container_identifiers", {})
        molecular_mass = identifiers.get("entity_molecular_weight", "N/A")
        protein_name = identifiers.get("entry_name", "N/A")

        image_url = f"https://cdn.rcsb.org/images/structures/{pdb_code}_assembly-1.jpeg"
        response = requests.get(image_url)

        try:
            img = Image.open(BytesIO(response.content))
            img = img.resize((100, 100), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)

            table = PrettyTable(["PDB Code", "Molecular Mass", "Protein Name", "Thumbnail"])
            table.add_row([pdb_code, molecular_mass, protein_name, img])

            table_field = tk.Label(window, text=table)
            table_field.pack()

        except Image.UnidentifiedImageError:
            error_field = tk.Label(window, text="Error: Unable to identify image file")
            error_field.pack()

    else:
        error_field = tk.Label(window, text="Error: Invalid PDB code")
        error_field.pack()

# Rest of your code remains unchanged


window = tk.Tk()
window.title("RCSB PDB Data API Search")
window.geometry("500x500")

search_label = tk.Label(window, text="Enter PDB code:")
search_label.pack()

search_box = tk.Entry(window)
search_box.pack()

search_button = tk.Button(window, text="Search", command=search)
search_button.pack()

window.mainloop()
