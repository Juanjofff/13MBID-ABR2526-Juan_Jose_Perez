from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import os
import json
from typing import Dict, Any
import joblib

app = FastAPI(
    title="Modelo de clasificación de Clientes Bancarios",
    description="API para predecir si un cliente aceptará la oferta de un depósito a plazo",
    version="1.0.0"
)

class PredictionRequest(BaseModel):
    age: int
    job: str
    marital: str
    education: str
    housing: str
    loan: str
    contact: str
    month: str
    day_of_week: str
    duration: int
    campaign: int
    previous: int
    poutcome: str
    emp_var_rate: float
    cons_price_idx: float
    cons_conf_idx: float
    euribor3m: float
    nr_employed: float
    contacted_before: str

    class Config:
        schema_extra = {
            "example": {
                "age": 33,
                "job": "admin.",
                "marital": "single",
                "education": "university.degree",
                "housing": "no",
                "loan": "no",
                "contact": "cellular",
                "month": "apr",
                "day_of_week": "thu",
                "duration": 298,
                "campaign": 4,
                "previous": 0,
                "poutcome": "nonexistent",
                "emp_var_rate": -1.8,
                "cons_price_idx": 93.075,
                "cons_conf_idx": -47.1,
                "euribor3m": 1.41,
                "nr_employed": 5099.1,
                "contacted_before": "no"
            }
        }

class PredictionResponse(BaseModel):
    prediction: str  # "no" o "yes"
    probability: Dict[str, float]  # {"no": p_no, "yes": p_yes}
    model_info: Dict[str, Any]

#CARGAR EL MODELO Y EL PREPROCESADOR AL INICIAR LA APLICACIÓN
MODEL_PATH = "models/decision_tree_model.pkl"
PREPROCESSOR_PATH = "models/preprocessor.pkl"

try:
    model = joblib.load(MODEL_PATH)
    preprocessor = joblib.load(PREPROCESSOR_PATH)
    print("Modelo y preprocesador cargados correctamente")
except Exception as e:
    model = None
    preprocessor = None
    print(f"Error al cargar el modelo o el preprocesador: {e}")
    raise HTTPException(status_code=500, detail="Error al cargar el modelo o el preprocesador")

#DEFINIR LA RUTA DE LA API
@app.get("/")
def root():
    return {"message": "API para predecir si un cliente aceptará la oferta de un depósito a plazo"}

#DEFINIR LA RUTA DE LA API PARA VER EL ESTADO DE LA API
@app.get("/health")
def health():
    return {"status": "healthy"}

#DEFINIR LA RUTA DE LA API PARA HACER LAS PREDICCIONES
@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """ 
    Realiza una predicción utilizando un modelo cargado.
    """
    # Convertir la solicitud a un DataFrame
    if model is None or preprocessor is None:
        raise HTTPException(status_code=500, detail="Error al cargar el modelo o el preprocesador")
    try:
        input_data = pd.DataFrame([request.model_dump()])
        input_data_prep = preprocessor.transform(input_data)
        pred = model.predict(input_data_prep)[0]
        pred_label = "yes" if int(pred) == 1 else "no"
        probs = model.predict_proba(input_data_prep)[0]
        probability = {"no": float(probs[0]), "yes": float(probs[1])}
        model_info = {"model_type": type(model).__name__}
        return PredictionResponse(prediction=pred_label, probability=probability, model_info=model_info)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al hacer la predicción: {e}")
    