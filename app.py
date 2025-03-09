from fastapi import FastAPI
import joblib
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

# Load the pre-trained cosine similarity model and movie titles
cosine_sim = joblib.load('model/cosine_sim.pkl')
movie_titles = joblib.load('model/movie_titles.pkl')


@app.get("/recommend")
def recommend_movie(movie_name: str):
    try:
        # Find the movie index from movie_titles
        if movie_name not in movie_titles:
            return {"error": "Movie not found."}

        movie_index = movie_titles.index(movie_name)

        # Get the similarity scores for the given movie
        similarity_scores = list(enumerate(cosine_sim[movie_index]))

        # Sort the movies by similarity
        sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

        # Return the top 5 recommended movies
        recommended_movies = []
        for i in range(1, 6):  # Skipping the first movie as it's the input movie itself
            idx = sorted_scores[i][0]
            recommended_movies.append(movie_titles[idx])

        return {"recommended_movies": recommended_movies}

    except Exception as e:
        return {"error": str(e)}
