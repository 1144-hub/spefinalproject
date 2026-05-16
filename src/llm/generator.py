import os
from llama_index.llms.groq import Groq
from dotenv import load_dotenv

def get_llm_generator():
    """
    Initializes the LLM used for final synthesis.
    Defaults to Groq's Llama-3 model for 100% free, lightning-fast inference.
    """
    # Load environment variables (like GROQ_API_KEY) from .env file if present
    load_dotenv()
    
    if "GROQ_API_KEY" not in os.environ:
        print("WARNING: GROQ_API_KEY environment variable not set. LLM generation may fail.")
        
    llm = Groq(
        model="llama-3.1-8b-instant",
        temperature=0.0, # 0.0 temperature strongly reduces hallucinations for procedural data
    )
    return llm
