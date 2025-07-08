import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
import os

# Enable memory growth for the GPU
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        print("Memory growth enabled for GPU.")
    except RuntimeError as e:
        print(f"Error enabling memory growth: {e}")

# Path to your CSV file
csv_file = "/home/kondr/football_manager_proj/fman_initial_Dat_Analysis_test/fbmandataset.csv"

# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv(csv_file)

# Create a smaller sample (e.g., 10,000 rows)
sample_size = 10000
df_sample = df.sample(n=sample_size, random_state=42)

# Select only numeric columns for normalization
numeric_columns = df_sample.select_dtypes(include=["number"]).columns
df_sample[numeric_columns] = df_sample[numeric_columns] / df_sample[numeric_columns].max()

# Extract features for clustering
features = tf.convert_to_tensor(df_sample[numeric_columns].values, dtype=tf.float32)

# Perform K-Means clustering using TensorFlow
def kmeans_clustering(features, num_clusters, num_iterations=10):
    # Randomly initialize cluster centroids
    centroids = tf.Variable(tf.random.shuffle(features)[:num_clusters])

    for _ in range(num_iterations):
        # Compute distances between features and centroids
        distances = tf.reduce_sum(tf.square(tf.expand_dims(features, axis=1) - centroids), axis=2)
        cluster_assignments = tf.argmin(distances, axis=1)

        # Update centroids
        for i in range(num_clusters):
            mask = tf.equal(cluster_assignments, i)
            cluster_points = tf.boolean_mask(features, mask)
            if tf.size(cluster_points) > 0:  # Avoid empty clusters
                centroids[i].assign(tf.reduce_mean(cluster_points, axis=0))

    # Compute inertia (sum of squared distances)
    inertia = tf.reduce_sum(tf.reduce_min(distances, axis=1))
    return cluster_assignments, centroids, inertia.numpy()

# Test multiple cluster numbers and compute inertia
cluster_range = range(1, 15)  # Test 1 to 10 clusters
inertia_values = []

for num_clusters in cluster_range:
    _, _, inertia = kmeans_clustering(features, num_clusters)
    inertia_values.append(inertia)
    print(f"Number of clusters: {num_clusters}, Inertia: {inertia}")

# Plot the Elbow Method graph
plt.figure(figsize=(8, 5))
plt.plot(cluster_range, inertia_values, marker='o')
plt.title("Elbow Method: Number of Clusters vs Inertia")
plt.xlabel("Number of Clusters")
plt.ylabel("Inertia")
plt.grid()
elbow_path = os.path.join(script_dir, "elbow_method_tf.png")
plt.savefig(elbow_path)  # Save the plot to the script's folder
print(f"Elbow Method graph saved as '{elbow_path}'.")
#code not working, don't try to run it