"""
LLM (Large Language Model) Module

This module handles LLM integration, prompt engineering, and query orchestration
for the NetRestore RAG system. It manages the generation of procedural responses
based on retrieved SOP context.

Components:
    - generator.py: LLM client initialization (Groq API integration)
    - prompts.py: Chain-of-thought system prompts and QA templates
    - qa_engine.py: Conversational QA engine with memory and query routing
"""