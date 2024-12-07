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

user_query = "Write a 3-paragraph story about a dog"

client = OpenAI()
completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": user_query}
    ]
)
result = completion.choices[0].message.content
print(result)