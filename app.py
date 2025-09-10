import os
from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# 🔹 Tomar URI desde variable de entorno
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise RuntimeError("❌ Falta definir la variable de entorno MONGO_URI en Render")

# Conexión a MongoDB Atlas
client = MongoClient(MONGO_URI)
db = client["smart_parking"]
col = db["polygons"]

@app.route("/polygons", methods=["GET"])
def get_polygons():
    polygons = list(col.find({}, {"_id": 0}))
    # Ordenar por coordenada X promedio
    polygons.sort(key=lambda p: sum(x for x, _ in p["points"]) / len(p["points"]))
    return jsonify(polygons)

@app.route("/status", methods=["GET"])
def get_status():
    total = col.count_documents({})
    occupied = col.count_documents({"occupied": True})
    free = total - occupied
    return jsonify({
        "total": total,
        "occupied": occupied,
        "free": free
    })

@app.route("/")
def home():
    return jsonify({"message": "🚗 Smart Parking API funcionando"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
