import os
from flask import Flask, jsonify
from models.models import db
from blueprints.citas_bp import citas_bp


def create_app():
    """Crea y configura la aplicación Flask del servicio de citas."""
    app = Flask(__name__)

    # Configuración 
    # base de datos propia e independiente de service_admin
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "sqlite:///db_citas.sqlite"
    )
    # desactivamos el seguimiento de modificaciones para mejorar el rendimiento
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Inicializamos la base de datos 
    db.init_app(app)

    # Registramos el blueprint de citas 
    # contiene todas las rutas de gestión de citas médicas
    app.register_blueprint(citas_bp)

    # Creamos las tablas 
    with app.app_context():
        db.create_all() # crea la tabla de citas si no existe

    # Manejo de errores global
    @app.errorhandler(404)
    def not_found(e):
        # devuelve un JSON en vez de la página de error por defecto
        return jsonify({"error": str(e)}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Error interno del servidor"}), 500

    return app

# punto de entrada del programa
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5001, debug=True)