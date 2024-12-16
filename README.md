# Stenotrophomonas Study

This repository provides Python tools for calculating genome metrics, generating visualizations, and analyzing genomic data related to the chapter II of my doctoral thesis, and upcoming publication.

## Features
- **Genome Metrics Calculator**:
  - Parses multiple FASTA files in a directory.
  - Calculates genome statistics including:
    - Genome size
    - GC content
    - Number of contigs
    - N50
    - Longest and shortest contig lengths
    - Average contig length
  - Saves results to a CSV file.

- **Visualization Tools**:
  - Generate maps of isolate distribution by country.
  - Create standalone legends for maps.
  - Generate pie charts grouped by continents and species.
  - Produce histograms of ANI percentages.

- **Matrix Analysis Tools**:
  - Create clustermaps for similarity matrices (ANIb, dDDH, AAI).
  - Convert similarity matrices to Newick-formatted phylogenetic trees.
  - Compare ANIb vs. GGDC values with scatter plots.

- **Gene Presence/Absence Analysis**:
  - Generate heatmaps from gene presence/absence data.

- **Co-occurrence Networks**:
  - Generate co-occurrence networks for resistance and virulence genes.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/zelaco/Stenotrophomonas_study.git
   cd Stenotrophomonas_study
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
### 1. Genome Metrics Calculator
Calculates genome size statistics from FASTA files.
```bash
python scripts/genome_metrics.py --input-dir /path/to/fasta_files --output-file /path/to/output.csv
```

### 2. Visualization Tools
#### Generate a Map
Generate a choropleth map of isolate distribution by country.
```bash
python scripts/map.py --metadata /path/to/metadata.xlsx --output /path/to/map.html
```

#### Generate a Legend
Create a standalone legend for species or other metadata.
```bash
python scripts/map_legend.py --metadata /path/to/metadata.xlsx --output /path/to/legend.png
```

#### Generate Pie Charts
Plot pie charts showing species lineage by continent.
```bash
python scripts/map_piechart.py --metadata /path/to/metadata.xlsx --output /path/to/pie_chart.png
```

#### Generate ANI Histogram
Create a histogram of ANI percentages.
```bash
python scripts/anib_histogram.py --matrix /path/to/anib_matrix.xlsx --output /path/to/histogram.png
```

### 3. Matrix Analysis Tools
#### Generate a Clustermap
Create a hierarchical clustermap for similarity matrices.
```bash
python scripts/clustermap.py --matrix /path/to/matrix.xlsx --output /path/to/clustermap.png
```

#### Convert Matrix to Newick
Convert similarity matrices into Newick-formatted trees.
```bash
python scripts/matrix_to_newick.py --matrix /path/to/matrix.xlsx --output /path/to/tree.newick
```

#### Compare ANIb vs GGDC
Plot correlations between ANIb and GGDC values.
```bash
python scripts/anib_vs_ggdc.py --anib /path/to/anib_matrix.xlsx --ggdc /path/to/ggdc_matrix.xlsx --output /path/to/scatterplot.png
```

### 4. Gene Presence/Absence Analysis
#### Generate a Gene Heatmap
Generate heatmaps from gene presence/absence data.
```bash
python scripts/gene_presence_absence.py --gene-file /path/to/gene_presence.csv --output /path/to/heatmap.png
```

### 5. Pan-Genome Analysis
#### Calculate and Plot Pan-Core Genome Evolution
Calculate pan-genome statistics and plot pan-core genome evolution.
```bash
python scripts/pan_genome_analysis.py --gene-file /path/to/gene_presence.csv \
                                       --output-stats /path/to/pan_genome_stats.csv \
                                       --output-plot /path/to/pan_core_genome.png
```

### 6. Co-occurrence Networks
Visualize co-occurrence of resistance and virulence genes.
```bash
python scripts/co_occurrence_arg_vf.py --metadata /path/to/metadata.xlsx \
                                       --virulence /path/to/virulence_genes.tab \
                                       --resistance /path/to/resistance_genes.tab \
                                       --output /path/to/co_occurrence_network.png
```


