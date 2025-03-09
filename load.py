import pickle

cosine_sim_path = '/cosine_sim.pkl'
movie_titles_path = '/movie_titles.pkl'

# Try loading the files
try:
    with open(cosine_sim_path, 'rb') as f:
        cosine_sim = pickle.load(f)
        print("Cosine similarity matrix loaded successfully.")
except Exception as e:
    print(f"Error loading cosine_sim.pkl: {e}")

try:
    with open(movie_titles_path, 'rb') as f:
        movie_titles = pickle.load(f)
        print("Movie titles loaded successfully.")
except Exception as e:
    print(f"Error loading movie_titles.pkl: {e}")

print(cosine_sim[:5])  # Print first 5 rows to check the structure