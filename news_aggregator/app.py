"""
News Aggregator Flask Application
==================================
Main application file that integrates all components:
- News fetching
- NLP processing
- Text summarization
- Web interface

Author: News Aggregator Project
Date: 2024
"""

import pkgutil
import importlib.util
import os
import sys

# Enforce running under Python 3.10 to avoid incompatibilities with
# newer stdlib changes (e.g. pkgutil differences in 3.14).
if not (sys.version_info.major == 3 and sys.version_info.minor == 10):
    sys.stderr.write(
        "ERROR: This application requires Python 3.10.\n"
        f"Detected Python {sys.version_info.major}.{sys.version_info.minor}.\n"
        "Please run using Python 3.10 (for example, use a pyenv/conda env or the project's venv).\n"
    )
    # Exit with non-zero so CI/builds fail fast when wrong interpreter is used
    sys.exit(2)

# Compatibility shim: Python 3.14 removed `pkgutil.get_loader` which
# older versions of Flask still call. Provide a minimal compatibility
# implementation so Flask can locate package paths.
if not hasattr(pkgutil, 'get_loader'):
    def _get_loader(name):
        # Special-case '__main__' when running the app as a script.
        if name == '__main__':
            main_mod = sys.modules.get('__main__')
            filename = getattr(main_mod, '__file__', None)
            if filename:
                class _MainLoader:
                    def get_filename(self, fullname):
                        return os.path.abspath(filename)

                return _MainLoader()

        spec = importlib.util.find_spec(name)
        if spec is None:
            return None

        class _Loader:
            def get_filename(self, fullname):
                return spec.origin

        return _Loader()

    pkgutil.get_loader = _get_loader

from flask import Flask, render_template, request, jsonify  # type: ignore
from datetime import datetime
import json
import os


# Timestamp helper to standardize format across the app
def now_ts(fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    return datetime.now().strftime(fmt)

# Import custom modules
from news_fetcher import NewsFetcher
from summarizer import TextSummarizer
from nlp_engine import NLPEngine

# Initialize Flask application
app = Flask(__name__)

# Configure upload folder
if not os.path.exists('data'):
    os.makedirs('data')
if not os.path.exists('models'):
    os.makedirs('models')
if not os.path.exists('templates'):
    os.makedirs('templates')

# Initialize components
print(f"\n[{now_ts()}] Initializing News Aggregator Application...")
news_fetcher = NewsFetcher()
summarizer = TextSummarizer()
nlp_engine = NLPEngine()

# Global variables for caching
cached_articles = {}
cached_summaries = {}


@app.route('/')
def index():
    """
    Render the home page.
    """
    return render_template('index.html')


@app.route('/api/categories', methods=['GET'])
def get_categories():
    """
    Get available news categories.
    """
    categories = ['general', 'technology', 'sports', 'entertainment']
    return jsonify({
        'status': 'success',
        'categories': categories,
        'timestamp': now_ts()
    })


@app.route('/api/fetch_news', methods=['POST'])
def fetch_news():
    """
    Fetch news articles for a specific category.
    """
    try:
        data = request.get_json()
        category = data.get('category', 'general')
        
        print(f"[{now_ts()}] Fetching {category} news...")
        
        # Fetch news
        articles = news_fetcher.fetch_news(category)
        
        # Cache the articles
        cached_articles[category] = articles
        
        print(f"[{now_ts()}] Successfully fetched {len(articles)} articles")
        
        return jsonify({
            'status': 'success',
            'category': category,
            'articles': articles,
            'count': len(articles),
            'timestamp': now_ts()
        })
    
    except Exception as e:
        print(f"[{now_ts()}] Error fetching news: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': now_ts()
        }), 500


@app.route('/api/preprocess_articles', methods=['POST'])
def preprocess_articles():
    """
    Preprocess fetched articles.
    """
    try:
        data = request.get_json()
        articles = data.get('articles', [])
        
        print(f"[{now_ts()}] Preprocessing {len(articles)} articles...")
        
        # Preprocess articles
        preprocessed = nlp_engine.preprocess_articles(articles)
        
        # Generate statistics
        stats = nlp_engine.generate_statistics(preprocessed)
        
        print(f"[{now_ts()}] Preprocessing complete")
        
        return jsonify({
            'status': 'success',
            'preprocessed_articles': preprocessed,
            'statistics': stats,
            'timestamp': now_ts()
        })
    
    except Exception as e:
        print(f"[{now_ts()}] Error preprocessing: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': now_ts()
        }), 500


@app.route('/api/summarize', methods=['POST'])
def summarize():
    """
    Summarize an article.
    """
    try:
        data = request.get_json()
        content = data.get('content', '')
        num_sentences = data.get('num_sentences', 3)
        
        print(f"[{now_ts()}] Summarizing article...")
        
        # Generate summary
        summary = summarizer.extractive_summarize(content, num_sentences=num_sentences)
        
        # Generate statistics
        stats = summarizer.get_summary_statistics(content, summary)
        
        print(f"[{now_ts()}] Summarization complete")
        
        return jsonify({
            'status': 'success',
            'original_content': content,
            'summary': summary,
            'statistics': stats,
            'timestamp': now_ts()
        })
    
    except Exception as e:
        print(f"[{now_ts()}] Error summarizing: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': now_ts()
        }), 500


@app.route('/api/categorize', methods=['POST'])
def categorize():
    """
    Categorize an article.
    """
    try:
        data = request.get_json()
        content = data.get('content', '')
        
        print(f"[{now_ts()}] Categorizing article...")
        
        # Categorize article
        category = nlp_engine.categorize_article(content, use_keywords=True)
        
        # Extract keywords
        keywords = nlp_engine.extract_keywords(content, num_keywords=5)
        
        print(f"[{now_ts()}] Categorization complete - Category: {category}")
        
        return jsonify({
            'status': 'success',
            'category': category,
            'keywords': keywords,
            'timestamp': now_ts()
        })
    
    except Exception as e:
        print(f"[{now_ts()}] Error categorizing: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': now_ts()
        }), 500


@app.route('/api/analyze_articles', methods=['POST'])
def analyze_articles():
    """
    Perform complete analysis on articles (fetch, preprocess, summarize, categorize).
    """
    try:
        data = request.get_json()
        category = data.get('category', 'general')
        
        print(f"\n[{now_ts()}] === STARTING COMPLETE ANALYSIS ===")
        print(f"[{now_ts()}] Category: {category}")
        
        # Step 1: Fetch news
        print(f"[{now_ts()}] STEP 1: Fetching news articles...")
        articles = news_fetcher.fetch_news(category)
        
        # Step 2: Preprocess articles
        print(f"[{now_ts()}] STEP 2: Preprocessing articles...")
        preprocessed = nlp_engine.preprocess_articles(articles)
        
        # Step 3: Summarize articles
        print(f"[{now_ts()}] STEP 3: Summarizing articles...")
        summarized = summarizer.summarize_articles(articles, num_sentences=2)
        
        # Step 4: Categorize articles and extract keywords
        print(f"[{now_ts()}] STEP 4: Categorizing articles...")
        analyzed_articles = []
        
        for i, article in enumerate(articles):
            content = article.get('content') or article.get('description') or ""
            category_pred = nlp_engine.categorize_article(content, use_keywords=True)
            keywords = nlp_engine.extract_keywords(content, num_keywords=5)
            
            analyzed_article = {
                'source': article.get('source', 'Unknown'),
                'title': article.get('title', 'No title'),
                'original_content': content,
                'summary': summarized[i]['summary'],
                'category': category_pred,
                'keywords': keywords,
                'url': article.get('url', ''),
                'publishedAt': article.get('publishedAt', ''),
                'urlToImage': article.get('urlToImage', ''),
                'summary_stats': summarized[i]['statistics']
            }
            
            analyzed_articles.append(analyzed_article)
        
        # Generate overall statistics
        stats = nlp_engine.generate_statistics(articles)
        
        print(f"[{now_ts()}] === ANALYSIS COMPLETE ===")
        print(f"[{now_ts()}] Processed {len(analyzed_articles)} articles")
        
        return jsonify({
            'status': 'success',
            'category': category,
            'articles': analyzed_articles,
            'statistics': stats,
            'timestamp': now_ts()
        })
    
    except Exception as e:
        print(f"[{now_ts()}] ERROR: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': now_ts()
        }), 500


@app.route('/api/extract_keywords', methods=['POST'])
def extract_keywords():
    """
    Extract keywords from text.
    """
    try:
        data = request.get_json()
        content = data.get('content', '')
        num_keywords = data.get('num_keywords', 5)
        
        print(f"[{now_ts()}] Extracting keywords...")
        
        # Extract keywords
        keywords = nlp_engine.extract_keywords(content, num_keywords=num_keywords)
        
        print(f"[{now_ts()}] Extracted {len(keywords)} keywords")
        
        return jsonify({
            'status': 'success',
            'keywords': keywords,
            'count': len(keywords),
            'timestamp': now_ts()
        })
    
    except Exception as e:
        print(f"[{now_ts()}] Error extracting keywords: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': now_ts()
        }), 500


@app.route('/api/health', methods=['GET'])
def health():
    """
    Health check endpoint.
    """
    return jsonify({
        'status': 'healthy',
        'message': 'News Aggregator API is running',
        'timestamp': now_ts()
    })


@app.errorhandler(404)
def not_found(error):
    """
    Handle 404 errors.
    """
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found',
        'timestamp': now_ts()
    }), 404


@app.errorhandler(500)
def server_error(error):
    """
    Handle 500 errors.
    """
    return jsonify({
        'status': 'error',
        'message': 'Internal server error',
        'timestamp': now_ts()
    }), 500


if __name__ == '__main__':
    print(f"\n[{now_ts()}] ========================================" )
    print(f"[{now_ts()}] NEWS AGGREGATOR APPLICATION")
    print(f"[{now_ts()}] ========================================" )
    print(f"[{now_ts()}] Starting Flask development server...")
    port = int(os.environ.get('NEWS_AGG_PORT', os.environ.get('PORT', '5000')))
    host = os.environ.get('NEWS_AGG_HOST', '127.0.0.1')
    print(f"[{now_ts()}] Visit http://{host}:{port} in your browser")
    print(f"[{now_ts()}] Press CTRL+C to stop the server")
    print(f"[{now_ts()}] ========================================\n")
    
    # Run Flask application (port and host configurable via env vars)
    app.run(debug=True, host=host, port=port)
