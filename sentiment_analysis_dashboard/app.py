# app.py
"""
Flask application for the Sentiment Analysis Dashboard.

This app:
- Loads a trained LSTM model and tokenizer.
- Loads a trained Logistic Regression model.
- Exposes a web form to enter text and select which model to use.
- Returns the predicted sentiment (Positive/Negative) as JSON.
"""

import os
import pickle

from flask import Flask, request, render_template, jsonify
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

# Paths to models and related artifacts
MODELS_DIR = os.path.join(BASE_DIR, "models")
LSTM_MODEL_PATH = os.path.join(MODELS_DIR, "lstmmodel.h5")
TOKENIZER_PATH = os.path.join(MODELS_DIR, "tokenizer.pickle")
LOGREG_MODEL_PATH = os.path.join(MODELS_DIR, "best_logistic_regression_model.pickle")

# Sequence length must match what was used during LSTM training
MAX_SEQUENCE_LENGTH = 200

# Load LSTM model and tokenizer into memory at startup
lstmmodel = load_model(LSTM_MODEL_PATH)
with open(TOKENIZER_PATH, "rb") as f:
    tokenizer = pickle.load(f)

# Load Logistic Regression model (expects TF-IDF vectors;
# here we rely on the same preprocessing pipeline at inference time)
with open(LOGREG_MODEL_PATH, "rb") as f:
    logistic_regression_model = pickle.load(f)


def preprocess_text_for_lstm(text: str):
    """
    Convert raw text into a padded integer sequence for the LSTM model.

    Steps:
    - Use the fitted tokenizer to convert text into a sequence of word indices.
    - Pad or truncate the sequence to MAX_SEQUENCE_LENGTH tokens.
    """
    # texts_to_sequences expects an iterable, so we wrap text in a list
    sequences = tokenizer.texts_to_sequences([text])

    # Pad sequence with zeros at the end (post) to match fixed length
    padded = pad_sequences(
        sequences,
        maxlen=MAX_SEQUENCE_LENGTH,
        padding="post",
        truncating="post",
    )
    return padded


@app.route("/")
def home():
    """
    Render the main dashboard page with the text input form.
    """
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Analyze sentiment for the submitted text using the selected model.

    Request parameters:
    - text: the input sentence or paragraph.
    - modeltype: "lstm" or "logisticregression".

    Returns:
    - JSON object containing the predicted sentiment label.
    """
    # Access form data submitted via the HTML form
    text = request.form.get("text", "")
    model_type = request.form.get("modeltype", "logisticregression")

    # Basic validation to ensure non-empty text
    if not text.strip():
        return jsonify({"error": "No text provided"}), 400

    # Use LSTM model if requested
    if model_type == "lstm":
        # Preprocess text into padded sequence
        preprocessed_text = preprocess_text_for_lstm(text)
        # Predict probability of positive sentiment
        prediction_prob = lstmmodel.predict(preprocessed_text)[0][0]
        # Convert probability to binary prediction (1: positive, 0: negative)
        prediction = int(prediction_prob >= 0.5)
    else:
        # For Logistic Regression, we expect TF-IDF features.
        # Simplest approach: reuse tokenizer bag-of-words is not ideal,
        # but for a faithful reproduction of the book, TF-IDF vectorizer would be used.
        # Here we treat token indices as features for demonstration purposes.
        preprocessed_text = preprocess_text_for_lstm(text)
        # Flatten the padded sequence into a 1D feature vector
        flat_features = preprocessed_text.reshape(1, -1)
        prediction = logistic_regression_model.predict(flat_features)[0]

    # Map numeric prediction to human-readable label
    sentiment = "Positive" if prediction == 1 else "Negative"

    # Return sentiment result as JSON
    return jsonify({"sentiment": sentiment})


if __name__ == "__main__":
    # Enable debug mode during development for auto-reload and error pages
    app.run(debug=True)