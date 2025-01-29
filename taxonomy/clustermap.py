import pandas as pd
import seaborn as sns
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import squareform
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba

# Load matrix from Excel
ani_matrix = pd.read_excel('Data/matrix.xlsx', index_col=0)

# Make the matrix symmetrical by averaging reciprocal values
for i in range(ani_matrix.shape[0]):
    for j in range(i + 1, ani_matrix.shape[1]):
        avg_value = (ani_matrix.iloc[i, j] + ani_matrix.iloc[j, i]) / 2
        ani_matrix.iloc[i, j] = avg_value
        ani_matrix.iloc[j, i] = avg_value

# Convert the values to distance values 
distance_matrix = 100 - ani_matrix

# Convert the distance matrix to a condensed form (1D) for the linkage function
condensed_distance_matrix = squareform(distance_matrix)

# Perform hierarchical clustering using UPGMA (method='average')
linkage_matrix = linkage(condensed_distance_matrix, method='average')

# Load the updated metadata with the 'Color' column
metadata = pd.read_excel('Data/Metadata.xlsx')

# Extract the species and their colors
species_color_map = metadata.drop_duplicates(subset=['Isolate']).set_index('Isolate')['Color'].to_dict()

# Create a seaborn clustermap
clustermap = sns.clustermap(
    ani_matrix,
    row_linkage=linkage_matrix,
    col_linkage=linkage_matrix,  # You can set this to None if you want to cluster only rows
    cmap='coolwarm',
    figsize=(36, 30),  # Increase figure size
    dendrogram_ratio=(.1, 0),  # Adjust the ratio of the dendrogram to the heatmap
    cbar_pos=(1.05, 0.3, 0.03, 0.4)  # Adjust the position of the color bar (legend)
)

# Adjust dendrogram line thickness
for line in clustermap.ax_row_dendrogram.collections:
    line.set_linewidth(2)  # Thicker row dendrogram lines


# Adjust the font size and font name of the species names (row and column labels)
# Apply color mapping to row labels
for label in clustermap.ax_heatmap.get_yticklabels():
    species_name = label.get_text()
    color = species_color_map.get(species_name, 'black')  # Default to black if no color is found
    label.set_color(color)

# Remove the labels below (column labels)
clustermap.ax_heatmap.set_xticklabels([])
    
clustermap.ax_heatmap.set_yticklabels(
    clustermap.ax_heatmap.get_yticklabels(), fontsize=16, fontname='Arial') 

# Adjust the font size of the color bar (legend)
clustermap.ax_cbar.set_yticklabels(clustermap.ax_cbar.get_yticklabels(), fontsize=20) 

# Save the figure to a file
clustermap.savefig("Outputs/clustermap_matrix.png", dpi=300) 

# Extract the reordered indices of rows and columns from the clustermap
reordered_rows = clustermap.dendrogram_row.reordered_ind
reordered_cols = clustermap.dendrogram_col.reordered_ind

# Reorder the matrix according to the clustered heatmap order
reordered_matrix = ani_matrix.iloc[reordered_rows, reordered_cols]

# Export the reordered matrix to Excel or CSV
reordered_matrix.to_excel('Outputs/reordered_matrix.xlsx') 
