from flask import Flask, request, jsonify
from flask_cors import CORS

import joblib
import pandas as pd


# ==========================================
# Flask Application
# ==========================================

app = Flask(__name__)

CORS(app)


# ==========================================
# Load AI Model
# ==========================================

model = joblib.load(
    "../ai_model/model.pkl"
)


# ==========================================
# Prediction API
# ==========================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.get_json()


        cpu_usage = float(
            data["cpu_usage"]
        )

        memory_usage = float(
            data["memory_usage"]
        )

        io_operations = float(
            data["io_operations"]
        )

        process_type = float(
            data["process_type"]
        )


        # Create DataFrame with feature names

        input_data = pd.DataFrame(
            [[
                cpu_usage,
                memory_usage,
                io_operations,
                process_type
            ]],
            columns=[
                "cpu_usage",
                "memory_usage",
                "io_operations",
                "process_type"
            ]
        )


        # AI prediction

        prediction = model.predict(
            input_data
        )[0]


        return jsonify({
            "predicted_burst_time":
                round(float(prediction), 2)
        })


    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 400


# ==========================================
# Health Check
# ==========================================

@app.route("/")

def home():

    return jsonify({
        "message":
            "AI Process Scheduler API is running"
    })


# ==========================================
# Start Server
# ==========================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )