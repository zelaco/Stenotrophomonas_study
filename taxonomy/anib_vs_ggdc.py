import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# Load GGDC and ANIb matrices from Excel
ggdc_matrix = pd.read_excel('Data/GGDC.xlsx', index_col=0)
anib_matrix = pd.read_excel('Data/ANIb.xlsx', index_col=0)

# Ensure that both matrices have the same rows and columns in the same order
ggdc_matrix = ggdc_matrix.reindex(index=anib_matrix.index, columns=anib_matrix.columns)

# Symmetrize the ANIb matrix by taking the median of each pair (i, j) and (j, i)
anib_symmetric = anib_matrix.copy()
for i in range(anib_matrix.shape[0]):
    for j in range(anib_matrix.shape[1]):
        if i != j:
            median_value = np.median([anib_matrix.iat[i, j], anib_matrix.iat[j, i]])
            anib_symmetric.iat[i, j] = median_value
            anib_symmetric.iat[j, i] = median_value

# Function to get lower triangle values
def get_lower_triangle_values(matrix):
    lower_triangle_indices = np.tril_indices_from(matrix, k=-1)
    lower_triangle_values = matrix.values[lower_triangle_indices]
    return lower_triangle_values

# Extract lower triangle values
ggdc_values = get_lower_triangle_values(ggdc_matrix)
anib_values = get_lower_triangle_values(anib_symmetric)

# Check if the number of lower triangle values is the same
if len(ggdc_values) != len(anib_values):
    print("Warning: Mismatch in matrix dimensions!")

# Calculate Pearson correlation coefficient and p-value
pearson_corr, p_value = pearsonr(anib_values, ggdc_values)

# Format the p-value for display
if p_value < 1e-10:
    p_value_str = '< 1e-10'
else:
    p_value_str = f'{p_value:.2e}'

# Create a seaborn scatter plot 
plt.figure(figsize=(10, 6))
sns.scatterplot(x=anib_values, y=ggdc_values)

# Set font size
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

# Add labels
plt.xlabel('ANIb (%)', fontsize=16)
plt.ylabel('dDDH (%)', fontsize=16)

# Add the Pearson correlation coefficient as an annotation
plt.annotate(f'Pearson r = {pearson_corr:.2f}\nP-value: {p_value_str}', 
             xy=(0.05, 0.95), xycoords='axes fraction', fontsize=16, 
             ha='left', va='top', bbox=dict(boxstyle='round,pad=0.3', 
                                            edgecolor='black', facecolor='white'))

# Add lines at ANIb = 95, ANIb = 96, and GGDC = 70
plt.axvline(x=95, color='#c43939', linestyle='--', label='ANIb = 95%')
plt.axvline(x=96, color='#c43939', linestyle='--', label='ANIb = 96%')
plt.axhline(y=70, color='#c43939', linestyle='--', label='GGDC = 70%')

# Save the plot
plt.savefig('Outputs/anib_ggdc.png', dpi=300)

