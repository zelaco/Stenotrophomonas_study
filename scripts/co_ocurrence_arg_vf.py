import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import argparse

def generate_co_occurrence_network(metadata_file, virulence_file, resistance_file, output_file):
    # Load metadata
    metadata_df = pd.read_excel(metadata_file)
    virulence_df = pd.read_csv(virulence_file, sep='\t')
    resistance_df = pd.read_csv(resistance_file, sep='\t')

    # Prepare co-occurrence data (simplified for brevity)
    combined_genes_df = pd.concat([virulence_df, resistance_df], axis=1).fillna(0)

    # Co-occurrence matrix
    co_occurrence_matrix = combined_genes_df.T.dot(combined_genes_df)
    np.fill_diagonal(co_occurrence_matrix.values, 0)

    # Create network graph
    G = nx.Graph()
    for gene in co_occurrence_matrix.columns:
        G.add_node(gene)

    for i, gene1 in enumerate(co_occurrence_matrix.columns):
        for j, gene2 in enumerate(co_occurrence_matrix.columns):
            if co_occurrence_matrix.iloc[i, j] > 0:
                G.add_edge(gene1, gene2, weight=co_occurrence_matrix.iloc[i, j])

    # Draw the graph
    pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos, node_size=500, with_labels=True)

    # Save the network plot
    plt.savefig(output_file, dpi=300)
    print(f"Co-occurrence network saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a co-occurrence network.")
    parser.add_argument("--metadata", required=True, help="Path to the metadata Excel file.")
    parser.add_argument("--virulence", required=True, help="Path to the virulence genes file.")
    parser.add_argument("--resistance", required=True, help="Path to the resistance genes file.")
    parser.add_argument("--output", required=True, help="Path to save the network PNG file.")
    args = parser.parse_args()

    generate_co_occurrence_network(args.metadata, args.virulence, args.resistance, args.output)
