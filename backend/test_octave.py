from oct2py import Oct2Py
import os

# Ruta absoluta al archivo .m
script_path = os.path.abspath("backend")
print("Agregando ruta a Octave:", script_path)

oc = Oct2Py()
oc.addpath(script_path)  # Asegura que se cargue correctamente

# Verifica que existe la función newton_raphson
print("Probando ejecución...")
resultado = oc.feval("newton_raphson", "x^2 - 4", 2, 1e-6, 100)
print("Resultado:", resultado)
