from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configure API key
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_movie_recommendation(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a knowledgeable movie expert. Provide detailed movie recommendations with engaging descriptions."},
                {"role": "user", "content": f"Recommend a movie based on this request: {user_input}. Include title, year, director, brief plot, and why you recommend it. Make it conversational and engaging."}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return str(e)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.json['message']
    recommendation = get_movie_recommendation(user_message)
    return jsonify({
        'recommendation': recommendation
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
