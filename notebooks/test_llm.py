"""
CI Smoke Test: LLM API Integration
Verifies the Groq API key is valid and the LLM responds.
Jenkins runs this in the 'Integration Test (API Smoke)' stage via:
  timeout 60 python notebooks/test_llm.py
GROQ_API_KEY is injected by Jenkins from its credential store.
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.llm.generator import get_llm_generator


def test_llm_smoke():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("WARNING: GROQ_API_KEY not set — skipping LLM smoke test")
        return

    print("Testing Groq LLM connectivity...")
    llm = get_llm_generator()
    response = llm.complete("Reply with exactly one word: OK")
    assert response.text.strip(), "LLM returned empty response — check API key"
    print(f"✅ LLM smoke test passed. Response: '{response.text.strip()}'")


if __name__ == "__main__":
    test_llm_smoke()
