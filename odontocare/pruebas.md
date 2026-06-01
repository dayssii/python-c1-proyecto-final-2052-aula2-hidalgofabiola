# Documentación de Pruebas de Endpoints — OdontoCare

## Servicio Admin (http://localhost:5000)

---

### POST /auth/login
Inicia sesión y devuelve un token JWT.

**URL:** http://localhost:5000/auth/login  
**Headers:** ninguno  
**Body:**
```json
{
    "username": "admin",
    "password": "admin123"
}
```

---

### POST /admin/usuario
Crea un usuario con rol admin o secretaria.

**URL:** http://localhost:5000/admin/usuario  
**Headers:** Authorization: Bearer <token>  
**Body:**
```json
{
    "username": "secretaria1",
    "password": "pass.123",
    "rol": "secretaria"
}
```

---

### POST /admin/doctores
Crea un doctor y su usuario asociado.

**URL:** http://localhost:5000/admin/doctores  
**Headers:** Authorization: Bearer <token>  
**Body:**
```json
{
    "nombre": "Dra. Ursula Iguaran",
    "especialidad": "Ortodoncia",
    "username": "dr.iguaran",
    "password": "pass.123"
}
```

---

### GET /admin/doctores
Lista todos los doctores.

**URL:** http://localhost:5000/admin/doctores  
**Headers:** Authorization: Bearer <token>  
**Body:** ninguno

---

### GET /admin/doctores/<id>
Obtiene un doctor por su ID.

**URL:** http://localhost:5000/admin/doctores/1  
**Headers:** Authorization: Bearer <token>  
**Body:** ninguno

---

### POST /admin/pacientes
Crea un paciente y su usuario asociado.

**URL:** http://localhost:5000/admin/pacientes  
**Headers:** Authorization: Bearer <token>  
**Body:**
```json
{
    "nombre": "Petra Cotes",
    "telefono": "612345678",
    "username": "petra.cotes",
    "password": "pass.123"
}
```

---

### GET /admin/pacientes
Lista todos los pacientes.

**URL:** http://localhost:5000/admin/pacientes  
**Headers:** Authorization: Bearer <token>  
**Body:** ninguno

---

### GET /admin/pacientes/<id>
Obtiene un paciente por su ID.

**URL:** http://localhost:5000/admin/pacientes/1  
**Headers:** Authorization: Bearer <token>  
**Body:** ninguno

---

### POST /admin/centros
Crea un centro médico.

**URL:** http://localhost:5000/admin/centros  
**Headers:** Authorization: Bearer <token>  
**Body:**
```json
{
    "nombre": "Clínica Dental Macondo",
    "direccion": "Avenida Colombia 1, Macondo"
}
```

---

### GET /admin/centros
Lista todos los centros médicos.

**URL:** http://localhost:5000/admin/centros  
**Headers:** Authorization: Bearer <token>  
**Body:** ninguno

---

### GET /admin/centros/<id>
Obtiene un centro médico por su ID.

**URL:** http://localhost:5000/admin/centros/1  
**Headers:** Authorization: Bearer <token>  
**Body:** ninguno

---

## Servicio Citas (http://localhost:5001)

---

### POST /citas
Agenda una nueva cita médica.

**URL:** http://localhost:5001/citas  
**Headers:** Authorization: Bearer <token>  
**Body:**
```json
{
    "fecha": "15/09/2026 10:00",
    "motivo": "Revisión general y limpieza dental",
    "id_paciente": 1,
    "id_doctor": 1,
    "id_centro": 1
}
```

---

### GET /citas
Lista las citas según el rol del usuario. Admite filtros y paginación.

**URL:** http://localhost:5001/citas  
**URL con filtros (admin):** http://localhost:5001/citas?id_doctor=1&estado=Programada&page=1&per_page=10  
**URL con filtro fecha (secretaria):** http://localhost:5001/citas?fecha=15/09/2026  
**Headers:** Authorization: Bearer <token>  
**Body:** ninguno

**Comportamiento según rol:**
- Admin: puede filtrar por id_doctor, id_centro, id_paciente, estado y fecha
- Secretaria: solo puede filtrar por fecha
- Medico: solo ve sus propias citas
- Paciente: solo ve sus propias citas

---

### GET /citas/<id>
Obtiene una cita por su ID.

**URL:** http://localhost:5001/citas/1  
**Headers:** Authorization: Bearer <token>  
**Body:** ninguno

---

### PUT /citas/<id>
Cancela una cita existente.

**URL:** http://localhost:5001/citas/1  
**Headers:** Authorization: Bearer <token>  
**Body:** ninguno