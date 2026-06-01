from flask_sqlalchemy import SQLAlchemy # Libreria que nos permite hablar con la base de datos usando Python en vez de SQL puro
db = SQLAlchemy() # Creamos el objeto que luego conectaremos a Flask

# Creamos la tabla de usuarios
class Usuario(db.Model): # le dice a SQLAlchemy que esta clase es una tabla
    __tablename__ = "usuarios"

    # cada db.Colum es una columna de esta tabla
    id_usuario = db.Column(db.Integer, primary_key=True) # el ID único de cada fila
    username = db.Column(db.String(80), unique=True, nullable=False) # indica que este campo no puede estar vacío
    password = db.Column(db.String(256), nullable=False) # siempre guardamos la contraseña encriptada
    rol = db.Column(db.String(20), nullable=False)  # admin, medico, secretaria, paciente

    def to_dict(self): # convierte el objeto a JSON para devolverlo en la API
        return {
            "id_usuario": self.id_usuario,
            "username": self.username,
            "rol": self.rol,
        }

# Creamos la tabla de médicos  
class Doctor(db.Model):
    __tablename__ = "doctores"

    id_doctor = db.Column(db.Integer, primary_key=True)
    # relación con la tabla usuarios
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuario"), nullable=True)
    nombre = db.Column(db.String(120), nullable=False)
    especialidad = db.Column(db.String(120), nullable=False)

    def to_dict(self):
        """Convierte el objeto a diccionario para devolverlo como JSON."""
        return {
            "id_doctor": self.id_doctor,
            "nombre": self.nombre,
            "especialidad": self.especialidad,
            "id_usuario": self.id_usuario,
        }
    
# Creamos la tabla de pacientes
class Paciente(db.Model):
    __tablename__ = "pacientes"

    id_paciente = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuario"), nullable=True)
    nombre = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    estado = db.Column(db.String(10), default="ACTIVO")  # ACTIVO o INACTIVO, solo los ACTIVOS pueden tener citas

    def to_dict(self):
        """Convierte el objeto a diccionario para devolverlo como JSON."""
        return {
            "id_paciente": self.id_paciente,
            "nombre": self.nombre,
            "telefono": self.telefono,
            "estado": self.estado,
            "id_usuario": self.id_usuario,
        }


# Creamos la tabla de centros médicos
class CentroMedico(db.Model):
    __tablename__ = "centros_medicos"

    id_centro = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        """Convierte el objeto a diccionario para devolverlo como JSON."""
        return {
            "id_centro": self.id_centro,
            "nombre": self.nombre,
            "direccion": self.direccion,
        }