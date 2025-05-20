import os
import io
import base64
import numpy as np
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from oct2py import Oct2Py

# Inicializa Octave y configura el path al script newton_raphson.m
oc = Oct2Py()
script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
oc.addpath(script_path)

def ejecutar_newton(funcion, x0, tolerancia, max_iter):
    try:
        # Llama a la función de Octave y recibe raíz, iteraciones y contador
        root, iteraciones, contador = oc.feval("newton_raphson", funcion, x0, tolerancia, max_iter, nout=3)
        root = float(root)

        # Verifica si la raíz es válida
        if np.isnan(root):
            return "No se encontró una raíz válida.", None, [], None

        # Convierte las iteraciones en una lista de diccionarios
        iter_list = []
        if iteraciones is not None:
            for fila in iteraciones:
                iter_list.append({
                    'iteracion': int(fila[0]),
                    'x': float(fila[1]),
                    'fx': float(fila[2])
                })

        # Genera imagen de la función con la raíz
        img = graficar_funcion(funcion, root)
        return root, img, iter_list, int(contador)

    except Exception as e:
        return f"Error al ejecutar Octave: {str(e)}", None, None, None

def graficar_funcion(funcion, raiz):
    def traducir_a_numpy(expr):
        expr = expr.replace('^', '**')
        expr = expr.replace('exp', 'np.exp')
        expr = expr.replace('log10', 'np.log10')
        expr = expr.replace('log', 'np.log')  
        expr = expr.replace('sqrt', 'np.sqrt')
        expr = expr.replace('sin', 'np.sin')
        expr = expr.replace('cos', 'np.cos')
        expr = expr.replace('tan', 'np.tan')
        return expr

    try:
        # Crear rango de valores alrededor de la raíz
        x = np.linspace(raiz - 5, raiz + 5, 400)

        # Traducir la expresión para que sea compatible con NumPy/Python
        expr = traducir_a_numpy(funcion)

        # Evaluar la expresión
        y = [eval(expr, {"x": val, "np": np}) for val in x]

        # Graficar
        plt.figure(figsize=(6, 4))
        plt.plot(x, y, label=f'f(x) = {funcion}')
        plt.axhline(0, color='black', linewidth=0.7)
        plt.axvline(raiz, color='red', linestyle='--', label=f'Raíz ≈ {raiz:.5f}')
        plt.legend()
        plt.grid(True)

        # Guardar la figura en buffer y convertir a base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)

        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        return img_base64

    except Exception as e:
        print(f"Error al graficar: {e}")
        return None
