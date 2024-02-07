import subprocess

# Replace 'MLC.zip' with the actual file you want to open in PrusaSlicer.
file_to_open = 'MLC.zip'

program = "PrusaSlicer"

try:
    # Execute the shell command to open the file with PrusaSlicer.
    subprocess.Popen(['open', '-a', program, file_to_open])
except Exception as e:
    print(f"Error executing the shell command: {str(e)}")
