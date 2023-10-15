import FreeCAD
import ImportGui
import Mesh

# Nastavte cestu ke souboru .wrl
input_file = "/Users/jakubvavra/Desktop/mlk.wrl"

# Načtěte soubor .wrl
doc = FreeCAD.newDocument("ImportedModel")
ImportGui.open(input_file)

# Exportujte do formátu .stp
output_file = "/Users/jakubvavra/Desktop/soubor.stp"
Mesh.export([doc.getObject("Shape")], output_file)