import pymol
from pymol import cmd
from openbabel import openbabel as ob

smiles = "CN1[C@@H]2CC[C@H]1CC(C2)OC(=O)C(CO)C3=CC=CC=C3"  # Replace with your desired SMILES notation

# Create an Open Babel molecule object
mol = ob.OBMol()

# Read the SMILES string and add it to the molecule object
obconversion = ob.OBConversion()
obconversion.SetInAndOutFormats("smi", "mol")
obconversion.ReadString(mol, smiles)

# Convert the molecule to 3D coordinates
forcefield = ob.OBForceField.FindForceField("MMFF94")
forcefield.Setup(mol)
forcefield.SteepestDescent(500)  # You can adjust the number of steps

# Save the molecule as a PDB file
obconversion.SetInAndOutFormats("mol", "pdb")
mol_filename = "molecule.pdb"
obconversion.WriteFile(mol, mol_filename)

cmd.load("molecule.pdb")

cmd.set("sphere_scale", 0.7, "all")
cmd.set("sphere_mode", 0)
cmd.set("sphere_quality", 3)

cmd.select("carbon_atoms", "elem C")  # Select carbon atoms
cmd.show("spheres", "carbon_atoms")  # Display carbon atoms as sticks (you can use other representations as well)

cmd.hide("everything")

cmd.select("hydrogen_atoms", "elem H")  # Select hydrogen atoms
cmd.show("spheres", "hydrogen_atoms")  # Display hydrogen atoms as sticks (you can use other representations as well)

cmd.hide("everything")

cmd.select("nitrogen_atoms", "elem N")  # Select nitrogen atoms
cmd.show("spheres", "nitrogen_atoms")  # Display nitrogen atoms as sticks (you can use other representations as well)

cmd.hide("everything")

cmd.select("oxygen_atoms", "elem O")  # Select oxygen atoms
cmd.show("spheres", "oxygen_atoms")   # Display oxygen atoms as sticks (you can use other representations as well)

cmd.save("output.stl", "carbon_atoms")
cmd.save("output.stl", "all")