import pandas as pd
import matplotlib.pyplot as plt
import os

# Define the directory containing the processed rentability files
processed_data_dir = 'practica1/data/processed'

# Define the degree codes and their corresponding file names
degree_files = {
    '1511': 'processed_rentability_1511.csv',
    '1512': 'processed_rentability_1512.csv',
    '1513': 'processed_rentability_1513.csv',
    '1514': 'processed_rentability_1514.csv',
    '1515': 'processed_rentability_1515.csv'
}

# Initialize a dictionary to store the data for each degree
rentability_data = {}

# Load the data for each degree
for degree, filename in degree_files.items():
    filepath = os.path.join(processed_data_dir, filename)
    if os.path.exists(filepath):
        df = pd.read_csv(filepath)
        rentability_data[degree] = df
    else:
        print(f"Warning: {filepath} does not exist.")

# Plot the rentability evolution for each degree
plt.figure(figsize=(12, 8))

for degree, df in rentability_data.items():
    plt.plot(df['year'], df['rentability'], marker='o', label=f'Degree {degree}')

plt.title('Evolution of Rentability for Each Degree Through the Years')
plt.xlabel('Year')
plt.ylabel('Rentability')
plt.xticks(rotation=45)
plt.legend(title='Degree')
plt.grid(True)
plt.tight_layout()

# Save the plot to a file
output_filepath = os.path.join(processed_data_dir, 'rentability_evolution.png')
plt.savefig(output_filepath)
plt.show()

print(f"Plot saved: {output_filepath}")