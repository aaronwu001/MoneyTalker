from flask import Flask, jsonify, request
from flask_cors import CORS
import openai
import os
import dotenv
from openai import OpenAI

# Load environment variables from a .env file
dotenv.load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = api_key


app = Flask(__name__)
CORS(app)  # 允許跨域請求

@app.route('/', methods=['GET'])
def test():
    try:
        return jsonify({"message": "This is home."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        

@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    user_query = data.get("query", "")
    
    if not user_query:
        return jsonify({"error": "Query is required"}), 400
    
    try:
        # return jsonify({"response": "hello"}), 200
        client = OpenAI()
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": user_query}
            ]
        )
        result = completion.choices[0].message.content
        return jsonify({"response": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
