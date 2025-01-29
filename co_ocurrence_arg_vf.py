import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Load the provided files
metadata_path = "Data/Metadata.xlsx"
virulence_path = "Data/summary_vfdb.tab"
resistance_path = "Data/summary_ncbi.tab"

# Load metadata
metadata_df = pd.read_excel(metadata_path)

# Load virulence and resistance data
virulence_df = pd.read_csv(virulence_path, sep='\t')
resistance_df = pd.read_csv(resistance_path, sep='\t')

# Correct the column name for Isolate
isolate_names = metadata_df['Isolate']

# Rename index of resistance and virulence dataframes to match metadata isolate names
virulence_df.set_index('#FILE', inplace=True)
resistance_df.set_index('#FILE', inplace=True)

# Keep only rows present in metadata to ensure consistency
virulence_df = virulence_df.loc[virulence_df.index.intersection(isolate_names)]
resistance_df = resistance_df.loc[resistance_df.index.intersection(isolate_names)]

# Combine virulence and resistance data
combined_genes_df = pd.concat([virulence_df, resistance_df], axis=1)
combined_genes_df.fillna(0, inplace=True)  

# Convert any remaining gene presence values to binary (0 or 1)
combined_genes_df = combined_genes_df.applymap(lambda x: 1 if isinstance(x, (int, float)) and x > 0 else 0)

# Adding isolation source information from metadata
combined_genes_df = combined_genes_df.join(metadata_df.set_index('Isolate')['Isolation Source'])

# Prepare co-occurrence matrix for resistance and virulence genes
# Calculate co-occurrence across isolates
co_occurrence_matrix = combined_genes_df.iloc[:, :-1].T.dot(combined_genes_df.iloc[:, :-1])
np.fill_diagonal(co_occurrence_matrix.values, 0)  # Set diagonal to 0 to avoid self-co-occurrence

# Creating a NetworkX graph from the co-occurrence matrix
G = nx.Graph()

# Adding nodes to the graph (genes)
for gene in co_occurrence_matrix.columns:
    # Determine the type of gene (Resistance or Virulence)
    gene_type = "Resistance" if gene in resistance_df.columns else "Virulence"
    # Adding the node with the gene type as an attribute
    G.add_node(gene, type=gene_type)

# Adding edges (connections) based on co-occurrence values
for i, gene1 in enumerate(co_occurrence_matrix.columns):
    for j, gene2 in enumerate(co_occurrence_matrix.columns):
        if co_occurrence_matrix.iloc[i, j] > 0:  # Only add edge if co-occurrence is greater than 0
            G.add_edge(gene1, gene2, weight=co_occurrence_matrix.iloc[i, j])

# Determine the isolation source for each gene
# Creating a dictionary to keep track of counts for each source per gene
gene_source_counts = {}

# Iterate over the combined dataframe to count occurrences of each gene per source type
for gene in combined_genes_df.columns[:-1]:  # Exclude the isolation source column
    gene_source_counts[gene] = combined_genes_df.groupby('Isolation Source')[gene].sum()

# Create a dictionary to hold the most frequent isolation source for each gene
gene_colors = {}

# Assign a color based on the highest occurrence across the sources
for gene, counts in gene_source_counts.items():
    if counts.get('Clinical', 0) >= counts.get('Environmental', 0) and counts.get('Clinical', 0) >= counts.get('Anthropogenic', 0):
        gene_colors[gene] = '#bd3b2a'  # Clinical
    elif counts.get('Anthropogenic', 0) >= counts.get('Environmental', 0):
        gene_colors[gene] = '#cfcb65'  # Anthropogenic
    else:
        gene_colors[gene] = '#6c945c'  # Environmental

# Draw the updated graph with different line styles for edges
plt.figure(figsize=(15, 12))

# Define edge line styles based on the type of genes they connect
edge_styles = []

for edge in G.edges():
    node1, node2 = edge
    # Both nodes are resistance genes
    if G.nodes[node1]['type'] == 'Resistance' and G.nodes[node2]['type'] == 'Resistance':
        edge_styles.append(('solid', '#7a7878'))  # Solid line for resistance-resistance
    # Both nodes are virulence genes
    elif G.nodes[node1]['type'] == 'Virulence' and G.nodes[node2]['type'] == 'Virulence':
        edge_styles.append(('dashed', '#424141'))  # Dashed line for virulence-virulence
    # One node is resistance and the other is virulence
    else:
        edge_styles.append(('dotted', '#000000'))  # Dotted line for resistance-virulence

# Drawing nodes with the existing color scheme for isolation source
pos = nx.spring_layout(G, k=0.5)  # Position nodes using Fruchterman-Reingold force-directed algorithm
nx.draw_networkx_nodes(G, pos, node_color=[gene_colors[node] for node in G.nodes()], node_size=600, alpha=0.8)

# Draw edges with different styles
for (edge, style) in zip(G.edges(), edge_styles):
    nx.draw_networkx_edges(G, pos, edgelist=[edge], style=style[0], edge_color=style[1], alpha=0.6)

# Draw labels for nodes with reduced font size for better fitting
nx.draw_networkx_labels(G, pos, font_size=8)

# Adding legend to explain node colors and edge styles
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='Environmental', markerfacecolor='#6c945c', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='Anthropogenic', markerfacecolor='#cfcb65', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='Clinical', markerfacecolor='#bd3b2a', markersize=10),
    Line2D([0], [0], color='#7a7878', lw=2, linestyle='solid', label='Resistance-Resistance'),
    Line2D([0], [0], color='#424141', lw=2, linestyle='dashed', label='Virulence-Virulence'),
    Line2D([0], [0], color='#000000', lw=2, linestyle='dotted', label='Resistance-Virulence'),
]

plt.legend(handles=legend_elements, loc='upper right', fontsize='medium', frameon=True)


plt.savefig('Outputs/co_ocurrence.png', dpi=300)
