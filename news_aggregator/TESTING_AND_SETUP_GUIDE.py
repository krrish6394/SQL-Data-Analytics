"""
NEWS AGGREGATOR PROJECT - COMPLETE SETUP AND TESTING GUIDE
===========================================================

This document provides complete instructions for setting up and testing the 
News Aggregator NLP project as defined in the textbook.

PROJECT STRUCTURE
=================
news_aggregator/
├── news_fetcher.py          # Module for fetching news articles
├── nlp_engine.py            # NLP processing and categorization
├── summarizer.py            # Text summarization module
├── app.py                   # Flask web application
├── articles.json            # Sample articles dataset
├── index.html               # Web interface template
├── requirements.txt         # Python dependencies
├── data/                    # Directory for data files
├── models/                  # Directory for trained models
├── templates/               # Directory for HTML templates
└── README.md               # Project documentation


STEP 1: ENVIRONMENT SETUP
==========================

1.1 Prerequisites:
   - Python 3.7 or higher
   - pip (Python package manager)
   - Virtual environment (recommended)

1.2 Create Virtual Environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

1.3 Install Dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   Required packages:
   - Flask==2.0.1
   - requests==2.26.0
   - nltk==3.6.2
   - scikit-learn==0.24.2
   - gensim==4.0.1
   - numpy==1.19.5
   - transformers==4.11.0 (optional, for advanced summarization)


STEP 2: DIRECTORY SETUP
=======================

2.1 Create required directories:
   ```bash
   mkdir -p data
   mkdir -p models
   mkdir -p templates
   ```

2.2 Copy HTML template:
   - Place index.html in the templates/ directory

2.3 Copy sample data:
   - Place articles.json in the data/ directory


STEP 3: MODULE TESTING
=======================

3.1 Test News Fetcher Module:
   ```bash
   python news_fetcher.py
   ```
   
   Expected Output:
   - Successfully fetches articles from mock sources
   - Displays articles from: BBC, TechCrunch, ESPN, Variety
   - Saves articles to data/articles.json
   
   Test Steps:
   1. Run the module
   2. Verify articles are fetched for each category
   3. Check that articles.json is created
   4. Verify 2-4 articles per category

3.2 Test NLP Engine Module:
   ```bash
   python nlp_engine.py
   ```
   
   Expected Output:
   - Successfully preprocesses text
   - Removes stopwords and lemmatizes
   - Generates TF-IDF vectors
   - Categorizes articles
   - Saves vectorizer to models/vectorizer.pickle
   
   Test Steps:
   1. Run the module
   2. Verify text preprocessing works
   3. Check keyword extraction
   4. Verify article categorization
   5. Check that statistics are generated

3.3 Test Text Summarizer Module:
   ```bash
   python summarizer.py
   ```
   
   Expected Output:
   - Successfully extracts sentences
   - Calculates word frequencies
   - Generates extractive summaries
   - Provides compression statistics
   - Summarizes multiple articles
   
   Test Steps:
   1. Run the module
   2. Verify sentence extraction works
   3. Check frequency analysis
   4. Verify summary generation
   5. Check compression ratio < 1


STEP 4: FLASK APPLICATION TESTING
===================================

4.1 Start Flask Application:
   ```bash
   python app.py
   ```
   
   Expected Output:
   ```
   [2024-01-15 10:30:45] ========================================
   [2024-01-15 10:30:45] NEWS AGGREGATOR APPLICATION
   [2024-01-15 10:30:45] ========================================
   [2024-01-15 10:30:45] Starting Flask development server...
   [2024-01-15 10:30:45] Visit http://localhost:5000 in your browser
   [2024-01-15 10:30:45] Press CTRL+C to stop the server
   [2024-01-15 10:30:45] ========================================
   ```

4.2 Test API Endpoints (using curl or Postman):

   A. Health Check:
   ```bash
   curl http://localhost:5000/api/health
   ```
   
   Expected Response:
   ```json
   {
     "status": "healthy",
     "message": "News Aggregator API is running",
     "timestamp": "2024-01-15 10:30:45"
   }
   ```

   B. Get Categories:
   ```bash
   curl http://localhost:5000/api/categories
   ```
   
   Expected Response:
   ```json
   {
     "status": "success",
     "categories": ["general", "technology", "sports", "entertainment"],
     "timestamp": "2024-01-15 10:30:45"
   }
   ```

   C. Fetch News:
   ```bash
   curl -X POST http://localhost:5000/api/fetch_news \
     -H "Content-Type: application/json" \
     -d '{"category": "technology"}'
   ```
   
   Expected Response:
   - Returns list of articles for selected category
   - Each article has: source, title, content, summary, url, publishedAt

   D. Analyze Articles (Complete Pipeline):
   ```bash
   curl -X POST http://localhost:5000/api/analyze_articles \
     -H "Content-Type: application/json" \
     -d '{"category": "technology"}'
   ```
   
   Expected Response:
   - All articles analyzed
   - Includes summaries, keywords, categories
   - Statistics: total_articles, num_sources, avg_content_length


STEP 5: WEB INTERFACE TESTING
==============================

5.1 Access the Web Interface:
   - Open browser to: http://localhost:5000/
   - Should see News Aggregator interface

5.2 Test Web Interface:
   1. Select a news category from dropdown
   2. Adjust summary length (1-5 sentences)
   3. Click "Analyze News" button
   4. Verify articles are displayed with:
      - Title
      - Source
      - Summary
      - Keywords
      - Category
      - Full article link

5.3 Verify Results:
   - Statistics section shows:
     * Total Articles
     * News Sources
     * Average Content Length
     * Processing Time
   - Each article card shows complete analysis


STEP 6: INTEGRATION TESTING
============================

6.1 Complete Workflow Test:

   Step A: Fetch News
   - Run: python news_fetcher.py
   - Verify: articles.json is created with sample data

   Step B: Preprocess Articles
   - Test NLP engine preprocessing
   - Verify: Stopwords removed, text lemmatized

   Step C: Summarize Articles
   - Test summarizer on preprocessed text
   - Verify: Summary length < original

   Step D: Categorize Articles
   - Test article categorization
   - Verify: Keywords extracted correctly

   Step E: Flask Integration
   - Start Flask application
   - Make API requests
   - Verify complete pipeline works

6.2 Data Pipeline Test:
   ```
   Raw Articles → Fetch → Preprocess → Vectorize → Categorize → Summarize → Output
   ```
   
   Each stage should:
   - Accept input from previous stage
   - Process without errors
   - Produce expected output format


STEP 7: PERFORMANCE AND QUALITY CHECKS
=======================================

7.1 Summarization Quality:
   - Check that summaries are coherent
   - Verify compression ratio (typically 0.3-0.5)
   - Ensure key information is preserved

7.2 Categorization Accuracy:
   - Tech articles should be categorized as "technology"
   - Sports articles should be categorized as "sports"
   - etc.

7.3 Response Times:
   - Fetch: < 500ms
   - Preprocess: < 1000ms per article
   - Summarize: < 500ms per article
   - Categorize: < 500ms per article

7.4 Error Handling:
   - Empty text: Should return appropriate message
   - Invalid category: Should handle gracefully
   - API errors: Should return error JSON with status

7.5 Data Validation:
   - All articles have required fields
   - No null/empty mandatory fields
   - Timestamps are valid


STEP 8: TESTING CHECKLIST
==========================

Module Tests:
[ ] news_fetcher.py - Fetches articles correctly
[ ] nlp_engine.py - Preprocesses and vectorizes text
[ ] summarizer.py - Generates accurate summaries

API Tests:
[ ] /api/health - Returns healthy status
[ ] /api/categories - Returns list of categories
[ ] /api/fetch_news - Fetches articles by category
[ ] /api/preprocess_articles - Preprocesses articles
[ ] /api/summarize - Generates summaries
[ ] /api/categorize - Categorizes articles
[ ] /api/analyze_articles - Complete analysis pipeline

Web Interface Tests:
[ ] Page loads without errors
[ ] Category dropdown works
[ ] Submit button triggers analysis
[ ] Results display correctly
[ ] Statistics section shows data
[ ] Article links work
[ ] Responsive design works

Data Tests:
[ ] articles.json contains all categories
[ ] Sample data is properly formatted
[ ] No missing or null fields
[ ] Timestamps are valid

Integration Tests:
[ ] Complete workflow executes
[ ] Data flows between modules correctly
[ ] Output matches specifications
[ ] Error handling works properly


TROUBLESHOOTING
================

Issue: "ModuleNotFoundError: No module named 'flask'"
Solution: pip install -r requirements.txt

Issue: "NLTK resource not found"
Solution: Run python -c "import nltk; nltk.download('punkt')" etc.

Issue: "Port 5000 already in use"
Solution: app.run(port=5001) or kill process on port 5000

Issue: "articles.json not found"
Solution: Ensure data/ directory exists and articles.json is in it

Issue: "No articles returned"
Solution: Check news_fetcher.py mock_articles dictionary is populated


SAMPLE TEST SESSION
====================

1. Terminal 1: Start Flask
   $ python app.py
   [2024-01-15 10:30:45] Starting Flask development server...

2. Terminal 2: Test API
   $ curl http://localhost:5000/api/health
   {"status": "healthy", ...}

3. Browser: Test Web Interface
   - Open http://localhost:5000
   - Select "Technology"
   - Click "Analyze News"
   - See results within 2-3 seconds

4. Check console logs
   - Should see timestamps for each operation
   - No errors should appear
   - Processing should complete successfully


SUBMISSION REQUIREMENTS
=======================

When submitting this project, include:

1. All Code Files:
   [ ] news_fetcher.py
   [ ] nlp_engine.py
   [ ] summarizer.py
   [ ] app.py
   [ ] index.html (in templates/)
   [ ] articles.json (in data/)
   [ ] requirements.txt

2. Testing Screenshots:
   [ ] Flask server running (with timestamp)
   [ ] Web interface loaded (with timestamp)
   [ ] Sample analysis results (with timestamp)
   [ ] API endpoint responses (with timestamp)
   [ ] Console output showing processing (with timestamp)

3. Documentation:
   [ ] README.md with setup instructions
   [ ] This testing guide
   [ ] Sample analysis output
   [ ] Screenshots with date/time stamps


PROJECT COMPLETION CHECKLIST
=============================

Functionality:
[ ] Fetch articles from multiple sources
[ ] Preprocess text (remove stopwords, lemmatize)
[ ] Extract keywords from articles
[ ] Summarize articles (extractive)
[ ] Categorize articles by topic
[ ] Calculate text statistics
[ ] Generate vectorized representations
[ ] Provide web interface

Technical Implementation:
[ ] All code is commented
[ ] Error handling implemented
[ ] Modular design followed
[ ] All imports are correct
[ ] No unhandled exceptions

Testing Verification:
[ ] All modules tested individually
[ ] API endpoints tested
[ ] Web interface tested
[ ] Integration tested
[ ] Error handling verified
[ ] Performance acceptable

Documentation:
[ ] Code comments present
[ ] Functions have docstrings
[ ] README provided
[ ] Setup instructions complete
[ ] Testing instructions provided

Deliverables:
[ ] All code files present
[ ] Sample data included
[ ] Test results documented
[ ] Screenshots with timestamps
[ ] Properly formatted submission


EXPECTED RESULTS
=================

Sample Run Output:

News Fetcher:
- Fetches 2-4 articles per category
- 4 news sources: BBC, TechCrunch, ESPN, Variety
- Articles have: title, source, content, url, published date

NLP Engine:
- Processes articles correctly
- Removes common English stopwords
- Lemmatizes words to base forms
- Extracts relevant keywords
- Categorizes articles by topic

Summarizer:
- Generates 2-3 sentence summaries
- Compression ratio: 0.3-0.5
- Preserves key information
- Proper sentence ordering

Web Interface:
- Loads at http://localhost:5000
- Category selection works
- Results display within 2-3 seconds
- All articles shown with complete information
- Statistics display correctly
- No JavaScript errors in console

Flask API:
- All endpoints respond with valid JSON
- Proper HTTP status codes returned
- Timestamp on every response
- Consistent response format
- Error messages clear and helpful


END OF TESTING GUIDE
====================
"""

# This file serves as documentation for testing the News Aggregator project.
# Execute the steps in order and verify each checkpoint.
