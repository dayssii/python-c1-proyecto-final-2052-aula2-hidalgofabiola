"""
carga_inicial.py — Cliente OdontoCare
Leemos datos.csv y carga doctores, pacientes y centros en la API.
Luego agendamos una cita de ejemplo.
"""

import csv
import json
import sys
import requests

# Configuración 
ADMIN_URL = "http://localhost:5000"
CITAS_URL = "http://localhost:5001"
CSV_FILE = "datos.csv"


def login():
    """Hace login como admin y devuelve el token."""
    resp = requests.post(
        f"{ADMIN_URL}/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    if resp.status_code != 200:
        print(f"ERROR - Login fallido: {resp.json()}")
        sys.exit(1)
    print("OK - Login correcto como admin")
    return resp.json()["token"]


def headers(token):
    """Devuelve el header con el token."""
    return {"Authorization": f"Bearer {token}"}


def cargar_doctor(token, row):
    """Envía un doctor a la API, si ya existe obtiene su ID."""
    payload = {
        "nombre": row["nombre"].strip(),
        "especialidad": row["especialidad"].strip(),
        "username": row["username"].strip(),
        "password": row["password"].strip(),
    }
    resp = requests.post(
        f"{ADMIN_URL}/admin/doctores",
        json=payload,
        headers=headers(token)
    )
    if resp.status_code == 201:
        id_ = resp.json()["doctor"]["id_doctor"]
        print(f"  >> Doctor creado: {payload['nombre']} (id={id_})")
        return id_
    else:
        # si ya existe, buscamos su ID en la lista
        doctores = requests.get(f"{ADMIN_URL}/admin/doctores", headers=headers(token)).json()
        doctor = next((d for d in doctores if d["nombre"] == payload["nombre"]), None)
        if doctor:
            print(f"  >> Doctor ya existe: {payload['nombre']} (id={doctor['id_doctor']})")
            return doctor["id_doctor"]
        return None


def cargar_paciente(token, row):
    """Envía un paciente a la API, si ya existe obtiene su ID."""
    payload = {
        "nombre": row["nombre"].strip(),
        "telefono": row["telefono"].strip(),
        "username": row["username"].strip(),
        "password": row["password"].strip(),
    }
    resp = requests.post(
        f"{ADMIN_URL}/admin/pacientes",
        json=payload,
        headers=headers(token)
    )
    if resp.status_code == 201:
        id_ = resp.json()["paciente"]["id_paciente"]
        print(f"  >> Paciente creado: {payload['nombre']} (id={id_})")
        return id_
    else:
        # si ya existe, buscamos su ID en la lista
        pacientes = requests.get(f"{ADMIN_URL}/admin/pacientes", headers=headers(token)).json()
        paciente = next((p for p in pacientes if p["nombre"] == payload["nombre"]), None)
        if paciente:
            print(f"  >> Paciente ya existe: {payload['nombre']} (id={paciente['id_paciente']})")
            return paciente["id_paciente"]
        return None


def cargar_centro(token, row):
    """Envía un centro médico a la API, si ya existe obtiene su ID."""
    payload = {
        "nombre": row["nombre"].strip(),
        "direccion": row["direccion"].strip(),
    }
    resp = requests.post(
        f"{ADMIN_URL}/admin/centros",
        json=payload,
        headers=headers(token)
    )
    if resp.status_code == 201:
        id_ = resp.json()["centro"]["id_centro"]
        print(f"  >> Centro creado: {payload['nombre']} (id={id_})")
        return id_
    else:
        # si ya existe, buscamos su ID en la lista
        centros = requests.get(f"{ADMIN_URL}/admin/centros", headers=headers(token)).json()
        centro = next((c for c in centros if c["nombre"] == payload["nombre"]), None)
        if centro:
            print(f"  >> Centro ya existe: {payload['nombre']} (id={centro['id_centro']})")
            return centro["id_centro"]
        return None


def main():
    print("=" * 50)
    print("   OdontoCare — Carga Inicial")
    print("=" * 50)

    # Login
    token = login()

    # Leer CSV y cargar datos
    doctores, pacientes, centros = [], [], []
    print("Procesando datos.csv...")

    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            tipo = row["tipo"].strip().lower()
            if tipo == "doctor":
                id_ = cargar_doctor(token, row)
                if id_:
                    doctores.append(id_)
            elif tipo == "paciente":
                id_ = cargar_paciente(token, row)
                if id_:
                    pacientes.append(id_)
            elif tipo == "centro":
                id_ = cargar_centro(token, row)
                if id_:
                    centros.append(id_)

    # Agendar cita de ejemplo
    print("Agendando cita de ejemplo...")
    resp = requests.post(
        f"{CITAS_URL}/citas",
        json={
            "fecha": "15-09-2026 10:00",
            "motivo": "Revisión general",
            "id_paciente": pacientes[0],
            "id_doctor": doctores[0],
            "id_centro": centros[0],
        },
        headers=headers(token)
    )

    # Imprimir resultado
    if resp.status_code == 201:
        print(">> Cita creada:")
        print(json.dumps(resp.json(), indent=2, ensure_ascii=False))
    else:
        print(f"Error: {resp.json()}")

    print("\n" + "=" * 50)
    print("   Carga completada")
    print("=" * 50)


if __name__ == "__main__":
    main()