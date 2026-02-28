"""
Script para entrenar un modelo de clasificación utilizando la técnica con mejor rendimiento que fuera 
seleccionada durante la experimentación.
"""

#Importaciones generales
import pandas as pd
import mlflow
import mlflow.sklearn

# Importaciones para el preprocesamiento
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import RobustScaler
from sklearn.utils import resample

# Importaciones para la evaluación y experimentación
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import f1_score, recall_score, precision_score, accuracy_score
from mlflow.models import infer_signature
from sklearn.tree import DecisionTreeClassifier

def load_data(path):
    """
    Función para cargar los datos desde un archivo CSV

    Args:
        path (str): Ruta del archivo CSV

    Returns:
        X_train, X_test, y_train, y_test (pandas.DataFrame): Variables predictoras y variable objetivo para el conjunto de entrenamiento y prueba
    """
    df = pd.read_csv(path, sep=';')
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

#ToDo: Continuar desde aqui con el balanceo, modelado y guardado  con mlflow