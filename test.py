from flask import Flask
import openai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Debug: Print loaded API keys (optional; disable in production)
print(f"Loaded OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY')}")
print(f"Loaded FLASK_APP_API_KEY: {os.getenv('FLASK_APP_API_KEY')}")

# Get API keys
openai.api_key = os.getenv("OPENAI_API_KEY")
API_KEY = os.getenv("FLASK_APP_API_KEY")

# Validate API keys
if not openai.api_key or not API_KEY:
    raise ValueError("Missing required environment variables: OPENAI_API_KEY or FLASK_APP_API_KEY")

app = Flask(__name__)

@app.route("/")
def home():
    return "Environment variables are loaded correctly!"

if __name__ == "__main__":
    app.run(debug=True)
