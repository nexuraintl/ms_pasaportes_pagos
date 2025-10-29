from flask import Flask, jsonify
import mysql.connector
import os

app = Flask(__name__)

def get_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT", 3306))
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error de conexión: {err}")
        return None

@app.route("/count", methods=["GET"])
def count_pagos():
    conn = get_connection()
    if not conn:
        return jsonify({"error": "db_error", "message": "No se pudo conectar a la base de datos"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) AS total_aceptados FROM tn_pasaporte_pagos WHERE estado_descripcion LIKE 'Aceptado';")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify(result)
    except mysql.connector.Error as err:
        print(f"Error en la consulta: {err}")
        return jsonify({"error": "db_error", "message": str(err)}), 500

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Servicio de conteo de pagos aceptados"})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
