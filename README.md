# Movie Recommendation System Documentation

## Overview

I've been working with this movie recommendation system that uses machine learning to suggest similar movies based on content analysis. After spending time understanding and testing the codebase, I wanted to document my experience and provide a guide for other developers.

The system analyzes movie metadata (genres, keywords, cast, director) and uses content-based filtering to make recommendations. It's built with Python and uses TF-IDF vectorization with cosine similarity - pretty standard ML approach but works well.

**Original Project**: https://github.com/yvidhya/Movie-Recommendation-System

## What You'll Need

Based on my setup experience, here's what you need to get this running:

### Software Requirements
- **Python 3.7+** (I used 3.9 and it worked fine)
- **pip** for package management
- **Git** to clone the repo


## Getting Started

Here's how I got everything set up:

### 1. Clone and Setup
```bash
# Get the code
git clone https://github.com/yvidhya/Movie-Recommendation-System.git
cd Movie-Recommendation-System

#Create a virtual environment 
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
# Install the main packages
pip install pandas numpy scikit-learn flask jupyter

#Requirements.txt 
pip install -r requirements.txt
```

### 3. Get the Dataset
You'll need a movies.csv file. I downloaded mine from Kaggle's movie dataset. Make sure it has these columns:
- `title`, `genres`, `keywords`, `cast`, `director`, `tagline`

Place it in the main project directory.

## Running the Project

I found three ways to run this, depending on what you want to do:

### Option 1: Jupyter Notebook 
```bash
jupyter notebook
```
Then open the main notebook file. This is great for experimenting and understanding how everything works.

### Option 2: Flask API
```bash
python app.py
```
This starts a web server at `http://localhost:5000`. You can then make API calls to get recommendations.

### Option 3: Direct Python Script
```bash
python main.py
```
Runs the recommendation engine directly in the terminal.

## Key Functions I Analyzed

After digging through the code, I found two functions that are central to how this whole system works:

### 1. `load_and_preprocess_data()`

This function handles all the data cleaning and preparation. Here's what I learned about it:

**What it does**: Takes the raw CSV data and cleans it up for the ML algorithms.

**Parameters**:
- `file_path` (string): Path to your movies.csv file
- `columns` (list, optional): Which columns to load (useful for large datasets)

**The preprocessing steps**:
1. Loads the CSV with pandas
2. Handles missing values (fills empty genres with "Unknown", etc.)
3. Combines text features (genres + keywords + cast + director)
4. Cleans up the text (removes special characters, normalizes)

**Returns**: 
- Cleaned DataFrame and combined text features ready for vectorization

**Example**:
```python
movies_df, features = load_and_preprocess_data('movies.csv')
print(f"Loaded {len(movies_df)} movies")
```

**Issues I ran into**: 
- Some CSV files have encoding issues - try adding `encoding='utf-8'` if you get errors
- Missing data can break things, so the function handles this pretty well

### 2. `get_movie_recommendations()`

This is the heart of the recommendation system. After studying it, here's how it works:

**What it does**: Takes a movie title and finds similar movies using TF-IDF and cosine similarity.

**Parameters**:
- `movie_title` (string): The movie you want recommendations for
- `movies_df` (DataFrame): Your preprocessed movie data
- `n_recommendations` (int): How many suggestions you want (default is 10)
- `similarity_threshold` (float): Minimum similarity score to include

**The algorithm**:
1. Checks if the movie exists in the dataset
2. Creates TF-IDF vectors from the combined text features
3. Calculates cosine similarity between all movies
4. Ranks movies by similarity score
5. Returns the top N recommendations

**Returns**: List of dictionaries with movie info and similarity scores

**Example**:
```python
recommendations = get_movie_recommendations(
    movie_title="The Dark Knight",
    movies_df=movies_df,
    n_recommendations=5
)

for movie in recommendations:
    print(f"{movie['title']} - Score: {movie['similarity_score']:.3f}")
```


## API Usage

If you run the Flask version, you can make HTTP requests:

```bash
# Get recommendations
curl "http://localhost:5000/recommend?movie=The%20Dark%20Knight&count=5"

# Search for movies
curl "http://localhost:5000/search?query=batman"
```

## Issues I Fixed

### Package Installation Problems
If you get `ModuleNotFoundError`, make sure you're in your virtual environment:
```bash
# Check if you're in the right environment
which python
pip list

# Install missing packages
pip install scikit-learn pandas numpy flask
```

### Dataset Issues
The biggest issue was getting the right dataset format. If you get file errors:
1. Double-check the file path
2. Make sure your CSV has the right columns
3. Try a smaller dataset first (like 1000 movies) to test

### Memory Problems
With large datasets, I ran into memory issues. Solutions:
```python
# Limit dataset size for testing
movies_df = movies_df.head(5000)

# Reduce TF-IDF features
vectorizer = TfidfVectorizer(max_features=1000)
```

### Port Conflicts
If Flask won't start because port 5000 is busy:
```python
# In app.py, change the port
app.run(debug=True, port=5001)
```

## Performance Notes

From my testing:
- **Small datasets** (1000 movies): Near-instant recommendations
- **Medium datasets** (10,000 movies): 2-3 seconds
- **Large datasets** (50,000+ movies): 10+ seconds, high memory usage

The system works well for typical use cases but might need optimization for production use.

## What I'd Improve

After working with this system, here are some ideas for enhancement:
1. Add user ratings and collaborative filtering
2. Cache similarity matrices for faster repeated queries
3. Add more sophisticated text preprocessing
4. Create a better web interface
5. Add evaluation metrics to measure recommendation quality

## Final Thoughts

This is a solid implementation of content-based recommendation. The code is clean and well-structured, making it easy to understand and modify. It's a great starting point for learning about recommendation systems or building something more sophisticated.

The main limitation is that it only considers content similarity, not user preferences or ratings. But for a content-based system, it does exactly what it's supposed to do.

Feel free to reach out if you run into issues or want to discuss improvements!