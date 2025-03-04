import os
import openai
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Get OpenAI API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.json
    prompt = data.get("input", "")
    settings = data.get("settings", {})

    try:
        client = openai.OpenAI(api_key=openai_api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=settings.get("temperature", 0.7),
            top_p=settings.get("top_p", 0.9),
            max_tokens=settings.get("max_tokens", 100),
            frequency_penalty=settings.get("frequency_penalty", 0),
            presence_penalty=settings.get("presence_penalty", 0),
        )

        return jsonify({"response": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
