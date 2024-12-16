import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse

def pan_genome_clustermap(gene_file, output_file):
    # Load gene presence/absence data
    df = pd.read_csv(gene_file, index_col=0, low_memory=False)
    data_binary = df.iloc[:, 3:].T.notna().astype(int)

    # Generate clustermap
    clustermap = sns.clustermap(
        data_binary,
        cmap='Blues',
        figsize=(20, 30),
        row_cluster=True,
        col_cluster=False
    )
    clustermap.ax_heatmap.set_xticklabels([])
    clustermap.cax.set_visible(False)

    # Save heatmap
    clustermap.savefig(output_file, dpi=300)
    print(f"Clustermap saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate clustermap for gene presence/absence data.")
    parser.add_argument("--gene-file", required=True, help="Path to the gene presence/absence CSV file.")
    parser.add_argument("--output", required=True, help="Path to save the clustermap PNG file.")
    args = parser.parse_args()

    pan_genome_clustermap(args.gene_file, args.output)
