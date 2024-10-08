# pip install -r requirements.txt
import sys
import requests
from io import BytesIO
import re
import os
from pathlib import Path
import tempfile
import json
from MoleculeModelGenerating import ZIPmolecule, verify_value_json
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QFileDialog, QTableWidget, QTableWidgetItem, QSlider, QMessageBox, QCheckBox, QDialog, QScrollBar
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot

VERSION = "v2.1.1"

current_directory = os.path.dirname(__file__)

class WorkerThread(QThread):
    finished = pyqtSignal()
    data_fetched = pyqtSignal(str, str)

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.temp_pdb_path = None
        self.filename = None

    def determine_input_type(self, input_str):
        cas_pattern = re.compile(r"^\d{2,7}-\d{2}-\d$")
        if input_str.isdigit() or input_str.isalpha() or cas_pattern.match(input_str):
            return "CID"
        elif re.match(r'^[a-zA-Z0-9]{4}$', input_str):
            return "PDB"
        elif os.path.exists(input_str):
            return "File"
        else:
            return "Unknown"

    def fetch_data(self):
        input_str = self.main_window.systematic_name_entry.text()
        input_type = self.determine_input_type(input_str)
        print("Input String:", input_str, input_type)

        if input_type == "CID":
            self.fetch_pubchem_data()
        elif input_type == "PDB":
            self.fetch_pdb_data()
        elif input_type == "File":
            self.fetch_file_data()
            print("File input detected.")
        else:
            self.show_error("Error", "Input type not determined.")

    def fetch_file_data(self):
        file_path = self.main_window.systematic_name_entry.text()
        file_path_for_filename = Path(file_path)
        self.model_template = file_path
        print(self.model_template)

        self.set_image(os.path.abspath(os.path.join(current_directory, "../../graphical/icon_v1_file.jpg")))
        self.set_table_info(file_path, "Imported file", "")

        self.temp_pdb_path = file_path
        self.filename = file_path_for_filename.stem

    def fetch_pubchem_data(self):
        cid = None
        systematic_name = self.main_window.systematic_name_entry.text()
        all_digits = all(char.isdigit() for char in systematic_name)

        if not all_digits:
            pubchem_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{systematic_name}/cids/JSON"
            response = requests.get(pubchem_url)

            if response.status_code == 200:
                data = response.json()
                cid = data.get('IdentifierList', {}).get('CID', [])[0]
                if cid is None:
                    self.show_error("Error", "CID not found for the given name.")
                    return
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

            self.set_table_info(iupac_name, trivial_name, str(cid))
            self.download_and_display_image(image_url)
        else:
            self.show_error("Error", "Chyba")

        pubchem_coordinates_url_3d = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/{cid}/record/SDF?record_type=3d&response_type=display"

        # Send an HTTP GET request to the URL
        response_coordinates = requests.get(pubchem_coordinates_url_3d)
        
        # Check if the request was successful (status code 200)
        if response_coordinates.status_code == 200:
            # Create a temporary file to store the SDF data
            with tempfile.NamedTemporaryFile(suffix=".sdf", delete=False) as temp_sdf_file:
                temp_sdf_filename = temp_sdf_file.name
                temp_sdf_file.write(response_coordinates.content)
                self.temp_pdb_path = os.path.join(tempfile.gettempdir(), temp_sdf_filename)
                print(self.temp_pdb_path)
        elif response_coordinates.status_code == 404:
            # Second URL (2D coordinates)
            pubchem_coordinates_url_2d = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/{cid}/record/SDF?record_type=2d&response_type=display"

            # Try fetching from the second URL
            response_coordinates = requests.get(pubchem_coordinates_url_2d)

            # Check if this request was successful
            if response_coordinates.status_code == 200:
                # Create a temporary file to store the SDF data
                with tempfile.NamedTemporaryFile(suffix=".sdf", delete=False) as temp_sdf_file:
                    temp_sdf_filename = temp_sdf_file.name
                    temp_sdf_file.write(response_coordinates.content)
                    self.temp_pdb_path = os.path.join(tempfile.gettempdir(), temp_sdf_filename)
                    print(self.temp_pdb_path)
            else:
                # Handle other errors or no data found
                print(f"Failed to retrieve data: Status code {response_coordinates.status_code}")
        else:
            # Handle other errors for the first URL
            print(f"Failed to retrieve data: Status code {response_coordinates.status_code}")
            
        self.filename = "cid"+str(cid)
        self.data_fetched.emit(self.temp_pdb_path, self.filename)

    def fetch_pdb_data(self):
        pdb_code = self.main_window.systematic_name_entry.text()
        self.model_template = pdb_code
        print(self.model_template)
        self.fetch_pdb_data_from_api(pdb_code)

    def fetch_pdb_data_from_api(self, pdb_code):
        pdb = pdb_code.lower()
        graphql_url = "https://data.rcsb.org/graphql"
        image_url = f"https://cdn.rcsb.org/images/structures/{pdb}_assembly-1.jpeg"

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

            self.set_table_info(protein_name, str(molecular_mass)+" kDa", pdb)
            self.download_and_display_image(image_url) 

        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            print(f"An unexpected error occurred: {err}")

        pdb_coordinates_url = "https://files.rcsb.org/view/"+str(pdb)+".pdb"

        # Send an HTTP GET request to the URL
        response_coordinates = requests.get(pdb_coordinates_url)
            
        # Check if the request was successful (status code 200)
        if response_coordinates.status_code == 200:
            # Create a temporary file to store the SDF data
            with tempfile.NamedTemporaryFile(suffix=".pdb", delete=False) as temp_sdf_file:
                temp_sdf_filename = temp_sdf_file.name
                temp_sdf_file.write(response_coordinates.content)
                self.temp_pdb_path = os.path.join(tempfile.gettempdir(), temp_sdf_filename)
                print(self.temp_pdb_path)
        
        self.filename = pdb

    def download_and_display_image(self, image_url):
        response = requests.get(image_url)
        if response.status_code == 200:
            image_data = BytesIO(response.content)
            pixmap = QPixmap()
            pixmap.loadFromData(image_data.getvalue())
            pixmap = pixmap.scaled(self.main_window.image_label.width(), self.main_window.image_label.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.main_window.image_label.setPixmap(pixmap)
        else:
            self.show_error("Error", "Can not load the image") 

    def set_table_info(self, first_item, second_item, third_item):
        # Update the labels with the fetched data
        self.main_window.table.setItem(0, 1, QTableWidgetItem(first_item))
        self.main_window.table.setItem(1, 1, QTableWidgetItem(second_item))
        self.main_window.table.setItem(2, 1, QTableWidgetItem(third_item))
        self.main_window.table.viewport().update()

    def show_error(self, title, message):
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Critical)
        error_box.setWindowTitle(title)
        error_box.setText(message)
        error_box.exec_()  

    def run(self):
        print("Thread Working...")
        
        self.fetch_data()

        # Emit the signal with the fetched data
        self.data_fetched.emit(str(self.temp_pdb_path), str(self.filename))

        self.finished.emit()

class SettingsWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        
        # Assume the settings file is named settings.json and located at a specific path
        self.settings_file_path = os.path.join(os.path.dirname(__file__), 'Settings.json')
        
        # Load settings
        self.settings = self.load_settings()

        layout = QVBoxLayout()

        # Setting for large_c_chain_protection
        setting_layout = QHBoxLayout()
        self.label_large_c_chain = QLabel("Large C chain (100):")
        self.text_field_large_c_chain = QLineEdit(str(self.settings.get('large_c_chain_protection', '')))
        setting_layout.addWidget(self.label_large_c_chain)
        setting_layout.addStretch()
        setting_layout.addWidget(self.text_field_large_c_chain)
        layout.addLayout(setting_layout)

        # Setting for resolution_limit
        setting_layout = QHBoxLayout()
        self.label_resolution_limit = QLabel("Resolution limit when large C (8):")
        self.text_field_resolution_limit = QLineEdit(str(self.settings.get('resolution_limit', '')))
        setting_layout.addWidget(self.label_resolution_limit)
        setting_layout.addStretch()
        setting_layout.addWidget(self.text_field_resolution_limit)
        layout.addLayout(setting_layout)

        # Setting for radius_factor
        setting_layout = QHBoxLayout()
        self.label_radius_factor = QLabel("Radius multiplication factor (70):")
        self.text_field_radius_factor = QLineEdit(str(self.settings.get('radius_factor', '')))
        setting_layout.addWidget(self.label_radius_factor)
        setting_layout.addStretch()
        setting_layout.addWidget(self.text_field_radius_factor)
        layout.addLayout(setting_layout)

        # Change button
        self.change_button = QPushButton("Change Value")
        self.change_button.clicked.connect(self.change_variable)
        layout.addWidget(self.change_button)

        self.setLayout(layout)

    def load_settings(self):
        """Load settings from a JSON file."""
        try:
            with open(self.settings_file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}  # Return an empty dict if the file does not exist

    def change_variable(self):
        """Save the changed values back to the JSON file."""
        # Validate and update settings
        try:
            self.settings['large_c_chain_protection'] = int(self.text_field_large_c_chain.text())
            self.settings['resolution_limit'] = int(self.text_field_resolution_limit.text())
            self.settings['radius_factor'] = int(self.text_field_radius_factor.text())
        except ValueError:
            # Handle invalid input; show an error message if necessary
            return

        # Write updated settings back to the JSON file
        with open(self.settings_file_path, 'w') as file:
            json.dump(self.settings, file, indent=4)
            print("Variables changed")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_W and event.modifiers() & Qt.ControlModifier:
            self.close()
        else:
            super().keyPressEvent(event)

class MultiColouredMoleculesSTLGenerator(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MultiColouredMoleculesSTLGenerator, self).__init__(*args, **kwargs)
        self.setWindowTitle("3D Print Multi-Color Molecules - " + VERSION)
        self.directory_path = os.path.expanduser("~")  # Set a default directory
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(self)
        left_layout = QVBoxLayout()
        center_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # Widgets
        self.systematic_name_entry = QLineEdit()
        self.file_button = QPushButton("Choose File")
        self.directory_path = Path.home() / "Desktop"
        self.directory_label = QLabel(str(self.directory_path))
        self.directory_button = QPushButton("Choose Directory")
        self.choice_menu = QComboBox()
        self.table = QTableWidget(3, 2)
        self.image_label = QLabel()
        self.image_label.setFixedSize(200, 200)
        self.file_path = ""
        self.VDW = None
        self.BS = None
        self.quality_slider = QSlider(Qt.Horizontal)
        self.quality_label = QLabel("Quality: 50")
        self.generate_hydrogens_checkbox = QCheckBox("Generate Hydrogens")
        self.generate_hydrogens_checkbox.stateChanged.connect(self.update_generate_hydrogens)
        self.generate_hydrogens_checkbox.setCheckState(Qt.Checked)
        self.generate_model_button = QPushButton("Generate Model")
        self.default_image_path = os.path.abspath(os.path.join(current_directory, "../../graphical/icon_v1.jpg"))  # Replace with the actual path to your default image
        
        # Horizontal layout for input, file button and fetch button
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.systematic_name_entry)
        input_layout.addWidget(self.file_button)
        self.file_button.clicked.connect(self.choose_file)

        fetch_button = QPushButton("Fetch Data")
        #fetch_button.clicked.connect(self.fetch_data)
        fetch_button.clicked.connect(self.start_worker_thread1)
        input_layout.addWidget(fetch_button)

        center_layout.addLayout(input_layout)

        # Connect the returnPressed signal of the QLineEdit to the fetch_data slot
        self.systematic_name_entry.returnPressed.connect(self.start_worker_thread1)

        # Horizontal layout for directory selection
        directory_layout = QHBoxLayout()
        directory_layout.addWidget(self.directory_button)
        directory_layout.addWidget(self.directory_label)
        center_layout.addLayout(directory_layout)

        # Connect the directory button's clicked signal to the choose_directory slot
        self.directory_button.clicked.connect(self.choose_directory)

        # Combo box for choices
        self.choice_menu.addItems(["VDW", "BS - to be implemented"])
        center_layout.addWidget(self.choice_menu)

        # Table for labels
        table_image_layout = QHBoxLayout()
        self.setup_table()
        table_image_layout.addWidget(self.table)
        # Image label with the default image
        self.set_image(self.default_image_path)
        table_image_layout.addWidget(self.image_label)
        center_layout.addLayout(table_image_layout)

        # Slider for quality
        self.quality_slider.setMinimum(1)
        self.quality_slider.setMaximum(100)
        self.quality_slider.setValue(50)
        self.quality_slider.valueChanged.connect(self.update_quality)
        quality_layout = QHBoxLayout()
        quality_layout.addWidget(self.quality_label)
        quality_layout.addWidget(self.quality_slider)
        center_layout.addLayout(quality_layout)

        # Add the checkbox
        hydrogens_layout = QHBoxLayout()
        hydrogens_layout.addWidget(self.generate_hydrogens_checkbox)
            
       # Add settings button
        settings_button = QPushButton("Settings")
        settings_button.setFixedSize(100, 30)  # Adjust the width and height as needed
        settings_button.clicked.connect(self.open_settings)
        hydrogens_layout.addWidget(settings_button)

        center_layout.addLayout(hydrogens_layout)

        # Button to generate model
        center_layout.addWidget(self.generate_model_button)
        self.generate_model_button.clicked.connect(self.generate_model)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(center_layout)
        main_layout.addLayout(right_layout)

        central_widget.setLayout(main_layout)

        self.statusBar().showMessage("")

        self.show()

    def setup_table(self):
        self.table.setHorizontalHeaderLabels(["Property", "Value"])
        self.table.setItem(0, 0, QTableWidgetItem("Name"))
        self.table.setItem(1, 0, QTableWidgetItem("Description"))
        self.table.setItem(2, 0, QTableWidgetItem("ID Number"))
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)

    def start_worker_thread1(self):
        self.thread1 = WorkerThread(self)
        self.thread1.start()
        print("Worker thread 1 started")
        self.thread1.data_fetched.connect(self.update_model_data)

    @pyqtSlot(str, str)
    def update_model_data(self, temp_pdb_path, filename):
        #Update the model data when the thread finishes
        self.temp_pdb_path = temp_pdb_path
        self.filename = filename
        print(f"Received temp_pdb_path: {self.temp_pdb_path}")
        print(f"Received filename: {self.filename}")

    def choose_directory(self):
        self.directory_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        self.directory_label.setText(self.directory_path)
        
    def choose_file(self):
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")
        if self.file_path:
            self.systematic_name_entry.setText(self.file_path)

    def set_image(self, image_path):
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(pixmap)

    def update_quality(self, value):
        self.quality_label.setText(f"Quality: {value}")

    def update_generate_hydrogens(self, state):
        if state == Qt.Checked:
            self.hydrogens = True
        else:
            self.hydrogens = False
        print("Hydrogens: "+str(self.hydrogens))

    def generate_model(self):
        self.thread1.finished.connect(self.generate_model)
        print("Generating model...")
        
        # Set output path
        output_directory = self.directory_path if self.directory_path else "No directory chosen"
        os.chdir(output_directory)

        # Load data from the CSV file
        csv_filename = 'PubChemElements_all.csv'
        csv_path = os.path.abspath(__file__)
        csv_absolute_path = os.path.join(os.path.dirname(csv_path), csv_filename)

        # Load data from the PDB file
        if self.temp_pdb_path is None:
            print("Error: No PDB file path set.")
            return
        pdb_filename = self.temp_pdb_path  # Replace with the actual file name
        file_path = os.path.abspath(__file__)
        pdb_absolute_path = os.path.join(os.path.dirname(file_path), pdb_filename)

        # Atom model settings
        #radius_factor = 0.7
        radius_factor = verify_value_json("radius_factor", 70)/100
        print("Radius factor: "+str(radius_factor))
        model = self.choice_menu.currentText()
        resolution = self.quality_slider.value()
        filename = self.filename

        print("Model: "+str(model)+", Resolution: "+str(resolution))

        #make_molecule_stl_VanDerWaals(pdb_absolute_path, resolution, csv_absolute_path, radius_factor)
        ZIPmolecule(model, pdb_absolute_path, resolution, csv_absolute_path, radius_factor, filename, self.hydrogens)

    def open_settings(self):
        self.settings_window = SettingsWindow()
        self.settings_window.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MultiColouredMoleculesSTLGenerator()
    window.show()
    sys.exit(app.exec_())