import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap

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

        # Horizontal layout for input and button
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.systematic_name_entry)

        fetch_button = QPushButton("Fetch Data")
        fetch_button.clicked.connect(self.fetch_data)
        input_layout.addWidget(fetch_button)

        layout.addLayout(input_layout)

        for label in self.result_labels.values():
            layout.addWidget(label)

        layout.addWidget(self.image_label)

        self.setLayout(layout)
        self.setWindowTitle("Chemical Information App")
        self.show()

        # Connect the returnPressed signal of the QLineEdit to the fetch_data slot
        self.systematic_name_entry.returnPressed.connect(self.fetch_data)

    def fetch_data(self):
        input_str = self.systematic_name_entry.text()
        print(input_str)

if __name__ == '__main__':
    app = QApplication([])
    chem_info_app = ChemicalInfoApp()
    app.exec_()
