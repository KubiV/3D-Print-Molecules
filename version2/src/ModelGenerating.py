import numpy as np
from stl import mesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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

    #fig = plt.figure()
    #ax = fig.add_subplot(111, projection='3d')

    # Plot the mesh
    #ax.plot_trisurf(combined_vertices[:, 0], combined_vertices[:, 1], combined_vertices[:, 2], triangles=combined_faces, cmap='viridis')

    # Show the plot
    #plt.show()

radius = 1.0
resolution = 10

# Define the translation vectors for each sphere
translation_vectors = [
    np.array([1.0, 2.0, 3.0]),
    np.array([-2.0, 0.0, 1.0]),
    np.array([0.0, -2.0, 0.0]),
    np.array([1.0, -2.0, 0.0])
]

# Save all spheres in one STL file
#create_and_save_multiple_spheres(radius, resolution, translation_vectors, "combined_spheres.stl")

