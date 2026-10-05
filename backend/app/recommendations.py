class RecommendationEngine:
    """Rank lists against a text query using TF-IDF and cosine similarity."""

    def __init__(self, lists):
        self.lists = lists

    def recommend(self, user_input, limit=5):
        if not self.lists or not user_input or not user_input.strip():
            return []

        # Imported here so the rest of the app starts even if scikit-learn is slow to load.
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity

        documents = [f"{item.get('name', '')} {item.get('description') or ''}" for item in self.lists]
        try:
            vectorizer = TfidfVectorizer()
            matrix = vectorizer.fit_transform(documents)
        except ValueError:  # every document is empty
            return []

        scores = cosine_similarity(vectorizer.transform([user_input]), matrix)[0]
        ranked = sorted(zip(self.lists, scores), key=lambda pair: pair[1], reverse=True)
        return [item for item, score in ranked[:limit] if score > 0]
