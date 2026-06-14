"""
News Fetcher Module
====================
This module is responsible for fetching news articles from various sources using APIs.
It collects articles from multiple news sources and stores them in JSON format for processing.

Author: News Aggregator Project
Date: 2024
"""

import json
import requests
from datetime import datetime

# Define mock API responses since NewsAPI requires authentication
# In production, replace with actual API calls to NewsAPI

class NewsFetcher:
    """
    A class to fetch news articles from various sources.
    This version uses mock data for demonstration purposes.
    """
    
    def __init__(self):
        """
        Initialize the NewsFetcher with mock news sources.
        In production, this would load from news_sources.json with actual API keys.
        """
        # Mock news sources configuration
        self.sources = [
            {"name": "BBC News", "category": "general"},
            {"name": "TechCrunch", "category": "technology"},
            {"name": "ESPN", "category": "sports"},
            {"name": "Variety", "category": "entertainment"},
        ]
        
        # Mock articles database
        self.mock_articles = {
            "general": [
                {
                    "source": "BBC News",
                    "title": "Global Climate Summit Reaches Historic Agreement",
                    "description": "World leaders have reached a groundbreaking agreement on climate change at the annual summit.",
                    "content": "World leaders from over 190 countries have reached a groundbreaking agreement on climate change at the annual summit. The agreement sets ambitious targets for reducing greenhouse gas emissions by 50% before 2050. Scientists hail the accord as a significant step in combating global warming and protecting the environment for future generations. The agreement includes provisions for developing nations to receive financial support for green initiatives.",
                    "url": "https://bbc.com/news/climate-summit",
                    "publishedAt": "2024-01-15T10:30:00Z",
                    "urlToImage": "https://bbc.com/images/climate.jpg"
                },
                {
                    "source": "BBC News",
                    "title": "Stock Market Reaches All-Time High",
                    "description": "Major stock indices hit record levels as investor confidence continues to grow.",
                    "content": "The global stock market has reached an all-time high today, with the S&P 500, Nasdaq, and other major indices showing strong performance. Investors remain optimistic about economic recovery and corporate earnings growth. Analysts attribute the surge to positive economic data and improved business sentiment across multiple sectors.",
                    "url": "https://bbc.com/news/stock-market",
                    "publishedAt": "2024-01-14T14:15:00Z",
                    "urlToImage": "https://bbc.com/images/stock.jpg"
                },
            ],
            "technology": [
                {
                    "source": "TechCrunch",
                    "title": "New AI Breakthrough: Advanced Language Model Released",
                    "description": "Tech companies announce latest advances in artificial intelligence and machine learning.",
                    "content": "Leading technology companies have announced breakthrough developments in artificial intelligence. A new language model with improved reasoning capabilities has been released to researchers and developers. The model shows significant improvements in understanding context, nuance, and complex queries. This advancement is expected to accelerate innovation in various AI applications including virtual assistants, content generation, and automated analysis.",
                    "url": "https://techcrunch.com/ai-breakthrough",
                    "publishedAt": "2024-01-15T08:45:00Z",
                    "urlToImage": "https://techcrunch.com/images/ai.jpg"
                },
                {
                    "source": "TechCrunch",
                    "title": "Quantum Computing Makes Progress",
                    "description": "Researchers announce significant progress in developing practical quantum computers.",
                    "content": "Quantum computing researchers have announced significant progress toward building practical quantum computers. New error correction techniques allow quantum systems to maintain their computational advantage for longer periods. Tech companies like IBM and Google are investing heavily in quantum research, with the expectation that practical quantum computers could solve certain problems exponentially faster than classical computers.",
                    "url": "https://techcrunch.com/quantum",
                    "publishedAt": "2024-01-14T11:20:00Z",
                    "urlToImage": "https://techcrunch.com/images/quantum.jpg"
                },
            ],
            "sports": [
                {
                    "source": "ESPN",
                    "title": "Championship Team Advances to Finals",
                    "description": "In an exciting match, the championship team defeats rivals to advance to the finals.",
                    "content": "In a thrilling match that went into overtime, the championship team defeated their rivals 3-2 to advance to the finals. The star player scored the winning goal with just two minutes remaining in overtime. Fans celebrated as the team secured their place in the championship finals scheduled for next month. The team will face the other semifinal winner in the championship match.",
                    "url": "https://espn.com/sports/championship",
                    "publishedAt": "2024-01-15T19:30:00Z",
                    "urlToImage": "https://espn.com/images/championship.jpg"
                },
                {
                    "source": "ESPN",
                    "title": "Star Athlete Breaks Long-Standing Record",
                    "description": "A legendary athlete shatters a record that has stood for over two decades.",
                    "content": "In a historic moment for sports, a legendary athlete has broken a record that has stood for over twenty years. The record, previously held by another sports icon, was broken during an international competition. Fans around the world celebrated this achievement on social media. The athlete expressed gratitude to their team and coaches for the opportunity to make history.",
                    "url": "https://espn.com/sports/record",
                    "publishedAt": "2024-01-14T16:45:00Z",
                    "urlToImage": "https://espn.com/images/record.jpg"
                },
            ],
            "entertainment": [
                {
                    "source": "Variety",
                    "title": "New Blockbuster Film Breaks Box Office Records",
                    "description": "A highly anticipated film has shattered box office records on its opening weekend.",
                    "content": "A long-awaited blockbuster film has shattered box office records, earning over $500 million in its opening weekend globally. The film, based on a popular book series, features an all-star cast and cutting-edge special effects. Critics have praised the film for its engaging storyline and stunning visuals. The studio has announced plans for sequels given the overwhelming commercial success.",
                    "url": "https://variety.com/entertainment/blockbuster",
                    "publishedAt": "2024-01-15T20:00:00Z",
                    "urlToImage": "https://variety.com/images/blockbuster.jpg"
                },
                {
                    "source": "Variety",
                    "title": "Award-Winning Series Announces Final Season",
                    "description": "A popular television series announces that the upcoming season will be its final one.",
                    "content": "A critically acclaimed television series has announced that the upcoming season will be its final one. The announcement has sparked emotional reactions from fans who have followed the show since its debut. The final season will consist of ten episodes and air over the next three months. The showrunner has promised a satisfying conclusion to the complex and beloved series.",
                    "url": "https://variety.com/entertainment/series",
                    "publishedAt": "2024-01-14T18:10:00Z",
                    "urlToImage": "https://variety.com/images/series.jpg"
                },
            ]
        }
    
    def fetch_news(self, category="general"):
        """
        Fetch news articles for a specific category.
        
        Args:
            category (str): The news category to fetch (general, technology, sports, entertainment)
            
        Returns:
            list: A list of article dictionaries
        """
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Fetching {category} news...")
        
        # Return mock articles for the requested category
        if category in self.mock_articles:
            articles = self.mock_articles[category]
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Successfully fetched {len(articles)} articles from {category}")
            return articles
        else:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Category '{category}' not found. Returning general news.")
            return self.mock_articles.get("general", [])
    
    def fetch_all_news(self):
        """
        Fetch news from all categories.
        
        Returns:
            dict: A dictionary with categories as keys and article lists as values
        """
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Fetching all news from all categories...")
        all_articles = {}
        
        for category in self.mock_articles.keys():
            all_articles[category] = self.fetch_news(category)
        
        return all_articles
    
    def save_articles_to_file(self, articles, filename='data/articles.json'):
        """
        Save fetched articles to a JSON file.
        
        Args:
            articles (list or dict): Articles to save
            filename (str): Output file path
        """
        try:
            with open(filename, 'w') as f:
                json.dump(articles, f, indent=4)
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Articles saved to {filename}")
        except Exception as e:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error saving articles: {str(e)}")
    
    def load_articles_from_file(self, filename='data/articles.json'):
        """
        Load articles from a JSON file.
        
        Args:
            filename (str): Input file path
            
        Returns:
            list or dict: Loaded articles
        """
        try:
            with open(filename, 'r') as f:
                articles = json.load(f)
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Articles loaded from {filename}")
            return articles
        except FileNotFoundError:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] File {filename} not found")
            return []
        except Exception as e:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error loading articles: {str(e)}")
            return []


# Main execution
if __name__ == "__main__":
    # Create a NewsFetcher instance
    fetcher = NewsFetcher()
    
    # Fetch news for different categories
    print("\n" + "="*70)
    print("NEWS FETCHER - DEMONSTRATION")
    print("="*70)
    
    # Test fetching news by category
    print("\n1. Fetching Technology News:")
    print("-" * 70)
    tech_news = fetcher.fetch_news("technology")
    for article in tech_news:
        print(f"\nTitle: {article['title']}")
        print(f"Source: {article['source']}")
        print(f"Published: {article['publishedAt']}")
    
    # Test fetching all news
    print("\n\n2. Fetching All News Categories:")
    print("-" * 70)
    all_news = fetcher.fetch_all_news()
    for category, articles in all_news.items():
        print(f"\n{category.upper()}: {len(articles)} articles")
    
    # Save articles to file
    print("\n\n3. Saving Articles to File:")
    print("-" * 70)
    fetcher.save_articles_to_file(all_news)
    
    # Load articles from file
    print("\n4. Loading Articles from File:")
    print("-" * 70)
    loaded_articles = fetcher.load_articles_from_file()
    
    print("\n" + "="*70)
    print("NEWS FETCHER DEMONSTRATION COMPLETE")
    print("="*70)
