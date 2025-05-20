
import os
import io
import base64
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from oct2py import Oct2Py

# Inicializa Octave y configura el path al script newton_raphson_transferencia.m
oc = Oct2Py()
script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
oc.addpath(script_path)

def ejecutar_newton_transferencia(T0, Tamb, Tcrit, k, x0, tolerancia, max_iter):
    try:
        # Llamada a la función de Octave con 7 argumentos
        x_critico, iteraciones, contador = oc.feval(
            "newton_raphson_transferencia", T0, Tamb, Tcrit, k, x0, tolerancia, max_iter, nout=3
        )
        x_critico = float(x_critico)

        if np.isnan(x_critico):
            return "No se encontró una distancia válida.", None, [], None

        # Convertir iteraciones a lista de diccionarios
        iter_list = []
        if iteraciones is not None:
            for fila in iteraciones:
                iter_list.append({
                    'iteracion': int(fila[0]),
                    'x': float(fila[1]),
                    'fx': float(fila[2])
                })

        # Generar imagen con la función de transferencia
        img = graficar_transferencia(T0, Tamb, Tcrit, k, x_critico)

        return x_critico, img, iter_list, int(contador)

    except Exception as e:
        return f"Error al ejecutar Octave: {str(e)}", None, None, None

def graficar_transferencia(T0, Tamb, Tcrit, k, x_critico):
    try:
        x = np.linspace(0, x_critico + 5, 400)
        y = Tamb + (T0 - Tamb) * np.exp(-k * x)

        plt.figure(figsize=(6, 4))
        plt.plot(x, y, label=f'T(x) = {Tamb} + ({T0} - {Tamb})·e^(-{k}·x)', color='orange')
        plt.axhline(Tcrit, color='gray', linestyle='--', label=f'T crítica = {Tcrit}°C')
        plt.axvline(x_critico, color='red', linestyle='--', label=f'Distancia ≈ {x_critico:.2f} m')
        plt.title("Disminución de temperatura en tubería")
        plt.xlabel("Distancia (m)")
        plt.ylabel("Temperatura (°C)")
        plt.grid(True)
        plt.legend()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)

        return base64.b64encode(buf.read()).decode('utf-8')

    except Exception as e:
        print(f"Error al graficar: {e}")
        return None
