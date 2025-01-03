import pandas as pd
import seaborn as sns
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import squareform
import matplotlib.pyplot as plt
import argparse

def load_and_prepare_matrix(file_path):
    """
    Load a similarity matrix (e.g., ANIb, dDDH, AAI) and ensure it's symmetrical.
    """
    matrix = pd.read_excel(file_path, index_col=0)

    # Make the matrix symmetrical by averaging reciprocal values
    for i in range(matrix.shape[0]):
        for j in range(i + 1, matrix.shape[1]):
            avg_value = (matrix.iloc[i, j] + matrix.iloc[j, i]) / 2
            matrix.iloc[i, j] = avg_value
            matrix.iloc[j, i] = avg_value

    return matrix

def calculate_distance_matrix(similarity_matrix):
    """
    Convert a similarity matrix into a distance matrix (100 - similarity).
    """
    distance_matrix = 100 - similarity_matrix
    return distance_matrix

def generate_clustermap(similarity_matrix, metadata=None, output="clustermap.png"):
    """
    Generate a clustermap for a similarity matrix.

    Args:
        similarity_matrix: A symmetrical pandas DataFrame with similarity values.
        metadata: Path to the metadata file (optional) to color labels by species or other annotations.
        output: Path to save the clustermap image.
    """
    # Convert similarity matrix to distance matrix
    distance_matrix = calculate_distance_matrix(similarity_matrix)

    # Convert the distance matrix to a condensed form for clustering
    condensed_distance_matrix = squareform(distance_matrix)

    # Perform hierarchical clustering
    linkage_matrix = linkage(condensed_distance_matrix, method='average')

    # Load metadata if provided
    species_color_map = None
    if metadata:
        metadata = pd.read_excel(metadata)
        species_color_map = metadata.set_index('Isolate')['Color'].to_dict()

    # Create the clustermap
    clustermap = sns.clustermap(
        similarity_matrix,
        row_linkage=linkage_matrix,
        col_linkage=linkage_matrix,
        cmap='coolwarm',
        figsize=(20, 20),
        dendrogram_ratio=(.1, .1),
        cbar_pos=(1.05, 0.3, 0.03, 0.4)
    )

    # Adjust label colors based on metadata if available
    if species_color_map:
        for label in clustermap.ax_heatmap.get_yticklabels():
            species_name = label.get_text()
            color = species_color_map.get(species_name, 'black')  # Default to black if no match
            label.set_color(color)

    # Remove column labels for clean output
    clustermap.ax_heatmap.set_xticklabels([])
    clustermap.ax_heatmap.set_yticklabels(clustermap.ax_heatmap.get_yticklabels(), fontsize=12)

    # Save the clustermap
    clustermap.savefig(output, dpi=300)
    print(f"Clustermap saved to {output}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a clustermap from a similarity matrix.")
    parser.add_argument("--matrix", required=True, help="Path to the similarity matrix file (Excel format).")
    parser.add_argument("--metadata", required=False, help="Path to the metadata file (Excel format). Optional.")
    parser.add_argument("--output", required=True, help="Path to save the generated clustermap image.")

    args = parser.parse_args()

    # Load and process the matrix
    matrix = load_and_prepare_matrix(args.matrix)

    # Generate and save the clustermap
    generate_clustermap(matrix, metadata=args.metadata, output=args.output)
