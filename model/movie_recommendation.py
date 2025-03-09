import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib

# Load the dataset (replace with the path to your dataset file)
# The dataset should have 'movieId', 'title', and 'genres' columns.
movies = pd.read_csv('data/movies.csv')  # Assuming movies.csv contains 'movieId', 'title', 'genres'

# Preprocessing the genres data (remove any leading/trailing spaces)
movies['genres'] = movies['genres'].apply(lambda x: x.strip())

# Use TF-IDF to convert genres into numerical format
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
genre_matrix = tfidf_vectorizer.fit_transform(movies['genres'])

# Compute cosine similarity between all movies based on their genres
cosine_sim = cosine_similarity(genre_matrix, genre_matrix)

# Save the cosine similarity matrix and movie titles into files
joblib.dump(cosine_sim, 'cosine_sim.pkl')  # Save cosine similarity matrix
joblib.dump(movies['title'].tolist(), 'movie_titles.pkl')  # Save movie titles

print("Model saved successfully!")
