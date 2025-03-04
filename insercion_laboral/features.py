import pandas as pd
import os

# Base directories
interim_dir = "practica1/data/interim/"
processed_dir = "practica1/data/processed/"

# Keep just degree and mean
for year in os.listdir(interim_dir):
    year_dir = os.path.join(interim_dir, year)
    if os.path.isdir(year_dir):  
        processed_year_dir = os.path.join(processed_dir, year)
        os.makedirs(processed_year_dir, exist_ok=True)

        for gender in ['female', 'male', 'total']:
            file_path = os.path.join(year_dir, f"filtered_{year}_{gender}.csv")
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                df = df[['degree', 'mean', 'n_graduates']]
                processed_file_path = os.path.join(processed_year_dir, f"processed_{year}_{gender}.csv")
                df.to_csv(processed_file_path, index=False, encoding="utf-8")
                print(f"File saved: {processed_file_path}")
