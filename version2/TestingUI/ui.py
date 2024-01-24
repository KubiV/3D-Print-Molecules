import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QComboBox, QFileDialog, QTableWidget, QTableWidgetItem, QSlider, QGridLayout
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class ChemicalInfoApp(QWidget):
    def __init__(self):
        super().__init__()

        self.systematic_name_entry = QLineEdit()
        self.file_button = QPushButton("Choose File")
        self.directory_label = QLabel("No directory chosen")
        self.directory_button = QPushButton("Choose Directory")
        self.choice_menu = QComboBox()
        self.table = QTableWidget(3, 2)
        self.image_label = QLabel()
        self.image_label.setFixedSize(200, 200)  # Set the fixed size for the image label
        self.directory_path = ""
        self.file_path = ""
        self.VDR = None
        self.BS = None
        self.quality_slider = QSlider(Qt.Horizontal)
        self.quality_label = QLabel("Quality: 50")
        self.generate_model_button = QPushButton("Generate Model")
        self.default_image_path = "/Users/jakubvavra/Documents/GitHub/3D-Print-Molecules/graphical/icon_v1.jpg"  # Replace with the actual path to your default image

        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        left_layout = QVBoxLayout()
        center_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # Horizontal layout for input, file button and fetch button
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.systematic_name_entry)
        input_layout.addWidget(self.file_button)
        self.file_button.clicked.connect(self.choose_file)

        fetch_button = QPushButton("Fetch Data")
        fetch_button.clicked.connect(self.fetch_data)
        input_layout.addWidget(fetch_button)

        center_layout.addLayout(input_layout)

        # Connect the returnPressed signal of the QLineEdit to the fetch_data slot
        self.systematic_name_entry.returnPressed.connect(self.fetch_data)

        # Horizontal layout for directory selection
        directory_layout = QHBoxLayout()
        directory_layout.addWidget(self.directory_button)
        directory_layout.addWidget(self.directory_label)
        center_layout.addLayout(directory_layout)

        # Connect the directory button's clicked signal to the choose_directory slot
        self.directory_button.clicked.connect(self.choose_directory)

        # Combo box for choices
        self.choice_menu.addItems(["VDR", "BS"])
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

        # Button to generate model
        center_layout.addWidget(self.generate_model_button)
        self.generate_model_button.clicked.connect(self.generate_model)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(center_layout)
        main_layout.addLayout(right_layout)

        self.setWindowTitle("Chemical Information App")
        self.show()

    def setup_table(self):
        self.table.setHorizontalHeaderLabels(["Property", "Value"])
        self.table.setItem(0, 0, QTableWidgetItem("Name"))
        self.table.setItem(1, 0, QTableWidgetItem("Description"))
        self.table.setItem(2, 0, QTableWidgetItem("ID Number"))
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)

    def fetch_data(self):
        # Fetch data logic goes here
        # For now, just printing the text input
        input_str = self.systematic_name_entry.text()
        print("Input String:", input_str)

        # Update the image label with a new image upon fetching data
        # Replace 'path/to/fetched_image.png' with the actual path to the fetched image
        self.set_image("path/to/fetched_image.png")

        # Update table with dummy data for demonstration
        self.table.setItem(0, 1, QTableWidgetItem(input_str))
        self.table.setItem(1, 1, QTableWidgetItem("Dummy description"))
        self.table.setItem(2, 1, QTableWidgetItem("12345"))

    def choose_directory(self):
        self.directory_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        self.directory_label.setText(self.directory_path if self.directory_path else "No directory chosen")

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

    def generate_model(self):
        # Placeholder for generate model logic
        print("Generating model...")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    chem_info_app = ChemicalInfoApp()
    sys.exit(app.exec_())
