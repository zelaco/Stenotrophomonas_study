import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Load matrix from Excel
ani_matrix = pd.read_excel('Data/ANIb.xlsx', index_col=0)

# Make the matrix symmetrical by averaging reciprocal values
for i in range(ani_matrix.shape[0]):
    for j in range(i + 1, ani_matrix.shape[1]):
        avg_value = (ani_matrix.iloc[i, j] + ani_matrix.iloc[j, i]) / 2
        ani_matrix.iloc[i, j] = avg_value
        ani_matrix.iloc[j, i] = avg_value

# Convert the values to distance values 
distance_matrix = 100 - ani_matrix

# Convert the DataFrame to a NumPy array for extracting the upper triangle
ani_array = ani_matrix.to_numpy()

# Extracting only the upper triangle of the matrix (since ANI matrices are symmetric)
upper_triangle = ani_array[np.triu_indices_from(ani_array, k=1)]


# Plotting the histogram
plt.figure(figsize=(10, 6))
plt.hist(upper_triangle, bins=28, color='#3e7bb8', edgecolor='black')

# Set font size
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.xlabel('ANIb (%)', fontsize=16)
plt.ylabel('Frequency', fontsize=16)
plt.savefig('Outputs/histogram.png', dpi=300)
