#Testing Python script
from PDBfileParse import extract_coordinates2
from version2.src.MoleculeModelGenerating import extract_coord

def choose_function(function1, function2, *args, **kwargs):
    # Call the first function
    output1 = function1(*args, **kwargs)

    # Count 'C' in the output
    c_count = len(output1.get('C', []))
    print(c_count)
    # Check if there are less than 2 'C'
    if c_count < 2:
        output2 = function2(*args, **kwargs)
        return output2
    else:
        return output1

# Example usage
#result = choose_function(function1, function2, args_for_functions)

pdb_filename2 = '/Users/jakubvavra/Documents/GitHub/3D-Print-Molecules/version2/ExamplePDB/atp.pdb'    
pdb_filename1 = '/Users/jakubvavra/Documents/GitHub/3D-Print-Molecules/version2/ExamplePDB/4WB5.pdb'    
pdb_filename = pdb_filename1

A = extract_coordinates2(pdb_filename)
print("Function 1:"+str(A))
B = extract_coord(pdb_filename)
print("Function 2:"+str(B))
print()


coordinates_dict = choose_function(extract_coordinates2, extract_coord, pdb_filename)
print()
print()
print("-----------")
print(coordinates_dict)