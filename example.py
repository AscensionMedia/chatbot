from openai import OpenAI


# Load API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")


response = client.chat.completions.create(model="gpt-3.5-turbo",
messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello, chatbot!"}
])
print(response.choices[0].message.content)
