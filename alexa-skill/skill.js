const Alexa = require('ask-sdk-core');
const joblib = require('joblib');
const path = require('path');

// Load pre-trained cosine similarity matrix and movie titles
const cosineSim = joblib.load(path.resolve(__dirname, '../model/cosine_sim.pkl'));
const movieTitles = joblib.load(path.resolve(__dirname, '../model/movie_titles.pkl'));

// Handler for the MovieRecommendationIntent
const MovieRecommendationIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'MovieRecommendationIntent';
    },
    handle(handlerInput) {
        const movieName = Alexa.getSlotValue(handlerInput.requestEnvelope, 'MovieName');
        const movieIndex = movieTitles.indexOf(movieName);

        if (movieIndex !== -1) {
            const simScores = cosineSim[movieIndex];
            const recommendedMovies = simScores
                .map((score, idx) => ({ score, movie: movieTitles[idx] }))
                .sort((a, b) => b.score - a.score)
                .slice(1, 6) // Get top 5 recommendations
                .map(item => item.movie);

            const speakOutput = `If you liked ${movieName}, you might also enjoy ${recommendedMovies.join(', ')}.`;
            return handlerInput.responseBuilder.speak(speakOutput).getResponse();
        } else {
            return handlerInput.responseBuilder.speak(`Sorry, I couldn't find a movie by the name ${movieName}. Please try again.`).getResponse();
        }
    }
};

// Lambda function export
exports.handler = Alexa.SkillBuilders.custom()
    .addRequestHandlers(MovieRecommendationIntentHandler)
    .lambda();
