import requests

def fetch_pdb_data():
    systematic_name = input("Nazev:")#systematic_name_entry.get()

    all_digits = True

    for char in systematic_name:
        if not char.isdigit():
            all_digits = False
            break

    if all_digits == False:

        pdb_url = f"https://search.rcsb.org/rcsbsearch/v2/query?json={{\"query\":{{\"type\":\"terminal\",\"service\":\"text\",\"parameters\":{{\"operator\":\"exact_match\",\"value\":\"{systematic_name}\",\"attribute\":\"rcsb_entity_source_organism.taxonomy_lineage.name\"}}}},\"return_type\":\"entry\"}}"
        response = requests.get(pdb_url)

        if response.status_code == 200:
            data = response.json()
            pdb_code = data['result_set'][0]['identifier']
            print(pdb_code)
        
    if all_digits == True:
        pdb_code = systematic_name

    pdb_property_url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_code}"
    response = requests.get(pdb_property_url)

    if response.status_code == 200:
        data = response.json()
        name = data['struct']['title']
        molecular_mass = data['pdbx_vrpt_summary']['pdbx_formula_weight']
        print(name, molecular_mass)
            
    else:
        messagebox.showerror("Chyba")

fetch_pdb_data()
print(name, molecular_mass)