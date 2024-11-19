import re
import logging
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TextProcessor:
    def __init__(self):
        # Download NLTK resources with comprehensive error handling
        self._download_nltk_resources()

        # Initialize NLTK components
        try:
            self.stop_words = set(stopwords.words('english'))
            self.lemmatizer = WordNetLemmatizer()
        except Exception as e:
            logger.error(f"Error initializing NLTK components: {e}")
            self.stop_words = set()
            self.lemmatizer = None

    def _download_nltk_resources(self):
        """
        Download NLTK resources with comprehensive error handling
        """
        resources = [
            ('punkt', 'Tokenization'),
            ('stopwords', 'Stop Words'),
            ('wordnet', 'Lemmatization')
        ]

        for resource, description in resources:
            try:
                nltk.download(resource, quiet=True)
                logger.info(f"Successfully downloaded {description} resource")
            except Exception as e:
                logger.warning(f"Failed to download {description} resource: {e}")

    def preprocess_text(self, text):
        """
        Comprehensive text preprocessing method

        :param text: Input text to preprocess
        :return: Preprocessed text as a string
        """
        if not text:
            return ''

        try:
            # Lowercase and tokenize
            tokens = word_tokenize(text.lower())

            # Remove stopwords and lemmatize
            cleaned_tokens = [
                self.lemmatizer.lemmatize(token)
                for token in tokens
                if token.isalnum() and token not in self.stop_words
            ]

            return ' '.join(cleaned_tokens)

        except Exception as e:
            logger.error(f"Text preprocessing error: {e}")
            return text.lower()

    def calculate_similarity(self, text1, text2, method='cosine'):
        """
        Calculate text similarity using different methods

        :param text1: First text
        :param text2: Second text
        :param method: Similarity calculation method
        :return: Similarity score
        """
        if not text1 or not text2:
            return 0.0

        try:
            if method == 'cosine':
                vectorizer = TfidfVectorizer()
                tfidf_matrix = vectorizer.fit_transform([
                    self.preprocess_text(text1),
                    self.preprocess_text(text2)
                ])
                return cosine_similarity(tfidf_matrix)[0][1]

            elif method == 'jaccard':
                # Jaccard similarity
                set1 = set(self.preprocess_text(text1).split())
                set2 = set(self.preprocess_text(text2).split())

                intersection = len(set1.intersection(set2))
                union = len(set1.union(set2))

                return intersection / union if union > 0 else 0.0

            else:
                logger.warning(f"Unsupported similarity method: {method}")
                return 0.0

        except Exception as e:
            logger.error(f"Similarity calculation error: {e}")
            return 0.0

    def extract_skills(self, text, custom_skills=None):
        """
        Extract skills from text

        :param text: Input text to extract skills from
        :param custom_skills: Optional custom list of skills
        :return: List of extracted skills
        """
        if not text:
            return []

        # Default skill list
        default_skills = [
            # Technical Skills
            'python', 'django', 'machine learning',
            'data analysis', 'javascript', 'react',
            'sql', 'tensorflow', 'keras',
            'pandas', 'numpy', 'docker',
            'kubernetes', 'aws', 'azure',

            # Soft Skills
            'communication', 'leadership',
            'teamwork', 'problem solving'
        ]

        # Use custom skills if provided, otherwise use default
        skill_keywords = custom_skills or default_skills

        try:
            processed_text = self.preprocess_text(text)

            # Find matching skills (case-insensitive)
            found_skills = [
                skill for skill in skill_keywords
                if skill.lower() in processed_text
            ]

            return list(set(found_skills))

        except Exception as e:
            logger.error(f"Skill extraction error: {e}")
            return []

    def extract_keywords(self, text, top_n=10):
        """
        Extract top keywords from text

        :param text: Input text
        :param top_n: Number of top keywords to return
        :return: List of top keywords
        """
        if not text:
            return []

        try:
            from collections import Counter

            # Preprocess and tokenize text
            processed_text = self.preprocess_text(text)
            tokens = processed_text.split()

            # Count token frequencies
            keyword_freq = Counter(tokens)

            # Return top N keywords
            return [keyword for keyword, _ in keyword_freq.most_common(top_n)]

        except Exception as e:
            logger.error(f"Keyword extraction error: {e}")
            return []

    def anonymize_text(self, text, replacement='[REDACTED]'):
        """
        Anonymize sensitive information in text

        :param text: Input text
        :param replacement: Replacement text for sensitive information
        :return: Anonymized text
        """
        if not text:
            return ''

        try:
            # Regex patterns for sensitive information
            patterns = [
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
                r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',  # Phone number
                r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'  # IP Address
            ]

            anonymized_text = text
            for pattern in patterns:
                anonymized_text = re.sub(pattern, replacement, anonymized_text)

            return anonymized_text

        except Exception as e:
            logger.error(f"Text anonymization error: {e}")
            return text
