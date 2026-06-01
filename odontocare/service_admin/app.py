import os
from flask import Flask, jsonify
from models.models import db, Usuario
from blueprints.auth_bp import auth_bp
from blueprints.admin_bp import admin_bp
from werkzeug.security import generate_password_hash


def create_app():
    """Crea y configura la aplicación Flask."""
    app = Flask(__name__)

    # Configuración 
    # URL de la base de datos, se puede cambiar por variable de entorno
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "sqlite:///db_admin.sqlite"
    )
    # desactivamos el seguimiento de modificaciones para mejorar el rendimiento
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # clave secreta para firmar los tokens JWT
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "odontocare-secret-key-2026-jwt-ok")

    # Inicializamos la base de datos 
    db.init_app(app)

    # Registramos los blueprints 
    # cada blueprint agrupa las rutas de un módulo funcional
    app.register_blueprint(auth_bp) # rutas de autenticación
    app.register_blueprint(admin_bp) # rutas de administración

    # Creamos las tablas y el admin inicial 
    with app.app_context():
        db.create_all() # crea las tablas si no existen
        _crear_admin_inicial() # crea el usuario admin por defecto

    # Manejo de errores global
    @app.errorhandler(404)
    def not_found(e):
        # devuelve un JSON en vez de la página de error por defecto
        return jsonify({"error": str(e)}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Error interno del servidor"}), 500

    return app


def _crear_admin_inicial():
    """Crea un usuario admin por defecto si no existe ninguno."""
    if not Usuario.query.filter_by(rol="admin").first():
        admin = Usuario(
            username="admin",
            password=generate_password_hash("admin123"),
            rol="admin",
        )
        db.session.add(admin)
        db.session.commit()
        print("OK - Admin inicial creado: admin / admin123")

# punto de entrada del programa
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)