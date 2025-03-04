# This module reads the raw data and prepares the pre-processed dataset

import pandas as pd
import os

raw_dir = "practica1/data/raw/"
interim_dir = "practica1/data/interim/"

def save_dataframe(df, filename):
    if not df.empty:
        df.to_csv(filename, index=False, encoding="utf-8")
        print(f"Archivo guardado: {filename}")

def process_file(file_path, sheet_name):
    # Extract the year from the file name (e.g., "il_2017_18_titulacion.xlsx" -> "2017_18")
    year = os.path.basename(file_path).split('_')[1] + '_' + os.path.basename(file_path).split('_')[2]

    # Create a directory for the year if it doesn't exist
    year_dir = os.path.join("practica1/data/interim", year)
    if not os.path.exists(year_dir):
        os.makedirs(year_dir)

    # Read the Excel sheet
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)

    # Filter rows based on the third column values
    df_merida = df[df[2].astype(str).str.contains("1511|1512|1513|1514|1515", na=False, case=False)]

    # Initialize lists for Male, Female, and Total rows
    gender_a_rows = []
    gender_b_rows = []
    gender_c_rows = []

    # Iterate through filtered rows in steps of 3 to get Male, Female, and Total
    for index in df_merida.index:
        degree_code = ''.join(filter(str.isdigit, str(df.iloc[index, 2])))  # Keep only digits
        gender_a_row = df.iloc[index].tolist()[2:]  
        gender_a_row[0] = degree_code
        gender_a_rows.append(gender_a_row)
        
        # Female row
        if index + 1 < len(df):
            gender_b = df.iloc[index + 1].copy().tolist()[2:]
            gender_b[0] = degree_code
            gender_b_rows.append(gender_b)
        
        # Total row
        if index + 2 < len(df):
            gender_c = df.iloc[index + 2].copy().tolist()[2:]
            gender_c[0] = degree_code
            gender_c_rows.append(gender_c)

    # Define column headers
    headers = ["degree", "gender", "mean", "std_deviation", "valid_answers", "n_graduates", "+-error"]

    # Convert the lists to DataFrames
    df_male = pd.DataFrame(gender_a_rows, columns=headers)
    df_female = pd.DataFrame(gender_b_rows, columns=headers)
    df_total = pd.DataFrame(gender_c_rows, columns=headers)

    # Save each DataFrame in the year directory
    save_dataframe(df_male, os.path.join(year_dir, f"filtered_{year}_male.csv"))
    save_dataframe(df_female, os.path.join(year_dir, f"filtered_{year}_female.csv"))
    save_dataframe(df_total, os.path.join(year_dir, f"filtered_{year}_total.csv"))

# Get all .xlsx files in the 'practica1/data/' directory
file_paths = [os.path.join(raw_dir, filename) for filename in os.listdir(raw_dir) if filename.endswith('.xlsx')]

# Process each file
for file_path in file_paths:
    process_file(file_path, sheet_name="P9")
