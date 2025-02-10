import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGridLayout, QLineEdit, QSpinBox, QDoubleSpinBox
from PyQt6.QtGui import QIntValidator, QDoubleValidator
from PyQt6.QtCore import Qt
import pyqtgraph as pg
import math
import numpy as np

# Clase de la interfaz
class MainWindow(QWidget):
    calcularMonto = True
    def __init__(self):
        super().__init__()

        # Deinicion del titulo y dimensiones de la ventana
        self.setWindowTitle("Calculadora de inversion con interes compuesto")
        self.setGeometry(100, 100, 800, 600)  # x, y, ancho, alto

        # Definicion del layout utilizado
        layout = QGridLayout()
        self.setLayout(layout)

        ### Botones para decidir que calcular
        # Boton para calcular el monto acumulado al final del tiempo total que se especificó.
        self.botonCalcularMonto = QPushButton(self)
        self.botonCalcularMonto.setText("Calcular Monto deseado/acumulado")
        self.botonCalcularMonto.clicked.connect(self.deshabilitarMonto)
        self.botonCalcularMonto.setEnabled(False)
        layout.addWidget(self.botonCalcularMonto, 0, 0, alignment=Qt.AlignmentFlag.AlignRight)

        # Boton para calcular el capital inicial necesario (P) para obtener al final del periodo de
        # tiempo un monto acumulado deseado.
        self.botonCalcularCapital = QPushButton(self)
        self.botonCalcularCapital.setText("Calcular Capital inicial necesario")
        self.botonCalcularCapital.clicked.connect(self.deshabilitarCapital)
        self.botonCalcularCapital.setEnabled(True)
        layout.addWidget(self.botonCalcularCapital, 0, 1, alignment=Qt.AlignmentFlag.AlignLeft)

        #### Formulario para capturar los datos necesarios
        # Label e imput para capturar el monto deseado o acumuldo
        layout.addWidget(QLabel("Monto deseado o acumulado: "), 1, 0)
        self.inputMontoDeseado = QLineEdit(self)
        self.inputMontoDeseado.setValidator(QDoubleValidator())
        self.inputMontoDeseado.setEnabled(False)
        layout.addWidget(self.inputMontoDeseado, 1, 1)

        # Label e imput para capturar el capital inicial
        layout.addWidget(QLabel("Capital inicial: "), 2, 0)
        self.inputCapitalInicial = QLineEdit(self)
        self.inputCapitalInicial.setValidator(QDoubleValidator())
        self.inputCapitalInicial.setEnabled(True)
        layout.addWidget(self.inputCapitalInicial, 2, 1)

        # Label e imput para capturar la tasa de interes
        layout.addWidget(QLabel("Tasa de interes en decimal: "), 3, 0)
        self.inputTasaInteres = QDoubleSpinBox(self)
        self.inputTasaInteres.setMinimum(0)
        self.inputTasaInteres.setMaximum(1)
        self.inputTasaInteres.setSingleStep(0.01)
        layout.addWidget(self.inputTasaInteres, 3, 1)

        # Label e imput para capturar las capitalizaciones
        layout.addWidget(QLabel("Capitalizaciones: "), 4, 0)
        self.inputCapitalizaciones = QSpinBox(self)
        self.inputCapitalizaciones.setMinimum(0)
        self.inputCapitalizaciones.setMaximum(1000)
        self.inputCapitalizaciones.setSingleStep(1)
        layout.addWidget(self.inputCapitalizaciones, 4, 1)

        # Label e imput para capturar el tiempo total en años
        layout.addWidget(QLabel("Tiempo total en años: "), 5, 0)
        self.inputTiempoTotal = QSpinBox(self)
        self.inputTiempoTotal.setMinimum(0)
        self.inputTiempoTotal.setMaximum(1000)
        self.inputTiempoTotal.setSingleStep(1)
        layout.addWidget(self.inputTiempoTotal, 5, 1)

        # Boton para calcular lo especificado.
        self.botonCalcular = QPushButton(self)
        self.botonCalcular.setText("Calcular")
        self.botonCalcular.clicked.connect(self.calcular)
        layout.addWidget(self.botonCalcular, 6, 0, 1, 2)

        # Boton para resetear los valores de los inputs
        self.botonResetear = QPushButton(self)
        self.botonResetear.setText("Limpiar")
        self.botonResetear.clicked.connect(self.resetearInputs)
        layout.addWidget(self.botonResetear, 7, 0, 1, 2)

        # Label para mostrar el resultado mediante el modelo discreto
        self.labelResultado = QLabel(self)
        self.labelResultado.setText("...")
        layout.addWidget(self.labelResultado, 8, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)

        # Label para mostrar el resultado mediante el modelo continuo
        self.labelResultadoC = QLabel(self)
        self.labelResultadoC.setText("...")
        layout.addWidget(self.labelResultadoC, 8, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignRight)

        # Creacion del grafico
        # Creación del gráfico
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setTitle("Capital con respecto al tiempo")
        self.plot_widget.setLabel("left", "Monto acumulado", color="white")
        self.plot_widget.setLabel("bottom", "Tiempo", color="white")
        self.plot_widget.enableAutoRange(True, True)  # Ajustar automáticamente la escala

        # Agregar el gráfico al layout
        layout.addWidget(self.plot_widget, 9, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)

    # Funcion para deshabilitar el campo de Monto inicial
    def deshabilitarMonto(self):
        self.botonCalcularMonto.setEnabled(False)
        self.botonCalcularCapital.setEnabled(True)
        self.inputMontoDeseado.setEnabled(False)
        self.inputCapitalInicial.setEnabled(True)
        self.calcularMonto = True
        self.resetearInputs()

    # Funcion para deshabilitar el campo de Capital inicial
    def deshabilitarCapital(self):
        self.botonCalcularMonto.setEnabled(True)
        self.botonCalcularCapital.setEnabled(False)
        self.inputMontoDeseado.setEnabled(True)
        self.inputCapitalInicial.setEnabled(False)
        self.calcularMonto = False
        self.resetearInputs()

    # Funcion para calcular el monto acumulado al final del tiempo total que se especificó.
    def calcular(self):
        try:
            tasaInteres = float(self.inputTasaInteres.value())
            capitalizaciones = float(self.inputCapitalizaciones.value())
            tiempoAnios = float(self.inputTiempoTotal.value())

            if self.calcularMonto:
                capitalInicial = float(self.inputCapitalInicial.text())

                # Modelo discreto
                resultadoMonto = capitalInicial * ((1 + (tasaInteres / capitalizaciones)) ** (capitalizaciones * tiempoAnios))
                montoRedondeado = round(resultadoMonto, 2)
                self.labelResultado.setText(f"El monto acumulado/deseado es: (discreto) ${montoRedondeado}")

                # Modelo continuo
                resultadoMontoC = capitalInicial * (math.e ** (tasaInteres * tiempoAnios))
                montoRedondeadoC = round(resultadoMontoC, 2)
                self.labelResultadoC.setText(f"El monto acumulado/deseado es: (continuo) ${montoRedondeadoC}")

                # Generar datos para la gráfica (exponencial)
                tiempos = np.linspace(0, tiempoAnios, 100)
                montos_discretos = capitalInicial * ((1 + (tasaInteres / capitalizaciones)) ** (capitalizaciones * tiempos))
                montos_continuos = capitalInicial * (math.e ** (tasaInteres * tiempos))

                # Limpiar y graficar
                self.plot_widget.clear()
                self.plot_widget.plot(tiempos, montos_discretos, pen=pg.mkPen(color='b', width=2), name="Discreto")
                #self.plot_widget.plot(tiempos, montos_continuos, pen=pg.mkPen(color='g', width=2, style=pg.QtCore.Qt.PenStyle.DashLine), name="Continuo")
                self.plot_widget.plot([tiempoAnios], [resultadoMonto], pen=None, symbol='o', symbolBrush='r',symbolSize=10)

                self.plot_widget.enableAutoRange(True, True)
            else:
                montoAcumulado = float(self.inputMontoDeseado.text())

                # Modelo discreto
                resultadoCapital = montoAcumulado / ((1 + (tasaInteres / capitalizaciones)) ** (capitalizaciones * tiempoAnios))
                capitalRedondeado = round(resultadoCapital, 2)
                self.labelResultado.setText(f"El capital inicial necesario es: (discreto) ${capitalRedondeado}")

                # Modelo continuo
                resultadoCapitalC = montoAcumulado / (math.e ** (tasaInteres * tiempoAnios))
                capitalRedondeadoC = round(resultadoCapitalC, 2)
                self.labelResultadoC.setText(f"El capital inicial necesario es: (continuo) ${capitalRedondeadoC}")

                # Generar datos para la gráfica
                tiempos = np.linspace(0, tiempoAnios, 100)
                montos_discretos = resultadoCapital * ((1 + (tasaInteres / capitalizaciones)) ** (capitalizaciones * tiempos))
                montos_continuos = resultadoCapital * (math.e ** (tasaInteres * tiempos))

                # Limpiar y graficar
                self.plot_widget.clear()
                self.plot_widget.plot(tiempos, montos_discretos, pen=pg.mkPen(color='b', width=2), name="Discreto")
                #self.plot_widget.plot(tiempos, montos_continuos, pen=pg.mkPen(color='g', width=2, style=pg.QtCore.Qt.PenStyle.DashLine), name="Continuo")
                self.plot_widget.plot([tiempoAnios], [montoAcumulado], pen=None, symbol='o', symbolBrush='r', symbolSize=10)

                self.plot_widget.enableAutoRange(True, True)
        except Exception as error:
            self.labelResultado.setText("Error al calcular")
            self.labelResultadoC.setText("Error al calcular")
            print(error)

    def resetearInputs(self):
        self.inputMontoDeseado.clear()
        self.inputCapitalInicial.clear()
        self.inputTasaInteres.setValue(0)
        self.inputCapitalizaciones.setValue(0)
        self.inputTiempoTotal.setValue(0)
        self.plot_widget.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())








