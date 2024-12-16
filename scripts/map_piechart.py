import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# Load the updated metadata with the 'Color' column
file_path = 'Data/Updated_Metadata.xlsx'
metadata = pd.read_excel(file_path)

# Group the data by continent and species (Final Id)
lineage_by_continent = metadata.groupby(['Continent', 'Final Id'])['Final Id'].count().unstack(fill_value=0)

# Get the species list in the order of the DataFrame
species_list = lineage_by_continent.columns.tolist()

# Extract the corresponding colors from the 'Color' column in the metadata
species_color_map = metadata.drop_duplicates(subset=['Final Id']).set_index('Final Id')['Color'].to_dict()

# Number of continents
n_continents = len(lineage_by_continent.index)

# Set up the pie chart grid layout: 2 rows and columns based on the number of continents
fig, axes = plt.subplots(2, (n_continents + 1) // 2, figsize=(20, 15))  # 2 rows, divide continents into columns

# Flatten axes for easier iteration
axes = axes.flatten()

# Plot pie charts for each continent
continents = lineage_by_continent.index.tolist()

for i, continent in enumerate(continents):
    sizes = lineage_by_continent.loc[continent]
    sizes = sizes[sizes > 0]  # Filter out zero values
    labels = sizes.index.tolist()
    colors = [species_color_map.get(species, "#000000") for species in labels]  # Get corresponding colors
    
    # Plot pie chart without labels and percentages
    axes[i].pie(sizes, colors=colors, startangle=90)
    axes[i].set_title(continent)

# Hide any unused subplot spaces
for ax in axes[len(continents):]:
    ax.axis('off')

# Adjust layout for pie charts
plt.tight_layout(rect=[0, 0.2, 1, 1])  # Leave space for the legend below the charts

# --- Shared legend creation ---

# Create custom legend handles to ensure correct color mapping
legend_handles = [Patch(color=species_color_map[species], label=species) for species in species_list]

# Add the legend below the pie charts
plt.legend(
    handles=legend_handles,
    title='Species',
    ncol=5,  # Number of columns for the legend
    fontsize='small',
    frameon=False,
    loc='right',
    bbox_to_anchor=(0, -0.5)
)


# save the plot
plt.savefig('Outputs/pie_chart.png', dpi=300)