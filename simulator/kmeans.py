import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

# Load the data from the uploaded file
file_path = 'average_affinity_matrix.csv'
affinity_matrix_df = pd.read_csv(file_path)

# Display the first few rows of the dataframe to understand its structure
affinity_matrix_df.head()

# Prepare the data for clustering using the affinity matrix as features
features = affinity_matrix_df.values

# Number of clusters (groups)
num_clusters = 50

# Applying K-means clustering using the affinity matrix
kmeans = KMeans(n_clusters=num_clusters, random_state=0)
clusters = kmeans.fit_predict(features)

# Creating a DataFrame for the cluster assignments
cluster_assignments_df = pd.DataFrame({'Node': [f"V GUOWANG #{i+1}" for i in range(len(clusters))], 'Cluster': [f"Group{c+1}" for c in clusters]})

# Save the DataFrame to a CSV file
output_file_path = 'node_cluster_50_assignments_affinity.csv'
cluster_assignments_df.to_csv(output_file_path, index=False)