# 3D Print Molecules in Colour
 Python based program which makes easier to 3D print moleculs in muliticolour by automatical separation and export of atoms of each kind. 
 
![Program output and PYMOL output comparison](https://github.com/KubiV/3D-Print-Molecules/blob/main/Photos/Img4.png)

## Usage
![GUI Description](https://github.com/KubiV/3D-Print-Molecules/blob/main/Photos/version2_ui1_description.jpg)

 1. Eneter molecule name, CID number or PDB code into the text filed or select your own PDB or SDF file with atom coordinates.
 2. Fetch data using Enter key or apropriate button.
 3. Check folder for savin the output file.
 4. Choose molecule 3D representation for export (now only VDW - Van der Waals model - spheres).
 5. Check molecule information in the table.
 6. Set quality of the model (be aware of large file protection - program automatically sets low quality for molecules with high number of carbons).
 7. Generate the model!

![Example usage](https://github.com/KubiV/3D-Print-Molecules/blob/main/Photos/AppUsage.gif)

 5. Import to [PrusaSlicer](https://www.prusa3d.com/page/prusaslicer_424/) all STL files at once! And confirm "Multi part object" -> YES.
   ![Molecule for 3D printing in PrusaSlicer (left) and in PyMOL (right)](https://github.com/KubiV/3D-Print-Molecules/blob/main/Photos/Img2.png)

 6. The script only exports models for all present atoms separatelly and storers them into a ZIP file
 
 7.  Scale the molecules, set the colours for multicolour printing and slice the model.

 8.  3D print your molecule!

## To do
 - Auto import to slicer
 - export selection butttons (modify what exactly do you want to export, quality settings ...)
 - custom relative size of bond or atom
 - add a settings tab (manualy edit paths for PyMOL and Open Babel)

## Common problems

 - Not installed Python - see links
 - Default output folder selected incorrectly

## Pyinstaller

`pyinstaller --onefile --windowed --name "3D print Multi-color Molecules" --icon=graphical/default_icon.icns --debug=all src/main.py`

`pyinstaller -y --clean -F -w -i graphical/default_icon.icns --debug=all src/main.py`

## Links

 - Python for Windows - https://apps.microsoft.com/detail/python-3-12/9NCVDN91XZQP
 - PrusaSlicer - https://www.prusa3d.com/page/prusaslicer_424/

 - PubChem - https://pubchem.ncbi.nlm.nih.gov
 - RCSB PDB Protein Data Bank - https://www.rcsb.org
