import os
import sys
from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError, RateLimitError, APIConnectionError

load_dotenv()

client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

TASKS = {
    "1" : {
        "name" : "Summarize",
        "prompt" : "You are a concize summarizer. Summarize the user text in 3-5 clear bullet points. Focus on the most important information."
    },
    "2" : {
        "name" : "Rewrite",
        "prompt" : "You are a professional editor. Rewrite the user's text in a clear professional tone. Maintain the original meaning but improve the clarity and readability."  
    },
    "3" : {
        "name" : "Key Points",
        "prompt" : "You are an analyst. Extract the key points from user's text as a numbered list. Each point should be one clear sentence."
    },
    "4" : {
        "name" : "Explain",
        "prompt" : "You are a patient teacher. Explain the user's text in simple terms that a non-expert can understand. Use analogies where helpful."
    }
}

def call_llm(system_prompt, user_text) -> dict:
    try:
        response = client.chat.completions.create(
            model = MODEL,
            messages = [
                {"role" : "system", "content" : system_prompt},
                {"role" : "user", "content" : user_text}
            ],
            temperature = 0.7,
            max_tokens = 500
        )
        return {
            "content" : response.choices[0].message.content,
            "token" : response.usage.total_tokens,
            "model" : response.model 
        }
    except AuthenticationError:
        return {"content" : "Invalid API Key, check your .env file.", "token" : 0, "model" : "N/A"}
    except RateLimitError:
        return {"content" : "Rate limit hit, wait a moment and try again.", "token" : 0, "model" : "N/A"}
    except APIConnectionError:
        return {"content" : "Can not connect, check your internet.", "token" : 0, "model" : "N/A"}
    except Exception as e:
        return {"content" : f"Error: {e}", "token" : 0, "model" : "N/A"}
    

def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("OpenAI Api Key is missing.")
        sys.exit(1)
        
    print("Tasks Available:")
    count = 0
    for task in TASKS.values():
        count += 1
        print(f"{count}. {task["name"]}")
    
    choice = input("Enter a task number: ").strip()
    if choice not in TASKS:
        print(choice)
        print("Invalid input. Enter number between 1 to 4 only.")
        sys.exit(1)
    
    task = TASKS[choice]
    print(f"Chosen task is: {task["name"]}")
    
    user_text = input("Paste your test for chosen task here:")
    
    result = call_llm(task["prompt"], user_text)
    print(f"\n{result}")
    
if __name__ == "__main__":
    main()
      

