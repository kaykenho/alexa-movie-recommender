# Movie Recommender Alexa Skill

A complete voice-driven movie recommendation system built with Amazon Alexa and AWS Lambda that provides personalized movie recommendations based on user preferences.

## Table of Contents

- [Overview](#overview)
- [Project Architecture](#project-architecture)
- [Components](#components)
  - [Movie Recommendation API](#movie-recommendation-api)
  - [Alexa Skill](#alexa-skill)
  - [AWS Lambda Function](#aws-lambda-function)
- [Setup and Deployment](#setup-and-deployment)
  - [API Setup](#api-setup)
  - [Lambda Function Setup](#lambda-function-setup)
  - [Alexa Skill Setup](#alexa-skill-setup)
- [Testing](#testing)
  - [Lambda Testing](#lambda-testing)
  - [Alexa Skill Testing](#alexa-skill-testing)
- [User Interaction Flow](#user-interaction-flow)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)

## Overview

The Movie Recommender Alexa Skill allows users to get personalized movie recommendations through voice interaction. Users can tell Alexa a movie they like, and the system will suggest similar movies they might enjoy.

Key features:
- Voice-activated movie recommendations
- Similarity-based recommendation algorithm
- Multi-turn conversations (ability to ask for more recommendations)
- Seamless integration between Alexa and a custom recommendation API

## Project Architecture

The system consists of three main components:

1. **Movie Recommendation API**: A FastAPI-based service that provides movie recommendations based on cosine similarity.
2. **AWS Lambda Function**: Processes Alexa requests and communicates with the API.
3. **Alexa Skill**: The voice interface that users interact with.

```
+----------------+       +------------------+       +----------------------+
|                |       |                  |       |                      |
|  Alexa Skill   | <---> |  Lambda Function | <---> | Recommendation API   |
|                |       |                  |       |                      |
+----------------+       +------------------+       +----------------------+
```

## Components

### Movie Recommendation API

A FastAPI-based API that provides movie recommendations using cosine similarity.

**Key Features:**
- Content-based recommendation algorithm using cosine similarity
- Pre-trained model stored in pickle files
- Configurable number of recommendations
- Error handling for unknown movies

**Files:**
- `app.py`: Main FastAPI application
- `model/cosine_sim.pkl`: Pre-computed cosine similarity matrix
- `model/movie_titles.pkl`: List of movie titles

### Alexa Skill

The Alexa Skill provides the voice interface users interact with.

**Key Features:**
- Custom invocation name: "movie recommender"
- Natural language interaction
- Multi-turn conversation support
- Session persistence for ongoing recommendations

**Interaction Model:**
- Invocation: "Alexa, open movie recommender"
- Sample Utterances:
  - "I like The Matrix"
  - "Recommend me something like Inception"
  - "More recommendations"

### AWS Lambda Function

The Lambda function processes requests from the Alexa Skill and communicates with the recommendation API.

**Key Features:**
- Handles different Alexa intent types
- Manages conversation state
- Communicates with the recommendation API
- Implements error handling and fallbacks

**Files:**
- `lambda_function.py`: Main Lambda handler

## Setup and Deployment

### API Setup

1. Clone the repository
2. Install dependencies:
   ```
   pip install fastapi uvicorn scikit-learn joblib
   ```
3. Deploy the API:
   - For development: `uvicorn app:app --reload`
   - For production: Deploy to a service like Heroku, AWS Elastic Beanstalk, or any platform supporting HTTPS

### Lambda Function Setup

1. Create a new Lambda function in AWS console:
   - Function name: `alexa-movie-recommender`
   - Runtime: Python 3.8+
   - Role: Create a basic Lambda role with logging permissions

2. Upload the Lambda code:
   - Copy the provided Lambda function code
   - Replace `API_ENDPOINT` with your actual API URL
   - If using mock data (for testing), ensure the mock section is uncommented

3. Configure the Lambda trigger:
   - Add an Alexa Skills Kit trigger
   - Enter your Alexa Skill ID when available

### Alexa Skill Setup

1. Create a new skill in the Alexa Developer Console:
   - Skill name: "Movie Recommender"
   - Invocation name: "movie recommender"
   - Choose a custom model
   - Host your own backend

2. Set up the interaction model:
   - Use the provided interaction model JSON
   - Create necessary intents and slots
   - Build the model

3. Configure the endpoint:
   - Select AWS Lambda as the service endpoint type
   - Enter your Lambda function's ARN
   - Save the endpoint

4. Test the skill:
   - Enable testing in Development mode
   - Test using the simulator or an Alexa device

## Testing

### Lambda Testing

Test the Lambda function using test events in the AWS Lambda console:

1. Create test events for different scenarios:
   - LaunchRequest
   - RecommendMovieIntent
   - AMAZON.YesIntent (for more recommendations)
   - AMAZON.NoIntent
   - AMAZON.HelpIntent

2. Sample LaunchRequest test event:
```json
{
  "version": "1.0",
  "session": {
    "new": true,
    "sessionId": "amzn1.echo-api.session.test-session-id",
    "application": {
      "applicationId": "amzn1.ask.skill.your-skill-id"
    },
    "attributes": {},
    "user": {
      "userId": "amzn1.ask.account.test-user-id"
    }
  },
  "context": {
    "System": {
      "application": {
        "applicationId": "amzn1.ask.skill.your-skill-id"
      },
      "user": {
        "userId": "amzn1.ask.account.test-user-id"
      },
      "device": {
        "deviceId": "amzn1.ask.device.test-device-id"
      }
    }
  },
  "request": {
    "type": "LaunchRequest",
    "requestId": "amzn1.echo-api.request.test-request-id",
    "timestamp": "2025-03-09T12:00:00Z",
    "locale": "en-US"
  }
}
```

3. Sample RecommendMovieIntent test event:
```json
{
  "version": "1.0",
  "session": {
    "new": false,
    "sessionId": "amzn1.echo-api.session.test-session-id",
    "application": {
      "applicationId": "amzn1.ask.skill.your-skill-id"
    },
    "attributes": {},
    "user": {
      "userId": "amzn1.ask.account.test-user-id"
    }
  },
  "request": {
    "type": "IntentRequest",
    "requestId": "amzn1.echo-api.request.test-request-id",
    "timestamp": "2025-03-09T12:01:00Z",
    "locale": "en-US",
    "intent": {
      "name": "RecommendMovieIntent",
      "slots": {
        "MovieName": {
          "name": "MovieName",
          "value": "The Matrix"
        }
      }
    }
  }
}
```

### Alexa Skill Testing

Test the Alexa Skill using the Alexa Developer Console:

1. Navigate to the Test tab
2. Use text or voice to interact with the skill
3. Sample conversation flow:
   - User: "Alexa, open movie recommender"
   - Alexa: "Welcome to Movie Recommender. Give me a movie that you like and I'll recommend another one."
   - User: "I like The Matrix"
   - Alexa: "Based on The Matrix, I recommend Inception. Would you like to hear more recommendations?"
   - User: "Yes"
   - Alexa: "Another recommendation is The Terminator. Would you like to hear more?"

## User Interaction Flow

1. **Invoke Skill**: "Alexa, open movie recommender"
2. **Welcome Message**: Alexa greets the user and asks for a movie
3. **Movie Selection**: User mentions a movie they like
4. **Recommendation**: Alexa provides a similar movie recommendation
5. **More Recommendations**: Alexa asks if the user wants more suggestions
6. **Continuing or Ending**: User can request more recommendations or end the session

## Troubleshooting

Common issues and solutions:

1. **Lambda function failing**:
   - Check CloudWatch logs for error messages
   - Verify the function has sufficient permissions
   - Ensure there are no syntax errors in the code

2. **API connection issues**:
   - Verify the API endpoint is publicly accessible via HTTPS
   - Check API endpoint in Lambda function
   - Temporarily use mock data for testing

3. **Alexa not understanding movie names**:
   - Enhance the interaction model with more sample utterances
   - Use AMAZON.Movie slot type to improve recognition

4. **Session attribute issues**:
   - Verify session attributes are properly set and maintained
   - Check for typos in attribute names

## Future Enhancements

Potential improvements to the system:

1. **User Profiles**: Store user preferences between sessions using DynamoDB
2. **Genre Filtering**: Allow users to specify genres they're interested in
3. **Release Date Filters**: Add options for newer or classic films
4. **Integration with Streaming Services**: Show where movies are available to watch
5. **Rating Information**: Include critic or user ratings in recommendations
6. **Voice Recognition Improvements**: Add custom slot types for better movie name recognition
7. **Multimodal Support**: Add visual elements for devices with screens
8. **Internationalization**: Support for additional languages and international film libraries
