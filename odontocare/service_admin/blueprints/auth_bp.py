# Importaciones
import os
from datetime import datetime, timedelta, timezone
from functools import wraps
import jwt # para generar y validar tokens
from flask import Blueprint, request, jsonify # Blueprint nos permite agrupar rutas relacionadas, y jsonify convierte diccionarios Python a respuestas JSON
from werkzeug.security import generate_password_hash, check_password_hash # encriptamos las contraseñas, nunca en texto plano
from models.models import db, Usuario 

# Creamos el blue print de autenticación
auth_bp = Blueprint ("auth", __name__, url_prefix="/auth") # agrupa todas las rutas de autenticación bajo "/auth"
# Clave secreta para firmar los tokens JWT
SECRET_KEY = os.environ.get("SECRET_KEY","odontocare-secret-key-2026-jwt-ok")

def generate_token(user): # crea un token con el id, username y rol del usuario, válido 8 horas
    """Genera un token JWT con los datos del usuario."""
    payload = {
        "id_usuario": user.id_usuario,
        "username": user.username,
        "rol": user.rol,
        "exp": datetime.now(timezone.utc) + timedelta(hours=8), #expira en 8 horas
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token): # comprueba si el token es válido, si no devuelve "None"
    """Valida el token JWT. Devuelve los datos del usuario o None si es invalido."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None # token expirado
    except jwt.InvalidTokenError:
        return None # token inválido
    
def token_required (f): 
    """Protege un endpoint exigiendo un token válido en el header. Comprueba que el header Authorization: Bearer <token> existe y es válido."""
    @wraps(f)
    def decorated(*args,**kwargs): # Comprueba que el header "Authorization: Bearer <token> existe y es válido"
        auth_header = request.headers.get("Authorization","")
        if not auth_header.startswith("Bearer"):
            return jsonify({"error":"Token requerido"}), 401
        token = auth_header.split(" ")[1] # extraemos el token del header
        payload = verify_token(token)
        if not payload:
            return jsonify({"error":"Token inválido o expirado"}), 401
        request.current_user = payload # guardamos los datos del usuario en la request
        return f(*args, **kwargs)
    return decorated

def role_required(*roles): 
    """Protege un endpoint exigiendo además un rol específico."""
    def decorator(f): 
        @wraps(f)
        @token_required # valida el token
        def decorated(*args, **kwargs): # comprueba que el rol del usuario es el permitido 
            if request.current_user["rol"] not in roles:
                return jsonify({"error": "Acceso denegado: rol insuficiente"}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator
    

# Endpoints
@auth_bp.route("/login", methods=["POST"]) # recibe username y password, devuelve el token JWT
def login():
    """Recibe username y password, devuelve JWT si las credenciales son válidas."""
    data = request.get_json()

    # comprobamos que vienen los dos campos obligatorios
    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "username y password son requeridos"}), 400

    # buscamos el usuario en la base de datos
    user = Usuario.query.filter_by(username=data["username"]).first()

    # comprobamos que existe y que la contraseña es correcta
    if not user or not check_password_hash(user.password, data["password"]):
        return jsonify({"error": "Credenciales incorrectas"}), 401

    # generamos el token y lo devolvemos junto el rol y username
    token = generate_token(user)
    return jsonify({"token": token, "rol": user.rol, "username": user.username}), 200


@auth_bp.route("/verificar", methods=["GET"]) # comprueba si un token es válido, lo usará el servicio de citas internamente
@token_required
def verificar():
    """Endpoint interno para verificar que un token es válido."""
    return jsonify({"valid": True, "user": request.current_user}), 200