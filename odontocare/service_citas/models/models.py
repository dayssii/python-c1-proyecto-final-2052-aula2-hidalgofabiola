from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# Creamos la tabla de citas médicas
# esta tabla vive en su propia base de datos, separada de service_admin
class Cita(db.Model):
    __tablename__ = "citas"

    # identificador único de la cita
    id_cita = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(20), nullable=False)  # formato "DD-MM-YYYY HH:MM"
    motivo = db.Column(db.String(300), nullable=False) # motivo de la consulta
    estado = db.Column(db.String(15), default="Programada")  # estado de la cita: Programada, Cancelada, Completada
    
    # referencias a otros servicios mediante ID
    # no usamos ForgeinKey por que estos datos están en la base de datos de service_admin
    id_paciente = db.Column(db.Integer, nullable=False) 
    id_doctor = db.Column(db.Integer, nullable=False)    
    id_centro = db.Column(db.Integer, nullable=False)    
    # usuario que registró la cita
    id_usuario_registra = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        """Convierte el objeto a diccionario para devolverlo como JSON."""
        return {
            "id_cita": self.id_cita,
            "fecha": self.fecha,
            "motivo": self.motivo,
            "estado": self.estado,
            "id_paciente": self.id_paciente,
            "id_doctor": self.id_doctor,
            "id_centro": self.id_centro,
            "id_usuario_registra": self.id_usuario_registra,
        }