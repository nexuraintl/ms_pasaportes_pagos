import os
import mariadb
from flask import Flask, jsonify

app = Flask(__name__)

# Configuración de conexión desde variables de entorno
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "35.193.47.107"),
    "user": os.getenv("DB_USER", "cloudrun"),
    "password": os.getenv("DB_PASSWORD", "SxqG7+oZ6jt1"),
    "database": os.getenv("DB_NAME", "cloudrun"),
    "port": int(os.getenv("DB_PORT", 3306))
}

def get_connection():
    """Crea una conexión nueva a la base de datos MariaDB."""
    try:
        conn = mariadb.connect(**DB_CONFIG)
        return conn
    except mariadb.Error as e:
        raise RuntimeError(f"Error al conectar a la base de datos: {e}")

@app.route("/count", methods=["GET"])
def count_aceptados():
    """Cuenta cuántos pagos están en estado 'Aceptado'."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM tn_pasaporte_pagos WHERE estado_descripcion LIKE 'Aceptado';")
        (total,) = cur.fetchone()
        cur.close()
        conn.close()
        return jsonify({"total_aceptados": int(total)}), 200
    except mariadb.Error as e:
        return jsonify({"error": "db_error", "message": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "server_error", "message": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    """Endpoint de prueba de vida."""
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
