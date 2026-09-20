
from flask import Flask, request, jsonify
import pandas as pd
import joblib

# Initialize Flask application
app = Flask(__name__)

# Load the trained SuperKart model
model = joblib.load("superkart_model.joblib")

# Define the expected input features
FEATURES = [
    "Product_Weight",
    "Product_Sugar_Content",
    "Product_Allocated_Area",
    "Product_MRP",
    "Store_Size",
    "Store_Location_City_Type",
    "Store_Type",
    "Product_Id_char",
    "Store_Age_Years",
    "Product_Type_Category"
]

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "SuperKart Sales Prediction API is running"
    })


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        # Convert input JSON into a DataFrame
        input_data = pd.DataFrame([data])

        # Keep features in the same order used during training
        input_data = input_data[FEATURES]

        # Generate prediction
        prediction = model.predict(input_data)[0]

        return jsonify({
            "prediction": float(prediction)
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400

@app.route("/predict_batch", methods=["POST"])
def predict_batch():
    try:
        data = request.get_json()

        input_data = pd.DataFrame(data)
        input_data = input_data[FEATURES]

        predictions = model.predict(input_data)

        return jsonify({
            "predictions": [float(prediction) for prediction in predictions]
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
