import pandas as pd

def test_great_expectations():
    """ Test de Great Expectations para el DataFrame de datos_banco
    
    """
    df = pd.read_csv('data/raw/bank-additional-full.csv', sep=';')

    results = {
        "success": True,
        "expectations": [],
        "statistics": {
            "success_count": 0, 
            "total_count": 0
            }
    }

    def add_expectation(expectation_name, condition, message=""):
        results["statistics"]["total_count"] += 1
        if condition:
            results["statistics"]["success_count"] += 1
            results["expectations"].append({
                "name": expectation_name,
                "success": True,
            })
        else:
            results["success"] = False
            results["expectations"].append({
                "name": expectation_name,
                "success": False,
                "message": message
            })
        
    # validaciones a verificar sobre los datos
    add_expectation(
        "age_range", 
        df["age"].between(18, 100).all(), 
        "La edad debe estar entre 18 y 100")
    add_expectation(
        "target_values",
        df["y"].isin(["yes", "no"]).all(),
        "La columna 'y' contiene valores no validos")

    #ToDo: Agregar mas validaciones, al menos 2

