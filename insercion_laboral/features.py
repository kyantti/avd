import pandas as pd
import os

interim_dir = 'practica1/data/interim/'
processed_dir = 'practica1/data/processed/'

def create_tables_per_degree(directory):
    data = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                year = root.split('/')[-1]
                if 'female' in file.lower():
                    gender = 'female'
                elif 'male' in file.lower():
                    gender = 'male'
                else:
                    gender = 'total'
                
                print(f"Processing file: {file_path}, Year: {year}, Gender: {gender}")  # Debug print
                
                df = pd.read_csv(file_path)
                df['year'] = year
                df['gender'] = gender
                data.append(df)
    
    result_df = pd.concat(data)
    result_df = result_df[['degree', 'year', 'gender', 'mean', 'n_graduates']]
    
    degrees = result_df['degree'].unique()
    mean_tables = {}
    rentability_tables = {}
    
    for degree in degrees:
        degree_df = result_df[result_df['degree'] == degree].copy()
        degree_df.drop(columns=['degree'], inplace=True)
        
        # Create mean table
        mean_tables[degree] = degree_df
        
        # Create rentability table for 'total' gender
        rentability_df = degree_df[degree_df['gender'] == 'total'].copy()
        rentability_df['rentability'] = rentability_df['n_graduates'] / (rentability_df['mean'] + 1)
        rentability_tables[degree] = rentability_df[['year', 'rentability']]
    
    return mean_tables, rentability_tables

# Usage
mean_tables, rentability_tables = create_tables_per_degree(interim_dir)

# Save mean tables
for degree, table in mean_tables.items():
    print(f"Degree: {degree} - Mean Table")
    print(table.to_string(index=False))
    output_path = os.path.join(processed_dir, f'processed_mean_{degree}.csv')
    table.to_csv(output_path, index=False)

# Save rentability tables
for degree, table in rentability_tables.items():
    print(f"Degree: {degree} - Rentability Table")
    print(table.to_string(index=False))
    output_path = os.path.join(processed_dir, f'processed_rentability_{degree}.csv')
    table.to_csv(output_path, index=False)