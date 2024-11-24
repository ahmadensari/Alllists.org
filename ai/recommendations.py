from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class RecommendationEngine:
    def __init__(self, lists):
        self.lists = lists

    def recommend(self, user_input):
        if not self.lists:
            return []
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([list['description'] for list in self.lists])
        user_vec = vectorizer.transform([user_input])
        similarity_scores = cosine_similarity(user_vec, tfidf_matrix)
        recommendations = sorted(
            zip(self.lists, similarity_scores[0]),
            key=lambda x: x[1],
            reverse=True
        )
        return [rec[0] for rec in recommendations[:5]]
