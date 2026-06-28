# News Aggregator App — Assignment Submission

Hi, I’m submitting my student project for the News Aggregator app.
This report explains what I built, how I ran it, and what I learned while working on it.

---

## 1. What this app does

This is a simple news aggregator built with Flask and a bit of NLP.
It fetches mock news articles, cleans and processes the text, summarizes content, and shows keywords and categories.
The app also exposes a small API for fetching articles and displaying analysis statistics like average content length.

## 2. Project highlights

- Built a Flask web app using `news_aggregator/app.py`
- Added a simple mock news fetcher in `news_aggregator/news_fetcher.py`
- Implemented preprocessing, keyword extraction, and article categorization in `news_aggregator/nlp_engine.py`
- Created a user interface in `news_aggregator/templates/index.html`
- Added project setup support with `news_aggregator/setup_env.sh`

## 3. How to run it

From the `news_aggregator` folder, run:

```bash
cd news_aggregator
.venv/bin/python app.py
```

If port 5000 is busy, use this instead:

```bash
cd news_aggregator
NEWS_AGG_PORT=5001 .venv/bin/python app.py
```

Then open the app in your browser at the address shown in the console.

## 4. What I learned

- How to organize a small Flask app with separate modules for fetching, NLP, and summarization
- How to handle inconsistent mock URLs and normalize them before sending them to the frontend
- How to avoid `NaN` in statistics display by aligning backend response fields with frontend rendering
- How to use a project-local Python virtual environment and run the app from the correct folder

## 5. Notes about the submission

- The app uses mock data instead of a real news API so it runs without API keys.
- The frontend shows helpful statistics and a list of analyzed articles.
- The `Read Full Article` button opens a valid source homepage for each mock article.
- The code is meant to be easy to read and understand, with simple logic that can be extended later.

## 6. Files included

- `app.py` — main Flask app
- `news_fetcher.py` — mock article provider
- `nlp_engine.py` — text preprocessing, categorization, keyword extraction
- `summarizer.py` — summarization and text statistics
- `templates/index.html` — single-page frontend
- `setup_env.sh` — helper script for environment setup
- `.venv/` — Python virtual environment for Python 3.10

## 7. Personal reflection

I enjoyed building the app because it combined backend logic with a simple frontend and some natural language processing.
Working through the environment setup and fixing UI/backend mismatches taught me how important consistent data structures are.

Thanks for reviewing my assignment!
