"""
Script para entrenar un modelo de clasificación utilizando la técnica con mejor rendimiento que fuera 
seleccionada durante la experimentación.
"""

#Importaciones generales
import pandas as pd
import mlflow
import mlflow.sklearn
import joblib
import json
from pathlib import Path
import argparse

# Importaciones para el preprocesamiento
from pandas.io.formats.style import plt
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import RobustScaler
from sklearn.utils import resample

# Importaciones para la evaluación y experimentación
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import f1_score, recall_score, precision_score, accuracy_score, confusion_matrix, ConfusionMatrixDisplay
from mlflow.models import infer_signature
from sklearn.tree import DecisionTreeClassifier

# Logger
import logging

def load_data(path):
    """
    Función para cargar los datos desde un archivo CSV

    Args:
        path (str): Ruta del archivo CSV

    Returns:
        X_train, X_test, y_train, y_test (pandas.DataFrame): Variables predictoras y variable objetivo para el conjunto de entrenamiento y prueba
    """
    df = pd.read_csv(path, sep=',')
    # Se divide el dataset en variables predictoras y variable objetivo
    X = df.drop('y', axis=1)
    y = df['y']
    return train_test_split(X, y, test_size=0.2, random_state=42,stratify=y)

def create_preprocessor(X_train):
    """
    Función para crear el preprocesador

    Args:
        X_train (pandas.DataFrame): Variables predictoras para el conjunto de entrenamiento

    Returns:
        preprocessor (sklearn.pipeline.Pipeline): Preprocesador creado
    """
    # Se separan las columnas numéricas
    numerical_columns=X_train.select_dtypes(exclude='object').columns
    categorical_columns=X_train.select_dtypes(include='object').columns

    x_train = X_train.copy()
    int_columns = x_train.select_dtypes(include='int').columns
    for col in int_columns:
        x_train[col] = x_train[col].astype(float)
    
    #Actualizamos numerical cols
    numerical_columns = x_train.select_dtypes(exclude='object').columns

    # Pipeline para valores numéricos
    num_pipeline = Pipeline(steps=[
        ('RobustScaler', RobustScaler())
    ])

    # Pipeline para valores categóricos
    cat_pipeline = Pipeline(steps=[
        ('OneHotEncoder', OneHotEncoder(drop='first',sparse_output=False))
    ])

    # Se configuran los preprocesadores
    preprocessor_full = ColumnTransformer([
        ('num_pipeline', num_pipeline, numerical_columns),
        ('cat_pipeline', cat_pipeline, categorical_columns)
    ]).set_output(transform='pandas')

    return preprocessor_full, x_train

def balance_data(X, y, random_state=42):
    """
    Función para balancear los datos

    Args:
        X (pandas.DataFrame): Variables predictoras
        y (pandas.Series): Variable objetivo
        random_state (int): Semilla para el generador de números aleatorios
    """
    # Combinar los datos preprocesados con las etiquetas
    train_data = X.copy()
    train_data['target'] = y.reset_index(drop=True)

    # Separar por clase
    class_0 = train_data[train_data['target'] == 0]
    class_1 = train_data[train_data['target'] == 1]

    # Encontrar la clase minoritaria
    min_count = min(len(class_0), len(class_1))

    # Submuestreo balanceado - tomar una muestra igual al tamaño de la clase minoritaria
    class_0_balanced = resample(class_0, n_samples=min_count, random_state=random_state)
    class_1_balanced = resample(class_1, n_samples=min_count, random_state=random_state)

    # Combinar las clases balanceadas
    balanced_data = pd.concat([class_0_balanced, class_1_balanced])

    # Separar características y objetivo
    x_train_resampled = balanced_data.drop('target', axis=1)
    y_train_resampled = balanced_data['target']

    return x_train_resampled, y_train_resampled

def train_model(
    data_path: str = '../data/processed/bank-processed.csv',
    model_output_path: str = '../models/decision_tree_model.pkl',
    preprocessor_output_path: str = '../models/preprocessor.pkl',
    metrics_output_path: str = '../metrics/metrics.json',
):
    """
    Método principal para entrenar el modelo de clasificación

    Args:
        data_path (str): Ruta del archivo CSV con los datos
        model_output_path (str): Ruta de salida para el modelo
        preprocessor_output_path (str): Ruta de salida para el preprocesador
        metrics_output_path (str): Ruta de salida para las métricas
    """
    mlflow.set_tracking_uri("file:../mlruns")
    mlflow.set_experiment("Proyecto 13MBID-ABR2526 - Producción")

    with mlflow.start_run(run_name="DecisionTree Producción"):
        logging.info("Iniciando entrenamiento del modelo de clasificación")
        logging.info("Cargando datos...")
        X_train, X_test, y_train, y_test = load_data(data_path)

        logging.info("Crendo preprocesador...")
        preprocessor, X_train_converted = create_preprocessor(X_train)
        X_test = X_test.copy()

        # Convertir columnas enteras en X_test también
        int_columns = X_test.select_dtypes(include=['int64','int32']).columns
        for col in int_columns:
            X_test[col] = X_test[col].astype('float64')

        logging.info("Preprocesando datos...")
        X_train_prep = preprocessor.fit_transform(X_train_converted)
        X_test_prep = preprocessor.transform(X_test)

        logging.info("Balanceando datos...")
        x_train_balanced, y_train_balanced = balance_data(X_train_prep, y_train)

        logging.info("Tamaño original: %s", len(X_train_prep))
        logging.info("Tamaño balanceado: %s", len(x_train_balanced))
        logging.info("Distribución: %s", y_train_balanced.value_counts().to_dict())

        logging.info("Entrenando modelo DecisionTree...")
        model = DecisionTreeClassifier(max_depth=10, random_state=42)
        model.fit(x_train_balanced, y_train_balanced)

        logging.info("Evaluando modelo...")
        y_pred = model.predict(X_test_prep)

        # Crear pipeline completo
        full_pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('classifier', model)
        ])

        # crear signatures y ejemplos de entrada 
        raw_info_example = X_train.iloc[:5]
        preprocessed_info_example = X_train_prep.iloc[:5]

        # Signature para el pipeline completo
        pipeline_signature = infer_signature(
            X_train, # Datos de entrada sin procesar
            y_pred, # Predicciones del modelo
        )

        # Signature para el preprocesador
        preprocessor_signature = infer_signature(
            X_train, # Datos de entrada sin procesar
            X_train_prep, # Datos procesados
        )

        # Signature para el modelo
        model_signature = infer_signature(
            X_train_prep, # Datos procesados
            y_pred, # Predicciones 
        )

        # Calcular métricas 
        metrics = {
            "f1_score": f1_score(y_test, y_pred),
            "recall_score": recall_score(y_test, y_pred),
            "precision_score": precision_score(y_test, y_pred),
            "accuracy_score": accuracy_score(y_test, y_pred),
        }

        # Matriz de confusión
        cm = confusion_matrix(y_test, y_pred)

        # Registrar parámetros 
        mlflow.log_params({
            "model_type": "DecisionTreeClassifier",
            "criterion": model.criterion,
            "max_depth": model.max_depth,
            "min_samples_split": model.min_samples_split,
            "min_samples_leaf": model.min_samples_leaf,
            "balancing_method": "undersampling",
            "train_samples": len(x_train_balanced),
            "test_samples": len(X_test_prep),
            "random_state": 42,
        })

        # Registrar métricas 
        mlflow.log_metrics(metrics)
        
        # Registrar matriz de confusión
        fig, ax = plt.subplots(figsize=(8, 6))
        ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['No', 'Yes']).plot(ax=ax)
        plt.title('Confusion Matrix - Production Model')
        mlflow.log_figure(fig, 'confusion_matrix.png')
        plt.close(fig)

        # Registrar pipeline completo
        mlflow.sklearn.log_model(
            sk_model=full_pipeline,
            name="pipeline",
            signature=pipeline_signature
        )

        # Registrar preprocesador
        mlflow.sklearn.log_model(
            sk_model=preprocessor,
            name="preprocessor",
            signature=preprocessor_signature
        )

        # Registrar modelo
        mlflow.sklearn.log_model(
            sk_model=model,
            name="classifier",
            signature=model_signature
        )

        logging.info("Modelo registrado en MLFlow con el id de ejecución %s", mlflow.active_run().info.run_id)

        # Guardar modelo localmente
        logging.info("Guardando modelo...")
        Path(model_output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(preprocessor_output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(metrics_output_path).parent.mkdir(parents=True, exist_ok=True)

        joblib.dump(model, model_output_path)
        joblib.dump(preprocessor, preprocessor_output_path)
        with open(metrics_output_path, 'w') as f:
            json.dump(metrics, f, indent=2)

        return model, preprocessor, metrics

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Entrenar modelo de producción")
    parser.add_argument(
        "--data_path", 
        type=str, 
        default="data/processed/bank-processed.csv", 
        help="Ruta del archivo de datos procesados"
    )
    parser.add_argument(
        "--model_output_path",
        type=str,
        default="models/decision_tree_model.pkl",
        help="Ruta de salida para el modelo"
    )
    parser.add_argument(
        "--preprocessor_output_path",
        type=str,
        default="models/preprocessor.pkl",
        help="Ruta de salida para el preprocesador"
    )
    parser.add_argument(
        "--metrics_output_path",
        type=str,
        default="metrics/train_metrics.json",
        help="Ruta de salida para las métricas"
    )
    args = parser.parse_args()
    train_model(
        data_path=args.data_path,   
        model_output_path=args.model_output_path,
        preprocessor_output_path=args.preprocessor_output_path,
        metrics_output_path=args.metrics_output_path
    )