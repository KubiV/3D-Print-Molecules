# 3D Print Molecules
 Python script which makes easier to 3D print moleculs in muliticolour by automatical separate export of atoms of each kind. 
 
![Molecule for 3D printing in PrusaSlicer (left) and in PyMOL (right)](https://github.com/KubiV/3D-Print-Molecules/blob/main/Photos/Img1.png)

## Usage

 1. Main script works in the directory, which is set in the terminal (first of all don't forget to execute `cd Folder/desired_folder` ).

[`MultiMaterial_STL_Molecules.py`](https://github.com/KubiV/3D-Print-Molecules/blob/main/MultiMaterial_STL_Molecules.py)

  2. Install Incentive [PyMOL](https://pymol.org/2/) program and [Open Babel](http://openbabel.org/wiki/Main_Page)

  3. Set the permissions and make sure that in the script the path to the executable file is correct (depends on the operating system).

    app_to_open_with = "executable_file"

**macOS**

    /Applications/PyMOL.app/Contents/MacOS/PyMOL

**Windows**
to be specified

**Ubuntu**
to be specified

 4. Execute the script and enter the [PubChem](https://pubchem.ncbi.nlm.nih.gov) CID number (Compound ID number) for the molecule. The .stl files are generated for C, O, H, N atoms separately and one for the molecule as a whole.

 5. Import to [PrusaSlicer](https://www.prusa3d.com/page/prusaslicer_424/) all STL files at once! And confirm "Multi part object" -> YES.
   ![Molecule for 3D printing in PrusaSlicer (left) and in PyMOL (right)](https://github.com/KubiV/3D-Print-Molecules/blob/main/Photos/Img2.png)

 6. The script only exports models of C, O, H, N so there is chance that your molecule contain extra atoms or does not contain exported atoms - so keep in mind empty stl files or not exported atoms in these cases.
 
 7.  Scale the molecules, set the colours for multicolour printing and slice the model.

 8.  3D print your molecule!

## To do
 - Auto import to slicer
 - export selection butttons (modify what exactly do you want to export, quality settings ...)
 - custom relative size of bond or atom
 - add a settings tab (manualy edit paths for PyMOL and Open Babel)
 - ✅one app using pyinstaller
 - ✅ direct import of .pdb
 - ✅ auto quit PyMOL
 - ✅ GUI or more intuitive text UI
 - ✅ Integrated CID/PDB database view and number search via PubChem PUG REST and RCSB PDB Data API
 - ✅ Optimize intermediate files saving (tempfile or io.BytesIO module)
 - ✅ Auto-install dependencies (python modules, openBabel, PyMOL, slicer) or wizzard

## Common problems

 - Not installed Python - see links
 - Not installed Pillow module - run `pip3 install Pillow` in python
 - Not installed Incentive PyMOL (NOT the opensource version, the Incentive isneeded) - see links
 - Not installed Open Babel - see links

## Links

 - Python for Windows - https://apps.microsoft.com/detail/python-3-12/9NCVDN91XZQP
 - Incentive PyMOL - https://pymol.org/2/
 - Open Babel - http://openbabel.org/wiki/Main_Page
 - Open Babel for Windows - https://github.com/openbabel/openbabel/releases
 - Open Babel for macOS - https://formulae.brew.sh/formula/open-babel
 - PrusaSlicer - https://www.prusa3d.com/page/prusaslicer_424/

 - PubChem - https://pubchem.ncbi.nlm.nih.gov
 - RCSB PDB Protein Data Bank - https://www.rcsb.org
