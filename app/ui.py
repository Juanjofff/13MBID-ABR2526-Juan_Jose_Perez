import sys
from pathlib import Path

# Asegurar que el raíz del proyecto esté en el path (para streamlit run app/ui.py)
_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

import streamlit as st
import requests
import plotly.graph_objects as go

from app.main import PredictionRequest

#Configuración de la página
st.set_page_config(
    page_title="Predicción de suscripción bancaria",
    page_icon=":money_with_wings:",
    layout="wide"
)

#Título y descripción
st.title("Predicción de suscripción a depósito a plazo fijo")
st.markdown("""
Esta aplicación utiliza un modelo de Machine Learning para predecir si un cliente aceptará la oferta de un depósito a plazo fijo.
""")

# URL de la API
API_URL = st.sidebar.text_input("URL de la API", value="http://localhost:8000")

# Verificar el estado de la API
st.sidebar.markdown("---")
st.sidebar.subheader("Estado de la API")

try:
    health_response = requests.get(f"{API_URL}/health", timeout=2)
    if health_response.status_code == 200:
        health_data = health_response.json()
        st.sidebar.success(f"Api Conectada")
        st.sidebar.json(health_data)
    else:
        st.sidebar.error(f"Error al verificar el estado de la API: {health_response.status_code}")
except requests.exceptions.RequestException as e:
    st.sidebar.error(f"Error al verificar el estado de la API: {e}")

# Crear pestañas 
tab1, tab2 = st.tabs(["Predicción Individual", "Información del Modelo"])

# Pestaña 1: Predicción Individual
with tab1:
    st.subheader("Predicción Individual")
    st.write("Ingresa los datos del cliente para hacer una predicción.")
    with st.form("prediction_form"):
        age = st.number_input("Edad", min_value=18, max_value=100, value=30)
        job = st.selectbox("Trabajo", ["admin.", "blue-collar", "entrepreneur", "housemaid", "management", "retired", "self-employed", "services", "student", "technician", "unemployed", "unknown"])
        marital = st.selectbox("Estado Civil", ["single", "married", "divorced", "unknown"])
        education = st.selectbox("Educación", ["basic.4y", "basic.6y", "basic.9y", "high.school", "university.degree", "unknown"])
        housing = st.selectbox("¿Tiene préstamo hipotecario?", ["yes", "no", "unknown"])
        loan = st.selectbox("¿Tiene préstamo personal?", ["yes", "no", "unknown"])
        contact = st.selectbox("Tipo de contacto", ["cellular", "telephone"])
        # Meses que el modelo vio en entrenamiento (dataset bank: apr, aug, dec, jul, jun, mar, may, nov, oct, sep)
        month = st.selectbox("Mes del último contacto", ["apr", "aug", "dec", "jul", "jun", "mar", "may", "nov", "oct", "sep"])
        day_of_week = st.selectbox("Día de la semana del último contacto", ["mon", "tue", "wed", "thu", "fri"])
        duration = st.number_input("Duración del último contacto en segundos", min_value=0, value=100)
        campaign = st.number_input("Número de contactos en esta campaña", min_value=0, value=1)
        previous = st.number_input("Número de contactos previos a esta campaña", min_value=0, value=0)
        poutcome = st.selectbox("Resultado de la campaña anterior", ["failure", "nonexistent", "success"])
        emp_var_rate = st.number_input("Tasa de variación del empleo", min_value=-100, max_value=100, value=0)
        cons_price_idx = st.number_input("Índice de precios al consumidor", min_value=0, value=100)
        cons_conf_idx = st.number_input("Índice de confianza del consumidor", min_value=0, value=100)

        euribor3m = st.number_input("Tasa Euribor a 3 meses", min_value=0, value=100)
        nr_employed = st.number_input("Número de empleados", min_value=0, value=100)
        contacted_before = st.selectbox("¿Ha sido contactado antes?", ["yes", "no"])

        submit_button = st.form_submit_button("Hacer Predicción")

        if submit_button:
            with st.spinner("Haciendo predicción..."):
                try:
                    prediction_request = PredictionRequest(
                        age=age,
                        job=job,
                        marital=marital,
                        education=education,
                        housing=housing,
                        loan=loan,
                        contact=contact,
                        month=month,
                        day_of_week=day_of_week,
                        duration=duration,
                        campaign=campaign,
                        previous=previous,
                        poutcome=poutcome,
                        emp_var_rate=emp_var_rate,
                        cons_price_idx=cons_price_idx,
                        cons_conf_idx=cons_conf_idx,
                        euribor3m=euribor3m,
                        nr_employed=nr_employed,
                        contacted_before=contacted_before
                    )
                    prediction_response = requests.post(f"{API_URL}/predict", json=prediction_request.model_dump(), timeout=10)
                    if prediction_response.status_code == 200:
                        prediction_data = prediction_response.json()
                        st.success("Predicción realizada correctamente")
                        st.json(prediction_data)
                        st.plotly_chart(go.Figure().add_trace(go.Bar(x=list(prediction_data['probability'].keys()), y=list(prediction_data['probability'].values()))))
                    else:
                        st.error(f"Error al hacer la predicción: {prediction_response.status_code}")
                        st.error(prediction_response.text)
                except Exception as e:
                    st.error(f"Error al hacer la predicción: {e}")
                    st.exception(e)

# Pestaña 2: Información del Modelo
with tab2:
    st.subheader("Información del Modelo")
    st.markdown("""
    ### Características del Modelo
    Este modelo de Machine Learning está diseñado para predecir si un cliente bancario suscribirá a un depósito a plazo fijo basándose en:

    #### Variables de Entrada
    - **age**: Edad del cliente
    - **job**: Trabajo del cliente
    - **marital**: Estado civil del cliente
    - **education**: Nivel educativo del cliente
    - **housing**: ¿Tiene préstamo hipotecario?
    - **loan**: ¿Tiene préstamo personal?
    - **contact**: Tipo de contacto
    - **month**: Mes del último contacto
    - **day_of_week**: Día de la semana del último contacto
    - **duration**: Duración del último contacto en segundos
    - **campaign**: Número de contactos en esta campaña
    - **previous**: Número de contactos previos a esta campaña
    - **poutcome**: Resultado de la campaña anterior
    - **emp_var_rate**: Tasa de variación del empleo
    - **cons_price_idx**: Índice de precios al consumidor
    - **cons_conf_idx**: Índice de confianza del consumidor
    - **euribor3m**: Tasa Euribor a 3 meses
    - **nr_employed**: Número de empleados
    - **contacted_before**: ¿Ha sido contactado antes?

    #### Variable de Salida
    - **prediction**: Predicción de si el cliente suscribirá a un depósito a plazo fijo
    - **probability**: Probabilidad de que el cliente suscribirá a un depósito a plazo fijo
    - **model_info**: Información del modelo



    """)
