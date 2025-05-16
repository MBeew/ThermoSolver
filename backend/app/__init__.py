from flask import Flask
from flask_cors import CORS
import os

def create_app():
    # Define rutas absolutas hacia las carpetas de frontend
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    templates_path = os.path.join(base_dir, 'frontend', 'templates')
    static_path = os.path.join(base_dir, 'frontend', 'static')

    # Crear la app Flask con rutas personalizadas
    app = Flask(__name__, template_folder=templates_path, static_folder=static_path)
    CORS(app)

    from .routes import main
    app.register_blueprint(main)

    return app
