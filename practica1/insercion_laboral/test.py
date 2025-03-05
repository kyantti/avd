import pandas as pd
import matplotlib.pyplot as plt
import os

# Ruta base de los datos procesados
processed_dir = "practica1/data/processed/"
year = "2017_18"  # Cambia esto por el año que quieras analizar

# Leer el archivo total (puedes cambiar por 'male' o 'female')
file_path = os.path.join(processed_dir, year, f"processed_{year}_total.csv")

if os.path.exists(file_path):
    df = pd.read_csv(file_path)

    # Calcular la rentabilidad
    df["rentabilidad"] = df["n_graduates"] / (df["mean"] + 1)

    # Ordenar por rentabilidad
    df = df.sort_values(by="rentabilidad", ascending=False)

    # Gráfico de barras horizontales
    plt.figure(figsize=(10, 6))
    plt.barh(df["degree"], df["rentabilidad"], color="skyblue")
    plt.xlabel("Rentabilidad")
    plt.ylabel("Grado")
    plt.title(f"Rentabilidad de los Grados - {year}")
    plt.gca().invert_yaxis()  # Invertir el eje Y para que los más rentables estén arriba
    plt.grid(axis="x", linestyle="--", alpha=0.7)

    plt.show()
else:
    print("No se encontró el archivo.")
