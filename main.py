import os
from flask import Flask, jsonify
from mysql.connector import pooling, Error

app = Flask(__name__)

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

POOL = None
def init_pool():
    global POOL
    if POOL is None:
        POOL = pooling.MySQLConnectionPool(
            pool_name="cloudrun_pool",
            pool_size=int(os.getenv("DB_POOL_SIZE", "5")),
            **DB_CONFIG
        )

@app.before_first_request
def startup():
    init_pool()

@app.route("/count", methods=["GET"])
def count_aceptados():
    try:
        init_pool()
        conn = POOL.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT COUNT(*) AS total_aceptados FROM tn_pasaporte_pagos WHERE estado_descripcion LIKE 'Aceptado';"
        )
        row = cursor.fetchone()
        total = int(row["total_aceptados"]) if row and row.get("total_aceptados") is not None else 0
        cursor.close()
        conn.close()
        return jsonify({"total_aceptados": total}), 200
    except Error as e:
        # no sweet words. log and return minimal info.
        return jsonify({"error": "db_error", "message": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "server_error", "message": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    return "ok", 200

if __name__ == "__main__":
    init_pool()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
