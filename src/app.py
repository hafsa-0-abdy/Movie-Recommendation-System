from flask import Flask, request, jsonify
from recommendation import MovieRecommender

app = Flask(__name__)
recommender = MovieRecommender("../data/movies.csv")  # Update with actual path

@app.route('/recommend', methods=['GET'])
def recommend():
    movie_name = request.args.get('title')
    num_recommendations = int(request.args.get('num', 5))
    recommendations = recommender.recommend(movie_name, num_recommendations)
    return jsonify({"recommended_movies": recommendations})

if __name__ == '__main__':
    app.run(debug=True)
