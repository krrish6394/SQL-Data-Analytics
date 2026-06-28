# scripts/lstmmodel.py
"""
LSTM-based sentiment analysis model for the Sentiment Analysis Dashboard.

This script:
- Loads the preprocessed IMDB train and test data.
- Tokenizes reviews and pads sequences.
- Builds and trains an LSTM model in Keras.
- Saves the trained model and tokenizer to the models/ directory.
- Evaluates the model on the test set.
"""

import os
import pickle
import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import accuracy_score, classification_report

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, "data", "processeddata")
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Paths for preprocessed CSVs
TRAIN_PREPROCESSED_PATH = os.path.join(
    PROCESSED_DATA_DIR, "traindata_preprocessed.csv"
)
TEST_PREPROCESSED_PATH = os.path.join(
    PROCESSED_DATA_DIR, "testdata_preprocessed.csv"
)

# Paths for saving model and tokenizer
LSTM_MODEL_PATH = os.path.join(MODELS_DIR, "lstmmodel.h5")
TOKENIZER_PATH = os.path.join(MODELS_DIR, "tokenizer.pickle")

# Hyperparameters for tokenization and model structure
VOCAB_SIZE = 5000          # Maximum number of words in the vocabulary
MAX_SEQUENCE_LENGTH = 200  # Maximum sequence length for padding
EMBEDDING_DIM = 100        # Size of word embedding vectors


def main():
    """
    Train and evaluate the LSTM sentiment analysis model.
    """
    # Load preprocessed training and test data
    train_data = pd.read_csv(TRAIN_PREPROCESSED_PATH)
    test_data = pd.read_csv(TEST_PREPROCESSED_PATH)

    # Extract text and labels
    X_train_texts = train_data["review"].astype(str).tolist()
    y_train = train_data["sentiment"].apply(lambda x: 1 if x == "positive" else 0).values

    X_test_texts = test_data["review"].astype(str).tolist()
    y_test = test_data["sentiment"].apply(lambda x: 1 if x == "positive" else 0).values

    # Initialize and fit tokenizer on training texts
    tokenizer = Tokenizer(num_words=VOCAB_SIZE, oov_token="OOV")
    tokenizer.fit_on_texts(X_train_texts)

    # Convert training and test texts to sequences of integer indices
    X_train_sequences = tokenizer.texts_to_sequences(X_train_texts)
    X_test_sequences = tokenizer.texts_to_sequences(X_test_texts)

    # Pad sequences so that they all have the same length
    X_train_padded = pad_sequences(
        X_train_sequences,
        maxlen=MAX_SEQUENCE_LENGTH,
        padding="post",
        truncating="post",
    )
    X_test_padded = pad_sequences(
        X_test_sequences,
        maxlen=MAX_SEQUENCE_LENGTH,
        padding="post",
        truncating="post",
    )

    # Build the LSTM model as described in the book
    model = Sequential()
    model.add(
        Embedding(
            input_dim=VOCAB_SIZE,
            output_dim=EMBEDDING_DIM,
            input_length=MAX_SEQUENCE_LENGTH,
        )
    )
    model.add(LSTM(128, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(64))
    model.add(Dropout(0.2))
    model.add(Dense(1, activation="sigmoid"))

    # Compile model with binary crossentropy and Adam optimizer
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss="binary_crossentropy",
        metrics=["accuracy"],
    )

    # Train the model with a validation split
    print("Training LSTM model...")
    history = model.fit(
        X_train_padded,
        y_train,
        epochs=10,
        batch_size=32,
        validation_split=0.2,
    )

    # Save the trained model
    model.save(LSTM_MODEL_PATH)
    print(f"Saved LSTM model to {LSTM_MODEL_PATH}")

    # Save the tokenizer to reuse preprocessing at inference time
    with open(TOKENIZER_PATH, "wb") as f:
        pickle.dump(tokenizer, f)
    print(f"Saved tokenizer to {TOKENIZER_PATH}")

    # Evaluate on the test set
    print("Evaluating LSTM model on test set...")
    y_pred_prob = model.predict(X_test_padded)
    y_pred = (y_pred_prob >= 0.5).astype(int).flatten()

    accuracy = accuracy_score(y_test, y_pred)
    print("Test Accuracy:", accuracy)
    print("Classification Report:")
    print(classification_report(y_test, y_pred))


if __name__ == "__main__":
    main()