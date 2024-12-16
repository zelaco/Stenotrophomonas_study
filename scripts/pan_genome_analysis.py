import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse

def calculate_pan_genome_stats(data_binary_df):
    """
    Calculate pan-genome size statistics (core, shell, cloud, and unique genes).
    """
    num_genomes = data_binary_df.shape[0]

    # Core Genes: present in 99% to 100% of strains
    core_genes = data_binary_df.columns[(data_binary_df.sum(axis=0) / num_genomes >= 0.99)].size

    # Soft Core Genes: present in 95% to 99% of strains
    soft_core_genes = data_binary_df.columns[(data_binary_df.sum(axis=0) / num_genomes >= 0.95) & 
                                             (data_binary_df.sum(axis=0) / num_genomes < 0.99)].size

    # Shell Genes: present in 15% to 95% of strains
    shell_genes = data_binary_df.columns[(data_binary_df.sum(axis=0) / num_genomes >= 0.15) & 
                                         (data_binary_df.sum(axis=0) / num_genomes < 0.95)].size

    # Cloud Genes: present in 1% to 15% of strains
    cloud_genes = data_binary_df.columns[(data_binary_df.sum(axis=0) / num_genomes >= 0.01) & 
                                         (data_binary_df.sum(axis=0) / num_genomes < 0.15)].size

    # Unique Genes: present in only 1 strain
    unique_genes = data_binary_df.columns[(data_binary_df.sum(axis=0) == 1)].size

    # Total number of orthologous groups (Pan-genome size)
    pan_genome = data_binary_df.shape[1]

    return core_genes, soft_core_genes, shell_genes, cloud_genes, unique_genes, pan_genome

def calculate_pan_core_evolution(data_binary_df, iterations=500):
    """
    Calculate the evolution of core and pan-genome sizes using bootstrapping.
    """
    genomes = data_binary_df.index.tolist()
    core_genome_sizes_list = []
    pan_genome_sizes_list = []

    for _ in range(iterations):
        np.random.shuffle(genomes)
        core_genome = set(data_binary_df.columns)
        pan_genome = set()
        core_genome_sizes = []
        pan_genome_sizes = []

        for genome in genomes:
            genome_orthologs = set(data_binary_df.columns[data_binary_df.loc[genome] == 1])
            core_genome &= genome_orthologs
            pan_genome |= genome_orthologs
            core_genome_sizes.append(len(core_genome))
            pan_genome_sizes.append(len(pan_genome))

        core_genome_sizes_list.append(core_genome_sizes)
        pan_genome_sizes_list.append(pan_genome_sizes)

    return (np.mean(core_genome_sizes_list, axis=0), 
            np.std(core_genome_sizes_list, axis=0), 
            np.mean(pan_genome_sizes_list, axis=0), 
            np.std(pan_genome_sizes_list, axis=0))

def plot_pan_core_evolution(core_mean, core_std, pan_mean, pan_std, output_file):
    """
    Plot the evolution of core and pan-genome sizes and save the plot.
    """
    plt.figure(figsize=(10, 6))
    plt.errorbar(range(1, len(core_mean) + 1), core_mean, yerr=core_std, label='Core Genome', 
                 color='#2ca02c', marker='o', capsize=4)
    plt.errorbar(range(1, len(pan_mean) + 1), pan_mean, yerr=pan_std, label='Pan Genome', 
                 color='#1f77b4', marker='o', capsize=4)
    plt.xlabel("Number of Genomes")
    plt.ylabel("Number of Genes")
    plt.legend()
    plt.savefig(output_file, dpi=300)
    plt.close()
    print(f"Pan-core genome evolution plot saved to {output_file}")

def main(gene_presence_file, output_stats_file, output_plot_file):
    # Load the gene presence/absence CSV file
    gene_presence_df = pd.read_csv(gene_presence_file, index_col=0, low_memory=False)
    data_binary_df = gene_presence_df.iloc[:, 3:].T.notna().astype(int)

    # Calculate pan-genome statistics
    core, soft_core, shell, cloud, unique, pan_genome = calculate_pan_genome_stats(data_binary_df)

    # Save statistics to file
    stats = {
        "Core Genes": core,
        "Soft Core Genes": soft_core,
        "Shell Genes": shell,
        "Cloud Genes": cloud,
        "Unique Genes": unique,
        "Pan-genome Size": pan_genome,
    }
    pd.DataFrame(stats, index=["Count"]).to_csv(output_stats_file)
    print(f"Pan-genome statistics saved to {output_stats_file}")

    # Calculate and plot pan-core genome evolution
    core_mean, core_std, pan_mean, pan_std = calculate_pan_core_evolution(data_binary_df)
    plot_pan_core_evolution(core_mean, core_std, pan_mean, pan_std, output_plot_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze and plot pan-genome statistics and evolution.")
    parser.add_argument("--gene-file", required=True, help="Path to the gene presence/absence CSV file.")
    parser.add_argument("--output-stats", required=True, help="Path to save pan-genome statistics CSV.")
    parser.add_argument("--output-plot", required=True, help="Path to save pan-core genome evolution plot.")
    args = parser.parse_args()

    main(args.gene_file, args.output_stats, args.output_plot)
