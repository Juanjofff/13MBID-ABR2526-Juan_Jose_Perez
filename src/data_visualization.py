import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def visualize_data(source: str = 'data/raw/bank-additional-full.csv',
    output: str = "docs/figures/") -> None:
    """ genera una serie de gráficos sobre los datos y los exporta 
    
    Args:
        source: ruta del archivo de datos
        output: ruta de la carpeta de salida
    """

    # Crear la carpeta de salida si no existe
    Path(output).mkdir(parents=True, exist_ok=True)

    # Leer los datos
    df = pd.read_csv(source, sep=';')

    # Gráfico 1: Distribución de la variable objetivo
    plt.figure(figsize=(6, 4))
    sns.countplot(x="y", data=df)
    plt.title("Distribución de la variable objetivo (suscripción al depósito)")
    plt.xlabel("¿Suscribió un depósito a plazo?")
    plt.ylabel("Cantidad de clientes")
    plt.savefig(output + "distribution_target.png")
    plt.close()

    # Grafico 2: Distribución de nivel educativo
    plt.figure(figsize=(6, 4))
    col = "education"
    order = df[col].value_counts().index
    sns.countplot(y=col, data=df, order=order)
    plt.title(f"Distribución de {col}")
    plt.xlabel("Cantidad")
    plt.ylabel(col)
    plt.savefig(output + f"distribution_of_{col}.png")
    plt.close()

    # Grafico 3: Distribución de la variable job
    plt.figure(figsize=(6, 4))
    col = "job"
    order = df[col].value_counts().index
    sns.countplot(y=col, data=df, order=order)
    plt.title(f"Distribución de {col}")
    plt.xlabel("Cantidad")
    plt.ylabel(col)
    plt.savefig(output + f"distribution_of_{col}.png")
    plt.close()

    # Grafico 4: Distribución de la variable marital
    plt.figure(figsize=(6, 4))
    col = "marital"
    order = df[col].value_counts().index
    sns.countplot(y=col, data=df, order=order)
    plt.title(f"Distribución de {col}")
    plt.xlabel("Cantidad")
    plt.ylabel(col)
    plt.savefig(output + f"distribution_of_{col}.png")
    plt.close()
   
if __name__ == "__main__":
    visualize_data()
