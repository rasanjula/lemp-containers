import os
from flask import Flask, jsonify
import mysql.connector
from datetime import timezone
from zoneinfo import ZoneInfo  # NEW

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "db")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "apppass")
DB_NAME = os.getenv("DB_NAME", "appdb")

@app.get("/api")
def root_api():
    return jsonify(message="Backend is up")

@app.get("/api/time")
def time_from_db():
    # Fetch server time (UTC in your setup) and convert to Europe/Helsinki
    conn = mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    cur = conn.cursor()
    cur.execute("SELECT NOW()")
    row = cur.fetchone()
    cur.close(); conn.close()

    utc_dt = row[0].replace(tzinfo=timezone.utc)
    helsinki_dt = utc_dt.astimezone(ZoneInfo("Europe/Helsinki"))

    return jsonify(
        server_time=str(utc_dt),  # legacy UTC
        server_time_helsinki=helsinki_dt.isoformat(timespec="seconds")
    )

@app.get("/api/health")
def health():
    return jsonify(ok=True)
