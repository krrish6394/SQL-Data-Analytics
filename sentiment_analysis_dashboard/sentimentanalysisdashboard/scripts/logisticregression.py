# scripts/logisticregression.py
"""
Train a Logistic Regression sentiment analysis model on the preprocessed IMDB data.

This script:
- Loads the preprocessed training data and TF-IDF vectors.
- Optionally balances the dataset using SMOTE (if you decide to add that step).
- Trains a Logistic Regression classifier.
- Evaluates it on the test set.
- Saves the trained model for reuse in the Flask app.
"""

import os
import pickle
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROCESSED_DATA_DIR = os.path.join(BASE_DIR, "data", "processeddata")
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Paths to preprocessed data and TF-IDF matrices
TRAIN_PREPROCESSED_PATH = os.path.join(
    PROCESSED_DATA_DIR, "traindata_preprocessed.csv"
)
TEST_PREPROCESSED_PATH = os.path.join(
    PROCESSED_DATA_DIR, "testdata_preprocessed.csv"
)
X_TRAIN_PATH = os.path.join(PROCESSED_DATA_DIR, "X_train.pickle")
X_TEST_PATH = os.path.join(PROCESSED_DATA_DIR, "X_test.pickle")

# Path to save the trained Logistic Regression model
MODEL_PATH = os.path.join(MODELS_DIR, "logistic_regression_model.pickle")


def main():
    """
    Train and evaluate the Logistic Regression sentiment model.
    """
    # Load preprocessed training and test datasets
    train_data = pd.read_csv(TRAIN_PREPROCESSED_PATH)
    test_data = pd.read_csv(TEST_PREPROCESSED_PATH)

    # Load vectorized feature matrices from disk
    with open(X_TRAIN_PATH, "rb") as f:
        X_train = pickle.load(f)
    with open(X_TEST_PATH, "rb") as f:
        X_test = pickle.load(f)

    # Extract labels as binary values (1 for positive, 0 for negative)
    # IMDB 'sentiment' column contains 'positive' / 'negative'
    y_train = train_data["sentiment"].apply(lambda x: 1 if x == "positive" else 0)
    y_test = test_data["sentiment"].apply(lambda x: 1 if x == "positive" else 0)

    # Initialize Logistic Regression model with a sufficiently large max_iter
    model = LogisticRegression(max_iter=1000)

    # Fit model on the training data
    print("Training Logistic Regression model...")
    model.fit(X_train, y_train)

    # Save the trained model for reuse in the dashboard
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    print(f"Saved Logistic Regression model to {MODEL_PATH}")

    # Evaluate the model on the test set
    print("Evaluating model on test set...")
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print("Test Accuracy:", accuracy)
    print("Classification Report:")
    print(classification_report(y_test, y_pred))


if __name__ == "__main__":
    main()