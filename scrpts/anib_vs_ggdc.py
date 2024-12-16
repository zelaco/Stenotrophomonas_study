import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import argparse

def anib_vs_ggdc_correlation(anib_file, ggdc_file, output_file):
    # Load matrices
    ggdc = pd.read_excel(ggdc_file, index_col=0)
    anib = pd.read_excel(anib_file, index_col=0)

    # Extract lower triangle values
    ggdc_values = ggdc.values[np.tril_indices_from(ggdc.values, k=-1)]
    anib_values = anib.values[np.tril_indices_from(anib.values, k=-1)]

    # Calculate Pearson correlation
    r, p_value = pearsonr(anib_values, ggdc_values)
    p_value_str = "< 1e-10" if p_value < 1e-10 else f"{p_value:.2e}"

    # Plot scatter plot
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=anib_values, y=ggdc_values)
    plt.xlabel('ANIb (%)', fontsize=16)
    plt.ylabel('dDDH (%)', fontsize=16)
    plt.annotate(f'Pearson r = {r:.2f}\nP-value: {p_value_str}',
                 xy=(0.05, 0.95), xycoords='axes fraction', fontsize=16, 
                 ha='left', va='top')
    plt.axvline(95, color='red', linestyle='--', label='ANIb = 95%')
    plt.axhline(70, color='blue', linestyle='--', label='GGDC = 70%')
    plt.legend()
    plt.tight_layout()

    # Save the plot
    plt.savefig(output_file, dpi=300)
    print(f"Scatter plot saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare ANIb and GGDC values.")
    parser.add_argument("--anib", required=True, help="Path to the ANIb Excel file.")
    parser.add_argument("--ggdc", required=True, help="Path to the GGDC Excel file.")
    parser.add_argument("--output", required=True, help="Path to save the scatter plot.")
    args = parser.parse_args()

    anib_vs_ggdc_correlation(args.anib, args.ggdc, args.output)
