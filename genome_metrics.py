from Bio import SeqIO
import os
import csv
import numpy as np

def calculate_genome_metrics(fasta_file):
    contig_lengths = []
    gc_count = 0
    total_length = 0

    for record in SeqIO.parse(fasta_file, "fasta"):
        seq = record.seq
        length = len(seq)
        contig_lengths.append(length)
        total_length += length
        gc_count += seq.count('G') + seq.count('C')

    if total_length > 0:
        gc_content = (gc_count / total_length) * 100
    else:
        gc_content = 0

    contig_lengths.sort(reverse=True)
    cumulative_lengths = np.cumsum(contig_lengths)
    half_genome_size = total_length / 2
    n50 = next(length for length, cum_len in zip(contig_lengths, cumulative_lengths) if cum_len >= half_genome_size)

    num_contigs = len(contig_lengths)
    longest_contig = contig_lengths[0] if contig_lengths else 0
    shortest_contig = contig_lengths[-1] if contig_lengths else 0
    average_contig_length = total_length / num_contigs if num_contigs > 0 else 0

    return total_length, gc_content, num_contigs, n50, longest_contig, shortest_contig, average_contig_length

def process_fasta_files_in_directory(directory):
    results = []

    for filename in os.listdir(directory):
        if filename.endswith(".fasta") or filename.endswith(".fa"):
            filepath = os.path.join(directory, filename)
            metrics = calculate_genome_metrics(filepath)
            isolate_name = os.path.splitext(filename)[0]
            results.append((isolate_name, *metrics))

    return results

def save_results_to_csv(results, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Isolate Name', 'Genome Size', 'GC Content', 'Number of Contigs', 'N50', 'Longest Contig', 'Shortest Contig', 'Average Contig Length']
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
        for result in results:
            writer.writerow(result)

# Specify the directory containing the FASTA files and the output CSV file
directory = "genomes"
output_file = "genome_stats.csv"

results = process_fasta_files_in_directory(directory)
save_results_to_csv(results, output_file)

print(f"Results saved to {output_file}")
