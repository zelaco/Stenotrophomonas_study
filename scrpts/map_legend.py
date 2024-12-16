import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import argparse

def generate_legend(metadata_file, output_file):
    # Load the updated metadata with the 'Color' column
    metadata = pd.read_excel(metadata_file)

    # Extract the species and their colors
    species_color_map = metadata.drop_duplicates(subset=['Final Id']).set_index('Final Id')['Color'].to_dict()

    # Create custom legend handles
    legend_handles = [Patch(color=color, label=species) for species, color in species_color_map.items()]

    # Create a figure for just the legend
    fig, ax = plt.subplots(figsize=(8, len(legend_handles) / 8))
    ax.axis('off')

    # Add the legend
    plt.legend(
        handles=legend_handles,
        title='Species',
        ncol=4,
        fontsize='small',
        frameon=False,
        loc='center'
    )

    # Save the legend
    plt.savefig(output_file, dpi=300)
    print(f"Legend saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a standalone legend for species.")
    parser.add_argument("--metadata", required=True, help="Path to the metadata Excel file.")
    parser.add_argument("--output", required=True, help="Path to save the legend PNG file.")
    args = parser.parse_args()

    generate_legend(args.metadata, args.output)
