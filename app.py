from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
import traceback

app = Flask(__name__)
CORS(app)

# Load your OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/api/remedies/ai', methods=['GET'])
def get_ai_remedy():
    symptoms = request.args.get('symptoms', '')
    if not symptoms:
        return jsonify({"error": "No symptoms provided"}), 400

    prompt = f"""You are an experienced doctor. A patient has the following symptoms: {symptoms}.
    Suggest appropriate homeopathic and allopathic remedies with dosage or potency where applicable."""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful medical assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200
        )

        remedy = response['choices'][0]['message']['content']
        return jsonify({"remedy": remedy})

    except Exception as e:
        print("❌ AI Exception:", traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return "AI Remedy API running"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
