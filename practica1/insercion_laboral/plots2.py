import pandas as pd
import os
import matplotlib.pyplot as plt

processed_data_dir = 'practica1/data/processed'
figures_dir = 'practica1/reports/figures'

os.makedirs(figures_dir, exist_ok=True)

degree_map = {
    '1511': 'GRADO EN ENFERMERÍA (1511)---CENTRO UNIVERSITARIO DE MÉRIDA',
    '1512': 'GRADO EN INGENIERÍA EN DISEÑO INDUSTRIAL Y DESARROLLO DE PRODUCTOS (1512)---CENTRO UNIVERSITARIO DE MÉRIDA',
    '1513': 'GRADO EN INGENIERÍA EN GEOMÁTICA Y TOPOGRAFÍA (1513)---CENTRO UNIVERSITARIO DE MÉRIDA',
    '1514': 'GRADO EN INGENIERÍA INFORMÁTICA EN TECNOLOGÍAS DE LA INFORMACIÓN (1514)---CENTRO UNIVERSITARIO DE MÉRIDA',
    '1515': 'GRADO EN INGENIERÍA TELEMÁTICA EN TELECOMUNICACIÓN (1515)---CENTRO UNIVERSITARIO DE MÉRIDA'
}

# Load and process each year and gender's CSV
def load_year_gender_data(year, gender):
    filename = f"processed_{year}_{gender}.csv"
    filepath = os.path.join(processed_data_dir, str(year), filename)
    
    # Check if the file exists before attempting to load it
    if os.path.exists(filepath):
        # Load the CSV into a pandas DataFrame
        df = pd.read_csv(filepath)
        
        # Add the 'year' and 'gender' columns to the DataFrame
        df['year'] = year
        df['gender'] = gender
        
        return df
    else:
        print(f"Warning: {filepath} does not exist.")
        return pd.DataFrame()

# empty list to collect data
all_data = []

degree_codes = ['1511', '1512', '1513', '1514', '1515']
years = ['2016_17', '2017_18', '2018_19', '2019_20', '2020_21'] 
genders = ['male', 'female', 'total']

# Loop through each degree code
for degree_code in degree_codes:
    # Loop through each year and gender to load the data for this degree
    for year in years:
        for gender in genders:
            gender_data = load_year_gender_data(year, gender)
            
            if not gender_data.empty:
                # Filter the data for this specific degree code and append
                degree_data = gender_data[gender_data['degree'] == int(degree_code)]
                all_data.append(degree_data)

# Concatenate all the DataFrames into a single DataFrame
consolidated_df = pd.concat(all_data, ignore_index=True)

# Convert 'mean' to numeric, '---' becomes NaN
consolidated_df['mean'] = pd.to_numeric(consolidated_df['mean'], errors='coerce')

# Plotting the evolution for each degree using both line and bar plots
for degree_code in degree_codes:
    degree_data = consolidated_df[consolidated_df['degree'] == int(degree_code)]
    
    # Prepare the data for plotting: mean per year and gender
    plot_data = degree_data.groupby(['year', 'gender'])['mean'].mean().unstack()  # Average mean per year and gender
    
    # Line plot
    plot_data.plot(kind='line', figsize=(10, 6), marker='o')  # Create a line plot with markers
    plt.title(f'Evolution of {degree_map.get(degree_code, f"Degree {degree_code}")} over the years (Line Plot)')
    plt.xlabel('Year')
    plt.ylabel('Mean')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.legend(title='Gender')
    plt.grid(True)
    
    # Save the line plot for this degree
    line_plot_filename = os.path.join(figures_dir, f"evolution_line_{degree_code}.png")
    plt.tight_layout()
    plt.savefig(line_plot_filename)  # Save the line plot to a file
    plt.close()  # Close the plot to free memory
    print(f"Line plot saved: {line_plot_filename}")
    
    # Bar plot
    plot_data.plot(kind='bar', figsize=(10, 6), stacked=False)
    plt.title(f'Evolution of {degree_map.get(degree_code, f"Degree {degree_code}")} over the years (Bar Plot)')
    plt.xlabel('Year')
    plt.ylabel('Mean')
    plt.xticks(rotation=45)
    plt.legend(title='Gender')
    plt.grid(True)
    
    # Save the bar plot for this degree
    bar_plot_filename = os.path.join(figures_dir, f"evolution_bar_{degree_code}.png")
    plt.tight_layout()
    plt.savefig(bar_plot_filename)  # Save the bar plot to a file
    plt.close()  # Close the plot to free memory
    print(f"Bar plot saved: {bar_plot_filename}")

    # Bubble plot for 'total' gender, using 'n_graduates' as bubble size
    total_gender_data = degree_data[degree_data['gender'] == 'total']
    
    # Ensure 'n_graduates' is a numeric column
    total_gender_data['n_graduates'] = pd.to_numeric(total_gender_data['n_graduates'], errors='coerce')
    
    # Prepare data for the bubble chart (x: year, y: mean, size: n_graduates)
    bubble_data = total_gender_data.groupby(['year'])[['mean', 'n_graduates']].mean()  # Average per year
    
    # Create the bubble chart
    plt.figure(figsize=(10, 6))
    plt.scatter(bubble_data.index, bubble_data['mean'], s=bubble_data['n_graduates'] / 10, alpha=0.5, c=bubble_data['mean'], cmap='viridis', edgecolors='w', linewidth=0.5)
    plt.title(f'Evolution of {degree_map.get(degree_code, f"Degree {degree_code}")} (Bubble Plot)')
    plt.xlabel('Year')
    plt.ylabel('Mean')
    plt.xticks(rotation=45)
    plt.colorbar(label='Mean')
    plt.grid(True)
    
    # Save the bubble plot for this degree
    bubble_plot_filename = os.path.join(figures_dir, f"evolution_bubble_{degree_code}.png")
    plt.tight_layout()
    plt.savefig(bubble_plot_filename)  # Save the bubble plot to a file
    plt.close()  # Close the plot to free memory
    print(f"Bubble plot saved: {bubble_plot_filename}")
