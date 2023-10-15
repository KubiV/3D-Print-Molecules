import pymol

# Spuštění instance PyMOLu
pymol.launch()

# Načtení molekuly
pymol.cmd.load("your_molecule.pdb", "molecule_name")

# Změna zobrazení na sticks
pymol.cmd.show("sticks", "molecule_name")

# Změna barvy na červenou
pymol.cmd.color("red", "molecule_name")


# generally I don't print hydrogens and solvent molecules
hide everything
remove hydrogens
remove solvent
# sphere settings
show spheres, SELN # replace SELN with your chosen selection name or "all"
set sphere_scale, 0.7, (all)
# set spheres to render triangles, so that viewing represents the exported file
set sphere_mode, 0
set sphere_quality, 3
# cartoon settings
show cartoon, SELN
set cartoon_oval_width, 0.7
set cartoon_sampling, 10
set cartoon_oval_quality, 20
# licorice settings
show licorice, SELN
set stick_radius, 1
set stick_ball, 1
set stick_quality, 20
# surface settings
show surface, SELN
set surface_quality, 1
set solvent_radius, 0.5



show
show reprentation [,object]
show reprentation [,(selection)]
show (selection)



import pymol
from pymol import cmd
import pybel

smiles = "CCO"  # Replace with your desired SMILES notation

# Convert SMILES to MOL2 format using Pybel
mol = next(pybel.readstring("smi", smiles))
mol.addh()
mol.make3D()
mol.write("mol2", "molecule.mol2")

cmd.load("molecule.mol2")

cmd.set("sphere_scale", 0.7, "all")
cmd.set("sphere_mode", 0)
cmd.set("sphere_quality", 3)

cmd.select("carbon_atoms", "elem C")  # Select carbon atoms
cmd.show("spheres", "carbon_atoms")  # Display carbon atoms as sticks (you can use other representations as well)

cmd.hide("everything")

cmd.select("hydrogen_atoms", "elem H")  # Select carbon atoms
cmd.show("spheres", "hydrogen_atoms")  # Display carbon atoms as sticks (you can use other representations as well)

cmd.hide("everything")

cmd.select("nitrogen_atoms", "elem N")  # Select carbon atoms
cmd.show("spheres", "nitrogen_atoms")  # Display carbon atoms as sticks (you can use other representations as well)

cmd.hide("everything")

cmd.select("oxygen_atoms", "elem O")  # Select carbon atoms
cmd.show("spheres", "oxygen_atoms")

cmd.hide("everything")
cmd.save("output.stl", "all")


# Uložení obrázku
pymol.cmd.png("output_image.png", width=800, height=600, dpi=300)

# Zavření PyMOLu
pymol.cmd.quit()


