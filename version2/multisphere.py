import numpy as np
from stl import mesh

def create_sphere(radius, resolution):
    phi = np.linspace(0, np.pi, resolution)
    theta = np.linspace(0, 2 * np.pi, resolution)
    phi, theta = np.meshgrid(phi, theta)

    x = radius * np.sin(phi) * np.cos(theta)
    y = radius * np.sin(phi) * np.sin(theta)
    z = radius * np.cos(phi)

    return x, y, z

def translate(vertices, translation_vector):
    return vertices + translation_vector

def save_to_stl(filename, vertices, faces):
    mesh_data = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, face in enumerate(faces):
        for j in range(3):
            mesh_data.vectors[i][j] = vertices[face[j], :]

    mesh_data.save(filename)

def create_and_save_multiple_spheres(radius, resolution, translation_vectors, output_filename):
    all_vertices = []
    all_faces = []

    for translation_vector in translation_vectors:
        # Create the sphere
        x, y, z = create_sphere(radius, resolution)

        # Flatten the coordinates for vertices
        vertices = np.vstack([x.flatten(), y.flatten(), z.flatten()]).T

        # Translate the sphere
        translated_vertices = translate(vertices, translation_vector)

        # Create faces
        num_faces = (resolution - 1) * (resolution - 1) * 2
        faces = np.zeros((num_faces, 3), dtype=np.uint32)

        count = 0
        for j in range(resolution - 1):
            for k in range(resolution - 1):
                faces[count] = [j * resolution + k, (j + 1) * resolution + k, j * resolution + k + 1]
                count += 1
                faces[count] = [(j + 1) * resolution + k, (j + 1) * resolution + k + 1, j * resolution + k + 1]
                count += 1

        # Append vertices and faces to the overall lists
        all_vertices.append(translated_vertices)
        all_faces.append(faces)

    # Combine vertices and faces for all spheres
    combined_vertices = np.vstack(all_vertices)
    combined_faces = np.vstack([f + i * resolution**2 for i, f in enumerate(all_faces)])

    # Save all spheres to a single STL file
    save_to_stl(output_filename, combined_vertices, combined_faces)

def main():
    # Set the parameters for the spheres
    radius = 1.0
    resolution = 100

    # Define the translation vectors for each sphere
    translation_vectors = ['np.array([101.263 132.51   19.074])', 'np.array([ 98.757 132.171  16.304])', 'np.array([ 95.002 127.923  25.94 ])', 'np.array([ 97.195 136.775  16.142])', 'np.array([100.911 130.999  18.214])', 'np.array([ 96.821 125.429  26.398])', 'np.array([ 93.002 127.452  25.547])', 'np.array([101.092 131.88   15.889])', 'np.array([ 95.78  127.31   28.233])', 'np.array([ 99.841 128.736  17.589])', 'np.array([ 98.543 127.251  27.255])', 'np.array([ 98.563 128.615  15.875])', 'np.array([ 97.138 129.402  26.46 ])', 'np.array([ 97.288 129.604  18.106])', 'np.array([ 98.309 128.578  24.85 ])', 'np.array([ 91.942 123.873  23.603])', 'np.array([ 98.873 128.665  19.79 ])', 'np.array([ 98.358 125.529  24.768])', 'np.array([ 94.28  123.25   23.457])', 'np.array([ 96.012 124.771  24.383])', 'np.array([100.542 138.616  18.783])', 'np.array([ 91.179 127.363  26.151])', 'np.array([ 89.556 127.102  25.55 ])', 'np.array([ 97.748 129.913  20.409])', 'np.array([ 99.759 126.507  25.112])', 'np.array([101.481 137.266  19.379])']

    # Save all spheres in one STL file
    create_and_save_multiple_spheres(radius, resolution, translation_vectors, "combined_spheres.stl")

if __name__ == "__main__":
    main()
