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
    add_expectation(
        "contact_values",
        df["contact"].isin(["cellular", "telephone"]).all(),
        "La columna 'contact' contiene valores no validos")
    add_expectation(
        "marital_values",
        df["marital"].isin(["divorced", "married", "single", "unknown"]).all(),
        "La columna 'marital' contiene valores no validos")
    add_expectation( 
        "month_values",
        df["month"].isin(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]).all(),
        "La columna 'month' contiene valores no validos")
    add_expectation(
        "day_of_week_values",
        df["day_of_week"].isin(["mon", "tue", "wed", "thu", "fri", "sat", "sun"]).all(),
        "La columna 'day_of_week' contiene valores no validos")

