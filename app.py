from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# 🔹 Conexión a MongoDB Atlas
MONGO_URI = "mongodb+srv://admin:admin123@cluster0.mongodb.net/smart_parking"
client = MongoClient(MONGO_URI)
db = client["smart_parking"]
col = db["polygons"]

@app.route("/polygons", methods=["GET"])
def get_polygons():
    polygons = list(col.find({}, {"_id": 0}))
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
