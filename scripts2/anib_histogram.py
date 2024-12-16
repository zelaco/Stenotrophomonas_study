import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse

def generate_anib_histogram(matrix_file, output_file):
    # Load the ANI matrix
    ani_matrix = pd.read_excel(matrix_file, index_col=0)

    # Convert matrix to numpy array and extract the upper triangle
    ani_array = ani_matrix.to_numpy()
    upper_triangle = ani_array[np.triu_indices_from(ani_array, k=1)]

    # Plot the histogram
    plt.figure(figsize=(10, 6))
    plt.hist(upper_triangle, bins=28, color='#3e7bb8', edgecolor='black')
    plt.xlabel('ANIb (%)', fontsize=16)
    plt.ylabel('Frequency', fontsize=16)
    plt.tight_layout()

    # Save the plot
    plt.savefig(output_file, dpi=300)
    print(f"Histogram saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate an ANI histogram.")
    parser.add_argument("--matrix", required=True, help="Path to the ANI matrix Excel file.")
    parser.add_argument("--output", required=True, help="Path to save the histogram PNG file.")
    args = parser.parse_args()

    generate_anib_histogram(args.matrix, args.output)
