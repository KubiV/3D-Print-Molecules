# 3D Print Molecules
 Python script which makes easier to 3D print moleculs in muliticolour by automatical separate export of atoms of each kind. 
 
![Molecule for 3D printing in PrusaSlicer (left) and in PyMOL (right)](https://github.com/KubiV/3D-Print-Molecules/blob/main/Photos/Img1.png)

## Usage

 1. Main script works in the directory, whete it is located.

[`PubChemCID_to_3Dprint.py`](https://github.com/KubiV/3D-Print-Molecules/blob/main/PubChemCID_to_3Dprint.py)

  2. Install Incentive [PyMOL](https://pymol.org/2/) program.

  3. Set the permissions and make sure that in the script the path to the executable file is correct (depends on the operating system).

    app_to_open_with = "executable_file"

**macOS**

    /Applications/PyMOL.app/Contents/MacOS/PyMOL

**Windows**
to be specified

**Ubuntu**
to be specified

 4. Execute the script and enter the [PubChem](https://pubchem.ncbi.nlm.nih.gov) CID number (Compound ID number) for the molecule. The .stl files are generated for C, O, H, N atoms separately and one for the molecule as a whole.

 5. Import to [PrusaSlicer](https://www.prusa3d.com/page/prusaslicer_424/) all STL files at once! And confirm "Multi part object" -> YES
   ![Molecule for 3D printing in PrusaSlicer (left) and in PyMOL (right)](https://github.com/KubiV/3D-Print-Molecules/blob/main/Photos/Img2.png)

 6.  Scale the molecules, set the colours for multicolour printing and slice the model.

 7.  3D print your molecule!

## Links

 - Incentive PyMOL - https://pymol.org/2/
 - PubChem - https://pubchem.ncbi.nlm.nih.gov
 - PrusaSlicer - https://www.prusa3d.com/page/prusaslicer_424/
