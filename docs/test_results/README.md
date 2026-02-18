# Reportes de tests (pytest-html)

Los archivos `test_results.html` y `test_results_gx.html` se generan con pytest-html. La tabla **Environment** y el **detalle de cada test** (filas expandibles, logs) se rellenan con JavaScript.

Si abres el HTML con doble clic (`file://`), el navegador puede no ejecutar ese script (en MAC) y verás las tablas vacías.

**Para ver toda la información** (Environment + detalle de tests), sirve la carpeta con un servidor HTTP local:

```bash
# Desde la raíz del repositorio:
make serve-report
```

Luego abre en el navegador:

- http://localhost:8080/test_results.html
- http://localhost:8080/test_results_gx.html

(O sin Make: `python3 -m http.server 8080 -d docs/test_results` y abre las URLs anteriores.)

Para cerrar el proceso presiona Ctrl + C
