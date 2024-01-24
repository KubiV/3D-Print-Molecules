# Helper functions

import csv

def csv_to_python_structure(csv_file_path):
    """
    Read a CSV file and convert its contents to a Python data structure.

    Args:
    csv_file_path (str): The path to the CSV file.

    Returns:
    list: A list of dictionaries, where each dictionary represents a row in the CSV.
    """
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
        return data

def print_python_structure(data):
    """
    Print the Python data structure in a format that can be copied into a script.

    Args:
    data (list): The Python data structure to print.
    """
    print("data = [")
    for row in data:
        print("    {")
        for key, value in row.items():
            print(f"        '{key}': '{value}',")
        print("    },")
    print("]")

def save_python_structure(data, output_file_path):
    """
    Save the Python data structure to a file in a format that can be copied into a script.

    Args:
    data (list): The Python data structure to save.
    output_file_path (str): The path to the output file where the data will be saved.
    """
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write("data = [\n")
        for row in data:
            file.write("    {\n")
            for key, value in row.items():
                file.write(f"        '{key}': '{value}',\n")
            file.write("    },\n")
        file.write("]\n")

def main():
    csv_file_path = '/Users/jakubvavra/Documents/GitHub/3D-Print-Molecules/version2/src/PubChemElements_all.csv'  # Replace with your CSV file path
    data = csv_to_python_structure(csv_file_path)
    save_python_structure(data, "/Users/jakubvavra/Desktop/table.py")

if __name__ == "__main__":
    main()
