import os
from flask import Flask, request, jsonify
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get API keys from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
flask_api_key = os.getenv("FLASK_APP_API_KEY")

# Ensure keys are loaded correctly
if not openai_api_key:
    raise ValueError("Missing environment variable: OPENAI_API_KEY")
if not flask_api_key:
    raise ValueError("Missing environment variable: FLASK_APP_API_KEY")

# Set OpenAI API key
openai.api_key = openai_api_key

# Initialize conversation history
conversation_history = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "system", "content": "You are an AI teacher specialized in Python programming."}
]

@app.route("/")
def home():
    """
    Home route to confirm the Flask app is running.
    """
    return "Welcome to the Flask Chatbot App!"

@app.route("/chat", methods=["POST"])
def chat():
    """
    Endpoint to handle chatbot conversations.
    """
    global conversation_history

    # Validate API Key in Authorization Header
    auth_header = request.headers.get("Authorization")
    if not auth_header or auth_header != f"Bearer {flask_api_key}":
        return jsonify({"error": "Unauthorized"}), 401

    # Parse user message from request
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Message is required"}), 400

    user_message = data["message"]

    # Log the user message for debugging purposes
    print(f"User message received: {user_message}")

    # Append user message to conversation history
    conversation_history.append({"role": "user", "content": user_message})

    try:
        # Generate a response using OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation_history
        )
        bot_reply = response["choices"][0]["message"]["content"]

        # Append the bot's reply to conversation history
        conversation_history.append({"role": "assistant", "content": bot_reply})

        return jsonify({"reply": bot_reply})
    except Exception as e:
        # Log any errors for debugging purposes
        print(f"Error during OpenAI API call: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    from waitress import serve
    print("Starting Flask app with Waitress...")
    serve(app, host="0.0.0.0", port=8000)
