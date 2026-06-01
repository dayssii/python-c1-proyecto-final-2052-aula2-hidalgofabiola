# Importaciones
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash # para encriptar contraseñas antes de guardarlas
from models.models import db, Usuario, Doctor, Paciente, CentroMedico
from blueprints.auth_bp import role_required # el decorador que creamos en "auth_bp-py" para proteger los endpoints

# Creamos el blueprint de administración
admin_bp = Blueprint("admin", __name__, url_prefix="/admin") # todas las rutas de este blueprint empezarán por "/admin"

# Endpoints usuarios
@admin_bp.route("/usuario", methods=["POST"])
@role_required("admin")
def crear_usuario():
    """Crea un usuario con rol admin o secretaria."""
    data = request.get_json()

    # comprobamos que vienen todos los campos necesarios
    if not all(data.get(c) for c in ["username", "password", "rol"]):
        return jsonify({"error": "username, password y rol son requeridos"}), 400
    
    # solo se pueden crear usuarios admi o secretaria desde aquí
    if data["rol"] not in ("admin","secretaria"):
        return jsonify({"error":"Rol inválido. Solo 'admin' o 'secretaria'"}), 400
    
    # comprobamos que el username no exista ya
    if Usuario.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "El username ya existe"}), 409
    
    # creamos el usuario con la contraseña encriptada
    user = Usuario(
        username=data["username"],
        password=generate_password_hash(data["password"]),
        rol=data["rol"],
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"mensaje": "Usuario creado", "usuario": user.to.dict()}), 201

@admin_bp.route("/usuarios", methods=["GET"])
@role_required("admin")
def listar_usuarios():
    """Devuelve la lista de todos los usuarios."""
    usuarios = Usuario.query.all()
    return jsonify([u.to_dict() for u in usuarios]), 200

@admin_bp.route("/usuarios/<int:id>", methods=["GET"])
@role_required("admin")
def obtener_usuario(id):
   """Devuelve un usuario por su ID."""
   u = Usuario.query.get_or_404(id, decription="Usuaro no encontrado")
   return jsonify(u.to_dict()), 200


# Endpoints doctores
@admin_bp.route("/doctores", methods=["POST"])
@role_required("admin")
def crear_doctor():
    """Crea un doctor y su usuario asociado con rol 'medico'."""
    data = request.get_json()

    # comprobamos campos obligatorios
    if not all(data.get(c) for c in ["nombre", "especialidad", "username", "password"]):
        return jsonify({"error": "nombre, especialidad, username y password son requeridos"}), 400

    # comprobamos que el username no exista ya
    if Usuario.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "El username ya existe"}), 409

    # creamos primero el usuario con rol medico
    user = Usuario(
        username=data["username"],
        password=generate_password_hash(data["password"]),
        rol="medico",
    )
    db.session.add(user)
    db.session.flush()  # obtenemos el id_usuario antes del commit, nos permite guardar el usuario en memoria para obtener su ID sin cerrar la transición todavia

    # luego creamos el doctor vinculado a ese usuario
    doctor = Doctor(
        nombre=data["nombre"],
        especialidad=data["especialidad"],
        id_usuario=user.id_usuario,
    )
    db.session.add(doctor)
    db.session.commit()
    return jsonify({"mensaje": "Doctor creado", "doctor": doctor.to_dict()}), 201


@admin_bp.route("/doctores", methods=["GET"])
@role_required("admin", "secretaria")
def listar_doctores():
    """Devuelve la lista de todos los doctores."""
    doctores = Doctor.query.all()
    return jsonify([d.to_dict() for d in doctores]), 200


@admin_bp.route("/doctores/<int:id>", methods=["GET"])
@role_required("admin", "secretaria", "medico")
def obtener_doctor(id):
    """Devuelve un doctor por su ID."""
    d = Doctor.query.get_or_404(id, description="Doctor no encontrado")
    return jsonify(d.to_dict()), 200


# Endpoints pacientes

@admin_bp.route("/pacientes", methods=["POST"])
@role_required("admin")
def crear_paciente():
    """Crea un paciente y su usuario asociado con rol 'paciente'."""
    data = request.get_json()

    # comprobamos campos obligatorios
    if not all(data.get(c) for c in ["nombre", "telefono", "username", "password"]):
        return jsonify({"error": "nombre, telefono, username y password son requeridos"}), 400

    # comprobamos que el username no exista ya
    if Usuario.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "El username ya existe"}), 409

    # creamos primero el usuario con rol paciente
    user = Usuario(
        username=data["username"],
        password=generate_password_hash(data["password"]),
        rol="paciente",
    )
    db.session.add(user)
    db.session.flush() # obtenemos el id_usuario antes del commit

    # luego creamos el paciente vinculado a ese usuario
    paciente = Paciente(
        nombre=data["nombre"],
        telefono=data["telefono"],
        id_usuario=user.id_usuario,
        estado="ACTIVO",
    )
    db.session.add(paciente)
    db.session.commit()
    return jsonify({"mensaje": "Paciente creado", "paciente": paciente.to_dict()}), 201


@admin_bp.route("/pacientes", methods=["GET"])
@role_required("admin", "secretaria")
def listar_pacientes():
    """Devuelve la lista de todos los pacientes."""
    pacientes = Paciente.query.all()
    return jsonify([p.to_dict() for p in pacientes]), 200


@admin_bp.route("/pacientes/<int:id>", methods=["GET"])
@role_required("admin", "secretaria")
def obtener_paciente(id):
    """Devuelve un paciente por su ID."""
    p = Paciente.query.get_or_404(id, description="Paciente no encontrado")
    return jsonify(p.to_dict()), 200


# Endpoints Centros médicos

@admin_bp.route("/centros", methods=["POST"])
@role_required("admin")
def crear_centro():
    """Crea un centro médico."""
    data = request.get_json()

    # comprobamos campos obligatorios
    if not data.get("nombre") or not data.get("direccion"):
        return jsonify({"error": "nombre y direccion son requeridos"}), 400

    centro = CentroMedico(nombre=data["nombre"], direccion=data["direccion"])
    db.session.add(centro)
    db.session.commit()
    return jsonify({"mensaje": "Centro creado", "centro": centro.to_dict()}), 201


@admin_bp.route("/centros", methods=["GET"])
@role_required("admin", "secretaria", "medico", "paciente")
def listar_centros():
    """Devuelve la lista de todos los centros médicos."""
    centros = CentroMedico.query.all()
    return jsonify([c.to_dict() for c in centros]), 200


@admin_bp.route("/centros/<int:id>", methods=["GET"])
@role_required("admin", "secretaria", "medico", "paciente")
def obtener_centro(id):
    """Devuelve un centro médico por su ID."""
    c = CentroMedico.query.get_or_404(id, description="Centro no encontrado")
    return jsonify(c.to_dict()), 200