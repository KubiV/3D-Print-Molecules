import subprocess

def open_in_slicer():

    # Specify the path to the file you want to open
    file_path = "/Users/jakubvavra/Desktop/MLC.zip"

    # Specify the application you want to use to open the file
    application_name = "PrusaSlicer.app"

    # Use the 'open' command with the specified application
    subprocess.call(["open", "-a", application_name, file_path])

open_in_slicer()