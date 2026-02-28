# Reportes de tests (pytest-html)

Los archivos `test_results.html` y `test_results_gx.html` se generan con pytest-html. La tabla **Environment** y el **detalle de cada test** (filas expandibles, logs) se rellenan con JavaScript.

Si abres el HTML con doble clic (`file://`), el navegador puede no ejecutar ese script (en MAC) y verás las tablas vacías.

**Para ver toda la información** (Environment + detalle de tests), sirve la carpeta con un servidor HTTP local:

```bash
# Desde la raíz del repositorio:
make serve-report
```

Luego abre en el navegador:

- [http://localhost:8080/test_results.html](http://localhost:8080/test_results.html)
- [http://localhost:8080/test_results_gx.html](http://localhost:8080/test_results_gx.html)

(O sin Make: `python3 -m http.server 8080 -d docs/test_results` y abre las URLs anteriores.)

Para cerrar el proceso presiona Ctrl + C

---

## Tabla de evaluaciones

En la tabla de evaluaciones se detallan los tests generados en cada archivo.

### Archivo: `test/test_data_quality.py`


| Test                   | Descripción                                                                                                                                                                                                                                                                |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `test_esquema`         | Valida el esquema del DataFrame con Pandera: tipos (int, float, str) y nombres de las 21 columnas esperadas (age, job, marital, education, default, housing, loan, contact, month, day_of_week, duration, campaign, pdays, previous, poutcome, indicadores económicos, y). |
| `test_basico`          | Comprueba que el DataFrame no esté vacío, que no haya valores nulos y que tenga exactamente 21 columnas.                                                                                                                                                                   |
| `test_columna_contact` | Verifica que la columna `contact` tenga exactamente 2 valores únicos, que solo admita "cellular" y "telephone", y que no tenga nulos.                                                                                                                                      |
| `test_columna_marital` | Verifica que la columna `marital` tenga exactamente 4 valores únicos, que solo admita "divorced", "married", "single" y "unknown", y que no tenga nulos.                                                                                                                   |


### Archivo: `test/test_data_gx.py`


| Test                      | Expectativas incluidas | Descripción                                                                                                |
| ------------------------- | ---------------------- | ---------------------------------------------------------------------------------------------------------- |
| `test_great_expectations` | `age_range`            | La columna `age` debe estar en el rango [18, 100].                                                         |
|                           | `target_values`        | La columna `y` solo admite "yes" y "no".                                                                   |
|                           | `contact_values`       | La columna `contact` solo admite "cellular" y "telephone".                                                 |
|                           | `marital_values`       | La columna `marital` solo admite "divorced", "married", "single" y "unknown".                              |
|                           | `month_values`         | La columna `month` solo admite códigos de mes: jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec. |
|                           | `day_of_week_values`   | La columna `day_of_week` solo admite mon, tue, wed, thu, fri, sat, sun.                                    |


Los reportes HTML se generan con:

- `dvc repro test_data_quality` → `docs/test_results/test_results.html`
- `dvc repro test_data_gx` → `docs/test_results/test_results_gx.html`

