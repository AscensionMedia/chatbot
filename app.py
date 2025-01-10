from flask import Flask, request, jsonify
from openai import OpenAI

client = OpenAI(api_key="")

app = Flask(__name__)

# Set your OpenAI API Key

# Add a global variable to store conversation history
conversation_history = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "system", "content": "You are an AI teacher specialized in Python programming."}
]

# Define an API Key for authorization
API_KEY = ""

@app.route("/")
def home():
    return "Welcome to the Flask App!"

@app.route("/chat", methods=["POST"])
def chat():
    global conversation_history

    # Log the Authorization header
    auth_header = request.headers.get("Authorization")
    print(f"Authorization header received: {auth_header}")  # Debugging log
    if auth_header != f"Bearer {API_KEY}":
        print("Unauthorized access.")  # Debugging log
        return jsonify({"error": "Unauthorized"}), 401

    # Log the request body
    print(f"Request JSON received: {request.get_json()}")  # Debugging log

    data = request.json
    if not data or "message" not in data:
        return jsonify({"error": "Message is required"}), 400

    user_message = data["message"]
    print(f"User message: {user_message}")  # Debugging log    

    if not data or "message" not in data:
        return jsonify({"error": "Message is required"}), 400

    user_message = data["message"]

    # Append user message to conversation history
    conversation_history.append({"role": "user", "content": user_message})

    try:
        # Generate response from OpenAI
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=conversation_history)
        bot_reply = response.choices[0].message.content

        # Append bot reply to conversation history
        conversation_history.append({"role": "assistant", "content": bot_reply})
        return jsonify({"reply": bot_reply})
    except Exception as e:
        print(f"Error during OpenAI API call: {e}")  # Debugging log
        return jsonify({"error": str(e)}), 500

@app.route("/routes", methods=["GET"])
def list_routes():
    routes = [str(rule) for rule in app.url_map.iter_rules()]
    return jsonify(routes)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
