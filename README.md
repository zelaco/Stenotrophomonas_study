# Stenotrophomonas Study

## Code supplement

This repository provides Python scripts for calculating genome metrics, generating visualizations, and analyzing genomic data related to the chapter II of my doctoral thesis, and upcoming publication. regarding genomes of the genus Stenotrophomonas.

## Script explanation
- **'genome_metrics.py'**:
    - Parses multiple FASTA files in a directory.
    - Calculates genome statistics including:
        - Genome size
        - GC content
        - Number of contigs
        - N50
        - Longest and shortest contig lengths
        - Average contig length
    - Saves results to a CSV file.

- **map directory**:
  - Requires a metadata excel file with country, continent and species name information
  - 'map/map.py' generates a map of isolate distribution by country.
  - [map/map_legend.py] creates a standalone custom legend for the map data.
  - [map/map_piechart.py] generates pie charts grouped by continents and species.

- **taxonomy directory**:
  - Requires similarity matrix of genome-based identification data (ANIb. dDDH or AAI)
  - [taxonomy/clustermap.py] creates clustermaps for similarity matrices (ANIb, dDDH, AAI), with colored species names based on the previous metadata file.
  - [taxonomy/anib_vs_ggdc.py] compares the ANIb and dDDH values with scatter plots, with lines indicating species thresholds.
  - [taxonomy/anib_histogram.py] creates an histogram of the distributed anib values.

- **[pan_genome.ipynb]**:
  - requires a gene presence/absence matrix 
  - Generates a clustermap from gene presence/absence data.
  - Provides data regarding the core and pan genome size.
  - Performs a plot showing the evolution of core and pan genome based on the previous data.

- **[co_occurrence_arg_vf.py]**:
  - Requires a metadata file with origin information and the summary table outputs from abricate regarding antibiotic resistance and virulence genes
  - generates co-occurrence networks for resistance and virulence genes.

## Contact

If you have any questions or need further information, feel free to reach out:

    Email: [j.serpa@uib.es]
    GitHub: [github.com/zelaco]
