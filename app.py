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

from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import os

# Import custom modules
from news_fetcher import NewsFetcher
from nlp_engine import NLPEngine
from summarizer import TextSummarizer

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
print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Initializing News Aggregator Application...")
news_fetcher = NewsFetcher()
nlp_engine = NLPEngine()
summarizer = TextSummarizer()

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
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })


@app.route('/api/fetch_news', methods=['POST'])
def fetch_news():
    """
    Fetch news articles for a specific category.
    """
    try:
        data = request.get_json()
        category = data.get('category', 'general')
        
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Fetching {category} news...")
        
        # Fetch news
        articles = news_fetcher.fetch_news(category)
        
        # Cache the articles
        cached_articles[category] = articles
        
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Successfully fetched {len(articles)} articles")
        
        return jsonify({
            'status': 'success',
            'category': category,
            'articles': articles,
            'count': len(articles),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error fetching news: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }), 500


@app.route('/api/preprocess_articles', methods=['POST'])
def preprocess_articles():
    """
    Preprocess fetched articles.
    """
    try:
        data = request.get_json()
        articles = data.get('articles', [])
        
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Preprocessing {len(articles)} articles...")
        
        # Preprocess articles
        preprocessed = nlp_engine.preprocess_articles(articles)
        
        # Generate statistics
        stats = nlp_engine.generate_statistics(preprocessed)
        
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Preprocessing complete")
        
        return jsonify({
            'status': 'success',
            'preprocessed_articles': preprocessed,
            'statistics': stats,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error preprocessing: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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
        
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Summarizing article...")
        
        # Generate summary
        summary = summarizer.extractive_summarize(content, num_sentences=num_sentences)
        
        # Generate statistics
        stats = summarizer.get_summary_statistics(content, summary)
        
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Summarization complete")
        
        return jsonify({
            'status': 'success',
            'original_content': content,
            'summary': summary,
            'statistics': stats,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error summarizing: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }), 500


@app.route('/api/categorize', methods=['POST'])
def categorize():
    """
    Categorize an article.
    """
    try:
        data = request.get_json()
        content = data.get('content', '')
        
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Categorizing article...")
        
        # Categorize article
        category = nlp_engine.categorize_article(content, use_keywords=True)
        
        # Extract keywords
        keywords = nlp_engine.extract_keywords(content, num_keywords=5)
        
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Categorization complete - Category: {category}")
        
        return jsonify({
            'status': 'success',
            'category': category,
            'keywords': keywords,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error categorizing: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }), 500


@app.route('/api/analyze_articles', methods=['POST'])
def analyze_articles():
    """
    Perform complete analysis on articles (fetch, preprocess, summarize, categorize).
    """
    try:
        data = request.get_json()
        category = data.get('category', 'general')
        
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] === STARTING COMPLETE ANALYSIS ===")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Category: {category}")
        
        # Step 1: Fetch news
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] STEP 1: Fetching news articles...")
        articles = news_fetcher.fetch_news(category)
        
        # Step 2: Preprocess articles
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] STEP 2: Preprocessing articles...")
        preprocessed = nlp_engine.preprocess_articles(articles)
        
        # Step 3: Summarize articles
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] STEP 3: Summarizing articles...")
        summarized = summarizer.summarize_articles(articles, num_sentences=2)
        
        # Step 4: Categorize articles and extract keywords
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] STEP 4: Categorizing articles...")
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
        
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] === ANALYSIS COMPLETE ===")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Processed {len(analyzed_articles)} articles")
        
        return jsonify({
            'status': 'success',
            'category': category,
            'articles': analyzed_articles,
            'statistics': stats,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ERROR: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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
        
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Extracting keywords...")
        
        # Extract keywords
        keywords = nlp_engine.extract_keywords(content, num_keywords=num_keywords)
        
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Extracted {len(keywords)} keywords")
        
        return jsonify({
            'status': 'success',
            'keywords': keywords,
            'count': len(keywords),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error extracting keywords: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }), 500


@app.route('/api/health', methods=['GET'])
def health():
    """
    Health check endpoint.
    """
    return jsonify({
        'status': 'healthy',
        'message': 'News Aggregator API is running',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })


@app.errorhandler(404)
def not_found(error):
    """
    Handle 404 errors.
    """
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }), 404


@app.errorhandler(500)
def server_error(error):
    """
    Handle 500 errors.
    """
    return jsonify({
        'status': 'error',
        'message': 'Internal server error',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }), 500


if __name__ == '__main__':
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ========================================")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] NEWS AGGREGATOR APPLICATION")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ========================================")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting Flask development server...")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Visit http://localhost:5000 in your browser")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Press CTRL+C to stop the server")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ========================================\n")
    
    # Run Flask application
    app.run(debug=True, host='127.0.0.1', port=5000)
