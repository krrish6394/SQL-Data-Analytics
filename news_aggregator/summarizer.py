"""
Text Summarizer Module
======================
This module implements both extractive and abstractive text summarization.
- Extractive Summarization: Selects important sentences from original text
- Abstractive Summarization: Generates new summary using pre-trained models

Author: News Aggregator Project
Date: 2024
"""

import nltk
import string
from datetime import datetime
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist

# Download required NLTK resources
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')


class TextSummarizer:
    """
    A class for summarizing text using extractive summarization methods.
    """
    
    def __init__(self):
        """
        Initialize the TextSummarizer.
        """
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Text Summarizer initialized")
    
    def extract_sentences(self, text):
        """
        Extract sentences from text.
        
        Args:
            text (str): Input text
            
        Returns:
            list: List of sentences
        """
        try:
            sentences = sent_tokenize(text)
            return sentences
        except Exception as e:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error extracting sentences: {str(e)}")
            return []
    
    def calculate_word_frequencies(self, text):
        """
        Calculate word frequencies in text.
        
        Args:
            text (str): Input text
            
        Returns:
            FreqDist: Frequency distribution of words
        """
        try:
            # Tokenize and convert to lowercase
            words = word_tokenize(text.lower())
            
            # Remove punctuation and stopwords
            stop_words = set(stopwords.words('english'))
            words = [
                word for word in words 
                if word not in string.punctuation and word not in stop_words
            ]
            
            # Calculate frequencies
            freq_dist = FreqDist(words)
            
            return freq_dist
        except Exception as e:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error calculating frequencies: {str(e)}")
            return FreqDist()
    
    def score_sentences(self, sentences, freq_dist):
        """
        Score sentences based on word frequencies.
        
        Args:
            sentences (list): List of sentences
            freq_dist (FreqDist): Word frequency distribution
            
        Returns:
            dict: Sentence scores
        """
        sentence_scores = {}
        
        for sentence in sentences:
            words = word_tokenize(sentence.lower())
            
            # Sum up frequencies for each word in the sentence
            score = 0
            for word in words:
                if word in freq_dist:
                    score += freq_dist[word]
            
            # Store the score
            if score > 0:
                sentence_scores[sentence] = score
        
        return sentence_scores
    
    def extractive_summarize(self, text, num_sentences=3):
        """
        Generate an extractive summary of text.
        
        Args:
            text (str): Input text to summarize
            num_sentences (int): Number of sentences in the summary
            
        Returns:
            str: Summarized text
        """
        try:
            # Validate input
            if not text or len(text.strip()) == 0:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Empty text provided for summarization")
                return ""
            
            # Extract sentences
            sentences = self.extract_sentences(text)
            
            # Handle case where we have fewer sentences than requested
            if len(sentences) <= num_sentences:
                return text
            
            # Calculate word frequencies
            freq_dist = self.calculate_word_frequencies(text)
            
            # Score sentences
            sentence_scores = self.score_sentences(sentences, freq_dist)
            
            # Select top sentences
            if len(sentence_scores) == 0:
                return sentences[0]  # Return first sentence if no scoring worked
            
            # Sort sentences by score
            sorted_sentences = sorted(
                sentence_scores.items(),
                key=lambda x: x[1],
                reverse=True
            )
            
            # Select top N sentences
            top_sentences = [sent for sent, score in sorted_sentences[:num_sentences]]
            
            # Maintain original sentence order
            summary_sentences = [sent for sent in sentences if sent in top_sentences]
            
            # Combine into summary
            summary = ' '.join(summary_sentences)
            
            return summary
        
        except Exception as e:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error in extractive summarization: {str(e)}")
            return text[:200] + "..."
    
    def abstractive_summarize_simple(self, text, max_length=100):
        """
        Generate a simple abstractive-style summary (for demo purposes).
        This is a simplified version that combines key sentences and creates a new heading.
        
        Args:
            text (str): Input text to summarize
            max_length (int): Maximum length of summary
            
        Returns:
            str: Summarized text
        """
        try:
            # Get extractive summary
            extractive = self.extractive_summarize(text, num_sentences=2)
            
            # Truncate if needed
            if len(extractive) > max_length:
                extractive = extractive[:max_length].rsplit(' ', 1)[0] + "..."
            
            return extractive
        
        except Exception as e:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error in abstractive summarization: {str(e)}")
            return text[:max_length] + "..."
    
    def get_summary_statistics(self, original_text, summary_text):
        """
        Calculate statistics about the summarization.
        
        Args:
            original_text (str): Original text
            summary_text (str): Summarized text
            
        Returns:
            dict: Statistics dictionary
        """
        stats = {
            'original_length': len(original_text),
            'summary_length': len(summary_text),
            'original_word_count': len(original_text.split()),
            'summary_word_count': len(summary_text.split()),
            'compression_ratio': round(len(summary_text) / len(original_text), 2) if original_text else 0,
            'word_reduction_ratio': round(
                (len(original_text.split()) - len(summary_text.split())) / len(original_text.split()),
                2
            ) if original_text.split() else 0
        }
        
        return stats
    
    def summarize_articles(self, articles, num_sentences=3):
        """
        Summarize multiple articles.
        
        Args:
            articles (list): List of article dictionaries
            num_sentences (int): Number of sentences per summary
            
        Returns:
            list: Articles with summaries
        """
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Summarizing {len(articles)} articles...")
        
        summarized_articles = []
        
        for i, article in enumerate(articles):
            # Get content
            content = article.get('content') or article.get('description') or ""
            
            # Generate summary
            summary = self.extractive_summarize(content, num_sentences=num_sentences)
            
            # Create summarized article
            summarized_article = {
                'source': article.get('source', 'Unknown'),
                'title': article.get('title', 'No title'),
                'original_content': content,
                'summary': summary,
                'url': article.get('url', ''),
                'publishedAt': article.get('publishedAt', ''),
                'urlToImage': article.get('urlToImage', ''),
                'statistics': self.get_summary_statistics(content, summary)
            }
            
            summarized_articles.append(summarized_article)
            
            if (i + 1) % 5 == 0:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Summarized {i + 1}/{len(articles)} articles")
        
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Summarization complete")
        
        return summarized_articles


# Main execution
if __name__ == "__main__":
    print("\n" + "="*70)
    print("TEXT SUMMARIZER - DEMONSTRATION")
    print("="*70)
    
    # Create summarizer instance
    summarizer = TextSummarizer()
    
    # Sample long text for testing
    sample_text = """
    Natural language processing (NLP) is a subfield of linguistics, computer science, 
    and artificial intelligence concerned with the interactions between computers and human language. 
    In particular, it is about how to program computers to process and analyze large amounts of natural 
    language data. The result is a computer capable of "understanding" the contents of documents, 
    including the contextual nuances of the language within them. The technology can then accurately 
    extract information and insights contained in the documents as well as categorize and organize 
    the documents themselves.
    
    NLP has become increasingly important in various applications such as machine translation, 
    sentiment analysis, question answering, and chatbots. Machine learning and deep learning 
    techniques have revolutionized the field, enabling more sophisticated and accurate models. 
    These models can understand complex linguistic patterns and relationships in text data.
    
    The field continues to evolve with new techniques and approaches being developed regularly. 
    Recent advances in transformer-based models like BERT and GPT have achieved state-of-the-art 
    results on many NLP tasks. These models are trained on massive amounts of text data and can 
    be fine-tuned for specific applications.
    """
    
    # Test sentence extraction
    print("\n1. Sentence Extraction:")
    print("-" * 70)
    sentences = summarizer.extract_sentences(sample_text)
    print(f"Number of sentences: {len(sentences)}")
    for i, sent in enumerate(sentences[:3], 1):
        print(f"{i}. {sent[:80]}...")
    
    # Test word frequency calculation
    print("\n2. Word Frequency Analysis:")
    print("-" * 70)
    freq_dist = summarizer.calculate_word_frequencies(sample_text)
    print("Top 10 most common words:")
    for word, freq in freq_dist.most_common(10):
        print(f"  {word}: {freq}")
    
    # Test extractive summarization
    print("\n3. Extractive Summarization (3 sentences):")
    print("-" * 70)
    summary = summarizer.extractive_summarize(sample_text, num_sentences=3)
    print(f"Summary:\n{summary}")
    
    # Test abstractive summarization
    print("\n4. Abstractive Summarization (simplified):")
    print("-" * 70)
    abstract_summary = summarizer.abstractive_summarize_simple(sample_text, max_length=150)
    print(f"Summary:\n{abstract_summary}")
    
    # Test summarization statistics
    print("\n5. Summarization Statistics:")
    print("-" * 70)
    stats = summarizer.get_summary_statistics(sample_text, summary)
    print(f"Original length: {stats['original_length']} characters")
    print(f"Summary length: {stats['summary_length']} characters")
    print(f"Original words: {stats['original_word_count']}")
    print(f"Summary words: {stats['summary_word_count']}")
    print(f"Compression ratio: {stats['compression_ratio']}")
    print(f"Word reduction: {stats['word_reduction_ratio']}")
    
    # Test with multiple articles
    print("\n6. Summarizing Multiple Articles:")
    print("-" * 70)
    sample_articles = [
        {
            'source': 'BBC',
            'title': 'Climate Change Article',
            'content': sample_text,
            'description': 'NLP article',
            'url': 'https://example.com/1',
            'publishedAt': '2024-01-15',
            'urlToImage': 'https://example.com/image1.jpg'
        },
        {
            'source': 'CNN',
            'title': 'Technology Article',
            'content': "Technology is changing the world. Artificial intelligence is transforming industries. Machine learning models are becoming more sophisticated.",
            'description': 'Tech news',
            'url': 'https://example.com/2',
            'publishedAt': '2024-01-15',
            'urlToImage': 'https://example.com/image2.jpg'
        }
    ]
    
    summarized = summarizer.summarize_articles(sample_articles, num_sentences=2)
    
    for article in summarized:
        print(f"\nTitle: {article['title']}")
        print(f"Original length: {article['statistics']['original_length']} chars")
        print(f"Summary: {article['summary'][:100]}...")
    
    print("\n" + "="*70)
    print("TEXT SUMMARIZER DEMONSTRATION COMPLETE")
    print("="*70)
