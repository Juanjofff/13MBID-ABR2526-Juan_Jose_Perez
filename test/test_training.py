import pytest
import json
from pathlib import Path
import sys 

def test_training_metrics_regression(tmp_path):
    """
    Test para verificar que las métricas de entrenamiento son correctas
    """
    project_root = Path(__file__).resolve().parents[1]
    baseline_path = project_root / 'metrics' / 'train_metrics.json'
    if not baseline_path.exists():
        pytest.skip(f"No se encontró la baseline {baseline_path}. Ejecuta el entrenamiento para generarla.")
    
    # cargar métricas baseline
    with open(baseline_path, 'r') as f:
        baseline_metrics = json.load(f)
    
    # hacer importable src y cargar la función de entramiento 
    sys.path.insert(0, str(project_root / 'src'))
    from train_model import train_model
    
    # ejecutar entrenamiento con rutas aisladas (no sobreescribir baseline)
    data_path = project_root / 'data' / 'processed' / 'bank-processed.csv'
    model_path = tmp_path / 'decision_tree_model.pkl'
    preprocessor_path = tmp_path / 'preprocessor.pkl'
    metrics_path = tmp_path / 'train_metrics.json'

    _,_, metrics = train_model(data_path=data_path, model_output_path=model_path, preprocessor_output_path=preprocessor_path, metrics_output_path=metrics_path)
    
    # Comparar claves y valores con toleraancia pequeña
    assert set(metrics.keys()) == set(baseline_metrics.keys())
    atol = 1e-9
    for k in baseline_metrics.keys():
        assert metrics[k] == pytest.approx(baseline_metrics[k], rel=0, abs=atol), (f"Métrica {k} cambió: baseline={baseline_metrics[k]}, nueva={metrics[k]}")
