import json
import urllib.request
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response

# Replace with your ngrok URL
API_URL = 'https://3ad1-138-199-46-6.ngrok-free.app/recommend'

# Function to fetch movie recommendations from FastAPI server using urllib
def fetch_movie_recommendation(movie_name):
    try:
        # Prepare the URL with query parameters (movie name)
        url = f"{API_URL}?movie_name={urllib.parse.quote(movie_name)}"

        # Send the HTTP GET request to the FastAPI server
        with urllib.request.urlopen(url) as response:
            # Read the response and parse it as JSON
            recommendations = json.loads(response.read().decode())

        if 'recommended_movies' in recommendations:
            return recommendations['recommended_movies']
        else:
            return f"Sorry, I couldn't find any recommendations for {movie_name}."
    except Exception as e:
        print(f"Error: {str(e)}")
        return 'Sorry, there was an error processing your request.'

class MovieRecommendationIntentHandler:
    def can_handle(self, handler_input: HandlerInput):
        return handler_input.request_envelope.request.intent.name == 'MovieRecommendationIntent'

    def handle(self, handler_input: HandlerInput):
        # Getting the movie name from the slot
        movie_name = handler_input.request_envelope.request.intent.slots['MovieName'].value

        # Fetching the movie recommendation from the FastAPI server
        recommended_movies = fetch_movie_recommendation(movie_name)

        if isinstance(recommended_movies, list):
            # Handle the case where recommendations are returned as a list
            recommended_movie = ', '.join(recommended_movies)
            speech_output = f'Based on {movie_name}, I recommend you watch: {recommended_movie}'
        else:
            # Handle the error case
            speech_output = recommended_movies

        return handler_input.response_builder.speak(speech_output).response


# Lambda function handler for Alexa request
def lambda_handler(event, context):
    skill_builder = SkillBuilder()
    skill_builder.add_request_handler(MovieRecommendationIntentHandler())
    return skill_builder.lambda_handler()(event, context)
