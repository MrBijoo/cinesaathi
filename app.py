from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
import json

load_dotenv()

app = Flask(__name__)

# Configure API keys
openai.api_key = os.getenv('OPENAI_API_KEY')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

def get_movie_recommendation(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a knowledgeable movie expert. Provide detailed movie recommendations."},
                {"role": "user", "content": f"Recommend a movie based on this request: {user_input}. Include title, year, director, brief plot, and why you recommend it."}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return str(e)

def get_movie_trailer(movie_name):
    try:
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        search_response = youtube.search().list(
            q=f"{movie_name} official trailer",
            part='id,snippet',
            maxResults=1
        ).execute()

        if search_response['items']:
            video_id = search_response['items'][0]['id']['videoId']
            return f"https://www.youtube.com/embed/{video_id}"
        return None
    except Exception as e:
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.json['message']
    
    # Get movie recommendation
    recommendation = get_movie_recommendation(user_message)
    
    # Extract movie title (assuming it's the first line or contains "Title:")
    movie_title = recommendation.split('\n')[0].replace('Title:', '').strip()
    
    # Get trailer
    trailer_url = get_movie_trailer(movie_title)
    
    return jsonify({
        'recommendation': recommendation,
        'trailer_url': trailer_url
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
