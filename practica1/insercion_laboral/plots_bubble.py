import pandas as pd
import os
import matplotlib.pyplot as plt

processed_data_dir = 'practica1/data/processed'
figures_dir = 'practica1/reports/figures'

os.makedirs(figures_dir, exist_ok=True)

degree_map = {
    '1511': 'GRADO EN ENFERMERÍA',
    '1512': 'GRADO EN INGENIERÍA EN DISEÑO INDUSTRIAL Y DESARROLLO DE PRODUCTOS',
    '1513': 'GRADO EN INGENIERÍA EN GEOMÁTICA Y TOPOGRAFÍA',
    '1514': 'GRADO EN INGENIERÍA INFORMÁTICA EN TECNOLOGÍAS DE LA INFORMACIÓN',
    '1515': 'GRADO EN INGENIERÍA TELEMÁTICA EN TELECOMUNICACIÓN'
}

# Load and process each year and gender's CSV
def load_year_gender_data(year, gender):
    filename = f"processed_{year}_{gender}.csv"
    filepath = os.path.join(processed_data_dir, str(year), filename)
    
    if os.path.exists(filepath):
        df = pd.read_csv(filepath)
        df['year'] = year
        df['gender'] = gender
        return df
    else:
        print(f"Warning: {filepath} does not exist.")
        return pd.DataFrame()

all_data = []
degree_codes = ['1511', '1512', '1513', '1514', '1515']
years = ['2016_17', '2017_18', '2018_19', '2019_20', '2020_21']
genders = ['total']

for degree_code in degree_codes:
    for year in years:
        for gender in genders:
            gender_data = load_year_gender_data(year, gender)
            if not gender_data.empty:
                degree_data = gender_data[gender_data['degree'] == int(degree_code)]
                all_data.append(degree_data)

consolidated_df = pd.concat(all_data, ignore_index=True)

# Convert 'mean' to numeric, '---' becomes NaN
consolidated_df['mean'] = pd.to_numeric(consolidated_df['mean'], errors='coerce')
consolidated_df['n_graduates'] = pd.to_numeric(consolidated_df['n_graduates'], errors='coerce')

# Bubble plot for each degree
for degree_code in degree_codes:
    degree_data = consolidated_df[consolidated_df['degree'] == int(degree_code)]

    plt.figure(figsize=(10, 6))
    
    # Create scatter plot with bubble size proportional to n_graduates
    plt.scatter(
        degree_data['year'], 
        degree_data['mean'], 
        s=degree_data['n_graduates'] * 10,  # Scale bubble size
        alpha=0.6,
        edgecolors="k"
    )

    plt.title(f'Evolución del empleo y egresados en {degree_map.get(degree_code, f"Degree {degree_code}")}')
    plt.xlabel('Año')
    plt.ylabel('Tiempo medio en encontrar empleo')
    plt.xticks(rotation=45)
    plt.grid(True)

    # Save the bubble plot
    bubble_plot_filename = os.path.join(figures_dir, f"bubble_plot_{degree_code}.png")
    plt.tight_layout()
    plt.savefig(bubble_plot_filename)
    plt.close()
    print(f"Bubble plot saved: {bubble_plot_filename}")
