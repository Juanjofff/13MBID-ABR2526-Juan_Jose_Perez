.PHONY: check_python check_virtualenv create_env serve-report

check_python:
	@echo "Se verifica instalación de python."
	@python3 --version >/dev/null 2>&1 || { echo >&2 "No se pudo iniciar Python, revisar instalación."; exit 1; }
	@echo "Verificación ok."

check_virtualenv: check_python
	@echo "Se verifica instalación de la librería venv."
	@python3 -c 'import venv' >/dev/null 2>&1 || { echo >&2 "No se encontró venv. Se debe instalar para seguir."; exit 1; }
	@echo "Verificación ok."
	
create_env: check_virtualenv
	@python3 -m venv .env --prompt 13MBID
	@echo "Se crea el entorno virtual."

create_requirements:
	@echo "Se crea el archivo de dependencias a instalar."
	echo "jupyter" >> config/requirements.txt
	echo "pandas" >> config/requirements.txt
	echo "numpy" >> config/requirements.txt
	echo "scikit-learn" >> config/requirements.txt
	echo "mlflow" >> config/requirements.txt
	echo "dvc" >> config/requirements.txt
	echo "ydata_profiling" >> config/requirements.txt
	echo "streamlit" >> config/requirements.txt
	echo "streamlit-ace" >> config/requirements.txt
	echo "pytest" >> config/requirements.txt
	echo "pandera" >> config/requirements.txt
	echo "great_expectations" >> config/requirements.txt
	echo "fastapi" >> config/requirements.txt
	echo "plotly" >> config/requirements.txt
	@echo "Archivo generado en el directorio config."
	@echo off

clean:
	@rm -rf .env
	@echo "Se eliminó el entorno virtual."

# Sirve los reportes HTML para ver Environment y detalle de tests (el JS no corre con file://).
serve-report:
	@echo "Sirviendo reportes en http://localhost:8080"
	@echo "Abre: http://localhost:8080/test_results.html  o  http://localhost:8080/test_results_gx.html"
	@echo "Detén el servidor con Ctrl+C."
	@python3 -m http.server 8080 -d docs/test_results