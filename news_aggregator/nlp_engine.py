"""
Simple NLPEngine for the News Aggregator
Provides lightweight preprocessing, categorization and keyword extraction utilities
This is a minimal implementation to satisfy the app's API and avoid NameErrors.
"""
from datetime import datetime
import re
from collections import Counter
from typing import List, Dict, Any

from summarizer import TextSummarizer


class NLPEngine:
    def __init__(self):
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] NLPEngine initialized")
        self.summarizer = TextSummarizer()

        # Simple keyword lists for coarse categorization
        self.category_keywords = {
            'technology': ['technology', 'ai', 'artificial', 'machine learning', 'tech', 'software', 'computer'],
            'sports': ['football', 'soccer', 'basketball', 'tennis', 'cricket', 'athlete', 'game'],
            'entertainment': ['movie', 'film', 'music', 'celebrity', 'tv', 'concert', 'show'],
            'business': ['market', 'economy', 'business', 'finance', 'stock', 'company'],
            'health': ['health', 'medical', 'doctor', 'covid', 'vaccine', 'disease'],
            'science': ['research', 'science', 'space', 'nasa', 'study']
        }

    def _clean_text(self, text: str) -> str:
        if not text:
            return ""
        # Basic cleanup: remove extra whitespace and control chars
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def preprocess_articles(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Return a list of articles with cleaned content and basic metadata."""
        preprocessed = []
        for a in articles:
            content = a.get('content') or a.get('description') or ''
            cleaned = self._clean_text(content)
            preprocessed.append({
                'source': a.get('source', 'Unknown'),
                'title': a.get('title', ''),
                'cleaned_content': cleaned,
                'url': a.get('url', ''),
                'publishedAt': a.get('publishedAt', '')
            })
        return preprocessed

    def generate_statistics(self, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate simple statistics for a list of articles or raw text list."""
        try:
            total = len(articles)
            lengths = []
            for a in articles:
                # Accept either dicts with content keys or raw strings
                if isinstance(a, dict):
                    content = a.get('content') or a.get('description') or a.get('original_content') or ''
                else:
                    content = str(a)
                lengths.append(len(content))

            avg_length = sum(lengths) / total if total else 0
            sources = {a.get('source', 'Unknown') for a in articles if isinstance(a, dict)}
            stats = {
                'total_articles': total,
                'num_sources': len(sources),
                'average_length_chars': int(avg_length),
                'avg_content_length': int(avg_length),
            }
            return stats
        except Exception:
            return {
                'total_articles': 0,
                'num_sources': 0,
                'average_length_chars': 0,
                'avg_content_length': 0,
            }

    def categorize_article(self, content: str, use_keywords: bool = True) -> str:
        """Naive keyword-based categorization."""
        text = (content or '').lower()
        if not text:
            return 'general'

        if use_keywords:
            scores = Counter()
            for cat, keys in self.category_keywords.items():
                for k in keys:
                    if k in text:
                        scores[cat] += 1
            if scores:
                return scores.most_common(1)[0][0]

        # fallback
        return 'general'

    def extract_keywords(self, content: str, num_keywords: int = 5) -> List[str]:
        """Extract top `num_keywords` using frequency distribution from the summarizer utilities."""
        text = (content or '').lower()
        if not text:
            return []

        freq = self.summarizer.calculate_word_frequencies(text)
        common = [w for w, _ in freq.most_common(num_keywords)]
        return common


if __name__ == '__main__':
    engine = NLPEngine()
    print('NLPEngine ready')
