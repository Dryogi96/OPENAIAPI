from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# Load OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def index():
    return "✅ AI Remedy API is running!"

@app.route('/api/remedies/ai', methods=['GET'])
def get_ai_remedy():
    symptoms = request.args.get('symptoms', '')
    if not symptoms:
        return jsonify({"error": "No symptoms provided"}), 400

    prompt = f"""
    A patient is reporting the following symptoms: {symptoms}.
    Suggest suitable remedies in two formats:
    🏥 Homeopathic Remedy (include name + potency if possible)
    💊 Allopathic Remedy (include name + dosage if possible)
    Keep it simple and clear.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Change to "gpt-4" if preferred
            messages=[
                {"role": "system", "content": "You are a helpful and experienced medical assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        result = response['choices'][0]['message']['content']
        return jsonify({"remedy": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Bind to correct host and port for Render
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
