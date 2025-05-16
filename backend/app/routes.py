from flask import Blueprint, jsonify, request, render_template
from .octave_interface import ejecutar_newton

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
    funcion = data.get('funcion')
    x0 = float(data.get('x0', 0))
    tolerancia = float(data.get('tolerancia', 1e-6))
    max_iter = int(data.get('max_iter', 100))

    if not funcion:
        return jsonify({'error': 'La función es obligatoria'}), 400

    resultado, img_base64, iteraciones, contador = ejecutar_newton(funcion, x0, tolerancia, max_iter)

    if isinstance(resultado, str) and resultado.startswith("Error"):
        return jsonify({'error': resultado}), 500

    return jsonify({
        'resultado': resultado,
        'imagen': img_base64,
        'iteraciones': iteraciones,
        'contador': contador
    })


