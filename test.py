import openai

# Set your OpenAI API key
openai.api_key = "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"

try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use "gpt-4" if you have access
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, chatbot!"}
        ]
    )
    print(response['choices'][0]['message']['content'])
except Exception as e:
    print({"error": str(e)})
