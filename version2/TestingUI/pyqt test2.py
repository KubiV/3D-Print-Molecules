import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap
from io import BytesIO
import re
import os

class ChemicalInfoApp(QWidget):
    def __init__(self):
        super().__init__()

        self.model_template = None

        self.systematic_name_entry = QLineEdit()
        self.result_labels = {
            "name": QLabel(""),
            "description": QLabel(""),
            "id_number": QLabel(""),
        }
        self.image_label = QLabel("")

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(self.systematic_name_entry)

        fetch_button = QPushButton("Fetch Data")
        fetch_button.clicked.connect(self.fetch_data)
        layout.addWidget(fetch_button)

        for label in self.result_labels.values():
            layout.addWidget(label)

        layout.addWidget(self.image_label)

        self.setLayout(layout)
        self.setWindowTitle("Chemical Information App")
        self.show()

    def determine_input_type(self, input_str):
        if input_str.isdigit() or input_str.isalpha():
            return "CID"
        elif re.match(r'^[a-zA-Z0-9]{4}$', input_str):
            return "PDB"
        elif os.path.exists(input_str):
            return "File"
        else:
            return "Unknown"

    def fetch_data(self):
        input_str = self.systematic_name_entry.text()
        input_type = self.determine_input_type(input_str)

        if input_type == "CID":
            self.fetch_pubchem_data()
        elif input_type == "PDB":
            self.fetch_pdb_data()
        elif input_type == "File":
            self.fetch_file_data()
            print("File input detected.")
        else:
            self.show_error("Error", "Nepodařilo se určit typ vstupu.")

    def fetch_file_data(self):
        file_path = self.systematic_name_entry.text()
        self.model_template = file_path
        print(self.model_template)

        # Update the labels in the second row with the fetched data
        self.result_labels["name"].setText(file_path)
        self.result_labels["description"].setText(" ")
        self.result_labels["id_number"].setText(" ")

    def fetch_pubchem_data(self):
        systematic_name = self.systematic_name_entry.text()
        all_digits = all(char.isdigit() for char in systematic_name)

        if not all_digits:
            pubchem_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{systematic_name}/cids/JSON"
            response = requests.get(pubchem_url)

            if response.status_code == 200:
                data = response.json()
                cid = data['IdentifierList']['CID'][0]
                self.model_template = cid
                print(self.model_template)
        else:
            cid = systematic_name

        pubchem_property_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/property/IUPACName,MolecularFormula,MolecularWeight,CanonicalSMILES,IsomericSMILES/JSON"
        response = requests.get(pubchem_property_url)

        if response.status_code == 200:
            data = response.json()
            iupac_name = data['PropertyTable']['Properties'][0]['IUPACName']
            trivial_name = data['PropertyTable']['Properties'][0]['MolecularFormula']
            cid = data['PropertyTable']['Properties'][0]['CID']
            image_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/PNG"

            # Update the labels with the fetched data
            self.result_labels["name"].setText(iupac_name)
            self.result_labels["description"].setText(trivial_name)
            self.result_labels["id_number"].setText(str(cid))

            # Download and display the image
            self.download_and_display_image(image_url)
        else:
            self.show_error("Error", "Chyba")

    def fetch_pdb_data(self):
        pdb_code = self.systematic_name_entry.text()
        self.model_template = pdb_code
        print(self.model_template)
        self.fetch_pdb_data_from_api(pdb_code)

    def fetch_pdb_data_from_api(self, pdb_code):
        pdb = pdb_code.lower()
        graphql_url = "https://data.rcsb.org/graphql"
        image_url = f"https://cdn.rcsb.org/images/structures/{pdb}_assembly-1.jpeg"
        self.download_and_display_image(image_url)

        graphql_query = """
        query ($id: String!) {
            entry(entry_id: $id) {
                struct {
                    title
                }
                rcsb_entry_info {
                    molecular_weight
                }
            }
        }
        """

        variables = {"id": pdb_code}

        headers = {
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(graphql_url, json={"query": graphql_query, "variables": variables}, headers=headers)
            response.raise_for_status()

            data = response.json()["data"]["entry"]
            protein_name = data["struct"]["title"]
            molecular_mass = data["rcsb_entry_info"]["molecular_weight"]

            # Update the labels with the fetched data
            self.result_labels["name"].setText(protein_name)
            self.result_labels["description"].setText(str(molecular_mass)+" kDa")
            self.result_labels["id_number"].setText(str(pdb_code))

        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            print(f"An unexpected error occurred: {err}")

    def download_and_display_image(self, image_url):
        response = requests.get(image_url)
        if response.status_code == 200:
            image_data = BytesIO(response.content)
            pixmap = QPixmap()
            pixmap.loadFromData(image_data.getvalue())

            # Display the image
            self.image_label.setPixmap(pixmap)
        else:
            self.show_error("Error", "Nepodařilo se načíst obrázek.")

    def show_error(self, title, message):
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Critical)
        error_box.setWindowTitle(title)
        error_box.setText(message)
        error_box.exec_()


if __name__ == '__main__':
    app = QApplication([])
    chem_info_app = ChemicalInfoApp()
    app.exec_()
