# pip install numpy-stl tripy
# pip install numpy-stl meshlabxml


from stl import mesh
from meshlabxml import MeshlabXML

def repair_stl(input_file, output_file):
    # Load the STL file
    mesh_data = mesh.Mesh.from_file(input_file)

    # Check if the mesh is watertight
    if not mesh_data.is_watertight:
        # Save the mesh to a temporary file
        temp_file = "temp.stl"
        mesh_data.save(temp_file)

        # Use MeshlabXML to repair the mesh
        meshlab_script = """
        <!DOCTYPE FilterScript>
        <FilterScript>
            <filter name="closeholes" />
        </FilterScript>
        """
        ml = MeshlabXML()
        ml.load_mesh(temp_file)
        ml.apply_filter_script(meshlab_script)
        ml.save_mesh(output_file)

    else:
        # If the mesh is already watertight, save it directly
        mesh_data.save(output_file)

# Replace 'input.stl' and 'output.stl' with your file names
repair_stl('C_output.stl', 'C_repaired.stl')
