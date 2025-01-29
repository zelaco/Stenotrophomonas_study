import re
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# Load the metadata 
file_path = 'Data/Metadata.xlsx'
metadata = pd.read_excel(file_path)

# Extract the species and their colors
species_color_map = metadata.drop_duplicates(subset=['Final Id']).set_index('Final Id')['Color'].to_dict()

# Function to sort species names based on numeric parts 
def sort_species(species_list):
    def extract_number(s):
        match = re.search(r'\bsp(\d+)\b', s)
        return int(match.group(1)) if match else float('inf')  # Sort species with 'sp' numerically, others last
    return sorted(species_list, key=extract_number)

# Sort the species list
sorted_species = sort_species(list(species_color_map.keys()))

# Function to format species names
def format_species_name(species):
    # Check if the species has ' spX'
    if ' sp' in species:
        # Separate the genus and spX
        genus, sp_part = species.split(' sp', 1)
        return rf'$\it{{{genus}}}$ sp{sp_part}'  # Italicize only the genus part, keep spX normal
    else:
        # Italicize the entire species name if it doesn't have 'sp', including any spaces between genus and species
        return rf'$\it{{{species.replace(" ", "\ ")}}}$'  # Keep the space between genus and species

# Create custom legend handles for the sorted species, with correct italicization
legend_handles = [Patch(color=species_color_map[species], label=format_species_name(species)) for species in sorted_species]

# Create a figure for just the legend
fig, ax = plt.subplots(figsize=(8, len(legend_handles) / 8)) 
ax.axis('off')  

# Add the legend with four columns
legend = plt.legend(
    handles=legend_handles,
    title='Species',
    ncol=4,  
    fontsize='small',
    frameon=False,
    loc='center'
)


# Show only the legend
plt.savefig('Outputs/legend.png', dpi=300)
