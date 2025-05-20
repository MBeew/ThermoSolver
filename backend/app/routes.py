from flask import Blueprint, jsonify, request, render_template
from .octave_interface import ejecutar_newton_transferencia

main = Blueprint('main', __name__)

@main.route('/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'Servidor ThermoSolver activo'})

@main.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@main.route('/calcular', methods=['POST'])
def calcular():
    data = request.get_json()

    # Recoger datos del frontend
    try:
        T0 = float(data.get('T0'))
        Tamb = float(data.get('Tamb'))
        Tcrit = float(data.get('Tcrit'))
        k = float(data.get('k'))
        x0 = float(data.get('x0', 0))
        tolerancia = float(data.get('tolerancia', 1e-6))
        max_iter = int(data.get('max_iter', 100))
    except (TypeError, ValueError):
        return jsonify({'error': 'Parámetros inválidos o faltantes'}), 400

    # Depuración: Imprimir valores que se enviarán a Octave
    print(f"[DEBUG] Parámetros recibidos: T0={T0}, Tamb={Tamb}, Tcrit={Tcrit}, k={k}, x0={x0}, tol={tolerancia}, max_iter={max_iter}")

    # Ejecutar cálculo usando Octave
    resultado, img_base64, iteraciones, contador = ejecutar_newton_transferencia(
        T0, Tamb, Tcrit, k, x0, tolerancia, max_iter
    )

    # Verificar errores
    if isinstance(resultado, str) and resultado.startswith("Error"):
        return jsonify({'error': resultado}), 500

    # Responder al frontend
    return jsonify({
        'x_critico': resultado,
        'imagen': img_base64,
        'iteraciones': iteraciones,
        'contador': contador
    })
