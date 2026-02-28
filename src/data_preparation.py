import pandas as pd
import numpy as np

INPUT_CSV = "data/raw/bank-additional-full.csv"
OUTPUT_CSV = "data/processed/bank-processed.csv"

def preprocess_data(input_csv: str = INPUT_CSV, output_csv: str = OUTPUT_CSV):
    """ Prepara los datos para el modelo
    
    """
    # Leer los datos
    df = pd.read_csv(input_csv, sep=';')

    # Adaptar nombres de columnas 
    df.columns = df.columns.str.replace(".", "_")

    # eliminar espacios en blanco al inicio/final en columnas de tipo objeto
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].str.strip()

    # transformar los valores 'unknown' en NaN
    df.replace('unknown', np.nan, inplace=True)

    # se elimina la columna 'default'
    df.drop(columns=['default'], inplace=True)

    # se hace un filtro para eliminar las filas con valores NaN
    df.dropna(inplace=True)

    # se hace un filtro para eliminar las filas duplicadas
    df.drop_duplicates(inplace=True)

    # Mapear la columna objetivo 'y' a valores binarios
    map = {
        'yes': 1,
        'no': 0
    }
    df['y'] = df['y'].map(map)

    # reindexar para índice consecutivo
    df.reset_index(drop=True, inplace=True)

    # save the processed dataset
    df.to_csv(output_csv, index=False)

    return df.shape

if __name__ == "__main__":
    rows, columns = preprocess_data()
    with open('docs/transformation.txt', 'w') as f:
        f.write("Transformaciones realizadas:")
        f.write("- Se reemplazaron los valores 'unknown' por NaN \n ")
        f.write("- Se eliminaron las filas con valores nulos \n ")
        f.write("- Se eliminaron las filas duplicadas \n ")
        f.write("- Se eliminaron la columna 'default' debido a la cantidad de valores desconocidos (nulos) \n ")
        f.write("- Se eliminaron espacios en blanco al inicio/final en cadenas \n ")
        f.write("- Se reindexó el DataFrame \n ")
        f.write("- Se mapearon los valores de la columna objetivo 'y' a valores binarios \n ")
        f.write(f"- Cantidad de filas finales: {rows} \n ")
        f.write(f"- Cantidad de columnas finales: {columns}")
