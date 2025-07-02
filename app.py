from flask import Flask, request, jsonify
import openai
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["tasdar"]
logs = db["logs"]

@app.route("/")
def index():
    return "TAS.DAR Realiti Aktif"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    user_input = data.get("message", "")
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Anda ialah AI sahabat TAS.DAR."},
                  {"role": "user", "content": user_input}]
    )
    answer = response.choices[0].message["content"]
    logs.insert_one({"message": user_input, "response": answer})
    return jsonify({"reply": answer})

if __name__ == "__main__":
    app.run()
