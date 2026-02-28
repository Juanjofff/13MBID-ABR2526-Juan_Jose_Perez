import pandas as pd
import pytest
from pandera.pandas import DataFrameSchema, Column
from datetime import datetime

@pytest.fixture
def datos_banco():
    """ Fixture para cargar los datos del banco desde un archivo csv 
    
    Returns:
        pd.DataFrame: DataFrame que contiene los datos del banco
    """
    df = pd.read_csv('data/raw/bank-additional-full.csv', sep=';')
    return df

def test_esquema(datos_banco):
    """ Test de Esquema para el DataFrame de datos_banco
    
    Args:
        datos_banco(pd.DataFrame): DataFrame que contiene los datos del banco
    """
    df = datos_banco
    schema = DataFrameSchema( {
        "age": Column(int, nullable=False),
        "job": Column(str, nullable=False),
        "marital": Column(str, nullable=False),
        "education": Column(str, nullable=False),
        "default": Column(str, nullable=True),
        "housing": Column(str, nullable=False),
        "loan": Column(str, nullable=False),
        "contact": Column(str, nullable=False),
        "month": Column(str, nullable=False),
        "day_of_week": Column(str, nullable=False),
        "duration": Column(int, nullable=False),
        "campaign": Column(int, nullable=False),
        "pdays": Column(int, nullable=False),
        "previous": Column(int, nullable=False),
        "poutcome": Column(str, nullable=False),
        "emp.var.rate": Column(float, nullable=False),
        "cons.price.idx": Column(float, nullable=False),
        "cons.conf.idx": Column(float, nullable=False),
        "euribor3m": Column(float, nullable=False),
        "nr.employed": Column(float, nullable=False),
        "y": Column(str, nullable=False)} )

    schema.validate(df)

def test_basico(datos_banco):
    """ Test de Basico para el DataFrame de datos_banco
    
    Args:
        datos_banco(pd.DataFrame): DataFrame que contiene los datos del banco
    """
    df = datos_banco

    # Verificar que el DataFrame no este vacio
    assert not df.empty, "El DataFrame esta vacio"

    # Verificar nulos
    assert df.isnull().sum().sum() == 0, "El DataFrame tiene valores nulos"

    # Verificar duplicados
    #assert df.duplicated().sum() == 0, "El DataFrame tiene valores duplicados"

    # Verificar cantidad de columnas
    assert df.shape[1] == 21, "El DataFrame tiene 21 columnas"

def test_columna_contact(datos_banco):
    """ Test de la columna contact para el DataFrame de datos_banco
    
    Args:
        datos_banco(pd.DataFrame): DataFrame que contiene los datos del banco
    """
    df = datos_banco
    assert df["contact"].nunique() == 2, "La columna contact debe tener exactamente 2 valores únicos"
    assert df["contact"].isin(["cellular", "telephone"]).all(), "La columna contact solo admite 'cellular' y 'telephone'"
    assert df["contact"].isnull().sum() == 0, "La columna contact no debe tener nulos"

def test_columna_marital(datos_banco):
    """ Test de la columna marital para el DataFrame de datos_banco
    
    Args:
        datos_banco(pd.DataFrame): DataFrame que contiene los datos del banco
    """
    df = datos_banco
    assert df["marital"].nunique() == 4, "La columna marital debe tener exactamente 4 valores únicos"
    assert df["marital"].isin(["divorced", "married", "single", "unknown"]).all(), "La columna marital solo admite divorced, married, single, unknown"
    assert df["marital"].isnull().sum() == 0, "La columna marital no debe tener nulos"
