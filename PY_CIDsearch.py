import tkinter as tk
from tkinter import messagebox
import requests

def format_formula(input):
    return input.replace(r'\d', "<sub>$&</sub>")

def fetch_pubchem_data():
    systematic_name = systematic_name_entry.get()

    pubchem_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{systematic_name}/cids/JSON"
    response = requests.get(pubchem_url)

    if response.status_code == 200:
        data = response.json()
        cid = data['IdentifierList']['CID'][0]

        pubchem_property_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/property/IUPACName,MolecularFormula,MolecularWeight,CanonicalSMILES,IsomericSMILES/JSON"
        response = requests.get(pubchem_property_url)

        if response.status_code == 200:
            data = response.json()
            iupac_name = data['PropertyTable']['Properties'][0]['IUPACName']
            trivial_name = data['PropertyTable']['Properties'][0]['MolecularFormula']
            cid = data['PropertyTable']['Properties'][0]['CID']
            image_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/PNG"

            # Zde můžete vytvářet řádek tabulky a provádět další manipulace s daty.

            messagebox.showinfo("Výsledek", f"IUPAC Název: {iupac_name}\nTriviální Název: {format_formula(trivial_name)}\nCID: {cid}")
        else:
            messagebox.showerror("Chyba", "Nepodařilo se načíst data z PubChem.")
    else:
        messagebox.showerror("Chyba", "Nepodařilo se najít systémový název.")

# Vytvoření základního okna
root = tk.Tk()
root.title("PubChem Data")

# Vytvoření vstupního pole a tlačítka
systematic_name_label = tk.Label(root, text="Zadej systémový název:")
systematic_name_label.pack()
systematic_name_entry = tk.Entry(root)
systematic_name_entry.pack()
fetch_button = tk.Button(root, text="Získat data z PubChem", command=fetch_pubchem_data)
fetch_button.pack()

root.mainloop()
