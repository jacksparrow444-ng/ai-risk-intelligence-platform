import os
from dotenv import load_dotenv
from google import genai

# Load .env file from the parent directory
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)

chat = client.chats.create(
    model="gemini-3.6-flash"
)

response = chat.send_message("Say OK if working")

print(response.text)