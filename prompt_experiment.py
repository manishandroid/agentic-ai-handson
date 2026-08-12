import os
import sys
import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

SAMPLE_TEXT = """
    Artificial Intelligence has transformed how business operates.
    Companies now use machine learning for everything from customer services chatbots to predictive
    maintenance in manufacturing. However, the rapid adoption of AI has also raised concerns about job
    displacement, algorithmic bias and data privacy. Expert argue that responsible AI development requires
    transparency, fairness and accountability at every stage of the development lifecycle.
""".strip()

total_tokens = 0
total_calls = 0

def call_llm(prompt: str, temperature: float = 0.7) -> tuple[str, int]:
    global total_tokens, total_calls
    start = time.time()
    
    response = client.chat.completions.create(
        model = MODEL,
        messages = [{"role":"user", "content": prompt}],
        temperature = temperature,
        max_tokens = 300
    )
    
    elapsed = time.time() - start
    tokens = response.usage.total_tokens
    total_tokens += tokens
    total_calls += 1
    
    text = response.choices[0].message.content
    print(f"[{tokens} tokens, {elapsed:.1f}s]")
    return text, tokens

def experiment_specificity():
    levels = [
        ("Vague", f"Summarize this:\n{SAMPLE_TEXT}"),
        ("Specific", f"Summarize this text in exactly 3 bullet points:\n{SAMPLE_TEXT}"),
        ("Highly Specific", f"Summarize this text in exactly 3 bullet points, each under 15 words, focusing only on business impact:\n{SAMPLE_TEXT}")
    ]
    
    for label, prompt in levels:
        print(f"\n --- Level: {label} ---")
        print(f"   Prompt: '{prompt.split(chr(10))[0]}'")
        result, _ = call_llm(prompt)
        print(f"Output:\n{result}")

def experiment_persona():
    personas = [
        ("CEO", f"You are briefing a CEO who has 30 seconds. Summarize the key busoness decision from this text:\n{SAMPLE_TEXT}"),
        ("10-year-old", f"Explain this to a curious 10-year-old using simple words and an analogy:\n{SAMPLE_TEXT}"),
        ("Software Engineer", f"Summarize this for a software engineer evaluating AI tools for their team. Focus on technical implication:\n{SAMPLE_TEXT}")
    ]

    for persona, prompt in personas:
        print(f"\n --- Audience: {persona} ---")
        result, _ = call_llm(prompt)
        print(f"\nOutput:\n{result}")
    
def experiment_format():
     
    formats =[
         ("Free Text", f"Summarize this:\n{SAMPLE_TEXT}"),
         ("JSON", f"Summarize this as valid JSON with keys: \"main_point\", \"risks\", \"opprotunities\". Output ONLY the JSON:\n{SAMPLE_TEXT}"),
         ("Markdown Table", f"Summarize this as a markdown table with columns: Theme | Key point | Implication. Include 3 rows:\n{SAMPLE_TEXT}"),
    ]  

    for fmt, prompt in formats:
        print(f"\n --- Format: {fmt} ---")
        result, _ = call_llm(prompt)
        print(f"\nOutput:\n{result}") 
    
def experiment_temperature():
    prompt = f"Write a one-sentence creative tagline for theis technology:\n{SAMPLE_TEXT}"
    temps = [0.0, 0.7, 1.5, 2.0]
    
    for temp in temps:
        result, _ = call_llm(prompt, temp)
        print(f"\nOutput:\n{result}")
           
def main():
    if __name__ == "__main__":
        print("Choose an experiment:\n1. Experiment Specificity\n2. Experiment Persona\n3. Experiment Format\n4. Experiment Temperature")
        experiment = int(input("\nExperiment number: "))
        match experiment:
            case 1: experiment_specificity()
            case 2: experiment_persona()
            case 3: experiment_format()
            case 4: experiment_temperature()
            case _: print("Kindly choose correct experiment, invalid input received!")
        
    
main()
