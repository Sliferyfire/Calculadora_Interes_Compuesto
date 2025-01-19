# Calculadora de Inversión con Interés Compuesto

Este proyecto es una calculadora de inversión que utiliza **interés compuesto**. Fue desarrollada en Python utilizando PyQt6 para la interfaz gráfica y PyQtGraph para la representación visual de los resultados.

## Características

- Cálculo del **monto acumulado/deseado** al final de un periodo de tiempo especificado.
- Determinación del **capital inicial necesario** para alcanzar un monto deseado al final del periodo.
- Cálculos realizados mediante modelos discretos y continuos de capitalización.
- Representación gráfica del crecimiento del capital con respecto al tiempo.

## Requisitos del sistema

- **Python** 3.9 o superior.
- Paquetes requeridos:
  - `PyQt6`
  - `pyqtgraph`
  - `numpy`

## Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/tu_usuario/tu_repositorio.git
   cd tu_repositorio
   ```

2. Instala las dependencias:
   ```bash
   pip install PyQt6 pyqtgraph numpy
   ```

## Uso

Ejecuta el archivo principal para iniciar la aplicación:
```bash
python main.py
```

### Instrucciones:

1. Selecciona qué deseas calcular:
   - **Monto acumulado/deseado**.
   - **Capital inicial necesario**.
2. Ingresa los valores requeridos:
   - Monto deseado/acumulado o capital inicial.
   - Tasa de interés (en formato decimal).
   - Número de capitalizaciones por año.
   - Tiempo total (en años).
3. Haz clic en **Calcular** para ver los resultados.
4. Utiliza el botón **Limpiar** para reiniciar los campos.

La aplicación generará un gráfico que muestra la evolución del capital con respecto al tiempo.

## Estructura del proyecto

```
├── main.py           # Código principal del proyecto
├── README.md         # Este archivo
└── screenshot.png    # Captura de pantalla de la aplicación (agregar manualmente)
```

## Autor

- **[Aaron David Olguin]** - [sliferyfire@gmail.com]

