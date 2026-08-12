import os
import sys
from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError, APIConnectionError

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("ERROR: OPENAI_API_KEY not found!")
    print("Copy .env.example to .env and add your key")
    sys.exit(1)
    
client = OpenAI(api_key = api_key)
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

# -- The Call

print("Sending prompt: What is generative AI in one sentence?")

try:
    response = client.chat.completions.create(
        model = MODEL,
        messages=[
            {"role" : "system", "content" : "You are a helpful assistance. Be concise"},
            {"role" : "user", "content" : "What is generative AI in one sentence?"}
        ],
        temperature = 0.7,
        max_tokens = 100 
    )
    
   #  respone + errors
   
    print(f"Response: {response.choices[0].message.content}")
    print(f"Token Used: {response.usage.total_tokens}")
    
except AuthenticationError:
    print("ERROR: Invalid API Key. Check your .env file")
except APIConnectionError:
    print("ERROR: Can not connect, check your internet")
except Exception as e:
    print(f"Unexpected Error: {e}")
