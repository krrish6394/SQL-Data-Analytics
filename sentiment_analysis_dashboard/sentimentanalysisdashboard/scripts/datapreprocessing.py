# scripts/datapreprocessing.py
"""
Data preprocessing script for the Sentiment Analysis Dashboard project.

This script:
- Loads the IMDB movie reviews dataset from data/rawdata/IMDBDataset.csv.
- Splits the data into training and test sets.
- Applies text preprocessing (normalization, tokenization, stop word removal,
  lemmatization).
- Saves the preprocessed train and test CSVs.
- Vectorizes the text with TF-IDF and saves the vectorizer and vectorized matrices.
"""

import os
import string
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download required NLTK resources (no-op if already downloaded)
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

# Resolve base directory as the project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Construct paths for input and output data
RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "rawdata", "IMDBDataset.csv")
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, "data", "processeddata")
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Ensure output directories exist
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

# Initialize lemmatizer and stopword list once for efficiency
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))


def preprocess_text(text: str) -> str:
    """
    Apply basic NLP preprocessing to a single input string.

    Steps:
    - Convert to lowercase.
    - Tokenize into words.
    - Remove punctuation and English stopwords.
    - Lemmatize remaining tokens.
    - Join tokens back into a single cleaned string.
    """
    # Convert text to lowercase to normalize case
    text = text.lower()

    # Tokenize into individual tokens using NLTK
    tokens = nltk.word_tokenize(text)

    # Filter out punctuation and stopwords
    filtered_tokens = [
        tok
        for tok in tokens
        if tok not in string.punctuation and tok not in stop_words
    ]

    # Lemmatize each remaining token to its base form
    lemmatized_tokens = [lemmatizer.lemmatize(tok) for tok in filtered_tokens]

    # Reconstruct the cleaned text string
    return " ".join(lemmatized_tokens)


def main():
    """
    Main entry point for preprocessing.

    - Loads IMDB dataset.
    - Splits into train/test.
    - Applies preprocessing.
    - Saves preprocessed CSVs.
    - Vectorizes with TF-IDF and saves vectorizer and matrices.
    """
    # Load the IMDB dataset CSV from Kaggle (columns: 'review', 'sentiment')
    data = pd.read_csv(RAW_DATA_PATH)

    # Rename columns to more generic names for clarity
    data = data.rename(columns={"review": "review", "sentiment": "sentiment"})

    # Print a few rows for sanity check when running interactively
    print("Sample of raw data:")
    print(data.head())

    # Split into training and test sets (80/20) with a fixed random state for reproducibility
    train_data, test_data = train_test_split(
        data, test_size=0.2, random_state=42
    )

    # Apply preprocessing to the 'review' column for both train and test sets
    print("Preprocessing training reviews...")
    train_data["review"] = train_data["review"].apply(preprocess_text)

    print("Preprocessing test reviews...")
    test_data["review"] = test_data["review"].apply(preprocess_text)

    # Save preprocessed CSVs for later use by other scripts
    train_preprocessed_path = os.path.join(
        PROCESSED_DATA_DIR, "traindata_preprocessed.csv"
    )
    test_preprocessed_path = os.path.join(
        PROCESSED_DATA_DIR, "testdata_preprocessed.csv"
    )

    train_data.to_csv(train_preprocessed_path, index=False)
    test_data.to_csv(test_preprocessed_path, index=False)

    print(f"Saved preprocessed training data to {train_preprocessed_path}")
    print(f"Saved preprocessed test data to {test_preprocessed_path}")

    # Initialize TF-IDF vectorizer with a maximum vocabulary size
    vectorizer = TfidfVectorizer(max_features=5000)

    # Fit vectorizer on training reviews and transform train and test
    print("Vectorizing text with TF-IDF...")
    X_train = vectorizer.fit_transform(train_data["review"]).toarray()
    X_test = vectorizer.transform(test_data["review"]).toarray()

    # Persist vectorizer and vectorized matrices to disk
    vectorizer_path = os.path.join(MODELS_DIR, "vectorizer.pickle")
    X_train_path = os.path.join(PROCESSED_DATA_DIR, "X_train.pickle")
    X_test_path = os.path.join(PROCESSED_DATA_DIR, "X_test.pickle")

    with open(vectorizer_path, "wb") as f:
        pickle.dump(vectorizer, f)

    with open(X_train_path, "wb") as f:
        pickle.dump(X_train, f)

    with open(X_test_path, "wb") as f:
        pickle.dump(X_test, f)

    print(f"Saved TF-IDF vectorizer to {vectorizer_path}")
    print(f"Saved X_train matrix to {X_train_path}")
    print(f"Saved X_test matrix to {X_test_path}")
    print("Preprocessing complete.")


if __name__ == "__main__":
    main()