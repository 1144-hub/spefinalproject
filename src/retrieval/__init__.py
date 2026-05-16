"""
Retrieval Module

This module implements the hybrid retrieval pipeline for the NetRestore RAG system,
combining dense vector search, sparse BM25 keyword search, and cross-encoder reranking
for optimal document retrieval accuracy.

Components:
    - embeddings.py: Embedding model initialization (HuggingFace integration)
    - vector_store.py: ChromaDB vector storage and index management
    - hybrid_search.py: Hybrid retrieval with BM25 + vector + reranking
    - reranker.py: Cross-encoder reranking for result refinement
"""