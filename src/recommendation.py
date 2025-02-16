import numpy as np
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class MovieRecommender:
    def __init__(self, data_path):
        self.movie_data = pd.read_csv(data_path)
        self._prepare_data()

    def _prepare_data(self):
        featured_features = ['genres', 'keywords', 'tagline', 'cast', 'director']
        for feature in featured_features:
            self.movie_data[feature] = self.movie_data[feature].fillna('')
        
        combined_features = self.movie_data['genres'] + ' ' + self.movie_data['keywords'] + ' ' + self.movie_data['tagline'] + ' ' + self.movie_data['cast'] + ' ' + self.movie_data['director']
        vectorizer = TfidfVectorizer(stop_words='english')
        self.feat_vector = vectorizer.fit_transform(combined_features)
        self.similar = cosine_similarity(self.feat_vector)

    def recommend(self, movie_name, num_recommendations=10):
        list_all_titles = self.movie_data['title'].tolist()
        close_matches = difflib.get_close_matches(movie_name, list_all_titles)
        
        if not close_matches:
            return ["No matching movies found."]

        close_match = close_matches[0]
        index_movie = self.movie_data[self.movie_data.title == close_match].index[0]
        similar_score = list(enumerate(self.similar[index_movie]))
        sorted_similar_movies = sorted(similar_score, key=lambda x: x[1], reverse=True)[1:num_recommendations+1]

        recommendations = [self.movie_data.iloc[index]['title'] for index, _ in sorted_similar_movies]
        return recommendations
