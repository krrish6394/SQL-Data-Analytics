# scripts/evaluatemodel.py
"""
Evaluate the best Logistic Regression sentiment analysis model.

This script:
- Loads the best Logistic Regression model from disk.
- Loads the test TF-IDF matrix and labels.
- Computes accuracy, precision, recall, and F1-score.
- Plots the confusion matrix.
"""

import os
import pickle
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, "data", "processeddata")
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Paths to data and model
TEST_PREPROCESSED_PATH = os.path.join(
    PROCESSED_DATA_DIR, "testdata_preprocessed.csv"
)
X_TEST_PATH = os.path.join(PROCESSED_DATA_DIR, "X_test.pickle")
BEST_MODEL_PATH = os.path.join(MODELS_DIR, "best_logistic_regression_model.pickle")


def main():
    """
    Load model and test data, run evaluation, and display metrics.
    """
    # Load preprocessed test data and vectorized features
    test_data = pd.read_csv(TEST_PREPROCESSED_PATH)
    with open(X_TEST_PATH, "rb") as f:
        X_test = pickle.load(f)

    # Convert textual labels to binary numeric form
    y_test = test_data["sentiment"].apply(lambda x: 1 if x == "positive" else 0)

    # Load the best Logistic Regression model found via hyperparameter tuning
    with open(BEST_MODEL_PATH, "rb") as f:
        best_model = pickle.load(f)

    # Predict labels on the test set
    y_pred = best_model.predict(X_test)

    # Compute accuracy and print classification report
    accuracy = accuracy_score(y_test, y_pred)
    print("Test Accuracy:", accuracy)
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    # Compute confusion matrix
    cm = confusion_matrix(y_test, y_pred, labels=[0, 1])

    # Plot confusion matrix with labels "Negative" and "Positive"
    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm, display_labels=["Negative", "Positive"]
    )
    disp.plot(cmap=plt.cm.Blues)
    plt.title("Logistic Regression Confusion Matrix")
    plt.show()


if __name__ == "__main__":
    main()