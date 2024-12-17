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
python scripts/genome_metrics.py --input-dir <FASTA FILES DIRECTORY> --output-file <OUTPUT.csv>
```

### 2. Visualization Tools
#### Generate a Map
Generate a choropleth map of isolate distribution by country.
```bash
python scripts/map.py --metadata <EXCEL FILE> --output <HTML FILE>
```

#### Generate a Legend
Create a standalone legend for species or other metadata.
```bash
python scripts/map_legend.py --metadata <EXCEL FILE> --output <PNG FILE>
```

#### Generate Pie Charts
Plot pie charts showing species lineage by continent.
```bash
python scripts/map_piechart.py --metadata <EXCEL FILE> --output <PNG FILE>
```

#### Generate ANI Histogram
Create a histogram of ANI percentages.
```bash
python scripts/anib_histogram.py --matrix <EXCEL FILE> --output <PNG FILE>
```

### 3. Matrix Analysis Tools
#### Generate a Clustermap
Create a hierarchical clustermap for similarity matrices.
```bash
python scripts/clustermap.py --matrix <EXCEL FILE> --output <PNG FILE>
```

#### Convert Matrix to Newick
Convert similarity matrices into Newick-formatted trees.
```bash
python scripts/matrix_to_newick.py --matrix <EXCEL FILE> --output <NEWICK FILE>
```

#### Compare ANIb vs GGDC
Plot correlations between ANIb and GGDC values.
```bash
python scripts/anib_vs_ggdc.py --anib <EXCEL FILE> --ggdc <EXCEL FILE> --output <PNG FILE>
```

### 4. Gene Presence/Absence Analysis
#### Generate a Gene Heatmap
Generate heatmaps from gene presence/absence data.
```bash
python scripts/gene_presence_absence.py --gene-file <CSV FILE> --output <PNG FILE>
```

### 5. Pan-Genome Analysis
#### Calculate and Plot Pan-Core Genome Evolution
Calculate pan-genome statistics and plot pan-core genome evolution.
```bash
python scripts/pan_genome_analysis.py --gene-file <CSV FILE> \
                                       --output-stats <CSV FILE> \
                                       --output-plot <PNG FILE>
```

### 6. Co-occurrence Networks
Visualize co-occurrence of resistance and virulence genes.
```bash
python scripts/co_occurrence_arg_vf.py --metadata <EXCEL FILE> \
                                       --virulence <TABULAR FILE> \
                                       --resistance <TABULAR FILE> \
                                       --output <PNG FILE>
```


