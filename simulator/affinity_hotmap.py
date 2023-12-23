import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_lower_triangle_affinity_matrix(file_path):
    """
    Plot a heatmap for the lower triangle of the affinity matrix stored in a CSV file.

    :param file_path: Path to the CSV file containing the affinity matrix.
    """
    # Load the affinity matrix from the CSV file
    affinity_matrix = pd.read_csv(file_path, header=None).values

    # Mask the upper triangle of the matrix
    mask = np.triu(np.ones_like(affinity_matrix, dtype=bool))

    # Plotting
    plt.figure(figsize=(10, 8))
    plt.imshow(np.ma.array(affinity_matrix, mask=mask), cmap='hot', interpolation='nearest')
    plt.colorbar()
    plt.title("Lower Triangle of Affinity Matrix Heatmap")
    plt.xlabel("Satellite Index")
    plt.ylabel("Satellite Index")
    plt.show()

# Example usage:
# plot_lower_triangle_affinity_matrix('path_to_your_affinity_matrix_file.csv')
# Replace 'path_to_your_affinity_matrix_file.csv' with the actual path to your file.

filepath = 'average_affinity_matrix.csv'
plot_lower_triangle_affinity_matrix(filepath)