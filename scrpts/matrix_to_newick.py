import pandas as pd
import numpy as np
import scipy.cluster.hierarchy as sch
import argparse

def matrix_to_newick(matrix_file, output_file):
    # Load the matrix
    df = pd.read_excel(matrix_file, index_col=0)
    
    # Ensure matrix is symmetrical
    size = len(df.columns)
    similarity_matrix = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            if i == j:
                similarity_matrix[i, j] = 1
            elif i < j:
                values = [df.iloc[i, j], df.iloc[j, i]]
                similarity_matrix[i, j] = similarity_matrix[j, i] = np.median([v for v in values if pd.notna(v)])
    np.fill_diagonal(similarity_matrix, 1)

    # Convert to distance matrix
    max_similarity = np.nanmax(similarity_matrix)
    distance_matrix = max_similarity - similarity_matrix
    np.fill_diagonal(distance_matrix, 0)
    condensed_distance_matrix = sch.distance.squareform(distance_matrix)

    # Perform clustering
    linkage_matrix = sch.linkage(condensed_distance_matrix, method='average')

    # Convert to Newick format
    def to_newick(Z, labels):
        def get_newick(node, parent_dist, leaf_names, newick, distances):
            if node < len(leaf_names):
                return f"{leaf_names[node]}:{parent_dist - distances[node]}{newick}"
            else:
                left, right = int(Z[node - len(leaf_names), 0]), int(Z[node - len(leaf_names), 1])
                dist = Z[node - len(leaf_names), 2]
                return f"({get_newick(left, dist, leaf_names, newick, distances)},{get_newick(right, dist, leaf_names, newick, distances)}):{parent_dist - distances[node]}{newick}"
        distances = {i + len(labels): merge[2] for i, merge in enumerate(Z)}
        return get_newick(len(Z) + len(labels) - 1, Z[-1, 2], labels, "", distances) + ";"

    newick_tree = to_newick(linkage_matrix, df.columns.tolist())

    # Save Newick tree
    with open(output_file, 'w') as f:
        f.write(newick_tree)
    print(f"Newick tree saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert similarity matrix to Newick tree.")
    parser.add_argument("--matrix", required=True, help="Path to the similarity matrix Excel file.")
    parser.add_argument("--output", required=True, help="Path to save the Newick tree.")
    args = parser.parse_args()

    matrix_to_newick(args.matrix, args.output)
