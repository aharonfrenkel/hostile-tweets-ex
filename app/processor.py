from collections import Counter
from typing import Self

import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')


WEAPON_LIST = pd.read_csv("../data/weapon_list.txt", header=None)[0].tolist()


class Processor:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.analyzer = SentimentIntensityAnalyzer()

    def find_rarest_word(self) -> Self:
        """Find the rarest word in each text"""
        self.data["rarest_word"] = self.data["Text"].apply(self._rarest_word)
        return self

    def find_sentiment(self) -> Self:
        """Find sentiment of each text using VADER"""
        self.data["sentiment"] = self.data["Text"].apply(self._analyze_sentiment)
        return self

    def find_weapon(self) -> Self:
        """Find weapons in each text based on blacklist"""
        self.data["weapons_detected"] = self.data["Text"].apply(self._find_weapon)
        return self

    def _find_weapon(text: str):
        words = text.split()
        for word in words:
            if word in WEAPON_LIST:
                return word
        return None

    def _rarest_word(text: str):
        words = text.split()
        counts = Counter(words)
        return min(counts, key=counts.get)

    def _analyze_sentiment(self, text: str) -> str:
        """
        Analyze sentiment using VADER
        Returns: 'positive', 'negative', or 'neutral'
        """
        if pd.isna(text) or not isinstance(text, str):
            return "neutral"

        try:
            score = self.analyzer.polarity_scores(text)
            compound = score['compound']

            # Based on the requirements:
            # Positive: 0.5 to 1
            # Neutral: -0.49 to 0.49
            # Negative: -1 to -0.5
            if compound >= 0.5:
                return "positive"
            elif compound <= -0.5:
                return "negative"
            else:
                return "neutral"

        except Exception as e:
            print(f"Error analyzing sentiment for text: {e}")
            return "neutral"

    def process_all(self) -> Self:
        """Process all features in one call"""
        return self.find_rarest_word().find_sentiment().find_weapon()