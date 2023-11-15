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
mol_filename = smiles + ".pdb"
obconversion.WriteFile(mol, mol_filename)