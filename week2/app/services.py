from .llm_client import generate

PROMPTS = {
    "summarize": "Summarize the following text concisely in 3-5 bullet points.",
    "rewrite": "Rewrite the following text in a clear, professional tone.",
    "keypoints": "Extract the keypoints from the following text as a numbered list.",
    "explain": "Explain the following concept in simple terms that anyone cam uderstand."
}

def process_task(task, text):
    if task not in PROMPTS:
        raise ValueError(f"Unknown task: {task}, Available: {list(PROMPTS.keys())}")
    
    result = generate(PROMPTS[task], text)
    return {
        "task": task,
        "content": result["content"],
        "tokens_used": result["tokens_used"]
    }

